# 高级功能文档

本文档介绍 Linux Wallpaper Engine GUI 的高级功能和配置选项。

## 目录

- [命令行参数](#命令行参数)
- [配置文件详解](#配置文件详解)
- [后端参数映射](#后端参数映射)
- [系统集成](#系统集成)
- [截图功能详解](#截图功能详解)
- [定时轮换功能](#定时轮换功能)
- [多显示器配置](#多显示器配置)
- [日志系统](#日志系统)
- [故障排查](#故障排查)

---

## 命令行参数

### 启动模式

```bash
# 前台启动（默认）
python3 run_gui.py

# 后台启动（无窗口）
python3 run_gui.py --hidden
python3 run_gui.py --minimized  # 同上
```

### 窗口控制

所有以下命令会发送到已运行的实例（单实例模式）：

```bash
# 显示窗口
python3 run_gui.py --show

# 隐藏窗口（保持进程）
python3 run_gui.py --hide

# 切换显示/隐藏状态
python3 run_gui.py --toggle
```

### 壁纸控制

```bash
# 应用上次壁纸
python3 run_gui.py --apply-last

# 随机切换壁纸
python3 run_gui.py --random

# 停止当前壁纸
python3 run_gui.py --stop

# 刷新壁纸库
python3 run_gui.py --refresh
```

### 退出程序

```bash
# 完全退出（关闭 GUI 和所有壁纸进程）
python3 run_gui.py --quit
```

---

## 配置文件详解

配置文件位置：`~/.config/linux-wallpaperengine-gui/config.json`

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

### 配置字段说明

#### 基础设置

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `workshopPath` | string | 自动检测 | Steam Workshop 壁纸目录路径 |
| `assetsPath` | string | null | Wallpaper Engine assets 文件夹路径（null = 自动检测） |
| `fps` | int | 30 | 帧率限制（1-144） |
| `volume` | int | 50 | 音量（0-100） |
| `scaling` | string | "default" | 缩放模式：`default`/`stretch`/`fit`/`fill` |
| `silence` | bool | true | 是否静音 |

#### 高级渲染

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `clamping` | string | "default" | 纹理钳制模式：`default`/`clamp`/`border` |
| `disableParallax` | bool | false | 禁用视差效果 |
| `disableParticles` | bool | false | 禁用粒子系统 |

#### 音频控制

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `disableAutoMute` | bool | false | 禁用自动静音（全屏时） |
| `disableAudioProcessing` | bool | false | 禁用音频处理逻辑 |

#### 性能优化

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `noFullscreenPause` | bool | false | 全屏时不暂停壁纸 |
| `disableMouse` | bool | false | 禁用鼠标交互 |

#### 自动化

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `autoStartEnabled` | bool | false | 开机自启 |
| `silentStart` | bool | false | 静默启动（后台模式） |
| `autoRotateEnabled` | bool | false | 定时随机切换 |
| `rotateInterval` | int | 30 | 切换间隔（分钟） |

#### 截图配置

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `screenshotDelay` | int | 10 | 截图前等待时间（秒） |
| `screenshotWidth` | int | 3840 | 截图宽度 |
| `screenshotHeight` | int | 2160 | 截图高度 |
| `useXvfb` | bool | true | 使用 Xvfb 静默截图 |

#### 状态记录

| 字段 | 类型 | 说明 |
|------|------|------|
| `lastWallpaper` | string | 最后应用的壁纸 ID |
| `lastScreen` | string | 最后选择的屏幕名称 |
| `activeWallpapers` | object | 各屏幕当前壁纸映射 |
| `wallpaperProperties` | object | 各壁纸自定义属性 |

---

## 后端参数映射

GUI 配置会转换为 `linux-wallpaperengine` 的命令行参数：

| GUI 配置 | 后端参数 | 示例 |
|---------|---------|------|
| `fps: 30` | `--fps 30` | 帧率限制 |
| `scaling: "stretch"` | `--scaling stretch` | 拉伸缩放 |
| `silence: true` | `--silent` | 静音 |
| `volume: 50` | `--volume 50` | 音量 |
| `noFullscreenPause: true` | `--no-fullscreen-pause` | 不暂停 |
| `disableMouse: true` | `--disable-mouse` | 禁用鼠标 |
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

## 系统集成

### 生成桌面快捷方式

在 Settings > General 页面点击 "Create Desktop Entry" 按钮会生成：

**文件位置**：`~/.local/share/applications/linux-wallpaperengine-gui.desktop`

**内容示例**：
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

点击 "Enable Autostart" 按钮会生成：

**文件位置**：`~/.config/autostart/linux-wallpaperengine-gui.desktop`

如果启用了"静默启动"，`Exec` 行会变为：
```
Exec=/usr/bin/python3 /home/user/suw/run_gui.py --hidden
```

### 窗口管理器集成示例

#### Compact Mode 窗口管理配置

由于 Wayland 协议限制，应用无法强制控制平铺窗口管理器（如 Niri/Hyprland）下的窗口大小。为了获得最佳体验（浮窗模式），请在您的 WM 配置文件中添加以下规则：

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
windowrulev2 = size 300 740,title:^(Wallpaper Preview)$
windowrulev2 = center,title:^(Wallpaper Preview)$
```

#### Niri (常规启动)

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
}

---

## Compact Mode 窗口配置 (Niri/Hyprland)

Compact Mode 旨在提供一个极简的预览窗口。在平铺窗口管理器中，你可能需要配置特定的窗口规则来保持其尺寸或浮动状态。

### Niri (config.kdl)

```kdl
window-rule {
    match title="Wallpaper Preview"
    default-column-width { fixed 300; }
    default-window-height { fixed 740; }
}
```

### Hyprland (hyprland.conf)

```
windowrulev2 = float, title:^(Wallpaper Preview)$
windowrulev2 = size 300 740, title:^(Wallpaper Preview)$
```

---

## 截图功能详解

### 工作原理

1. **检测 Xvfb**：检查系统是否安装 `xvfb-run`
2. **选择模式**：
   - 有 Xvfb：静默模式（虚拟 X 服务器）
   - 无 Xvfb：窗口模式（物理窗口）
3. **启动渲染**：使用 `--screenshot` 参数启动后端
4. **智能延迟**：
   - Video 壁纸：5 秒（快速采样第一帧）
   - Web/Scene 壁纸：使用配置的延迟时间
5. **保存文件**：截图保存到 `~/Pictures/wallpaperengine/`

### 配置选项

在 Settings > Advanced 中可配置：

- **Screenshot Delay**：截图前等待时间（秒）
  - 推荐值：Video=5, Web/Scene=10-15
- **Screenshot Resolution**：截图分辨率
  - 推荐：3840x2160（4K）
  - 用途：解决平铺窗口管理器的画面裁剪问题
- **Use Xvfb for Screenshots**：是否使用虚拟 X 服务器
  - 开启：后台截图，不弹窗
  - 关闭：物理窗口模式（某些壁纸兼容性更好）

### 安装 Xvfb

```bash
# Arch Linux
sudo pacman -S xorg-server-xvfb

# Ubuntu/Debian
sudo apt install xvfb
```

### 手动截图命令

```bash
# 使用 Xvfb（后台）
xvfb-run -a -s "-screen 0 3840x2160x24" \
  linux-wallpaperengine \
  --screenshot /path/to/wallpaper \
  --screenshot-delay 10

# 窗口模式
linux-wallpaperengine \
  --screenshot /path/to/wallpaper \
  --fps 30 \
  --screenshot-delay 10
```

---

## 定时轮换功能

### 启用方式

在 Settings > Automation 中：
1. 勾选 "Enable Auto Rotate"
2. 设置 "Rotate Interval" (分钟)
3. 点击 Save Settings

### 工作机制

- 使用 `GLib.timeout_add_seconds` 定时器
- 每隔指定时间调用随机切换逻辑
- 支持多显示器（所有屏幕同时随机切换）
- 窗口隐藏时仍继续运行

### 使用场景

- **幻灯片模式**：每 5 分钟切换一次，体验不同壁纸
- **内存管理**：每 30 分钟切换，缓解 Web 壁纸内存泄漏
- **随机性**：避免长期看同一壁纸

### 停止轮换

- 取消勾选 "Enable Auto Rotate" 并保存
- 或手动应用特定壁纸（会重置定时器）

---

## 多显示器配置

### 屏幕检测

GUI 会自动检测：
1. X11：使用 `xrandr --listmonitors`
2. Wayland：使用 `wlr-randr`（如果可用）
3. 回退：允许手动输入屏幕名称

### 配置独立壁纸

1. 在顶栏下拉菜单选择目标显示器
2. 浏览并应用壁纸
3. 重复以上步骤为其他显示器配置

### 配置文件示例

```json
{
  "activeWallpapers": {
    "eDP-1": "1234567890",   // 笔记本内屏
    "HDMI-1": "9876543210",  // 外接显示器
    "DP-1": "1122334455"     // 第二外接显示器
  }
}
```

### 已知问题

- 屏幕断开后需要手动停止对应壁纸（GUI 启动时会自动清理）
- 不同刷新率的显示器可能导致 FPS 不一致
- 旋转屏幕的壁纸缩放可能异常

---

## 日志系统

### 日志来源

- **Controller**：GUI 控制逻辑
- **Engine**：`linux-wallpaperengine` 后端输出
- **GUI**：GTK 界面事件

### 日志级别

- **DEBUG**：详细调试信息（灰色）
- **INFO**：一般信息（白色）
- **WARNING**：警告（黄色）
- **ERROR**：错误（红色）

### 日志文件位置

- **GUI 日志**：`~/.config/linux-wallpaperengine-gui/app.log`
- **引擎日志**：`~/.config/linux-wallpaperengine-gui/engine_<wallpaper_id>.log`

### 查看日志

**在 GUI 中**：
- 切换到 Settings 页面
- 点击 Logs 标签
- 日志自动刷新（可点击 Refresh 强制刷新）

**命令行**：
```bash
# 查看 GUI 日志
tail -f ~/.config/linux-wallpaperengine-gui/app.log

# 查看引擎日志
tail -f ~/.config/linux-wallpaperengine-gui/engine_*.log
```

### 复制日志

点击 "Copy Logs" 按钮会将所有日志复制到系统剪贴板，方便提交 Issue。

---

## 故障排查

### 壁纸无法应用

**症状**：点击 Apply 后没有反应或立即消失

**排查步骤**：
1. 检查日志（Settings > Logs）是否有错误
2. 确认 `linux-wallpaperengine` 在 PATH 中：
   ```bash
   which linux-wallpaperengine
   ```
3. 尝试手动运行后端：
   ```bash
   linux-wallpaperengine --screen-root eDP-1 /path/to/wallpaper
   ```
4. 检查壁纸文件夹是否完整（有 `project.json`）

---

### 截图失败

**症状**：点击截图按钮后无输出或报错

**排查步骤**：
1. 检查截图目录是否可写：
   ```bash
   ls -ld ~/Pictures/wallpaperengine
   ```
2. 如果启用了 Xvfb，确认已安装：
   ```bash
   which xvfb-run
   ```
3. 尝试关闭 Xvfb 模式（Settings > Advanced）
4. 增加截图延迟时间（10 秒以上）

---

### 系统托盘图标不显示

**症状**：GUI 启动后托盘区没有图标

**排查步骤**：
1. 确认安装了 `libayatana-appindicator`：
   ```bash
   # Arch
   pacman -Q libayatana-appindicator
   
   # Ubuntu/Debian
   dpkg -l | grep libayatana-appindicator3-1
   ```
2. 检查是否有系统托盘支持：
   - GNOME：需要安装 "AppIndicator Support" 扩展
   - Waybar：确保配置了 `tray` 模块
   - i3/Sway：可能需要 `waybar` 或其他状态栏

---

### 内存占用过高

**症状**：长期运行后内存超过 500MB

**解决方案**：
1. 启用定时轮换（Settings > Automation）
2. 避免使用复杂 Web 壁纸
3. 降低 FPS（Settings > General）
4. 使用 systemd 定时任务定期重启：
   ```bash
   # 创建 ~/.config/systemd/user/wallpaper-restart.service
   [Unit]
   Description=Restart Wallpaper Engine
   
   [Service]
   Type=oneshot
   ExecStart=/usr/bin/python3 /home/user/suw/run_gui.py --stop
   ExecStartPost=/bin/sleep 2
   ExecStartPost=/usr/bin/python3 /home/user/suw/run_gui.py --apply-last
   ```
   
   ```bash
   # 创建 ~/.config/systemd/user/wallpaper-restart.timer
   [Unit]
   Description=Restart Wallpaper Engine every 6 hours
   
   [Timer]
   OnBootSec=6h
   OnUnitActiveSec=6h
   
   [Install]
   WantedBy=timers.target
   ```
   
   ```bash
   systemctl --user enable --now wallpaper-restart.timer
   ```

---

### GUI 无法启动

**症状**：运行 `python3 run_gui.py` 后报错

**常见错误**：

1. **ModuleNotFoundError: No module named 'gi'**
   ```bash
   # 缺少 PyGObject
   sudo pacman -S python-gobject  # Arch
   sudo apt install python3-gi     # Ubuntu
   ```

2. **gi.repository.GLib.Error: Settings schema 'org.gnome.desktop.interface' is not installed**
   ```bash
   # 缺少 GNOME schemas
   sudo pacman -S gsettings-desktop-schemas  # Arch
   sudo apt install gsettings-desktop-schemas # Ubuntu
   ```

3. **ImportError: cannot import name 'Adw' from 'gi.repository'**
   ```bash
   # 缺少 Libadwaita
   sudo pacman -S libadwaita  # Arch
   sudo apt install gir1.2-adw-1  # Ubuntu
   ```

---

## 性能调优

### 降低 CPU 占用

1. 降低 FPS（Settings > General）：30fps -> 24fps 或更低
2. 启用"禁用粒子系统"（Settings > Advanced）
3. 启用"禁用视差效果"（Settings > Advanced）
4. 使用 Video 壁纸代替 Scene/Web

### 降低内存占用

1. 避免使用 Web 壁纸
2. 启用定时轮换（强制定期释放内存）
3. 禁用音频处理（Settings > Audio）

### 降低 GPU 占用

1. 降低 FPS
2. 使用简单壁纸
3. 启用"全屏时暂停"（取消勾选 "No Fullscreen Pause"）

---

## 获取帮助

如果以上方法无法解决问题：

1. 查看 [docs/COMPATIBILITY.md](COMPATIBILITY.md) 确认环境兼容性
2. 检查 [GitHub Issues](https://github.com/your-repo/issues) 是否有相似问题
3. 提交新 Issue 并附上：
   - 系统信息（`uname -a`）
   - 桌面环境
   - 完整日志（Settings > Logs > Copy Logs）
   - 壁纸 ID 和类型
