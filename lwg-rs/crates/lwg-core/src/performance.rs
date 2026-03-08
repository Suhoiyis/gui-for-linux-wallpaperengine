//! 性能监控器

use serde::{Deserialize, Serialize};
use std::collections::{HashMap, VecDeque};
use std::sync::Arc;
use std::time::{Duration, Instant};
use sysinfo::{Pid, ProcessRefreshKind, RefreshKind, System};
use tracing::{debug, warn};

const HISTORY_SIZE: usize = 60;
/// sysinfo 需要至少这个间隔才能正确计算 CPU 使用率
const MIN_CPU_INTERVAL: Duration = Duration::from_millis(200);

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
    pub cpu_cores: usize,
    pub total_memory_gb: f32,
    pub process_count: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct ScreenshotRecord {
    pub timestamp: u64,
    pub wp_id: String,
    pub output_path: String,
    pub duration: f32,
    pub max_cpu: f32,
    pub max_mem: f32,
}

/// Task tracker for monitoring screenshot processes
#[derive(Debug, Clone)]
pub struct TaskTracker {
    pub category: String,
    pub pid: usize,
    pub start_time: Instant,
}

impl TaskTracker {
    pub fn new(category: &str, pid: usize) -> Self {
        Self {
            category: category.to_string(),
            pid,
            start_time: Instant::now(),
        }
    }
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

fn get_gpu_usage() -> Option<f32> {
    if let Ok(content) = std::fs::read_to_string("/sys/class/drm/card0/device/gpu_busy_percent") {
        if let Ok(percent) = content.trim().parse::<f32>() {
            return Some(percent);
        }
    }
    for i in 0..5 {
        let freq_path = format!("/sys/class/drm/card0/device/hwmon/hwmon{}/freq1_input", i);
        if let Ok(content) = std::fs::read_to_string(&freq_path) {
            if let Ok(freq_hz) = content.trim().parse::<f64>() {
                let max_freq = 2500000000.0;
                return Some(((freq_hz / max_freq) * 100.0).min(100.0) as f32);
            }
        }
    }
    None
}

/// 查找真正的 linux-wallpaperengine 进程
/// 使用进程组 (process group) 来查找同组的所有进程
fn find_real_process(pid: usize, timeout_ms: u64) -> Option<usize> {
    // 首先检查进程名
    let comm_path = format!("/proc/{}/comm", pid);
    if let Ok(name) = std::fs::read_to_string(&comm_path) {
        let name = name.trim();
        if name.contains("wallpaper") {
            debug!("Found wallpaper directly: PID={}, name={}", pid, name);
            return Some(pid);
        }
    }
    
    // 获取进程组 ID (PGID)
    // /proc/[pid]/stat format: pid (comm) state ppid pgrp ...
    // Process names can contain spaces, so we need to find the last ')' first
    let pgid = {
        let stat_path = format!("/proc/{}/stat", pid);
        if let Ok(stat) = std::fs::read_to_string(&stat_path) {
            // Find the last ')' to handle process names with spaces
            if let Some(pos) = stat.rfind(')') {
                let remainder = &stat[pos + 2..]; // Skip ") "
                let parts: Vec<&str> = remainder.split_whitespace().collect();
                if parts.len() >= 3 {
                    parts[2].parse::<i32>().unwrap_or(-1) // pgrp is at index 2 after comm
                } else { -1 }
            } else { -1 }
        } else { -1 }
    };
    
    debug!("PID={}, PGID={}", pid, pgid);
    
    // 在整个 /proc 中查找同进程组的 wallpaper 进程
    fn find_in_pgid(target_pgid: i32) -> Option<usize> {
        if let Ok(entries) = std::fs::read_dir("/proc") {
            for entry in entries.flatten() {
                if let Ok(pid_str) = entry.file_name().to_string_lossy().parse::<i32>() {
                    let stat_path = format!("/proc/{}/stat", pid_str);
                    if let Ok(stat) = std::fs::read_to_string(&stat_path) {
                        // Find the last ')' to handle process names with spaces
                        if let Some(pos) = stat.rfind(')') {
                            let remainder = &stat[pos + 2..]; // Skip ") "
                            let parts: Vec<&str> = remainder.split_whitespace().collect();
                            if parts.len() >= 3 {
                                if let Ok(pgrp) = parts[2].parse::<i32>() {
                                    if pgrp == target_pgid {
                                        let comm_path = format!("/proc/{}/comm", pid_str);
                                        if let Ok(comm) = std::fs::read_to_string(&comm_path) {
                                            let comm = comm.trim();
                                            if comm.contains("wallpaper") {
                                                debug!("Found in pgid: PID={}, name={}", pid_str, comm);
                                                return Some(pid_str as usize);
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        None
    }
    
    if pgid > 0 {
        if let Some(found) = find_in_pgid(pgid) { return Some(found); }
    }
    
    // 超时重试
    if timeout_ms > 0 {
        let start = Instant::now();
        while start.elapsed() < Duration::from_millis(timeout_ms) {
            std::thread::sleep(Duration::from_millis(100));
            if pgid > 0 {
                if let Some(found) = find_in_pgid(pgid) {
                    debug!("Found after wait: PID={}", found);
                    return Some(found);
                }
            }
        }
    }

    warn!("No wallpaper found, using PID={}", pid);
    Some(pid)
}

pub struct PerformanceMonitor {
    history: Arc<std::sync::Mutex<HashMap<String, HistoryData>>>,
    screenshot_history: VecDeque<ScreenshotRecord>,
    processes: HashMap<String, usize>,
    cpu_count: usize,
    /// 持久的 System 实例用于正确计算 CPU 使用率
    system: std::sync::Mutex<System>,
    /// 上次刷新时间，用于确保两次刷新之间有足够间隔
    last_refresh: std::sync::Mutex<Instant>,
}

impl PerformanceMonitor {
    pub fn new() -> Self {
        let mut system = System::new_with_specifics(
            RefreshKind::new().with_processes(ProcessRefreshKind::everything()),
        );
        // 关键：启动时做第一次刷新，建立基准
        system.refresh_processes_specifics(ProcessRefreshKind::everything());
        let cpu_count = system.cpus().len().max(1);

        let monitor = Self {
            history: Arc::new(std::sync::Mutex::new(HashMap::new())),
            screenshot_history: VecDeque::with_capacity(10),
            processes: HashMap::new(),
            cpu_count,
            system: std::sync::Mutex::new(system),
            // 设为足够久远，确保第一次 sample 时间差足够
            last_refresh: std::sync::Mutex::new(
                Instant::now() - MIN_CPU_INTERVAL - Duration::from_millis(100),
            ),
        };
        let pid = std::process::id() as usize;
        let mut m = monitor;
        m.register_process("frontend", pid);
        m
    }

    pub fn register_process(&mut self, category: &str, pid: usize) {
        self.processes.insert(category.to_string(), pid);
        if let Ok(mut history) = self.history.lock() {
            history
                .entry(category.to_string())
                .or_insert_with(HistoryData::new);
        }
    }

    pub fn unregister_process(&mut self, category: &str) {
        self.processes.remove(category);
        if let Ok(mut history) = self.history.lock() {
            history.remove(category);
        }
    }

    pub fn get_stats(&self) -> SystemStatsPayload {
        let mut system = System::new_all();
        system.refresh_all();
        let mut total_cpu = 0.0f32;
        let mut total_memory_mb = 0.0f32;
        let mut total_threads = 0i32;
        let mut processes = HashMap::new();

        for (category, &pid) in &self.processes {
            if let Some(process) = system.process(Pid::from(pid)) {
                let cpu = process.cpu_usage();
                let run_time = process.run_time();
                let memory_mb = (process.memory() / 1024 / 1024) as f32;
                let thread_names = get_thread_names(pid as i32);
                let threads = thread_names.len() as i32;
                let name = process.name().to_string();
                let status = format!("{:?}", process.status());
                let cmd = process
                    .cmd()
                    .iter()
                    .map(|s| s.clone())
                    .collect::<Vec<_>>()
                    .join(" ");
                let gpu_usage = if category == "frontend" || category == "backend" {
                    get_gpu_usage()
                } else {
                    None
                };

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

                processes.insert(
                    category.clone(),
                    ProcessStats {
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
                    },
                );
                total_cpu += cpu;
                total_memory_mb += memory_mb;
                total_threads += threads;
            }
        }

        SystemStatsPayload {
            total_cpu,
            total_memory_mb,
            total_threads,
            processes: processes.clone(),
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap_or_default()
                .as_secs(),
            cpu_cores: system.cpus().len(),
            total_memory_gb: system.total_memory() as f32 / 1024.0 / 1024.0 / 1024.0,
            process_count: processes.len(),
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

    /// Start tracking a task (e.g., screenshot process)
    /// This initializes history for the task
    pub fn start_task(&mut self, category: &str, pid: usize) -> TaskTracker {
        // 对于 screenshot 进程，查找真正的 linux-wallpaperengine 子进程
        let real_pid = if category == "screenshot" {
            find_real_process(pid, 500).unwrap_or(pid) // 等待 500ms
        } else {
            pid
        };

        // Register the process and initialize history
        self.processes.insert(category.to_string(), real_pid);
        if let Ok(mut history) = self.history.lock() {
            history.insert(category.to_string(), HistoryData::new());
        }

        // 关键：首次刷新建立基准
        if let Ok(mut sys) = self.system.lock() {
            sys.refresh_processes_specifics(ProcessRefreshKind::everything());
        }
        if let Ok(mut last) = self.last_refresh.lock() {
            *last = Instant::now();
        }

        debug!(
            "start_task: category={}, original_pid={}, real_pid={}",
            category, pid, real_pid
        );

        TaskTracker::new(category, real_pid)
    }

    /// Sample the current CPU/memory usage for a task
    /// Call this periodically during the task execution
    /// NOTE: CPU/MEM monitoring temporarily disabled, only time tracking is active
    pub fn sample_task(&self, _tracker: &TaskTracker) {
        // CPU/MEM 监控暂时禁用，后期修复
        // 只保留时间监控
    }

    /// Stop tracking a task and return statistics
    /// Returns: (duration, max_cpu, max_mem, avg_cpu, avg_mem)
    pub fn stop_task(&self, tracker: &TaskTracker) -> (f32, f32, f32, f32, f32) {
        let duration = tracker.start_time.elapsed().as_secs_f32();

        // Get statistics from history
        let (max_cpu, max_mem, avg_cpu, avg_mem) = if let Ok(mut history) = self.history.lock() {
            if let Some(hist) = history.get(&tracker.category) {
                let cpu_hist: Vec<f32> = hist.cpu.iter().cloned().collect();
                let mem_hist: Vec<f32> = hist.memory_mb.iter().cloned().collect();

                debug!(
                    "stop_task: category={}, cpu_samples={}, mem_samples={}",
                    tracker.category,
                    cpu_hist.len(),
                    mem_hist.len()
                );

                let max_cpu = if !cpu_hist.is_empty() {
                    cpu_hist.iter().cloned().fold(0.0f32, f32::max)
                } else {
                    0.0
                };

                let max_mem = if !mem_hist.is_empty() {
                    mem_hist.iter().cloned().fold(0.0f32, f32::max)
                } else {
                    0.0
                };

                let avg_cpu = if !cpu_hist.is_empty() {
                    cpu_hist.iter().sum::<f32>() / cpu_hist.len() as f32
                } else {
                    0.0
                };

                let avg_mem = if !mem_hist.is_empty() {
                    mem_hist.iter().sum::<f32>() / mem_hist.len() as f32
                } else {
                    0.0
                };

                debug!(
                    "stop_task: max_cpu={}, max_mem={}, avg_cpu={}, avg_mem={}",
                    max_cpu, max_mem, avg_cpu, avg_mem
                );

                // Remove history for this task
                history.remove(&tracker.category);

                (max_cpu, max_mem, avg_cpu, avg_mem)
            } else {
                warn!(
                    "No history for category={}",
                    tracker.category
                );
                (0.0, 0.0, 0.0, 0.0)
            }
        } else {
            warn!("Failed to lock history");
            (0.0, 0.0, 0.0, 0.0)
        };

        (duration, max_cpu, max_mem, avg_cpu, avg_mem)
    }
}

impl Default for PerformanceMonitor {
    fn default() -> Self {
        Self::new()
    }
}
