use crate::error::{LwgError, LwgResult};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use tracing::{debug, info, warn};

/// 应用配置结构体
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct AppConfig {
    pub fps: u32,
    pub volume: u32,
    pub scaling: String,
    #[serde(rename = "muteAudio")]
    pub silence: bool,
    pub no_fullscreen_pause: bool,
    pub disable_mouse: bool,
    #[serde(rename = "noAutomute")]
    pub no_auto_mute: bool,
    pub no_audio_processing: bool,
    pub disable_parallax: bool,
    pub disable_particles: bool,
    pub clamping: String,
    pub last_wallpaper: Option<String>,
    pub last_screen: Option<String>,
    pub wallpaper_properties: HashMap<String, serde_json::Value>,
    pub screenshot_delay: u32,
    pub screenshot_res: String,
    pub prefer_xvfb: bool,
    #[serde(alias = "active_monitors")]
    pub active_monitors: HashMap<String, String>,
    pub cycle_enabled: bool,
    pub cycle_interval: u32,
    pub cycle_order: String,
    pub assets_path: Option<String>,
    pub workshop_path: Option<String>,
    #[serde(alias = "wayland_only_active")]
    pub wayland_only_active: bool,
    #[serde(alias = "wayland_ignore_appids")]
    pub wayland_ignore_appids: String,
    #[serde(alias = "compact_mode")]
    pub compact_mode: bool,
    pub wallpaper_nicknames: HashMap<String, String>,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            fps: 30,
            volume: 0,
            scaling: "default".to_string(),
            silence: true,
            no_fullscreen_pause: false,
            disable_mouse: false,
            no_auto_mute: false,
            no_audio_processing: false,
            disable_parallax: false,
            disable_particles: false,
            clamping: "clamp".to_string(),
            last_wallpaper: None,
            last_screen: None,
            wallpaper_properties: HashMap::new(),
            screenshot_delay: 20,
            screenshot_res: "3840x2160".to_string(),
            prefer_xvfb: true,
            active_monitors: HashMap::new(),
            cycle_enabled: false,
            cycle_interval: 15,
            cycle_order: "random".to_string(),
            assets_path: None,
            workshop_path: None,
            wayland_only_active: false,
            wayland_ignore_appids: String::new(),
            compact_mode: false,
            wallpaper_nicknames: HashMap::new(),
        }
    }
}

impl AppConfig {
    /// 合并用户配置与默认值
    pub fn merge_with_default(user_config: serde_json::Value) -> Self {
        let default = Self::default();

        if let serde_json::Value::Object(map) = user_config {
            let mut config = default;

            // 正确读取所有值，包括 0 和 false
            if let Some(v) = map.get("fps").and_then(|v| v.as_u64()) {
                config.fps = v as u32;
            }
            if let Some(v) = map.get("volume").and_then(|v| v.as_u64()) {
                config.volume = v as u32; // 可以正确读取 0
            }
            if let Some(v) = map.get("scaling").and_then(|v| v.as_str()) {
                config.scaling = v.to_string();
            }
            // Support both "silence" (legacy) and "muteAudio" (new)
            if let Some(v) = map.get("muteAudio").and_then(|v| v.as_bool()) {
                config.silence = v;
            } else if let Some(v) = map.get("silence").and_then(|v| v.as_bool()) {
                config.silence = v;
            }
            if let Some(v) = map.get("noFullscreenPause").and_then(|v| v.as_bool()) {
                config.no_fullscreen_pause = v;
            }
            if let Some(v) = map.get("disableMouse").and_then(|v| v.as_bool()) {
                config.disable_mouse = v;
            }
            // Support both "noAutomute" (new) and "noautomute" (legacy)
            if let Some(v) = map.get("noAutomute").and_then(|v| v.as_bool()) {
                config.no_auto_mute = v;
            } else if let Some(v) = map.get("noautomute").and_then(|v| v.as_bool()) {
                config.no_auto_mute = v;
            }
            if let Some(v) = map.get("noAudioProcessing").and_then(|v| v.as_bool()) {
                config.no_audio_processing = v;
            }
            if let Some(v) = map.get("disableParallax").and_then(|v| v.as_bool()) {
                config.disable_parallax = v;
            }
            if let Some(v) = map.get("disableParticles").and_then(|v| v.as_bool()) {
                config.disable_particles = v;
            }
            if let Some(v) = map.get("clamping").and_then(|v| v.as_str()) {
                config.clamping = v.to_string();
            }
            if let Some(v) = map.get("lastWallpaper").and_then(|v| v.as_str()) {
                config.last_wallpaper = Some(v.to_string());
            }
            if let Some(v) = map.get("lastScreen").and_then(|v| v.as_str()) {
                config.last_screen = Some(v.to_string());
            }
            if let Some(v) = map.get("screenshotDelay").and_then(|v| v.as_u64()) {
                config.screenshot_delay = v as u32;
            }
            if let Some(v) = map.get("screenshotRes").and_then(|v| v.as_str()) {
                config.screenshot_res = v.to_string();
            }
            if let Some(v) = map.get("preferXvfb").and_then(|v| v.as_bool()) {
                config.prefer_xvfb = v;
            }
            if let Some(v) = map.get("cycleEnabled").and_then(|v| v.as_bool()) {
                config.cycle_enabled = v;
            }
            if let Some(v) = map.get("cycleInterval").and_then(|v| v.as_u64()) {
                config.cycle_interval = v as u32;
            }
            if let Some(v) = map.get("cycleOrder").and_then(|v| v.as_str()) {
                config.cycle_order = v.to_string();
            }
            if let Some(v) = map.get("assetsPath").and_then(|v| v.as_str()) {
                config.assets_path = Some(v.to_string());
            }
            if let Some(v) = map.get("workshopPath").and_then(|v| v.as_str()) {
                config.workshop_path = Some(v.to_string());
            }
            if let Some(v) = map.get("waylandOnlyActive").and_then(|v| v.as_bool()) {
                config.wayland_only_active = v;
            }
            if let Some(v) = map.get("waylandIgnoreAppids").and_then(|v| v.as_str()) {
                config.wayland_ignore_appids = v.to_string();
            }
            if let Some(v) = map.get("compactMode").and_then(|v| v.as_bool()) {
                config.compact_mode = v;
            }

            return config;
        }

        default
    }
}

