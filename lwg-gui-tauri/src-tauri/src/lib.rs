mod tray;

use serde::{Deserialize, Serialize};
use tauri::{Emitter, Manager, State};
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
use std::collections::HashMap;
use tokio::sync::Mutex;
use tauri_plugin_autostart::MacosLauncher;
use tauri_plugin_window_state::StateFlags;
// std::time imported locally where needed


// ================= 平台特定导入 =================

#[cfg(target_os = "linux")]
use lwg_core::{
    ConfigManager as LwgConfigManager,
    controller::WallpaperController,
    config::AppConfig as LwgAppConfig,
    config::Playlist as LwgPlaylist,
    wallpaper::WallpaperManager,
    PerformanceMonitor,
    ScreenshotRecord,
    ScreenshotHistoryManager,
    LogManager, LogEntry, LogSource,
    StateManager,
    state::{ActiveWallpaper as LwgActiveWallpaper},
    HistoryManager, HistoryEntry,
    NicknameManager,
    FavoriteManager,
};


#[cfg(target_os = "linux")]
fn log_gui(state: &State<'_, TauriState>, message: &str) {
    if let Ok(lm) = state.log_manager.lock() {
        lm.info(LogSource::GUI, message);
    }
}

// Non-Linux: provide local ScreenshotRecord definition
#[cfg(not(target_os = "linux"))]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScreenshotRecord {
    pub timestamp: u64,
    pub wp_id: String,
    pub output_path: String,
    pub duration: f32,
    pub max_cpu: f32,
    pub max_mem: f32,
}

#[cfg(not(target_os = "linux"))]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HistoryEntry {
    pub id: String,
    pub title: String,
    pub preview: String,
    pub timestamp: String,
}

// ================= 数据结构 =================

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Wallpaper {
    id: String,
    title: String,
    preview: String,
    wtype: String,
    path: String,
    description: Option<String>,  // 新增
    tags: Vec<String>,
    size: String,
}

/// GitHub 更新检查结果
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UpdateCheckResult {
    pub has_update: bool,
    pub current_version: String,
    pub latest_version: Option<String>,
    pub download_url: Option<String>,
}

/// 播放列表
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "camelCase")]
pub struct Playlist {
    pub id: String,
    pub name: String,
    pub wallpaper_ids: Vec<String>,
    pub created_at: u64,
    pub updated_at: u64,
}

/// 跨平台配置结构体 (user preferences only)
/// Linux: 与 lwg_core::AppConfig 完全一致
/// Windows: Mock 版本，用于 UI 开发
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
    pub wallpaper_properties: std::collections::HashMap<String, serde_json::Value>,
    pub screenshot_delay: u32,
    pub screenshot_res: String,
    pub prefer_xvfb: bool,
    pub cycle_enabled: bool,
    pub cycle_interval: u32,
    pub cycle_order: String,
    pub assets_path: Option<String>,
    pub workshop_path: Option<String>,
    pub wayland_only_active: bool,
    pub wayland_ignore_appids: String,
    pub compact_mode: bool,
    pub wallpaper_nicknames: std::collections::HashMap<String, String>,
    #[serde(rename = "startHidden")]
    pub start_hidden: bool,
    #[serde(rename = "autoRestore")]
    pub auto_restore: bool,
    pub playlists: Vec<Playlist>,
    pub cycle_playlist_id: Option<String>,
    pub playlist_sidebar_open: bool,
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
            wallpaper_properties: std::collections::HashMap::new(),
            screenshot_delay: 20,
            screenshot_res: "3840x2160".to_string(),
            prefer_xvfb: true,
            cycle_enabled: false,
            cycle_interval: 15,
            cycle_order: "random".to_string(),
            assets_path: None,
            workshop_path: None,
            wayland_only_active: false,
            wayland_ignore_appids: String::new(),
            compact_mode: false,
            wallpaper_nicknames: std::collections::HashMap::new(),
            start_hidden: false,
            auto_restore: false,
            playlists: Vec::new(),
            cycle_playlist_id: None,
            playlist_sidebar_open: true,
        }
    }
}

/// Represents an active wallpaper on a screen
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct ActiveWallpaper {
    pub wallpaper_id: String,
    pub is_playing: bool,
}

/// Runtime state - direct mapping of screen -> active wallpaper
pub type AppState = std::collections::HashMap<String, ActiveWallpaper>;

#[cfg(target_os = "linux")]
impl From<LwgAppConfig> for AppConfig {
    fn from(config: LwgAppConfig) -> Self {
        Self {
            fps: config.fps,
            volume: config.volume,
            scaling: config.scaling,
            silence: config.silence,
            no_fullscreen_pause: config.no_fullscreen_pause,
            disable_mouse: config.disable_mouse,
            no_auto_mute: config.no_auto_mute,
            no_audio_processing: config.no_audio_processing,
            disable_parallax: config.disable_parallax,
            disable_particles: config.disable_particles,
            clamping: config.clamping,
            wallpaper_properties: config.wallpaper_properties,
            screenshot_delay: config.screenshot_delay,
            screenshot_res: config.screenshot_res,
            prefer_xvfb: config.prefer_xvfb,
            cycle_enabled: config.cycle_enabled,
            cycle_interval: config.cycle_interval,
            cycle_order: config.cycle_order,
            assets_path: config.assets_path,
            workshop_path: config.workshop_path,
            wayland_only_active: config.wayland_only_active,
            wayland_ignore_appids: config.wayland_ignore_appids,
            compact_mode: config.compact_mode,
            wallpaper_nicknames: config.wallpaper_nicknames,
            start_hidden: config.start_hidden,
            auto_restore: config.auto_restore,
            playlists: config.playlists.into_iter().map(|p| p.into()).collect(),
            cycle_playlist_id: config.cycle_playlist_id,
            playlist_sidebar_open: config.playlist_sidebar_open,
        }
    }
}

#[cfg(target_os = "linux")]
impl From<AppConfig> for LwgAppConfig {
    fn from(config: AppConfig) -> Self {
        Self {
            fps: config.fps,
            volume: config.volume,
            scaling: config.scaling,
            silence: config.silence,
            no_fullscreen_pause: config.no_fullscreen_pause,
            disable_mouse: config.disable_mouse,
            no_auto_mute: config.no_auto_mute,
            no_audio_processing: config.no_audio_processing,
            disable_parallax: config.disable_parallax,
            disable_particles: config.disable_particles,
            clamping: config.clamping,
            wallpaper_properties: config.wallpaper_properties,
            screenshot_delay: config.screenshot_delay,
            screenshot_res: config.screenshot_res,
            prefer_xvfb: config.prefer_xvfb,
            cycle_enabled: config.cycle_enabled,
            cycle_interval: config.cycle_interval,
            cycle_order: config.cycle_order,
            assets_path: config.assets_path,
            workshop_path: config.workshop_path,
            wayland_only_active: config.wayland_only_active,
            wayland_ignore_appids: config.wayland_ignore_appids,
            compact_mode: config.compact_mode,
            wallpaper_nicknames: config.wallpaper_nicknames,
            start_hidden: config.start_hidden,
            auto_restore: config.auto_restore,
            playlists: config.playlists.into_iter().map(|p| p.into()).collect(),
            cycle_playlist_id: config.cycle_playlist_id,
            playlist_sidebar_open: config.playlist_sidebar_open,
        }
    }
}

#[cfg(target_os = "linux")]
impl From<LwgActiveWallpaper> for ActiveWallpaper {
    fn from(aw: LwgActiveWallpaper) -> Self {
        Self {
            wallpaper_id: aw.wallpaper_id,
            is_playing: aw.is_playing,
        }
    }
}

#[cfg(target_os = "linux")]
impl From<ActiveWallpaper> for LwgActiveWallpaper {
    fn from(aw: ActiveWallpaper) -> Self {
        Self {
            wallpaper_id: aw.wallpaper_id,
            is_playing: aw.is_playing,
        }
    }
}

#[cfg(target_os = "linux")]
impl From<LwgPlaylist> for Playlist {
    fn from(p: LwgPlaylist) -> Self {
        Self {
            id: p.id,
            name: p.name,
            wallpaper_ids: p.wallpaper_ids,
            created_at: p.created_at,
            updated_at: p.updated_at,
        }
    }
}

#[cfg(target_os = "linux")]
impl From<Playlist> for LwgPlaylist {
    fn from(p: Playlist) -> Self {
        Self {
            id: p.id,
            name: p.name,
            wallpaper_ids: p.wallpaper_ids,
            created_at: p.created_at,
            updated_at: p.updated_at,
        }
    }
}




// ================= TauriState =================

struct TauriState {
    #[cfg(target_os = "linux")]
    controller: Mutex<WallpaperController>,

    #[cfg(target_os = "linux")]
    config_manager: Mutex<LwgConfigManager>,

    #[cfg(target_os = "linux")]
    state_manager: Mutex<StateManager>,

    #[cfg(target_os = "linux")]
    history_manager: Mutex<HistoryManager>,

    #[cfg(target_os = "linux")]
    screenshot_history_manager: Mutex<ScreenshotHistoryManager>,

    #[cfg(target_os = "linux")]
    performance_monitor: Arc<std::sync::Mutex<PerformanceMonitor>>,

    #[cfg(target_os = "linux")]
    log_manager: Arc<std::sync::Mutex<LogManager>>,

    #[cfg(target_os = "linux")]
    nickname_manager: Mutex<NicknameManager>,

    #[cfg(target_os = "linux")]
    favorite_manager: Mutex<FavoriteManager>,

    monitor_running: Arc<AtomicBool>,

    /// 轮换定时器任务句柄
    #[cfg(target_os = "linux")]
    cycle_task: Arc<Mutex<Option<tokio::task::JoinHandle<()>>>>,

    /// 轮换运行标志
    cycle_running: Arc<AtomicBool>,

