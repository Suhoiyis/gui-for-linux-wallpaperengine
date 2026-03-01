use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[error("JSON parse error: {0}")]
    Json(#[from] serde_json::Error),
}

/// 核心配置结构体
/// 对应 Python 版本的 config.py 中的类
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")] // 保持与 Python 版可能存在的 camelCase 兼容
pub struct AppConfig {
    /// 是否允许开机自启
    #[serde(default = "default_true")]
    pub auto_start: bool,
    
    /// Steam Workshop 的路径
    #[serde(default)]
    pub workshop_path: Option<String>,
    
    /// 当前选中的壁纸 ID
    #[serde(default)]
    pub current_wallpaper_id: Option<String>,

    // 在这里添加更多 Python 版本中有的字段...
    // 比如 audio_volume, playback_speed 等
}

fn default_true() -> bool { true }

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            auto_start: true,
            workshop_path: None,
            current_wallpaper_id: None,
        }
    }
}

impl AppConfig {
    /// 获取配置文件的完整路径
    /// Linux: ~/.config/lwg/settings.json
    pub fn get_config_path() -> Result<PathBuf, ConfigError> {
        let proj_dirs = directories::ProjectDirs::from("com", "github", "lwg")
            .ok_or_else(|| std::io::Error::new(std::io::ErrorKind::NotFound, "Config dir not found"))?;
        
        let config_dir = proj_dirs.config_dir().to_path_buf();
        
        // 确保目录存在
        if !config_dir.exists() {
            std::fs::create_dir_all(&config_dir)?;
        }
        
        Ok(config_dir.join("settings.json"))
    }

    /// 从文件加载配置
    pub async fn load() -> Result<Self, ConfigError> {
        let path = Self::get_config_path()?;
        
        if !path.exists() {
            // 如果文件不存在，返回默认配置并保存
            let default_config = Self::default();
            default_config.save().await?;
            return Ok(default_config);
        }

        let content = tokio::fs::read_to_string(path).await?;
        let config: AppConfig = serde_json::from_str(&content)?;
        Ok(config)
    }

    /// 保存配置到文件
    pub async fn save(&self) -> Result<(), ConfigError> {
        let path = Self::get_config_path()?;
        let content = serde_json::to_string_pretty(self)?;
        tokio::fs::write(path, content).await?;
        Ok(())
    }
}
