//! 性能监控器

use serde::{Deserialize, Serialize};
use std::collections::{HashMap, VecDeque};
use std::sync::Arc;
use sysinfo::{Pid, System};

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

    if let Ok(entries) = std::fs::read_dir(&task_dir) {
        for entry in entries.flatten() {
            if let Ok(metadata) = entry.metadata() {
                if metadata.is_dir() {
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

/// Attempts to read GPU usage from sysfs
/// Tries AMD GPU first, falls back to NVIDIA
fn get_gpu_usage() -> Option<f32> {
    // Try AMD GPU: gpu_busy_percent returns 0-100
    if let Ok(content) = std::fs::read_to_string("/sys/class/drm/card0/device/gpu_busy_percent") {
        if let Ok(percent) = content.trim().parse::<f32>() {
            return Some(percent);
        }
    }

    // Try NVIDIA: hwmon freq indicates GPU activity
    for i in 0..5 {
        let freq_path = format!("/sys/class/drm/card0/device/hwmon/hwmon{}/freq1_input", i);
        if let Ok(content) = std::fs::read_to_string(&freq_path) {
            if let Ok(freq_hz) = content.trim().parse::<f64>() {
                let max_freq = 2500000000.0; // 2.5 GHz
                let usage_percent = ((freq_hz / max_freq) * 100.0).min(100.0) as f32;
                return Some(usage_percent);
            }
        }
    }

    None
}

pub struct PerformanceMonitor {
    history: Arc<std::sync::Mutex<HashMap<String, HistoryData>>>,
    screenshot_history: VecDeque<ScreenshotRecord>,
    /// Map of category -> PID for multi-process tracking
    processes: HashMap<String, usize>,
}

impl PerformanceMonitor {
    pub fn new() -> Self {
        let mut monitor = Self {
            history: Arc::new(std::sync::Mutex::new(HashMap::new())),
            screenshot_history: VecDeque::with_capacity(10),
            processes: HashMap::new(),
        };
        let pid = std::process::id() as usize;
        monitor.register_process("frontend", pid);
        monitor
    }

    /// Register a process for monitoring (stores PID and initializes history)
    pub fn register_process(&mut self, category: &str, pid: usize) {
        self.processes.insert(category.to_string(), pid);
        if let Ok(mut history) = self.history.lock() {
            history
                .entry(category.to_string())
                .or_insert_with(HistoryData::new);
        }
    }

    /// Unregister a process from monitoring
    pub fn unregister_process(&mut self, category: &str) {
        self.processes.remove(category);
        if let Ok(mut history) = self.history.lock() {
            history.remove(category);
        }
    }

    /// Get stats for all registered processes
    pub fn get_stats(&self) -> SystemStatsPayload {
        let mut system = System::new_all();
        system.refresh_all();

        let mut total_cpu = 0.0f32;
        let mut total_memory_mb = 0.0f32;
        let mut total_threads = 0i32;
        let mut processes = HashMap::new();

        // Iterate over all registered processes
        for (category, &pid) in &self.processes {
            if let Some(process) = system.process(Pid::from(pid)) {
                let cpu = process.cpu_usage();
                let memory_mb = (process.memory() / 1024 / 1024) as f32;

                // Get thread names first (needed for thread count)
                let thread_names = get_thread_names(pid as i32);
                let threads = thread_names.len() as i32;

                // Get process name and status
                let name = process.name().to_string();
                let status = format!("{:?}", process.status());
                let cmd = process
                    .cmd()
                    .iter()
                    .map(|s| s.clone())
                    .collect::<Vec<_>>()
                    .join(" ");

                // Get GPU usage (only for frontend/backend)
                let gpu_usage = if category == "frontend" || category == "backend" {
                    get_gpu_usage()
                } else {
                    None
                };

                // Update history
                let (cpu_history, mem_history) = {
                    if let Ok(mut history) = self.history.lock() {
                        if let Some(hist) = history.get_mut(category) {
                            hist.add(cpu, memory_mb);
                            (
                                hist.cpu.iter().cloned().collect(),
                                hist.memory_mb.iter().cloned().collect(),
                            )
                        } else {
                            (Vec::new(), Vec::new())
                        }
                    } else {
                        (Vec::new(), Vec::new())
                    }
                };

                let process_stats = ProcessStats {
                    pid: pid as i32,
                    name,
                    cmd,
                    status,
                    cpu,
                    memory_mb,
                    threads,
                    cpu_history,
                    mem_history,
                    thread_names,
                    gpu_usage,
                };

                processes.insert(category.clone(), process_stats);

                total_cpu += cpu;
                total_memory_mb += memory_mb;
                total_threads += threads;
            }
        }

        SystemStatsPayload {
            total_cpu,
            total_memory_mb,
            total_threads,
            processes,
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap_or_default()
                .as_secs(),
        }
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
