<a href="CONFIGURATION.md">English</a> | <strong>中文</strong>

# 配置参考

本文档提供了 LWG (Linux Wallpaper Engine) GUI v2.0.0 中可用配置设置的完整参考。

## 设置参考

### 播放与性能

| 界面标签 | JSON 键 | 类型 | 默认值 | 描述 |
|----------|----------|------|---------|-------------|
| 帧率限制 | `fps` | `number` | `30` | 壁纸渲染的帧率限制 (10–144)。 |
| 缩放模式 | `scaling` | `string` | `"default"` | 壁纸适应屏幕的缩放方式 (`default`, `stretch`, `fit`, `fill`)。 |
| 纹理钳制模式 | `clamping` | `string` | `"clamp"` | 纹理环绕模式 (`clamp`, `border`, `repeat`)。 |
| 禁用视差效果 | `disableParallax` | `boolean` | `false` | 停止鼠标移动产生的视差效果。 |
| 禁用粒子效果 | `disableParticles` | `boolean` | `false` | 关闭雨、火等粒子效果。 |
| 全屏不暂停 | `noFullscreenPause` | `boolean` | `false` | 即使开启全屏应用也保持壁纸播放。 |
| 禁用鼠标交互 | `disableMouse` | `boolean` | `false` | 忽略壁纸上的鼠标点击和交互。 |
| 启用自动轮换 | `cycleEnabled` | `boolean` | `false` | 按设定的时间间隔自动切换壁纸。 |
| 轮换间隔（分钟） | `cycleInterval` | `number` | `15` | 自动切换壁纸之间的时间间隔。 |
| 轮换顺序 | `cycleOrder` | `string` | `"random"` | 壁纸轮换的顺序 (`random`, `id`)。 |
| 仅活动时暂停 | `waylandOnlyActive` | `boolean` | `false` | (仅限 Wayland) 仅在应用处于焦点时暂停壁纸。 |
| 忽略应用 ID 列表 | `waylandIgnoreAppids` | `string` | `""` | (仅限 Wayland) 自动暂停时忽略的应用 ID 列表（逗号分隔）。 |

### 音频与显示

| 界面标签 | JSON 键 | 类型 | 默认值 | 描述 |
|----------|----------|------|---------|-------------|
| 静音音频 | `muteAudio` | `boolean` | `true` | 静音所有音频输出并禁用音频处理。 |
| 主音量 | `volume` | `number` | `0` | 全局音量级别 (0–100)。 |
| 禁用自动静音 | `noAutomute` | `boolean` | `false` | 防止应用在其他应用播放声音时自动静音。 |
| 禁用音频处理 | `noAudioProcessing` | `boolean` | `false` | 禁用频谱分析以节省 CPU 资源。 |
| 应用外观 | `theme` | `string` | `"system"` | 界面主题 (`system`, `dark`, `light`)。 |

### 系统与工具

| 界面标签 | JSON 键 | 类型 | 默认值 | 描述 |
|----------|----------|------|---------|-------------|
| Steam Workshop 路径 | `workshopPath` | `string` | `null` | Steam Workshop 壁纸目录的路径。 |
| Assets 目录 | `assetsPath` | `string` | `null` | 引擎 Assets 目录的路径（如果为空则自动检测）。 |
| 开机自启 | `autostart` | `boolean` | `false` | 系统登录时自动启动应用。 |
| 启动时隐藏 | `startHidden` | `boolean` | `false` | 启动时将应用最小化到系统托盘。 |
| 自动恢复 | `autoRestore` | `boolean` | `false` | 启动时自动恢复上次使用的壁纸。 |
| 目标分辨率 | `screenshotRes` | `string` | `"3840x2160"` | 壁纸截图的分辨率。 |
| 优先使用静默截图 (Xvfb) | `preferXvfb` | `boolean` | `true` | 使用 Xvfb 进行后台截图，无需显示窗口。 |
| 别名管理 | `wallpaperNicknames` | `object` | `{}` | 分配给特定壁纸的自定义名称。 |

