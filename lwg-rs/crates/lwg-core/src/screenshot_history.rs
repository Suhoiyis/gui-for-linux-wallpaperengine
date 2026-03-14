//! 截图历史管理器
//!
//! 独立的历史管理器，用于持久化截图记录。
//! 与 PerformanceMonitor 分离，避免阻塞后台性能监控线程。

use crate::error::LwgResult;
use crate::performance::ScreenshotRecord;
use std::collections::VecDeque;
use tracing::info;

/// 截图历史管理器
///
/// 负责截图记录的持久化存储，使用原子写入确保数据安全。
/// 最大保存 10 条记录，超过时移除最旧的记录。
pub struct ScreenshotHistoryManager {
    history: VecDeque<ScreenshotRecord>,
    max_entries: usize,
    history_path: std::path::PathBuf,
}

impl ScreenshotHistoryManager {
    /// 创建新的截图历史管理器
    ///
    /// 自动从 `~/.cache/linux-wallpaperengine-gui/screenshot_history.json` 加载历史记录。
    /// 如果文件不存在或损坏，返回空历史管理器。
    pub fn new() -> LwgResult<Self> {
        let cache_dir = dirs::cache_dir().ok_or_else(|| {
            crate::error::LwgError::ConfigError("Cannot get cache directory".to_string())
        })?;
        let history_dir = cache_dir.join("linux-wallpaperengine-gui");
        std::fs::create_dir_all(&history_dir)?;
        let history_path = history_dir.join("screenshot_history.json");

        let mut manager = Self {
            history: VecDeque::new(),
            max_entries: 10,
            history_path,
        };

        if let Err(e) = manager.load() {
            tracing::warn!("Failed to load screenshot history: {}", e);
        }

        Ok(manager)
    }

    /// 创建用于测试的历史管理器，使用临时目录
    #[cfg(test)]
    pub fn new_for_test() -> LwgResult<Self> {
        use std::sync::atomic::{AtomicU64, Ordering};
        static COUNTER: AtomicU64 = AtomicU64::new(0);
        let id = COUNTER.fetch_add(1, Ordering::SeqCst);
        let temp_dir = std::env::temp_dir().join(format!("lwg-screenshot-history-test-{}", id));
        std::fs::create_dir_all(&temp_dir)?;
        let history_path = temp_dir.join("screenshot_history.json");

        let manager = Self {
            history: VecDeque::new(),
            max_entries: 10,
            history_path,
        };

        Ok(manager)
    }

    /// 加载历史记录
    fn load(&mut self) -> LwgResult<()> {
        if !self.history_path.exists() {
            return Ok(());
        }

        let content = std::fs::read_to_string(&self.history_path)?;

        // 尝试解析 JSON，如果失败则记录警告并返回空历史
        match serde_json::from_str::<Vec<ScreenshotRecord>>(&content) {
            Ok(entries) => {
                self.history = entries.into_iter().collect();
                info!("Loaded {} screenshot history entries", self.history.len());
            }
            Err(e) => {
                tracing::warn!(
                    "Failed to parse screenshot history JSON: {}, starting fresh",
                    e
                );
                // 不返回错误，保持空历史
            }
        }

        Ok(())
    }

    /// 保存历史记录（原子写入）
    ///
    /// 先写入 `.tmp` 文件，然后重命名为目标文件，
    /// 防止写入过程中崩溃导致数据损坏。
    pub fn save(&self) -> LwgResult<()> {
        let entries: Vec<_> = self.history.iter().cloned().collect();
        let content = serde_json::to_string_pretty(&entries)?;
        let tmp_path = self.history_path.with_extension("tmp");

        std::fs::write(&tmp_path, content)?;
        std::fs::rename(&tmp_path, &self.history_path)?;

        Ok(())
    }

    /// 添加截图记录
    ///
    /// 添加到队列头部，超过 10 条时移除最旧的记录。
    /// 添加后自动保存到文件。
    pub fn add(&mut self, record: ScreenshotRecord) -> LwgResult<()> {
        // 添加到头部
        self.history.push_front(record);

        // 限制数量，移除最旧的
        while self.history.len() > self.max_entries {
            self.history.pop_back();
        }

        self.save()?;
        Ok(())
    }

