use crate::error::{LwgError, LwgResult};
use std::collections::HashSet;
use tracing::info;

/// Manages wallpaper favorites with persistent storage
pub struct FavoriteManager {
    favorites: HashSet<String>,
    favorites_path: std::path::PathBuf,
}

impl FavoriteManager {
    /// Create a new FavoriteManager, loading existing favorites from disk
    pub fn new() -> LwgResult<Self> {
        let data_dir = dirs::data_local_dir()
            .ok_or_else(|| LwgError::ConfigError("Cannot get data directory".to_string()))?
            .join("linux-wallpaperengine-gui");
        std::fs::create_dir_all(&data_dir)?;
        let favorites_path = data_dir.join("favorites.json");

        let mut manager = Self {
            favorites: HashSet::new(),
            favorites_path,
        };

        if let Err(e) = manager.load() {
            tracing::warn!("Failed to load favorites: {}", e);
        }

        Ok(manager)
    }

    #[cfg(test)]
    pub fn new_for_test() -> LwgResult<Self> {
        use std::sync::atomic::{AtomicU64, Ordering};
        static COUNTER: AtomicU64 = AtomicU64::new(0);
        let id = COUNTER.fetch_add(1, Ordering::SeqCst);
        let temp_dir = std::env::temp_dir().join(format!("lwg-favorite-test-{}", id));
        std::fs::create_dir_all(&temp_dir)?;
        let favorites_path = temp_dir.join("favorites.json");

        Ok(Self {
            favorites: HashSet::new(),
            favorites_path,
        })
    }

    /// Load favorites from disk
    fn load(&mut self) -> LwgResult<()> {
        if !self.favorites_path.exists() {
            return Ok(());
        }

        let content = std::fs::read_to_string(&self.favorites_path)?;
        // JSON array -> Vec<String> -> HashSet
        let list: Vec<String> = serde_json::from_str(&content)?;
        self.favorites = list.into_iter().collect();
        info!("Loaded {} favorites", self.favorites.len());

        Ok(())
    }

    /// Save favorites to disk (atomic write)
    pub fn save(&self) -> LwgResult<()> {
        // HashSet -> Vec<String> for JSON serialization
        let list: Vec<&String> = self.favorites.iter().collect();
        let content = serde_json::to_string_pretty(&list)?;
        let tmp_path = self.favorites_path.with_extension("tmp");
        std::fs::write(&tmp_path, content)?;
        std::fs::rename(&tmp_path, &self.favorites_path)?;
        Ok(())
    }

    /// Toggle favorite status for a wallpaper, returns the new state (true = favorited)
    pub fn toggle(&mut self, wallpaper_id: &str) -> LwgResult<bool> {
        let is_now_favorite = if self.favorites.contains(wallpaper_id) {
            self.favorites.remove(wallpaper_id);
            false
        } else {
            self.favorites.insert(wallpaper_id.to_string());
            true
        };
        self.save()?;
        Ok(is_now_favorite)
    }

    /// Check if a wallpaper is favorited
    pub fn is_favorite(&self, wallpaper_id: &str) -> bool {
        self.favorites.contains(wallpaper_id)
    }

    /// Get all favorited wallpaper IDs
    pub fn list(&self) -> Vec<String> {
        self.favorites.iter().cloned().collect()
    }

    /// Get the number of favorites
    pub fn len(&self) -> usize {
        self.favorites.len()
    }

    /// Check if there are no favorites
    pub fn is_empty(&self) -> bool {
        self.favorites.is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_toggle_favorite() {
        let mut manager = FavoriteManager::new_for_test().unwrap();

        // Initially not a favorite
        assert!(!manager.is_favorite("12345"));

        // Toggle on
        let result = manager.toggle("12345").unwrap();
        assert!(result);
        assert!(manager.is_favorite("12345"));

        // Toggle off
        let result = manager.toggle("12345").unwrap();
        assert!(!result);
        assert!(!manager.is_favorite("12345"));
    }

    #[test]
    fn test_list_favorites() {
        let mut manager = FavoriteManager::new_for_test().unwrap();

        assert!(manager.list().is_empty());

        manager.toggle("111").unwrap();
        manager.toggle("222").unwrap();
        manager.toggle("333").unwrap();

        let list = manager.list();
        assert_eq!(list.len(), 3);
        assert!(list.contains(&"111".to_string()));
        assert!(list.contains(&"222".to_string()));
        assert!(list.contains(&"333".to_string()));
    }

    #[test]
    fn test_persistence() {
        let mut manager = FavoriteManager::new_for_test().unwrap();
        let path = manager.favorites_path.clone();

        // Add favorites
        manager.toggle("persist_test_1").unwrap();
        manager.toggle("persist_test_2").unwrap();

        // Verify file exists
        assert!(path.exists());

        // Read file content
        let content = std::fs::read_to_string(&path).unwrap();
        let loaded: Vec<String> = serde_json::from_str(&content).unwrap();
        assert_eq!(loaded.len(), 2);
    }
}
