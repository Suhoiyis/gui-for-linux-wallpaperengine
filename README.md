<h1 align="center">
  <img src="pic/icons/GUI_rounded.png" alt="Logo" width="128" height="128" style="border-radius: 20px;"/><br>
  LINUX WALLPAPER ENGINE GUI
</h1>

<p align="center">A modern desktop interface for managing and applying Steam Workshop live wallpapers on Linux, built with Tauri + React + Rust.</p>

<p align="center">
  <a href="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases/latest">
    <img src="https://img.shields.io/github/v/release/Suhoiyis/gui-for-linux-wallpaperengine?color=success&label=Release&style=flat-square" alt="Latest Release">
  </a>
  <a href="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Suhoiyis/gui-for-linux-wallpaperengine?style=flat-square&color=blue" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Platform-Linux-lightgrey?style=flat-square&logo=linux" alt="Platform">
  <img src="https://img.shields.io/badge/Tauri-v2-24c8d8?style=flat-square&logo=tauri" alt="Tauri">
  <img src="https://img.shields.io/badge/React-19-61dafb?style=flat-square&logo=react" alt="React">
  <img src="https://img.shields.io/badge/Rust-1.75+-dea584?style=flat-square&logo=rust" alt="Rust">
</p>

<p align="center">
    <strong>English</strong> | 
    <a href="README_ZH.md">简体中文</a>
<p>

