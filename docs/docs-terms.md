# Bilingual Terminology Glossary / 双语术语表

> This glossary ensures consistent terminology across all bilingual documentation.
> 本术语表确保所有双语文档中的术语保持一致。

---

## Core Feature Names / 核心功能名称

| English | 中文 | Context |
|---------|------|---------|
| Playback History | 播放历史 | v0.10.3-beta feature |
| Nickname (System) | 别名（系统） | v0.10.2 feature, also "壁纸昵称" |
| Compact Preview Mode | 紧凑预览模式 | v0.10.0 feature |
| Performance Monitor | 性能监控 | v0.9.0 feature |
| Screenshot History | 截图历史记录 | v0.9.2 feature |
| Hamburger Menu | 汉堡菜单 | v0.10.3-alpha, global app menu |
| Update Checker | 更新检查器 | v0.10.3 feature |
| Timed Rotation | 定时轮换 | v0.8.0 feature |
| Cycle Order | 轮换顺序 | v0.8.11 feature, rotation mode |
| Sorting | 排序 | v0.8.2 feature |
| System Tray | 系统托盘 | v0.7.0 feature |
| Desktop Entry / Shortcut | 桌面快捷方式 | v0.8.0 feature |
| Autostart | 开机自启 | v0.8.0 feature |
| Graceful Quit | 优雅退出 | v0.10.3-alpha feature |
| Welcome Guide | 欢迎向导 | v0.10.3 feature |
| About Dialog | 关于对话框 | v0.10.3-beta feature |

## Theme & Visual / 主题与视觉

| English | 中文 | Notes |
|---------|------|-------|
| Light/Dark Theme Adaptive | 浅色/深色主题自适应 | ❌ Do NOT use "深色主题" alone |
| System Accent Color Sync | 系统强调色同步 | v0.10.5 feature |
| Capsule Glow Design | 胶囊光晕设计 | v0.10.5, wallpaper name display |
| Accessibility | 可访问性 | Focus-visible styles |
| Named Colors | 命名颜色 | GTK/Libadwaita CSS variables |
| Dark Mode | 深色模式 | Only when contrasting with Light Mode |
| Light Mode | 浅色模式 | v0.10.4/v0.10.5 |

## UI Components / 界面组件

| English | 中文 | Notes |
|---------|------|-------|
| Sidebar | 侧边栏 | Right detail panel |
| Toolbar | 工具栏 | Top action bar |
| Navigation Bar / Top Bar | 顶栏/导航栏 | Top navigation area |
| Grid View | 网格视图 | Wallpaper card layout |
| List View | 列表视图 | Wallpaper list layout |
| Toast Notification | Toast 通知 | Adw.ToastOverlay |
| Capsule / Tag | 胶囊/标签 | Styled label chips |
| Dropdown | 下拉菜单 | Gtk.DropDown |
| Split Button | 拆分按钮 | Apply button with dropdown |
| Spinner | 加载圈 | Gtk.Spinner |

## Multi-Monitor / 多显示器

| English | 中文 | Notes |
|---------|------|-------|
| Multi-Monitor Support | 多显示器支持 | v0.8.0 beta |
| Link/Unlink Mode | 链接/独立模式 | v0.8.4, Same/Diff mode |
| Same Mode | 同步模式 | Apply to all screens |
| Diff Mode | 独立模式 | Apply to selected screen |
| Screen Selector | 屏幕选择器 | Top bar dropdown |
| Dynamic Screen Detection | 动态屏幕检测 | v0.10.4, auto-detect primary |
| Primary Display | 主显示器 | Auto-detected via xrandr |

## Screenshot / 截图

| English | 中文 | Notes |
|---------|------|-------|
| Silent Screenshot | 静默截图 | Xvfb mode |
| Screenshot Resolution | 截图分辨率 | Default 3840x2160 |
| Xvfb (Virtual Framebuffer) | 虚拟帧缓冲 | For headless screenshot |
| Screenshot Delay | 截图延迟 | Wait before capture |
| Animated Screenshot Button | 动态截图按钮 | v0.10.4, Spinner feedback |

## Wallpaper Types / 壁纸类型

| English | 中文 | Notes |
|---------|------|-------|
| Video Wallpaper | 视频壁纸 | .mp4, .webm |
| Web Wallpaper | Web 壁纸 | .html, CEF-based |
| Scene Wallpaper | 场景壁纸 | .pkg, 3D scenes |
| GIF Thumbnail | GIF 缩略图 | Smart frame extraction |
| Dynamic Preview | 动态预览 | GIF animation playback |

