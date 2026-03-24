<strong>English</strong> | <a href="CONFIGURATION_ZH.md">中文</a>

# Configuration Reference

This document provides a complete reference for the configuration settings available in LWG (Linux Wallpaper Engine) GUI v2.0.0.

## Settings Reference

### Playback & Performance

| UI Label | JSON Key | Type | Default | Description |
|----------|----------|------|---------|-------------|
| Target FPS Limit | `fps` | `number` | `30` | Frame rate limit for wallpaper rendering (10–144). |
| Scaling Mode | `scaling` | `string` | `"default"` | How the wallpaper is scaled to fit the screen (`default`, `stretch`, `fit`, `fill`). |
| Texture Clamping | `clamping` | `string` | `"clamp"` | Texture wrapping mode (`clamp`, `border`, `repeat`). |
| Disable Parallax | `disableParallax` | `boolean` | `false` | Stop mouse movement parallax effects. |
| Disable Particles | `disableParticles` | `boolean` | `false` | Turn off rain, fire, and other particle effects. |
| No Fullscreen Pause | `noFullscreenPause` | `boolean` | `false` | Keep wallpapers playing even when a fullscreen application is open. |
| Disable Mouse Interaction | `disableMouse` | `boolean` | `false` | Ignore mouse clicks and interactions on the wallpaper. |
| Enable Auto-Cycle | `cycleEnabled` | `boolean` | `false` | Automatically switch wallpapers at a set interval. |
| Cycle Interval (minutes) | `cycleInterval` | `number` | `15` | Time between automatic wallpaper switches. |
| Cycle Order | `cycleOrder` | `string` | `"random"` | Order of wallpaper rotation (`random`, `id`). |
| Pause Only When Active | `waylandOnlyActive` | `boolean` | `false` | (Wayland only) Only pause the wallpaper if the application is focused. |
| Ignore Application IDs | `waylandIgnoreAppids` | `string` | `""` | (Wayland only) Comma-separated list of app IDs to ignore when auto-pausing. |

### Audio & Display

| UI Label | JSON Key | Type | Default | Description |
|----------|----------|------|---------|-------------|
| Mute Audio | `muteAudio` | `boolean` | `true` | Mute all audio output and disable audio processing. |
| Master Volume | `volume` | `number` | `0` | Global volume level (0–100). |
| Disable Auto Mute | `noAutomute` | `boolean` | `false` | Prevent the app from muting when other applications play sound. |
| No Audio Processing | `noAudioProcessing` | `boolean` | `false` | Disable spectrum analysis to save CPU resources. |
| App Appearance | `theme` | `string` | `"system"` | Interface theme (`system`, `dark`, `light`). |

### System & Tools

| UI Label | JSON Key | Type | Default | Description |
|----------|----------|------|---------|-------------|
| Steam Workshop Path | `workshopPath` | `string` | `null` | Path to your Steam Workshop wallpaper directory. |
| Assets Directory | `assetsPath` | `string` | `null` | Path to the engine assets directory (auto-detected if empty). |
| Run on Startup | `autostart` | `boolean` | `false` | Launch the application automatically on system login. |
| Start Hidden | `startHidden` | `boolean` | `false` | Minimize the application to the system tray on launch. |
| Auto Restore | `autoRestore` | `boolean` | `false` | Automatically restore the last used wallpapers on launch. |
| Target Resolution | `screenshotRes` | `string` | `"3840x2160"` | Resolution for wallpaper screenshots. |
| Prefer Silent Capture (Xvfb) | `preferXvfb` | `boolean` | `true` | Use Xvfb for background screenshots without a visible window. |
| Manage Nicknames | `wallpaperNicknames` | `object` | `{}` | Custom names assigned to specific wallpapers. |

### Log Monitor

| UI Label | JSON Key | Type | Default | Description |
|----------|----------|------|---------|-------------|
| Log Filter | `filter` | `string` | `"All"` | Filter logs by source (`All`, `GUI`, `Core`, `Engine`, `Controller`). |

## JSON Key Mapping Table