    /// 轮换目标屏幕（"all" 或具体屏幕名如 "eDP-1"）
    #[cfg(target_os = "linux")]
    cycle_screen: Arc<Mutex<String>>,

    /// 壁纸 ID 缓存（避免每次轮换都扫描磁盘）
    #[cfg(target_os = "linux")]
    cached_wallpaper_ids: Arc<std::sync::RwLock<Vec<String>>>,

    #[cfg(not(target_os = "linux"))]
    _dummy: bool,
}


// ================= 辅助函数 =================

/// 检查配置变更是否需要重启壁纸
/// 只影响壁纸属性的配置项才需要重启
#[cfg(target_os = "linux")]
fn needs_wallpaper_restart(old: &LwgAppConfig, new: &LwgAppConfig) -> bool {
    // 壁纸渲染相关配置
    old.fps != new.fps ||
    old.scaling != new.scaling ||
    old.clamping != new.clamping ||
    old.volume != new.volume ||
    old.silence != new.silence ||
    old.disable_parallax != new.disable_parallax ||
    old.disable_particles != new.disable_particles ||
    old.no_fullscreen_pause != new.no_fullscreen_pause ||
    old.disable_mouse != new.disable_mouse ||
    old.no_auto_mute != new.no_auto_mute ||
    old.no_audio_processing != new.no_audio_processing ||
    old.assets_path != new.assets_path ||
    old.wayland_only_active != new.wayland_only_active ||
    old.wayland_ignore_appids != new.wayland_ignore_appids
}

/// 格式化文件大小
fn format_size(bytes: u64) -> String {
    if bytes == 0 { return "0 MB".to_string(); }
    format!("{:.1} MB", bytes as f64 / 1024.0 / 1024.0)
}

/// 默认壁纸库路径
fn get_default_workshop_path() -> String {
    let home = std::env::var("HOME").unwrap_or_else(|_| "/home".to_string());
    format!("{}/.local/share/Steam/steamapps/workshop/content/431960", home)
}

// ================= Mock 数据生成 =================

#[cfg(not(target_os = "linux"))]
fn generate_mock_wallpapers() -> Vec<Wallpaper> {
    vec![
        Wallpaper {
            id: "mock_001".to_string(),
            title: "Mock Cyberpunk City".to_string(),
            preview: "https://picsum.photos/seed/cyber/400/225".to_string(),
            wtype: "web".to_string(),
            path: "/mock/path/cyberpunk".to_string(),
            description: None,
            tags: vec!["cyberpunk".to_string(), "city".to_string(), "neon".to_string()],
            size: "45.2 MB".to_string(),
        },
        Wallpaper {
            id: "mock_002".to_string(),
            title: "Mock Mountain Sunset".to_string(),
            preview: "https://picsum.photos/seed/mountain/400/225".to_string(),
            wtype: "video".to_string(),
            path: "/mock/path/mountain".to_string(),
            description: None,
            tags: vec!["nature".to_string(), "sunset".to_string(), "mountain".to_string()],
            size: "128.5 MB".to_string(),
        },
        Wallpaper {
            id: "mock_003".to_string(),
            title: "Mock Space Station".to_string(),
            preview: "https://picsum.photos/seed/space/400/225".to_string(),
            wtype: "scene".to_string(),
            path: "/mock/path/space".to_string(),
            description: None,
            tags: vec!["space".to_string(), "scifi".to_string(), "station".to_string()],
            size: "256.8 MB".to_string(),
        },
        Wallpaper {
            id: "mock_004".to_string(),
            title: "Mock Rainy Tokyo".to_string(),
            preview: "https://picsum.photos/seed/tokyo/400/225".to_string(),
            wtype: "web".to_string(),
            path: "/mock/path/tokyo".to_string(),
            description: None,
            tags: vec!["japan".to_string(), "rain".to_string(), "city".to_string()],
            size: "67.3 MB".to_string(),
        },
        Wallpaper {
            id: "mock_005".to_string(),
            title: "Mock Ocean Waves".to_string(),
            preview: "https://picsum.photos/seed/ocean/400/225".to_string(),
            wtype: "video".to_string(),
            path: "/mock/path/ocean".to_string(),
            description: None,
            tags: vec!["ocean".to_string(), "waves".to_string(), "nature".to_string()],
            size: "189.1 MB".to_string(),
        },
        Wallpaper {
            id: "mock_006".to_string(),
            title: "Mock Fireplace".to_string(),
            preview: "https://picsum.photos/seed/fire/400/225".to_string(),
            wtype: "video".to_string(),
            path: "/mock/path/fireplace".to_string(),
            description: None,
            tags: vec!["cozy".to_string(), "fire".to_string(), "warm".to_string()],
            size: "52.4 MB".to_string(),
        },
    ]
}

// ================= Tauri 命令 =================

#[tauri::command]
async fn get_wallpapers(_state: State<'_, TauriState>) -> Result<Vec<Wallpaper>, String> {
    #[cfg(target_os = "linux")]
    {
        println!("🐧 [Linux] 扫描壁纸库...");
        log_gui(&_state, "Scanning wallpaper library...");

        // 从配置获取 workshop_path，否则使用默认路径
        let config_manager = _state.config_manager.lock().await;
        let workshop_path = config_manager.config().workshop_path
            .clone()
            .unwrap_or_else(|| get_default_workshop_path());
        drop(config_manager);

        println!("📁 [Linux] Workshop 路径: {}", workshop_path);

        // 使用 WallpaperManager 扫描
        let mut manager = WallpaperManager::new(&workshop_path);
        let wallpapers = manager.scan()
            .map_err(|e| format!("扫描失败: {:?}", e))?;

        // 转换为前端需要的格式
        let result: Vec<Wallpaper> = wallpapers.values().map(|w| {
            Wallpaper {
                id: w.id.clone(),
                title: w.title.clone(),
                preview: w.preview.to_string_lossy().to_string(),
                wtype: w.wp_type.clone(),
                path: format!("{}/{}", workshop_path, w.id),
                description: if w.description.is_empty() { None } else { Some(w.description.clone()) },
                tags: w.tags.clone(),
                size: format_size(w.size),
            }
        }).collect();

        // 更新壁纸 ID 缓存（用于轮换功能）
        {
            let ids: Vec<String> = result.iter().map(|w| w.id.clone()).collect();
            if let Ok(mut cache) = _state.cached_wallpaper_ids.write() {
                *cache = ids;
                println!("🔄 [Linux] 已更新壁纸缓存: {} 张", result.len());
            }
        }

        log_gui(&_state, &format!("Found {} wallpapers", result.len()));
        println!("✅ [Linux] 扫描到 {} 张壁纸", result.len());
        Ok(result)
    }

    #[cfg(not(target_os = "linux"))]
    {
        println!("🪟 [Windows Mock] 返回模拟壁纸数据");
        Ok(generate_mock_wallpapers())
    }
}

#[tauri::command]
async fn apply_wallpaper(
    id: String,
    screen: Option<String>,
    app: tauri::AppHandle,
    _state: State<'_, TauriState>
) -> Result<(), String> {

    #[cfg(target_os = "linux")]
    {
        println!("▶️ [Rust] 正在应用壁纸: {} (屏幕: {:?})", id, screen);
        log_gui(&_state, &format!("Applying wallpaper: {} (screen: {:?})", id, screen));
        let mut controller = _state.controller.lock().await;
        controller.apply(&id, screen.as_deref()).await.map_err(|e| format!("应用失败: {:?}", e))?;
        println!("✅ [Rust] 壁纸应用成功！");
        log_gui(&_state, "Wallpaper applied successfully");
        // 通知前端刷新活动壁纸
        if let Err(e) = app.emit("wallpaper-changed", ()) {
            eprintln!("[WARN] Failed to emit wallpaper-changed event: {:?}", e);
        }
        return Ok(());
    }

    #[cfg(not(target_os = "linux"))]
    {
        println!("🪟 [Windows] 模拟应用成功: {}", id);
        if let Err(e) = app.emit("wallpaper-changed", ()) {
            eprintln!("[WARN] Failed to emit wallpaper-changed event: {:?}", e);
        }
        Ok(())
    }
}

#[tauri::command]
async fn stop_wallpaper(
    app: tauri::AppHandle,
    _state: State<'_, TauriState>
) -> Result<(), String> {
    #[cfg(target_os = "linux")]
    {
        log_gui(&_state, "Stopping wallpaper");
        let mut controller = _state.controller.lock().await;
        controller.stop().await;
        log_gui(&_state, "Wallpaper stopped");
        // 通知前端刷新活动壁纸
        if let Err(e) = app.emit("wallpaper-changed", ()) {
            eprintln!("[WARN] Failed to emit wallpaper-changed event: {:?}", e);
        }
        Ok(())
    }

    #[cfg(not(target_os = "linux"))]
    {
        println!("🪟 [Windows] 模拟停止");
        if let Err(e) = app.emit("wallpaper-changed", ()) {
            eprintln!("[WARN] Failed to emit wallpaper-changed event: {:?}", e);
        }
        Ok(())
    }
}



