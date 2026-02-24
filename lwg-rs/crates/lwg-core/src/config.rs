use crate::error::{LwgError, LwgResult};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use tracing::{debug, info, warn};

/// 应用配置结构体
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppConfig {
    pub fps: u32,
    pub volume: u32,
    pub scaling: String,
    pub silence: bool,
    pub no_fullscreen_pause: bool,
    pub disable_mouse: bool,
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
    pub active_monitors: HashMap<String, String>,
    pub cycle_enabled: bool,
    pub cycle_interval: u32,
    pub cycle_order: String,
    pub assets_path: Option<String>,
    pub wayland_only_active: bool,
    pub wayland_ignore_appids: String,
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
            
            if let Some(v) = map.get("fps").and_then(|v| v.as_u64()) {
                config.fps = v as u32;
            }
            if let Some(v) = map.get("volume").and_then(|v| v.as_u64()) {
                config.volume = v as u32;
            }
            if let Some(v) = map.get("scaling").and_then(|v| v.as_str()) {
                config.scaling = v.to_string();
            }
            if let Some(v) = map.get("silence").and_then(|v| v.as_bool()) {
                config.silence = v;
            }
            if let Some(v) = map.get("noFullscreenPause").and_then(|v| v.as_bool()) {
                config.no_fullscreen_pause = v;
            }
            if let Some(v) = map.get("disableMouse").and_then(|v| v.as_bool()) {
                config.disable_mouse = v;
            }
            if let Some(v) = map.get("noautomute").and_then(|v| v.as_bool()) {
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
            if let Some(v) = map.get("wayland_only_active").and_then(|v| v.as_bool()) {
                config.wayland_only_active = v;
            }
            if let Some(v) = map.get("wayland_ignore_appids").and_then(|v| v.as_str()) {
                config.wayland_ignore_appids = v.to_string();
            }
            if let Some(v) = map.get("compact_mode").and_then(|v| v.as_bool()) {
                config.compact_mode = v;
            }
            if let Some(v) = map.get("wallpaperNicknames").and_then(|v| v.as_object()) {
                config.wallpaper_nicknames = v.iter()
                    .filter_map(|(k, v)| v.as_str().map(|s| (k.clone(), s.to_string())))
                    .collect();
            }
            if let Some(v) = map.get("active_monitors").and_then(|v| v.as_object()) {
                config.active_monitors = v.iter()
                    .filter_map(|(k, v)| v.as_str().map(|s| (k.clone(), s.to_string())))
                    .collect();
            }
            if let Some(v) = map.get("wallpaperProperties").and_then(|v| v.as_object()) {
                config.wallpaper_properties = v.clone().into_iter().collect();
            }
            
            config
        } else {
            default
        }
    }
}

/// 配置管理器
pub struct ConfigManager {
    pub config: AppConfig,
    config_path: PathBuf,
}

impl ConfigManager {
    /// 创建新的配置管理器并加载配置
    pub fn new() -> LwgResult<Self> {
        let config_dir = Self::get_config_dir();
        let config_path = config_dir.join("config.json");
        
        std::fs::create_dir_all(&config_dir)?;
        
        let config = if config_path.exists() {
            debug!("Loading config from {:?}", config_path);
            let content = std::fs::read_to_string(&config_path)?;
            let user_value: serde_json::Value = serde_json::from_str(&content)?;
            AppConfig::merge_with_default(user_value)
        } else {
            info!("Config file not found, using defaults");
            AppConfig::default()
        };
        
        Ok(Self {
            config,
            config_path,
        })
    }
    
    /// 从指定路径加载配置（用于测试）
    pub fn from_path(path: impl AsRef<Path>) -> LwgResult<Self> {
        let config_path = path.as_ref().to_path_buf();
        
        let config = if config_path.exists() {
            let content = std::fs::read_to_string(&config_path)?;
            let user_value: serde_json::Value = serde_json::from_str(&content)?;
            AppConfig::merge_with_default(user_value)
        } else {
            AppConfig::default()
        };
        
        Ok(Self {
            config,
            config_path,
        })
    }
    
