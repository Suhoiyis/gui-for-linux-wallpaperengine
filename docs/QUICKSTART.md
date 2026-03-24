<strong>English</strong> | <a href="QUICKSTART_ZH.md">中文</a>

# Quickstart Guide

This guide helps you set up and start using the Linux Wallpaper Engine (LWG) GUI on your system.

## System Requirements

LWG GUI needs a modern Linux distribution like Ubuntu 22.04 or newer. The application relies on WebKitGTK for the webview.

Install the webview dependency on Ubuntu or Debian:
```bash
sudo apt install libwebkit2gtk-4.1-0
```

**Arch Linux / Manjaro:**
```bash
sudo pacman -S webkit2gtk-4.1
```

## Installation

### 1. Install the Backend

The GUI works as a controller for the `linux-wallpaperengine` rendering engine. You need to install this backend before running the app.

**Arch Linux users** can install it from the AUR:
```bash
yay -S linux-wallpaperengine
```

**Other distributions** should follow the instructions at the [official repository](https://github.com/Almamu/linux-wallpaperengine).

**Verify the installation** by running:
```bash
which linux-wallpaperengine
```
The command should return a path like `/usr/bin/linux-wallpaperengine`.

### 2. Download the GUI

Get the latest AppImage from the [Releases page](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases). Download the file named `linux-wallpaperengine-gui-v2.0.0-x86_64.AppImage`.

## First Launch

Find the AppImage file you just downloaded. Right-click it and choose **Properties**, then enable the option to **Allow executing file as program**. You can also use the terminal:
```bash
chmod +x linux-wallpaperengine-gui-v2.0.0-x86_64.AppImage
```
Double-click the file to start the app. It'll scan your Steam Workshop folders for wallpapers automatically.

## Basic Usage Flow

### Applying a Wallpaper
Open the **Library** tab to see your wallpapers. Click any card to view its details, then hit the **Apply** button.

### Multi-Monitor Setup
Use the monitor dropdown at the top to pick a specific screen or select "All Screens" to apply the same wallpaper to all displays.

### System Tray
The app puts an icon in your system tray. Right-click it to pause, resume, or change wallpapers quickly.
