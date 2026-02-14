import os

# Application constants
APP_ID = 'com.github.wallpaperengine.gui'
VERSION = '0.10.5'

# Configuration Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.expanduser("~/.config/linux-wallpaperengine-gui")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
WORKSHOP_PATH = os.path.expanduser("~/.local/share/Steam/steamapps/workshop/content/431960")
ASSETS_PATH = os.path.expanduser("~/.local/share/Steam/steamapps/common/wallpaper_engine/assets")
ICON_PATH = os.path.join(PROJECT_ROOT, "pic/icons/gui_tray_rounded.png")

DEFAULT_CONFIG = {
    "fps": 30,
    "volume": 0,
    "scaling": "default",
    "silence": True,
    "noFullscreenPause": False,
    "disableMouse": False,
    "noautomute": False,
    "noAudioProcessing": False,
    "disableParallax": False,
    "disableParticles": False,
    "clamping": "clamp",
    "lastWallpaper": None,
    "lastScreen": None,
    "wallpaperProperties": {},
    "screenshotDelay": 20,
    "screenshotRes": "3840x2160",
    "preferXvfb": True,
    "active_monitors": {},
    "cycleEnabled": False,
    "cycleInterval": 15,
    "cycleOrder": "random", # random, title, size, type, id
    "assetsPath": None,  # Custom assets directory (None = auto-detect)
    "wayland_only_active": False,
    "wayland_ignore_appids": "",
    "compact_mode": False,  # Compact preview mode for tiling WMs
}