The configuration is stored in `~/.config/linux-wallpaperengine-gui/config.json`.

| UI Label | JSON Key | Type | Default |
|----------|----------|------|---------|
| Target FPS Limit | `fps` | `number` | `30` |
| Master Volume | `volume` | `number` | `0` |
| Scaling Mode | `scaling` | `string` | `"default"` |
| Mute Audio | `muteAudio` | `boolean` | `true` |
| No Fullscreen Pause | `noFullscreenPause` | `boolean` | `false` |
| Disable Mouse Interaction | `disableMouse` | `boolean` | `false` |
| Disable Auto Mute | `noAutomute` | `boolean` | `false` |
| No Audio Processing | `noAudioProcessing` | `boolean` | `false` |
| Disable Parallax | `disableParallax` | `boolean` | `false` |
| Disable Particles | `disableParticles` | `boolean` | `false` |
| Texture Clamping | `clamping` | `string` | `"clamp"` |
| Target Resolution | `screenshotRes` | `string` | `"3840x2160"` |
| Prefer Silent Capture (Xvfb) | `preferXvfb` | `boolean` | `true` |
| Enable Auto-Cycle | `cycleEnabled` | `boolean` | `false` |
| Cycle Interval (minutes) | `cycleInterval` | `number` | `15` |
| Cycle Order | `cycleOrder` | `string` | `"random"` |
| Assets Directory | `assetsPath` | `string` | `null` |
| Steam Workshop Path | `workshopPath` | `string` | `null` |
| Pause Only When Active | `waylandOnlyActive` | `boolean` | `false` |
| Ignore Application IDs | `waylandIgnoreAppids` | `string` | `""` |
| Compact Mode | `compactMode` | `boolean` | `false` |
| Start Hidden | `startHidden` | `boolean` | `false` |
| Auto Restore | `autoRestore` | `boolean` | `false` |
| Playlists | `playlists` | `array` | `[]` |
| Cycle Playlist ID | `cyclePlaylistId` | `string` | `null` |
| Playlist Sidebar Open | `playlistSidebarOpen` | `boolean` | `true` |

---

## Backend Parameter Mapping

GUI settings are translated into command-line arguments for the `linux-wallpaperengine` backend. This table shows how each GUI setting maps to the backend CLI:

| GUI Setting | Backend Argument | Example |
|-------------|------------------|---------|
| Target FPS Limit | `--fps` | `--fps 30` |
| Scaling Mode | `--scaling` | `--scaling stretch` |
| Mute Audio | `--silent` | `--silent` |
| Master Volume | `--volume` | `--volume 50` |
| No Fullscreen Pause | `--no-fullscreen-pause` | `--no-fullscreen-pause` |
| Disable Mouse Interaction | `--disable-mouse` | `--disable-mouse` |
| Texture Clamping | `--clamping` | `--clamping clamp` |
| Disable Parallax | `--disable-parallax` | `--disable-parallax` |
| Disable Particles | `--disable-particles` | `--disable-particles` |
| Disable Auto Mute | `--no-auto-mute` | `--no-auto-mute` |
| No Audio Processing | `--no-audio-processing` | `--no-audio-processing` |
| Assets Directory | `--assets-dir` | `--assets-dir /path/to/assets` |

### Full Command Example

When you apply a wallpaper, the GUI constructs a command like:

```bash
linux-wallpaperengine \
  --screen-root eDP-1 \
  --fps 30 \
  --volume 50 \
  --scaling default \
  --silent \
  --no-fullscreen-pause \
  /path/to/wallpaper/folder
```

### Wayland-Specific Arguments

| GUI Setting | Backend Argument | Description |
|-------------|------------------|-------------|
| Pause Only When Active | `--fullscreen-pause-only-active` | Only pause if the focused window is fullscreen |
| Ignore Application IDs | `--fullscreen-pause-ignore-appid` | Comma-separated app IDs to ignore (e.g., `waybar,niri`) |

---

## System Integration

### Autostart Configuration