### 日志监控

| 界面标签 | JSON 键 | 类型 | 默认值 | 描述 |
|----------|----------|------|---------|-------------|
| 日志过滤器 | `filter` | `string` | `"All"` | 按来源过滤日志 (`All`, `GUI`, `Core`, `Engine`, `Controller`)。 |

## JSON 键映射表

配置文件存储在 `~/.config/linux-wallpaperengine-gui/config.json`。

| 界面标签 | JSON 键 | 类型 | 默认值 |
|----------|----------|------|---------|
| 帧率限制 | `fps` | `number` | `30` |
| 主音量 | `volume` | `number` | `0` |
| 缩放模式 | `scaling` | `string` | `"default"` |
| 静音音频 | `muteAudio` | `boolean` | `true` |
| 全屏不暂停 | `noFullscreenPause` | `boolean` | `false` |
| 禁用鼠标交互 | `disableMouse` | `boolean` | `false` |
| 禁用自动静音 | `noAutomute` | `boolean` | `false` |
| 禁用音频处理 | `noAudioProcessing` | `boolean` | `false` |
| 禁用视差效果 | `disableParallax` | `boolean` | `false` |
| 禁用粒子效果 | `disableParticles` | `boolean` | `false` |
| 纹理钳制模式 | `clamping` | `string` | `"clamp"` |
| 目标分辨率 | `screenshotRes` | `string` | `"3840x2160"` |
| 优先使用静默截图 (Xvfb) | `preferXvfb` | `boolean` | `true` |
| 启用自动轮换 | `cycleEnabled` | `boolean` | `false` |
| 轮换间隔（分钟） | `cycleInterval` | `number` | `15` |
| 轮换顺序 | `cycleOrder` | `string` | `"random"` |
| Assets 目录 | `assetsPath` | `string` | `null` |
| Steam Workshop 路径 | `workshopPath` | `string` | `null` |
| 仅活动时暂停 | `waylandOnlyActive` | `boolean` | `false` |
| 忽略应用 ID 列表 | `waylandIgnoreAppids` | `string` | `""` |
| 紧凑模式 | `compactMode` | `boolean` | `false` |
| 启动时隐藏 | `startHidden` | `boolean` | `false` |
| 自动恢复 | `autoRestore` | `boolean` | `false` |
| 播放列表 | `playlists` | `array` | `[]` |
| 轮换播放列表 ID | `cyclePlaylistId` | `string` | `null` |
| 播放列表侧边栏开启 | `playlistSidebarOpen` | `boolean` | `true` |

---

## 后端参数映射

GUI 设置会转换为 `linux-wallpaperengine` 后端的命令行参数。下表显示了每个 GUI 设置如何映射到后端 CLI：

| GUI 设置 | 后端参数 | 示例 |
|-------------|------------------|---------|
| 帧率限制 | `--fps` | `--fps 30` |
| 缩放模式 | `--scaling` | `--scaling stretch` |
| 静音音频 | `--silent` | `--silent` |
| 主音量 | `--volume` | `--volume 50` |
| 全屏不暂停 | `--no-fullscreen-pause` | `--no-fullscreen-pause` |
| 禁用鼠标交互 | `--disable-mouse` | `--disable-mouse` |
| 纹理钳制模式 | `--clamping` | `--clamping clamp` |
| 禁用视差效果 | `--disable-parallax` | `--disable-parallax` |
| 禁用粒子效果 | `--disable-particles` | `--disable-particles` |
| 禁用自动静音 | `--no-auto-mute` | `--no-auto-mute` |
| 禁用音频处理 | `--no-audio-processing` | `--no-audio-processing` |
| Assets 目录 | `--assets-dir` | `--assets-dir /path/to/assets` |

### 完整命令示例

当您应用壁纸时，GUI 会构造如下命令：

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

### Wayland 专用参数