#[tauri::command]
async fn delete_wallpaper(
    wallpaper_id: String,
    path: String,
    app: tauri::AppHandle,
    _state: State<'_, TauriState>
) -> Result<(), String> {
    #[cfg(target_os = "linux")]
    {
        println!("🗑️ [Rust] Deleting wallpaper: {} at path: {}", wallpaper_id, path);
        log_gui(&_state, &format!("Deleting wallpaper: {}", wallpaper_id));
        
        let wallpaper_path = std::path::Path::new(&path);
        if !wallpaper_path.exists() {
            return Err(format!("Wallpaper folder not found: {}", path));
        }
        
        let workshop_path = {
            let cm = _state.config_manager.lock().await;
            cm.config().workshop_path.clone()
        };
        
        let allowed_base = match workshop_path {
            Some(ref base) => std::path::Path::new(base),
            None => {
                return Err("No workshop path configured. Cannot safely delete wallpaper.".to_string());
            }
        };
        
        let canonical_wallpaper = match std::fs::canonicalize(wallpaper_path) {
            Ok(p) => p,
            Err(e) => return Err(format!("Failed to resolve wallpaper path: {:?}", e)),
        };
        
        let canonical_base = match std::fs::canonicalize(allowed_base) {
            Ok(p) => p,
            Err(e) => return Err(format!("Failed to resolve workshop path: {:?}", e)),
        };
        
        if !canonical_wallpaper.starts_with(&canonical_base) {
            return Err(format!(
                "Security error: path '{}' is outside allowed workshop directory",
                canonical_wallpaper.display()
            ));
        }
        
        let path_contains_id = canonical_wallpaper
            .components()
            .any(|c| c.as_os_str().to_string_lossy().contains(&wallpaper_id));
        if !path_contains_id {
            return Err(format!(
                "Security error: path '{}' does not contain wallpaper_id as a path component",
                canonical_wallpaper.display()
            ));
        }
        
        {
            let controller = _state.controller.lock().await;
            let active = controller.get_active_wallpapers().await;
            let screens_with_wallpaper: Vec<String> = active
                .iter()
                .filter(|(_, aw)| aw.wallpaper_id == wallpaper_id && aw.is_playing)
                .map(|(screen, _)| screen.clone())
                .collect();
            drop(controller);
            
            if !screens_with_wallpaper.is_empty() {
                println!("⏹️ [Rust] Wallpaper is active on screens: {:?}, stopping...", screens_with_wallpaper);
                let mut controller = _state.controller.lock().await;
                for screen in &screens_with_wallpaper {
                    if let Err(e) = controller.stop_screen(screen).await {
                        eprintln!("[WARN] Failed to stop screen {}: {:?}", screen, e);
                    }
                }
            }
        }
        
        std::fs::remove_dir_all(&canonical_wallpaper)
            .map_err(|e| format!("Failed to delete wallpaper folder: {:?}", e))?;
        
        // Clean up dead IDs from playlists
        {
            let mut cm = _state.config_manager.lock().await;
            let mut should_save = false;
            
            for playlist in cm.config_mut().playlists.iter_mut() {
                let original_len = playlist.wallpaper_ids.len();
                playlist.wallpaper_ids.retain(|id| id != &wallpaper_id);
                if playlist.wallpaper_ids.len() != original_len {
                    should_save = true;
                    playlist.updated_at = std::time::SystemTime::now()
                        .duration_since(std::time::UNIX_EPOCH)
                        .unwrap()
                        .as_secs();
                }
            }
            
            if should_save {
                cm.save().map_err(|e| format!("Failed to save playlists: {:?}", e))?;
                println!("🧹 [Rust] Cleaned wallpaper ID from playlists");
            }
        }
        
        println!("✅ [Rust] Wallpaper deleted successfully: {}", wallpaper_id);
        log_gui(&_state, &format!("Wallpaper deleted: {}", wallpaper_id));
        
        // Emit event to notify frontend
        if let Err(e) = app.emit("wallpaper-changed", ()) {
            eprintln!("[WARN] Failed to emit wallpaper-changed event: {:?}", e);
        }
        
        Ok(())
    }

    #[cfg(not(target_os = "linux"))]
    {
        println!("🪟 [Windows] Mock delete wallpaper: {}", wallpaper_id);
        if let Err(e) = app.emit("wallpaper-changed", ()) {
            eprintln!("[WARN] Failed to emit wallpaper-changed event: {:?}", e);
        }
        Ok(())
    }
}
// ================= Settings Commands =================

// ================= Settings Commands =================

#[tauri::command]
async fn get_settings(_state: State<'_, TauriState>) -> Result<AppConfig, String> {
    #[cfg(target_os = "linux")]
    {
        let config_manager = _state.config_manager.lock().await;
        Ok(config_manager.config().clone().into()) // 转换为本地 AppConfig
    }

    #[cfg(not(target_os = "linux"))]
    {
        println!("🪟 [Windows Mock] 返回默认配置");
        Ok(AppConfig::default())
    }
}

#[tauri::command]
async fn save_settings(
    config: AppConfig,
    _state: State<'_, TauriState>
) -> Result<bool, String> {
    #[cfg(target_os = "linux")]
    {
        println!("💾 [Linux] 正在保存配置...");

        let mut config_manager = _state.config_manager.lock().await;
        let old_config = config_manager.config().clone();

        // 转换并更新配置
        let lwg_config: LwgAppConfig = config.into();
        *config_manager.config_mut() = lwg_config.clone();

        // 保存到文件
        config_manager.save().map_err(|e| format!("保存失败: {:?}", e))?;

        // 检查是否需要重启壁纸
        let needs_restart = needs_wallpaper_restart(&old_config, &lwg_config);

        if needs_restart {
            println!("🔄 [Linux] 检测到壁纸相关配置变更，准备重启壁纸...");
            drop(config_manager); // 释放锁

            let mut controller = _state.controller.lock().await;
            controller.restart_wallpapers().await.map_err(|e| format!("重启失败: {:?}", e))?;
            println!("✅ [Linux] 壁纸已重启");
        } else {
            println!("ℹ️ [Linux] 配置已保存（无需重启壁纸）");
        }

        Ok(needs_restart)
    }

    #[cfg(not(target_os = "linux"))]
    {
        println!("🪟 [Windows Mock] 模拟保存配置: fps={}, volume={}", config.fps, config.volume);
        Ok(false)
    }
}


// ================= State Commands =================

#[tauri::command]
async fn get_state(_state: State<'_, TauriState>) -> Result<AppState, String> {
    #[cfg(target_os = "linux")]
    {
        let state_manager = _state.state_manager.lock().await;
        Ok(state_manager.state().iter()
            .map(|(k, v)| (k.clone(), ActiveWallpaper {
                wallpaper_id: v.wallpaper_id.clone(),
                is_playing: v.is_playing,
            }))
            .collect())
    }

    #[cfg(not(target_os = "linux"))]
    {
        Ok(AppState::new())
    }
}



#[tauri::command]
async fn save_state(
    app_state: AppState,
    _state: State<'_, TauriState>
) -> Result<bool, String> {
    #[cfg(target_os = "linux")]
    {
        // 更新 state_manager（持久化）
        let mut state_manager = _state.state_manager.lock().await;
        let new_state: HashMap<String, LwgActiveWallpaper> = app_state.into_iter()
            .map(|(k, v)| (k, LwgActiveWallpaper {
                wallpaper_id: v.wallpaper_id,
                is_playing: v.is_playing,
            }))
            .collect();
        *state_manager.state_mut() = new_state.clone();
        state_manager.save().map_err(|e| format!("Failed to save state: {:?}", e))?;
        drop(state_manager);

        // 同步控制器的内存状态
        let mut controller = _state.controller.lock().await;
        controller.sync_state(new_state).await;

        Ok(true)
    }

    #[cfg(not(target_os = "linux"))]
    {
        Ok(true)
    }
}


#[tauri::command]
async fn add_history(
    id: String,
    title: String,
    preview: String,
    _state: State<'_, TauriState>
) -> Result<bool, String> {
    #[cfg(target_os = "linux")]
    {
        let mut history_manager = _state.history_manager.lock().await;
        history_manager.add(&id, &title, &preview)
            .map_err(|e| format!("Failed to add history: {:?}", e))?;
        Ok(true)
    }

    #[cfg(not(target_os = "linux"))]
    {
        Ok(true)
    }
}

#[tauri::command]
async fn get_history(
    _state: State<'_, TauriState>
) -> Result<Vec<HistoryEntry>, String> {
    #[cfg(target_os = "linux")]
    {
        let history_manager = _state.history_manager.lock().await;
        Ok(history_manager.list().iter().cloned().collect())
    }

    #[cfg(not(target_os = "linux"))]
    {
        Ok(vec![])
    }
}

#[tauri::command]
async fn clear_history(
    _state: State<'_, TauriState>
) -> Result<bool, String> {
    #[cfg(target_os = "linux")]
    {
        let mut history_manager = _state.history_manager.lock().await;
        history_manager.clear()
            .map_err(|e| format!("Failed to clear history: {:?}", e))?;
        Ok(true)
    }

    #[cfg(not(target_os = "linux"))]
    {
        Ok(true)
    }
}

// ================= Nickname Commands =================

#[tauri::command]
async fn get_nicknames(
    state: State<'_, TauriState>
) -> Result<HashMap<String, String>, String> {
    #[cfg(target_os = "linux")]
    {
        let manager = state.nickname_manager.lock().await;
        Ok(manager.list().clone())
    }

    #[cfg(not(target_os = "linux"))]
    {
        Ok(HashMap::new())
    }
}

#[tauri::command]
async fn set_nickname(
    id: String,
    nickname: String,
    state: State<'_, TauriState>
) -> Result<(), String> {
    #[cfg(target_os = "linux")]
    {
        let mut manager = state.nickname_manager.lock().await;
        manager.set(&id, &nickname)
            .map_err(|e| format!("Failed to set nickname: {}", e))?;
        Ok(())
    }

    #[cfg(not(target_os = "linux"))]
    {
        let _ = (id, nickname);
        Ok(())
    }
}

// ================= Favorite Commands =================

#[tauri::command]
async fn get_favorites(
    state: State<'_, TauriState>
) -> Result<Vec<String>, String> {
    #[cfg(target_os = "linux")]
    {
        let manager = state.favorite_manager.lock().await;
        Ok(manager.list())
    }

    #[cfg(not(target_os = "linux"))]
    {
        Ok(Vec::new())
    }
}

#[tauri::command]
async fn toggle_favorite(
    id: String,
    state: State<'_, TauriState>
) -> Result<bool, String> {
    #[cfg(target_os = "linux")]
    {
        let mut manager = state.favorite_manager.lock().await;
        let is_now_favorite = manager.toggle(&id)
            .map_err(|e| format!("Failed to toggle favorite: {}", e))?;
        Ok(is_now_favorite)
    }

    #[cfg(not(target_os = "linux"))]
    {
        let _ = id;
        Ok(false)
    }
}