    /// 保存配置到文件
    pub fn save(&self) -> LwgResult<()> {
        debug!("Saving config to {:?}", self.config_path);
        let content = serde_json::to_string_pretty(&self.config)?;
        std::fs::write(&self.config_path, content)?;
        Ok(())
    }
    
    /// 获取配置目录
    pub fn get_config_dir() -> PathBuf {
        dirs::config_dir()
            .map(|d| d.join("linux-wallpaperengine-gui"))
            .unwrap_or_else(|| PathBuf::from("~/.config/linux-wallpaperengine-gui"))
    }
    
    /// 获取壁纸库路径
    pub fn get_workshop_path() -> PathBuf {
        dirs::home_dir()
            .map(|d| d.join(".local/share/Steam/steamapps/workshop/content/431960"))
            .unwrap_or_else(|| PathBuf::from("~/.local/share/Steam/steamapps/workshop/content/431960"))
    }
    
    /// 获取通用配置项（支持嵌套 key，如 "fps" 或 "scaling"）
    pub fn get(&self, key: &str) -> Option<serde_json::Value> {
        match key {
            "fps" => Some(serde_json::json!(self.config.fps)),
            "volume" => Some(serde_json::json!(self.config.volume)),
            "scaling" => Some(serde_json::json!(self.config.scaling)),
            "silence" => Some(serde_json::json!(self.config.silence)),
            "lastWallpaper" => self.config.last_wallpaper.clone().map(|x| serde_json::json!(x)),
            "lastScreen" => self.config.last_screen.clone().map(|x| serde_json::json!(x)),
            "active_monitors" => Some(serde_json::to_value(&self.config.active_monitors).ok()?),
            "cycleEnabled" => Some(serde_json::json!(self.config.cycle_enabled)),
            "cycleInterval" => Some(serde_json::json!(self.config.cycle_interval)),
            "cycleOrder" => Some(serde_json::json!(self.config.cycle_order)),
            _ => None,
        }
    }
    
    /// 设置配置项
    pub fn set(&mut self, key: &str, value: impl Serialize) -> LwgResult<()> {
        let json_value = serde_json::to_value(value)?;
        
        match key {
            "fps" => {
                if let Some(v) = json_value.as_u64() {
                    self.config.fps = v as u32;
                }
            }
            "volume" => {
                if let Some(v) = json_value.as_u64() {
                    self.config.volume = v as u32;
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
                if let Ok(map) = serde_json::from_value::<HashMap<String, String>>(json_value) {
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
            _ => {
                warn!("Unknown config key: {}", key);
            }
        }
        
        self.save()?;
        Ok(())
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
    use std::io::Write;
    use tempfile::NamedTempFile;
    
    #[test]
    fn test_default_config() {
        let config = AppConfig::default();
        assert_eq!(config.fps, 30);
        assert_eq!(config.volume, 0);
        assert_eq!(config.scaling, "default");
        assert!(config.silence);
    }
    
    #[test]
    fn test_merge_with_default() {
        let user = serde_json::json!({
            "fps": 60,
            "scaling": "stretch",
            "lastWallpaper": "12345"
        });
        
        let config = AppConfig::merge_with_default(user);
        assert_eq!(config.fps, 60);
        assert_eq!(config.scaling, "stretch");
        assert_eq!(config.last_wallpaper, Some("12345".to_string()));
        assert_eq!(config.volume, 0); // default
        assert!(config.silence); // default
    }
    
    #[test]
    fn test_load_and_save() {
        let mut temp_file = NamedTempFile::new().unwrap();
        let config_json = r#"{"fps": 45, "volume": 50}"#;
        temp_file.write_all(config_json.as_bytes()).unwrap();
        
        let manager = ConfigManager::from_path(temp_file.path()).unwrap();
        assert_eq!(manager.config.fps, 45);
        assert_eq!(manager.config.volume, 50);
    }
}
