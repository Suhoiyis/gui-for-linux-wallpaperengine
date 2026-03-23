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

- 🎨 **Light/Dark Theme Adaptive**: Fully adapts to your system theme with automatic accent color sync
- 🖥️ **Multi-Monitor Support**: Set independent wallpapers for each display with Link/Unlink mode
- ✏️ **Nickname System**: Assign custom nicknames to wallpapers for easier identification
- ⭐ **Favorites System**: Mark your favorite wallpapers for quick access (NEW)
- 📋 **Playlists**: Create custom wallpaper collections with drag-and-drop ordering (NEW)
- 🔍 **Search & Sort**: Real-time keyword search; sort by name, size, or ID
- 📺 **System Tray**: Native tray icon with play/stop/random controls
- ⌨️ **Command-Line Control**: Full CLI support for headless operation

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

## ⚙️ Configuration

Configuration files follow XDG specifications:

| File | Location | Purpose |
|------|----------|---------|
| `config.json` | `~/.config/linux-wallpaperengine-gui/` | Main settings |
| `state.json` | `~/.local/state/linux-wallpaperengine-gui/` | Runtime state |
| `nicknames.json` | `~/.local/share/linux-wallpaperengine-gui/` | Custom names |
| `favorites.json` | `~/.local/share/linux-wallpaperengine-gui/` | Favorites list |
| `playback_history.json` | `~/.cache/linux-wallpaperengine-gui/` | Playback history |
| `screenshot_history.json` | `~/.cache/linux-wallpaperengine-gui/` | Screenshot history |

For complete configuration reference, see [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

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

For detailed compatibility information, see [docs/old/COMPATIBILITY.md](docs/old/COMPATIBILITY.md).

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | Quick start guide |
| [docs/CONFIGURATION.md](docs/CONFIGURATION.md) | Complete settings reference |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues and solutions |
| [docs/MIGRATION.md](docs/MIGRATION.md) | Migration guide from Python version |
| [docs/old/](docs/old/) | Legacy Python version documentation |

## 🏛️ Technical Architecture

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
│  └──────────────────────────────────────────────┘│
└──────────────────────────────────────────────────┘
```

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