/// 配置管理器
pub struct ConfigManager {
    pub config: AppConfig,
    config_path: PathBuf,
    /// Holds the backing temp file alive so it is deleted when this manager is dropped (test only).
    #[cfg(test)]
    _tempfile: Option<tempfile::NamedTempFile>,
}

impl ConfigManager {
    /// 创建新的配置管理器
    pub fn new() -> LwgResult<Self> {
        let config_dir = dirs::config_dir()
            .ok_or_else(|| LwgError::ConfigError("无法获取配置目录".to_string()))?
            .join("linux-wallpaperengine-gui");

        std::fs::create_dir_all(&config_dir)?;

        let config_path = config_dir.join("config.json");

        let config = if config_path.exists() {
            let content = std::fs::read_to_string(&config_path)?;
            let user_config: serde_json::Value = serde_json::from_str(&content)?;
            AppConfig::merge_with_default(user_config)
        } else {
            AppConfig::default()
        };

        let manager = Self {
            config,
            config_path,
            #[cfg(test)]
            _tempfile: None,
        };
        manager.save()?;

        Ok(manager)
    }

    /// 获取配置项（正确处理 None 和 falsy 值）
    pub fn get(&self, key: &str) -> Option<serde_json::Value> {
        match key {
            "fps" => Some(serde_json::json!(self.config.fps)),
            "volume" => Some(serde_json::json!(self.config.volume)), // 正确返回 0
            "scaling" => Some(serde_json::json!(self.config.scaling)),
            "silence" => Some(serde_json::json!(self.config.silence)),
            "noFullscreenPause" => Some(serde_json::json!(self.config.no_fullscreen_pause)),
            "disableMouse" => Some(serde_json::json!(self.config.disable_mouse)),
            "noAutomute" => Some(serde_json::json!(self.config.no_auto_mute)),
            "noAudioProcessing" => Some(serde_json::json!(self.config.no_audio_processing)),
            "disableParallax" => Some(serde_json::json!(self.config.disable_parallax)),
            "disableParticles" => Some(serde_json::json!(self.config.disable_particles)),
            "clamping" => Some(serde_json::json!(self.config.clamping)),
            "lastWallpaper" => self
                .config
                .last_wallpaper
                .as_ref()
                .map(|v| serde_json::json!(v)),
            "lastScreen" => self
                .config
                .last_screen
                .as_ref()
                .map(|v| serde_json::json!(v)),
            "cycleEnabled" => Some(serde_json::json!(self.config.cycle_enabled)),
            "cycleInterval" => Some(serde_json::json!(self.config.cycle_interval)),
            "cycleOrder" => Some(serde_json::json!(self.config.cycle_order)),
            "assetsPath" => self
                .config
                .assets_path
                .as_ref()
                .map(|v| serde_json::json!(v)),
            "workshopPath" => self
                .config
                .workshop_path
                .as_ref()
                .map(|v| serde_json::json!(v)),
            _ => None,
        }
    }

