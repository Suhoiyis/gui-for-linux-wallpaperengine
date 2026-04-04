# LWG (Linux Wallpaper Engine) GUI Project Rules

## 🎯 Project Overview

A Linux Wallpaper Engine GUI application built with **Python + GTK4 + Libadwaita**. The project provides a modern interface for managing and applying Steam Workshop live wallpapers on Linux.

- **Active Development Zone**: `py_GUI/` (Python GTK4 application)
- **Optional Rust Library**: `lwg-rs/` (Independent Rust core library, can be used for performance-critical operations)
- **Archived Experiment**: `lwg-gui-tauri/` (Tauri + React version - archived due to WebKit memory issues)

### Project Status

| Component | Status | Description |
|-----------|--------|-------------|
| `py_GUI/` | 🟢 Active | Main development target |
| `lwg-rs/` | 🟡 Maintained | Independent Rust library (optional) |
| `lwg-gui-tauri/` | 🔴 Archived | Tauri experiment - not maintained |

> **Note**: The Tauri version was archived due to severe WebKit memory leaks (~3GB on startup), which is unacceptable for a desktop application. The Python version using GTK4 has significantly better memory footprint.

---

## 📂 Directory Structure & Agent Navigation Guide

### 1. Main Application (`/py_GUI/`)

This is the primary development zone for all UI and application logic.

```
py_GUI/
├── core/                    # Business logic layer
│   ├── config.py           # Configuration management
│   ├── controller.py       # Wallpaper process control
│   ├── wallpaper.py        # Wallpaper scanning & metadata
│   ├── screen.py           # Multi-monitor management
│   ├── state.py            # Application state & event bus
│   ├── history.py          # Playback history (30 entries)
│   ├── nickname.py         # Wallpaper nickname system
│   ├── playlists.py        # Playlist & favorites service
│   ├── performance.py      # CPU/memory monitoring
│   ├── logger.py           # Logging system
│   ├── updater.py          # GitHub update checker
│   └── integrations.py     # System integration (.desktop, etc.)
│
├── ui/                      # User interface layer
│   ├── app.py              # Main application window
│   ├── pages/              # Page views
│   │   ├── library.py      # Wallpaper library (main page)
│   │   ├── settings.py     # Settings page
│   │   └── performance.py  # Performance monitor page
│   ├── components/         # Reusable UI components
│   │   ├── layout/         # NavBar, Sidebar
│   │   ├── library/        # Wallpaper grid, sidebar, playlist panel
│   │   ├── dialogs/        # Various dialogs
│   │   ├── common/         # Shared widgets
│   │   └── performance/    # Sparkline charts
│   ├── tray.py             # System tray (Rust sidecar launcher)
│   └── compact_window.py   # Compact preview mode
│
├── main.py                  # Application entry point
└── const.py                # Constants, version, CSS styles
```

### 2. Rust Core Library (`/lwg-rs/`)

An independent Rust library that can be optionally used for performance-critical operations.

```
lwg-rs/
├── crates/
│   └── lwg-core/           # Core library
│       ├── src/config.rs   # Configuration structures
│       ├── src/controller.rs # Wallpaper controller
│       ├── src/wallpaper.rs # Wallpaper management
│       ├── src/performance.rs # Performance monitoring
│       ├── src/history.rs  # History management
│       ├── src/nickname.rs # Nickname system
│       ├── src/favorite.rs # Favorites system
│       └── src/logger.rs   # Logging utilities
```

> **Usage**: The Rust library can be integrated via PyO3 or used as a standalone CLI tool. It is NOT required for the Python app to function.

### 3. Archived Tauri Experiment (`/lwg-gui-tauri/`)

> ⚠️ **ARCHIVED**: This version is no longer maintained. Kept for reference only.

Reason for archival: WebKitGTK memory leak causing ~3GB RAM usage on startup, which is unacceptable for a desktop application.

---

## ⚠️ Core Development Rules

### Rule 1: Configuration Management

- **Location**: `~/.config/linux-wallpaperengine-gui/config.json`
- **State File**: `~/.local/state/linux-wallpaperengine-gui/state.json`
- **Naming Convention**: Python uses `snake_case` internally (e.g., `wayland_only_active`)
- **Legacy Compatibility**: Field aliases are defined in `py_GUI/core/schema.py`

```python
# Example: ConfigManager usage
config = ConfigManager()
fps = config.get("fps", default=30)
config.set("silence", True)  # Auto-saves
```

**Configuration Keys** (see `py_GUI/core/schema.py` for full list):
| Key | Default | Description |
|-----|---------|-------------|
| `fps` | 30 | Frame rate limit (1-144) |
| `volume` | 0 | Audio volume (0-100) |
| `silence` | True | Mute audio |
| `scaling` | "default" | Scaling mode |
| `clamping` | "clamp" | Clamping mode |
| `cycleEnabled` | False | Auto-rotation enabled |
| `cycleInterval` | 15 | Rotation interval (minutes) |
| `workshopPath` | None | Steam Workshop path |

### Rule 2: State Management

- **StateBus**: Event-driven state updates via `AppStateBus`
- **StateManager**: Persistent state for multi-monitor wallpaper mappings

