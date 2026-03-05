use crate::error::LwgResult;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::Path;
use tracing::info;

/// 别名管理器
pub struct NicknameManager {
    nicknames: HashMap<String, String>,
    config_path: std::path::PathBuf,
}

impl NicknameManager {
    /// 创建新的别名管理器
    pub fn new(config_dir: impl AsRef<Path>) -> Self {
        let config_path = config_dir.as_ref().join("nicknames.json");

        let mut manager = Self {
            nicknames: HashMap::new(),
            config_path,
        };

        if let Err(e) = manager.load() {
            tracing::warn!("Failed to load nicknames: {}", e);
        }

        manager
    }

    /// 从配置文件中加载别名（兼容 Python 版的 wallpaperNicknames 字段）
    pub fn load_from_config(&mut self, config: &serde_json::Value) -> LwgResult<()> {
        if let Some(nicknames) = config.get("wallpaperNicknames").and_then(|v| v.as_object()) {
            for (k, v) in nicknames {
                if let Some(nickname) = v.as_str() {
                    self.nicknames.insert(k.clone(), nickname.to_string());
                }
            }
        }
        Ok(())
    }

    /// 加载别名（独立文件）
    fn load(&mut self) -> LwgResult<()> {
        if !self.config_path.exists() {
            return Ok(());
        }

        let content = std::fs::read_to_string(&self.config_path)?;
        self.nicknames = serde_json::from_str(&content)?;
        info!("Loaded {} nicknames", self.nicknames.len());

        Ok(())
    }

    /// 保存别名到文件
    pub fn save(&self) -> LwgResult<()> {
        let content = serde_json::to_string_pretty(&self.nicknames)?;
        std::fs::write(&self.config_path, content)?;
        Ok(())
    }

    /// 设置别名
    pub fn set(
        &mut self,
        wallpaper_id: impl Into<String>,
        nickname: impl Into<String>,
    ) -> LwgResult<()> {
        let id = wallpaper_id.into();
        let name = nickname.into();

        if name.is_empty() {
            self.nicknames.remove(&id);
        } else {
            self.nicknames.insert(id, name);
        }

        self.save()?;
        Ok(())
    }

    /// 获取别名
    pub fn get(&self, wallpaper_id: &str) -> Option<&String> {
        self.nicknames.get(wallpaper_id)
    }

    /// 删除别名
    pub fn remove(&mut self, wallpaper_id: &str) -> LwgResult<bool> {
        let removed = self.nicknames.remove(wallpaper_id).is_some();
        if removed {
            self.save()?;
        }
        Ok(removed)
    }

    /// 获取所有别名
    pub fn list(&self) -> &HashMap<String, String> {
        &self.nicknames
    }

    /// 批量更新别名
    pub fn batch_update(&mut self, updates: HashMap<String, String>) -> LwgResult<()> {
        for (id, name) in updates {
            if name.is_empty() {
                self.nicknames.remove(&id);
            } else {
                self.nicknames.insert(id, name);
            }
        }
        self.save()?;
        Ok(())
    }

    /// 获取带别名的显示名称
    pub fn get_display_name(&self, wallpaper_id: &str, default_title: &str) -> String {
        self.nicknames
            .get(wallpaper_id)
            .cloned()
            .unwrap_or_else(|| default_title.to_string())
    }

    /// 获取别名数量
    pub fn len(&self) -> usize {
        self.nicknames.len()
    }

    /// 检查是否为空
    pub fn is_empty(&self) -> bool {
        self.nicknames.is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn test_set_and_get() {
        let temp_dir = TempDir::new().unwrap();
        let mut manager = NicknameManager::new(temp_dir.path());

        manager.set("12345", "My Wallpaper").unwrap();
        assert_eq!(manager.get("12345"), Some(&"My Wallpaper".to_string()));

        manager.set("12345", "").unwrap();
        assert_eq!(manager.get("12345"), None);
    }

    #[test]
    fn test_display_name() {
        let temp_dir = TempDir::new().unwrap();
        let mut manager = NicknameManager::new(temp_dir.path());

        assert_eq!(
            manager.get_display_name("12345", "Original Title"),
            "Original Title"
        );

        manager.set("12345", "My Nickname").unwrap();
        assert_eq!(
            manager.get_display_name("12345", "Original Title"),
            "My Nickname"
        );
    }
}
