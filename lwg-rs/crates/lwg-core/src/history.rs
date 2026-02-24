use crate::error::LwgResult;
use chrono::{DateTime, Local};
use serde::{Deserialize, Serialize};
use std::collections::VecDeque;
use std::path::Path;
use tracing::info;

/// 历史记录条目
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HistoryEntry {
    pub id: String,
    pub title: String,
    pub preview: String,
    pub timestamp: DateTime<Local>,
}

/// 历史记录管理器
pub struct HistoryManager {
    history: VecDeque<HistoryEntry>,
    max_entries: usize,
    history_path: std::path::PathBuf,
}

impl HistoryManager {
    /// 创建新的历史记录管理器
    pub fn new(config_dir: impl AsRef<Path>) -> Self {
        let history_path = config_dir.as_ref().join("history.json");

        let mut manager = Self {
            history: VecDeque::new(),
            max_entries: 30,
            history_path,
        };

        if let Err(e) = manager.load() {
            tracing::warn!("Failed to load history: {}", e);
        }

        manager
    }

    /// 加载历史记录
    fn load(&mut self) -> LwgResult<()> {
        if !self.history_path.exists() {
            return Ok(());
        }

        let content = std::fs::read_to_string(&self.history_path)?;
        let entries: Vec<HistoryEntry> = serde_json::from_str(&content)?;

        self.history = entries.into_iter().collect();
        info!("Loaded {} history entries", self.history.len());

        Ok(())
    }

    /// 保存历史记录
    pub fn save(&self) -> LwgResult<()> {
        let entries: Vec<_> = self.history.iter().cloned().collect();
        let content = serde_json::to_string_pretty(&entries)?;
        std::fs::write(&self.history_path, content)?;
        Ok(())
    }

    /// 添加历史记录
    pub fn add(
        &mut self,
        id: impl Into<String>,
        title: impl Into<String>,
        preview: impl Into<String>,
    ) -> LwgResult<()> {
        let entry = HistoryEntry {
            id: id.into(),
            title: title.into(),
            preview: preview.into(),
            timestamp: Local::now(),
        };

        // 去重：如果已存在，先移除旧条目
        self.history.retain(|e| e.id != entry.id);

        // 添加到头部
        self.history.push_front(entry);

        // 限制数量
        while self.history.len() > self.max_entries {
            self.history.pop_back();
        }

        self.save()?;
        Ok(())
    }

    /// 获取所有历史记录
    pub fn list(&self) -> &VecDeque<HistoryEntry> {
        &self.history
    }

    /// 获取最近的一条记录
    pub fn last(&self) -> Option<&HistoryEntry> {
        self.history.front()
    }

    /// 清空历史记录
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
    use tempfile::TempDir;

    #[test]
    fn test_add_and_list() {
        let temp_dir = TempDir::new().unwrap();
        let mut manager = HistoryManager::new(temp_dir.path());

        manager.add("1", "Wallpaper 1", "/path/1.jpg").unwrap();
        manager.add("2", "Wallpaper 2", "/path/2.jpg").unwrap();

        assert_eq!(manager.len(), 2);
        assert_eq!(manager.last().unwrap().id, "2");
    }

    #[test]
    fn test_deduplication() {
        let temp_dir = TempDir::new().unwrap();
        let mut manager = HistoryManager::new(temp_dir.path());

        manager.add("1", "Wallpaper 1", "/path/1.jpg").unwrap();
        manager.add("2", "Wallpaper 2", "/path/2.jpg").unwrap();
        manager
            .add("1", "Wallpaper 1 Updated", "/path/1.jpg")
            .unwrap();

        assert_eq!(manager.len(), 2);
        assert_eq!(manager.last().unwrap().title, "Wallpaper 1 Updated");
    }

    #[test]
    fn test_max_entries() {
        let temp_dir = TempDir::new().unwrap();
        let mut manager = HistoryManager::new(temp_dir.path());

        for i in 0..35 {
            manager
                .add(format!("{}", i), format!("Wallpaper {}", i), "/path.jpg")
                .unwrap();
        }

        assert_eq!(manager.len(), 30);
    }
}
