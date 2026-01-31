import os

# Application constants
APP_ID = 'com.github.wallpaperengine.gui'
VERSION = '0.8.1'

# Configuration Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.expanduser("~/.config/linux-wallpaperengine-gui")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
WORKSHOP_PATH = os.path.expanduser("~/.local/share/Steam/steamapps/workshop/content/431960")
ASSETS_PATH = os.path.expanduser("~/.local/share/Steam/steamapps/common/wallpaper_engine/assets")
ICON_PATH = os.path.join(PROJECT_ROOT, "gui_tray.png")

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
    "assetsPath": None,  # Custom assets directory (None = auto-detect)
}

# CSS Styling
CSS_STYLE = """
/* Global */
window {
    background-color: #1d1d1d;
}

/* Top navigation bar */
.nav-bar {
    background: rgba(0, 0, 0, 0.3);
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

togglebutton:focus {
    outline: none;
    box-shadow: none;
    border: none;
}

.nav-btn {
    background: #2a2a2a;
    color: rgba(255,255,255,0.87);
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 600;
    border: none;
    min-height: 36px;
    transition: all 0.2s;
    box-shadow: none;
    outline: none;
    border-bottom: none;
    border-top: none;
    border-left: none;
    border-right: none;
}

.nav-btn:hover {
    background: #464646;
    border: none;
    border-bottom: none;
}

.nav-btn.active, .nav-btn:checked {
    background: #007bff;
    color: white;
    box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
    border: none;
    border-bottom: none;
}

.nav-btn:focus, .nav-btn:focus-visible {
    outline: none;
    box-shadow: none;
}

/* Toolbar */
.toolbar {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 20px;
    padding: 6px 15px;
    margin: 0 20px 10px 20px;
}

.status-label {
    color: rgba(255,255,255,0.4);
    font-weight: 600;
    font-size: 0.85em;
    letter-spacing: 0.5px;
}

.status-value {
    color: #007bff;
    font-weight: 700;
    text-transform: uppercase;
}

.search-entry {
    min-height: 20px;
    padding: 0px 6px;
    font-size: 0.85em;
}

.mode-btn {
    background: #2a2a2a;
    color: rgba(255,255,255,0.87);
    border-radius: 10px;
    padding: 6px 6px;
    border: none;
    min-height: 36px;
    min-width: 36px;
    font-size: 1.2em;
}

.mode-btn:hover {
    background: #464646;
}

.mode-btn.active, .mode-btn:checked {
    background: #007bff;
    color: white;
}

.stop-btn {
    background: #2a2a2a;
    color: #ef4444;
    font-size: 1.4em;
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
    background: rgba(66, 66, 66, 0.5);
    border-radius: 5px;
    border: 3px solid transparent;
    transition: all 0.2s ease-out;
    padding: 0;
}

.wallpaper-item:hover {
    border-color: rgba(0, 123, 255, 0.5);
    box-shadow: 0 0 15px rgba(0, 123, 255, 0.7);
}

.wallpaper-item.selected {
    border-color: #007bff;
    box-shadow: 0 0 15px rgba(0, 123, 255, 0.7);
}

.wallpaper-name {
    background: black;
    border-radius: 10px;
    border: 2px solid #007bff;
    padding: 5px 10px;
    font-weight: 400;
    font-size: 0.9em;
}

/* Wallpaper list - List view */
.list-item {
    background: rgba(61, 61, 61, 0.4);
    border-radius: 12px;
    border: 2px solid transparent;
    padding: 12px;
    margin: 5px 0;
    transition: all 0.2s;
}

.list-item:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.15);
}

.list-item.selected {
    border-color: #007bff;
    background: rgba(0, 123, 255, 0.1);
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
    color: #fbbf24;
    font-size: 0.85em;
}

.list-folder {
    color: #86efac;
    font-size: 0.85em;
}

/* Sidebar */
.sidebar {
    background: #2a2a2a;
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
    color: rgba(255,255,255,0.6);
    font-size: 0.9em;
    margin: 5px 20px;
}

.sidebar-section {
    font-weight: 600;
    font-size: 0.9em;
    color: rgba(255,255,255,0.6);
    margin: 15px 20px 5px 20px;
    padding-bottom: 5px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

.sidebar-desc {
    font-size: 0.9em;
    color: rgba(255,255,255,0.8);
    margin: 0 20px;
    line-height: 1.4;
}

.tag-chip {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 4px 6px;
    font-size: 0.85em;
    margin: 2px;
}

.folder-chip {
    background: rgba(0, 123, 255, 0.15);
    border: 1px solid rgba(0, 123, 255, 0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-weight: 800;
    color: #3b82f6;
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
    margin: 5px 20px 5px 0;
}

.sidebar-btn {
    background: #007bff;
    color: white;
    border-radius: 25px;
    font-weight: bold;
    padding: 10px 20px;
    border: none;
    margin: 10px 20px;
}

.sidebar-btn:hover {
    background: #53a6ff;
}

.sidebar-btn.secondary {
    background: transparent;
    border: 1px solid rgba(255,255,255,0.2);
}

.sidebar-btn.secondary:hover {
    background: rgba(255,255,255,0.1);
}

/* Settings page */
.settings-container {
    background: rgba(20, 20, 20, 0.5);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    margin: 20px;
}

.settings-sidebar {
    background: rgba(20, 20, 20, 0.6);
    border-right: 1px solid rgba(255,255,255,0.08);
    padding: 32px 16px;
}

.settings-header {
    font-size: 1.5em;
    font-weight: 800;
    margin-bottom: 8px;
}

.settings-subheader {
    color: rgba(255,255,255,0.4);
    font-size: 0.85em;
}

.settings-nav-item {
    background: transparent;
    color: rgba(255,255,255,0.4);
    border-radius: 10px;
    padding: 12px 16px;
    font-weight: 500;
    border: none;
}

.settings-nav-item:hover {
    background: rgba(255,255,255,0.15);
    color: rgba(255,255,255,0.87);
}

.settings-nav-item.active, .settings-nav-item:checked {
    background: #007bff;
    color: white;
    box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.settings-section-title {
    font-size: 1.4em;
    font-weight: 700;
    margin-bottom: 8px;
}

.settings-section-desc {
    color: rgba(255,255,255,0.5);
    font-size: 0.9em;
    margin-bottom: 20px;
}

.setting-row {
    background: rgba(61, 61, 61, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
}

.setting-label {
    font-weight: 500;
}

.setting-desc {
    color: rgba(255,255,255,0.5);
    font-size: 0.85em;
}

.action-btn {
    border-radius: 10px;
    padding: 12px;
    font-weight: 600;
    border: none;
}

.action-btn.primary {
    background: #007bff;
    color: white;
}

.action-btn.primary:hover {
    background: #53a6ff;
}

.action-btn.secondary {
    background: rgba(61, 61, 61, 0.4);
    border: 1px solid rgba(255,255,255,0.08);
}

.action-btn.secondary:hover {
    background: rgba(255,255,255,0.15);
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

/* Scrollbar */
scrollbar {
    background: transparent;
}

scrollbar slider {
    background: #007bff;
    border-radius: 9999px;
    min-width: 6px;
    min-height: 6px;
}

scrollbar slider:hover {
    background: #53a6ff;
}

/* Common */
.text-muted {
    color: rgba(255,255,255,0.4);
}

.card {
    border-radius: 12px;
}

spinbutton {
    background: rgba(61, 61, 61, 0.4);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.08);
}

entry {
    background: rgba(61, 61, 61, 0.4);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 8px 12px;
}

switch {
    background: rgba(61, 61, 61, 0.6);
}

switch:checked {
    background: #007bff;
}

dropdown button {
    background: rgba(61, 61, 61, 0.4);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.08);
}
"""
