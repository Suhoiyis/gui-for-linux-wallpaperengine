# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Linux Wallpaper Engine GUI — a desktop app for managing Steam Workshop live wallpapers on Linux. The project has three implementations:

- **`py_GUI/`** — Active, Python + GTK4 + Libadwaita (main stable version)
- **`py_GUI/ui/qt/`** — Active development on `feature/qt` branch, PySide6 + Qt Quick (QML) rewrite in progress
- **`lwg-rs/`** — Optional Rust core library (independent, not required for the Python app)
- **`lwg-gui-tauri/`** — Archived Tauri experiment (WebKitGTK memory leak, ~3GB RAM on startup)

The app controls `linux-wallpaperengine` (external C++ binary) via subprocess. It does NOT bundle or build the engine.

## Running

```bash
# GTK4 version
python3 py_GUI/main.py
python3 run_gui.py

# Qt Quick version (feature/qt branch)
python3 py_GUI/ui/qt/main.py

# CLI commands (single-instance, routed to running app)
python3 py_GUI/main.py --show|--hide|--toggle|--random|--stop|--quit

# Rust tray
cd tray_rs && cargo build --release
```

## Building

```bash
./build_appimage.sh          # Python GTK4 AppImage
cd lwg-rs && cargo build --release  # Rust workspace
```

## System Dependencies

Arch: `sudo pacman -S python-gobject gtk4 libadwaita libayatana-appindicator python-pyside6`
Debian: `sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 libayatana-appindicator3-1`

## Architecture

### Core Data Flow

```
UI (GTK4 or QML) → WallpaperController → subprocess → linux-wallpaperengine (C++)
System Tray (Rust ksni) → Unix Abstract Socket IPC → Python handler
```

### Python Core Layer (`py_GUI/core/`)

All core managers are imported and used by both GTK4 and Qt UIs:

- `config.py` → ConfigManager: reads/writes `~/.config/linux-wallpaperengine-gui/config.json`
- `controller.py` → WallpaperController: spawns/controls the C++ engine subprocess
- `wallpaper.py` → WallpaperManager: scans Steam Workshop directory for wallpapers
- `state.py` → StateManager + AppStateBus: persistent state + cross-component event bus
- `history.py` → HistoryManager: 30-entry playback history
- `nickname.py` → NicknameManager: wallpaper alias persistence
- `playlists.py` → PlaylistService + Favorites
- `performance.py` → PerformanceMonitor: CPU/memory tracking via `psutil`
- `schema.py` → Config key definitions, defaults, and camelCase/snake_case aliases (source of truth)

### Qt Quick Layer (`py_GUI/ui/qt/`)

- `backend.py` — Single `Backend` QObject exposing all core managers to QML via Properties/Signals/Slots
- `qml/Main.qml` — App shell with StackLayout page container
- `qml/components/` — All UI components (LibraryPage, SettingsPage, PerformancePage, etc.)
- `qml/Theme.js` + `Theme.qml` — Shared color/theme constants

The Qt backend reuses the same Python core modules (`ConfigManager`, `WallpaperController`, etc.) — no duplicated business logic.

### GTK4 UI Layer (`py_GUI/ui/`)

- `app.py` — Main Adw.Application window
- `pages/library.py` — Wallpaper grid (largest file, ~73KB)
- `pages/settings/` — Settings tabs
- `components/` — NavBar, Sidebar, dialogs, sparkline charts

## Critical Rules

1. **Never guess config keys** — check `py_GUI/core/schema.py` for all valid keys, defaults, and aliases.
2. **Engine flag mapping is tricky** — `silence` → `--silent`, `fps` → `-f` (not `--fps`), `clamping` → `--clamp` (not `--clamping`). Always verify in `controller.py`.
3. **Config key naming** — Python uses `snake_case` internally but config JSON uses camelCase. Aliases in `schema.py` bridge both (e.g., `silence` ↔ `muteAudio`).
4. **Use AppStateBus for cross-component communication** — not direct method calls between UI components.
5. **Handle falsy-but-valid config values** — `ConfigManager.get()` treats `0` and `False` as intentional, not missing. Use `default` parameter for truly absent keys.
6. **Theme colors** — GTK4 uses `@window_bg_color`, `@accent_bg_color` etc. Qt uses `Theme.js` constants. Never hard-code raw colors.

## Key Config/State Paths

| File | Path | Purpose |
|------|------|---------|
| User config | `~/.config/linux-wallpaperengine-gui/config.json` | Settings |
| Runtime state | `~/.local/state/linux-wallpaperengine-gui/state.json` | Active monitors, last wallpaper |
| History | `~/.config/linux-wallpaperengine-gui/history.json` | Playback history |
| Version | `py_GUI/const.py` `VERSION` | Single version string |

## Adding a New Setting

1. Add key + default in `py_GUI/core/schema.py`
2. Add UI controls in `py_GUI/ui/pages/settings/` (GTK4) or `py_GUI/ui/qt/qml/components/SettingsPage.qml` (Qt)
3. If it maps to an engine argument, update `py_GUI/core/controller.py`