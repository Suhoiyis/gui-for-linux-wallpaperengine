// =============================================================================
// tray.rs — Tauri v2 native system tray
// Replaces the legacy standalone `tray_rs` process.
// Features:
//   - Left-click to toggle main window visibility
//   - Right-click context menu: Show Window / Play·Stop / Random / Quit
//   - State-aware icon (colored = running, grayscale = stopped)
//   - Dynamic tooltip showing engine running state
//   - Background polling loop (2s interval) to keep icon/tooltip fresh
// =============================================================================

use std::fs;
use std::path::Path;
use std::sync::{Arc, atomic::{AtomicBool, Ordering}};
use std::thread;
use std::time::Duration;

use tauri::{
    App, AppHandle, Emitter, Manager,
    image::Image,
    menu::{MenuBuilder, MenuItemBuilder, PredefinedMenuItem},
    tray::{TrayIconBuilder, TrayIconEvent, MouseButton, MouseButtonState},
};

// ─── Engine detection (ported from tray_rs) ──────────────────────────────────

/// Returns true if `linux-wallpaperengine` is currently running in /proc.
pub fn is_engine_running() -> bool {
    let Ok(entries) = fs::read_dir("/proc") else { return false; };
    for entry in entries.flatten() {
        let name = entry.file_name();
        let name = name.to_string_lossy();
        if !name.chars().all(|c| c.is_ascii_digit()) {
            continue;
        }
        // Try /proc/{pid}/exe first (fast)
        let exe_path = entry.path().join("exe");
        if let Ok(target) = fs::read_link(&exe_path) {
            if let Some(fname) = target.file_name().and_then(|s| s.to_str()) {
                if fname == "linux-wallpaperengine" {
                    return true;
                }
            }
        } else {
            // Fallback: read cmdline
            let cmdline_path = entry.path().join("cmdline");
            if let Ok(bytes) = fs::read(&cmdline_path) {
                if let Some(pos) = bytes.iter().position(|&b| b == 0) {
                    let exec_path = String::from_utf8_lossy(&bytes[..pos]);
                    let exec_name = Path::new(exec_path.as_ref())
                        .file_name()
                        .and_then(|s| s.to_str())
                        .unwrap_or("");
                    if exec_name == "linux-wallpaperengine" {
                        return true;
                    }
                }
            }
        }
    }
    false
}

// ─── Icon loading helpers ─────────────────────────────────────────────────────

/// Load tray icon from the bundled resource directory.
fn load_icon(app: &AppHandle, filename: &str) -> Option<Image<'static>> {
    // Try bundled resource path (works in production builds)
    let resource_path = app
        .path()
        .resource_dir()
        .ok()?
        .join("icons")
        .join(filename);

    if resource_path.exists() {
        return Image::from_path(&resource_path).ok();
    }

    // Dev fallback: look relative to the src-tauri directory
    let dev_path = std::env::current_exe()
        .ok()?
        .parent()? // target/debug
        .parent()? // target
        .parent()? // src-tauri root
        .join("icons")
        .join(filename);

    Image::from_path(&dev_path).ok()
}

// ─── Tray setup entry point ───────────────────────────────────────────────────

