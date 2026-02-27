use lwg_core::wallpaper::WallpaperManager;
use lwg_core::config::{ConfigManager, AppConfig};
use lwg_core::controller::WallpaperController;
use lwg_core::performance::PerformanceMonitor;
use lwg_core::screen::ScreenManager;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::Mutex;
use tauri::Manager;

// Shared state
pub struct AppState {
    pub wallpaper_manager: Arc<Mutex<Option<WallpaperManager>>>,
    pub config: Arc<Mutex<AppConfig>>,
    pub controller: Arc<Mutex<WallpaperController>>,
    pub perf_monitor: Arc<Mutex<PerformanceMonitor>>,
}

// Wallpaper data for frontend
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WallpaperData {
    pub id: String,
    pub title: String,
    pub preview: String,
    pub wp_type: String,
    pub size: u64,
}

impl From<lwg_core::wallpaper::Wallpaper> for WallpaperData {
    fn from(wp: lwg_core::wallpaper::Wallpaper) -> Self {
        Self {
            id: wp.id,
            title: wp.title,
            preview: wp.preview.to_string_lossy().to_string(),
            wp_type: wp.wp_type,
            size: wp.size,
        }
    }
}

// Performance stats for frontend
#[derive(Debug, Clone, Serialize)]
pub struct PerformanceStats {
    pub cpu: f32,
    pub memory: f32,
}

// Tauri Commands
#[tauri::command]
async fn scan_wallpapers(state: tauri::State<'_, AppState>) -> Result<Vec<WallpaperData>, String> {
    let mut wm_guard = state.wallpaper_manager.lock().await;
    
    // Auto-detect workshop path if not initialized
    if wm_guard.is_none() {
        let home = std::env::var("HOME").unwrap_or_default();
        let possible_paths = vec![
            format!("{}/.local/share/Steam/steamapps/workshop/content/431960", home),
            format!("{}/.steam/steam/steamapps/workshop/content/431960", home),
            format!("{}/.steam/root/steamapps/workshop/content/431960", home),
        ];
        
        for path in possible_paths {
            if std::path::Path::new(&path).exists() {
                let mut wm = WallpaperManager::new(path);
                if wm.scan().is_ok() {
                    *wm_guard = Some(wm);
                    break;
                }
            }
        }
    }
    
    if let Some(ref wm) = *wm_guard {
        match wm.scan() {
            Ok(wallpapers) => {
                let data: Vec<WallpaperData> = wallpapers.values()
                    .cloned()
                    .map(WallpaperData::from)
                    .collect();
                Ok(data)
            }
            Err(e) => Err(format!("Failed to scan wallpapers: {}", e))
        }
    } else {
        Err("No workshop path found. Please configure assets_path.".to_string())
    }
}

#[tauri::command]
async fn apply_wallpaper(id: String, state: tauri::State<'_, AppState>) -> Result<(), String> {
    let controller = state.controller.lock().await;
    controller.apply(&id, None).await
        .map_err(|e| format!("Failed to apply wallpaper: {:?}", e))
}

#[tauri::command]
async fn open_wallpaper_folder(id: String, state: tauri::State<'_, AppState>) -> Result<(), String> {
    let wm_guard = state.wallpaper_manager.lock().await;
    
    if let Some(ref wm) = *wm_guard {
        if let Some(wp) = wm.get(&id) {
            let path = wp.preview.parent().unwrap_or(&wp.preview);
            
            // Try file managers
            for fm in &["thunar", "nautilus", "dolphin", "xdg-open"] {
                if which::which(fm).is_ok() {
                    std::process::Command::new(fm)
                        .arg(path)
                        .spawn()
                        .map_err(|e| format!("Failed to open folder: {}", e))?;
                    return Ok(());
                }
            }
        }
    }
    
    Err("Wallpaper not found".to_string())
}

#[tauri::command]
async fn delete_wallpaper(id: String, state: tauri::State<'_, AppState>) -> Result<bool, String> {
    let mut wm_guard = state.wallpaper_manager.lock().await;
    
    if let Some(ref mut wm) = *wm_guard {
        wm.delete(&id)
            .map_err(|e| format!("Failed to delete wallpaper: {}", e))
    } else {
        Err("Wallpaper manager not initialized".to_string())
    }
}

#[tauri::command]
async fn get_performance_stats(state: tauri::State<'_, AppState>) -> Result<PerformanceStats, String> {
    let monitor = state.perf_monitor.lock().await;
    let stats = monitor.get_stats();
    Ok(PerformanceStats {
        cpu: stats.total_cpu,
        memory: stats.total_memory_mb,
    })
}

#[tauri::command]
async fn get_screens() -> Result<Vec<String>, String> {
    let screen_manager = ScreenManager::new();
    Ok(screen_manager.names())
}

#[tauri::command]
async fn get_config(state: tauri::State<'_, AppState>) -> Result<AppConfig, String> {
    let config = state.config.lock().await;
    Ok(config.clone())
}

#[tauri::command]
async fn save_config(key: String, value: serde_json::Value, state: tauri::State<'_, AppState>) -> Result<(), String> {
    let mut config = state.config.lock().await;
    
    match key.as_str() {
        "fps" => if let Some(v) = value.as_u64() { config.fps = v as u32; },
        "volume" => if let Some(v) = value.as_u64() { config.volume = v as u32; },
        "silence" => if let Some(v) = value.as_bool() { config.silence = v; },
        "scaling" => if let Some(v) = value.as_str() { config.scaling = v.to_string(); },
        "no_fullscreen_pause" => if let Some(v) = value.as_bool() { config.no_fullscreen_pause = v; },
        "disable_mouse" => if let Some(v) = value.as_bool() { config.disable_mouse = v; },
        "no_auto_mute" => if let Some(v) = value.as_bool() { config.no_auto_mute = v; },
        "no_audio_processing" => if let Some(v) = value.as_bool() { config.no_audio_processing = v; },
        "disable_parallax" => if let Some(v) = value.as_bool() { config.disable_parallax = v; },
        "disable_particles" => if let Some(v) = value.as_bool() { config.disable_particles = v; },
        "clamping" => if let Some(v) = value.as_str() { config.clamping = v.to_string(); },
        _ => return Err(format!("Unknown config key: {}", key)),
    }
    
    Ok(())
}

// Run the application
pub fn run() {
    // Initialize config
    let config_manager = ConfigManager::new().expect("Failed to initialize config manager");
    let config = Arc::new(Mutex::new(config_manager.config.clone()));
    
    // Initialize controller
    let controller = Arc::new(Mutex::new(WallpaperController::new(config.clone())));
    
    // Initialize performance monitor
    let perf_monitor = Arc::new(Mutex::new(PerformanceMonitor::new()));
    
    // Initialize wallpaper manager (lazy)
    let wallpaper_manager = Arc::new(Mutex::new(None));
    
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(AppState {
            wallpaper_manager,
            config,
            controller,
            perf_monitor,
        })
        .invoke_handler(tauri::generate_handler![
            scan_wallpapers,
            apply_wallpaper,
            open_wallpaper_folder,
            delete_wallpaper,
            get_performance_stats,
            get_screens,
            get_config,
            save_config,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}