# CSS Styling
CSS_STYLE = """
/* Global */
window {
    background-color: @window_bg_color;
}

/* Top navigation bar */
.nav-bar {
    background: alpha(@window_bg_color, 0.3);
    border-radius: 12px;
    padding: 4px;
    margin: 10px 20px;
    border: none;
    border-bottom: none;
}

/* Toggle button defaults */
togglebutton {
    border: none;
    box-shadow: none;
    outline: none;
    border-bottom: none;
}

togglebutton:focus-visible {
    outline: 2px solid @accent_bg_color;
    outline-offset: 2px;
}

.nav-btn {
    background: alpha(@theme_fg_color, 0.08);
    color: @theme_fg_color;
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 600;
    border: 1px solid alpha(@theme_fg_color, 0.1);
    min-height: 36px;
    transition: all 0.2s;
    box-shadow: none;
    outline: none;
}

.nav-btn:hover {
    background: alpha(@theme_fg_color, 0.12);
    border-color: alpha(@theme_fg_color, 0.2);
}

.nav-btn.active, .nav-btn:checked {
    background: @accent_bg_color;
    color: @accent_fg_color;
    box-shadow: 0 4px 12px alpha(@accent_bg_color, 0.3);
    border: none;
    border-bottom: none;
}

.nav-btn:focus, .nav-btn:focus-visible {
    outline: 2px solid @accent_bg_color;
    outline-offset: 2px;
    box-shadow: 0 0 0 2px alpha(@accent_bg_color, 0.4);
}

/* Fix for MenuButton & DropDown double-layer look and hit-box */
menubutton.nav-btn, dropdown.nav-btn {
    background: transparent;
    border: none;
    box-shadow: none;
    outline: none;
    padding: 0;
    margin: 0;
    border-radius: inherit;
}

menubutton.nav-btn > button, dropdown.nav-btn > button {
    background: alpha(@theme_fg_color, 0.08);
    color: @theme_fg_color;
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 600;
    border: 1px solid alpha(@theme_fg_color, 0.1);
    min-height: 36px;
    transition: all 0.2s;
    box-shadow: none;
    margin: 0;
}

menubutton.nav-btn > button:focus-visible, dropdown.nav-btn > button:focus-visible {
    outline: 2px solid @accent_bg_color;
    outline-offset: 2px;
    box-shadow: 0 0 0 2px alpha(@accent_bg_color, 0.4);
}

menubutton.nav-btn > button:hover, dropdown.nav-btn > button:hover {
    background: alpha(@theme_fg_color, 0.12);
    border-color: alpha(@theme_fg_color, 0.2);
}

menubutton.nav-btn > button:active,
menubutton.nav-btn > button:checked,
dropdown.nav-btn > button:active {
    background: @accent_bg_color;
    color: @accent_fg_color;
    box-shadow: 0 4px 12px alpha(@accent_bg_color, 0.3);
    border: none;
    border-bottom: none;
}

/* Toolbar */
.toolbar {
    background: alpha(@window_bg_color, 0.3);
    border-radius: 20px;
    padding: 6px 15px;
    margin: 0 20px 10px 20px;
}

.status-label {
    color: alpha(@theme_fg_color, 0.4);
    font-weight: 600;
    font-size: 0.85em;
    letter-spacing: 0.5px;
}

.status-value {
    color: @accent_bg_color;
    font-weight: 700;
    text-transform: uppercase;
}

.status-value-yellow {
    color: alpha(@theme_fg_color, 0.6);
    font-weight: 700;
    text-transform: uppercase;
}

.search-entry {
    min-height: 20px;
    padding: 0px 6px;
    font-size: 0.85em;
}

.mode-btn {
    background: alpha(@theme_fg_color, 0.08);
    color: @theme_fg_color;
    border-radius: 10px;
    padding: 6px 6px;
    border: 1px solid alpha(@theme_fg_color, 0.1);
    min-height: 36px;
    min-width: 36px;
    font-size: 1.2em;
    transition: all 0.2s;
}

.mode-btn:hover {
    background: alpha(@theme_fg_color, 0.12);
    border-color: alpha(@theme_fg_color, 0.2);
}

.mode-btn.active, .mode-btn:checked {
    background: @accent_bg_color;
    color: @accent_fg_color;
    border-color: @accent_bg_color;
}

.stop-btn {
    background: alpha(@theme_fg_color, 0.08);
    color: #ef4444;
    border: 1px solid alpha(@theme_fg_color, 0.1);
}

.stop-btn image {
    color: #ef4444;
}

.stop-btn:hover {
    background: #450a0a;
    color: #f87171;
}

/* Wallpaper card - Grid view */
.wallpaper-card {
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.wallpaper-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
}

.wallpaper-item {
    background: alpha(@window_bg_color, 0.5);
    border-radius: 5px;
    border: 3px solid transparent;
    transition: all 0.2s ease-out;
    padding: 0;
}

.wallpaper-item:hover {
    border-color: alpha(@accent_bg_color, 0.5);
    box-shadow: 0 0 15px alpha(@accent_bg_color, 0.7);
}

.wallpaper-item.selected {
    border-color: @accent_bg_color;
    box-shadow: 0 0 15px alpha(@accent_bg_color, 0.7);
}

.wallpaper-name {
    background: alpha(@window_bg_color, 0.9);
    color: @theme_fg_color;
    border-radius: 20px;
    padding: 4px 14px;
    border: 1px solid alpha(@accent_bg_color, 0.3);
    box-shadow: 0 0 12px alpha(@accent_bg_color, 0.4);
    font-weight: 500;
    font-size: 0.85em;
}

/* Wallpaper list - List view */
.list-item {
    background: alpha(@window_bg_color, 0.4);
    border-radius: 12px;
    border: 2px solid transparent;
    padding: 12px;
    margin: 5px 0;
    transition: all 0.2s;
}

.list-item:hover {
    background: alpha(@theme_fg_color, 0.15);
    border-color: alpha(@theme_fg_color, 0.15);
}

.list-item.selected {
    border-color: @accent_bg_color;
    background: alpha(@accent_bg_color, 0.1);
}

.list-title {
    font-weight: 600;
    font-size: 1.1em;
}

.list-type {
    color: #7dd3fc;
    font-size: 0.85em;
}

.list-tags {
    color: #a78bfa;
    font-size: 0.85em;
}

.list-size {
    color: #4ade80;
    font-weight: 600;
    font-size: 0.85em;
}

.list-index {
    color: #facc15;
    font-weight: 600;
    font-size: 0.85em;
}

.list-folder {
    color: #86efac;
    font-size: 0.85em;
}

/* Sidebar */
.sidebar {
    background: alpha(@window_bg_color, 0.8);
    border-radius: 15px;
    margin: 20px;
    margin-left: 0;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.3);
    min-width: 320px;
    max-width: 320px;
    width: 320px;
}

.sidebar-preview {
    border-radius: 10px;
    margin: 20px;
}

.sidebar-title {
    font-size: 1.3em;
    font-weight: bold;
    margin: 0 20px;
}

.sidebar-subtitle {
    color: alpha(@theme_fg_color, 0.6);
    font-size: 0.9em;
    margin: 5px 20px;
}

.sidebar-section {
    font-weight: 600;
    font-size: 0.9em;
    color: alpha(@theme_fg_color, 0.6);
    margin: 15px 20px 5px 20px;
    padding-bottom: 5px;
    border-bottom: 1px solid alpha(@theme_fg_color, 0.08);
}

.sidebar-desc {
    font-size: 0.9em;
    color: alpha(@theme_fg_color, 0.8);
    margin: 0 20px;
    line-height: 1.4;
}

.tag-chip {
    background: alpha(@theme_fg_color, 0.1);
    border-radius: 15px;
    padding: 4px 6px;
    font-size: 0.85em;
    margin: 2px;
}

.folder-chip {
    background: alpha(@accent_bg_color, 0.15);
    border: 1px solid alpha(@accent_bg_color, 0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-weight: 800;
    color: @accent_bg_color;
    font-size: 0.85em;
    margin: 5px 0 5px 20px;
}

.size-chip {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-weight: 600;
    color: #22c55e;
    font-size: 0.85em;
    margin: 5px 0 5px 0;
}

.index-chip {
    background: rgba(234, 179, 8, 0.15);
    border: 1px solid rgba(234, 179, 8, 0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-weight: 600;
    color: #eab308;
    font-size: 0.85em;
    margin: 5px 0 5px 0;
}

.sidebar-btn {
    background: @accent_bg_color;
    color: @accent_fg_color;
    border-radius: 25px;
    font-weight: bold;
    padding: 10px 20px;
    border: none;
    margin: 10px 20px;
}

.sidebar-btn:hover {
    background: alpha(@accent_bg_color, 0.8);
}

.sidebar-btn.secondary {
    background: transparent;
    border: 1px solid alpha(@theme_fg_color, 0.2);
}

.sidebar-btn.secondary:hover {
    background: alpha(@theme_fg_color, 0.1);
}

# .sidebar-btn.danger {
#     background: #dc2626;
#     color: white;
# }

# .sidebar-btn.danger:hover {
#     background: #ef4444;
# }

/* Settings page */
.settings-container {
    background: alpha(@window_bg_color, 0.5);
    border-radius: 16px;
    border: 1px solid alpha(@theme_fg_color, 0.08);
    margin: 20px;
}

.settings-sidebar {
    background: alpha(@window_bg_color, 0.6);
    border-right: 1px solid alpha(@theme_fg_color, 0.08);
    padding: 32px 16px;
}

.settings-header {
    font-size: 1.5em;
    font-weight: 800;
    margin-bottom: 8px;
}

.settings-subheader {
    color: alpha(@theme_fg_color, 0.4);
    font-size: 0.85em;
}

.settings-nav-item {
    background: transparent;
    color: alpha(@theme_fg_color, 0.4);
    border-radius: 10px;
    padding: 12px 16px;
    font-weight: 500;
    border: none;
}

.settings-nav-item:hover {
    background: alpha(@theme_fg_color, 0.15);
    color: @theme_fg_color;
}

.settings-nav-item.active, .settings-nav-item:checked {
    background: @accent_bg_color;
    color: @accent_fg_color;
    box-shadow: 0 4px 12px alpha(@accent_bg_color, 0.3);
}

.settings-section-title {
    font-size: 1.4em;
    font-weight: 700;
    margin-bottom: 8px;
}

.settings-section-desc {
    color: alpha(@theme_fg_color, 0.5);
    font-size: 0.9em;
    margin-bottom: 20px;
}

.setting-row {
    background: alpha(@window_bg_color, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
}

.setting-label {
    font-weight: 500;
}

.setting-desc {
    color: alpha(@theme_fg_color, 0.5);
    font-size: 0.85em;
}

.action-btn {
    border-radius: 10px;
    padding: 12px;
    font-weight: 600;
    border: none;
}

.action-btn.primary {
    background: @accent_bg_color;
    color: @accent_fg_color;
}

.action-btn.primary:hover {
    background: alpha(@accent_bg_color, 0.8);
}

.action-btn.secondary {
    background: alpha(@window_bg_color, 0.4);
    border: 1px solid alpha(@theme_fg_color, 0.08);
}

.action-btn.secondary:hover {
    background: alpha(@theme_fg_color, 0.15);
}

.action-btn.danger {
    background: transparent;
    color: #ef4444;
}

.status-panel {
    margin-top: 5px;
    margin-bottom: 5px;
}

.action-btn.danger:hover {
    background: rgba(255, 77, 77, 0.1);
}

/* Scrollbar - thin & elegant */
scrollbar {
    background: transparent;
    opacity: 0.5;
    transition: opacity 200ms ease-in-out;
}

scrollbar:hover {
    opacity: 1;
}

scrollbar trough {
    background: transparent;
    border: none;
    box-shadow: none;
    outline: none;
    min-width: 3px;
    min-height: 3px;
}

scrollbar slider {
    background: alpha(@theme_fg_color, 0.3);
    border-radius: 9999px;
    min-width: 3px;
    min-height: 3px;
    margin: 0;
    padding: 0;
    transition: all 200ms ease-in-out;
}

scrollbar slider:hover {
    background: alpha(@theme_fg_color, 0.5);
}

/* Common */
.text-muted {
    color: alpha(@theme_fg_color, 0.4);
}

.card {
    border-radius: 12px;
}

spinbutton {
    background: alpha(@window_bg_color, 0.4);
    border-radius: 8px;
    border: 1px solid alpha(@theme_fg_color, 0.08);
}

entry {
    background: alpha(@window_bg_color, 0.4);
    border-radius: 8px;
    border: 1px solid alpha(@theme_fg_color, 0.08);
    padding: 8px 12px;
}

switch {
    background: alpha(@window_bg_color, 0.6);
}

switch:checked {
    background: @accent_bg_color;
}

dropdown button {
    background: alpha(@window_bg_color, 0.4);
    border-radius: 8px;
    border: 1px solid alpha(@theme_fg_color, 0.08);
}

/* Boxed Expander */
.boxed-expander {
    background: alpha(@theme_fg_color, 0.03);
    border: 1px solid alpha(@theme_fg_color, 0.08);
    border-radius: 8px;
    margin: 5px 0;
    padding: 2px;
}

.boxed-expander title {
    border-radius: 8px;
    padding: 8px;
}

.boxed-expander:checked {
    background: alpha(@theme_fg_color, 0.05);
    border-color: alpha(@theme_fg_color, 0.15);
}

/* Nickname Support */
.nickname-text {
    font-style: italic;
    font-weight: bold;
    color: alpha(@theme_fg_color, 0.9);
}

.original-name-text {
    font-size: 0.85em;
    color: alpha(@theme_fg_color, 0.7);
    margin: 0 20px 5px 20px;
}

/* Popover Menu Buttons */
.popover-btn {
    padding: 4px 8px;
    margin: 0px;
    border-radius: 6px;
    background: transparent;
    border: none;
    box-shadow: none;
    transition: background 0.2s;
}

.popover-btn:hover {
    background: alpha(@theme_fg_color, 0.1);
}

.popover-btn label {
    margin: 0;
}
"""
