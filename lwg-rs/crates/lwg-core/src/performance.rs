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

pub struct PerformanceMonitor {
    history: Arc<std::sync::Mutex<HashMap<String, HistoryData>>>,
}

impl PerformanceMonitor {
    pub fn new() -> Self {
        let mut monitor = Self {
            history: Arc::new(std::sync::Mutex::new(HashMap::new())),
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
                thread_names: Vec::new(),
            });

            if let Ok(mut history) = self.history.lock() {
                if let Some(hist) = history.get_mut("frontend") {
                    hist.add(cpu, memory_mb);
                }
            }
        }

        stats
    }
}

impl Default for PerformanceMonitor {
    fn default() -> Self {
        Self::new()
    }
}