// Allowed non-runtime keys for single value updates
const ALLOWED_KEYS: &[&str] = &["workshopPath", "assetsPath", "screenshotRes", "preferXvfb", "screenshotDelay", "cycleEnabled", "cycleInterval", "cycleOrder", "compactMode"];

#[tauri::command]
async fn update_config_value(
    key: String,
    value: serde_json::Value,
    _state: State<'_, TauriState>,
) -> Result<AppConfig, String> {
    #[cfg(target_os = "linux")]
    {
        // Check if key is in allowed list
        if !ALLOWED_KEYS.contains(&key.as_str()) {
            return Err(format!("Key '{}' is not allowed for update. Only non-runtime settings can be updated individually.", key));
        }

        println!("🔧 [Linux] 正在更新配置键: {} = {:?}", key, value);

        let mut config_manager = _state.config_manager.lock().await;
        let mut lwg_config = config_manager.config().clone();


        // Update the specific key based on its name
        match key.as_str() {
            "workshopPath" => {
                if let Some(s) = value.as_str() {
                    lwg_config.workshop_path = Some(s.to_string());
                } else {
                    lwg_config.workshop_path = None;
                }
            },
            "assetsPath" => {
                if let Some(s) = value.as_str() {
                    lwg_config.assets_path = Some(s.to_string());
                } else {
                    lwg_config.assets_path = None;
                }
            },
            "screenshotRes" => {
                if let Some(s) = value.as_str() {
                    lwg_config.screenshot_res = s.to_string();
                } else {
                    return Err("screenshotRes must be a string".to_string());
                }
            },
            "preferXvfb" => {
                if let Some(b) = value.as_bool() {
                    lwg_config.prefer_xvfb = b;
                } else {
                    return Err("preferXvfb must be a boolean".to_string());
                }
            },
            "screenshotDelay" => {
                if let Some(n) = value.as_u64() {
                    lwg_config.screenshot_delay = n as u32;
                } else {
                    return Err("screenshotDelay must be a number".to_string());
                }
            },
            "cycleEnabled" => {
                if let Some(b) = value.as_bool() {
                    lwg_config.cycle_enabled = b;
                } else {
                    return Err("cycleEnabled must be a boolean".to_string());
                }
            },
            "cycleInterval" => {
                if let Some(n) = value.as_u64() {
                    lwg_config.cycle_interval = n as u32;
                } else {
                    return Err("cycleInterval must be a number".to_string());
                }
            },
            "cycleOrder" => {
                if let Some(s) = value.as_str() {
                    lwg_config.cycle_order = s.to_string();
                } else {
                    return Err("cycleOrder must be a string".to_string());
                }
            },
            "compactMode" => {
                if let Some(b) = value.as_bool() {
                    lwg_config.compact_mode = b;
                } else {
                    return Err("compactMode must be a boolean".to_string());
                }
            },
            _ => {
                return Err(format!("Unknown key: {}", key));
            }
        }

        // Save to disk
        *config_manager.config_mut() = lwg_config.clone();
        config_manager.save().map_err(|e| format!("保存失败: {:?}", e))?;

        println!("✅ [Linux] 配置键已更新并保存");

        // Convert back to AppConfig and return
        Ok(lwg_config.into())
    }

    #[cfg(not(target_os = "linux"))]
    {
        println!("🪟 [Windows Mock] 模拟更新配置键: {} = {:?}", key, value);
        Ok(AppConfig::default())
    }

}

#[tauri::command]
async fn restart_wallpapers(_state: State<'_, TauriState>) -> Result<(), String> {
    #[cfg(target_os = "linux")]
    {
        println!("🔄 [Rust] 手动重启壁纸...");
        let mut controller = _state.controller.lock().await;
        controller.restart_wallpapers().await.map_err(|e| format!("重启失败: {:?}", e))?;
        println!("✅ [Rust] 壁纸已重启");
        Ok(())
    }

    #[cfg(not(target_os = "linux"))]
    {
        println!("🪟 [Windows] 模拟重启壁纸");
        Ok(())
    }
}

// ================= App Lifecycle Commands =================

#[tauri::command]
async fn quit_app(app: tauri::AppHandle, state: State<'_, TauriState>) -> Result<(), String> {
    println!("🛑 [Rust] Quitting application...");
    
    // Stop wallpapers (Linux only)
    #[cfg(target_os = "linux")]
    {
        let mut controller = state.controller.lock().await;
        controller.stop().await;
        println!("✅ [Rust] Wallpapers stopped");
    }
    
    // Exit app
    app.exit(0);
    Ok(())
}

#[tauri::command]
async fn restart_app(_app: tauri::AppHandle, state: State<'_, TauriState>) -> Result<(), String> {
    println!("🔄 [Rust] Restarting application...");
    
    // Stop wallpapers (Linux only)
    #[cfg(target_os = "linux")]
    {
        let mut controller = state.controller.lock().await;
        controller.stop().await;
        println!("✅ [Rust] Wallpapers stopped");
    }
    
    // Filter args (remove --hidden)
    let args: Vec<String> = std::env::args()
        .skip(1)
        .filter(|arg| arg != "--hidden")
        .collect();
    
    // Check if running as AppImage (check APPIMAGE env var)
    let exe_path = std::env::var("APPIMAGE")
        .ok()
        .unwrap_or_else(|| {
            std::env::current_exe()
                .expect("Failed to get current exe")
                .to_string_lossy()
                .to_string()
        });
    println!("📍 [Rust] Restart path: {}", exe_path);
    
    // Check if running in dev mode
    let is_dev_mode = exe_path.contains("target/debug");
    
    // Spawn new process in a new session (detaches from current process group)
    #[cfg(target_os = "linux")]
    {
        use std::os::unix::process::CommandExt;
        use std::process::{Command, Stdio};
        
        let mut cmd = Command::new(&exe_path);
        cmd.args(&args)
            .current_dir(std::env::var("HOME").unwrap_or_else(|_| "/".to_string()))
            .stdin(Stdio::null())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .process_group(0);
        
        // In dev mode, pass dev server URL so new process connects to Vite
        if is_dev_mode {
            cmd.env("TAURI_DEV_SERVER_URL", "http://localhost:1420");
            println!("🔧 [Rust] Dev mode: setting TAURI_DEV_SERVER_URL");
        }
        
        cmd.spawn()
            .map_err(|e| format!("Failed to restart: {}", e))?;
    }
    
    #[cfg(not(target_os = "linux"))]
    std::process::Command::new(&exe_path)
        .args(&args)
        .spawn()
        .map_err(|e| format!("Failed to restart: {}", e))?;
    
    println!("✅ [Rust] New process spawned, exiting current...");
    
    std::process::exit(0);
}

// ================= System Integration Commands =================
#[tauri::command]
fn get_display_server() -> String {
    std::env::var("XDG_SESSION_TYPE")
        .unwrap_or_else(|_| "unknown".to_string())
        .to_lowercase()
}

#[tauri::command]
fn check_xvfb_available() -> bool {
    which::which("xvfb-run").is_ok()
}

#[tauri::command]
fn get_connected_monitors() -> Result<Vec<String>, String> {
    #[cfg(target_os = "linux")]
    {
        use std::fs;

        let mut monitors = Vec::new();

        let drm_dir = fs::read_dir("/sys/class/drm")
            .map_err(|e| format!("Failed to read /sys/class/drm: {}", e))?;

        for entry in drm_dir.flatten() {
            let name = entry.file_name();
            let name_str = name.to_string_lossy();

            // 匹配 cardX-XXX 格式（如 card0-eDP-1）
            if name_str.starts_with("card") && name_str.contains('-') {
                let status_path = entry.path().join("status");
                if let Ok(status) = fs::read_to_string(&status_path) {
                    // 精确匹配 "connected"，排除 "disconnected"
                    if status.trim() == "connected" {
                        // 提取显示器名称：去掉 cardX- 前缀
                        let monitor_name = name_str
                            .split_once('-')
                            .map(|(_, rest)| rest.to_string())
                            .unwrap_or_else(|| name_str.to_string());
                        monitors.push(monitor_name);
                    }
                }
            }
        }

        Ok(monitors)
    }

    #[cfg(not(target_os = "linux"))]
    {
        Ok(vec![])
    }
}




// ================= Performance Monitoring Commands =================

#[tauri::command]
async fn start_performance_monitor(
    app: tauri::AppHandle,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    // 使用 compare_exchange 原子操作避免竞态条件
    // 如果当前值是 false，则设置为 true；如果已经是 true，则直接返回
    if state.monitor_running.compare_exchange(
        false,
        true,
        Ordering::SeqCst,
        Ordering::SeqCst
    ).is_err() {
        return Ok(()); // 已经在运行
    }

    let running = state.monitor_running.clone();

    #[cfg(target_os = "linux")]
    let monitor = state.performance_monitor.clone();

    // Spawn background thread for periodic stats emission
    std::thread::spawn(move || {
        while running.load(Ordering::SeqCst) {
            #[cfg(target_os = "linux")]
            {
                if let Ok(monitor) = monitor.lock() {
                    let stats = monitor.get_stats();
                    if let Err(e) = app.emit("performance-update", &stats) {
                        eprintln!("[WARN] Failed to emit performance-update: {:?}", e);
                    }
                }
            }

            #[cfg(not(target_os = "linux"))]
{
                // Emit empty stats on non-Linux platforms
                if let Err(e) = app.emit("performance-update", serde_json::json!({
                    "total_cpu": 0.0,
                    "total_memory_mb": 0.0,
                    "total_threads": 0,
                    "processes": {},
                    "timestamp": 0
                })) {
                    eprintln!("[WARN] Failed to emit performance-update: {:?}", e);
                }
            }

            std::thread::sleep(std::time::Duration::from_secs(1));
        }
    });

    println!("✅ [Rust] Performance monitor started");
    Ok(())
}

