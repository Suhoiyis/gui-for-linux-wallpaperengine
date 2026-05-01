// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    // Fix: WebKit DMABuf renderer fails silently in AppImage sandbox
    // Must be set before ANY Tauri/WebKit initialization
    std::env::set_var("WEBKIT_DISABLE_DMABUF_RENDERER", "1");

    // Reduce memory pressure in WebKitGTK runtime
    if std::env::var_os("G_SLICE").is_none() {
        std::env::set_var("G_SLICE", "always-malloc");
    }
    if std::env::var_os("MALLOC_ARENA_MAX").is_none() {
        std::env::set_var("MALLOC_ARENA_MAX", "2");
    }

    // Tell JavaScriptCore to be more aggressive with garbage collection
    // and limit JIT compilation tiers to reduce code cache memory.
    // These must be set before WebKit initializes.
    if std::env::var_os("JSC_useJIT").is_none() {
        // Keep JIT but disable the most memory-hungry tier
        std::env::set_var("JSC_useDFGJIT", "false");
    }

    lwg_gui_tauri_lib::run()
}
