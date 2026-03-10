use crate::error::{LwgError, LwgResult};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::PathBuf;
use tracing::{debug, info};

/// Runtime state (persisted to state.json)
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct AppState {
    pub last_wallpaper: Option<String>,
    pub last_screen: Option<String>,
    pub active_monitors: HashMap<String, String>, // Persisted for multi-monitor support
}

impl Default for AppState {
    fn default() -> Self {
        Self {
            last_wallpaper: None,
            last_screen: None,
            active_monitors: HashMap::new(),
        }
    }
}

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
            AppState::default()
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



    pub fn get_active_monitors(&self) -> &HashMap<String, String> {
        &self.state.active_monitors
    }

    pub fn set_active_monitors(&mut self, monitors: HashMap<String, String>) -> LwgResult<()> {
        self.state.active_monitors = monitors;
        debug!("Active monitors updated");
        Ok(())
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
            state: AppState::default(),
            state_path,
        }
    }

    #[test]
    fn test_appstate_default() {
        let state = AppState::default();
        assert!(state.last_wallpaper.is_none());
        assert!(state.last_screen.is_none());
        assert!(state.active_monitors.is_empty());
    }

    #[test]
    fn test_appstate_serialize_deserialize() {
        let mut state = AppState {
            last_wallpaper: Some("wallpaper_123".to_string()),
            last_screen: Some("HDMI-1".to_string()),
            active_monitors: HashMap::new(),
        };
        state
            .active_monitors
            .insert("DP-1".to_string(), "1920x1080".to_string());

        let json = serde_json::to_string(&state).expect("Failed to serialize");
        let deserialized: AppState = serde_json::from_str(&json).expect("Failed to deserialize");

        assert_eq!(
            deserialized.last_wallpaper,
            Some("wallpaper_123".to_string())
        );
        assert_eq!(deserialized.last_screen, Some("HDMI-1".to_string()));
        // active_monitors should be preserved after serialization
        assert_eq!(
            deserialized.active_monitors.get("DP-1"),
            Some(&"1920x1080".to_string())
        );


    }

    #[test]
    fn test_appstate_active_monitors_serialized() {
        let mut state = AppState::default();
        state
            .active_monitors
            .insert("DP-1".to_string(), "12345".to_string());

        let json = serde_json::to_string_pretty(&state).expect("Failed to serialize");

        // Verify active_monitors IS in the JSON (for multi-monitor support)
        assert!(json.contains("activeMonitors"));
        assert!(json.contains("DP-1"));
    }


    #[test]
    fn test_statemanager_save_creates_file() {
        let temp_dir = TempDir::new().expect("Failed to create temp dir");
        let mut manager = create_test_state_manager(&temp_dir);

        manager.state.last_wallpaper = Some("test_wallpaper".to_string());
        manager.save().expect("Failed to save state");

        assert!(manager.state_path.exists());
        let content = fs::read_to_string(&manager.state_path).expect("Failed to read file");
        assert!(content.contains("test_wallpaper"));
    }

    #[test]
    fn test_statemanager_get_set_active_monitors() {
        let temp_dir = TempDir::new().expect("Failed to create temp dir");
        let mut manager = create_test_state_manager(&temp_dir);

        let mut monitors = HashMap::new();
        monitors.insert("DP-1".to_string(), "1920x1080".to_string());

        manager
            .set_active_monitors(monitors.clone())
            .expect("Failed to set monitors");

        assert_eq!(manager.get_active_monitors(), &monitors);
    }

    #[test]
    fn test_statemanager_state_mut() {
        let temp_dir = TempDir::new().expect("Failed to create temp dir");
        let mut manager = create_test_state_manager(&temp_dir);

        {
            let state = manager.state_mut();
            state.last_wallpaper = Some("mutated".to_string());
        }

        assert_eq!(manager.state().last_wallpaper, Some("mutated".to_string()));
    }

    #[test]
    fn test_statemanager_camelcase_serialization() {
        let state = AppState {
            last_wallpaper: Some("wp".to_string()),
            last_screen: Some("screen".to_string()),
            active_monitors: HashMap::new(),
        };

        let json = serde_json::to_string(&state).expect("Failed to serialize");

        // Verify camelCase keys are used
        assert!(json.contains("lastWallpaper"));
        assert!(json.contains("lastScreen"));
    }

    #[test]
    fn test_statemanager_default_impl() {
        let _manager = StateManager::default();
        // Just ensure it doesn't panic
    }
}