| GUI 设置 | 后端参数 | 描述 |
|-------------|------------------|-------------|
| 仅活动时暂停 | `--fullscreen-pause-only-active` | 仅当焦点窗口全屏时暂停 |
| 忽略应用 ID 列表 | `--fullscreen-pause-ignore-appid` | 逗号分隔的要忽略的应用 ID（如 `waybar,niri`） |

---

## 系统集成

### 自启动配置

在 **设置 > 系统** 中启用"开机自启"，应用会在登录时自动启动。

**位置**：`~/.config/autostart/linux-wallpaperengine-gui.desktop`

如果启用了"启动时隐藏"，应用会最小化到系统托盘启动。

### 窗口管理器集成

#### 紧凑模式窗口规则

为了在平铺式窗口管理器中获得最佳体验，请为紧凑预览窗口添加浮动规则：

**Niri** (config.kdl)：
```kdl
window-rule {
    match title="Wallpaper Preview"
    open-floating true
}
```

**Hyprland** (hyprland.conf)：
```ini
windowrulev2 = float,title:^(Wallpaper Preview)$
windowrulev2 = size 300 700,title:^(Wallpaper Preview)$
windowrulev2 = center,title:^(Wallpaper Preview)$
```

---

## 性能调优

### 降低 CPU 占用

1. **降低 FPS**：从 30fps 降至 24fps 或更低（设置 > 播放）
2. **禁用粒子效果**：启用"禁用粒子效果"（设置 > 播放）
3. **禁用视差效果**：启用"禁用视差效果"（设置 > 播放）
4. **壁纸类型**：使用 Video 壁纸而非 Scene 或 Web 类型

### 降低内存占用

1. **避免 Web 壁纸**：它们内部使用 Chromium 引擎 (CEF)
2. **启用定时轮换**：定期重启后端以清除内存泄漏（设置 > 播放 > 启用自动轮换）
3. **禁用音频处理**：在设置 > 播放中关闭

### 降低 GPU 占用

1. 降低 FPS
2. 使用更简单的壁纸（Video 优于 Scene）
3. 确保"全屏不暂停"**未勾选**，以便游戏时暂停

---

## 配置文件位置

应用遵循 XDG 基础目录规范：

| 类型 | 路径 | 用途 |
|------|------|---------|
| **配置** | `~/.config/linux-wallpaperengine-gui/` | 主设置 (`config.json`) |
| **状态** | `~/.local/state/linux-wallpaperengine-gui/` | 运行时状态 (`state.json`) |
| **数据** | `~/.local/share/linux-wallpaperengine-gui/` | 持久数据（别名、收藏、播放列表） |
| **缓存** | `~/.cache/linux-wallpaperengine-gui/` | 临时数据（历史、日志） |

### 文件摘要

| 文件 | 位置 | 用途 |
|------|----------|---------|
| `config.json` | `~/.config/linux-wallpaperengine-gui/` | 主设置 |
| `state.json` | `~/.local/state/linux-wallpaperengine-gui/` | 运行时状态（屏幕 → 壁纸映射） |
| `nicknames.json` | `~/.local/share/linux-wallpaperengine-gui/` | 自定义壁纸名称 |
| `favorites.json` | `~/.local/share/linux-wallpaperengine-gui/` | 收藏列表 |
| `playlists.json` | `~/.local/share/linux-wallpaperengine-gui/` | 用户播放列表 |
| `playback_history.json` | `~/.cache/linux-wallpaperengine-gui/` | 最近壁纸历史 |
| `screenshot_history.json` | `~/.cache/linux-wallpaperengine-gui/` | 截图历史 |

---

## 相关文档

- [TROUBLESHOOTING_ZH.md](TROUBLESHOOTING_ZH.md) - 常见问题与解决方案
- [MIGRATION_ZH.md](MIGRATION_ZH.md) - 从 Python 版本迁移指南
- [docs/old/ADVANCED.md](old/ADVANCED.md) - 旧版 Python 文档（仅供参考）
