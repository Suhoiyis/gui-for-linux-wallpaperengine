pub mod config;
pub mod properties;
pub mod performance;
pub mod controller;
pub mod error;
pub mod history;
pub mod nickname;
pub mod screen;
pub mod wallpaper;

pub use config::{AppConfig, ConfigManager};
pub use controller::{ScreenshotManager, WallpaperController};
pub use error::{LwgError, LwgResult};
pub use history::{HistoryEntry, HistoryManager};
pub use nickname::NicknameManager;
pub use screen::{Display, ScreenManager};
pub use wallpaper::{Wallpaper, WallpaperManager};
