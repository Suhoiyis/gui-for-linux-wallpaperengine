[中文](TROUBLESHOOTING_ZH.md)

# 🐛 Troubleshooting Guide (Tauri v2.0.0)

This guide helps you resolve common issues with the LWG (Linux Wallpaper Engine) GUI and its backend.

## Common Issues

This section covers the most frequent problems users encounter.

- **Wallpaper not showing**: Ensure `linux-wallpaperengine` is installed and the Assets path is correct.
- **Tray icon missing**: Check if your desktop environment supports AppIndicators (see Tray Icon section).
- **Multi-monitor sync**: Use the Link/Unlink button to control all screens at once.
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
- **Display Detection**: The app uses a fallback chain to detect monitors:
  1. `xrandr` (X11)
  2. `wlr-randr` (Wayland/wlroots)
  3. `kscreen-doctor` (KDE Plasma)
  If your monitors aren't showing up, ensure the appropriate tool for your environment is installed.

### Path Configuration
- **Workshop Path**: Must point to the Steam Workshop folder (usually ending in `431960`).
- **Assets Path**: Must point to the `assets` folder of `linux-wallpaperengine`.
- **Fix**: Go to **Settings > System & Tools** to verify and update these paths.

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
- **Link/Unlink**: Use the 🔗 icon to toggle between "Same wallpaper on all screens" and "Different wallpapers per screen".

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
- **Pause Only When Active**: Only pauses the wallpaper if the *currently focused* window is fullscreen.
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