    /// 设置配置项（带变更检测）
    pub fn set(&mut self, key: &str, value: impl Serialize) -> LwgResult<()> {
        let json_value = serde_json::to_value(value)?;

        // 变更检测：如果值相同则不保存
        if let Some(current) = self.get(key) {
            if current == json_value {
                debug!("配置值未变化：{} = {:?}", key, json_value);
                return Ok(());
            }
        }

        match key {
            "fps" => {
                if let Some(v) = json_value.as_u64() {
                    self.config.fps = v as u32;
                }
            }
            "volume" => {
                if let Some(v) = json_value.as_u64() {
                    self.config.volume = v as u32; // 正确设置 0
                }
            }
            "scaling" => {
                if let Some(v) = json_value.as_str() {
                    self.config.scaling = v.to_string();
                }
            }
            "silence" => {
                if let Some(v) = json_value.as_bool() {
                    self.config.silence = v;
                }
            }
            "lastWallpaper" => {
                self.config.last_wallpaper = json_value.as_str().map(|s| s.to_string());
            }
            "lastScreen" => {
                self.config.last_screen = json_value.as_str().map(|s| s.to_string());
            }
            "active_monitors" => {
                if let Ok(map) =
                    serde_json::from_value::<HashMap<String, String>>(json_value.clone())
                {
                    self.config.active_monitors = map;
                }
            }
            "cycleEnabled" => {
                if let Some(v) = json_value.as_bool() {
                    self.config.cycle_enabled = v;
                }
            }
            "cycleInterval" => {
                if let Some(v) = json_value.as_u64() {
                    self.config.cycle_interval = v as u32;
                }
            }
            "assetsPath" => {
                self.config.assets_path = json_value.as_str().map(|s| s.to_string());
            }
            "workshopPath" => {
                self.config.workshop_path = json_value.as_str().map(|s| s.to_string());
            }
            _ => {
                warn!("未知配置键：{}", key);
            }
        }

        info!("配置已更新：{} = {:?}", key, json_value);
        self.save()?;
        Ok(())
    }

    /// 验证路径是否存在
    pub fn validate_path(&self, path: &str) -> LwgResult<()> {
        let path = Path::new(path);
        if !path.exists() {
            return Err(LwgError::ConfigError(format!(
                "路径不存在：{}",
                path.display()
            )));
        }
        if !path.is_dir() {
            return Err(LwgError::ConfigError(format!(
                "不是目录：{}",
                path.display()
            )));
        }
        Ok(())
    }

    /// 保存配置
    pub fn save(&self) -> LwgResult<()> {
        let json = serde_json::to_string_pretty(&self.config)?;
        std::fs::write(&self.config_path, json)?;
        debug!("配置已保存：{:?}", self.config_path);
        Ok(())
    }

    /// Creates a config manager for testing backed by a unique temporary file,
    /// avoiding concurrent read/write races on the shared config file.
    /// The temporary file is deleted automatically when the returned manager is dropped.
    #[cfg(test)]
    pub fn new_for_test() -> LwgResult<Self> {
        let tmp = tempfile::NamedTempFile::new()?;
        let config_path = tmp.path().to_path_buf();
        let manager = Self {
            config: AppConfig::default(),
            config_path,
            _tempfile: Some(tmp),
        };
        manager.save()?;
        Ok(manager)
    }

    /// 获取配置的可变引用
    pub fn config_mut(&mut self) -> &mut AppConfig {
        &mut self.config
    }

    /// 获取配置的不可变引用
    pub fn config(&self) -> &AppConfig {
        &self.config
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default_config() {
        let config = AppConfig::default();
        assert_eq!(config.fps, 30);
        assert_eq!(config.volume, 0); // 正确默认为 0
        assert_eq!(config.scaling, "default");
        assert!(config.silence);
        assert!(config.workshop_path.is_none());
    }

    #[test]
    fn test_merge_with_default() {
        let user = serde_json::json!({
            "fps": 60,
            "volume": 0,  // 测试 0 值不会被忽略
            "scaling": "stretch",
            "lastWallpaper": "12345",
            "workshopPath": "/path/to/workshop"
        });

        let config = AppConfig::merge_with_default(user);
        assert_eq!(config.fps, 60);
        assert_eq!(config.volume, 0); // 正确读取 0
        assert_eq!(config.scaling, "stretch");
        assert_eq!(config.last_wallpaper, Some("12345".to_string()));
        assert_eq!(config.workshop_path, Some("/path/to/workshop".to_string()));
    }

    #[test]
    fn test_serialization_camel_case() {
        let config = AppConfig::default();
        let json = serde_json::to_string(&config).unwrap();
        // Verify camelCase serialization
        assert!(json.contains("muteAudio"));
        assert!(json.contains("noAutomute"));
        assert!(json.contains("noFullscreenPause"));
        assert!(json.contains("workshopPath"));
    }
}

#[cfg(test)]
mod tests_config_extended {
    use super::*;

    #[test]
    fn test_config_get_set() {
        let mut config = ConfigManager::new().unwrap();
        config.set("fps", 60u32).unwrap();
        let value = config.get("fps");
        assert_eq!(value, Some(serde_json::json!(60)));
    }

    #[test]
    fn test_config_volume_zero() {
        let mut config = ConfigManager::new().unwrap();
        config.set("volume", 0u32).unwrap();
        let value = config.get("volume");
        assert_eq!(value, Some(serde_json::json!(0)));
    }

    #[test]
    fn test_config_path_validation() {
        let config = ConfigManager::new().unwrap();
        assert!(config.validate_path("/tmp").is_ok());
        assert!(config.validate_path("/nonexistent_path_12345").is_err());
    }
}
