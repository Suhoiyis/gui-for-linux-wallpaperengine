# 🐛 Common Errors & Troubleshooting

[中文](TROUBLESHOOTING_ZH.md)

This document records common errors and their meanings for both the GUI and the `linux-wallpaperengine` backend.

## 1. GUI User Prompts

### ⚠️ Toast Notifications
The GUI now uses Toast notifications to provide instant error feedback without needing to check logs:

#### Workshop/Assets Path Related
- **`⚠️ Workshop path does not exist: /path/to/dir`**
  - **Reason**: The configured Workshop directory does not exist or is inaccessible.
  - **Solution**: Check if the path is correct, or use the Browse button to select the correct `431960` folder.

- **`⚠️ Assets path does not exist: /path/to/assets`**
  - **Reason**: The configured Assets directory does not exist or is inaccessible.
  - **Solution**: Check if the path is correct, or use the Browse button to select the `wallpaper_engine/assets` folder.

#### Wallpaper Scanning Related
- **`⚠️ Workshop directory not found: /path/to/workshop`**
  - **Reason**: The Workshop directory path is incorrect or Steam is not installed.
  - **Solution**: Select the correct Steam Workshop path in Settings.

- **`⚠️ No wallpapers found in: /path/to/workshop`**
  - **Reason**: The directory exists but is empty, or contains no valid wallpaper folders.
  - **Solution**: Ensure wallpapers have been downloaded via Steam, or check if the correct Workshop path is selected.

- **`⚠️ X wallpaper(s) failed to load`**
  - **Reason**: The `project.json` files for some wallpapers are corrupted or incorrectly formatted.
  - **Solution**: Re-subscribe to or verify the integrity of these wallpapers in Steam.

#### Backend Startup Related
- **`❌ Wallpaper engine failed to start - check logs`**
  - **Reason**: The `linux-wallpaperengine` backend failed to start.
  - **Solution**: Check the Settings > Logs page for detailed error information.

- **`❌ Failed to start engine: [error message]`**
  - **Reason**: A fatal error occurred while starting the backend process.
  - **Solution**: Troubleshoot based on the specific error message.

### Viewing Detailed Logs
When a Toast notification mentions "check logs":

1. **Open the Logs page**: Settings → Logs
2. **Check for the latest errors**: Look for red `ERROR` entries.
3. **Common log errors**:
   - `Cannot find a valid assets folder` → Assets path configuration error.
   - `Failed to initialize GLEW` → OpenGL/GLX environment issues.
   - `Permission denied` → Insufficient file permissions.
   - `Process exited immediately` → Backend failed to start; check detailed output.

---

## 2. Backend Log Analysis

### Screenshot speed is slow (5-10 seconds)
- **Symptom**: After clicking screenshot, it takes several seconds for the success notification to appear.
- **Reason**: If `xvfb` is installed on the system, the program uses **CPU software rendering** to generate 4K screenshots. While slower, this method ensures:
  1. **No window pop-up**: Completely silent, does not interrupt your work.
  2. **Perfect 4K**: Not limited by physical screen resolution or tiling window manager layouts.
- **Suggestion**: This is normal behavior; please wait patiently.

### `Failed to initialize GLEW: No GLX display`
- **Symptom**:
  1. The wallpaper runs, but some effects (e.g., particles, audio waveforms) are invisible.
  2. **Web wallpaper properties fail**: After setting properties via GUI or CLI (e.g., `language=chinese`), logs show `Applying override value`, but the visuals remain unchanged.
- **Reason**: The backend has a hardcoded dependency on X11's GLX extension. In pure Wayland environments, the OpenGL environment initialization is incomplete, causing Chromium's (CEF) JavaScript injection interface (used for modifying web properties) to fail silently.
- **Impact**:
  - **Scene type**: Complex effects fail to render.
  - **Web type**: **Interactive features are completely paralyzed**, making it impossible to dynamically adjust any wallpaper properties.

---

## 3. Web Wallpaper Specific Errors

### Logs show `Applying override value` but the interface doesn't change
- **Symptom**: Running `linux-wallpaperengine <ID> --set-property key=value` in a terminal shows successful application logs, but the wallpaper remains in its default state.
- **Root Causes**:
  1. **Missing Environment**: Refer to the `GLX display` error above; an abnormal rendering context prevents the backend from communicating with the webpage via `ExecuteJavaScript`.
  2. **Initialization Timing**: Some wallpapers register property listeners in the `DOMContentLoaded` event, while the backend injects properties too early, causing the commands to be lost before the page is ready.
  3. **SSL Errors**: If `handshake failed ... net_error -101` appears in the logs, it means external resources (like CDN scripts) failed to load, which might block the initialization of property listeners.

---

## 4. Setting Environment Limitations

### `Disable Auto Mute` is ineffective
- **Symptom**: When enabled, the wallpaper still mutes when other apps play sound, or the feature doesn't work at all.
- **Reason**: Under Wayland, restricted by PipeWire/Portal security mechanisms, the backend process may be unable to detect the state of global audio streams.

### `Disable Particles` shows no visual change
- **Reason**: If the wallpaper already fails to render the particle system due to a `GLX display` error, this toggle will not produce any additional visual difference.
- **Suggestion**: Only test on X11 environments or wallpapers where particle systems are known to display correctly.

### `Disable Parallax` (To be verified)
- **Status**: **Not yet fully tested on Scene wallpapers with 3D effects.**
- **Expected Behavior**: This toggle should stop the parallax swaying effect of the background as the mouse moves.

### Role of `Clamping Mode`
- Used to resolve edge stretching issues in non-standard resolutions. If the wallpaper displays normally, it is recommended to keep the default `clamp` value.

### `GLFW error 65548: Wayland: The platform does not support setting the window position`
- **Symptom**: This error appears in the logs.
- **Reason**: GLFW attempts to force window coordinates under Wayland, but the Wayland protocol prohibits clients from setting their own positions (managed by the compositor).
- **Impact**: Usually harmless, but in some cases, it may suggest the window failed to correctly fullscreen or gain input focus.

---

## 5. Resource Loading Issues

### `Particle '...' max particles: ...` but nothing on screen
- **Symptom**: Logs show the particle system is loaded (e.g., `Particle 'Getsuga Tenshou Mouse Trail'...`) and textures are found, but nothing appears on screen.
- **Reason**:
  1. **Input Lost**: Particle emitters rely on mouse position, but global mouse coordinates (0,0) cannot be obtained under Wayland, so particles are never emitted.
  2. **Rendering Layer Error**: Particles are rendered beneath the background layer (Z-fighting or blending mode error).

### `Cannot find a valid assets folder`
- **Symptom**: Startup fails with a message saying assets cannot be found.
- **Solution**: Ensure you have installed the Steam version of Wallpaper Engine, or manually copy the `assets` folder to the same directory as `linux-wallpaperengine`.
