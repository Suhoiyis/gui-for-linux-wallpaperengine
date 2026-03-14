use crate::error::{LwgError, LwgResult};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::PathBuf;
use tracing::{debug, info};

/// Represents an active wallpaper on a screen
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct ActiveWallpaper {
    pub wallpaper_id: String,
    pub is_playing: bool,
}

impl ActiveWallpaper {
    pub fn new(wallpaper_id: impl Into<String>) -> Self {
        Self {
            wallpaper_id: wallpaper_id.into(),
            is_playing: true,
        }
    }
}

/// Runtime state - direct mapping of screen -> active wallpaper
pub type AppState = HashMap<String, ActiveWallpaper>;

/// State manager for runtime state persistence
pub struct StateManager {
    pub state: AppState,
    state_path: PathBuf,
}

impl StateManager {
    pub fn new() -> LwgResult<Self> {
        let state_dir = dirs::state_dir()
            .ok_or_else(|| LwgError::ConfigError("Cannot get state directory".to_string()))?
            .join("linux-wallpaperengine-gui");

        std::fs::create_dir_all(&state_dir)?;
        let state_path = state_dir.join("state.json");

        let state = if state_path.exists() {
            let content = std::fs::read_to_string(&state_path)?;
            serde_json::from_str(&content).unwrap_or_default()
        } else {
            AppState::new()
        };

        let manager = Self { state, state_path };
        manager.save()?;
        info!("StateManager initialized at: {:?}", manager.state_path);
        Ok(manager)
    }

    pub fn save(&self) -> LwgResult<()> {
        let json = serde_json::to_string_pretty(&self.state)?;
        let tmp_path = self.state_path.with_extension("tmp");

        std::fs::write(&tmp_path, json)?;
        std::fs::rename(&tmp_path, &self.state_path)?;

        debug!("State saved: {:?}", self.state_path);
        Ok(())
    }

    pub fn get(&self, screen: &str) -> Option<&ActiveWallpaper> {
        self.state.get(screen)
    }

    pub fn insert(&mut self, screen: impl Into<String>, wallpaper: ActiveWallpaper) {
        self.state.insert(screen.into(), wallpaper);
    }

    pub fn remove(&mut self, screen: &str) -> Option<ActiveWallpaper> {
        self.state.remove(screen)
    }

    pub fn is_empty(&self) -> bool {
        self.state.is_empty()
    }

    pub fn iter(&self) -> impl Iterator<Item = (&String, &ActiveWallpaper)> {
        self.state.iter()
    }

    pub fn state_mut(&mut self) -> &mut AppState {
        &mut self.state
    }

    pub fn state(&self) -> &AppState {
        &self.state
    }
}

impl Default for StateManager {
    fn default() -> Self {
        Self::new().expect("Failed to create default StateManager")
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    fn create_test_state_manager(temp_dir: &TempDir) -> StateManager {
        let state_path = temp_dir.path().join("state.json");
        StateManager {
            state: AppState::new(),
            state_path,
        }
    }

    #[test]
    fn test_appstate_default() {
        let state = AppState::new();
        assert!(state.is_empty());
    }

    #[test]
    fn test_appstate_serialize_deserialize() {
        let mut state = AppState::new();
        state.insert("DP-1".to_string(), ActiveWallpaper::new("1920x1080"));
        state.insert("HDMI-1".to_string(), ActiveWallpaper::new("wallpaper_123"));

        let json = serde_json::to_string(&state).expect("Failed to serialize");
        let deserialized: AppState = serde_json::from_str(&json).expect("Failed to deserialize");

        assert_eq!(deserialized.len(), 2);

        let aw = deserialized.get("DP-1").expect("DP-1 should exist");
        assert_eq!(aw.wallpaper_id, "1920x1080");
        assert!(aw.is_playing);

        let aw2 = deserialized.get("HDMI-1").expect("HDMI-1 should exist");
        assert_eq!(aw2.wallpaper_id, "wallpaper_123");
    }

    #[test]
    fn test_statemanager_save_creates_file() {
        let temp_dir = TempDir::new().expect("Failed to create temp dir");
        let mut manager = create_test_state_manager(&temp_dir);

        manager.insert("HDMI-1", ActiveWallpaper::new("test_wallpaper"));
        manager.save().expect("Failed to save state");

        assert!(manager.state_path.exists());
        let content = fs::read_to_string(&manager.state_path).expect("Failed to read file");
        assert!(content.contains("test_wallpaper"));
        assert!(content.contains("HDMI-1"));
    }

    #[test]
    fn test_statemanager_get_set() {
        let temp_dir = TempDir::new().expect("Failed to create temp dir");
        let mut manager = create_test_state_manager(&temp_dir);

        manager.insert("DP-1", ActiveWallpaper::new("1920x1080"));

        let aw = manager.get("DP-1").expect("DP-1 should exist");
        assert_eq!(aw.wallpaper_id, "1920x1080");
    }

    #[test]
    fn test_statemanager_remove() {
        let temp_dir = TempDir::new().expect("Failed to create temp dir");
        let mut manager = create_test_state_manager(&temp_dir);

        manager.insert("DP-1", ActiveWallpaper::new("test"));
        assert!(!manager.is_empty());

        manager.remove("DP-1");
        assert!(manager.is_empty());
    }

    #[test]
    fn test_statemanager_default_impl() {
        let _manager = StateManager::default();
        // Just ensure it doesn't panic
    }
}
