# Wallpaper Compatibility Guide
[中文](ADVANCED_ZH.md)

This document details the compatibility and limitations of Linux Wallpaper Engine GUI in different environments.

## Backend Architecture

This GUI relies on the `linux-wallpaperengine` C++ backend for rendering. This backend is implemented through reverse engineering (not an official port), and since the Linux graphics stack (especially Wayland) differs fundamentally from Windows, some wallpapers may not display perfectly.

## Wallpaper Type Compatibility

### ✅ Video Wallpapers (.mp4, .webm)

**Compatibility**: Fully supported

**Notes**:
- Video decoding uses mature FFmpeg/GStreamer libraries
- Supports loop playback and volume control
- Optimal performance with lowest resource usage
- **Recommended to prioritize Video type wallpapers**

**Test Environment**:
- ✅ X11 (GNOME/KDE)
- ✅ Wayland (Niri/Sway/Hyprland)

---

### ⚠️ Web Wallpapers (.html)

**Compatibility**: Partial support

**Available Features**:
- ✅ Basic rendering: Displays web content and animations
- ✅ JavaScript execution: Dynamic effects run normally
- ✅ Audio playback: Background music plays (subject to volume control)

**Known Issues**:
- ❌ **Property adjustments are non-functional**: Due to CEF (Chromium Embedded Framework) communication limitations in the C++ backend under Linux/Wayland, **Web wallpaper properties cannot be dynamically adjusted via GUI/CLI**.
  - Examples: Language switching, music toggle, color selection, real-time value changes, etc.
  - Most properties adjustable in the Windows version are effectively non-functional on Linux.
  - Wallpapers will run with their default property values.

**Technical Reasons**:
- CEF's IPC (Inter-Process Communication) implementation differs between Linux and Windows.
- The backend's attempts to inject JavaScript to modify `window.wallpaperPropertyListener` often fail silently due to environment mismatches or timing issues.
- Wayland's security isolation mechanisms further restrict cross-process communication.

**Solutions**:
- To modify Web wallpaper properties, try manually editing the wallpaper's `project.json` or HTML source files (requires some technical skill).
- Prioritize Web wallpapers with few properties or those whose default configuration meets your needs.

---

### ⚠️ Scene Wallpapers (.pkg)

**Compatibility**: Limited support

**Available Features**:
- ✅ Simple 2D/3D scenes: Basic models, textures, lighting
- ✅ Basic animation: Timeline animations, camera movement
- ⚠️ Basic particle systems: Simple particles may work correctly

**Known Issues**:
- ❌ **Complex particle systems fail**: Wallpapers with advanced particle effects may only display static scenes.
  - Symptom: Logs show `Particle system loaded` but no particles are visible on screen.
  - Reason: Particle systems rely on Windows-specific DirectX APIs; OpenGL translation may be incomplete.
  
- ❌ **Custom shaders fail or glitch**: Wallpapers using HLSL (DirectX shader language) may experience:
  - Missing effects
  - Screen tearing or visual glitches
  - Complete failure to render (black screen)
  - Reason: Automatic HLSL to GLSL translation does not fully support all syntax features.

- ❌ **Complex script logic**: Interactive scripts relying on Windows-specific APIs cannot be executed.

**Recommended Practices**:
- Check Workshop comments for feedback from Linux users before downloading.
- Prioritize Scene wallpapers labeled as "simple" or "low-end".
- Avoid wallpapers whose descriptions mention heavy particle effects or advanced shaders.

---

## Wayland Environment Special Notes

If you are using a Wayland compositor (Niri/Hyprland/Sway/GNOME Wayland), please note the following limitations:

### ❌ Mouse Interaction Fully Disabled

**Problem**:
- Mouse Trails effects cannot be displayed.
- Click interactions (e.g., clicking to switch scenes, dragging objects) do not respond.

**Reason**:
- Wayland's security isolation requires an application to have focus to read mouse positions.
- Applications running as a Background Layer typically cannot obtain global mouse coordinates.
- Even in windowed mode, some interactive scripts relying on Windows-specific APIs (`GetCursorPos`) will not work.

**No Solution**: This is an architectural limitation.

---

### ⚠️ OpenGL/GLX Compatibility Issues

**Symptoms**:
- Logs show `Failed to initialize GLEW: No GLX display`.
- Rendering layers for some effects are abnormal (e.g., particles appearing behind models).
- Web property injection is more likely to fail.

**Reason**:
- Some legacy effects rely on GLX (OpenGL Extension for X11).
- Pure Wayland environments lack GLX, providing only EGL.