> Built on [Almamu/linux-wallpaperengine](https://github.com/Almamu/linux-wallpaperengine) backend, optimized for GNOME / Wayland desktop environments.

## ✨ Features

### Core Features

- 🎨 **Light/Dark Theme Adaptive**: Adapts to your system's light or dark theme
- 🖥️ **Multi-Monitor Support**: Set independent wallpapers for each display via screen selector dropdown
- ✏️ **Nickname System**: Assign custom nicknames to wallpapers for easier identification
- ⭐ **Favorites System**: Mark your favorite wallpapers for quick access (NEW)
- 📋 **Playlists**: Create custom wallpaper collections with drag-and-drop ordering (NEW)
- 🔍 **Search & Sort**: Real-time keyword search; sort by name, size, or ID
- 📺 **System Tray**: Native tray icon with play/stop/random controls

### Advanced Features

- 🪟 **Compact Mode**: Mini-window designed for tiling window managers
- 📊 **Performance Monitor**: Real-time CPU/memory tracking with charts and process breakdown
- 📸 **Smart Screenshot**: Silent 4K capture via Xvfb with screenshot history
- 🔄 **Timed Rotation**: Auto-switch wallpapers at configurable intervals
- 🎛️ **Wayland Tweaks**: Fine-grained control for Wayland-specific behavior
- 📋 **Log Management**: Filter logs by source (GUI/Core/Engine/Controller)

## 🚀 Installation

### 1. Install the Backend (Required)

This GUI requires the core rendering engine:

```bash
# Arch Linux
yay -S linux-wallpaperengine

# Other distributions
# Follow build instructions at https://github.com/Almamu/linux-wallpaperengine
```

Verify installation:
```bash
which linux-wallpaperengine  # Should output the path
```

### 2. Install the GUI

Download the AppImage from the [Releases page](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases):

```bash
# Make it executable
chmod +x lwg-gui-*-x86_64.AppImage

# Run it
./lwg-gui-*-x86_64.AppImage
```

### System Requirements

- Ubuntu 22.04+ or equivalent
- `webkit2gtk-4.1` (usually pre-installed on modern distros)

```bash
# Ubuntu/Debian
sudo apt install libwebkit2gtk-4.1-0
```

## 📖 Basic Usage

### Browse & Apply Wallpapers

1. **Browse**: The app automatically scans your Steam Workshop wallpaper library on first launch
2. **Apply**: Double-click a wallpaper card or click the **Apply** button
3. **Random**: Click the 🎲 button or use the tray menu
4. **Stop**: Click the ⏹ button
5. **Multi-Monitor**: Select target display from the top bar dropdown

### Playlists & Favorites

- **Create Playlist**: Click "+" in the sidebar or select multiple wallpapers and create a new playlist
- **Add to Favorites**: Click the ⭐ icon on any wallpaper card
- **Quick Access**: Favorites and playlists appear in the sidebar

### Settings Organization

Settings are organized into 4 tabs:

| Tab | Settings |
|-----|----------|
| **Playback** | FPS, Scaling, Clamping, Parallax, Particles, Cycling, Wayland tweaks |
| **Display** | Volume, Mute, Theme |
| **System** | Paths, Autostart, Screenshot, Nicknames, Favorites |
| **Logs** | Real-time log viewer with filtering |

## 🚀 Autostart

The app can be configured to launch automatically on login via **Settings → System → Run on Startup**.

To start the app hidden (minimized to tray), enable **Settings → System → Start Hidden**.

**Example:** Autostart with Niri
```bash
# In your niri config.kdl
spawn-at-startup "path/to/linux-wallpaperengine-gui" "--hidden"
```

**Example:** Autostart with Hyprland
```ini
# In your hyprland.conf
exec-once = path/to/linux-wallpaperengine-gui --hidden
```

**Example:** Autostart with i3
```
# In your i3 config
exec --no-startup-id path/to/linux-wallpaperengine-gui --hidden
```

## ⚙️ Configuration

Configuration files follow XDG specifications. For a complete list of settings and file locations, see [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## ⚠️ Known Limitations

### Wallpaper Type Compatibility

| Type | Status | Notes |
|------|--------|-------|
| **Video** | ✅ Fully supported | MP4/WebM recommended |
| **Web** | ⚠️ Partial | Property adjustments may not work |
| **Scene** | ⚠️ Limited | Complex shaders may glitch |

### Wayland Limitations

- ❌ **Mouse interaction disabled**: Cannot obtain global cursor position
- ❌ **Web property injection limited**: CEF communication restricted

## ❓ FAQ

### System tray icon is not showing

1. GNOME users: Install the "AppIndicator Support" extension
2. Waybar users: Ensure the `tray` module is configured
3. i3/Sway users: You may need `waybar` or another status bar with tray support

### How do I set different wallpapers for each monitor?

Select the target display from the top bar dropdown (e.g., "eDP-1" or "HDMI-A-1"), then browse and apply a wallpaper. To apply the same wallpaper to all monitors, select "All Screens" from the dropdown.

### The compact preview window doesn't float in my tiling WM

You need to add a window rule in your WM configuration. For Niri and Hyprland examples, see [docs/old/ADVANCED.md](docs/old/ADVANCED.md#compact-preview-mode).

### Can I use this with Flatpak or AppImage?

**AppImage**: Fully supported. Download, make executable, and run.

**Flatpak**: Not officially supported yet. File access and sandbox restrictions may affect functionality.

### How do I report a bug?

1. Go to Settings → Logs and click **Copy Logs**
2. Open a [GitHub Issue](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues)
3. Include: system info (`uname -a`), desktop environment, wallpaper ID/type, and the copied logs

For more troubleshooting help, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md). For performance tuning, see [docs/CONFIGURATION.md](docs/CONFIGURATION.md#performance-tuning).

## 🔄 Update & Uninstall

### Updating

Download the latest AppImage from the [Releases page](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases) and replace the old file. Your configuration and playlists are preserved in `~/.config/linux-wallpaperengine-gui/`.

### Uninstalling

1. **AppImage**: Simply delete the AppImage file
2. **Config files** (optional):
   ```bash
   rm -rf ~/.config/linux-wallpaperengine-gui
   rm -rf ~/.local/state/linux-wallpaperengine-gui
   rm -rf ~/.local/share/linux-wallpaperengine-gui
   rm -rf ~/.cache/linux-wallpaperengine-gui
   ```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | Version history and release notes |
| [docs/CONFIGURATION.md](docs/CONFIGURATION.md) | Complete settings reference |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues and solutions |
| [docs/MIGRATION.md](docs/MIGRATION.md) | Migration guide from Python version |
| [docs/old/](docs/old/) | Legacy Python version documentation |

## 🏛️ Technical Architecture

### Project Structure

```
gui-for-linux-wallpaperengine/
├── lwg-gui-tauri/              # Main Tauri application
│   ├── src/                     # React frontend
│   │   ├── components/          # UI components (library, settings, performance)
│   │   ├── pages/               # Page views (Library, Settings, Performance)
│   │   ├── store/               # Zustand state management
│   │   └── api/                 # Tauri API wrappers
│   └── src-tauri/               # Rust backend
│       └── src/lib.rs           # Tauri commands and business logic
│
├── lwg-rs/                      # Rust core library
│   └── crates/lwg-core/         # Config, controller, wallpaper management
│
├── py_GUI/                      # Legacy Python version (reference only)
├── docs/                        # Documentation
│   ├── old/                     # Legacy Python documentation
│   └── assets/                  # Screenshots and images
└── pic/                         # Application icons
```

### Architecture Overview

```
┌──────────────────────────────────────────────────┐
│           Tauri + React + TypeScript             │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ Library  │  │ Settings │  │  Performance   │  │
│  │   Page   │  │   Page   │  │    Monitor     │  │
│  └────┬─────┘  └────┬─────┘  └───────┬────────┘  │
│       │             │                │           │
│  ┌────┴─────────────┴────────────────┴─────────┐ │
│  │         lwg-core (Rust crate)               │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐ │ │
│  │  │ Config   │ │ State    │ │  History     │ │ │
│  │  │ Manager  │ │ Manager  │ │  Manager     │ │ │
│  │  └──────────┘ └──────────┘ └──────────────┘ │ │
│  └──────────────────┬──────────────────────────┘ │
│                     │ subprocess                 │
│  ┌──────────────────┴───────────────────────────┐│
│  │         linux-wallpaperengine (C++)          ││
│  │         Rendering · Audio · Screenshot       ││
│  └──────────────────────────────────────────────┘│
└──────────────────────────────────────────────────┘
```

### Key Design Decisions

- **Single-instance architecture**: Only one instance can run at a time; second launch focuses the existing window
- **Hybrid save strategy**: Optimistic UI updates with debounced backend persistence
- **XDG compliance**: Config, state, and cache files follow XDG specifications
- **Type-safe IPC**: Full TypeScript types for Tauri commands

## 🔧 Tech Stack

- **Frontend**: React 19 + TypeScript + Tailwind CSS + shadcn/ui
- **Backend**: Tauri v2 + Rust (lwg-core crate)
- **Engine**: Almamu/linux-wallpaperengine (C++)
- **State**: Zustand with optimistic updates

## 🤝 Contributing

Contributions are welcome! 

- Feature requests and bug reports → [Open an Issue](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues)
- Code contributions → Submit a Pull Request

## 🙏 Acknowledgements

> Some UI design inspiration was drawn from [AzPepoze/linux-wallpaperengine-gui](https://github.com/AzPepoze/linux-wallpaperengine-gui).

## 📄 License

GPL-3.0 license

---

**Current Version**: v2.0.0

**Last Updated**: 2026-03-23