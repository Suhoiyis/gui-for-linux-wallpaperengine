//! 性能监控器

use std::collections::{HashMap, VecDeque};
use std::sync::Arc;
use sysinfo::{Pid, System};
use serde::{Deserialize, Serialize};

const HISTORY_SIZE: usize = 60;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessStats {
    pub pid: i32,
    pub name: String,
    pub cmd: String,
    pub status: String,
    pub cpu: f32,
    pub memory_mb: f32,
    pub threads: i32,
    pub cpu_history: Vec<f32>,
    pub mem_history: Vec<f32>,
    pub thread_names: Vec<String>,
    pub gpu_usage: Option<f32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemStatsPayload {
    pub total_cpu: f32,
    pub total_memory_mb: f32,
    pub total_threads: i32,
    pub processes: HashMap<String, ProcessStats>,
    pub timestamp: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScreenshotRecord {
    pub timestamp: u64,
    pub wp_id: String,
    pub output_path: String,
    pub duration: f32,
    pub max_cpu: f32,
    pub max_mem: f32,
}

#[derive(Debug, Clone)]
pub struct HistoryData {
    pub cpu: VecDeque<f32>,
    pub memory_mb: VecDeque<f32>,
}

impl HistoryData {
    pub fn new() -> Self {
        Self {
            cpu: VecDeque::with_capacity(HISTORY_SIZE),
            memory_mb: VecDeque::with_capacity(HISTORY_SIZE),
        }
    }

    pub fn add(&mut self, cpu: f32, memory_mb: f32) {
        if self.cpu.len() >= HISTORY_SIZE {
            self.cpu.pop_front();
            self.memory_mb.pop_front();
        }
        self.cpu.push_back(cpu);
        self.memory_mb.push_back(memory_mb);
    }
}

impl Default for HistoryData {
    fn default() -> Self {
        Self::new()
    }
}

/// Extracts thread names from /proc/{pid}/task/{tid}/comm
fn get_thread_names(pid: i32) -> Vec<String> {
    let mut names = Vec::new();
    let task_dir = format!("/proc/{}/task", pid);
    
    // Try to read the task directory
    if let Ok(entries) = std::fs::read_dir(&task_dir) {
        for entry in entries.flatten() {
            // For each TID (thread ID)
            if let Ok(metadata) = entry.metadata() {
                if metadata.is_dir() {
                    // Try to read the comm file for this thread
                    if let Ok(filename) = entry.file_name().into_string() {
                        let comm_path = format!("{}/{}/comm", task_dir, filename);
                        if let Ok(comm_content) = std::fs::read_to_string(&comm_path) {
                            names.push(comm_content.trim().to_string());
                        }
                    }
                }
            }
        }
    }
    
    names
}


pub struct PerformanceMonitor {
    history: Arc<std::sync::Mutex<HashMap<String, HistoryData>>>,
    screenshot_history: VecDeque<ScreenshotRecord>,
}

impl PerformanceMonitor {
    pub fn new() -> Self {
        let mut monitor = Self {
            history: Arc::new(std::sync::Mutex::new(HashMap::new())),
            screenshot_history: VecDeque::with_capacity(10),
        };
        let pid = std::process::id() as usize;
        monitor.add_process("frontend", pid);
        monitor
    }

    pub fn add_process(&self, name: &str, pid: usize) {
        if let Ok(mut history) = self.history.lock() {
            history.entry(name.to_string()).or_insert_with(HistoryData::new);
        }
    }

    pub fn get_stats(&self) -> SystemStatsPayload {
        let mut system = System::new_all();
        system.refresh_all();

        let mut stats = SystemStatsPayload {
            total_cpu: system.cpus().first().map(|c| c.cpu_usage()).unwrap_or(0.0),
            total_memory_mb: (system.used_memory() / 1024 / 1024) as f32,
            total_threads: 0,
            processes: HashMap::new(),
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap_or_default()
                .as_secs(),
        };

        let frontend_pid = std::process::id() as usize;
        if let Some(process) = system.process(Pid::from(frontend_pid)) {
            let cpu = process.cpu_usage();
            let memory_mb = (process.memory() / 1024 / 1024) as f32;
            
            stats.processes.insert("frontend".to_string(), ProcessStats {
                pid: frontend_pid as i32,
                name: "frontend".to_string(),
                cmd: String::new(),
                status: "Running".to_string(),
                cpu,
                memory_mb,
                threads: 0,
                cpu_history: Vec::new(),
                mem_history: Vec::new(),
                thread_names: get_thread_names(frontend_pid as i32),
                gpu_usage: get_gpu_usage(),
            });

            if let Ok(mut history) = self.history.lock() {
                if let Some(hist) = history.get_mut("frontend") {
                    hist.add(cpu, memory_mb);
                }
            }
        }

        stats
    }

    pub fn add_screenshot_history(&mut self, record: ScreenshotRecord) {
        if self.screenshot_history.len() >= 10 {
            self.screenshot_history.pop_front();
        }
        self.screenshot_history.push_back(record);
    }

    pub fn get_screenshot_history(&self) -> Vec<ScreenshotRecord> {
        self.screenshot_history.iter().cloned().collect()
    }

    pub fn clear_screenshot_history(&mut self) {
        self.screenshot_history.clear();
    }
}

impl Default for PerformanceMonitor {
    fn default() -> Self {
        Self::new()
    }
}

/// Attempts to read GPU usage from sysfs
/// Tries AMD GPU first (/sys/class/drm/card0/device/gpu_busy_percent)
/// Falls back to NVIDIA frequency check (/sys/class/drm/card0/device/hwmon/hwmonX/freq1_input)
/// Returns None silently if GPU files are not accessible
fn get_gpu_usage() -> Option<f32> {
    // Try AMD GPU: gpu_busy_percent returns 0-100
    if let Ok(content) = std::fs::read_to_string("/sys/class/drm/card0/device/gpu_busy_percent") {
        if let Ok(percent) = content.trim().parse::<f32>() {
            return Some(percent);
        }
    }

    // Try NVIDIA: hwmon freq indicates GPU activity (frequency in Hz)
    // Attempt multiple hwmon indices since they can vary
    for i in 0..5 {
        let freq_path = format!("/sys/class/drm/card0/device/hwmon/hwmon{}/freq1_input", i);
        if let Ok(content) = std::fs::read_to_string(&freq_path) {
            if let Ok(freq_hz) = content.trim().parse::<f64>() {
                // Normalize frequency to percentage (assuming max ~2.5 GHz typical)
                // This is a rough heuristic; actual max varies by GPU
                let max_freq = 2500000000.0; // 2.5 GHz in Hz
                let usage_percent = ((freq_hz / max_freq) * 100.0).min(100.0) as f32;
                return Some(usage_percent);
            }
        }
    }

    // GPU files not accessible, return None silently
    None
}
