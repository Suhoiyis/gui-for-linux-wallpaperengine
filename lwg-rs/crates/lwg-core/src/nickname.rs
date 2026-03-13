use crate::error::{LwgError, LwgResult};
use std::collections::HashMap;
use tracing::info;

const MAX_NICKNAME_LENGTH: usize = 100;

pub struct NicknameManager {
    nicknames: HashMap<String, String>,
    nicknames_path: std::path::PathBuf,
}

impl NicknameManager {
    pub fn new() -> LwgResult<Self> {
        let data_dir = dirs::data_local_dir()
            .ok_or_else(|| LwgError::ConfigError("Cannot get data directory".to_string()))?
            .join("linux-wallpaperengine-gui");
        std::fs::create_dir_all(&data_dir)?;
        let nicknames_path = data_dir.join("nicknames.json");

        let mut manager = Self {
            nicknames: HashMap::new(),
            nicknames_path,
        };

        if let Err(e) = manager.load() {
            tracing::warn!("Failed to load nicknames: {}", e);
        }

        Ok(manager)
    }

    #[cfg(test)]
    pub fn new_for_test() -> LwgResult<Self> {
        use std::sync::atomic::{AtomicU64, Ordering};
        static COUNTER: AtomicU64 = AtomicU64::new(0);
        let id = COUNTER.fetch_add(1, Ordering::SeqCst);
        let temp_dir = std::env::temp_dir().join(format!("lwg-nickname-test-{}", id));
        std::fs::create_dir_all(&temp_dir)?;
        let nicknames_path = temp_dir.join("nicknames.json");

        Ok(Self {
            nicknames: HashMap::new(),
            nicknames_path,
        })
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

    fn load(&mut self) -> LwgResult<()> {
        if !self.nicknames_path.exists() {
            return Ok(());
        }

        let content = std::fs::read_to_string(&self.nicknames_path)?;
        self.nicknames = serde_json::from_str(&content)?;
        info!("Loaded {} nicknames", self.nicknames.len());

        Ok(())
    }

    pub fn save(&self) -> LwgResult<()> {
        let content = serde_json::to_string_pretty(&self.nicknames)?;
        let tmp_path = self.nicknames_path.with_extension("tmp");
        std::fs::write(&tmp_path, content)?;
        std::fs::rename(&tmp_path, &self.nicknames_path)?;
        Ok(())
    }

    pub fn set(
        &mut self,
        wallpaper_id: impl Into<String>,
        nickname: impl Into<String>,
    ) -> LwgResult<()> {
        let id = wallpaper_id.into();
        let name = nickname.into();
        let trimmed = name.trim();

        if trimmed.is_empty() {
            self.nicknames.remove(&id);
        } else {
            let truncated = if trimmed.len() > MAX_NICKNAME_LENGTH {
                &trimmed[..MAX_NICKNAME_LENGTH]
            } else {
                trimmed
            };
            self.nicknames.insert(id, truncated.to_string());
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

    #[test]
    fn test_set_and_get() {
        let mut manager = NicknameManager::new_for_test().unwrap();

        manager.set("12345", "My Wallpaper").unwrap();
        assert_eq!(manager.get("12345"), Some(&"My Wallpaper".to_string()));

        manager.set("12345", "").unwrap();
        assert_eq!(manager.get("12345"), None);
    }

    #[test]
    fn test_display_name() {
        let mut manager = NicknameManager::new_for_test().unwrap();

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

    #[test]
    fn test_trim_and_truncate() {
        let mut manager = NicknameManager::new_for_test().unwrap();

        manager.set("12345", "  Hello World  ").unwrap();
        assert_eq!(manager.get("12345"), Some(&"Hello World".to_string()));

        let long_name = "x".repeat(150);
        manager.set("12346", &long_name).unwrap();
        assert_eq!(manager.get("12346").unwrap().len(), MAX_NICKNAME_LENGTH);
    }
}
