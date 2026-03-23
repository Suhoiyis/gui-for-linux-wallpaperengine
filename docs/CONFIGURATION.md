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
