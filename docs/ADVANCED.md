# Advanced Guide
[中文](ADVANCED_ZH.md)

This document provides a detailed overview of the advanced features and configuration options available in the Linux Wallpaper Engine GUI.

## Table of Contents

- [Command-Line Arguments](#command-line-arguments)
- [Configuration Reference](#configuration-reference)
- [Backend Parameter Mapping](#backend-parameter-mapping)
- [System Integration](#system-integration)
- [Playback History System](#playback-history-system)
- [Nickname Management](#nickname-management)
- [Compact Preview Mode](#compact-preview-mode)
- [Wayland Advanced Tweaks](#wayland-advanced-tweaks)
- [Screenshot Feature Details](#screenshot-feature-details)
- [Timed Rotation](#timed-rotation)
- [Multi-Monitor Configuration](#multi-monitor-configuration)
- [Log System](#log-system)
- [Troubleshooting](#troubleshooting)
- [Performance Tuning](#performance-tuning)

---

## Command-Line Arguments

### Launch Modes

```bash
# Launch in foreground (default)
python3 run_gui.py

# Launch in background (tray icon only)
python3 run_gui.py --hidden
python3 run_gui.py --minimized  # Alias for --hidden
```

### Window Control

All subsequent commands are sent to the already running instance (single-instance architecture):

```bash
# Show the window
python3 run_gui.py --show

# Hide the window (process keeps running)
python3 run_gui.py --hide

# Toggle show/hide state
python3 run_gui.py --toggle
```

### Wallpaper Control

```bash
# Apply the last used wallpaper
python3 run_gui.py --apply-last

# Randomly switch wallpaper
python3 run_gui.py --random

# Stop current wallpaper
python3 run_gui.py --stop

# Rescan wallpaper library
python3 run_gui.py --refresh
```

### Exit Program

```bash
# Fully exit (closes GUI and all wallpaper processes)
python3 run_gui.py --quit
```

---

## Configuration Reference

**Location**: `~/.config/linux-wallpaperengine-gui/config.json`

### Full Configuration Example

```json
{
  "workshopPath": "/home/user/.steam/steam/steamapps/workshop/content/431960",
  "assetsPath": "/home/user/.steam/steam/steamapps/common/wallpaper_engine/assets",
  "fps": 30,
  "volume": 50,
  "scaling": "default",
  "silence": true,
  "noFullscreenPause": false,
  "disableMouse": false,
  "clamping": "default",
  "disableParallax": false,
  "disableParticles": false,
  "disableAutoMute": false,
  "disableAudioProcessing": false,
  "autoStartEnabled": false,
  "silentStart": false,
  "autoRotateEnabled": false,
  "rotateInterval": 30,
  "cycleOrder": "random",
  "screenshotDelay": 10,
  "screenshotWidth": 3840,
  "screenshotHeight": 2160,
  "useXvfb": true,
  "lastWallpaper": "1234567890",
  "lastScreen": "eDP-1",
  "activeWallpapers": {
    "eDP-1": "1234567890",
    "HDMI-1": "9876543210"
  },
  "wallpaperProperties": {
    "1234567890": {
      "customProperty": "value"
    }
  }
}
```

### Configuration Fields

#### General Settings

| Field | Type | Default | Description |
|------|------|---------|-------------|
| `workshopPath` | string | Auto-detected | Path to Steam Workshop wallpaper directory |
| `assetsPath` | string | null | Path to Wallpaper Engine assets folder (null = auto-detect) |
| `fps` | int | 30 | Frame rate limit (1–144) |
| `volume` | int | 50 | Audio volume (0–100) |
| `scaling` | string | "default" | Scaling mode: `default`, `stretch`, `fit`, `fill` |
| `silence` | bool | true | Mute audio |

#### Advanced Rendering

| Field | Type | Default | Description |
|------|------|---------|-------------|
| `clamping` | string | "default" | Texture clamping mode: `default`, `clamp`, `border` |
| `disableParallax` | bool | false | Disable parallax effects |
| `disableParticles` | bool | false | Disable particle systems |

#### Audio Control

| Field | Type | Default | Description |
|------|------|---------|-------------|
| `disableAutoMute` | bool | false | Disable automatic muting when a window is fullscreen |
| `disableAudioProcessing` | bool | false | Disable audio processing logic |

#### Performance Optimization

| Field | Type | Default | Description |
|------|------|---------|-------------|
| `noFullscreenPause` | bool | false | Do not pause wallpaper when a window is fullscreen |
| `disableMouse` | bool | false | Disable mouse interaction |

#### Automation

| Field | Type | Default | Description |
|------|------|---------|-------------|
| `autoStartEnabled` | bool | false | Enable autostart on login |
| `silentStart` | bool | false | Silent start (background mode) |
| `autoRotateEnabled` | bool | false | Enable timed wallpaper rotation |
| `rotateInterval` | int | 30 | Rotation interval in minutes |
| `cycleOrder` | string | "random" | Cycle order: `random`, `title`, `size`, `type`, `id` |

#### Screenshot Configuration

| Field | Type | Default | Description |
|------|------|---------|-------------|
| `screenshotDelay` | int | 10 | Wait time before capture (seconds) |
| `screenshotWidth` | int | 3840 | Screenshot width |
| `screenshotHeight` | int | 2160 | Screenshot height |
| `useXvfb` | bool | true | Use Xvfb for silent screenshots |

#### State Persistence

| Field | Type | Description |
|------|------|-------------|
| `lastWallpaper` | string | ID of the last applied wallpaper |
| `lastScreen` | string | Name of the last selected screen |
| `activeWallpapers` | object | Mapping of current wallpapers per screen |
| `wallpaperProperties` | object | Custom properties for each wallpaper |

---

## Backend Parameter Mapping

GUI configurations are translated into command-line arguments for the `linux-wallpaperengine` backend:

| GUI Setting | Backend Argument | Description |
|-------------|------------------|-------------|
| `fps: 30` | `--fps 30` | Frame rate limit |
| `scaling: "stretch"` | `--scaling stretch` | Stretch scaling |
| `silence: true` | `--silent` | Mute audio |
| `volume: 50` | `--volume 50` | Audio volume |
| `noFullscreenPause: true` | `--no-fullscreen-pause` | Disable fullscreen pause |
| `disableMouse: true` | `--disable-mouse` | Disable mouse interaction |
| `clamping: "clamp"` | `--clamping clamp` | Texture clamping |
| `disableParallax: true` | `--disable-parallax` | Disable parallax |
| `disableParticles: true` | `--disable-particles` | Disable particles |
| `disableAutoMute: true` | `--no-auto-mute` | Disable auto-mute |
| `disableAudioProcessing: true` | `--no-audio-processing` | Disable audio processing |
| `assetsPath: "/path/to/assets"` | `--assets-dir /path/to/assets` | Custom assets directory |

### Full Command Example

```bash
linux-wallpaperengine \
  --screen-root eDP-1 \
  --fps 30 \
  --volume 50 \
  --scaling stretch \
  --silent \
  --no-fullscreen-pause \
  --disable-mouse \
  /path/to/wallpaper/folder
```

---

## System Integration

### Generate Desktop Shortcut

Clicking the "Create Desktop Entry" button in **Settings > General** generates:

**File Location**: `~/.local/share/applications/linux-wallpaperengine-gui.desktop`

**Example Content**:
```desktop
[Desktop Entry]
Type=Application
Name=Wallpaper Engine
Comment=Linux Wallpaper Engine GUI
Exec=/usr/bin/python3 /home/user/suw/run_gui.py
Icon=preferences-desktop-wallpaper
Terminal=false
Categories=Utility;
```

### Configure Autostart

Clicking the "Enable Autostart" button generates:

**File Location**: `~/.config/autostart/linux-wallpaperengine-gui.desktop`

If "Silent Start" is enabled, the `Exec` line becomes:
```
Exec=/usr/bin/python3 /home/user/suw/run_gui.py --hidden
```

### Window Manager Integration

#### Compact Mode Window Rules

Due to Wayland protocol limitations, the application cannot force window dimensions in tiling window managers (like Niri or Hyprland). For the best experience (floating mode), add the following rules to your WM configuration:

##### Niri (config.kdl)
```kdl
window-rule {
    match title="Wallpaper Preview"
    open-floating true
}
```

##### Hyprland (hyprland.conf)
```ini
windowrulev2 = float,title:^(Wallpaper Preview)$
windowrulev2 = size 300 700,title:^(Wallpaper Preview)$
windowrulev2 = center,title:^(Wallpaper Preview)$
```

#### Niri (Startup & Binds)

```kdl
spawn-at-startup "python3" "/home/user/suw/run_gui.py" "--hidden"

binds {
    Mod+W { spawn "python3" "/home/user/suw/run_gui.py" "--toggle"; }
    Mod+Shift+W { spawn "python3" "/home/user/suw/run_gui.py" "--random"; }
}
```

#### i3wm (config)

```
exec --no-startup-id python3 /home/user/suw/run_gui.py --hidden

bindsym $mod+w exec python3 /home/user/suw/run_gui.py --toggle
bindsym $mod+Shift+w exec python3 /home/user/suw/run_gui.py --random
```

#### Hyprland (hyprland.conf)

```
exec-once = python3 /home/user/suw/run_gui.py --hidden

bind = SUPER, W, exec, python3 /home/user/suw/run_gui.py --toggle
bind = SUPER SHIFT, W, exec, python3 /home/user/suw/run_gui.py --random
```

---

## Playback History System

Introduced in v0.10.3-beta, the Playback History system tracks your recently used wallpapers for quick access.

- **Capacity**: Stores up to 30 entries. It features auto-deduplication; re-applying a wallpaper already in history moves it to the top.
- **Access**: Open via the **Hamburger Menu (☰) → Playback History**.
- **Details**: Each entry displays a thumbnail, the wallpaper's nickname (in *italics*), the original ID, and a timestamp (formatted as `MM-DD HH:MM`).
- **One-Click Replay**: Clicking an entry immediately syncs the main window state and applies the wallpaper.
- **Management**: Includes a "Clear" button to wipe history and a capacity counter (e.g., `12 / 30`).

---

## Nickname Management

The Nickname System (v0.10.2) allows you to assign friendly names to wallpapers, making your library easier to navigate.

- **Storage**: Nicknames are persisted in `nicknames.json` via the `NicknameManager`.
- **Setting Nicknames**: Right-click any wallpaper in the grid and select "Set Nickname", or use the ✏️ button in the sidebar.
- **Batch Management**: Access the **Manage Nicknames** dialog in **Settings** to view, edit, or delete all nicknames in a single grid view.
- **Search Integration**: The global search bar matches both the custom nickname and the original wallpaper title.
- **Visuals**:
    - **Grid View**: Nicknames are displayed in **_italic bold_**.
    - **Sidebar**: Shows the "Nickname + Original Title" (the latter in small gray text).

---

## Compact Preview Mode

Designed specifically for tiling window managers (Niri, Hyprland, Sway), Compact Preview Mode (v0.10.0) provides a lightweight, standalone interface.

- **Behavior**: Operates as a separate window and is mutually exclusive with the main application window.
- **Dimensions**: Default size is 300×700.
- **Layout**:
    - **Top**: Large wallpaper preview with GIF animation support.
    - **Bottom**: 5 circular thumbnails with smooth wrap-around navigation.
- **Navigation**: Supports keyboard shortcuts (`←` and `→`) and on-screen navigation buttons.
- **Information**: Displays a blue capsule with the wallpaper ID (click to copy), the title, size, and index.
- **WM Rules**: It is highly recommended to set this window to "floating" in your WM config (see [System Integration](#compact-mode-window-rules)).

---

## Wayland Advanced Tweaks

Fine-grained control for Wayland sessions (v0.8.10) to handle compositor-specific behaviors.

- **Auto-Detection**: The GUI automatically detects if you are running a Wayland session.
- **Pause Only Active**: (`--fullscreen-pause-only-active`) Only pause the wallpaper when the currently focused window is fullscreen. This prevents background fullscreen windows from stopping your wallpaper.
- **Ignore App ID List**: (`--fullscreen-pause-ignore-appid`) A comma-separated list of App IDs (e.g., `waybar,niri`) that should be ignored by the fullscreen detection logic.
- **Use Case**: Prevents desktop components like docks, bars, or panels from accidentally triggering the wallpaper pause mechanism.

---

## Screenshot Feature Details

### How It Works

1. **Xvfb Detection**: Checks if `xvfb-run` is installed on the system.
2. **Mode Selection**:
   - **With Xvfb**: Silent mode (uses a virtual X server).
   - **Without Xvfb**: Window mode (opens a physical window briefly).
3. **Rendering**: Launches the backend with the `--screenshot` parameter.
4. **Smart Delay**:
   - **Video Wallpapers**: 5 seconds (fast sampling of the first frame).
   - **Web/Scene Wallpapers**: Uses the user-configured delay.
5. **Storage**: Screenshots are saved to `~/Pictures/wallpaperengine/`.

### Configuration

Available in **Settings > Advanced**:

- **Screenshot Delay**: Wait time before capture. Recommended: 5s for Video, 10-15s for Web/Scene.
- **Screenshot Resolution**: Default 3840x2160 (4K). This ensures high quality and avoids cropping issues in tiling WMs.
- **Use Xvfb for Screenshots**: Toggle between background silent capture and physical window mode.

### Resource Usage Statistics

Since v0.10.5, the screenshot process includes advanced resource monitoring:
- **High-Frequency Sampling**: Monitoring frequency increases to 0.1s during capture to catch short-lived tasks.
- **Hybrid Calculation**: For ultra-fast tasks (like video screenshots), it switches to CPU time delta calculation to ensure accuracy.
- **Normalization**: CPU usage is normalized across all cores (0-100% total system load) with peak filtering.

### Installation

```bash
# Arch Linux
sudo pacman -S xorg-server-xvfb

# Ubuntu/Debian
sudo apt install xvfb
```

---

## Timed Rotation

### Enabling Rotation

In **Settings > Automation**:
1. Check **Enable Auto Rotate**.
2. Set the **Rotate Interval** (in minutes).
3. Select the **Cycle Order**.
4. Click **Save Settings**.

### Cycle Order Options

Introduced in v0.8.11, you can choose how wallpapers are selected:
- **Random**: Selects a random wallpaper from the library.
- **Title (A-Z)**: Cycles alphabetically by title.
- **Size (↓/↑)**: Cycles by file size.
- **Type**: Cycles by wallpaper type (Video, Web, Scene).
- **ID**: Cycles by Steam Workshop ID.

**Configuration Key**: `cycleOrder`

### Mechanism

- Uses a `GLib.timeout_add_seconds` timer.
- Supports multi-monitor setups (all screens rotate simultaneously).
- Continues running even when the GUI window is hidden.
- Manual wallpaper application resets the timer.

---

## Multi-Monitor Configuration

### Screen Detection

The GUI automatically detects displays using:
1. **X11**: `xrandr --listmonitors`
2. **Wayland**: `wlr-randr` (if available)
3. **Fallback**: Allows manual entry of screen names.

### Independent Wallpapers

1. Select the target display from the dropdown in the top bar.
2. Browse and apply a wallpaper.
3. Repeat for other displays.

### Configuration Mapping

```json
{
  "activeWallpapers": {
    "eDP-1": "1234567890",   // Laptop internal screen
    "HDMI-1": "9876543210",  // External monitor
    "DP-1": "1122334455"     // Second external monitor
  }
}
```

### Known Issues

- Disconnected screens require manual cleanup (GUI cleans up on launch).
- Mixed refresh rates may cause inconsistent FPS.
- Scaling may behave unexpectedly on rotated screens.

---

## Log System

### Log Sources

- **Controller**: GUI control logic and process management.
- **Engine**: Output from the `linux-wallpaperengine` backend.
- **GUI**: GTK interface events and user interactions.

### Log Levels

- **DEBUG**: Detailed debugging information (Gray).
- **INFO**: General information (White).
- **WARNING**: Warnings (Yellow).
- **ERROR**: Errors (Red).

### File Locations

- **GUI Log**: `~/.config/linux-wallpaperengine-gui/app.log`
- **Engine Log**: `~/.config/linux-wallpaperengine-gui/engine_<wallpaper_id>.log`

### Viewing Logs

**In the GUI**:
- Go to **Settings > Logs**.
- Logs refresh automatically (or click **Refresh**).

**Via Terminal**:
```bash
# Follow GUI logs
tail -f ~/.config/linux-wallpaperengine-gui/app.log

# Follow engine logs
tail -f ~/.config/linux-wallpaperengine-gui/engine_*.log
```

---

## Troubleshooting

### Wallpaper Fails to Apply

**Symptoms**: Clicking Apply does nothing, or the wallpaper disappears immediately.

**Steps**:
1. Check **Settings > Logs** for errors.
2. Verify `linux-wallpaperengine` is in your PATH: `which linux-wallpaperengine`.
3. Try running the backend manually:
   ```bash
   linux-wallpaperengine --screen-root eDP-1 /path/to/wallpaper
   ```
4. Ensure the wallpaper folder contains a valid `project.json`.

### Screenshot Failures

**Symptoms**: No output file or error message when clicking the screenshot button.

**Steps**:
1. Check if the directory is writable: `ls -ld ~/Pictures/wallpaperengine`.
2. If using Xvfb, verify installation: `which xvfb-run`.
3. Try disabling Xvfb mode in **Settings > Advanced**.
4. Increase the **Screenshot Delay** to 10 seconds or more.

### System Tray Icon Missing

**Symptoms**: No icon appears in the tray area after launch.

**Steps**:
1. Verify `libayatana-appindicator` is installed.
2. Check for tray support in your environment:
   - **GNOME**: Requires "AppIndicator Support" extension.
   - **Waybar**: Ensure the `tray` module is enabled.
   - **i3/Sway**: May require `waybar` or a similar status bar.

---

## Performance Tuning

### Reducing CPU Usage

1. **Lower FPS**: Reduce from 30fps to 24fps or lower in **Settings > General**.
2. **Disable Particles**: Enable "Disable Particle Systems" in **Settings > Advanced**.
3. **Disable Parallax**: Enable "Disable Parallax Effects" in **Settings > Advanced**.
4. **Wallpaper Type**: Use **Video** wallpapers instead of Scene or Web types.

### Reducing Memory Usage

1. **Avoid Web Wallpapers**: They use an internal Chromium engine (CEF).
2. **Enable Timed Rotation**: Periodically restarts the backend to clear memory leaks.
3. **Disable Audio Processing**: Turn off in **Settings > Audio**.

### Reducing GPU Usage

1. Lower the FPS.
2. Use simpler wallpapers.
3. **Pause on Fullscreen**: Ensure "No Fullscreen Pause" is **unchecked**.

---

## Getting Help

If you cannot resolve an issue:

1. Consult [docs/COMPATIBILITY.md](COMPATIBILITY.md).
2. Search [GitHub Issues](https://github.com/your-repo/issues).
3. Submit a new Issue with:
   - System info (`uname -a`)
   - Desktop environment
   - Full logs (**Settings > Logs > Copy Logs**)
   - Wallpaper ID and type
