use crate::error::{LwgError, LwgResult};
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, VecDeque};
use std::process;
use tracing::{debug, error, info};

const HISTORY_SIZE: usize = 60;

/// 进程性能数据
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessStats {
    pub pid: i32,
    pub name: String,
    pub cpu: f32,
    pub memory_mb: f32,
    pub threads: i32,
    pub status: String,
}

/// 性能监控数据
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PerformanceStats {
    pub total_cpu: f32,
    pub total_memory_mb: f32,
    pub total_threads: i32,
    pub processes: HashMap<String, ProcessStats>,
    pub history: HashMap<String, HistoryData>,
}

/// 历史数据
#[derive(Debug, Clone, Serialize, Deserialize)]
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

/// 性能监控器
pub struct PerformanceMonitor {
    processes: HashMap<String, i32>,
    history: HashMap<String, HistoryData>,
    cpu_count: i32,
}

impl PerformanceMonitor {
    /// 创建新的性能监控器
    pub fn new() -> Self {
        let cpu_count = num_cpus::get() as i32;
        let mut monitor = Self {
            processes: HashMap::new(),
            history: HashMap::new(),
            cpu_count,
        };
        
        // 添加 frontend 进程（当前进程）
        let pid = process::id() as i32;
        monitor.processes.insert("frontend".to_string(), pid);
        monitor.init_history("frontend");
        
        monitor
    }

    /// 初始化历史数据
    fn init_history(&mut self, category: &str) {
        self.history.entry(category.to_string()).or_insert_with(HistoryData::new);
    }

    /// 获取性能数据
    pub fn get_stats(&mut self) -> PerformanceStats {
        let mut stats = PerformanceStats {
            total_cpu: 0.0,
            total_memory_mb: 0.0,
            total_threads: 0,
            processes: HashMap::new(),
            history: HashMap::new(),
        };

        // 简化实现：返回示例数据
        // TODO: 实现真实的进程监控
        
        for (category, &pid) in &self.processes {
            let process_stats = ProcessStats {
                pid,
                name: category.clone(),
                cpu: 5.0,  // 示例数据
                memory_mb: 50.0,  // 示例数据
                threads: 4,
                status: "running".to_string(),
            };

            stats.total_cpu += process_stats.cpu;
            stats.total_memory_mb += process_stats.memory_mb;
            stats.total_threads += process_stats.threads;
            stats.processes.insert(category.clone(), process_stats);

            // 更新历史数据
            if let Some(history) = self.history.get_mut(category) {
                history.add(5.0, 50.0);
                stats.history.insert(category.clone(), history.clone());
            }
        }

        stats
    }

    /// 添加进程
    pub fn add_process(&mut self, category: &str, pid: i32) {
        self.processes.insert(category.to_string(), pid);
        self.init_history(category);
        debug!("Added process {} with PID {}", category, pid);
    }

    /// 移除进程
    pub fn remove_process(&mut self, category: &str) {
        self.processes.remove(category);
        debug!("Removed process {}", category);
    }

    /// 获取 CPU 历史数据
    pub fn get_cpu_history(&self, category: &str) -> Option<&VecDeque<f32>> {
        self.history.get(category).map(|h| &h.cpu)
    }

    /// 获取内存历史数据
    pub fn get_memory_history(&self, category: &str) -> Option<&VecDeque<f32>> {
        self.history.get(category).map(|h| &h.memory_mb)
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
        assert!(monitor.processes.contains_key("frontend"));
    }

    #[test]
    fn test_get_stats() {
        let mut monitor = PerformanceMonitor::new();
        let stats = monitor.get_stats();
        assert!(stats.total_cpu >= 0.0);
        assert!(stats.total_memory_mb >= 0.0);
    }

    #[test]
    fn test_history_data() {
        let mut history = HistoryData::new();
        for i in 0..70 {
            history.add(i as f32, i as f32 * 2.0);
        }
        assert_eq!(history.cpu.len(), HISTORY_SIZE);
        assert_eq!(history.memory_mb.len(), HISTORY_SIZE);
    }
}