```python
# Example: State management
state = StateManager()
state.set_active_monitors({"HDMI-1": "12345678", "eDP-1": "87654321"})
active = state.get_active_monitors()  # Returns dict
```

**State File Structure** (`state.json`):
```json
{
  "active_monitors": {"HDMI-1": "2874425843"},
  "lastWallpaper": "2874425843",
  "lastScreen": "HDMI-1"
}
```

### Rule 3: UI Development

- **Framework**: GTK4 + Libadwaita
- **Styling**: Use GTK named colors (`@window_bg_color`, `@accent_bg_color`)
- **Theme**: Automatic light/dark mode adaptation
- **CSS**: Defined in `py_GUI/const.py` as `CSS_STYLE`

**Key UI Patterns**:
- Pages extend `Adw.Bin` or `Gtk.Box`
- Components are modular and reusable
- Dialogs use `Adw.Dialog` or `Gtk.Dialog`

### Rule 4: Logging

- **Sources**: GUI, Controller, Engine, Core
- **Implementation**: `py_GUI/core/logger.py`

```python
log_manager = LogManager()
log_manager.add_info("Message", "Source")
log_manager.add_error("Error occurred", "Controller")
log_manager.add_warning("Warning", "GUI")
```

**Log Sources**:
| Source | Description |
|--------|-------------|
| GUI | User interactions, UI events |
| Controller | Wallpaper apply/stop, process management |
| Engine | linux-wallpaperengine stdout/stderr |
| Core | Config parsing, internal utilities |

### Rule 5: Wallpaper Controller

- **Backend**: Controls `linux-wallpaperengine` (C++ binary) via subprocess
- **Implementation**: `py_GUI/core/controller.py`

**Engine Argument Mapping**:
| Config Key | Engine Flag | Notes |
|------------|-------------|-------|
| `silence=True` | `--silent` | Highest priority |
| `volume` | `--volume` | Only when not silent |
| `fps` | `-f` | Frame rate |
| `scaling` | `--scaling` | Scaling mode |
| `clamping` | `--clamp` | Note: `--clamp` not `--clamping` |

---

## 🤖 Instructions for the AI Agent

1. **Never guess config keys**: Check `py_GUI/core/schema.py` for all valid configuration keys and their defaults.

2. **Follow existing patterns**: Before implementing new features, check existing components in `py_GUI/ui/components/` for patterns.

3. **Respect the event bus**: Use `AppStateBus` for cross-component communication, not direct method calls.

4. **Backend integration**: The app controls `linux-wallpaperengine` (C++ backend) via subprocess. Check `py_GUI/core/controller.py` for command-line argument passing.

5. **Multi-monitor support**: Always consider multi-monitor scenarios. Use `ScreenManager` to get available screens.

6. **Check schema first**: `py_GUI/core/schema.py` defines all config keys, defaults, and aliases. It's the source of truth.

---

## 📦 Version Management

Version is defined in `py_GUI/const.py`:

```python
VERSION = "1.0.0-pre"
```

Also update in:
- `docs/CHANGELOG.md`
- Git tags for releases

---

## 🔧 Development Setup

### Requirements

- **Python**: 3.10+
- **GTK**: GTK4 + Libadwaita
- **Backend**: `linux-wallpaperengine` (install separately)

### System Dependencies (Arch Linux)

```bash
sudo pacman -S python-gobject gtk4 libadwaita libayatana-appindicator
```

### System Dependencies (Ubuntu/Debian)

```bash
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 libayatana-appindicator3-1
```

### Run Development

```bash
cd /home/yua/suw
python3 py_GUI/main.py
```

### CLI Commands

```bash
python3 py_GUI/main.py --show      # Show window
python3 py_GUI/main.py --hide      # Hide window
python3 py_GUI/main.py --toggle    # Toggle window
python3 py_GUI/main.py --random    # Random wallpaper
python3 py_GUI/main.py --stop      # Stop wallpaper
python3 py_GUI/main.py --quit      # Quit application
```

### Build AppImage

```bash
./build_appimage.sh
```

---

## 🖼️ System Tray Implementation

- **Implementation**: Rust sidecar (`lwg-rs/crates/lwg-tray/`) launched via `py_GUI/ui/tray.py`
- **Icons**: Stored in `pic/icons/` with fallback to local XDG directory
- **Features**: 
  - Dynamic icon (color/grayscale based on playback state)
  - Left-click toggle main window
  - Context menu with actions

---

## 📚 Related Documentation

| Document | Description |
|----------|-------------|
| `PROJECT.md` | Project architecture and technical details |
| `README.md` | User-facing documentation and features |
| `docs/ADVANCED.md` | Advanced features and configuration |
| `docs/COMPATIBILITY.md` | Wallpaper type compatibility |
| `docs/CHANGELOG.md` | Version history |

---

## 🚫 Common Pitfalls

1. **Engine flag mismatch**: Engine uses `--clamp` not `--clamping`. Always check `controller.py`.

2. **Config key confusion**: Frontend uses `muteAudio`, internal uses `silence`. Check `schema.py` for aliases.

3. **Empty fields**: Use `config.get("key", default)` to handle missing keys gracefully.

4. **State persistence**: `state.json` can be safely deleted; app will start fresh.
