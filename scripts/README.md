# AppImage Build Guide

This directory contains scripts for building the Linux Wallpaper Engine GUI as an AppImage.

## What is an AppImage?

An AppImage is a portable, self-contained executable that bundles the application and its dependencies into a single file. It:

- Requires no installation
- Works on any Linux distribution
- Can be run directly without sudo
- Is easily distributable

## Prerequisites

### System Requirements

- **Linux** (x86_64 architecture)
- **Python 3.10+**
- **appimagetool** - Download from https://github.com/AppImage/AppImageKit/releases

### Install appimagetool

**Arch Linux:**
```bash
sudo pacman -S appimagetool
```

**Ubuntu/Debian:**
```bash
sudo apt install appimagetool
```

**Manual Installation:**
```bash
# Download the AppImage
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

### System Dependencies

**Arch Linux:**
```bash
sudo pacman -S gtk4 libadwaita python-gobject python-pillow python-pyglet
```

**Ubuntu/Debian:**
```bash
sudo apt install libgtk-4-dev libadwaita-1-dev python3-gi gir1.2-gtk-4.0 \
                 gir1.2-adw-1 python3-pil python3-pyglet
```

### Backend (Required)

The GUI requires the `linux-wallpaperengine` backend:

```bash
# Follow: https://github.com/Almamu/linux-wallpaperengine
which linux-wallpaperengine  # Verify installation
```

## Building the AppImage

### Basic Usage

```bash
./scripts/build-appimage.sh
```

This will:
1. Create an AppDir structure at `build/AppDir`
2. Copy the Python application files
3. Install Python dependencies into the AppDir
4. Create wrapper scripts and entry points
5. Package desktop file and icon
6. Build the AppImage as `build/linux-wallpaperengine-gui-x86_64.AppImage`

### Advanced Options

```bash
# Specify custom AppDir location
./scripts/build-appimage.sh --appdir /tmp/AppDir

# Specify custom output directory
./scripts/build-appimage.sh --output /home/user/builds

# Both options
./scripts/build-appimage.sh --appdir /tmp/AppDir --output /home/user/builds

# Show help
./scripts/build-appimage.sh --help
```

## AppImage Structure

The generated AppImage contains:

```
AppImage (self-extracting)
├── AppRun                          # Entry point script
├── linux.wallpaperengine.gui.desktop  # Desktop integration
└── usr/
    ├── bin/
    │   └── linux-wallpaperengine-gui  # Executable wrapper
    ├── lib/
    │   └── python3.x/site-packages/   # Python dependencies
    ├── share/
    │   ├── applications/              # Desktop file
    │   └── icons/                     # Application icon
    └── opt/
        └── linux-wallpaperengine-gui/
            ├── py_GUI/                # Main application package
            └── run_gui.py             # Entry point
```

## Testing the AppImage

### Run directly:

```bash
./build/linux-wallpaperengine-gui-x86_64.AppImage
```

### Run in background (tray mode):

```bash
./build/linux-wallpaperengine-gui-x86_64.AppImage --hidden
```

### Get help:

```bash
./build/linux-wallpaperengine-gui-x86_64.AppImage --help
```

## Installing System-Wide

### Option 1: Copy to PATH

```bash
sudo cp build/linux-wallpaperengine-gui-x86_64.AppImage /usr/local/bin/
sudo chmod +x /usr/local/bin/linux-wallpaperengine-gui-x86_64.AppImage

# Create symlink (optional)
sudo ln -s /usr/local/bin/linux-wallpaperengine-gui-x86_64.AppImage /usr/local/bin/linux-wallpaperengine-gui
```

### Option 2: Use AppImageLauncher (recommended)

Install AppImageLauncher:
```bash
# Arch Linux
sudo pacman -S appimagelauncher

# Ubuntu/Debian
sudo add-apt-repository ppa:appimagelauncher-team/stable
sudo apt update && sudo apt install appimagelauncher
```

Then:
```bash
# Right-click the AppImage → Integrate
# Or run: ./build/linux-wallpaperengine-gui-x86_64.AppImage
```

## Desktop Integration

The AppImage includes a desktop file for system integration:

- **Desktop file**: `linux.wallpaperengine.gui.desktop`
- **Icon**: `pic/icons/GUI_rounded.png` (256×256 PNG)
- **Auto-integration**: The AppImage self-integrates into the desktop environment

## Troubleshooting

### AppImage won't start

**Check prerequisites:**
```bash
which python3
which appimagetool
```

**Run with debug output:**
```bash
APPIMAGE_DEBUG=1 ./build/linux-wallpaperengine-gui-x86_64.AppImage
```

### Missing dependencies

The script attempts to install Python dependencies, but some system libraries (GTK, Adwaita) must be installed system-wide:

```bash
# Arch Linux
sudo pacman -S gtk4 libadwaita python-gobject

# Ubuntu/Debian
sudo apt install libgtk-4-0 libadwaita-1 libgirepository1.0 gir1.2-gtk-4.0 gir1.2-adw-1
```

### Permission denied

Ensure the AppImage is executable:
```bash
chmod +x build/linux-wallpaperengine-gui-x86_64.AppImage
```

### Backend not found

The `linux-wallpaperengine` backend must be installed and in PATH:
```bash
which linux-wallpaperengine
# If not found, install from: https://github.com/Almamu/linux-wallpaperengine
```

## Build Configuration

Modify the script variables to customize the build:

| Variable | Default | Purpose |
|----------|---------|---------|
| `APPDIR` | `build/AppDir` | AppDir working directory |
| `OUTPUT_DIR` | `build` | Final AppImage output location |
| `PYTHON_VERSION` | `3` | Python major version |
| `ARCHITECTURE` | `x86_64` | Target architecture |
| `APP_NAME` | `Linux Wallpaper Engine GUI` | Application display name |
| `APP_ID` | `linux-wallpaperengine.gui` | Application ID |
| `EXECUTABLE_NAME` | `linux-wallpaperengine-gui` | Executable name |
| `ICON_SOURCE` | `pic/icons/GUI_rounded.png` | Icon file path |
| `DESKTOP_FILE` | `linux.wallpaperengine.gui.desktop` | Desktop file path |

## Size Optimization

The generated AppImage is typically 40–80 MB depending on system libraries.

**To reduce size:**
1. Use system-provided GTK and Adwaita libraries (current approach)
2. Avoid bundling heavy libraries (numpy, scipy, etc.)
3. Use UPX compression (optional, but may reduce compatibility):
   ```bash
   upx --best --lzma build/linux-wallpaperengine-gui-x86_64.AppImage
   ```

## Performance

The AppImage adds minimal overhead:
- **Startup time**: 1–2 seconds (FUSE mount overhead, cached)
- **Memory**: No additional overhead compared to system installation
- **Disk**: Single compressed file, uses less space than unpacked files

## Maintenance

### Rebuilding

To rebuild the AppImage after code changes:

```bash
./scripts/build-appimage.sh
```

The script automatically cleans the old AppDir and builds a new one.

### Updating Dependencies

To update Python dependencies, modify the `install_python_dependencies()` function in the script:

```bash
# Add new packages to the pip install command
python3 -m pip install \
    --target "$appdir_site_packages" \
    pillow pyglet newpackage  # Add here
```

## References

- [AppImage Documentation](https://docs.appimage.org/)
- [AppImageKit](https://github.com/AppImage/AppImageKit)
- [Linux Wallpaper Engine Backend](https://github.com/Almamu/linux-wallpaperengine)
- [Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/)