## Configuration / 配置

| English | 中文 | Notes |
|---------|------|-------|
| Configuration File | 配置文件 | config.json |
| Config Manager | 配置管理器 | ConfigManager class |
| Robust Config Fallback | 健壮配置回退 | v0.10.5, None-trap fix |
| Workshop Path | Workshop 路径 | Steam Workshop directory |
| Assets Path | Assets 路径 | Wallpaper Engine assets |
| FPS Limit | 帧率限制 | 1-144 |
| Scaling Mode | 缩放模式 | stretch/fit/fill/default |
| Clamping Mode | 纹理钳制模式 | default/clamp/border |

## Wayland / Wayland 环境

| English | 中文 | Notes |
|---------|------|-------|
| Wayland Advanced Tweaks | Wayland 高级调整 | v0.8.10 settings panel |
| Pause Only Active | 仅活动时暂停 | --fullscreen-pause-only-active |
| Ignore App ID List | 忽略应用列表 | --fullscreen-pause-ignore-appid |
| Fullscreen Pause | 全屏暂停 | Pause wallpaper on fullscreen |
| Mouse Interaction | 鼠标交互 | Disabled on Wayland |
| Compositor | 混成器/合成器 | Window manager (Niri, Sway, etc.) |

## Backend / 后端

| English | 中文 | Notes |
|---------|------|-------|
| linux-wallpaperengine | linux-wallpaperengine | C++ backend, keep as-is |
| Backend / Engine | 后端/引擎 | Rendering engine |
| Frontend / GUI | 前端/GUI | Python GTK4 app |
| Process Management | 进程管理 | Start/stop/restart backend |
| Single Instance | 单实例 | Only one GUI process |

## Architecture / 架构

| English | 中文 | Notes |
|---------|------|-------|
| Wallpaper Controller | 壁纸控制器 | WallpaperController class |
| History Manager | 历史管理器 | HistoryManager class |
| Nickname Manager | 别名管理器 | NicknameManager class |
| Performance Monitor | 性能监控器 | PerformanceMonitor class |
| Object Pooling | 对象池 | v0.10.1, thumbnail optimization |
| Animated Preview | 动态预览组件 | AnimatedPreview component |

## Platform & Distribution / 平台与分发

| English | 中文 | Notes |
|---------|------|-------|
| Arch Linux | Arch Linux | Primary test platform |
| Ubuntu / Debian | Ubuntu / Debian | Secondary platform |
| Niri | Niri | Primary Wayland compositor |
| Hyprland | Hyprland | Supported compositor |
| Sway | Sway | Supported compositor |
| AppImage | AppImage | Distribution format |
| Window Manager (WM) | 窗口管理器 | Tiling/floating WM |
| Tiling WM | 平铺窗口管理器 | Niri, Hyprland, i3, Sway |
| Intel Iris Xe | Intel Iris Xe | ❌ Do NOT write "Irix" |

## Log System / 日志系统

| English | 中文 | Notes |
|---------|------|-------|
| Log Filter | 日志过滤器 | v0.9.1, by module |
| Log Source | 日志来源 | Controller/Engine/GUI |
| Log Level | 日志级别 | DEBUG/INFO/WARNING/ERROR |

---

## Forbidden Terms / 禁止使用的术语

| ❌ Do NOT use | ✅ Use Instead | Reason |
|--------------|---------------|--------|
| 深色主题 (alone) | 浅色/深色主题自适应 | Misleading; light mode fully supported since v0.10.4 |
| Intel Irix Xe | Intel Iris Xe | Typo in original docs |
| 精简模式 | 紧凑预览模式 | Inconsistent naming |
| 昵称管理 | 别名管理 | Standardize to "别名" |
| Dark theme (alone, as feature) | Light/Dark theme adaptive | Same as Chinese |

---

## Document Naming Convention / 文档命名规范

| Language | Filename Pattern | Example |
|----------|-----------------|---------|
| English (Default) | `NAME.md` | `README.md`, `CHANGELOG.md` |
| Chinese | `NAME_CN.md` | `README_CN.md`, `docs/ADVANCED_CN.md` |

## Language Switch Link Format / 语言切换链接格式

| File | First Line |
|------|-----------|
| English docs | `[中文](FILENAME_CN.md)` |
| Chinese docs | `[English](FILENAME.md)` |
