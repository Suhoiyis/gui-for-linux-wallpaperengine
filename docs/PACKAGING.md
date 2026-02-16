# Packaging Guide for Linux Wallpaper Engine GUI

This document provides comprehensive instructions for building and distributing the Linux Wallpaper Engine GUI application as an AppImage and Arch Linux package.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [AppImage Package](#appimage-package)
  - [System Requirements](#appimage-system-requirements)
  - [Building the AppImage](#building-the-appimage)
  - [AppImage Usage](#appimage-usage)
- [Arch Linux Package](#arch-linux-package)
  - [System Requirements](#arch-package-system-requirements)
  - [Building from PKGBUILD](#building-from-pkgbuild)
  - [Installing the Package](#installing-the-package)
- [GitHub Actions CI/CD](#github-actions-cicd)
- [Troubleshooting](#troubleshooting)

## Overview

The Linux Wallpaper Engine GUI application is distributed in two primary formats:

1. **AppImage** - A universal Linux package that runs on most modern Linux distributions without installation
2. **Arch Linux Package** - A native package for Arch Linux and its derivatives (Manjaro, EndeavourOS, etc.)

Both packages use a **"system-gtk"** approach, meaning they rely on the host system to provide GTK4, libadwaita, and Python GObject bindings rather than bundling these large dependencies.

## Prerequisites

### For Building

- A Linux system with Python 3.10 or later
- Git (for cloning the repository)
- For AppImage: `appimagetool` (will be downloaded automatically by the build script)
- For Arch package: `base-devel` package group, Python build tools

### For Running

See the system requirements for each package format below.

## AppImage Package

### AppImage System Requirements

The AppImage requires the following to be pre-installed on the host system:

**Required (will fail without):**
- GTK4 (libgtk-4-1)
- libadwaita (libadwaita-1-0)
- Python 3.10 or later
- Python GObject bindings (PyGObject)
- Cairo (libcairo2)
- GObject introspection data (gir1.2-gtk-4.0, gir1.2-adw-1)

**Recommended (for full functionality):**
- MPV media player (for video wallpapers)
- Wallpaper Engine assets (from Steam)
- Python Pillow (PIL) - may be bundled or system-provided
- Python Pyglet - may be bundled or system-provided

**Distributions Tested:**
- Ubuntu 22.04 LTS and later
- Fedora 37 and later
- Arch Linux (rolling)
- openSUSE Tumbleweed

### Building the AppImage

#### Method 1: Using the Build Script

```bash
# Navigate to the project directory
cd /path/to/linux-wallpaperengine-gui

# Make the script executable
chmod +x scripts/build-appimage.sh

# Run the build script
./scripts/build-appimage.sh
```

The script will:
1. Check for `appimagetool` and download it if not present
2. Create the AppDir structure
3. Install the Python application and its dependencies
4. Create wrapper scripts
5. Build the final AppImage

The resulting AppImage will be in `build/linux-wallpaperengine-gui-<version>-x86_64.AppImage`

#### Method 2: Manual Build

For more control, you can manually create the AppImage:

```bash
# Create AppDir structure
mkdir -p build/AppDir/usr/bin
mkdir -p build/AppDir/usr/lib
mkdir -p build/AppDir/usr/share/applications
mkdir -p build/AppDir/usr/share/icons/hicolor/256x256/apps

# Install the application
pip install --prefix=build/AppDir/usr --no-deps .

# Copy additional files
cp linux.wallpaperengine.gui.desktop build/AppDir/usr/share/applications/
cp pic/icons/GUI_rounded.png build/AppDir/usr/share/icons/hicolor/256x256/apps/linux-wallpaperengine-gui.png

# Create AppRun
cat > build/AppDir/AppRun << 'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$HERE/usr/lib/python3.11/site-packages:$PYTHONPATH"
export PATH="$HERE/usr/bin:$PATH"
exec "$HERE/usr/bin/python3" -m linux_wallpaperengine_gui "$@"
EOF
chmod +x build/AppDir/AppRun

# Build AppImage
appimagetool build/AppDir build/linux-wallpaperengine-gui-$(git describe --tags | sed 's/^v//')-x86_64.AppImage
```

### AppImage Usage

#### Running the AppImage

```bash
# Make executable
chmod +x linux-wallpaperengine-gui-<version>-x86_64.AppImage

# Run directly
./linux-wallpaperengine-gui-<version>-x86_64.AppImage

# Or move to a location in PATH
mv linux-wallpaperengine-gui-<version>-x86_64.AppImage ~/.local/bin/linux-wallpaperengine-gui
chmod +x ~/.local/bin/linux-wallpaperengine-gui
linux-wallpaperengine-gui
```

#### Desktop Integration

The AppImage automatically handles desktop integration:

1. **First run**: The AppImage detects it's running from a non-standard location and offers to create a desktop entry
2. **AppImageUpdate**: If using AppImageUpdate for updates, desktop entries are automatically updated
3. **Manual integration**: Users can use the `--appimage-extract` option to manually extract and integrate

The application also provides a "Create Desktop Entry" button in Settings that creates a desktop file with the correct paths, including support for the `$APPIMAGE` environment variable.

## Arch Linux Package

### Arch Package System Requirements

The Arch Linux package has the following dependencies that will be automatically installed by `pacman`:

**Runtime dependencies (automatically installed):**
- gtk4
- libadwaita
- python (>=3.10)
- python-gobject
- python-pillow
- python-pyglet
- mpv (optional but recommended)
- wallpaper-engine-libwrap (shared library, must be installed separately or provided)

**Build dependencies (only needed for building):**
- git
- base-devel (group)
- python-build
- python-installer
- python-wheel
- python-setuptools

### Building from PKGBUILD

#### Method 1: Using makepkg

```bash
# Clone the repository or download the PKGBUILD
cd /path/to/linux-wallpaperengine-gui

# Install build dependencies
sudo pacman -S --needed base-devel git python-build python-installer python-wheel python-setuptools

# Build the package
makepkg -s

# The resulting package will be:
# linux-wallpaperengine-gui-<version>-x86_64.pkg.tar.zst
```

#### Method 2: Building in a Clean Environment

For a clean build without affecting your system:

```bash
# Install devtools (if not already installed)
sudo pacman -S devtools

# Build in a clean chroot
mkdir -p ~/build/chroot
cd /path/to/linux-wallpaperengine-gui

# Copy PKGBUILD and necessary files
cp PKGBUILD linux.wallpaperengine.gui.desktop ~/build/chroot/
cp -r pic ~/build/chroot/

# Build
extra-x86_64-build ~/build/chroot/PKGBUILD
```

### Installing the Package

#### Local Installation with pacman

```bash
# Install the pre-built package
sudo pacman -U linux-wallpaperengine-gui-<version>-x86_64.pkg.tar.zst

# Or with explicit confirmation
sudo pacman -U --noconfirm linux-wallpaperengine-gui-<version>-x86_64.pkg.tar.zst
```

#### Removing the Package

```bash
# Remove the package
sudo pacman -R linux-wallpaperengine-gui

# Or remove with unused dependencies
sudo pacman -Rs linux-wallpaperengine-gui
```

#### Querying Package Information

```bash
# Show package details
pacman -Qi linux-wallpaperengine-gui

# List package files
pacman -Ql linux-wallpaperengine-gui

# Check for file conflicts
pacman -Qk linux-wallpaperengine-gui
```

## GitHub Actions CI/CD

The project includes a GitHub Actions workflow for automated building and releasing.

### Workflow Triggers

The workflow is triggered by:

1. **Git tags** (e.g., `v1.0.0`) - Automatically builds and releases
2. **Manual workflow dispatch** - Allows building test versions

### Workflow Jobs

The workflow consists of three jobs:

1. **build-appimage**: Builds the AppImage package on Ubuntu
2. **build-arch-package**: Builds the Arch Linux package in an Arch container
3. **create-release**: Combines artifacts and creates a GitHub release

### Release Artifacts

Each release includes:

- `linux-wallpaperengine-gui-<version>-x86_64.AppImage` - Universal Linux package
- `linux-wallpaperengine-gui-<version>-x86_64.pkg.tar.zst` - Arch Linux package

### Using the Workflow

#### Creating a Release

```bash
# Tag a new version
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push the tag to trigger the workflow
git push origin v1.0.0
```

#### Testing the Workflow

1. Go to the Actions tab in your GitHub repository
2. Select the "Release AppImage and Arch Package" workflow
3. Click "Run workflow"
4. Enter a test version tag (e.g., `v0.0.0-test`)
5. Click "Run workflow"

## Troubleshooting

### Common Issues

#### AppImage Issues

**Issue**: AppImage fails to start with GTK errors
- **Cause**: Missing GTK4/libadwaita on host system
- **Solution**: Install system dependencies (see AppImage System Requirements)

**Issue**: `appimagetool: command not found`
- **Cause**: appimagetool not installed
- **Solution**: Download from https://github.com/AppImage/AppImageKit/releases

**Issue**: AppImage doesn't show icon in file manager
- **Cause**: File manager doesn't support AppImage icons
- **Solution**: Extract the AppImage and create a proper desktop entry manually

#### Arch Package Issues

**Issue**: `makepkg: command not found`
- **Cause**: base-devel group not installed
- **Solution**: `sudo pacman -S base-devel`

**Issue**: Package build fails with "missing dependencies"
- **Cause**: Build dependencies not installed
- **Solution**: Install makedepends listed in PKGBUILD

**Issue**: `pacman -U` fails with "conflicting files"
- **Cause**: Files from manual installation exist
- **Solution**: Remove conflicting files manually, or use `--overwrite '*'` flag

**Issue**: Package installs but application doesn't start
- **Cause**: Missing runtime dependencies
- **Solution**: Check `pacman -Qi linux-wallpaperengine-gui` for missing dependencies

#### GitHub Actions Issues

**Issue**: Workflow fails with "permission denied"
- **Cause**: Scripts not executable
- **Solution**: Ensure scripts have `chmod +x` in the repository

**Issue**: Arch package build fails in container
- **Cause**: Outdated Arch Linux container
- **Solution**: Update the container base image or wait for upstream updates

**Issue**: Artifacts not uploaded to release
- **Cause**: Artifact paths don't match
- **Solution**: Check the upload-artifact step for correct paths

### Getting Help

If you encounter issues not covered here:

1. Check the project README for updated information
2. Review the GitHub Issues page for similar problems
3. Run the application with debug logging: `linux-wallpaperengine-gui --verbose`
4. For AppImage issues, extract and run manually: `./app.AppImage --appimage-extract && ./squashfs-root/AppRun`

---

**Last Updated**: 2025-02-16  
**Package Version**: See git tags for current version  
**Maintainer**: Project maintainers (see GitHub repository)