#[tauri::command]
async fn stop_performance_monitor(
    state: State<'_, TauriState>,
) -> Result<(), String> {
    state.monitor_running.store(false, Ordering::SeqCst);
    println!("✅ [Rust] Performance monitor stopped");
    Ok(())
}

#[tauri::command]
async fn get_screenshot_history(
    state: State<'_, TauriState>,
) -> Result<Vec<ScreenshotRecord>, String> {
    #[cfg(target_os = "linux")]
    {
        let manager = state.screenshot_history_manager.lock().await;
        Ok(manager.list())
    }

    #[cfg(not(target_os = "linux"))]
    {
        Ok(Vec::new())
    }
}

#[tauri::command]
async fn clear_screenshot_history(
    state: State<'_, TauriState>,
) -> Result<(), String> {
    #[cfg(target_os = "linux")]
    {
        let mut manager = state.screenshot_history_manager.lock().await;
        manager.clear().map_err(|e| format!("Failed to clear: {}", e))?;
    }
    Ok(())
}

#[tauri::command]
async fn take_screenshot(
    wallpaper_id: String,
    output_path: Option<String>,
    state: State<'_, TauriState>,
) -> Result<ScreenshotRecord, String> {
    #[cfg(target_os = "linux")]
    {

        use lwg_core::controller::ScreenshotManager;

        println!("📸 Screenshot requested for wallpaper: {}", wallpaper_id);


        let config = state.config_manager.lock().await.config().clone();

        let path = output_path.unwrap_or_else(|| {
            get_default_screenshot_path(&wallpaper_id, &config.screenshot_res, "png")
        });
        println!("📁 Output path: {}", path);
        println!("⚙️ Config: res={}, prefer_xvfb={}", config.screenshot_res, config.prefer_xvfb);
        
        let shared_config = Arc::new(tokio::sync::Mutex::new(config));
        let screenshot_manager = ScreenshotManager::new(shared_config);

        println!("🚀 Starting screenshot process...");
        let (mut child, tracker) = screenshot_manager
            .take_screenshot_with_monitor(
                &wallpaper_id,
                &path,
                state.performance_monitor.clone(),
            )
            .await
            .map_err(|e| {
                println!("❌ Failed to start: {}", e);
                format!("Failed to start screenshot: {}", e)
            })?;

        println!("✅ Process started with PID: {}", child.id());

        const SCREENSHOT_TIMEOUT_SECS: u64 = 30;

        println!("⏳ Waiting for screenshot (timeout: {}s)...", SCREENSHOT_TIMEOUT_SECS);

        // 获取并校验进程退出状态码
        let status = ScreenshotManager::wait_for_screenshot(
            &mut child,
            &path,
            SCREENSHOT_TIMEOUT_SECS,
            Some(state.performance_monitor.clone()),
            Some(&tracker),
        )
        .await
        .map_err(|e| {
            println!("❌ Wait failed: {}", e);
            format!("Screenshot failed: {}", e)
        })?;
        // 先检查文件是否生成成功（优先于进程状态）
        // 即使进程被 SIGKILL 强制终止，只要文件存在且有效就算成功
        if std::path::Path::new(&path).exists() {
            if let Ok(metadata) = std::fs::metadata(&path) {
                if metadata.len() > 0 {
                    println!("✅ Screenshot file exists: {} ({} bytes)", path, metadata.len());
                    // 文件存在且有效，继续处理（不管进程状态）
                } else {
                    println!("⚠️ Screenshot file is empty: {}", path);
                    return Err("截图文件为空".to_string());
                }
            }
        } else {
            // 文件不存在，才检查进程状态
            if !status.success() {
                let log_msg = std::fs::read_to_string("/tmp/wallpaper_screenshot_error.log").unwrap_or_default();
                println!("❌ Process exited with error: {}\nLogs:\n{}", status, log_msg);
                return Err(format!("截图进程崩溃 ({})。请检查 /tmp/wallpaper_screenshot_error.log", status));
            }
            println!("⚠️ Screenshot file NOT found: {}", path);
            return Err(format!("截图程序已运行完毕，但未能生成文件：{}", path));
        }

        println!("✅ Screenshot process completed");

        // 完成截图并保存历史
        let record = ScreenshotManager::finalize_screenshot(
            tracker,
            wallpaper_id.clone(),
            path.clone(),
            state.performance_monitor.clone(),
        )
        .map_err(|e| format!("Failed to finalize screenshot: {}", e))?;

        // 添加到历史记录
        {
            let mut manager = state.screenshot_history_manager.lock().await;
            manager.add(record.clone()).map_err(|e| format!("Failed to add screenshot history: {}", e))?;
        }

        println!("✅ Screenshot saved: {}", path);
        Ok(record)
    }

    #[cfg(not(target_os = "linux"))]
    {
        Err("Screenshot is only available on Linux".to_string())
    }
}

/// 生成默认截图路径
/// 格式：YYYY-MM-DD_HH-MM-SS_分辨率_壁纸ID.png
///
/// # Arguments
/// * `wallpaper_id` - 壁纸 ID
/// * `resolution` - 分辨率（如 "3840x2160"）
/// * `format` - 图片格式，支持 "png" 或 "jpg"
fn get_default_screenshot_path(wallpaper_id: &str, resolution: &str, format: &str) -> String {
    use std::fs;
    use chrono::Local;

    let home = std::env::var("HOME").unwrap_or_else(|_| "/home".to_string());
    let dir = format!("{}/Pictures/wallpaperengine", home);

    // 创建目录
    if let Err(e) = fs::create_dir_all(&dir) {
        eprintln!("[WARN] Failed to create screenshot directory '{}': {:?}", dir, e);
    }

    let now = Local::now();
    let datetime_str = now.format("%Y-%m-%d_%H:%M:%S").to_string();

    // 确定扩展名
    let extension = if format.to_lowercase() == "png" { "png" } else { "jpg" };

    // 生成文件名：YYYY-MM-DD_HH-MM-SS_分辨率_壁纸 id.{ext}
    let filename = format!("{}_{}_{}.{}", datetime_str, resolution, wallpaper_id, extension);

    format!("{}/{}", dir, filename)
}

#[tauri::command]
async fn open_folder(path: String) -> Result<(), String> {
    #[cfg(target_os = "linux")]
    {
        use std::process::Command;

        // 检查路径是否存在
        let path = std::path::Path::new(&path);
        let folder = if path.is_file() {
            path.parent().unwrap_or(path)
        } else {
            path
        };

        // 尝试真正的文件管理器（跳过 xdg-open，它可能被错误配置）
        let file_managers = ["nautilus", "thunar", "dolphin", "xdg-open"];
        for fm in &file_managers {
            if Command::new(fm).arg(folder).spawn().is_ok() {
                return Ok(());
            }
        }

        Err("No file manager found. Please install xdg-open, nautilus, thunar, or dolphin.".to_string())
    }

    #[cfg(not(target_os = "linux"))]
    {
        let _ = path;
        Err("Open folder is only available on Linux".to_string())
    }
}
#[tauri::command]
async fn open_image(path: String) -> Result<(), String> {
    #[cfg(target_os = "linux")]
    {
        use std::process::Command;

        // 检查文件是否存在
        let path = std::path::Path::new(&path);
        if !path.exists() {
            return Err(format!("File not found: {}", path.display()));
        }

        // 使用 xdg-open 打开图片
        if Command::new("xdg-open").arg(&path).spawn().is_ok() {
            return Ok(());
        }

        Err("Failed to open image. Please ensure xdg-open is installed.".to_string())
    }

    #[cfg(not(target_os = "linux"))]
    {
        let _ = path;
        Err("Open image is only available on Linux".to_string())
    }
}


#[tauri::command]
async fn get_active_wallpapers(
    state: State<'_, TauriState>,
) -> Result<HashMap<String, ActiveWallpaper>, String> {
    #[cfg(target_os = "linux")]
    {
        let controller = state.controller.lock().await;
        let active = controller.get_active_wallpapers().await;
        Ok(active.into_iter().map(|(k, v)| (k, v.into())).collect())
    }

    #[cfg(not(target_os = "linux"))]
    {
        Ok(HashMap::new())
    }
}



// ================= Update Check Commands =================

/// GitHub Release API 响应结构
#[derive(Debug, Deserialize)]
struct GitHubRelease {
    tag_name: String,
    html_url: String,
}

/// 获取应用程序版本号
#[tauri::command]
fn get_app_version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

/// 检查 GitHub 上的最新版本
#[tauri::command]
async fn check_for_updates() -> Result<UpdateCheckResult, String> {
    const GITHUB_API_URL: &str = "https://api.github.com/repos/Suhoiyis/gui-for-linux-wallpaperengine/releases/latest";
    const USER_AGENT: &str = "tauri-app";

    // 获取当前版本（从 Cargo.toml 读取）
    let current_version = env!("CARGO_PKG_VERSION").to_string();

    // 创建 HTTP 客户端，带超时设置
    let client = reqwest::Client::builder()
        .timeout(std::time::Duration::from_secs(30))
        .build()
        .map_err(|e| format!("创建 HTTP 客户端失败: {}", e))?;

    // 发送请求，必须包含 User-Agent 头（GitHub API 强制要求）
    let response = client
        .get(GITHUB_API_URL)
        .header("User-Agent", USER_AGENT)
        .header("Accept", "application/vnd.github.v3+json")
        .send()
        .await
        .map_err(|e| {
            if e.is_timeout() {
                "网络请求超时，请检查网络连接".to_string()
            } else if e.is_connect() {
                "无法连接到 GitHub，请检查网络".to_string()
            } else {
                format!("网络请求失败: {}", e)
            }
        })?;

    // 检查响应状态码
    let status = response.status();
    if status == reqwest::StatusCode::NOT_FOUND {
        // 404: 没有发布版本
        return Ok(UpdateCheckResult {
            has_update: false,
            current_version,
            latest_version: None,
            download_url: None,
        });
    } else if status == reqwest::StatusCode::FORBIDDEN {
        // 403: 速率限制
        return Err("请求过于频繁，请稍后再试".to_string());
    } else if !status.is_success() {
        return Err(format!("GitHub API 返回错误: {}", status));
    }

    // 解析 JSON 响应
    let release: GitHubRelease = response
        .json()
        .await
        .map_err(|e| format!("解析响应失败: {}", e))?;

    // 版本比较：移除 'v' 前缀后比较
    let latest_version = release.tag_name.trim_start_matches('v').to_string();
    let current_normalized = current_version.trim_start_matches('v');

    let has_update = latest_version != current_normalized;

    Ok(UpdateCheckResult {
        has_update,
        current_version,
        latest_version: Some(release.tag_name),
        download_url: Some(release.html_url),
    })
}

