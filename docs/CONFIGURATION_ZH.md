[English](CONFIGURATION.md)

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
