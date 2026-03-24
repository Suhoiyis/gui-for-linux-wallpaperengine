<strong>English</strong> | <a href="MIGRATION_ZH.md">中文</a>

# Migration Guide: Python to Tauri v2.0.0

This guide outlines the major changes and migration steps for moving from the legacy Python GTK implementation to the new Tauri React architecture.

## Python to Tauri

The project has migrated from Python/GTK to Tauri/React. Below are the key changes you need to know.

## Architecture Change: Python GTK → Tauri React

The project has undergone a complete architectural overhaul to improve performance, type safety, and user experience.

| Feature         | Legacy (Python)                  | New (Tauri v2.0.0)                            |
| :-------------- | :------------------------------- | :-------------------------------------------- |
| **Frontend**    | Python 3.10+ / GTK4 / Libadwaita | React / TypeScript / Tailwind CSS / shadcn/ui |
| **Backend**     | Python (Subprocess management)   | Rust (`lwg-core` crate)                       |
| **Engine**      | `linux-wallpaperengine` (C++)    | `linux-wallpaperengine` (C++)                 |
| **IPC**         | Abstract Socket (Tray <-> GUI)   | Tauri Commands & Events                       |
| **Performance** | Interpreter overhead             | Native Rust performance                       |

## Config File Change: Single File → 6 Separate Files

To better follow XDG specifications and improve data management, the configuration has been split from a single `config.json` into six specialized JSON files.

| File                        | Path                                        | Purpose                                         |
| :-------------------------- | :------------------------------------------ | :---------------------------------------------- |
| **config.json**             | `~/.config/linux-wallpaperengine-gui/`      | Main application settings (FPS, volume, paths). |
| **state.json**              | `~/.local/state/linux-wallpaperengine-gui/` | Runtime state (screen-to-wallpaper mappings).   |
| **nicknames.json**          | `~/.local/share/linux-wallpaperengine-gui/` | Custom wallpaper nicknames.                     |
| **favorites.json**          | `~/.local/share/linux-wallpaperengine-gui/` | List of favorited wallpaper IDs.                |
| **playback_history.json**   | `~/.cache/linux-wallpaperengine-gui/`       | History of the last 30 played wallpapers.       |
| **screenshot_history.json** | `~/.cache/linux-wallpaperengine-gui/`       | History of the last 10 screenshot records.      |

### Field Naming Compatibility

The new version maintains backward compatibility with legacy configuration files through Rust's `serde` aliases. While the frontend uses `camelCase`, the backend can still parse the old `snake_case` keys.

| Legacy Key (Python)     | New Key (Tauri)       | Notes                                            |
| :---------------------- | :-------------------- | :----------------------------------------------- |
| `silence`               | `muteAudio`           | Mutes all wallpaper audio.                       |
| `noautomute`            | `noAutomute`          | Prevents muting when other apps play sound.      |
| `wayland_only_active`   | `waylandOnlyActive`   | Pause only when the active window is fullscreen. |
| `wayland_ignore_appids` | `waylandIgnoreAppids` | List of App IDs to ignore for pausing.           |
| `compact_mode`          | `compactMode`         | Mini-window mode for tiling WMs.                 |
| `active_monitors`       | `AppState`            | Now stored in `state.json`.                      |

## Settings Tab Mapping

The settings interface has been reorganized for better clarity.

| Python Tab   | Tauri Tab    | Description                                                           |
| :----------- | :----------- | :-------------------------------------------------------------------- |
| **General**  | **Playback** | FPS, Scaling, Clamping, Parallax, Particles, Cycling, Wayland tweaks. |
| **Audio**    | **Display**  | Volume, Mute, Theme.                                                  |
| **Advanced** | **System**   | Paths, Autostart, Screenshot, Nicknames, Favorites.                   |
| **Logs**     | **Logs**     | Real-time logs from GUI, Core, Engine, and Controller.                |

## New Features

- **Playlist Support**: Create, edit, and cycle through custom wallpaper collections with a dedicated sidebar.
- **Favorites System**: One-click favoriting for quick access to your most-used wallpapers.
- **Batch Operations**: Improved management for nicknames and playlists.
- **Modern UI**: A faster, more responsive interface built with React and Tailwind CSS.
- **Enhanced Performance Monitor**: Real-time CPU/Memory charts with per-process breakdown (Frontend, Backend, Tray).
- **Tauri v2.0.0**: Leverages the latest Tauri features for better OS integration and security.