/// Call this once from within `tauri::Builder::setup()`.
pub fn setup_tray(app: &mut App) -> tauri::Result<()> {
    let app_handle = app.handle().clone();

    // 🔧 Override GLib's application name so Waybar shows a human-readable tooltip
    // instead of the binary name "lwg-gui-tauri". The glib library is already linked
    // transitively via GTK/webkit2gtk.
    #[cfg(target_os = "linux")]
    {
        extern "C" {
            fn g_set_application_name(application_name: *const std::os::raw::c_char);
        }
        let name = std::ffi::CString::new("Wallpaper Engine GUI").unwrap();
        unsafe { g_set_application_name(name.as_ptr()); }
    }

    // ── Build context menu ────────────────────────────────────────────────────
    let show_item = MenuItemBuilder::new("Show Window")
        .id("show_window")
        .build(app)?;

    let play_stop_item = MenuItemBuilder::new("Play / Stop Wallpaper")
        .id("play_stop")
        .build(app)?;

    let random_item = MenuItemBuilder::new("Random Wallpaper")
        .id("random")
        .build(app)?;

    let quit_item = MenuItemBuilder::new("Quit")
        .id("quit")
        .build(app)?;

    let sep1 = PredefinedMenuItem::separator(app)?;
    let sep2 = PredefinedMenuItem::separator(app)?;

    let menu = MenuBuilder::new(app)
        .item(&show_item)
        .item(&sep1)
        .item(&play_stop_item)
        .item(&random_item)
        .item(&sep2)
        .item(&quit_item)
        .build()?;

    // ── Load initial icon ─────────────────────────────────────────────────────
    let running_icon = load_icon(&app_handle, "tray.png");
    let stopped_icon = load_icon(&app_handle, "tray-stopped.png");

    let initial_icon = if is_engine_running() {
        running_icon.clone()
    } else {
        stopped_icon.clone()
    };

    // ── Build tray icon ───────────────────────────────────────────────────────
    // NOTE: On Linux with libappindicator, `set_tooltip()` is a no-op.
    // Waybar reads the app's `productName` from tauri.conf.json as the tooltip.
    let mut tray_builder = TrayIconBuilder::with_id("lwg-tray")
        .menu(&menu)
        .tooltip("Wallpaper Engine GUI")
        .show_menu_on_left_click(false);

    if let Some(icon) = initial_icon {
        tray_builder = tray_builder.icon(icon);
    }

    let tray = tray_builder.build(app)?;
    let tray_id = tray.id().clone();

    // ── Menu event handler ────────────────────────────────────────────────────
    {
        let ah = app_handle.clone();
        app.on_menu_event(move |_app, event| {
            let id = event.id().as_ref();
            match id {
                "show_window" => {
                    toggle_window(&ah, true);
                }
                "play_stop" => {
                    let ah2 = ah.clone();
                    thread::spawn(move || {
                        if is_engine_running() {
                            // Stop: invoke stop_wallpaper command
                            let _ = tauri::async_runtime::block_on(async {
                                ah2.emit("tray-stop-wallpaper", ())
                            });
                        } else {
                            // Resume last wallpaper
                            let _ = ah2.emit("tray-apply-last", ());
                        }
                    });
                }
                "random" => {
                    let _ = ah.emit("tray-random-wallpaper", ());
                }
                "quit" => {
                    let _ = ah.emit("tray-quit-request", ());
                }
                _ => {}
            }
        });
    }

    // ── Tray icon click handler (left-click toggles window) ───────────────────
    {
        let ah = app_handle.clone();
        tray.on_tray_icon_event(move |_tray, event| {
            if let TrayIconEvent::Click { button, button_state, .. } = event {
                if button == MouseButton::Left && button_state == MouseButtonState::Up {
                    toggle_window(&ah, false);
                }
            }
        });
    }

    // ── Background polling loop: refresh icon + tooltip every 2 seconds ───────
    {
        let ah = app_handle.clone();
        // We pick up the tray handle by ID after spawning
        let tray_id_clone = tray_id.clone();

        thread::spawn(move || {
            let mut last_state: Option<bool> = None;

            loop {
                thread::sleep(Duration::from_secs(2));

                let running = is_engine_running();

                if last_state == Some(running) {
                    continue; // No change — skip the update
                }
                last_state = Some(running);

                // Retrieve the live TrayIcon handle from the app
                if let Some(tray_handle) = ah.tray_by_id(&tray_id_clone) {
                    // Update tooltip
                    let tooltip = if running {
                        "Wallpaper Engine GUI\nStatus: Running"
                    } else {
                        "Wallpaper Engine GUI\nStatus: Stopped"
                    };
                    let _ = tray_handle.set_tooltip(Some(tooltip));

                    // Update icon
                    let icon_file = if running { "tray.png" } else { "tray-stopped.png" };
                    if let Some(icon) = load_icon(&ah, icon_file) {
                        let _ = tray_handle.set_icon(Some(icon));
                    }
                }
            }
        });
    }

    Ok(())
}

// ─── Window helpers ───────────────────────────────────────────────────────────

/// Show/hide the main window.
/// If `force_show` is true, always show. Otherwise toggle current visibility.
fn toggle_window(app: &AppHandle, force_show: bool) {
    if let Some(window) = app.get_webview_window("main") {
        let is_visible = window.is_visible().unwrap_or(false);
        if force_show || !is_visible {
            let _ = window.show();
            let _ = window.set_focus();
        } else {
            let _ = window.hide();
        }
    }
}