**Solution**:
- Ensure `xorg-xwayland` is installed (default on most distributions).
- Try adding an environment variable in the startup parameters (experimental):
  ```bash
  GDK_BACKEND=x11 python3 run_gui.py
  ```

---

### ❌ Web Interaction Communication Restricted

**Problem**:
- Property injection success rate for Web wallpapers is lower.
- CEF rendering occasionally shows black screens or flickering.

**Reason**:
- CEF support for Wayland is still maturing (relying on the Ozone layer).
- Timing issues in cross-process communication are more severe under Wayland.

**Mitigation**:
- In Settings > Advanced, uncheck "Disable Mouse Interaction" (while interaction still won't work, retaining mouse support may improve CEF stability).
- Use Video wallpapers instead of Web wallpapers.

---

## X11 Environment Compatibility

**Overall**: X11 compatibility is generally superior to Wayland.

**Known Issues**:
- ⚠️ Some desktop environments (e.g., XFCE/LXDE) may fail to set the wallpaper layer correctly.
- ⚠️ Tearing may occur when using compositors like Compton/Picom.

**Recommended Desktop Environments**:
- ✅ GNOME (X11)
- ✅ KDE Plasma (X11)
- ⚠️ i3/bspwm (requires manual window rule configuration)

---

## Hardware Compatibility

### GPU Requirements

**Minimum**:
- Graphics card supporting OpenGL 3.3
- Integrated graphics (Intel HD 4000+) can run simple wallpapers

**Recommended**:
- Dedicated graphics card (NVIDIA/AMD)
- OpenGL 4.5+ support

### Driver Issues

**NVIDIA**:
- ✅ Proprietary drivers (Recommended): Best compatibility
- ⚠️ Nouveau open-source drivers: Poor performance, complex scenes may lag

**AMD**:
- ✅ AMDGPU drivers (Mesa): Good support for modern cards
- ⚠️ Older cards may lack some OpenGL extensions

**Intel**:
- ✅ Mesa drivers: Integrated graphics support basic functionality
- ⚠️ Complex Scene wallpapers may lack sufficient performance

---

## Multi-Monitor Compatibility

**Current Status**: Beta support

**Known Issues**:
- ⚠️ Wallpapers on disconnected screens must be stopped manually (GUI will clean up configuration automatically).
- ⚠️ Monitors with different refresh rates may cause inconsistent FPS.
- ⚠️ Wallpaper scaling may be abnormal on rotated (portrait) screens.

---

## Performance and Memory

### Expected Resource Usage

| Wallpaper Type | Memory Usage | CPU Usage (30fps) | GPU Usage |
|---------|---------|-----------------|---------|
| Video (1080p) | ~100MB | 5-10% | Low |
| Web (Simple) | ~200MB | 10-20% | Low-Medium |
| Scene (Simple) | ~150MB | 10-15% | Medium |
| Scene (Complex) | ~300MB | 20-40% | High |

### Known Memory Leaks

**Symptoms**:
- Long-running (8+ hours) Web wallpapers may cause slow memory growth.
- Usage may eventually reach 500MB - 1GB.

**Reason**:
- Likely stems from CEF (Chromium engine) memory management issues.
- Could also be leaks in the C++ backend or Python bindings.

**Temporary Solutions**:
- Enable "Timed Rotation" in Settings > Automation to force periodic backend restarts.
- Use system crontab to periodically execute `python3 run_gui.py --stop && python3 run_gui.py --apply-last`.
- Avoid long-term use of complex Web wallpapers.

---

## Test Environment

This project is primarily developed and tested in the following environment:

**Primary Test Environment**:
- Distribution: Arch Linux
- Window Manager: Niri (Wayland)
- GPU: Intel Iris Xe

**Limited Testing**:
- GNOME (Wayland/X11) ~Planned~

**Untested**:
- Ubuntu/Debian systems
- Other Wayland compositors (e.g., River/Labwc)
- Other desktop environments (e.g., XFCE/Cinnamon)

If you encounter issues in other environments, please submit an Issue with detailed environment information.

---

## Light/Dark Theme Adaptive Support (v0.10.5)

Starting from v0.10.5, the application now seamlessly adapts to both light and dark system themes using GTK named colors. This eliminates the previous "dark mode only" limitation, ensuring all text, buttons, and UI elements remain perfectly readable regardless of your system theme settings.

---

## Getting Help

If you encounter compatibility issues, please provide the following information:

1. Distribution and version (`cat /etc/os-release`)
2. Desktop environment / Window manager
3. Display server (X11/Wayland)
4. GPU and driver version (`glxinfo | grep OpenGL`)
5. Wallpaper ID and type
6. Log output (Settings > Logs page)

Submit issues on the GitHub Issues page: [https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues)
