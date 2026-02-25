//! 性能监控器

use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use sysinfo::{Pid, ProcessExt, System, SystemExt};

const HISTORY_SIZE: usize = 60;

/// 进程性能数据
#[derive(Debug, Clone)]
pub struct ProcessStats {
    pub pid: i32,
    pub name: String,
    pub cpu: f32,
    pub memory_mb: f32,
    pub threads: i32,
    pub status: String,
}

/// 性能监控数据
#[derive(Debug, Clone)]
pub struct PerformanceStats {
    pub total_cpu: f32,
    pub total_memory_mb: f32,
    pub total_threads: i32,
    pub processes: HashMap<String, ProcessStats>,
}

/// 历史数据
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

use std::collections::VecDeque;

/// 性能监控器
pub struct PerformanceMonitor {
    system: Arc<RwLock<System>>,
    history: Arc<RwLock<HashMap<String, HistoryData>>>,
    cpu_count: i32,
}

impl PerformanceMonitor {
    /// 创建新的性能监控器
    pub fn new() -> Self {
        let mut system = System::new_all();
        system.refresh_all();
        
        let cpu_count = System::physical_core_count(&system).unwrap_or(1) as i32;
        
        let monitor = Self {
            system: Arc::new(RwLock::new(system)),
            history: Arc::new(RwLock::new(HashMap::new())),
            cpu_count,
        };

        // 初始化 frontend 进程监控
        monitor.add_process("frontend", std::process::id() as i32);

        monitor
    }

    /// 添加进程监控
    pub fn add_process(&self, name: &str, pid: i32) {
        if let Ok(mut history) = self.history.write() {
            history.entry(name.to_string()).or_insert_with(HistoryData::new);
        }

        if let Ok(mut system) = self.system.write() {
            system.refresh_process(Pid::from(pid as usize));
        }
    }

    /// 获取性能数据
    pub fn get_stats(&self) -> PerformanceStats {
        // 刷新系统数据
        if let Ok(mut system) = self.system.write() {
            system.refresh_all();
        }

        let mut stats = PerformanceStats {
            total_cpu: 0.0,
            total_memory_mb: 0.0,
            total_threads: 0,
            processes: HashMap::new(),
        };

        // 读取系统数据
        if let Ok(system) = self.system.read() {
            // 获取总 CPU 使用率
            stats.total_cpu = System::global_cpu_usage(&system);

            // 获取总内存使用
            let used_memory = System::used_memory(&system);
            stats.total_memory_mb = (used_memory / 1024 / 1024) as f32;

            // 监控 frontend 进程
            let frontend_pid = std::process::id() as usize;
            if let Some(process) = system.process(Pid::from(frontend_pid)) {
                let cpu = process.cpu_usage();
                let memory_mb = (process.memory() / 1024 / 1024) as f32;
                let threads = process.thread_kind().unwrap_or(1) as i32;
                
                let process_stats = ProcessStats {
                    pid: frontend_pid as i32,
                    name: "frontend".to_string(),
                    cpu,
                    memory_mb,
                    threads,
                    status: format!("{:?}", process.status()),
                };

                stats.processes.insert("frontend".to_string(), process_stats);
                stats.total_threads += threads;

                // 更新历史数据
                if let Ok(mut history) = self.history.write() {
                    if let Some(hist) = history.get_mut("frontend") {
                        hist.add(cpu, memory_mb);
                    }
                }
            }
        }

        stats
    }

    /// 获取 CPU 历史数据
    pub fn get_cpu_history(&self, process_name: &str) -> Option<Vec<f32>> {
        self.history
            .read()
            .ok()
            .and_then(|history| history.get(process_name))
            .map(|hist| hist.cpu.iter().cloned().collect())
    }
}

impl Default for PerformanceMonitor {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_performance_monitor_creation() {
        let monitor = PerformanceMonitor::new();
        assert!(monitor.cpu_count > 0);
    }

    #[test]
    fn test_get_stats() {
        let monitor = PerformanceMonitor::new();
        let stats = monitor.get_stats();
        
        assert!(stats.total_cpu >= 0.0);
        assert!(stats.total_memory_mb >= 0.0);
    }
}
