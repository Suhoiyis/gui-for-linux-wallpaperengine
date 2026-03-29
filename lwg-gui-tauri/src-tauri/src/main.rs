// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    // Fix: WebKit DMABuf renderer fails silently in AppImage sandbox
    // Must be set before ANY Tauri/WebKit initialization
    std::env::set_var("WEBKIT_DISABLE_DMABUF_RENDERER", "1");

    lwg_gui_tauri_lib::run()
}