// ================= 日志命令 =================

#[cfg(target_os = "linux")]
#[tauri::command]
async fn get_logs(state: State<'_, TauriState>) -> Result<Vec<LogEntry>, String> {
    let lm = state.log_manager.lock().map_err(|e| format!("Lock error: {}", e))?;
    Ok(lm.get_logs())
}

#[cfg(target_os = "linux")]
#[tauri::command]
async fn clear_logs(state: State<'_, TauriState>) -> Result<(), String> {
    let lm = state.log_manager.lock().map_err(|e| format!("Lock error: {}", e))?;
    lm.clear();
    Ok(())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn get_logs() -> Result<Vec<serde_json::Value>, String> {
    Ok(vec![])
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn clear_logs() -> Result<(), String> {
    Ok(())
}

// ================= 壁纸轮换命令 =================

/// Favorites 虚拟播放列表的特殊 ID
const FAVORITES_PLAYLIST_ID: &str = "__favorites__";

/// 选择下一张壁纸（纯函数，无副作用）
#[cfg(target_os = "linux")]
fn select_next_wallpaper(
    order: &str,
    current_id: Option<&str>,
    all_ids: &[String],
    cycle_playlist_id: Option<&str>,
    playlists: &[LwgPlaylist],
    favorite_ids: &[String],
) -> String {
    use std::collections::HashSet;

    let valid_ids: HashSet<&String> = all_ids.iter().collect();

    let candidate_ids: Vec<String> = if let Some(playlist_id) = cycle_playlist_id {
        if playlist_id == FAVORITES_PLAYLIST_ID {
            let valid_favorites: Vec<String> = favorite_ids
                .iter()
                .filter(|id| valid_ids.contains(id))
                .cloned()
                .collect();

            if valid_favorites.is_empty() {
                all_ids.to_vec()
            } else {
                valid_favorites
            }
        } else {
            let playlist_wallpapers = playlists
                .iter()
                .find(|p| p.id == playlist_id)
                .map(|p| p.wallpaper_ids.clone());

            match playlist_wallpapers {
                Some(ids) => {
                    let valid_playlist_ids: Vec<String> = ids
                        .iter()
                        .filter(|id| valid_ids.contains(id))
                        .cloned()
                        .collect();

                    if valid_playlist_ids.is_empty() {
                        all_ids.to_vec()
                    } else {
                        valid_playlist_ids
                    }
                }
                None => all_ids.to_vec(),
            }
        }
    } else {
        all_ids.to_vec()
    };

    if candidate_ids.is_empty() {
        return String::new();
    }

    match order {
        "random" => {
            use rand::seq::IndexedRandom;
            candidate_ids.choose(&mut rand::rng()).unwrap().clone()
        }
        "id" | _ => {
            let mut sorted = candidate_ids.to_vec();
            sorted.sort();

            let next_index = if let Some(current) = current_id {
                let current_index = sorted.iter()
                    .position(|id| id == current)
                    .unwrap_or(0);
                (current_index + 1) % sorted.len()
            } else {
                0
            };

            sorted[next_index].clone()
        }
    }
}

/// 执行一次轮换
/// 
/// ⚠️ 死锁防护：此函数严格遵守"锁的粒度极细"原则
/// 所有 .await 操作执行前，必须确保没有任何 Mutex 锁被持有
#[cfg(target_os = "linux")]
async fn trigger_cycle_internal(app: &tauri::AppHandle) -> Result<(), String> {
    let state = app.state::<TauriState>();

    // 步骤 1：快速获取配置（纯读取，立刻释放锁）
    let (cycle_order, cycle_screen, cycle_playlist_id, playlists) = {
        let (order, playlist_id, plists) = {
            let cm = state.config_manager.lock().await;
            (
                cm.config().cycle_order.clone(),
                cm.config().cycle_playlist_id.clone(),
                cm.config().playlists.clone(),
            )
        };
        let screen = state.cycle_screen.lock().await.clone();
        (order, screen, playlist_id, plists)
    };

    // 步骤 2：从缓存获取壁纸 ID 列表
    let all_wallpaper_ids = {
        let cache = state.cached_wallpaper_ids.read()
            .map_err(|e| format!("Cache read error: {}", e))?;
        cache.clone()
    };

    if all_wallpaper_ids.is_empty() {
        return Err("No wallpapers in cache. Please refresh wallpaper library.".to_string());
    }

    // 步骤 2.5：获取收藏壁纸 ID 列表
    let favorite_ids = {
        let fm = state.favorite_manager.lock().await;
        fm.list()
    };

    // 步骤 3：快速获取当前活跃状态（立刻释放锁）
    let active_state = {
        let controller = state.controller.lock().await;
        controller.get_active_wallpapers().await
    };

    if active_state.is_empty() {
        return Err("No active wallpapers to cycle.".to_string());
    }

    // 步骤 4：纯内存计算（无需任何锁）
    let mut new_state = active_state.clone();
    let mut cycled_wallpaper_id = String::new();

    if cycle_screen == "all" {
        let new_wp_id = select_next_wallpaper(
            &cycle_order,
            None,
            &all_wallpaper_ids,
            cycle_playlist_id.as_deref(),
            &playlists,
            &favorite_ids,
        );
        cycled_wallpaper_id = new_wp_id.clone();

        for (_, aw) in &mut new_state {
            aw.wallpaper_id = new_wp_id.clone();
            aw.is_playing = true;
        }
    } else {
        if let Some(aw) = new_state.get_mut(&cycle_screen) {
            let new_wp_id = select_next_wallpaper(
                &cycle_order,
                Some(&aw.wallpaper_id),
                &all_wallpaper_ids,
                cycle_playlist_id.as_deref(),
                &playlists,
                &favorite_ids,
            );
            cycled_wallpaper_id = new_wp_id.clone();
            aw.wallpaper_id = new_wp_id;
            aw.is_playing = true;
        }
    }

    // 步骤 5：快速同步内存状态（立刻释放锁）
    {
        let mut controller = state.controller.lock().await;
        controller.sync_state(new_state.clone()).await;
    }

    // 步骤 6：持久化状态
    {
        let mut sm = state.state_manager.lock().await;
        *sm.state_mut() = new_state.iter()
            .map(|(k, v)| (k.clone(), LwgActiveWallpaper {
                wallpaper_id: v.wallpaper_id.clone(),
                is_playing: v.is_playing,
            }))
            .collect();
        if let Err(e) = sm.save() {
            eprintln!("[ERROR] Failed to save state after cycle: {:?}", e);
        }
    }

    // 步骤 7：执行耗时的进程重启（不持有任何锁！）
    {
        let mut controller = state.controller.lock().await;
        controller.restart_wallpapers().await
            .map_err(|e| format!("Restart error: {:?}", e))?;
    }

    // 步骤 8：发送事件通知前端（包含壁纸 ID）
    if let Err(e) = app.emit("wallpaper-cycled", &cycled_wallpaper_id) {
        eprintln!("[ERROR] Failed to emit wallpaper-cycled event: {:?}", e);
    }

    // 记录日志
    if let Ok(lm) = state.log_manager.lock() {
        lm.info(LogSource::GUI, &format!("Wallpaper cycled ({})", cycle_order));
    }

    Ok(())
}

// ================= Playlist 命令 =================

/// 获取所有播放列表
#[cfg(target_os = "linux")]
#[tauri::command]
async fn get_playlists(
    state: State<'_, TauriState>,
) -> Result<Vec<Playlist>, String> {
    let cm = state.config_manager.lock().await;
    Ok(cm.config().playlists.iter().map(|p| p.clone().into()).collect())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn get_playlists() -> Result<Vec<Playlist>, String> {
    Ok(vec![])
}

/// 创建播放列表
#[cfg(target_os = "linux")]
#[tauri::command]
async fn create_playlist(
    id: String,
    name: String,
    wallpaper_ids: Vec<String>,
    state: State<'_, TauriState>,
) -> Result<Playlist, String> {
    let name = name.trim();
    if name.is_empty() {
        return Err("Playlist name cannot be empty".to_string());
    }
    if id.is_empty() || id.len() != 36 {
        return Err("Invalid playlist ID format".to_string());
    }

    {
        let cm = state.config_manager.lock().await;
        if cm.config().playlists.iter().any(|p| p.id == id) {
            return Err(format!("Playlist with ID {} already exists", id));
        }
    }

    let mut seen = std::collections::HashSet::new();
    let deduped_ids: Vec<String> = wallpaper_ids
        .into_iter()
        .filter(|id| seen.insert(id.clone()))
        .collect();

    let now = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_secs();

    let playlist = LwgPlaylist {
        id,
        name: name.to_string(),
        wallpaper_ids: deduped_ids,
        created_at: now,
        updated_at: now,
    };

    let result = playlist.clone();
    {
        let mut cm = state.config_manager.lock().await;
        cm.config_mut().playlists.push(playlist);
        cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    }

    Ok(result.into())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn create_playlist(
    id: String,
    name: String,
    wallpaper_ids: Vec<String>,
) -> Result<Playlist, String> {
    let now = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_secs();
    Ok(Playlist {
        id,
        name,
        wallpaper_ids,
        created_at: now,
        updated_at: now,
    })
}

/// 更新播放列表
#[cfg(target_os = "linux")]
#[tauri::command]
async fn update_playlist(
    id: String,
    name: Option<String>,
    wallpaper_ids: Option<Vec<String>>,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    let mut cm = state.config_manager.lock().await;

    let playlist = cm.config_mut()
        .playlists
        .iter_mut()
        .find(|p| p.id == id)
        .ok_or_else(|| format!("Playlist not found: {}", id))?;

    if let Some(n) = name {
        let n = n.trim();
        if n.is_empty() {
            return Err("Playlist name cannot be empty".to_string());
        }
        playlist.name = n.to_string();
    }

    if let Some(ids) = wallpaper_ids {
        let mut seen = std::collections::HashSet::new();
        let deduped_ids: Vec<String> = ids
            .into_iter()
            .filter(|id| seen.insert(id.clone()))
            .collect();
        playlist.wallpaper_ids = deduped_ids;
    }

    playlist.updated_at = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_secs();

    cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    Ok(())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn update_playlist(
    _id: String,
    _name: Option<String>,
    _wallpaper_ids: Option<Vec<String>>,
) -> Result<(), String> {
    Ok(())
}

/// 删除播放列表
#[cfg(target_os = "linux")]
#[tauri::command]
async fn delete_playlist(
    id: String,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    let mut cm = state.config_manager.lock().await;

    let index = cm.config()
        .playlists
        .iter()
        .position(|p| p.id == id)
        .ok_or_else(|| format!("Playlist not found: {}", id))?;

    cm.config_mut().playlists.remove(index);

    if cm.config().cycle_playlist_id.as_ref() == Some(&id) {
        cm.config_mut().cycle_playlist_id = None;
    }

    cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    Ok(())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn delete_playlist(_id: String) -> Result<(), String> {
    Ok(())
}

/// 重排序播放列表
#[cfg(target_os = "linux")]
#[tauri::command]
async fn reorder_playlists(
    ordered_ids: Vec<String>,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    let mut cm = state.config_manager.lock().await;

    let id_to_playlist: std::collections::HashMap<String, LwgPlaylist> = cm.config()
        .playlists
        .iter()
        .map(|p| (p.id.clone(), p.clone()))
        .collect();

    let mut new_playlists: Vec<LwgPlaylist> = Vec::new();
    let mut processed_ids: std::collections::HashSet<String> = std::collections::HashSet::new();

    for id in &ordered_ids {
        if let Some(playlist) = id_to_playlist.get(id) {
            new_playlists.push(playlist.clone());
            processed_ids.insert(id.clone());
        }
    }

    for playlist in &cm.config().playlists {
        if !processed_ids.contains(&playlist.id) {
            new_playlists.push(playlist.clone());
        }
    }

    cm.config_mut().playlists = new_playlists;
    cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    Ok(())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn reorder_playlists(_ordered_ids: Vec<String>) -> Result<(), String> {
    Ok(())
}

/// 设置轮换播放列表
/// 
/// 支持的特殊 ID：
/// - `__favorites__`: 使用收藏壁纸作为轮换源
#[cfg(target_os = "linux")]
#[tauri::command]
async fn set_cycle_playlist(
    id: Option<String>,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    let mut cm = state.config_manager.lock().await;

    if let Some(ref playlist_id) = id {
        if playlist_id != FAVORITES_PLAYLIST_ID {
            let exists = cm.config()
                .playlists
                .iter()
                .any(|p| &p.id == playlist_id);

            if !exists {
                return Err(format!("Playlist not found: {}", playlist_id));
            }
        }
    }

    cm.config_mut().cycle_playlist_id = id;
    cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    Ok(())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn set_cycle_playlist(_id: Option<String>) -> Result<(), String> {
    Ok(())
}

/// 获取当前轮换播放列表 ID
#[cfg(target_os = "linux")]
#[tauri::command]
async fn get_cycle_playlist(
    state: State<'_, TauriState>,
) -> Result<Option<String>, String> {
    let cm = state.config_manager.lock().await;
    Ok(cm.config().cycle_playlist_id.clone())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn get_cycle_playlist() -> Result<Option<String>, String> {
    Ok(None)
}

/// 获取侧边栏显示状态
#[cfg(target_os = "linux")]
#[tauri::command]
async fn get_playlist_sidebar_open(
    state: State<'_, TauriState>,
) -> Result<bool, String> {
    let cm = state.config_manager.lock().await;
    Ok(cm.config().playlist_sidebar_open)
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn get_playlist_sidebar_open() -> Result<bool, String> {
    Ok(true)
}

/// 设置侧边栏状态
#[cfg(target_os = "linux")]
#[tauri::command]
async fn set_playlist_sidebar_open(
    open: bool,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    let mut cm = state.config_manager.lock().await;
    cm.config_mut().playlist_sidebar_open = open;
    cm.save().map_err(|e| format!("Failed to save: {:?}", e))?;
    Ok(())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn set_playlist_sidebar_open(_open: bool) -> Result<(), String> {
    Ok(())
}

/// 启动轮换定时器
#[cfg(target_os = "linux")]
#[tauri::command]
async fn start_cycle_timer(
    app: tauri::AppHandle,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    // 1. 停止现有定时器（如果存在）
    {
        let mut task_guard = state.cycle_task.lock().await;
        if let Some(task) = task_guard.take() {
            state.cycle_running.store(false, Ordering::SeqCst);
            task.abort();
        }
    }

    // 2. 读取配置（快速获取，立刻释放锁）
    let interval_mins = {
        let cm = state.config_manager.lock().await;
        cm.config().cycle_interval.max(1)
    };

    // 3. 设置运行标志
    state.cycle_running.store(true, Ordering::SeqCst);

    // 4. 启动后台任务
    let running = state.cycle_running.clone();
    let app_handle = app.clone();

    let task = tokio::spawn(async move {
        let mut interval = tokio::time::interval(
            std::time::Duration::from_secs(interval_mins as u64 * 60)
        );

        while running.load(Ordering::SeqCst) {
            interval.tick().await;
            if !running.load(Ordering::SeqCst) {
                break;
            }

            if let Err(e) = trigger_cycle_internal(&app_handle).await {
                eprintln!("[Cycle] Error: {}", e);
            }
        }
    });

    // 5. 保存任务句柄
    *state.cycle_task.lock().await = Some(task);

    // 记录日志
    if let Ok(lm) = state.log_manager.lock() {
        lm.info(LogSource::GUI, &format!("Wallpaper cycling enabled (every {} mins)", interval_mins));
    }

    Ok(())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn start_cycle_timer() -> Result<(), String> {
    Ok(())
}

/// 停止轮换定时器
#[cfg(target_os = "linux")]
#[tauri::command]
async fn stop_cycle_timer(state: State<'_, TauriState>) -> Result<(), String> {
    state.cycle_running.store(false, Ordering::SeqCst);

    {
        let mut task_guard = state.cycle_task.lock().await;
        if let Some(task) = task_guard.take() {
            task.abort();
        }
    }

    if let Ok(lm) = state.log_manager.lock() {
        lm.info(LogSource::GUI, "Wallpaper cycling disabled");
    }

    Ok(())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn stop_cycle_timer() -> Result<(), String> {
    Ok(())
}

/// 设置轮换目标屏幕
#[cfg(target_os = "linux")]
#[tauri::command]
async fn set_cycle_screen(
    screen: String,
    state: State<'_, TauriState>,
) -> Result<(), String> {
    let mut cycle_screen = state.cycle_screen.lock().await;
    *cycle_screen = screen;
    Ok(())
}

#[cfg(not(target_os = "linux"))]
#[tauri::command]
async fn set_cycle_screen(_screen: String) -> Result<(), String> {
    Ok(())
}

// ================= 主入口 =================

pub fn run() {
    // 跨平台初始化状态
    #[cfg(target_os = "linux")]
    let app_state = {
        println!("🐧 [Linux] 初始化应用状态...");
        let mut config_manager = LwgConfigManager::new().expect("Failed to create ConfigManager");
        let state_manager = StateManager::new().expect("Failed to create StateManager");
        let history_manager = HistoryManager::new().expect("Failed to create HistoryManager");
        let screenshot_history_manager = ScreenshotHistoryManager::new().expect("Failed to create ScreenshotHistoryManager");
        
        // 初始化 NicknameManager
        let mut nickname_manager = NicknameManager::new().expect("Failed to create NicknameManager");
        
        // 迁移旧的 wallpaperNicknames 数据（如果存在）
        let old_nicknames = config_manager.config().wallpaper_nicknames.clone();
        if !old_nicknames.is_empty() {
            println!("🔄 [Migration] Migrating {} nicknames from config.json to nicknames.json", old_nicknames.len());
            let json = serde_json::to_value(&old_nicknames).unwrap_or(serde_json::Value::Object(serde_json::Map::new()));
            if let Err(e) = nickname_manager.load_from_config(&json) {
                eprintln!("⚠️ [Migration] Failed to migrate nicknames: {}", e);
            } else if let Err(e) = nickname_manager.save() {
                eprintln!("⚠️ [Migration] Failed to save migrated nicknames: {}", e);
            } else {
                // 清空 config 中的旧数据
                config_manager.config_mut().wallpaper_nicknames.clear();
                if let Err(e) = config_manager.save() {
                    eprintln!("⚠️ [Migration] Failed to clear old nicknames from config: {}", e);
                } else {
                    println!("✅ [Migration] Nicknames migrated successfully");
                }
            }
        }
        
        // 初始化 FavoriteManager
        let favorite_manager = FavoriteManager::new().expect("Failed to create FavoriteManager");
        
        let shared_config = Arc::new(tokio::sync::Mutex::new(config_manager.config().clone()));
        let shared_state = Arc::new(tokio::sync::Mutex::new(state_manager.state().clone()));
        let performance_monitor = Arc::new(std::sync::Mutex::new(PerformanceMonitor::new()));
        let mut controller = WallpaperController::new(shared_config.clone(), shared_state);
        controller.set_performance_monitor(performance_monitor.clone());

        // 创建日志管理器
        let log_manager = Arc::new(std::sync::Mutex::new(LogManager::new()));
        controller.set_log_manager(log_manager.clone());

        // ✨ 检测已运行的壁纸进程
        let detected = WallpaperController::detect_existing_processes();
        if !detected.is_empty() {
            println!("🔍 检测到 {} 个已运行的壁纸进程", detected.len());

            // 更新 state.active_monitors (now in shared state, not config)
            let state = shared_config.blocking_lock();
            let mut detected_pids = HashMap::new();

            for (screen, (pid, wp_id)) in &detected {
                // Note: active_monitors now tracked via controller's state
                detected_pids.insert(screen.clone(), *pid);
                println!("  屏幕 {}: PID {}, 壁纸 {}", screen, pid, wp_id);
            }
            drop(state);

            // 注入 detected_pids 到 controller
            controller.set_detected_pids(detected_pids);
        }

        // 初始化壁纸 ID 缓存（用于轮换功能）
        let cached_wallpaper_ids = {
            let workshop_path = config_manager.config().workshop_path.clone()
                .unwrap_or_else(|| get_default_workshop_path());
            let mut wm = WallpaperManager::new(&workshop_path);
            let ids = if let Ok(wallpapers) = wm.scan() {
                wallpapers.values().map(|w| w.id.clone()).collect()
            } else {
                Vec::new()
            };
            println!("🔄 [Init] 壁纸缓存初始化: {} 张", ids.len());
            Arc::new(std::sync::RwLock::new(ids))
        };

        // 初始化轮换屏幕选择为 "all"
        let cycle_screen = Arc::new(Mutex::new("all".to_string()));

        TauriState {
            controller: Mutex::new(controller),
            config_manager: Mutex::new(config_manager),
            state_manager: Mutex::new(state_manager),
            history_manager: Mutex::new(history_manager),
            screenshot_history_manager: Mutex::new(screenshot_history_manager),
            performance_monitor,
            log_manager,
            nickname_manager: Mutex::new(nickname_manager),
            favorite_manager: Mutex::new(favorite_manager),
            monitor_running: Arc::new(AtomicBool::new(false)),
            cycle_task: Arc::new(Mutex::new(None)),
            cycle_running: Arc::new(AtomicBool::new(false)),
            cycle_screen,
            cached_wallpaper_ids,
        }

    };

    #[cfg(not(target_os = "linux"))]
    let app_state = {
        println!("🪟 [Windows Mock] 初始化 Mock 应用状态...");
        TauriState {
            _dummy: true,
            monitor_running: Arc::new(AtomicBool::new(false)),
            cycle_running: Arc::new(AtomicBool::new(false)),
        }
    };

    // Clone log_manager BEFORE managing app_state (moved into .manage())
    #[cfg(target_os = "linux")]
    let log_manager_for_emit = app_state.log_manager.clone();

    tauri::Builder::default()
        .manage(app_state)
        .setup(move |app| {
            // ── Clean up legacy autostart file (migration) ─────────────────────────
            if let Some(config_dir) = dirs::config_dir() {
                let old_autostart_path = config_dir.join("autostart/linux-wallpaperengine-gui.desktop");
                if old_autostart_path.exists() {
                    let _ = std::fs::remove_file(&old_autostart_path);
                    println!("🧹 [Migration] Removed legacy autostart file: {:?}", old_autostart_path);
                }
            }

            // ── Handle --hidden parameter (window visibility) ───────────────────────
            let args: Vec<String> = std::env::args().collect();
            let start_hidden = args.contains(&"--hidden".to_string());

            if !start_hidden {
                if let Some(window) = app.get_webview_window("main") {
                    let _ = window.show();
                    let _ = window.set_focus();
                }
            }

            // ── System tray ───────────────────────────────────────────────────
            #[cfg(target_os = "linux")]
            tray::setup_tray(app)?;

            // Register log subscriber to emit log-entry events to frontend
            #[cfg(target_os = "linux")]
            {
                let app_handle = app.handle().clone();
                if let Ok(lm) = log_manager_for_emit.lock() {
                    lm.subscribe(move |entry| {
                        if let Err(e) = app_handle.emit("log-entry", entry) {
                            eprintln!("[WARN] Failed to emit log-entry: {:?}", e);
                        }
                    });
                }
            }

            // 输出启动日志
            #[cfg(target_os = "linux")]
            {
                if let Ok(lm) = log_manager_for_emit.lock() {
                    lm.info(LogSource::GUI, "LWG GUI started successfully");
                }
            }

            // ✨ Auto-restore wallpapers on startup
            #[cfg(target_os = "linux")]
            {
                let app_handle = app.handle().clone();

                tauri::async_runtime::spawn(async move {
                    let tauri_state = app_handle.state::<TauriState>();

                    let auto_restore = {
                        let cm = tauri_state.config_manager.lock().await;
                        cm.config().auto_restore
                    };

                    if auto_restore {
                        let has_active = {
                            let controller = tauri_state.controller.lock().await;
                            let active = controller.get_active_wallpapers().await;
                            active.values().any(|aw| aw.is_playing)
                        };

                        if has_active {
                            println!("🔄 [Auto-Restore] Restoring wallpapers...");
                            let mut controller = tauri_state.controller.lock().await;
                            match controller.restart_wallpapers().await {
                                Ok(()) => {
                                    println!("✅ [Auto-Restore] Wallpapers restored successfully");
                                    let _ = app_handle.emit("wallpaper-changed", ());
                                }
                                Err(e) => {
                                    eprintln!("❌ [Auto-Restore] Failed to restore wallpapers: {:?}", e);
                                }
                            }
                        }
                    }
                });
            }

            // ✨ Auto-start cycle timer if enabled
            #[cfg(target_os = "linux")]
            {
                let app_handle = app.handle().clone();

                tauri::async_runtime::spawn(async move {
                    let tauri_state = app_handle.state::<TauriState>();

                    let cycle_enabled = {
                        let cm = tauri_state.config_manager.lock().await;
                        cm.config().cycle_enabled
                    };

                    if cycle_enabled {
                        println!("🔄 [Auto-Cycle] Starting cycle timer on startup...");
                        
                        // 停止现有定时器
                        {
                            let mut task_guard = tauri_state.cycle_task.lock().await;
                            if let Some(task) = task_guard.take() {
                                tauri_state.cycle_running.store(false, Ordering::SeqCst);
                                task.abort();
                            }
                        }

                        // 读取配置
                        let interval_mins = {
                            let cm = tauri_state.config_manager.lock().await;
                            cm.config().cycle_interval.max(1)
                        };

                        // 设置运行标志
                        tauri_state.cycle_running.store(true, Ordering::SeqCst);

                        // 启动后台任务
                        let running = tauri_state.cycle_running.clone();
                        let app = app_handle.clone();

                        let task = tokio::spawn(async move {
                            let mut interval = tokio::time::interval(
                                std::time::Duration::from_secs(interval_mins as u64 * 60)
                            );

                            while running.load(Ordering::SeqCst) {
                                interval.tick().await;
                                if !running.load(Ordering::SeqCst) {
                                    break;
                                }

                                if let Err(e) = trigger_cycle_internal(&app).await {
                                    eprintln!("[Cycle] Error: {}", e);
                                }
                            }
                        });

                        *tauri_state.cycle_task.lock().await = Some(task);
                        println!("✅ [Auto-Cycle] Cycle timer started (every {} mins)", interval_mins);
                    }
                });
            }

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            get_wallpapers,
            apply_wallpaper,
            stop_wallpaper,
            delete_wallpaper,
            // Settings commands
            // Settings commands
            // Settings commands
            // Settings commands
            get_settings,
            save_settings,
            update_config_value,
            restart_wallpapers,
            // App lifecycle commands
            quit_app,
            restart_app,
            // State commands
            get_state,
            save_state,
            add_history,
            get_history,
            clear_history,
            // Nickname commands
            get_nicknames,
            set_nickname,
            // Favorite commands
            get_favorites,
            toggle_favorite,
            // System integration commands
            get_display_server,
            check_xvfb_available,
            get_connected_monitors,
            // Performance monitoring commands
            start_performance_monitor,
            stop_performance_monitor,
            get_screenshot_history,
            clear_screenshot_history,
            take_screenshot,
            // Active wallpaper commands
            get_active_wallpapers,
            open_folder,
            open_image,
            // Log commands
            get_logs,
            clear_logs,
            // Update check commands
            check_for_updates,
            get_app_version,
            // Playlist commands
            get_playlists,
            create_playlist,
            update_playlist,
            delete_playlist,
            reorder_playlists,
            set_cycle_playlist,
            get_cycle_playlist,
            get_playlist_sidebar_open,
            set_playlist_sidebar_open,
            // Cycle commands
            start_cycle_timer,
            stop_cycle_timer,
            set_cycle_screen,
        ])
        .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
            if let Some(window) = app.get_webview_window("main") {
                let _ = window.unminimize();
                let _ = window.show();
                let _ = window.set_focus();
            }
        }))
        .plugin(tauri_plugin_autostart::init(
            MacosLauncher::LaunchAgent,
            Some(vec!["--hidden"]),
        ))
        .plugin(
            tauri_plugin_window_state::Builder::default()
                .with_state_flags(StateFlags::POSITION | StateFlags::SIZE | StateFlags::MAXIMIZED)
                .build()
        )
        .plugin(tauri_plugin_notification::init())
        .plugin(tauri_plugin_opener::Builder::new().build())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_dialog::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
