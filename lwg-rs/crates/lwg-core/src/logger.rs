//! 日志管理器
//! 审计报告 Task 1.7-1.8: LogManager 实现

use std::collections::VecDeque;
use std::sync::{Arc, RwLock};

/// 日志级别
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LogLevel {
    Debug,
    Info,
    Warning,
    Error,
}

impl LogLevel {
    fn as_str(&self) -> &'static str {
        match self {
            LogLevel::Debug => "DEBUG",
            LogLevel::Info => "INFO",
            LogLevel::Warning => "WARNING",
            LogLevel::Error => "ERROR",
        }
    }
}

/// 日志来源
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LogSource {
    Controller,
    Engine,
    GUI,
}

impl LogSource {
    fn as_str(&self) -> &'static str {
        match self {
            LogSource::Controller => "Controller",
            LogSource::Engine => "Engine",
            LogSource::GUI => "GUI",
        }
    }
}

/// 日志条目
#[derive(Debug, Clone)]
pub struct LogEntry {
    pub level: LogLevel,
    pub source: LogSource,
    pub message: String,
    pub timestamp: u64,
}

/// 日志管理器
pub struct LogManager {
    logs: Arc<RwLock<VecDeque<LogEntry>>>,
    max_entries: usize,
    subscribers: Arc<RwLock<Vec<Box<dyn Fn(&LogEntry) + Send + Sync>>>>,
}

impl LogManager {
    /// 创建新的日志管理器
    pub fn new() -> Self {
        Self {
            logs: Arc::new(RwLock::new(VecDeque::with_capacity(500))),
            max_entries: 500,
            subscribers: Arc::new(RwLock::new(Vec::new())),
        }
    }

    /// 添加日志条目
    pub fn log(&self, level: LogLevel, source: LogSource, message: &str) {
        let entry = LogEntry {
            level,
            source,
            message: message.to_string(),
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap_or_default()
                .as_millis() as u64,
        };

        // 写入日志
        if let Ok(mut logs) = self.logs.write() {
            logs.push_back(entry.clone());
            
            // 限制日志数量
            while logs.len() > self.max_entries {
                logs.pop_front();
            }
        }

        // 通知订阅者
        if let Ok(subscribers) = self.subscribers.read() {
            for callback in subscribers.iter() {
                callback(&entry);
            }
        }

        // 输出到 stderr
        eprintln!(
            "[{}] [{}] [{}] {}",
            entry.level.as_str(),
            entry.source.as_str(),
            entry.timestamp,
            entry.message
        );
    }

    /// 添加日志订阅者（回调函数）
    pub fn subscribe<F>(&self, callback: F)
    where
        F: Fn(&LogEntry) + Send + Sync + 'static,
    {
        if let Ok(mut subscribers) = self.subscribers.write() {
            subscribers.push(Box::new(callback));
        }
    }

    /// 获取所有日志
    pub fn get_logs(&self) -> Vec<LogEntry> {
        self.logs
            .read()
            .map(|logs| logs.iter().cloned().collect())
            .unwrap_or_default()
    }

    /// 按级别过滤日志
    pub fn get_logs_by_level(&self, level: LogLevel) -> Vec<LogEntry> {
        self.logs
            .read()
            .map(|logs| logs.iter().filter(|e| e.level == level).cloned().collect())
            .unwrap_or_default()
    }

    /// 按来源过滤日志
    pub fn get_logs_by_source(&self, source: LogSource) -> Vec<LogEntry> {
        self.logs
            .read()
            .map(|logs| logs.iter().filter(|e| e.source == source).cloned().collect())
            .unwrap_or_default()
    }

    /// 清空日志
    pub fn clear(&self) {
        if let Ok(mut logs) = self.logs.write() {
            logs.clear();
        }
    }

    /// 获取日志数量
    pub fn len(&self) -> usize {
        self.logs
            .read()
            .map(|logs| logs.len())
            .unwrap_or(0)
    }
}

impl Default for LogManager {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_log_manager_creation() {
        let manager = LogManager::new();
        assert_eq!(manager.len(), 0);
    }

    #[test]
    fn test_log_entry() {
        let manager = LogManager::new();
        manager.log(LogLevel::Info, LogSource::GUI, "Test message");
        assert_eq!(manager.len(), 1);
        
        let logs = manager.get_logs();
        assert_eq!(logs[0].level, LogLevel::Info);
        assert_eq!(logs[0].source, LogSource::GUI);
    }

    #[test]
    fn test_log_filtering() {
        let manager = LogManager::new();
        manager.log(LogLevel::Debug, LogSource::Controller, "Debug 1");
        manager.log(LogLevel::Info, LogSource::Engine, "Info 1");
        manager.log(LogLevel::Warning, LogSource::GUI, "Warning 1");
        
        assert_eq!(manager.get_logs_by_level(LogLevel::Info).len(), 1);
        assert_eq!(manager.get_logs_by_source(LogSource::GUI).len(), 1);
    }

    #[test]
    fn test_log_limit() {
        let manager = LogManager::new();
        for i in 0..600 {
            manager.log(LogLevel::Info, LogSource::GUI, &format!("Log {}", i));
        }
        assert!(manager.len() <= 500);
    }
}