    /// 获取所有截图记录
    ///
    /// 按时间倒序返回（最新的在前）
    pub fn list(&self) -> Vec<ScreenshotRecord> {
        self.history.iter().cloned().collect()
    }

    /// 清空截图历史
    ///
    /// 清空内存中的记录并同步到文件
    pub fn clear(&mut self) -> LwgResult<()> {
        self.history.clear();
        self.save()?;
        Ok(())
    }

    /// 获取历史记录数量
    pub fn len(&self) -> usize {
        self.history.len()
    }

    /// 检查是否为空
    pub fn is_empty(&self) -> bool {
        self.history.is_empty()
    }

    /// 获取最大条目数
    pub fn max_entries(&self) -> usize {
        self.max_entries
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn create_test_record(id: &str) -> ScreenshotRecord {
        ScreenshotRecord {
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
            wp_id: id.to_string(),
            output_path: format!("/path/{}.png", id),
            duration: 10.0,
            max_cpu: 50.0,
            max_mem: 100.0,
        }
    }

    #[test]
    fn test_add_and_list() {
        let mut manager = ScreenshotHistoryManager::new_for_test().unwrap();

        manager.add(create_test_record("1")).unwrap();
        manager.add(create_test_record("2")).unwrap();

        assert_eq!(manager.len(), 2);
        let list = manager.list();
        assert_eq!(list[0].wp_id, "2"); // 最新的在前
        assert_eq!(list[1].wp_id, "1");
    }

    #[test]
    fn test_max_entries() {
        let mut manager = ScreenshotHistoryManager::new_for_test().unwrap();

        for i in 0..15 {
            manager.add(create_test_record(&format!("{}", i))).unwrap();
        }

        assert_eq!(manager.len(), 10);
        let list = manager.list();
        // 最新的 10 条应该保留 (14, 13, 12, ..., 5)
        assert_eq!(list[0].wp_id, "14");
        assert_eq!(list[9].wp_id, "5");
    }

    #[test]
    fn test_clear() {
        let mut manager = ScreenshotHistoryManager::new_for_test().unwrap();

        manager.add(create_test_record("1")).unwrap();
        manager.add(create_test_record("2")).unwrap();
        assert_eq!(manager.len(), 2);

        manager.clear().unwrap();
        assert!(manager.is_empty());
    }

    #[test]
    fn test_save_and_load() {
        let mut manager = ScreenshotHistoryManager::new_for_test().unwrap();

        // 添加记录
        manager.add(create_test_record("test1")).unwrap();
        manager.add(create_test_record("test2")).unwrap();

        // 保存
        manager.save().unwrap();

        // 创建新实例加载
        let path = manager.history_path.clone();
        let mut manager2 = ScreenshotHistoryManager {
            history: VecDeque::new(),
            max_entries: 10,
            history_path: path,
        };
        manager2.load().unwrap();

        assert_eq!(manager2.len(), 2);
        let list = manager2.list();
        assert_eq!(list[0].wp_id, "test2");
    }

    #[test]
    fn test_load_corrupted_json() {
        let manager = ScreenshotHistoryManager::new_for_test().unwrap();
        let path = manager.history_path.clone();

        // 写入无效 JSON
        std::fs::write(&path, "{ invalid json }").unwrap();

        // 加载应该成功但返回空历史
        let mut manager2 = ScreenshotHistoryManager {
            history: VecDeque::new(),
            max_entries: 10,
            history_path: path,
        };
        manager2.load().unwrap();
        assert!(manager2.is_empty());
    }

    #[test]
    fn test_load_missing_file() {
        let mut manager = ScreenshotHistoryManager {
            history: VecDeque::new(),
            max_entries: 10,
            history_path: std::path::PathBuf::from("/nonexistent/path.json"),
        };

        // 加载不存在的文件应该成功
        manager.load().unwrap();
        assert!(manager.is_empty());
    }
}
