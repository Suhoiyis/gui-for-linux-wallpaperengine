# 高级指南
[English](ADVANCED.md)

本文档详细介绍了 Linux Wallpaper Engine GUI 中提供的高级功能和配置选项。

## 目录

- [命令行参数](#command-line-arguments)
- [配置参考](#configuration-reference)
- [后端参数映射](#backend-parameter-mapping)
- [系统集成](#system-integration)
- [播放历史系统](#playback-history-system)
- [别名管理](#nickname-management)
- [紧凑预览模式](#compact-preview-mode)
- [Wayland 高级调整](#wayland-advanced-tweaks)
- [截图功能详情](#screenshot-feature-details)
- [定时轮换](#timed-rotation)
- [多显示器配置](#multi-monitor-configuration)
- [日志系统](#log-system)
- [故障排除](#troubleshooting)
- [性能调优](#performance-tuning)

---

## 命令行参数 <a name="command-line-arguments"></a>

### 启动模式

```bash
# 在前台启动（默认）
python3 run_gui.py

# 在后台启动（仅托盘图标）
python3 run_gui.py --hidden
python3 run_gui.py --minimized  # --hidden 的别名
```

### 窗口控制

所有后续命令都将发送到已运行的实例（单实例架构）：

```bash
# 显示窗口
python3 run_gui.py --show

# 隐藏窗口（进程继续运行）
python3 run_gui.py --hide

# 切换显示/隐藏状态
python3 run_gui.py --toggle
```

### 壁纸控制

```bash
# 应用上次使用的壁纸
python3 run_gui.py --apply-last

# 随机切换壁纸
python3 run_gui.py --random

# 停止当前壁纸
python3 run_gui.py --stop

# 重新扫描壁纸库
python3 run_gui.py --refresh
```

### 退出程序

```bash
# 完全退出（关闭 GUI 和所有壁纸进程）
python3 run_gui.py --quit
```

---

## 配置参考 <a name="configuration-reference"></a>

**位置**: `~/.config/linux-wallpaperengine-gui/config.json`

### 完整配置示例

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

### 配置字段

#### 常规设置

| 字段 | 类型 | 默认值 | 描述 |
|------|------|---------|-------------|
| `workshopPath` | string | 自动检测 | Steam Workshop 壁纸目录路径 |
| `assetsPath` | string | null | Wallpaper Engine 资源文件夹路径 (null = 自动检测) |
| `fps` | int | 30 | 帧率限制 (1–144) |
| `volume` | int | 50 | 音量 (0–100) |
| `scaling` | string | "default" | 缩放模式: `default`, `stretch`, `fit`, `fill` |
| `silence` | bool | true | 静音 |

#### 高级渲染

| 字段 | 类型 | 默认值 | 描述 |
|------|------|---------|-------------|
| `clamping` | string | "default" | 纹理钳制模式: `default`, `clamp`, `border` |
| `disableParallax` | bool | false | 禁用视差效果 |
| `disableParticles` | bool | false | 禁用粒子系统 |

#### 音频控制

| 字段 | 类型 | 默认值 | 描述 |
|------|------|---------|-------------|
| `disableAutoMute` | bool | false | 禁用窗口全屏时自动静音 |
| `disableAudioProcessing` | bool | false | 禁用音频处理逻辑 |

#### 性能优化

| 字段 | 类型 | 默认值 | 描述 |
|------|------|---------|-------------|
| `noFullscreenPause` | bool | false | 窗口全屏时不暂停壁纸 |
| `disableMouse` | bool | false | 禁用鼠标交互 |

#### 自动化

| 字段 | 类型 | 默认值 | 描述 |
|------|------|---------|-------------|
| `autoStartEnabled` | bool | false | 启用登录时开机自启 |
| `silentStart` | bool | false | 静默启动（后台模式） |
| `autoRotateEnabled` | bool | false | 启用定时轮换壁纸 |
| `rotateInterval` | int | 30 | 轮换间隔（分钟） |
| `cycleOrder` | string | "random" | 轮换顺序: `random`, `title`, `size`, `type`, `id` |

#### 截图配置

| 字段 | 类型 | 默认值 | 描述 |
|------|------|---------|-------------|
| `screenshotDelay` | int | 10 | 捕获前的等待时间（秒） |
| `screenshotWidth` | int | 3840 | 截图宽度 |
| `screenshotHeight` | int | 2160 | 截图高度 |
| `useXvfb` | bool | true | 使用 Xvfb 进行静默截图 |

#### 状态持久化

| 字段 | 类型 | 描述 |
|------|------|-------------|
| `lastWallpaper` | string | 上次应用的壁纸 ID |
| `lastScreen` | string | 上次选择的屏幕名称 |
| `activeWallpapers` | object | 每个屏幕当前壁纸的映射 |
| `wallpaperProperties` | object | 每个壁纸的自定义属性 |

---

## 后端参数映射 <a name="backend-parameter-mapping"></a>

GUI 配置被转换为 `linux-wallpaperengine` 后端的命令行参数：

| GUI 设置 | 后端参数 | 描述 |
|-------------|------------------|-------------|
| `fps: 30` | `--fps 30` | 帧率限制 |
| `scaling: "stretch"` | `--scaling stretch` | 拉伸缩放 |
| `silence: true` | `--silent` | 静音 |
| `volume: 50` | `--volume 50` | 音量 |
| `noFullscreenPause: true` | `--no-fullscreen-pause` | 禁用全屏暂停 |
| `disableMouse: true` | `--disable-mouse` | 禁用鼠标交互 |
| `clamping: "clamp"` | `--clamping clamp` | 纹理钳制 |
| `disableParallax: true` | `--disable-parallax` | 禁用视差 |
| `disableParticles: true` | `--disable-particles` | 禁用粒子 |
| `disableAutoMute: true` | `--no-auto-mute` | 禁用自动静音 |
| `disableAudioProcessing: true` | `--no-audio-processing` | 禁用音频处理 |
| `assetsPath: "/path/to/assets"` | `--assets-dir /path/to/assets` | 自定义资源目录 |

### 完整命令示例

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

## 系统集成 <a name="system-integration"></a>

### 生成桌面快捷方式

点击 **设置 > 常规** 中的“创建桌面快捷方式”按钮将生成：

**文件位置**: `~/.local/share/applications/linux-wallpaperengine-gui.desktop`

**示例内容**:
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

### 配置开机自启

点击“启用开机自启”按钮将生成：

**文件位置**: `~/.config/autostart/linux-wallpaperengine-gui.desktop`

如果启用了“静默启动”，`Exec` 行将变为：
```
Exec=/usr/bin/python3 /home/user/suw/run_gui.py --hidden
```

### 窗口管理器集成

#### 紧凑模式窗口规则 <a name="compact-mode-window-rules"></a>

由于 Wayland 协议限制，应用程序无法在平铺窗口管理器（如 Niri 或 Hyprland）中强制窗口尺寸。为了获得最佳体验（浮动模式），请将以下规则添加到您的 WM 配置中：

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

#### Niri (启动与绑定)

```kdl
spawn-at-startup "python3" "/home/user/suw/run_gui.py" "--hidden"

binds {
    Mod+W { spawn "python3" "/home/user/suw/run_gui.py" "--toggle"; }
    Mod+Shift+W { spawn "python3" "/home/user/suw/run_gui.py" "--random"; }
}
```

#### i3wm (配置)

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

## 播放历史系统 <a name="playback-history-system"></a>

在 v0.10.3-beta 中引入，播放历史系统跟踪您最近使用的壁纸以便快速访问。

- **容量**: 最多存储 30 条记录。具有自动去重功能；重新应用已在历史记录中的壁纸会将其移至顶部。
- **访问**: 通过 **汉堡菜单 (☰) → 播放历史** 打开。
- **详情**: 每个条目显示缩略图、壁纸的别名（*斜体*）、原始 ID 和时间戳（格式为 `MM-DD HH:MM`）。
- **一键重播**: 点击条目立即同步主窗口状态并应用壁纸。
- **管理**: 包括一个“清除”按钮以清空历史记录，以及一个容量计数器（例如 `12 / 30`）。

---

## 别名管理 <a name="nickname-management"></a>

别名系统 (v0.10.2) 允许您为壁纸分配易记的名称，使您的库更易于导航。

- **存储**: 别名通过 `NicknameManager` 持久化在 `nicknames.json` 中。
- **设置别名**: 右键单击网格中的任何壁纸并选择“设置别名”，或使用侧边栏中的 ✏️ 按钮。
- **批量管理**: 访问 **设置** 中的 **管理别名** 对话框，在单个网格视图中查看、编辑或删除所有别名。
- **搜索集成**: 全局搜索栏同时匹配自定义别名和原始壁纸标题。
- **视觉效果**:
    - **网格视图**: 别名以 **_斜体加粗_** 显示。
    - **侧边栏**: 显示“别名 + 原始标题”（后者为灰色小字）。

---

## 紧凑预览模式 <a name="compact-preview-mode"></a>

紧凑预览模式 (v0.10.0) 专为平铺窗口管理器（Niri, Hyprland, Sway）设计，提供轻量级的独立界面。

- **行为**: 作为一个单独的窗口运行，与主应用程序窗口互斥。
- **尺寸**: 默认大小为 300×700。
- **布局**:
    - **顶部**: 带有 GIF 动画支持的大型壁纸预览。
    - **底部**: 5 个圆形缩略图，支持平滑循环导航。
- **导航**: 支持键盘快捷键（`←` 和 `→`）和屏幕上的导航按钮。
- **信息**: 显示带有壁纸 ID 的蓝色胶囊（点击复制）、标题、大小和索引。
- **WM 规则**: 强烈建议在您的 WM 配置中将此窗口设置为“浮动”（参见 [系统集成](#compact-mode-window-rules)）。

---

## Wayland 高级调整 <a name="wayland-advanced-tweaks"></a>

针对 Wayland 会话 (v0.8.10) 的细粒度控制，以处理特定于合成器的行为。

- **自动检测**: GUI 会自动检测您是否正在运行 Wayland 会话。
- **仅活动时暂停**: (`--fullscreen-pause-only-active`) 仅当当前聚焦的窗口全屏时才暂停壁纸。这可以防止后台全屏窗口停止您的壁纸。
- **忽略应用列表**: (`--fullscreen-pause-ignore-appid`) 以逗号分隔的 App ID 列表（例如 `waybar,niri`），全屏检测逻辑应忽略这些 ID。
- **使用场景**: 防止桌面组件（如 dock、状态栏或面板）意外触发壁纸暂停机制。

---

## 截图功能详情 <a name="screenshot-feature-details"></a>

### 工作原理

1. **Xvfb 检测**: 检查系统上是否安装了 `xvfb-run`。
2. **模式选择**:
   - **有 Xvfb**: 静默模式（使用虚拟 X 服务器）。
   - **无 Xvfb**: 窗口模式（短暂打开一个物理窗口）。
3. **渲染**: 使用 `--screenshot` 参数启动后端。
4. **智能延迟**:
   - **视频壁纸**: 5 秒（快速采样第一帧）。
   - **网页/场景壁纸**: 使用用户配置的延迟。
5. **存储**: 截图保存到 `~/Pictures/wallpaperengine/`。

### 配置

可在 **设置 > 高级** 中找到：

- **截图延迟**: 捕获前的等待时间。建议：视频 5 秒，网页/场景 10-15 秒。
- **截图分辨率**: 默认 3840x2160 (4K)。这确保了高质量并避免了平铺 WM 中的裁剪问题。
- **使用 Xvfb 进行截图**: 在后台静默捕获和物理窗口模式之间切换。

### 资源使用统计

自 v0.10.5 起，截图过程包括高级资源监控：
- **高频采样**: 捕获期间监控频率增加到 0.1s，以捕捉短时任务。
- **混合计算**: 对于超快任务（如视频截图），它切换到 CPU 时间增量计算以确保准确性。
- **归一化**: CPU 使用率在所有核心上归一化（0-100% 总系统负载），并带有峰值过滤。

### 安装

```bash
# Arch Linux
sudo pacman -S xorg-server-xvfb

# Ubuntu/Debian
sudo apt install xvfb
```

---

## 定时轮换 <a name="timed-rotation"></a>

### 启用轮换

在 **设置 > 自动化** 中：
1. 勾选 **启用定时轮换**。
2. 设置 **轮换间隔**（分钟）。
3. 选择 **轮换顺序**。
4. 点击 **保存设置**。

### 轮换顺序选项

在 v0.8.11 中引入，您可以选择壁纸的选择方式：
- **随机**: 从库中随机选择一张壁纸。
- **标题 (A-Z)**: 按标题字母顺序循环。
- **大小 (↓/↑)**: 按文件大小循环。
- **类型**: 按壁纸类型（视频、网页、场景）循环。
- **ID**: 按 Steam Workshop ID 循环。

**配置键**: `cycleOrder`

### 机制

- 使用 `GLib.timeout_add_seconds` 定时器。
- 支持多显示器设置（所有屏幕同时轮换）。
- 即使 GUI 窗口隐藏，也会继续运行。
- 手动应用壁纸会重置定时器。

---

## 多显示器配置 <a name="multi-monitor-configuration"></a>

### 屏幕检测

GUI 使用以下方式自动检测显示器：
1. **X11**: `xrandr --listmonitors`
2. **Wayland**: `wlr-randr`（如果可用）
3. **回退**: 允许手动输入屏幕名称。

### 独立壁纸

1. 从顶部栏的下拉菜单中选择目标显示器。
2. 浏览并应用壁纸。
3. 对其他显示器重复此操作。

### 配置映射

```json
{
  "activeWallpapers": {
    "eDP-1": "1234567890",   // 笔记本内置屏幕
    "HDMI-1": "9876543210",  // 外接显示器
    "DP-1": "1122334455"     // 第二个外接显示器
  }
}
```

### 已知问题

- 断开连接的屏幕需要手动清理（GUI 在启动时会进行清理）。
- 混合刷新率可能会导致 FPS 不一致。
- 缩放可能会在旋转的屏幕上表现异常。

---

## 日志系统 <a name="log-system"></a>

### 日志来源

- **控制器**: GUI 控制逻辑和进程管理。
- **引擎**: 来自 `linux-wallpaperengine` 后端的输出。
- **GUI**: GTK 界面事件和用户交互。

### 日志级别

- **DEBUG**: 详细的调试信息（灰色）。
- **INFO**: 一般信息（白色）。
- **WARNING**: 警告（黄色）。
- **ERROR**: 错误（红色）。

### 文件位置

- **GUI 日志**: `~/.config/linux-wallpaperengine-gui/app.log`
- **引擎日志**: `~/.config/linux-wallpaperengine-gui/engine_<wallpaper_id>.log`

### 查看日志

**在 GUI 中**:
- 转到 **设置 > 日志**。
- 日志会自动刷新（或点击 **刷新**）。

**通过终端**:
```bash
# 跟踪 GUI 日志
tail -f ~/.config/linux-wallpaperengine-gui/app.log

# 跟踪引擎日志
tail -f ~/.config/linux-wallpaperengine-gui/engine_*.log
```

---

## 故障排除 <a name="troubleshooting"></a>

### 壁纸应用失败

**症状**: 点击应用没有任何反应，或者壁纸立即消失。

**步骤**:
1. 检查 **设置 > 日志** 中的错误。
2. 验证 `linux-wallpaperengine` 是否在您的 PATH 中：`which linux-wallpaperengine`。
3. 尝试手动运行后端：
   ```bash
   linux-wallpaperengine --screen-root eDP-1 /path/to/wallpaper
   ```
4. 确保壁纸文件夹包含有效的 `project.json`。

### 截图失败

**症状**: 点击截图按钮后没有输出文件或错误消息。

**步骤**:
1. 检查目录是否可写：`ls -ld ~/Pictures/wallpaperengine`。
2. 如果使用 Xvfb，验证安装：`which xvfb-run`。
3. 尝试在 **设置 > 高级** 中禁用 Xvfb 模式。
4. 将 **截图延迟** 增加到 10 秒或更长。

### 系统托盘图标缺失

**症状**: 启动后托盘区域没有出现图标。

**步骤**:
1. 验证是否安装了 `libayatana-appindicator`。
2. 检查您的环境是否支持托盘：
   - **GNOME**: 需要 "AppIndicator Support" 扩展。
   - **Waybar**: 确保启用了 `tray` 模块。
   - **i3/Sway**: 可能需要 `waybar` 或类似的状态栏。

---

## 性能调优 <a name="performance-tuning"></a>

### 降低 CPU 使用率

1. **降低 FPS**: 在 **设置 > 常规** 中从 30fps 降低到 24fps 或更低。
2. **禁用粒子**: 在 **设置 > 高级** 中启用“禁用粒子系统”。
3. **禁用视差**: 在 **设置 > 高级** 中启用“禁用视差效果”。
4. **壁纸类型**: 使用 **视频** 壁纸而不是场景或网页类型。

### 降低内存使用率

1. **避免网页壁纸**: 它们使用内部 Chromium 引擎 (CEF)。
2. **启用定时轮换**: 定期重启后端以清除内存泄漏。
3. **禁用音频处理**: 在 **设置 > 音频** 中关闭。

### 降低 GPU 使用率

1. 降低 FPS。
2. 使用更简单的壁纸。
3. **全屏时暂停**: 确保 **未勾选**“窗口全屏时不暂停壁纸”。

---

## 获取帮助

如果您无法解决问题：

1. 查阅 [docs/COMPATIBILITY.md](COMPATIBILITY.md)。
2. 搜索 [GitHub Issues](https://github.com/your-repo/issues)。
3. 提交一个新的 Issue，并包含：
   - 系统信息 (`uname -a`)
   - 桌面环境
   - 完整日志 (**设置 > 日志 > 复制日志**)
   - 壁纸 ID 和类型
