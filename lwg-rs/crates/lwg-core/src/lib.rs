pub mod controller;

pub mod config;
pub mod logger;
pub mod performance;
pub mod error;
pub mod history;
pub mod nickname;
pub mod screen;
pub mod wallpaper;

pub use config::{AppConfig, ConfigManager};
pub use error::{LwgError, LwgResult};
pub use history::{HistoryEntry, HistoryManager};
pub use nickname::NicknameManager;
pub use screen::{Display, ScreenManager};
pub use wallpaper::{Wallpaper, WallpaperManager};
pub use performance::{PerformanceMonitor, ScreenshotRecord, SystemStatsPayload};
