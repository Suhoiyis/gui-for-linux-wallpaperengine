//! 日志管理器
//! 用于 Tauri GUI 的实时日志系统

use chrono::Local;
use serde::{Deserialize, Serialize};
use std::collections::VecDeque;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{Arc, RwLock};

/// 日志级别
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum LogLevel {
    Debug,
    Info,
    #[serde(rename = "warn")]
    Warning,
    Error,
}

impl LogLevel {
    pub fn as_str(&self) -> &'static str {
        match self {
            LogLevel::Debug => "debug",
            LogLevel::Info => "info",
            LogLevel::Warning => "warn",
            LogLevel::Error => "error",
        }
    }
}

/// 日志来源
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum LogSource {
    Controller,
    Engine,
    GUI,
    Core,
}

impl LogSource {
    pub fn as_str(&self) -> &'static str {
        match self {
            LogSource::Controller => "Controller",
            LogSource::Engine => "Engine",
            LogSource::GUI => "GUI",
            LogSource::Core => "Core",
        }
    }
}

/// 日志条目 - 与前端 LogEntry 类型匹配
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LogEntry {
    pub id: u64,
    pub timestamp: String,
    pub level: LogLevel,
    pub source: LogSource,
    pub message: String,
}

/// 日志管理器
pub struct LogManager {
    logs: Arc<RwLock<VecDeque<LogEntry>>>,
    max_entries: usize,
    next_id: AtomicU64,
    subscribers: Arc<RwLock<Vec<Box<dyn Fn(&LogEntry) + Send + Sync>>>>,
}

impl LogManager {
    /// 创建新的日志管理器
    pub fn new() -> Self {
        Self {
            logs: Arc::new(RwLock::new(VecDeque::with_capacity(200))),
            max_entries: 200,
            next_id: AtomicU64::new(1),
            subscribers: Arc::new(RwLock::new(Vec::new())),
        }
    }

    /// 创建指定最大条目数的日志管理器
    pub fn with_max_entries(max_entries: usize) -> Self {
        Self {
            logs: Arc::new(RwLock::new(VecDeque::with_capacity(max_entries))),
            max_entries,
            next_id: AtomicU64::new(1),
            subscribers: Arc::new(RwLock::new(Vec::new())),
        }
    }

    /// 添加日志条目
    pub fn log(&self, level: LogLevel, source: LogSource, message: &str) {
        let entry = LogEntry {
            id: self.next_id.fetch_add(1, Ordering::Relaxed),
            timestamp: Local::now().format("%H:%M:%S").to_string(),
            level,
            source,
            message: message.to_string(),
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

        // 输出到 stderr (调试用)
        eprintln!(
            "[{}] [{}] [{}] {}",
            entry.timestamp,
            entry.level.as_str(),
            entry.source.as_str(),
            entry.message
        );
    }

    /// 添加 INFO 级别日志
    pub fn info(&self, source: LogSource, message: &str) {
        self.log(LogLevel::Info, source, message);
    }

    /// 添加 DEBUG 级别日志
    pub fn debug(&self, source: LogSource, message: &str) {
        self.log(LogLevel::Debug, source, message);
    }

    /// 添加 WARNING 级别日志
    pub fn warning(&self, source: LogSource, message: &str) {
        self.log(LogLevel::Warning, source, message);
    }

    /// 添加 ERROR 级别日志
    pub fn error(&self, source: LogSource, message: &str) {
        self.log(LogLevel::Error, source, message);
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

    /// 按来源过滤日志
    pub fn get_logs_by_source(&self, source: LogSource) -> Vec<LogEntry> {
        self.logs
            .read()
            .map(|logs| {
                logs.iter()
                    .filter(|e| e.source == source)
                    .cloned()
                    .collect()
            })
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
        self.logs.read().map(|logs| logs.len()).unwrap_or(0)
    }

    /// 检查是否为空
    pub fn is_empty(&self) -> bool {
        self.len() == 0
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
        assert!(!logs[0].timestamp.is_empty());
    }

    #[test]
    fn test_log_filtering() {
        let manager = LogManager::new();
        manager.log(LogLevel::Debug, LogSource::Controller, "Debug 1");
        manager.log(LogLevel::Info, LogSource::Engine, "Info 1");
        manager.log(LogLevel::Warning, LogSource::GUI, "Warning 1");

        assert_eq!(manager.get_logs_by_source(LogSource::GUI).len(), 1);
    }

    #[test]
    fn test_log_limit() {
        let manager = LogManager::new();
        for i in 0..300 {
            manager.log(LogLevel::Info, LogSource::GUI, &format!("Log {}", i));
        }
        assert!(manager.len() <= 200);
    }

    #[test]
    fn test_log_entry_serialization() {
        let entry = LogEntry {
            id: 1,
            timestamp: "10:00:01".to_string(),
            level: LogLevel::Info,
            source: LogSource::GUI,
            message: "Test".to_string(),
        };
        let json = serde_json::to_string(&entry).unwrap();
        assert!(json.contains("\"level\":\"info\""));
        assert!(json.contains("\"source\":\"GUI\""));
    }
}