Enable "Run on Startup" in Settings → System to launch the app automatically on login.

**Location**: `~/.config/autostart/linux-wallpaperengine-gui.desktop`

If "Start Hidden" is enabled, the app launches minimized to the system tray.

### Window Manager Integration

#### Compact Mode Window Rules

For the best experience in tiling window managers, add floating rules for the compact preview window:

**Niri** (config.kdl):
```kdl
window-rule {
    match title="Wallpaper Preview"
    open-floating true
}
```

**Hyprland** (hyprland.conf):
```ini
windowrulev2 = float,title:^(Wallpaper Preview)$
windowrulev2 = size 300 700,title:^(Wallpaper Preview)$
windowrulev2 = center,title:^(Wallpaper Preview)$
```

#### Startup & Keybinds

**Niri**:
```kdl
spawn-at-startup "path/to/lwg-gui" "--hidden"

binds {
    Mod+W { spawn "path/to/lwg-gui" "--toggle"; }
    Mod+Shift+W { spawn "path/to/lwg-gui" "--random"; }
}
```

**i3**:
```
exec --no-startup-id path/to/lwg-gui --hidden

bindsym $mod+w exec path/to/lwg-gui --toggle
bindsym $mod+Shift+w exec path/to/lwg-gui --random
```

**Hyprland**:
```ini
exec-once = path/to/lwg-gui --hidden

bind = SUPER, W, exec, path/to/lwg-gui --toggle
bind = SUPER SHIFT, W, exec, path/to/lwg-gui --random
```

---

## Performance Tuning

### Reducing CPU Usage

1. **Lower FPS**: Reduce from 30fps to 24fps or lower (Settings → Playback)
2. **Disable Particles**: Enable "Disable Particles" (Settings → Playback)
3. **Disable Parallax**: Enable "Disable Parallax" (Settings → Playback)
4. **Wallpaper Type**: Use Video wallpapers instead of Scene or Web types

### Reducing Memory Usage

1. **Avoid Web Wallpapers**: They use an internal Chromium engine (CEF)
2. **Enable Timed Rotation**: Periodically restarts the backend to clear memory leaks (Settings → Playback → Enable Auto-Cycle)
3. **Disable Audio Processing**: Turn off in Settings → Playback

### Reducing GPU Usage

1. Lower the FPS
2. Use simpler wallpapers (Video preferred over Scene)
3. Ensure "No Fullscreen Pause" is **unchecked** to pause when gaming

---

## Configuration File Locations

The application follows XDG Base Directory specifications:

| Type | Path | Purpose |
|------|------|---------|
| **Config** | `~/.config/linux-wallpaperengine-gui/` | Main settings (`config.json`) |
| **State** | `~/.local/state/linux-wallpaperengine-gui/` | Runtime state (`state.json`) |
| **Data** | `~/.local/share/linux-wallpaperengine-gui/` | Persistent data (nicknames, favorites, playlists) |
| **Cache** | `~/.cache/linux-wallpaperengine-gui/` | Temporary data (history, logs) |

### File Summary

| File | Location | Purpose |
|------|----------|---------|
| `config.json` | `~/.config/linux-wallpaperengine-gui/` | Main settings |
| `state.json` | `~/.local/state/linux-wallpaperengine-gui/` | Runtime state (screen → wallpaper mappings) |
| `nicknames.json` | `~/.local/share/linux-wallpaperengine-gui/` | Custom wallpaper names |
| `favorites.json` | `~/.local/share/linux-wallpaperengine-gui/` | Favorites list |
| `playlists.json` | `~/.local/share/linux-wallpaperengine-gui/` | User playlists |
| `playback_history.json` | `~/.cache/linux-wallpaperengine-gui/` | Recent wallpaper history |
| `screenshot_history.json` | `~/.cache/linux-wallpaperengine-gui/` | Screenshot history |

---

## Related Documentation

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [MIGRATION.md](MIGRATION.md) - Migration guide from Python version
- [docs/old/ADVANCED.md](old/ADVANCED.md) - Legacy Python documentation (for reference)
