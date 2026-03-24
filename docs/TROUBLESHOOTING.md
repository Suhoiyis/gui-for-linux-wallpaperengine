<strong>English</strong> | <a href="TROUBLESHOOTING_ZH.md">中文</a>

# 🐛 Troubleshooting Guide (Tauri v2.0.0)

This guide helps you resolve common issues with the LWG (Linux Wallpaper Engine) GUI and its backend.

## Common Issues

This section covers the most frequent problems users encounter.

- **Wallpaper not showing**: Ensure `linux-wallpaperengine` is installed and the Assets path is correct.
- **Tray icon missing**: Check if your desktop environment supports AppIndicators (see Tray Icon section).
- **Multi-monitor**: Use the screen dropdown in the top bar to select a specific monitor or "All Screens".
- **Wayland performance**: If the wallpaper is laggy, try lowering the FPS limit in Settings.

---

## 1. Common Installation Issues

### Backend Requirement

The GUI is a controller and requires the core rendering engine to be installed.

- **Issue**: "Wallpaper engine failed to start" or "Command not found".
- **Solution**: Ensure `linux-wallpaperengine` is installed and available in your `PATH`.
  - Arch Linux: `yay -S linux-wallpaperengine`
  - Others: Build from [Almamu/linux-wallpaperengine](https://github.com/Almamu/linux-wallpaperengine).

### System Dependencies

- **Tauri Runtime**: Requires `webkit2gtk`. Most distributions include this, but if the GUI fails to launch, ensure it's installed.
- **Display Detection**: The app reads `/sys/class/drm` directly to detect connected monitors. No external tools are required.

### Path Configuration

- **Workshop Path**: Must point to the Steam Workshop folder (usually ending in `431960`).
- **Assets Path**: Must point to the `assets` folder of `Wallpaper Engine`.
- **Fix**: Go to **Settings > System** to verify and update these paths.

---

## 2. Wallpaper Not Playing

### Check the Logs

If a wallpaper fails to start, the first step is always to check the logs.

1. Open **Settings > Log Monitor**.
2. Look for red `ERROR` entries.
3. Common errors:
   - `Failed to initialize GLEW`: OpenGL/GLX environment issues.
   - `Cannot find a valid assets folder`: Incorrect Assets path in Settings.
   - `Process exited immediately`: The backend crashed; check the `Engine` source logs for details.

### Corrupted Wallpapers

- **Symptom**: Some wallpapers load while others don't.
- **Solution**: Right-click the wallpaper and select "Open in File Manager". Check if `project.json` exists and is valid. You may need to re-subscribe to the wallpaper on Steam.

---

## 3. Tray Icon Not Showing

The system tray implementation depends on your desktop environment's support for StatusNotifierItem (SNI).

- **GNOME**: Install the **"AppIndicator and KStatusNotifierItem Support"** extension.
- **KDE Plasma**: Should work out of the box.
- **Waybar (Sway/Hyprland)**: Ensure the `tray` module is included in your Waybar configuration.
- **i3/Other WMs**: Ensure you have a system tray handler (like `nm-applet` or `pasystray`) running.

---

## 4. Multi-Monitor Issues

### Independent Wallpapers

- **How to**: Select the target display from the dropdown in the top bar, then apply a wallpaper.
- **All Screens**: Select "All Screens" from the dropdown to apply the same wallpaper to all monitors.

### Screen Name Mismatch

- **Issue**: Wallpapers don't restore after a reboot or monitor reconnection.
- **Reason**: If your OS changes the connector name (e.g., `HDMI-A-1` to `HDMI-A-2`), the saved state in `state.json` won't match.
- **Solution**: Re-apply the wallpaper to the new screen name.

---

## 5. Wayland-Specific Issues

### Protocol Limitations

Wayland's security model introduces several limitations:

- **No Mouse Interaction**: Global mouse coordinates cannot be obtained. Mouse trails, parallax effects, and click interactions in wallpapers will not work.
- **No "Primary" Display**: Unlike X11, Wayland compositors often don't define a "primary" monitor in a way that CLI tools can consistently report.
- **Web Property Injection**: CEF (Chromium) property injection often fails on Wayland due to GLX/OpenGL context issues. You may need to manually edit `project.json` to change wallpaper settings.

### Harmless Log Errors

- `GLFW error 65548: Wayland: The platform does not support setting the window position`: This is a protocol restriction and can be safely ignored.

### Wayland Tweaks

In **Settings > Playback & Perf**, you can find Wayland-specific options:

- **Pause Only When Active**: Only pauses the wallpaper if the _currently focused_ window is fullscreen.
- **Ignore Application IDs**: Prevent specific apps (like docks or bars) from triggering the auto-pause logic.

---

## 6. Log Collection Methods

When reporting a bug, providing logs is essential.

### Using the Log Monitor

1. Go to **Settings > Log Monitor**.
2. Use the **Filter** dropdown to isolate issues:
   - `GUI`: Issues with the interface or Tauri backend.
   - `Engine`: Issues with the `linux-wallpaperengine` process.
   - `Controller`: Issues with wallpaper management logic.
   - `Core`: Internal library errors.
3. Click **Copy** to copy the filtered logs to your clipboard.

### Deep Debugging

If the GUI won't open at all, run it from a terminal to see the `stderr` output:

```bash
# If using the binary
./linux-wallpaperengine-gui

# If running from source
npm run tauri dev
```

Check for any Rust panics or JavaScript errors in the terminal output.

---

## 7. Toast Notification Meanings

The GUI uses toast notifications to provide instant error feedback without needing to check logs.

### Workshop/Assets Path Errors

| Toast Message                     | Reason                                        | Solution                                                                       |
| --------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------ |
| `⚠️ Workshop path does not exist` | Configured Workshop directory is inaccessible | Verify the path or use the Browse button to select the correct `431960` folder |
| `⚠️ Assets path does not exist`   | Configured Assets directory is inaccessible   | Select the correct `wallpaper_engine/assets` folder in Settings                |
| `⚠️ Workshop directory not found` | Path is incorrect or Steam is not installed   | Select the correct Steam Workshop path in Settings                             |

### Wallpaper Scanning Errors

| Toast Message                      | Reason                         | Solution                                     |
| ---------------------------------- | ------------------------------ | -------------------------------------------- |
| `⚠️ No wallpapers found`           | Directory exists but is empty  | Ensure wallpapers are downloaded via Steam   |
| `⚠️ X wallpaper(s) failed to load` | Corrupted `project.json` files | Re-subscribe to or verify integrity in Steam |

### Backend Startup Errors

| Toast Message                          | Reason                       | Solution                                         |
| -------------------------------------- | ---------------------------- | ------------------------------------------------ |
| `❌ Wallpaper engine failed to start`  | Backend process crashed      | Check Settings → Logs for detailed errors        |
| `❌ Failed to start engine: [message]` | Fatal error starting backend | Troubleshoot based on the specific error message |

---

## 8. Engine Log Analysis

### Screenshot Slow (5-10 seconds)

- **Symptom**: Screenshot takes several seconds to complete.
- **Reason**: If `xvfb` is installed, the app uses **CPU software rendering** for silent 4K screenshots.
- **Benefits**: No window popup; consistent 4K quality regardless of screen resolution.
- **Note**: This is normal behavior; wait patiently.

### `Failed to initialize GLEW: No GLX display`

- **Symptom**:
  1. Wallpaper runs, but some effects (particles, audio waveforms) are invisible
  2. Web wallpaper properties don't apply despite logs showing `Applying override value`
- **Reason**: The backend has a hardcoded dependency on X11's GLX extension. In pure Wayland environments, OpenGL initialization is incomplete.
- **Impact**:
  - **Scene type**: Complex effects fail to render
  - **Web type**: Interactive features are completely paralyzed

### `Cannot find a valid assets folder`

- **Symptom**: Startup fails with assets not found message.
- **Solution**: Ensure Steam Wallpaper Engine is installed, or manually copy the `assets` folder.

---

## 9. Web Wallpaper Specific Errors

### Properties Don't Apply Despite Logs

- **Symptom**: `--set-property` commands show success in logs, but wallpaper remains unchanged.
- **Root Causes**:
  1. **Missing Environment**: GLX display error prevents `ExecuteJavaScript` communication
  2. **Initialization Timing**: Properties injected before `DOMContentLoaded` event
  3. **SSL Errors**: External resources (CDN scripts) failed to load (`handshake failed ... net_error -101`)

### Workaround

Manually edit the wallpaper's `project.json` or HTML source files to change default settings.

---

## 10. Setting Limitations

### `Disable Auto Mute` Ineffective

- **Symptom**: Wallpaper still mutes when other apps play sound.
- **Reason**: Under Wayland, PipeWire/Portal security mechanisms may prevent the backend from detecting global audio streams.

### `Disable Particles` No Visual Change

- **Reason**: If particles already fail to render due to GLX errors, this toggle produces no additional effect.
- **Suggestion**: Test only on X11 or wallpapers with known working particle systems.

### `GLFW error 65548: Wayland: Window position`

- **Meaning**: GLFW attempts to set window coordinates, but Wayland protocol prohibits clients from setting their own positions.
- **Impact**: Usually harmless; may indicate window focus issues in some cases.

---

## 11. Resource Loading Issues

### Particles Loaded But Not Visible

- **Symptom**: Logs show `Particle '...' max particles: ...` but nothing appears on screen.
- **Reasons**:
  1. **Input Lost**: Particle emitters rely on mouse position, but global coordinates (0,0) cannot be obtained under Wayland
  2. **Rendering Layer Error**: Particles rendered beneath background layer

### Assets Folder Not Found

- **Symptom**: `Cannot find a valid assets folder` error on startup.
- **Solution**:
  - Install Steam version of Wallpaper Engine, OR
  - Manually copy the `assets` folder to the same directory as `linux-wallpaperengine`

---

## Reporting Bugs

When submitting a bug report, please include:

1. **System Info**: Output of `uname -a`
2. **Desktop Environment**: GNOME, KDE, Hyprland, etc.
3. **Display Server**: X11 or Wayland
4. **Logs**: From Settings → Logs → Copy
5. **Wallpaper Details**: ID and type (Video/Web/Scene)
6. **Steps to Reproduce**: Detailed steps

Submit to [GitHub Issues](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues).
