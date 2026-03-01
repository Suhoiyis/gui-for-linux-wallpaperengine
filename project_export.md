# 项目结构与文件内容导出 (Rust Project)

**生成时间**: 2026-02-25 22:15:23
**根目录**: `/home/yua/gui-for-linux-wallpaperengine`
---

## 📂 项目结构图

```text
/
├── README_ZH.md
├── TESTING_AND_RELEASE_PLAN.md
├── build_appimage.sh
├── folder.py
├── linuxdeploy-plugin-gtk.sh
├── lwg-rs/
│   ├── Cargo.lock
│   ├── Cargo.toml
│   └── crates/
│       ├── lwg-core/
│       │   ├── Cargo.toml
│       │   └── src/
│       │       ├── config.rs
│       │       └── lib.rs
│       ├── lwg-ipc/
│       │   ├── Cargo.toml
│       │   └── src/
│       │       └── lib.rs
│       ├── lwg-tray/
│       │   ├── Cargo.toml
│       │   └── src/
│       │       └── main.rs
│       └── lwg-ui/
│           ├── Cargo.toml
│           └── src/
│               └── main.rs
├── pic/
│   └── icons/
│       ├── GUI.png
│       ├── GUI_glass.png
│       ├── GUI_rounded.png
│       ├── gui_tray.png
│       ├── gui_tray_glass.png
│       ├── gui_tray_rounded-stopped.png
│       └── gui_tray_rounded.png
├── py_GUI/
│   ├── __init__.py
│   ├── const.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── controller.py
│   │   ├── history.py
│   │   ├── integrations.py
│   │   ├── logger.py
│   │   ├── nickname.py
│   │   ├── performance.py
│   │   ├── properties.py
│   │   ├── screen.py
│   │   ├── updater.py
│   │   └── wallpaper.py
│   ├── main.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── compact_window.py
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── animated_preview.py
│   │   │   ├── dialogs.py
│   │   │   ├── history_dialog.py
│   │   │   ├── navbar.py
│   │   │   ├── nickname_manager_dialog.py
│   │   │   ├── sidebar.py
│   │   │   ├── sparkline.py
│   │   │   └── welcome_dialog.py
│   │   ├── pages/
│   │   │   ├── __init__.py
│   │   │   ├── performance.py
│   │   │   ├── settings.py
│   │   │   └── wallpapers.py
│   │   ├── tray.py
│   │   └── tray_process.py
│   └── utils.py
├── pyproject.toml
├── run_gui.py
└── tray_rs/
    ├── Cargo.lock
    ├── Cargo.toml
    └── src/
        └── main.rs
```

---

## 📄 文件详细内容

### 📄 文件: `README_ZH.md`

```markdown
<h1 align="center">
  <img src="pic/icons/GUI_rounded.png" alt="Logo" width="128" height="128" style="border-radius: 20px;"/><br>
  LINUX WALLPAPER ENGINE GUI
</h1>

<p align="center">一个现代化的 GTK4 图形界面，用于在 Linux 上管理和应用 Steam Workshop 动态壁纸。</p>

<p align="center">
  <a href="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases/latest">
    <img src="https://img.shields.io/github/v/release/Suhoiyis/gui-for-linux-wallpaperengine?color=success&label=Release&style=flat-square" alt="Latest Release">
  </a>
  <a href="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Suhoiyis/gui-for-linux-wallpaperengine?style=flat-square&color=blue" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Platform-Linux-lightgrey?style=flat-square&logo=linux" alt="Platform">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/GUI-GTK4-4A86CF?style=flat-square&logo=gnome&logoColor=white" alt="GTK4">
</p>

<p align="center">
    <a href="README.md">English</a> | 
    <strong>简体中文</strong>
<p>

> 基于 [linux-wallpaperengine](https://github.com/Almamu/linux-wallpaperengine) 后端构建，针对 GNOME / Wayland 桌面环境进行了优化。

> ## 🚀 架构升级公告
> **我们正在用 Rust 重写整个项目！**
> ### ⚡ 性能革新
> - 我们正计划进行一次重大架构升级——使用 Rust 完全重写核心模块。通过替换现有的 Python 架构，我们将为您带来：
>   - 🚀 原生级极致性能 — 摆脱解释器开销，运行速度大幅提升
>   - 💾 更低资源占用 — 内存消耗显著降低，轻量级运行
>   - 🔒 更强的类型安全 — 编译时检查，减少运行时错误
>   - 🛠️ 更好的并发支持 — 充分利用多核处理器
> 
> - 📍 查看进展：切换至 [main-pre](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/tree/main-pre) 分支 了解最新开发动态
> - 📥 尝鲜体验：在 [Pre-release](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases) 中下载最新构建版本 (Assets)
> 
> - ⚠️ 注意：Rust 版本目前处于开发阶段，可能存在不稳定因素，建议生产环境继续使用稳定版。



<div align="center">
  <table width="100%">
    <tr>
      <td align="center"><b>深色模式</b></td>
      <td align="center"><b>浅色模式</b></td>
    </tr>
    <tr>
      <td align="center">
        <img src="docs/assets/main-ui.png" width="400" style="display: block;">
      </td>
      <td align="center">
        <img src="docs/assets/light-theme.png" width="400" style="display: block;">
      </td>
    </tr>
  </table>
</div>

## ✨ 功能特性

### 核心功能

- 🎨 **浅色/深色主题自适应**: 完全适配系统的浅色或深色主题，并自动同步强调色 —— 告别浅色模式下难以阅读的文本
- 🖥️ **多显示器支持**: 为每个显示器设置独立的壁纸，支持“链接/取消链接”模式进行批量或逐屏控制
- 📜 **播放历史**: 自动追踪最近播放的 30 张壁纸，包含时间戳、缩略图和一键重播功能
- ✏️ **别名系统**: 为壁纸分配自定义别名以便于识别；支持批量管理和搜索集成
- 🔍 **搜索与排序**: 对标题、描述和标签进行实时关键词搜索；支持按名称、大小、类型或文件夹 ID 排序
- 📺 **智能系统托盘**: 具备状态感知的动态图标（根据播放状态智能切换彩色/灰阶）；支持原生左键单击一键切换主窗口；底层由零延迟的 Abstract Socket IPC 驱动。
- ⌨️ **命令行控制**: 完整的 CLI 支持，通过单实例架构实现无头操作和远程控制

### 进阶功能

- 🪟 **紧凑预览模式**: 专为平铺式窗口管理器（Niri, Hyprland, Sway）设计的独立迷你窗口（300×700），支持圆形缩略图导航和键盘快捷键

<p align="center">
  <img src="docs/assets/compact_mode.png" alt="Compact Preview Mode" width="40%"/>
  <br>
</p>

- 📊 **性能监控**: 实时 CPU/内存追踪，提供 60 秒实时趋势图、分进程明细（前端、后端、托盘）以及详细的线程列表

  <details>
    <summary>点击查看性能监控截图</summary>
    <div align="center">
      <br>
      <img src="docs/assets/performance-monitor.png" width="70%" alt="Performance Monitor">
      <p><em>实时CPU/内存跟踪和进程详细信息</em></p>
    </div>
  </details>

- 📸 **智能截图**: 通过 Xvfb 虚拟帧缓冲进行静默 4K 截屏，根据壁纸类型智能延迟，提供资源占用统计和截图历史（最近 10 张）
- 🔄 **定时轮换**: 按可配置的时间间隔自动切换壁纸；支持随机模式和按标题、大小、类型或文件夹 ID 的顺序轮换
- ☰ **汉堡菜单**: 全局应用菜单，包含播放历史、检查更新、欢迎指南、重启和退出
- 🎛️ **Wayland 高级微调**: 精细化控制 —— 仅在活动窗口全屏时暂停，忽略特定的 app ID（如 dock、状态栏）
- 📋 **日志管理**: 按模块（控制器/引擎/GUI）过滤日志，支持复制过滤后的输出以便提交错误报告
- 🖼️ **GIF 智能缩略图**: 智能帧提取（第 15 帧）以避免空白/黑色预览图；支持透明 GIF 渲染
- 🔔 **更新检查器**: 自动检查 GitHub Release，具备智能速率限制处理和语义化版本比较功能

## 🚀 安装指南

### 1. 安装后端（必须）
本 GUI 作为控制端，需要您的系统上先安装核心渲染引擎。
请参考 [Almamu/linux-wallpaperengine](https://github.com/Almamu/linux-wallpaperengine) 的编译说明进行安装，并确保该程序已加入系统的环境变量 PATH 中：

```bash
which linux-wallpaperengine  # 验证安装是否成功
```
（Arch Linux 用户可以直接从 AUR 安装：yay -S linux-wallpaperengine）

### 2. 安装 GUI 控制端
前往 [Releases 页面](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases) 下载最新版本，然后选择您喜欢的安装方式：

#### 方法 A：Arch Linux 安装包（Arch/Manjaro 用户推荐）

我们暂未将应用上架AUR仓库（正在计划中），但是我们现在提供了预编译的 .pkg.tar.zst 包。使用 pacman 安装会自动处理所有的 GUI 依赖项。

```Bash
# 请将文件名替换为您实际下载的文件
sudo pacman -U linux-wallpaperengine-gui-*-x86_64.pkg.tar.zst
```

安装完成后，您就可以直接在桌面应用启动器中找到它了。

#### 方法 B：AppImage
开箱即用的便携格式，无需配置依赖，完美集成桌面快捷方式和系统托盘。

```Bash
# 赋予执行权限
chmod +x linux-wallpaperengine-gui-*-x86_64.AppImage

# 运行
./linux-wallpaperengine-gui-*-x86_64.AppImage
```

#### 方法 C：源码运行
如果您更喜欢直接运行 Python 脚本，请先安装前置依赖库：

```Bash
# Arch Linux
sudo pacman -S python-gobject gtk4 libadwaita libayatana-appindicator
# Ubuntu / Debian
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 libayatana-appindicator3-1
```

然后克隆本仓库并运行：

```Bash
python3 run_gui.py
```

## 📖 基本用法

### 浏览与应用壁纸

1. **浏览**: 应用在首次启动时会自动扫描您的 Steam Workshop 壁纸库
2. **应用**: 双击壁纸卡片或点击侧边栏中的 **Apply** 按钮
3. **随机**: 点击工具栏中的 🎲 按钮或使用托盘菜单
4. **停止**: 点击工具栏中的 ⏹ 按钮
5. **多显示器**: 从顶栏下拉菜单中选择目标显示器，然后应用

### 播放历史

通过 **汉堡菜单 (☰) → 播放历史** 访问您最近的壁纸历史：

- 查看最近 30 张壁纸，包含缩略图、别名（斜体）、原始 ID 和时间戳（MM-DD HH:MM）
- 一键重播之前的任何壁纸 —— 主窗口会自动同步
- 清除历史记录或检查容量（当前 / 30）

### 别名管理

为您的壁纸赋予有意义的名称：

- **设置别名**: 右键点击壁纸 → "Set Nickname"，或点击侧边栏中的 ✏️ 按钮
- **批量管理**: 设置 → "Manage Nicknames"，在对话框中查看、编辑或删除所有别名
- **搜索集成**: 搜索框同时匹配别名和原始标题
- **视觉区分**: 别名在网格视图中以 *加粗斜体* 显示；侧边栏显示“别名 + 原始名称（灰色小字）”

### 紧凑预览模式

专为平铺式窗口管理器设计的轻量级预览窗口：

- **切换**: 点击工具栏中的紧凑模式图标
- **导航**: 使用 `←` `→` 键或屏幕按钮循环切换 5 个圆形缩略图
- **快速操作**: 应用、停止、碰运气（随机）以及跳转到当前壁纸
- **窗口规则**: 您可能需要配置窗口管理器使该窗口浮动 —— 参见 [进阶指南](docs/ADVANCED.md#compact-preview-mode)

### 性能监控

点击顶栏的监控图标打开性能页面：

- **概览卡片**: 总 CPU、总内存、活动线程
- **趋势图**: 60 秒 CPU 历史（颜色标识：绿色 < 20%，橙色 < 40%，红色 ≥ 40%）和内存历史（蓝色）
- **进程详情**: 展开前端/后端/托盘以查看各项指标、线程名称和当前播放的壁纸

<details>
<summary>点击展开设置页面截图</summary>
<br>
<div align="center">
  <img src="docs/assets/settings-page1.png" width="32%" alt="Settings page1">
  <img src="docs/assets/settings-page2.png" width="32%" alt="settings page2">
  <img src="docs/assets/settings-page3.png" width="32%" alt="settings page3">
  <p><em>General Settings / Audio / Advanced Tweaks</em></p>
</div>
</details>

## ⌨️ 命令行控制

所有命令都发送到同一个运行中的实例（单实例架构）：

| 命令 | 动作 |
|---------|--------|
| `--show` | 显示窗口 |
| `--hide` | 隐藏窗口（进程继续运行） |
| `--toggle` | 切换显示/隐藏 |
| `--random` | 随机切换壁纸 |
| `--stop` | 停止当前壁纸 |
| `--apply-last` | 应用上次使用的壁纸 |
| `--refresh` | 重新扫描壁纸库 |
| `--quit` | 完全退出（GUI + 所有壁纸进程） |

**示例:** 在 Niri 中自动启动
```bash
# In your niri config.kdl
spawn-at-startup "python3" "/path/to/run_gui.py" "--hidden"

binds {
    Mod+W { spawn "python3" "/path/to/run_gui.py" "--toggle"; }
    Mod+Shift+W { spawn "python3" "/path/to/run_gui.py" "--random"; }
}
```

## ⚙️ 配置

**位置:** `~/.config/linux-wallpaperengine-gui/config.json`

关键设置（均可通过 GUI 的设置页面进行配置）：

| 设置 | 默认值 | 描述 |
|---------|---------|-------------|
| `fps` | 30 | 帧率限制 (1–144) |
| `volume` | 50 | 音量 (0–100) |
| `scaling` | `"default"` | 缩放模式: default / stretch / fit / fill |
| `silence` | `true` | 静音 |
| `autoRotateEnabled` | `false` | 启用定时轮换 |
| `rotateInterval` | 30 | 轮换间隔（分钟） |
| `cycleOrder` | `"random"` | 轮换顺序: random / title / size / type / id |
| `useXvfb` | `true` | 使用 Xvfb 进行静默截图 |
| `screenshotRes` | `"3840x2160"` | 截图分辨率 |

有关完整的配置参考，请参阅 [docs/ADVANCED.md](docs/ADVANCED.md#configuration-reference)。

## ⚠️ 已知限制

### 壁纸类型兼容性

| 类型 | 状态 | 备注 |
|------|--------|-------|
| **Video** | ✅ 完全支持 | 推荐使用 MP4/WebM |
| **Web** | ⚠️ 部分支持 | 渲染正常，但 **属性调节功能失效**（后端限制） |
| **Scene** | ⚠️ 受限 | 复杂的粒子系统 / 自定义着色器可能会出现闪烁或失败 |

### Wayland 限制

- ❌ **禁用鼠标交互**: 无法获取全局光标位置；点击交互和鼠标拖尾效果无法工作
- ❌ **Web 属性注入受限**: 在 Wayland 的安全模型下，CEF 通信受到限制

有关详细的兼容性信息，请参阅 [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md)。

### 其他说明

- **内存增长**: 长期运行的 Web 壁纸可能会缓慢增加内存占用（上游引擎问题）。启用定时轮换可以缓解此问题。
- **测试环境**: 主要在 Arch Linux + Niri 上进行测试。其他环境可能需要调整。

## ❓ 常见问题

### 为什么 Web 壁纸的属性调节不起作用？

C++ 后端使用 CEF (Chromium Embedded Framework) 处理 Web 壁纸。在 Linux/Wayland 上，CEF 的进程间通信存在兼容性问题，导致 JavaScript 属性注入无法可靠工作。壁纸将以默认设置运行。作为权宜之计，您可以手动编辑壁纸的 `project.json` 或 HTML 源文件。

### 如何降低内存占用？

1. 避免使用 Web 壁纸（它们内部使用 CEF/Chromium）
2. 启用定时轮换（设置 → 自动化）以定期重启后端
3. 降低 FPS（设置 → 常规）
4. 禁用音频处理（设置 → 高级）

### 紧凑预览窗口在我的平铺式窗口管理器中没有浮动

您需要在窗口管理器配置中添加窗口规则。请参阅 [docs/ADVANCED.md](docs/ADVANCED.md#compact-preview-mode) 查看 Niri 和 Hyprland 的示例。

### 为什么截图很慢（5–10 秒）？

如果安装了 Xvfb，应用会使用 CPU 软件渲染来静默生成 4K 截图（无弹出窗口）。这虽然较慢，但无论您的物理屏幕分辨率或平铺式窗口管理器布局如何，都能保证一致的质量。您可以在“设置 → 高级”中禁用 Xvfb 模式以获得更快的（但会弹出窗口的）截图。

### 系统托盘图标不显示

1. 确认已安装 `libayatana-appindicator`
2. GNOME 用户：安装 "AppIndicator Support" 扩展
3. Waybar 用户：确保已配置 `tray` 模块
4. i3/Sway 用户：您可能需要 `waybar` 或其他支持托盘的状态栏

### 如何为每个显示器设置不同的壁纸？

从顶栏下拉菜单中选择目标显示器，然后浏览并应用壁纸。对每个显示器重复此操作。使用 🔗 链接/取消链接按钮在“应用于所有屏幕（相同模式）”或“仅应用于所选屏幕（差异模式）”之间切换。

### 我可以使用 Flatpak 或 AppImage 吗？

**AppImage**: 完全支持，具备零配置桌面集成。应用会自动创建 .desktop 快捷方式并在文件移动时自我修复；内置 FUSE 沙盒穿透机制，确保在所有 Linux 桌面环境下托盘图标都能 100% 正常渲染。

**Flatpak**: 目前尚未正式支持。文件访问和沙盒限制可能会影响功能。

### 如何报告错误？

1. 前往 设置 → 日志，点击 **Copy Logs**
2. 提交一个 [GitHub Issue](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues)
3. 包含：系统信息 (`uname -a`)、桌面环境、壁纸 ID/类型以及复制的日志

## 🏛️ 技术架构

### 项目结构

```
suw/
├── py_GUI/                    # Main application package
│   ├── core/                  # Core logic
│   │   ├── controller.py      # WallpaperController — process management
│   │   ├── config_manager.py  # ConfigManager — settings I/O with robust fallback
│   │   ├── history.py         # HistoryManager — playback history (30 entries)
│   │   └── nickname.py        # NicknameManager — alias persistence
│   ├── ui/                    # User interface
│   │   ├── app.py             # Main application window
│   │   ├── components/        # Reusable components (navbar, sidebar, preview)
│   │   └── pages/             # Page views (wallpapers, settings, performance)
│   ├── utils/                 # Utilities
│   │   ├── performance.py     # PerformanceMonitor — CPU/memory tracking
│   │   └── logger.py          # Logging configuration
│   └── const.py               # Constants, version, CSS styles
├── run_gui.py                 # Entry point
├── docs/                      # Documentation
│   └── assets/                # Screenshots and images
└── pic/icons/                 # Application icons
```

### 架构概览

```
┌──────────────────────────────────────────────────┐
│                    GTK4 + Libadwaita             │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ Wallpaper│  │ Settings │  │  Performance   │  │
│  │   Page   │  │   Page   │  │    Monitor     │  │
│  └────┬─────┘  └────┬─────┘  └───────┬────────┘  │
│       │             │                │           │
│  ┌────┴─────────────┴────────────────┴─────────┐ │
│  │           WallpaperController               │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐ │ │
│  │  │ Config   │ │ History  │ │  Nickname    │ │ │
│  │  │ Manager  │ │ Manager  │ │  Manager     │ │ │
│  │  └──────────┘ └──────────┘ └──────────────┘ │ │
│  └──────────────────┬──────────────────────────┘ │
│                     │ subprocess                 │
│  ┌──────────────────┴───────────────────────────┐│
│  │         linux-wallpaperengine (C++)          ││
│  │         Rendering · Audio · Screenshot       ││
│  └──────────────────────────────────────────────┘│
│                                                  │
│  ┌─────────────────────────────────────────────┐ │
│  │         System Tray (Rust + Ksní)           │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

### 关键设计决策

- **单实例架构**: 所有 CLI 命令都通过 `Gio.Application` 路由到运行中的 GTK 应用，避免进程重复
- **防御性配置**: `ConfigManager.get()` 正确处理 `None` 值和“假值但有效”的值（例如 `volume=0`）
- **主题变量**: 所有 UI 颜色均使用 GTK/Libadwaita 命名颜色（`@window_bg_color`, `@theme_fg_color`, `@accent_bg_color`），实现无缝主题适配
- **对象池**: 紧凑模式缩略图使用对象池技术以消除滚动卡顿

## 📚 文档

| 文档 | 描述 |
|----------|-------------|
| [CHANGELOG_CN.md](docs/CHANGELOG_ZH.md) | 版本历史和发布说明 |
| [docs/ADVANCED_CN.md](docs/ADVANCED_ZH.md) | 进阶功能、配置参考及窗口管理器集成 |
| [docs/COMPATIBILITY_CN.md](docs/COMPATIBILITY_ZH.md) | 壁纸类型兼容性、Wayland 限制及硬件要求 |
| [docs/TROUBLESHOOTING_CN.md](docs/TROUBLESHOOTING_ZH.md) | 常见错误、后端日志分析及修复方案 |

## 🔧 技术栈

- **语言**: Python 3.10+
- **UI 框架**: PyGObject (GTK4 + Libadwaita)
- **系统托盘**: Rust + Ksní
- **后端**: linux-wallpaperengine (C++)
- **图表**: 基于 Cairo 的实时趋势图组件

## 🤝 贡献

欢迎贡献！

- 功能请求和错误报告 → [提交 Issue](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues)
- 代码贡献 → 遵循现有代码风格并提交 Pull Request
- 同样欢迎对文档进行改进

## 🙏 致谢

> 部分 UI 设计灵感源自 [AzPepoze/linux-wallpaperengine-gui](https://github.com/AzPepoze/linux-wallpaperengine-gui)。
>
> 这是一个非常优秀的 GUI 项目 —— 我们推荐您也去关注一下。

## 📄 许可证

GPL-3.0 license

---

**Current Version**: v1.0.0-pre

**Last Updated**: 2026-02-24

*A Vibe Coding experiment project*

```

---

### 📄 文件: `TESTING_AND_RELEASE_PLAN.md`

```markdown
# Linux Wallpaper Engine GUI - 测试与发布计划

**文档版本**: v1.4
**创建日期**: 2026-01-25
**项目当前版本**: v0.10.6
## 📋 项目现状概览

### 当前状态
- **版本**: v0.10.6 (2026-02-15)
- **完成度**: ~98%
- **核心功能**: ✅ 基本完善
- **测试覆盖**: ❌ 待建立
- **发布渠道**: ❌ 仅源码

### 已完成的核心功能
- ✅ 壁纸浏览和管理
- ✅ 多显示器支持 (Beta)
- ✅ 系统托盘集成
- ✅ 定时轮换功能
- ✅ 高质量截图
- ✅ 命令行控制
- ✅ 配置管理
- ✅ 系统集成 (自启动、桌面快捷方式)
- ✅ **性能监控** (v0.9.2 增强：线程拆分、准确率优化、截图历史)
- ✅ **日志管理增强** (v0.9.1 新增)

---

## 🧪 自动化测试体系建设计划

### 阶段1: 基础测试框架搭建 (第1周)

#### 1.1 环境准备
```bash
# 安装测试依赖
sudo pacman -S xorg-server-xvfb imagemagick  # Arch
# sudo apt install xvfb imagemagick  # Ubuntu

pip install pytest pytest-mock pytest-cov pillow dbus-python

# 创建测试目录结构
mkdir -p tests/{unit,integration,visual,functional}
touch tests/__init__.py
```

#### 1.2 测试配置
- 创建 `pytest.ini` 配置文件
- 设置覆盖率报告 (HTML + 终端输出)
- 配置虚拟显示器环境

#### 1.3 核心工具类单元测试
- `ConfigManager`: 配置读写逻辑
- `WallpaperController`: 核心应用逻辑
- `ScreenManager`: 多屏幕检测
- `Logger`: 日志管理

**预期成果**: 基础测试框架可用，核心工具类覆盖率 > 80%

---

### 阶段2: 视觉回归测试 (第2-3周)

#### 2.1 虚拟显示器测试方案

**核心思路**: 虚拟显示器 + 自动截图对比
- 在虚拟显示器中运行测试，不影响主桌面
- 自动截图验证壁纸显示效果
- 与基准图像对比，确保视觉效果一致

#### 2.2 测试实现

**测试文件结构**:
```
tests/visual/
├── test_wallpaper_display.py      # 壁纸显示测试
├── test_screenshot_quality.py     # 截图质量测试
├── test_multi_screen.py          # 多显示器测试
├── baselines/                     # 基准截图目录
└── results/                      # 测试结果截图
```

**关键功能**:
- 虚拟显示器自动创建和清理
- 壁纸应用后自动截图
- 图像相似度对比算法
- 空白屏幕检测
- 多种壁纸类型测试

#### 2.3 测试用例设计

1. **基础显示测试**
   - 验证不同类型壁纸 (Video/Web/Scene) 能否正确显示
   - 检测显示是否为空白或异常

2. **视觉效果回归测试**
   - 对比截图与基准图像
   - 相似度阈值: > 90%
   - 自动生成差异报告

3. **多显示器测试**
   - 测试不同显示器独立控制
   - 验证屏幕切换逻辑
   - 测试显示器断开/重连场景

**预期成果**: 视觉效果自动化验证，无需人工干预

---

### 阶段3: 功能集成测试 (第4周)

#### 3.1 真实环境集成测试

**测试内容**:
- 完整的用户操作流程
- 与真实 `linux-wallpaperengine` 后端集成
- 系统托盘功能测试
- 命令行接口测试

#### 3.2 性能测试
- 壁纸加载时间测试 (< 5秒)
- 内存使用监控
- CPU 占用检测
- 长时间运行稳定性测试

#### 3.3 兼容性测试
- 不同桌面环境测试 (GNOME/KDE/Niri/Sway/Hyprland)
- 不同发行版兼容性 (Arch/Ubuntu/Fedora)
- Wayland vs X11 环境差异测试

**预期成果**: 全面的功能验证，确保在各种环境下正常工作

---

### 阶段4: 持续集成 (第5-6周)

#### 4.1 GitHub Actions 设置

**工作流程**:
```yaml
# .github/workflows/test.yml
name: Automated Testing
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Environment
        run: |
          sudo apt update
          sudo apt install xvfb imagemagick python3-gi gir1.2-gtk-4.0
      - name: Run Tests
        run: |
          xvfb-run -a pytest --cov=py_GUI --cov-report=xml
      - name: Upload Coverage
        uses: codecov/codecov-action@v3
```

#### 4.2 测试报告
- 覆盖率趋势图
- 视觉测试结果展示
- 性能基准报告
- 自动化测试通知

**预期成果**: 每次提交自动运行测试，及时发现问题

---

## 📦 发布与分发计划

### 1. 包管理系统支持

#### 1.1 Arch Linux AUR 包
**优先级**: 高 (Arch 用户多)

**任务清单**:
- [ ] 创建 `PKGBUILD` 文件
- [ ] 处理依赖关系 (python-gobject, gtk4, libadwaita等)
- [ ] 包含 `.desktop` 文件和图标
- [ ] 提交到 AUR 社区仓库

**PKGBUILD 示例**:
```bash
pkgname=linux-wallpaperengine-gui
pkgver=0.8.0
pkgrel=1
pkgdesc="Modern GTK4 GUI for managing Steam Workshop wallpapers on Linux"
arch=('any')
url="https://github.com/yourusername/linux-wallpaperengine-gui"
license=('GPL3')
depends=('python' 'python-gobject' 'gtk4' 'libadwaita' 'libayatana-appindicator')
optdepends=('linux-wallpaperengine: backend engine')
source=("$pkgname-$pkgver.tar.gz")
sha256sums=()
```

#### 1.2 Debian/Ubuntu 包
**优先级**: 中 (Ubuntu 用户基础大)

**任务清单**:
- [ ] 创建 `debian/` 目录结构
- [ ] 编写 `control`, `rules`, `changelog` 文件
- [ ] 处理 Python 包依赖
- [ ] 构建 `.deb` 包

#### 1.3 Fedora/CentOS RPM 包
**优先级**: 低
- [ ] 创建 `.spec` 文件
- [ ] 适配 Fedora 包管理规范

#### 1.4 Flatpak 包 (跨发行版)
**优先级**: 中 (沙盒化，安全性好)
- [ ] 创建 Flatpak manifest
- [ ] 处理权限和沙盒限制
- [ ] 提交到 Flathub

---

### 2. CI/CD 自动化构建

#### 2.1 多平台构建流水线
```yaml
# .github/workflows/build.yml
name: Build Packages
on:
  release:
    types: [published]
jobs:
  build-arch:
    runs-on: ubuntu-latest
    steps:
      - name: Build AUR package
        run: makepkg -s
  build-debian:
    runs-on: ubuntu-latest
    steps:
      - name: Build Debian package
        run: dpkg-buildpackage -us -uc
  build-flatpak:
    runs-on: ubuntu-latest
    steps:
      - name: Build Flatpak
        run: flatpak-builder build-dir com.example.wallpaper-gui.json
```

#### 2.2 自动发布流程
- 标签推送时自动构建包
- 生成安装脚本
- 更新文档和下载链接

---

### 3. 性能监控工具 ✅ **已完成 (v0.9.2)**

#### 3.1 实现概览

**实现位置**: `py_GUI/core/performance.py`, `py_GUI/ui/pages/performance.py`, `py_GUI/ui/components/sparkline.py`

**功能特性**:
| 功能 | 描述 |
|------|------|
| 总览卡片 | Total CPU、Total Memory、Active Threads 三项核心指标 |
| 历史曲线图 | 基于 Cairo 的 Sparkline 组件，显示最近 60 秒数据 |
| 进程详情 | Frontend/Backend/Tray 三个进程独立监控 |
| **线程拆分** | (v0.9.2) 每个进程独立的 "Thread Details" 下拉抽屉，包含完整线程名 |
| **截图历史** | (v0.9.2) 记录最近 10 次截图的耗时、资源占用，并提供快速查看/清除功能 |
| 动态着色 | CPU 根据负载变色（绿<20%、橙<40%、红≥40%），内存蓝色 |
| 壁纸详情 | Backend 进程可展开显示各显示器壁纸缩略图、标题、ID |

#### 3.2 技术实现

**核心类**: `PerformanceMonitor`
- 使用 `psutil` 进行进程级监控
- 1 秒采样间隔，60 秒历史缓冲
- 缓存 `psutil.Process` 对象避免重复查找
- 自动识别真正的后端进程（跳过 bash wrapper）

**UI 组件**: `Sparkline`
- 纯 Cairo 绘制，无外部依赖
- 自适应缩放（最小 10%，最大 100%）
- 右对齐模式（数据不足 60 秒时从右侧开始绘制）
- 网格线和刻度标签

**监控能力**:
| 指标 | 方式 | 精度 |
|------|------|------|
| 后端进程 CPU 占用 | psutil | 进程级 |
| 后端进程内存使用 | psutil | 进程级 |
| 进程存活状态 | psutil | 实时 |
| 线程名称 | /proc/{pid}/task | 实时 |
| 当前壁纸信息 | config + wp_manager | 实时 |

**无法监控的（后端不提供API）**:
| 指标 | 原因 |
|------|------|
| 真实 FPS | 需要后端暴露渲染帧率 |
| 渲染性能细节 | OpenGL/渲染管线内部 |
| GPU 使用率 | 需要后端或系统级接口 |

#### 3.3 性能基准测试
- 建立 Performance Regression 测试
- 不同壁纸类型的性能基准
- 长时间运行性能衰减监控

---

### 4. 用户反馈收集机制

#### 4.1 应用内反馈功能
**实现位置**: `py_GUI/ui/components/feedback_dialog.py`

**功能设计**:
- 快速反馈按钮 (菜单栏)
- 自动收集系统信息
- 错误日志自动附加
- 匿名使用统计 (可选)

#### 4.2 GitHub Issues 模板
创建标准化的 Issue 模板:
- Bug 报告模板
- 功能请求模板
- 兼容性问题模板

#### 4.3 使用统计收集
**隐私友好设计**:
- 匿名统计，不收集个人信息
- 用户可选择退出
- 透明公开收集的数据类型

**统计数据**:
- Linux 发行版分布
- 桌面环境使用情况
- 壁纸类型使用频率
- 功能使用统计

---

## 🚧 尚缺功能开发计划

### 优先级 P1 (核心缺失)
- **暂无** - 核心功能已基本完成

---

### 优先级 P2 (功能缺失)
> **注**: 自定义资源支持已在 v0.8.1 完成，移出此列表

#### 0. 滚动条样式优化 ⚠️ **搁置/待调研**
**描述**：滚动条视觉呈现两层结构（疑似 trough + slider 分离显示），尝试隐藏 trough 未完全生效

**当前状态**：
- 已优化：透明度淡入淡出、细化宽度（3px）、半透明白色
- 未解决：GTK4/Adwaita 主题下 scrollbar 仍显示双层结构，CSS `background: transparent` 未完全覆盖默认样式

**下一步**：
- 调研 GTK4 scrollbar 完整 CSS 节点（scrollbar > range > trough > slider）
- 尝试 `all: unset` 或 `-gtk-icon-source: none` 等强制重置
- 考虑是否为 Adwaita 主题特有行为

#### 1. 自定义资源支持 ✅ **已完成 (v0.8.1)**
**功能描述**: `--assets-dir` 自定义 assets 目录路径

**实现需求**:
- ✅ 修改配置文件结构，支持自定义资源路径
- ✅ 更新 CLI 参数解析
- ✅ UI 中添加路径选择器
- ✅ 资源验证和错误处理

**实现细节**:
- 配置字段: `assetsPath` (默认 None，自动检测)
- UI 组件: Settings 页面路径输入框 + 浏览按钮
- 后端集成: Controller 中传递 `--assets-dir` 参数
- 验证机制: 目录存在性 + materials/shaders 子目录检查
- 用户反馈: Toast 通知显示验证结果

**完成工作量**: 2天
**提交记录**: 
- `c303829` - 基础支持 (CLI 参数 + 配置 + UI 选择器)
- `783f2b9` - 错误反馈 (Toast 通知系统)
- `6811922` - 即时验证 (保存后路径验证反馈)

**技术验证**: 
- 后端期望: `materials/`, `shaders/`, `effects/` 子目录
- 实现验证: 检查 `materials/` 和 `shaders/` 存在性
- 兼容性: 与 linux-wallpaperengine v2.3+ 完全兼容

#### 2. 动态壁纸预览优化
**功能描述**: GIF 预览仅显示首帧，需要实现动画预览
**如果gif的第一帧是黑色的，现在gui里也直接显示为黑色，没法预览**

**技术挑战**:
- 性能优化: 避免大量 GIF 同时播放卡顿
- 内存控制: 限制同时播放的动画数量
- 用户体验: 提供播放/暂停控制

**实现方案**:
```python
class AnimatedPreview:
    def __init__(self):
        self.active_animations = {}  # 限制同时播放数量
        self.animation_limit = 3
    
    def start_animation(self, wallpaper_id):
        if len(self.active_animations) < self.animation_limit:
            # 开始播放动画
            pass
        else:
            # 显示静态预览
            pass
```

**预期工作量**: 3-4天

#### 3. Wayland 专属优化
**功能描述**: `--fullscreen-pause-only-active` 等精细化控制

**技术要求**:
- 检测窗口焦点状态
- 实现智能暂停机制
- 优化 Wayland 环境下的资源使用

**预期工作量**: 4-5天

---

### 优先级 P2.5 (性能优化)

#### 1. 托盘进程 Go 重写
**功能描述**: 用 Go 重写系统托盘进程，大幅降低内存占用

**背景分析**:
- 当前 Python + GTK3 托盘进程占用 ~64MB RSS / ~26MB PSS
- 这是 Python 解释器 + GTK3 + AppIndicator 的固有开销
- 图标本身只有 7KB，与内存占用无关

**优化目标**:
| 指标 | 当前 (Python) | 目标 (Go) |
|------|---------------|-----------|
| RSS | ~64 MB | ~8-15 MB |
| PSS | ~26 MB | ~5-10 MB |
| 启动时间 | ~500ms | ~50ms |

**技术方案**:
- 使用 `github.com/getlantern/systray` 或 `fyne.io/systray` 库
- 编译为单一二进制文件，无运行时依赖
- 复用现有 CLI 通信方式 (`run_gui.py --show/--random/--stop/--quit`)
- 保持功能完全兼容

**实现内容**:
1. 创建 `tray_go/` 目录
2. 实现 Go 托盘程序 (~100 行代码)
3. 编译为 `wallpaper-tray` 二进制
4. 更新 `py_GUI/ui/tray.py` 调用新二进制
5. 保留 Python 版本作为 fallback

**菜单功能** (与 Python 版本一致):
- 显示窗口 (粗体，中键点击)
- 播放/停止 (检测后端运行状态)
- 随机切换壁纸
- 退出程序

**预期工作量**: 1-2 小时


##### 托盘实现方案对比
1. 接受现状（当前 Python + GTK3）
| 指标 | 值 |
|------|-----|
| 内存占用 | ~26 MB (PSS) / 64 MB (RSS) |
| 开发成本 | 零 |
| 维护成本 | 低 |
特点：
- ✅ 已经实现，代码成熟
- ✅ 与主程序共享 GTK 库（如果同时运行）
- ❌ Python 解释器开销不可避免
---
2. 用 Go 重写托盘进程
| 指标 | 预估值 |
|------|-----|
| 内存占用 | 3-8 MB |
| 开发成本 | 中等（1-2小时） |
| 维护成本 | 低 |
特点：
- ✅ 最省资源的可行方案
- ✅ 编译为单一二进制文件，无运行时依赖
- ✅ 使用 github.com/getlantern/systray 或 fyne.io/systray
- ✅ 启动速度极快（~50ms vs Python ~500ms）
- ❌ 需要 Go 开发环境
- ❌ 与主程序通信需要 IPC（可复用现有 CLI 方式）
示例代码结构：
// 约 80 行代码
func main() {
    systray.Run(onReady, onExit)
}
func onReady() {
    systray.SetIcon(icon)
    mShow := systray.AddMenuItem("显示窗口", "")
    go func() {
        for range mShow.ClickedCh {
            exec.Command("python3", "run_gui.py", "--show").Start()
        }
    }()
}
---
3. 用 C 重写托盘进程
| 指标 | 预估值 |
|------|-----|
| 内存占用 | 2-5 MB |
| 开发成本 | 高（2-4小时） |
| 维护成本 | 中 |
特点：
- ✅ 理论上最省内存
- ✅ 直接调用 libayatana-appindicator3
- ❌ 代码量大（~200 行）
- ❌ 需要处理 GLib 主循环、信号等
- ❌ 编译依赖管理麻烦
---
4. 合并托盘到主进程
| 指标 | 值 |
|------|-----|
| 内存占用 | 节省 ~15-20 MB（省去一个 Python 解释器） |
| 开发成本 | 低-中（需要处理 GTK3/GTK4 混用问题） |
| 维护成本 | 低 |
特点：
- ✅ 减少一个进程
- ❌ GTK 版本冲突：主程序用 GTK4，托盘用 GTK3（AppIndicator 只支持 GTK3）
- ❌ 如果主进程崩溃，托盘也消失
- ❌ 需要在同一进程中混用 GTK3 和 GTK4（技术上很难实现）
结论：由于 GTK 版本冲突，这个方案不推荐。
---
5. 换用 Qt 托盘
| 指标 | 预估值 |
|------|-----|
| 内存占用 | ~20-30 MB |
| 开发成本 | 中 |
| 维护成本 | 中 |
特点：
- ❌ 需要安装 PyQt5/6 依赖
- ❌ 内存占用与 GTK 差不多
- ❌ 增加项目依赖复杂度
- ✅ QSystemTrayIcon 更现代化
结论：没有明显优势，不推荐。
---
推荐排序
| 排名 | 方案 | 内存 | 推荐理由 |
|------|------|------|----------|
| 🥇 | Go 重写 | 3-8 MB | 最佳平衡：省内存、易开发、易维护 |
| 🥈 | 接受现状 | 26 MB | 零成本，现代系统无压力 |
| 🥉 | C 重写 | 2-5 MB | 最省但开发成本高 |
| ❌ | 合并到主进程 | - | GTK3/GTK4 冲突，不可行 |
| ❌ | Qt 托盘 | ~25 MB | 无明显优势 |
---



---

### 优先级 P3 (低频/复杂)

#### 1. 窗口模式支持
**功能描述**: `--window` (需 UI 支持自定义几何坐标)

**实现内容**:
- CLI 参数添加窗口选项
- UI 窗口大小和位置设置界面
- 窗口模式下的渲染优化
- 配置持久化

**预期工作量**: 5-6天

#### 2. 播放列表功能
**功能描述**: `--playlist` (需 UI 支持列表管理)

**功能设计**:
- 播放列表创建和编辑
- 多种播放模式 (顺序/随机/加权)
- 播放列表导入/导出
- 定时轮换与播放列表集成

**UI 组件设计**:
```python
class PlaylistManager:
    def __init__(self):
        self.playlists = {}
        self.current_playlist = None
        self.play_mode = "random"  # random, sequential, weighted
    
    def create_playlist(self, name, wallpaper_ids):
        """创建新播放列表"""
        pass
    
    def get_next_wallpaper(self):
        """获取下一个壁纸"""
        pass
```

**预期工作量**: 7-10天


#### 3.删除功能 ⚠️ **搁置/调研中**
**描述**：目前的右键壁纸删除功能仅仅能删除文件夹下的文件，启动steam联网后steam会自动下载回此前删除的壁纸
- **当前状态**：实现了本地文件删除。
- **遇到的问题**：Steam 会自动重新下载订阅的物品。
- **尝试的方案**：直接修改 `appworkshop_431960.acf` manifest 文件以移除订阅。
- **搁置原因**：直接修改 Steam manifest 文件存在风险（可能导致 Steam 库状态异常），且需要重启 Steam 才能生效。
- **下一步**：调研是否有更安全的方法（如 `steamcmd` 命令行工具或 Steam Web API）来以编程方式取消订阅 Workshop 物品。目前代码中保留了 manifest 修改逻辑但已注释。

#### 4.指令显示/复制 ✅ **已完成 (v0.8.2)**
**描述**：显示出应用当前壁纸时使用的指令，并且允许用户直接点击复制，相比于在logs里面显示的更加直观

**实现细节**:
- 在 "CURRENTLY USING" 壁纸标题旁边新增 📋 按钮
- 悬停按钮显示当前后端命令预览（截断至 80 字符）
- 点击按钮复制完整命令到剪贴板，Toast 提示"已复制"
- `WallpaperController` 新增 `get_current_command()` 方法

#### 5.显示大小 ✅ **已完成 (v0.8.2)**
**描述**：（在右侧栏）显示每个壁纸占用磁盘空间大小，方便用户把控

**实现细节**:
- 在 Folder ID 旁边显示绿色标签，格式如 "85.1 MB"
- 扫描时计算文件夹大小，无额外性能开销
- 新增 `format_size()` 和 `get_folder_size()` 工具函数

#### 6.排序方式 ✅ **已完成 (v0.8.2)**
**描述**：允许壁纸列表里不同的排序方式，如：文件大小，名称，载入顺序，订阅日期，最后更新时间等

**实现细节**:
- 工具栏新增 ⇅ 排序下拉菜单
- 支持 5 种排序：Title, Size ↓, Size ↑, Type, ID
- 排序选项自动保存到配置文件
- 注：订阅日期和更新时间因数据不可靠未实现

#### 7.多显示器指令优化 ❌ **不采用**
**描述**：YouTube 上有人使用多进程 + sleep 方式启动多显示器壁纸

**YouTube 方案**:
```bash
linux-wallpaperengine --silent --screen-root DP-1 11111111 &
sleep 1
linux-wallpaperengine --silent --screen-root HDMI-A-1 2222222 &
sleep 1
linux-wallpaperengine --silent --screen-root DP-2 333333 &
```

**当前方案**（单进程多参数）:
```bash
linux-wallpaperengine --screen-root DP-1 --bg 11111111 --screen-root HDMI-A-1 --bg 2222222 [全局参数]
```

**决定不采用的原因**:
1. **内存开销过大**：多进程方案 3 显示器 = 3 进程 = 600MB-1.2GB，单进程仅需 200-400MB
2. **当前方案是官方支持的用法**：linux-wallpaperengine 本身设计了 `--screen-root X --bg Y` 的单进程多屏语法
3. **YouTube 方案是 workaround**：可能是早期版本不支持单进程多屏时的变通办法
4. **进程管理复杂**：停止/随机切换时需要同步管理多个 PID

**结论**：维持现状，除非遇到启动竞争导致的黑屏问题再考虑

#### 8.托盘功能随机 ✅ **已修复 (v0.8.2)**
**描述**：gui窗口关闭时，使用托盘右键功能"随机切换壁纸"似乎会唤出gui窗口，这个逻辑似乎与正常用户逻辑不符

**修复细节**:
- 问题原因：应用初始化后 `_is_first_activation` 标志未重置为 `False`，导致后续 CLI 命令触发 `activate()` 时误判为"首次激活"并显示窗口
- 修复位置：`py_GUI/ui/app.py` 初始化完成后添加 `self._is_first_activation = False`

#### 9.标题栏 ✅ **已修复 (v0.8.2)**
**描述**：没有标题栏绘制，建议直接让系统默认绘制标题栏（niri、hyprland下不需要，kde下推荐使用ked插件wallpaper-engine-kde-plugin，但在别的环境下没有绘制的标题栏用户没法方便地最大化、最小化、关闭窗口）

**修复细节**:
- 使用 `Gtk.ApplicationWindow` 替代 `Adw.ApplicationWindow`
- 标题栏由窗口管理器决定（SSD 模式）
- niri/Hyprland 等平铺 WM 不显示标题栏
- GNOME/KDE 等传统桌面显示系统标题栏（含最大化/最小化/关闭按钮）

#### 10.RANDOM ✅ **已修复 (v0.8.2)**
**描述**：使用自动切换功能切换壁纸后wallpaper cycling的random的随机计时器应该重置（暂不清楚手动切换壁纸能否使random的计时器重置）总不能刚刚手动切完一个想要的壁纸然后就以为计时器时间到了就又被换掉了吧
**修复细节**:
- 在手动应用壁纸 (`on_action_apply`) 时强制调用 `setup_cycle_timer()`
- 这会重置定时器倒计时，确保用户手动选择壁纸后，会重新开始完整的计时周期，不会被即将到期的自动切换打断。

#### 11.顶栏 ✅ **已修复 (v0.8.2)**
~~**描述**：顶栏的“窗口选择器”，“Home”“Settings”这一栏三个按键胶囊的底下有一个统一绘制的黑框，但是这个黑框看起来并不美观，能不能去除（当然顶栏的第二排，搜索框，排列方式那一排底下也有黑框，但是这一排的底部黑框可以保留）~~
~~**修复细节**:~~
~~- 在 CSS 中为 `.nav-btn` 类添加 `box-shadow: none;` 和 `outline: none;`，移除了 GTK 默认绘制的阴影/边框效果。~~

似乎尚未生效，需要观察

#### 12.多显示器选择 ✅ **代码已就绪 (v0.8.5)**
**描述**：实现多屏幕壁纸同步（Same）和差异化（Diff）控制，以及灵活的多选功能。

**状态说明**:
- 功能代码已合并至 v0.8.5。
- **注意**：由于开发环境限制，多显示器物理渲染效果尚未在真机多屏环境下验证（待测试）。

**实现细节**:
- **Link/Unlink 开关**：顶栏新增 🔗 按钮（多屏时显示），切换 "Apply All" 和 "Apply Single" 模式。
- **高级选择抽屉**：侧边栏 Apply 按钮升级为 Split Button，下拉菜单支持勾选特定屏幕组合（满足 `2+1` 场景）。仅在屏幕>=3且为Diff模式时显示。
- **后端支持**：Controller 新增 `screens` 参数支持批量应用。后端指令逻辑遵循 P3-7 单进程多屏模式。

#### 13.预览图 ✅ **已完成 (v0.8.6)**
**描述**：解决 GIF 壁纸预览图全黑问题，并提供动态预览。

**实现细节**:
- **智能缩略图 (P3-13)**：使用 Pillow 自动提取 GIF 第 15 帧（或 20% 处）作为静态封面，避开开头黑屏。
- **动态详情图 (P2-2)**：在侧边栏选中 GIF 时，直接播放原图动画。
- **高质量缩放**：采用 LANCZOS 算法生成清晰缩略图。

#### 14.总数显示 ✅ **已完成 (v0.8.3)**
**描述**：在顶栏"CURRENTLY USING"右侧显示壁纸序号/总数（N/M）

**实现细节**:
- 在"CURRENTLY USING"标题行右侧添加计数器标签
- 显示格式：N/M（当前壁纸在过滤列表中的序号/总数）
- 使用与壁纸名字相同的样式（`status-value` CSS class）
- 自动更新场景：壁纸变化、屏幕切换、搜索/排序/重新加载

#### 15.Wayland 高级控制 (P3-15) ✅ **已完成 (v0.8.10)**
**描述**：支持 Wayland 特有的暂停策略控制。
- `--fullscreen-pause-only-active`: 仅当全屏窗口处于活动状态时暂停。
- `--fullscreen-pause-ignore-appid`: 忽略特定应用程序（如 Dock、Bar）的全屏状态判定。

**实现细节**:
- 设置页面新增 "Wayland Tweaks" 区域，自动检测会话类型。
- 提供 Switch 和 Entry 控件，非 Wayland 环境自动禁用。
- 后端 Controller 读取配置并动态追加参数。

#### 16.壁纸属性自定义 (P2-3)
**描述**：支持修改壁纸的自定义属性（如颜色、速度、特效开关）。
- 解析 `linux-wallpaperengine --list-properties` 的输出。
- 动态生成设置表单（Slider, Color Picker, Checkbox）。
- 应用时传递 `--set-property key=value`。

#### 17.窗口化预览 (P3-16)
**描述**：利用 `--window` 参数提供独立的壁纸预览窗口，无需直接应用到桌面即可查看动态效果。

#### 18.性能卡顿分析 🔍
##### 问题现象
- 初次切换 grid ↔ list：2-3 秒卡顿
- 后续切换：正常响应
根本原因（确定）
##### 1. 双重过滤调用 ⚠️ 主要原因
###### 第1次过滤（第748行）
def refresh_wallpaper_grid(self):
    self._current_wp_ids = list(self.filter_wallpapers().keys())  # ← 第1次
    ...
    self.populate_grid()  # 或 populate_list()
###### 第2次过滤（第815行/第827行）
def populate_grid(self):
    filtered = self.filter_wallpapers()  # ← 第2次
    for folder_id, wp in filtered.items():
        card = self.create_grid_item(...)
每次切换都调用 filter_wallpapers() 两次，包括：
- 遍历所有壁纸并转换为小写
- 排序整个列表（O(n log n)）
假设有 500+ 个壁纸，这就是 1000+ 次字符串转换 + 两次排序。
---
##### 2. 同步图像加载 ⚠️ 次要原因，累积效应
create_grid_item() 和 create_list_item() 中：
###### 第869行（grid）和第942行（list）
texture = self.wp_manager.get_texture(wp["preview"], 170)
- Grid 模式：170×170px，如果有 100 个壁纸 = 100 次图像加载
- List 模式：100×100px，加载较小但仍需 I/O
虽然有 LRU 缓存，但初次切换时缓存是冷的（第一次加载 grid 时缓存了 170×170，切到 list 时需要 100×100 的新尺寸 = 缓存 miss）。
---
##### 3. 为什么第一次慢，后续快？
| 操作 | 第1次切换 | 第2次切换 |
|------|---------|---------|
| 过滤 | 2次过滤 | 2次过滤（已排序，可优化但此次仍执行） |
| 缓存 | 冷缓存（0 条项） | 热缓存（已有 100+ 条） |
| 图像 I/O | 100+ 次磁盘读取 | 0 次（全部缓存命中） |
| GTK 布局 | 第一次渲染，可能堆积任务 | GTK 内部状态已热 |
关键：图像缓存是全局的，一旦加载过就永久保存。
---
哪个函数最耗时？
基于代码复杂度：
| 函数 | 耗时 | 原因 |
|------|------|------|
| filter_wallpapers() | 中等 | 两次排序 + 字符串转换 |
| get_texture() | 最高 | 同步 I/O + 图像解码（GIF 尤其慢） |
| populate_grid/list() | 低-中等 | 循环创建 GTK 对象，但 GTK 对象本身不贵 |
| GTK 布局计算 | 未知 | 可能在后台累积，但应该是异步 |
排序：get_texture() > filter_wallpapers() > populate_x()
---
GIF 处理额外成本
如果壁纸包含 GIF，get_texture() 中：
if path.lower().endswith('.gif'):
    # PIL Image.open() + seek(15) + convert("RGBA") + thumbnail() + save to PNG + PixbufLoader.write()
这是最重的操作。如果有 20-30 个 GIF 壁纸，就能解释 2-3 秒的延迟。
---
为什么 GTK 布局不是主要原因
- GTK4 FlowBox/ListBox 的 append() 应该是异步的
- 布局计算一般被推迟到下一个主循环迭代
- 但如果有 100+ 个复杂 widget，仍可能影响首帧延迟
---
##### 总结
初次切换 grid→list 的 2-3 秒延迟由以下累积：
1. filter_wallpapers() 被调用 2 次（冗余）
   → 遍历 500+ 壁纸、转小写、排序
2. get_texture() 缓存冷启动
   → 需要加载 100+ 张图（特别是 GIF 的解码很慢）
3. 可能的 GTK 布局堆积
   → 100+ 新 widget 加入容器，布局计算延迟
后续切换快的原因：
  - 图像已全部缓存在内存中 → get_texture() 返回秒级
  - filter_wallpapers() 仍被调用 2 次，但成本低（数据在内存，不涉及 I/O）

性能优化方案 🚀
方案 A: 消除冗余过滤（高优先级） ⭐⭐⭐
问题：filter_wallpapers() 在 refresh_wallpaper_grid() 和 populate_grid/list() 中各调用一次
解决方案：
1. 在 refresh_wallpaper_grid() 中计算一次过滤结果
2. 将结果存储为实例变量（如 self._filtered_wallpapers）
3. populate_grid/list() 直接使用该缓存，不再重复过滤
4. 其他地方如果需要过滤结果，也使用同一份缓存
收益：
- 消除 50% 的排序操作（从 2 次 → 1 次）
- 消除重复的字符串转换和迭代
- 对于 500+ 壁纸库，估计减少 0.5-1 秒 延迟
实现成本：低（改 3-4 处代码）
---
方案 B: 异步图像加载（中优先级） ⭐⭐
问题：get_texture() 是同步调用，在 create_grid_item/list_item() 中阻塞 UI 线程
解决方案：
1. 改进 populate_grid/list() 使用分批加载：
   - 先创建所有 widget，先用占位符（空白或文字）
   - 通过 GLib.idle_add() 或 GLib.timeout_add() 分批加载图像
   - 后台线程（ThreadPool）加载图像，加载完成后更新 UI
2. 或者用"懒加载"策略：
   - 只加载可见区域（Viewport）的图像
   - 使用 ScrolledWindow 的滚动事件监听
   - 动态加载/卸载图像纹理
收益：
- UI 线程不被阻塞，响应立即
- 用户看到快速的"骨架屏" → 逐步加载图像的体验
- 如果用户不滚动到下面的图，不浪费时间加载
- 估计减少 1-2 秒 感知延迟
实现成本：中等（需要线程管理、UI 更新同步）
---
方案 C: 缓存预热（低优先级） ⭐
问题：第一次切换时图像缓存冷启动
解决方案：
1. 在应用启动时，后台预加载第一批（如前 50 个）常见尺寸的图像
2. 或者在用户切换视图时，提前加载对方视图的图像（预测性加载）
收益：
- 如果用户经常在 grid ↔ list 间切换，第二次以后的切换会更快
- 估计减少 0.3-0.5 秒（取决于预加载批次大小）
实现成本：低-中等（需要后台任务调度）
---
方案 D: 优化 GIF 处理（中优先级） ⭐⭐
问题：GIF 解码（PIL convert("RGBA") + thumbnail()）是最耗时操作
解决方案：
1. 检测 GIF 的实际帧率和复杂度，使用更激进的缩放
2. 用 Image.NEAREST 而不是 Image.Resampling.LANCZOS 加快缩放
3. 预先将常用 GIF 转换为 WebP/PNG，减少运行时解码
4. 限制一次加载的 GIF 数量（如果库里 GIF 太多）
收益：
- 如果库里有大量 GIF，可减少 0.5-1 秒
- 对纯视频/静态图库影响小
实现成本：低-中等
---
方案 E: 分离视图容器（高优先级） ⭐⭐⭐
问题：每次切换时，set_child() 在同一个 ScrolledWindow 中交换 FlowBox/ListBox，可能导致 GTK 重新布局
解决方案：
1. 预先创建两个 ScrolledWindow（一个用于 grid，一个用于 list）
2. 切换时只改变可见性（set_visible()），不是 set_child()
3. 两个容器同时接收 populate_grid/list() 的更新，保持同步
收益：
- 消除 GTK 布局重排的成本
- 视图间切换变成纯 CSS 可见性切换
- 估计减少 0.2-0.5 秒
实现成本：低-中等（需要修改 build_ui() 和切换逻辑）
---
推荐实施顺序
| 优先级 | 方案 | 预期收益 | 成本 | 实施难度 |
|------|------|--------|------|--------|
| 1 | A（消除冗余过滤） | 0.5-1s | 低 | 简单 |
| 2 | E（分离视图容器） | 0.2-0.5s | 低-中 | 简单 |
| 3 | B（异步加载） | 1-2s | 中 | 中等 |
| 4 | D（GIF 优化） | 0.5-1s（条件） | 低-中 | 简单 |
| 5 | C（缓存预热） | 0.3-0.5s | 低 | 简单 |
快速方案（5 分钟）：实施 A + E → 预期改善 0.7-1.5 秒
终极方案（1 小时）：实施 A + E + B → 预期改善 1.7-3 秒 + 响应性大幅提升

---

## 📅 实施时间表

### 第一阶段 (Week 1-2): 测试基础建设
- [x] 项目现状分析
- [x] 自定义资源支持实现 (v0.8.1) - 移出 P2 列表
- [ ] 测试框架搭建
- [ ] 核心类单元测试
- [ ] 虚拟显示器环境配置

### 第二阶段 (Week 3-4): 视觉测试实现
- [ ] 壁纸显示自动化验证
- [ ] 多显示器测试
- [ ] 性能基准测试
- [ ] 兼容性测试

### 第三阶段 (Week 5-6): 发布准备
- [ ] AUR 包创建和提交
- [ ] Debian 包构建
- [ ] CI/CD 流水线设置
- [ ] 文档完善

### 第四阶段 (Week 7-8): 功能完善
- [ ] P2 优先级功能开发
- [ ] 用户反馈机制实现
- [ ] 性能监控工具
- [ ] 社区反馈收集

### 第五阶段 (Week 9+): 长期维护
- [ ] P3 优先级功能 (按需)
- [ ] 社区贡献管理
- [ ] 版本迭代规划

---

## 🎯 成功指标

### 测试覆盖率目标
- 单元测试覆盖率: > 80%
- 集成测试覆盖率: > 70%
- 视觉测试成功率: > 95%

### 发布目标
- AUR 包成功发布并维护
- 至少 2 个 Linux 发行版包可用
- CI/CD 自动化覆盖率 100%
- 用户反馈收集机制运行良好

### 用户体验目标
- 新用户 5 分钟内完成安装和使用
- 壁纸加载时间 < 5 秒
- 应用启动时间 < 3 秒
- 内存占用 < 300MB

---

## 📝 备注

1. **测试优先**: 在开发新功能前，先建立完善的测试体系
2. **渐进发布**: 先建立基础发布渠道，再逐步完善
3. **社区驱动**: 重视用户反馈，基于实际需求调整优先级
4. **文档同步**: 每个功能都要有对应的用户文档
5. **质量第一**: 宁可功能少而精，不要功能多而乱

---

**最后更新**: 2026-02-15 (发布 v0.10.6)  
**负责人**: 开发团队  
**审核状态**: 待审核
```

---

### 📄 文件: `build_appimage.sh`

```bash
#!/bin/bash
set -e

# ================= 配置区 =================
APP_NAME="linux-wallpaperengine-gui"
# 获取当前 Python 版本 (例如 3.10)
PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

# 从 pyproject.toml 自动提取版本号
if [ -f "pyproject.toml" ]; then
    VERSION=$(grep '^version[[:space:]]*=' pyproject.toml | head -n 1 | cut -d'"' -f2 | cut -d"'" -f2)
else
    VERSION="unknown"
fi
echo "📌 检测到当前版本号: v$VERSION"
# ==========================================

# 1. 检查本地工具是否存在
if [ ! -f "./linuxdeploy-x86_64.AppImage" ] || [ ! -f "./linuxdeploy-plugin-gtk.sh" ]; then
    echo "❌ 错误: 找不到构建工具！"
    echo "请先在当前目录下载 'linuxdeploy-x86_64.AppImage' 和 'linuxdeploy-plugin-gtk.sh' 并赋予执行权限。"
    exit 1
fi

# 2. 准备 AppDir 目录
echo "📂 清理并创建 AppDir..."
rm -rf AppDir
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/512x512/apps
mkdir -p AppDir/usr/share/linux-wallpaperengine-gui
# 创建专门存放 Python 依赖的目录
mkdir -p AppDir/usr/lib/python${PY_VER}/site-packages

# 3. 复制 Python 源码
echo "📦 正在复制源码..."
if [ -d "src/py_GUI" ]; then
    cp -r src/py_GUI src/pic src/run_gui.py AppDir/usr/share/linux-wallpaperengine-gui/
elif [ -d "py_GUI" ]; then
    cp -r py_GUI pic run_gui.py AppDir/usr/share/linux-wallpaperengine-gui/
else
    echo "❌ 找不到源码目录，请检查路径！"
    exit 1
fi

# ✅ 新增：清理可能残留在旧目录的幽灵文件！
rm -f AppDir/usr/share/linux-wallpaperengine-gui/tray-rs-bin

# ✅ 新增：现场编译 Rust 托盘并放入系统标准可执行目录
echo "🦀 正在现场编译 Rust 托盘引擎..."
cd tray_rs
if ! cargo build --release; then
    echo "❌ 致命错误: Rust 托盘引擎编译失败，请检查 Rust 环境或报错信息。"
    exit 1
fi
cd ..

if [ ! -f "tray_rs/target/release/tray-rs" ]; then
    echo "❌ 致命错误: 未找到已编译的托盘二进制文件。"
    exit 1
fi

# 将拷贝目标从 usr/share/... 改为 usr/bin/
cp tray_rs/target/release/tray-rs AppDir/usr/bin/tray-rs-bin
chmod +x AppDir/usr/bin/tray-rs-bin

# 【核弹级清理】彻底铲除所有 __pycache__ 和 .pyc，防止旧字节码污染 AppImage
echo "🧹 清除 Python 缓存幽灵..."
find AppDir -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find AppDir -name "*.pyc" -delete 2>/dev/null || true

# 4. 安装 Python 依赖到 AppDir 内部
echo "🐍 正在安装 Python 依赖..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt --target=AppDir/usr/lib/python${PY_VER}/site-packages --upgrade
else
    echo "⚠️ 警告: 没有找到 requirements.txt，只打包源码。"
fi

# 5. 【关键修补】强制植入托盘所需的 GTK3 和 Ayatana 依赖
echo "🔧 手动修补：植入托盘所需的 GTK3 和 Ayatana 依赖..."
mkdir -p AppDir/usr/lib/girepository-1.0

# # 拷贝 typelib 让 Python 能够 import 它们 (加 || true 防止 set -e 导致脚本意外中断)
# cp /usr/lib/girepository-1.0/Gtk-3.0.typelib AppDir/usr/lib/girepository-1.0/ 2>/dev/null || echo "⚠️ 未找到 GTK3 typelib"
# cp /usr/lib/girepository-1.0/Gdk-3.0.typelib AppDir/usr/lib/girepository-1.0/ 2>/dev/null || true
# cp /usr/lib/girepository-1.0/AyatanaAppIndicator3-0.1.typelib AppDir/usr/lib/girepository-1.0/ 2>/dev/null || echo "⚠️ 未找到 Ayatana typelib"

# # 拷贝底层的 Ayatana C语言动态库
# cp /usr/lib/libayatana-appindicator3.so* AppDir/usr/lib/ 2>/dev/null || echo "⚠️ 未找到 libayatana-appindicator3.so"

# 6. 【终极绝杀】将图标 Base64 内嵌进 Python 模块，彻底绕开 FUSE 路径问题
echo "🔐 正在将图标转码为 Python 内存数据..."
ICON_TO_EMBED="AppDir/usr/share/linux-wallpaperengine-gui/pic/icons/GUI_rounded.png"
EMBED_TARGET="AppDir/usr/share/linux-wallpaperengine-gui/py_GUI/embedded_icon.py"

python3 - <<PYEOF
import base64
try:
    with open("${ICON_TO_EMBED}", "rb") as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    with open("${EMBED_TARGET}", "w") as f:
        f.write("# Auto-generated at build time. DO NOT EDIT.\n")
        f.write("ICON_DATA = b\"\"\"" + data + "\"\"\"\n")
    print("✅ 图标 Base64 内嵌成功！")
except Exception as e:
    print(f"❌ 图标内嵌失败: {e}")
PYEOF

# 7. 创建启动 Wrapper
echo "📝 创建启动脚本..."
cat > AppDir/usr/bin/launch_gui <<'EOF'
#!/bin/bash

# 1. 确定 APPDIR 挂载点
if [ -z "$APPDIR" ]; then
    SCRIPT_REAL="$(readlink -f "${0}")"
    export APPDIR="$(dirname "$(dirname "$(dirname "$SCRIPT_REAL")")")"
fi

# ╔═════════════════════════════════════════════════════════════╗
# ║  在 FUSE 挂载还 100% 存活时，提前把 Rust 二进制复制到 /tmp  ║
# ║  这是唯一能绕过 FUSE 挂载点在 Python 启动后可能被回收的方法 ║
# ╚═════════════════════════════════════════════════════════════╝
TRAY_SRC="$APPDIR/usr/bin/tray-rs-bin"
TRAY_DEST="/tmp/lwg-tray-rs-$(id -u)"

if [ -f "$TRAY_SRC" ]; then
    # 只有当目标不存在，或者 AppImage 里的源文件更新时才复制
    if [ ! -f "$TRAY_DEST" ] || [ "$TRAY_SRC" -nt "$TRAY_DEST" ]; then
        cp "$TRAY_SRC" "$TRAY_DEST" && chmod 755 "$TRAY_DEST"
    fi
    # 导出一个显式的环境变量，供 Python 直接使用
    export LWG_TRAY_BIN="$TRAY_DEST"
else
    echo "[launch_gui] WARNING: tray-rs-bin not found at $TRAY_SRC" >&2
fi

# 2. 设置标准环境变量
export PATH="$APPDIR/usr/bin:$PATH"
export PYTHONPATH="$APPDIR/usr/lib/python__PY_VER__/site-packages:$APPDIR/usr/share/linux-wallpaperengine-gui:$PYTHONPATH"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="/tmp/lwg-pycache-$(id -u)"

export LWG_IPC_SOCKET="lwg-ipc-$(id -u)"

cd "$APPDIR/usr/share/linux-wallpaperengine-gui"
exec python3 run_gui.py "$@"
EOF

# 替换版本号并赋予权限
sed -i "s/__PY_VER__/${PY_VER}/g" AppDir/usr/bin/launch_gui
chmod +x AppDir/usr/bin/launch_gui

# 8. 配置桌面文件
echo "🖼️ 处理图标 (缩放至 512x512)..."
ICON_DIR="AppDir/usr/share/icons/hicolor/512x512/apps"
mkdir -p "$ICON_DIR"
SOURCE_ICON="AppDir/usr/share/linux-wallpaperengine-gui/pic/icons/GUI_rounded.png"
TARGET_ICON="$ICON_DIR/${APP_NAME}.png"

if command -v ffmpeg >/dev/null; then
    ffmpeg -y -i "$SOURCE_ICON" -vf scale=512:512 "$TARGET_ICON" >/dev/null 2>&1
elif command -v convert >/dev/null; then
    convert "$SOURCE_ICON" -resize 512x512 "$TARGET_ICON"
else
    echo "⚠️ 警告: 没找到 ffmpeg 或 convert，无法缩放图标！"
    cp "$SOURCE_ICON" "$TARGET_ICON"
fi

echo "📦 植入托盘专用小图标..."
# 源文件路径
TRAY_SRC_SMALL="AppDir/usr/share/linux-wallpaperengine-gui/pic/icons/gui_tray_rounded.png"
TRAY_STOPPED_SMALL="AppDir/usr/share/linux-wallpaperengine-gui/pic/icons/gui_tray_rounded-stopped.png"

# 目标文件名 (注意命名要和 Python 代码里的逻辑一致)
cp "$TRAY_SRC_SMALL" "$ICON_DIR/com.wallpaperengine.tray.png"
cp "$TRAY_STOPPED_SMALL" "$ICON_DIR/com.wallpaperengine.tray-stopped.png"

# 满足 AppImage 根目录规范
cp "$TARGET_ICON" AppDir/${APP_NAME}.png
cp "$TARGET_ICON" AppDir/.DirIcon

cat > AppDir/usr/share/applications/${APP_NAME}.desktop <<EOF
[Desktop Entry]
Name=Wallpaper Engine GUI
Exec=launch_gui %U
Icon=${APP_NAME}
Type=Application
Categories=Utility;GTK;
StartupWMClass=com.wallpaperengine.gui
Terminal=false
EOF

# 9. 开始打包
echo "🚀 开始生成 AppImage..."
# export LINUXDEPLOY_PLUGIN_GTK_MODULES="canberra-gtk-module:canberra-gtk-module"
unset LINUXDEPLOY_PLUGIN_GTK_MODULES
export NO_STRIP=true
export DEPLOY_GTK_VERSION=4

# 通过环境变量 OUTPUT 强制规范 AppImage 的输出文件名
export OUTPUT="${APP_NAME}-${VERSION}-x86_64.AppImage"

ln -sf usr/bin/launch_gui AppDir/AppRun

# ... 前面的代码保持不变 ...

# ✅ 打包前验尸：确认文件真的进去了
echo "================= 打包前极度硬核验尸 ================="
ls -la AppDir/usr/bin/tray-rs-bin || echo "❌ 打包前就丢了！"

./linuxdeploy-x86_64.AppImage \
    --appdir AppDir \
    --plugin gtk \
    --desktop-file AppDir/usr/share/applications/${APP_NAME}.desktop \
    --icon-file "$TARGET_ICON" \
    --output appimage

# ✅ 打包后验尸：确认没有被 GTK 插件偷删
echo "================= 打包后极度硬核验尸 ================="
ls -la AppDir/usr/bin/tray-rs-bin 2>&1 || echo "❌ 卧槽！文件在打包后被 GTK 插件吃掉了！"

echo "✅ 打包完成！文件已生成: ${OUTPUT}"
```

---

### 📄 文件: `folder.py`

```python
import os
from pathlib import Path
from datetime import datetime

# ================= 配置区域 =================

# 1. 忽略的文件夹名称 (目录)
IGNORE_DIRS = {
    '.git', 
    '.github', 
    '.sisyphus', 
    'target',        # Rust 构建目录
    '__pycache__', 
    'node_modules', 
    'venv', 
    'env',
    '.vscode',       
    '.idea',         
    'dist',          
    'build',
    'docs'           # <--- 新增：忽略整个 docs 文件夹
}

# 2. 忽略的特定文件名 (文件)
IGNORE_FILES = {
    '.gitignore',
    'LICENSE',
    'PKGBUILD',      # <--- 新增：忽略 Arch Linux 打包脚本
    'Makefile',      # 可选：如果你也不想抓取 Makefile
    'README.md'      # 可选：通常 README 会在开头看，不需要在详细内容里再重复一遍，不需要可删除此行
}

# 输出文件名和脚本自身名称
OUTPUT_FILENAME = "project_export.md"
SCRIPT_FILENAME = "folder_to_markdown.py"
# ===========================================

def generate_ascii_tree(start_path, prefix=""):
    """
    递归生成 ASCII 树形结构字符串
    """
    tree_str = ""
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        return f"{prefix}[权限拒绝]\n"
    except Exception:
        return ""

    filtered_entries = []
    for e in entries:
        # 排除输出文件和脚本本身
        if e in [OUTPUT_FILENAME, SCRIPT_FILENAME]:
            continue
        
        full_path = os.path.join(start_path, e)
        
        # 排除 IGNORE_DIRS 中的文件夹
        if os.path.isdir(full_path) and e in IGNORE_DIRS:
            continue
            
        # 排除 IGNORE_FILES 中的特定文件
        if os.path.isfile(full_path) and e in IGNORE_FILES:
            continue
            
        filtered_entries.append(e)

    for i, entry in enumerate(filtered_entries):
        full_path = os.path.join(start_path, entry)
        is_last = (i == len(filtered_entries) - 1)
        
        connector = "└── " if is_last else "├── "
        tree_str += f"{prefix}{connector}{entry}"
        
        if os.path.isdir(full_path):
            tree_str += "/\n"
            extension = "    " if is_last else "│   "
            tree_str += generate_ascii_tree(full_path, prefix + extension)
        else:
            tree_str += "\n"
            
    return tree_str

def get_file_content(file_path):
    """
    读取文件内容，处理编码问题和大文件
    """
    try:
        if os.path.getsize(file_path) > 5 * 1024 * 1024:
            return "[文件过大 (>5MB)，已跳过读取]"
    except OSError:
        pass

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                return f.read()
        except Exception:
            return "[无法读取：可能是二进制文件或编码不支持]"
    except Exception as e:
        return f"[读取错误: {str(e)}]"

def should_ignore_file(file_path, ignore_dirs_set, ignore_files_set):
    """
    检查文件路径是否应该被忽略
    """
    # 检查路径中的文件夹部分
    for part in file_path.parts:
        if part in ignore_dirs_set:
            return True
    
    # 检查文件名本身
    if file_path.name in ignore_files_set:
        return True
        
    return False

def main():
    root_dir = Path('.')
    
    print(f"🚀 开始扫描 Rust 项目: {root_dir.absolute()}")
    print(f"🚫 忽略的文件夹: {', '.join(sorted(IGNORE_DIRS))}")
    print(f"🚫 忽略的文件: {', '.join(sorted(IGNORE_FILES))}")
    
    md_content = []
    
    # 1. 生成标题
    md_content.append("# 项目结构与文件内容导出 (Rust Project)\n\n")
    md_content.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md_content.append(f"**根目录**: `{root_dir.absolute()}`\n")
    md_content.append("---\n\n")
    
    # 2. 生成 ASCII 树形图
    md_content.append("## 📂 项目结构图\n\n")
    md_content.append("```text\n")
    md_content.append(f"{root_dir.name}/\n")
    tree_art = generate_ascii_tree(str(root_dir))
    md_content.append(tree_art)
    md_content.append("```\n\n")
    md_content.append("---\n\n")
    
    # 3. 递归抓取文件内容
    md_content.append("## 📄 文件详细内容\n\n")
    
    files_to_process = []
    
    print("🔍 正在遍历文件...")
    for f in root_dir.rglob('*'):
        if not f.is_file():
            continue
            
        if f.name in [OUTPUT_FILENAME, SCRIPT_FILENAME]:
            continue
            
        if should_ignore_file(f, IGNORE_DIRS, IGNORE_FILES):
            continue
            
        files_to_process.append(f)
    
    files_to_process.sort(key=lambda x: str(x))
    
    print(f"✅ 找到 {len(files_to_process)} 个有效文件，开始写入内容...")
    
    for idx, file_path in enumerate(files_to_process):
        rel_path = file_path.relative_to(root_dir)
        
        if (idx + 1) % 50 == 0:
            print(f"   处理中: {idx + 1}/{len(files_to_process)} ...")
        
        md_content.append(f"### 📄 文件: `{rel_path}`\n\n")
        
        content = get_file_content(str(file_path))
        
        suffix = file_path.suffix.lower()
        lang_map = {
            '.rs': 'rust',
            '.toml': 'toml',
            '.lock': 'toml',
            '.md': 'markdown',
            '.txt': 'text',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.sh': 'bash',
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.sql': 'sql',
            '.xml': 'xml',
            '.ini': 'ini',
            '.cfg': 'ini',
            '.env': 'bash',
        }
        lang = lang_map.get(suffix, '') 
        
        md_content.append(f"```{lang}\n{content}\n```\n\n")
        md_content.append("---\n\n")

    # 4. 写入文件
    print("💾 正在保存文件...")
    try:
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write("".join(md_content))
        print(f"🎉 完成！所有内容已保存到: {OUTPUT_FILENAME}")
        print(f"📊 总共处理了 {len(files_to_process)} 个文件。")
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")

if __name__ == "__main__":
    main()
```

---

### 📄 文件: `linuxdeploy-plugin-gtk.sh`

```bash
#! /usr/bin/env bash

# GTK3 environment variables: https://developer.gnome.org/gtk3/stable/gtk-running.html
# GTK4 environment variables: https://developer.gnome.org/gtk4/stable/gtk-running.html

# abort on all errors
set -e

if [ "$DEBUG" != "" ]; then
    set -x
    verbose="--verbose"
fi

SCRIPT="$(basename "$(readlink -f "$0")")"

show_usage() {
    echo "Usage: $SCRIPT --appdir <path to AppDir>"
    echo
    echo "Bundles resources for applications that use GTK into an AppDir"
    echo
    echo "Required variables:"
    echo "  LINUXDEPLOY=\".../linuxdeploy\" path to linuxdeploy (e.g., AppImage); set automatically when plugin is run directly by linuxdeploy"
    echo
    echo "Optional variables:"
    echo "  DEPLOY_GTK_VERSION (major version of GTK to deploy, e.g. '2', '3' or '4'; auto-detect by default)"
}

variable_is_true() {
    local var="$1"

    if [ -n "$var" ] && { [ "$var" == "true" ] || [ "$var" -gt 0 ]; } 2> /dev/null; then
        return 0 # true
    else
        return 1 # false
    fi
}

get_pkgconf_variable() {
    local variable="$1"
    local library="$2"
    local default_value="$3"

    pkgconfig_ret="$("$PKG_CONFIG" --variable="$variable" "$library")"
    if [ -n "$pkgconfig_ret" ]; then
        echo "$pkgconfig_ret"
    elif [ -n "$default_value" ]; then
        echo "$default_value"
    else
        echo "$0: there is no '$variable' variable for '$library' library." > /dev/stderr
        echo "Please check the '$library.pc' file is present in \$PKG_CONFIG_PATH (you may need to install the appropriate -dev/-devel package)." > /dev/stderr
        exit 1
    fi
}

copy_tree() {
    local src=("${@:1:$#-1}")
    local dst="${*:$#}"

    for elem in "${src[@]}"; do
        mkdir -p "${dst::-1}$elem"
        cp "$elem" --archive --parents --target-directory="$dst" $verbose
    done
}

copy_lib_tree() {
    # The source lib directory could be /usr/lib, /usr/lib64, or /usr/lib/x86_64-linux-gnu
    # Therefore, when copying lib directories, we need to transform that target path
    # to a consistent /usr/lib
    local src=("${@:1:$#-1}")
    local dst="${*:$#}"

    for elem in "${src[@]}"; do
        mkdir -p "${dst::-1}${elem/$LD_GTK_LIBRARY_PATH//usr/lib}"
        pushd "$LD_GTK_LIBRARY_PATH"
        cp "$(realpath --relative-to="$LD_GTK_LIBRARY_PATH" "$elem")" --archive --parents --target-directory="$dst/usr/lib" $verbose
        popd
    done
}

get_triplet_path() {
    if command -v dpkg-architecture > /dev/null; then
        echo "/usr/lib/$(dpkg-architecture -qDEB_HOST_MULTIARCH)"
    fi
}



search_library_path() {
    PATH_ARRAY=(
        "$(get_triplet_path)"
        "/usr/lib64"
        "/usr/lib"
    )

    for path in "${PATH_ARRAY[@]}"; do
        if [ -d "$path" ]; then
            echo "$path"
            return 0
        fi
    done
}

search_tool() {
    local tool="$1"
    local directory="$2"

    if command -v "$tool"; then
        return 0
    fi

    PATH_ARRAY=(
        "$(get_triplet_path)/$directory/$tool"
        "/usr/lib64/$directory/$tool"
        "/usr/lib/$directory/$tool"
        "/usr/bin/$tool"
        "/usr/bin/$tool-64"
        "/usr/bin/$tool-32"
    )

    for path in "${PATH_ARRAY[@]}"; do
        if [ -x "$path" ]; then
            echo "$path"
            return 0
        fi
    done
}

DEPLOY_GTK_VERSION="${DEPLOY_GTK_VERSION:-0}" # When not set by user, this variable use the integer '0' as a sentinel value
APPDIR=

while [ "$1" != "" ]; do
    case "$1" in
        --plugin-api-version)
            echo "0"
            exit 0
            ;;
        --appdir)
            APPDIR="$2"
            shift
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            echo "Invalid argument: $1"
            echo
            show_usage
            exit 1
            ;;
    esac
done

if [ "$APPDIR" == "" ]; then
    show_usage
    exit 1
fi

APPDIR="$(realpath "$APPDIR")"
mkdir -p "$APPDIR"

. /etc/os-release
if [ "$ID" = "debian" ] || [ "$ID" = "ubuntu" ]; then
    if ! command -v dpkg-architecture  &>/dev/null; then
        echo -e "$0: dpkg-architecture not found.\nInstall dpkg-dev then re-run the plugin."
        exit 1
    fi
fi

if command -v pkgconf > /dev/null; then
    PKG_CONFIG="pkgconf"
elif command -v pkg-config > /dev/null; then
    PKG_CONFIG="pkg-config"
else
    echo "$0: pkg-config/pkgconf not found in PATH, aborting"
    exit 1
fi

# GTK's library path *must not* have a trailing slash for later parameter substitution to work properly
LD_GTK_LIBRARY_PATH="$(realpath "${LD_GTK_LIBRARY_PATH:-$(search_library_path)}")"

if ! command -v find &>/dev/null && ! type find &>/dev/null; then
    echo -e "$0: find not found.\nInstall findutils then re-run the plugin."
    exit 1
fi

if [ -z "$LINUXDEPLOY" ]; then
    echo -e "$0: LINUXDEPLOY environment variable is not set.\nDownload a suitable linuxdeploy AppImage, set the environment variable and re-run the plugin."
    exit 1
fi

gtk_versions=0 # Count major versions of GTK when auto-detect GTK version
if [ "$DEPLOY_GTK_VERSION" -eq 0 ]; then
    echo "Determining which GTK version to deploy"
    while IFS= read -r -d '' file; do
        if [ "$DEPLOY_GTK_VERSION" -ne 2 ] && ldd "$file" | grep -q "libgtk-x11-2.0.so"; then
            DEPLOY_GTK_VERSION=2
            gtk_versions="$((gtk_versions+1))"
        fi
        if [ "$DEPLOY_GTK_VERSION" -ne 3 ] && ldd "$file" | grep -q "libgtk-3.so"; then
            DEPLOY_GTK_VERSION=3
            gtk_versions="$((gtk_versions+1))"
        fi
        if [ "$DEPLOY_GTK_VERSION" -ne 4 ] && ldd "$file" | grep -q "libgtk-4.so"; then
            DEPLOY_GTK_VERSION=4
            gtk_versions="$((gtk_versions+1))"
        fi
    done < <(find "$APPDIR/usr/bin" -executable -type f -print0)
fi

if [ "$gtk_versions" -gt 1 ]; then
    echo "$0: can not deploy multiple GTK versions at the same time."
    echo "Please set DEPLOY_GTK_VERSION to {2, 3, 4}."
    exit 1
elif [ "$DEPLOY_GTK_VERSION" -eq 0 ]; then
    echo "$0: failed to auto-detect GTK version."
    echo "Please set DEPLOY_GTK_VERSION to {2, 3, 4}."
    exit 1
fi

echo "Installing AppRun hook"
HOOKSDIR="$APPDIR/apprun-hooks"
HOOKFILE="$HOOKSDIR/linuxdeploy-plugin-gtk.sh"
mkdir -p "$HOOKSDIR"
cat > "$HOOKFILE" <<\EOF
#! /usr/bin/env bash

COLOR_SCHEME="$(dbus-send --session --dest=org.freedesktop.portal.Desktop --type=method_call --print-reply --reply-timeout=1000 /org/freedesktop/portal/desktop org.freedesktop.portal.Settings.Read 'string:org.freedesktop.appearance' 'string:color-scheme' 2> /dev/null | tail -n1 | cut -b35- | cut -d' ' -f2 || printf '')"
if [ -z "$COLOR_SCHEME" ]; then
    COLOR_SCHEME="$(gsettings get org.gnome.desktop.interface color-scheme 2> /dev/null || printf '')"
fi
case "$COLOR_SCHEME" in
    "1"|"'prefer-dark'")  GTK_THEME_VARIANT="dark";;
    "2"|"'prefer-light'") GTK_THEME_VARIANT="light";;
    *)                    GTK_THEME_VARIANT="light";;
esac
APPIMAGE_GTK_THEME="${APPIMAGE_GTK_THEME:-"Adwaita:$GTK_THEME_VARIANT"}" # Allow user to override theme (discouraged)

export APPDIR="${APPDIR:-"$(dirname "$(realpath "$0")")"}" # Workaround to run extracted AppImage
export GTK_DATA_PREFIX="$APPDIR"
# export GTK_THEME="$APPIMAGE_GTK_THEME" # Custom themes are broken
# export GDK_BACKEND=x11 # Crash with Wayland backend on Wayland
export XDG_DATA_DIRS="$APPDIR/usr/share:/usr/share:$XDG_DATA_DIRS" # g_get_system_data_dirs() from GLib
EOF

echo "Installing GLib schemas"
# Note: schemasdir is undefined on Ubuntu 16.04
glib_schemasdir="$(get_pkgconf_variable "schemasdir" "gio-2.0" "/usr/share/glib-2.0/schemas")"
copy_tree "$glib_schemasdir" "$APPDIR/"
glib-compile-schemas "$APPDIR/$glib_schemasdir"
cat >> "$HOOKFILE" <<EOF
export GSETTINGS_SCHEMA_DIR="\$APPDIR/$glib_schemasdir"
EOF

echo "Installing GIRepository Typelibs"
gi_typelibsdir="$(get_pkgconf_variable "typelibdir" "gobject-introspection-1.0" "$LD_GTK_LIBRARY_PATH/girepository-1.0")"
copy_lib_tree "$gi_typelibsdir" "$APPDIR/"
cat >> "$HOOKFILE" <<EOF
export GI_TYPELIB_PATH="\$APPDIR/${gi_typelibsdir/$LD_GTK_LIBRARY_PATH//usr/lib}"
EOF

case "$DEPLOY_GTK_VERSION" in
    2)
        # https://github.com/linuxdeploy/linuxdeploy-plugin-gtk/pull/20#issuecomment-826354261
        echo "WARNING: Gtk+2 applications are not fully supported by this plugin"
        ;;
    3)
        echo "Installing GTK 3.0 modules"
        gtk3_exec_prefix="$(get_pkgconf_variable "exec_prefix" "gtk+-3.0" "/usr")"
        gtk3_libdir="$(get_pkgconf_variable "libdir" "gtk+-3.0" "$LD_GTK_LIBRARY_PATH")/gtk-3.0"
        gtk3_path="$gtk3_libdir"
        gtk3_immodulesdir="$gtk3_libdir/$(get_pkgconf_variable "gtk_binary_version" "gtk+-3.0" "3.0.0")/immodules"
        gtk3_printbackendsdir="$gtk3_libdir/$(get_pkgconf_variable "gtk_binary_version" "gtk+-3.0" "3.0.0")/printbackends"
        gtk3_immodules_cache_file="$(dirname "$gtk3_immodulesdir")/immodules.cache"
        gtk3_immodules_query="$(search_tool "gtk-query-immodules-3.0" "libgtk-3-0")"
        copy_lib_tree "$gtk3_libdir" "$APPDIR/"
        cat >> "$HOOKFILE" <<EOF
export GTK_EXE_PREFIX="\$APPDIR/$gtk3_exec_prefix"
export GTK_PATH="\$APPDIR/${gtk3_path/$LD_GTK_LIBRARY_PATH//usr/lib}"
export GTK_IM_MODULE_FILE="\$APPDIR/${gtk3_immodules_cache_file/$LD_GTK_LIBRARY_PATH//usr/lib}"
EOF

        if [ -x "$gtk3_immodules_query" ]; then
            echo "Updating immodules cache in $APPDIR/${gtk3_immodules_cache_file/$LD_GTK_LIBRARY_PATH//usr/lib}"
            "$gtk3_immodules_query" > "$APPDIR/${gtk3_immodules_cache_file/$LD_GTK_LIBRARY_PATH//usr/lib}"
        else
            echo "WARNING: gtk-query-immodules-3.0 not found"
        fi
        if [ ! -f "$APPDIR/${gtk3_immodules_cache_file/$LD_GTK_LIBRARY_PATH//usr/lib}" ]; then
            echo "WARNING: immodules.cache file is missing"
        fi
        sed -i "s|$gtk3_libdir/3.0.0/immodules/||g" "$APPDIR/${gtk3_immodules_cache_file/$LD_GTK_LIBRARY_PATH//usr/lib}"
        ;;
    4)
        echo "Installing GTK 4.0 modules"
        gtk4_exec_prefix="$(get_pkgconf_variable "exec_prefix" "gtk4" "/usr")"
        gtk4_libdir="$(get_pkgconf_variable "libdir" "gtk4")/gtk-4.0"
        gtk4_path="$gtk4_libdir"
        copy_lib_tree "$gtk4_libdir" "$APPDIR/"
        cat >> "$HOOKFILE" <<EOF
export GTK_EXE_PREFIX="\$APPDIR/$gtk4_exec_prefix"
export GTK_PATH="\$APPDIR/${gtk4_path/$LD_GTK_LIBRARY_PATH//usr/lib}"
EOF
        ;;
    *)
        echo "$0: '$DEPLOY_GTK_VERSION' is not a valid GTK major version."
        echo "Please set DEPLOY_GTK_VERSION to {2, 3, 4}."
        exit 1
esac

echo "Installing GDK PixBufs"
gdk_libdir="$(get_pkgconf_variable "libdir" "gdk-pixbuf-2.0" "$LD_GTK_LIBRARY_PATH")"
gdk_pixbuf_binarydir="$(get_pkgconf_variable "gdk_pixbuf_binarydir" "gdk-pixbuf-2.0" "$gdk_libdir/gdk-pixbuf-2.0/2.10.0")"
gdk_pixbuf_cache_file="$(get_pkgconf_variable "gdk_pixbuf_cache_file" "gdk-pixbuf-2.0" "$gdk_pixbuf_binarydir/loaders.cache")"
gdk_pixbuf_moduledir="$(get_pkgconf_variable "gdk_pixbuf_moduledir" "gdk-pixbuf-2.0" "$gdk_pixbuf_binarydir/loaders")"
# Note: gdk_pixbuf_query_loaders variable is not defined on some systems
gdk_pixbuf_query="$(search_tool "gdk-pixbuf-query-loaders" "gdk-pixbuf-2.0")"
copy_lib_tree "$gdk_pixbuf_binarydir" "$APPDIR/"
cat >> "$HOOKFILE" <<EOF
export GDK_PIXBUF_MODULE_FILE="\$APPDIR/${gdk_pixbuf_cache_file/$LD_GTK_LIBRARY_PATH//usr/lib}"
EOF
if [ -x "$gdk_pixbuf_query" ]; then
    echo "Updating pixbuf cache in $APPDIR/${gdk_pixbuf_cache_file/$LD_GTK_LIBRARY_PATH//usr/lib}"
    "$gdk_pixbuf_query" > "$APPDIR/${gdk_pixbuf_cache_file/$LD_GTK_LIBRARY_PATH//usr/lib}"
else
    echo "WARNING: gdk-pixbuf-query-loaders not found"
fi
if [ ! -f "$APPDIR/${gdk_pixbuf_cache_file/$LD_GTK_LIBRARY_PATH//usr/lib}" ]; then
    echo "WARNING: loaders.cache file is missing"
fi
sed -i "s|$gdk_pixbuf_moduledir/||g" "$APPDIR/${gdk_pixbuf_cache_file/$LD_GTK_LIBRARY_PATH//usr/lib}"

echo "Copying more libraries"
gobject_libdir="$(get_pkgconf_variable "libdir" "gobject-2.0" "$LD_GTK_LIBRARY_PATH")"
gio_libdir="$(get_pkgconf_variable "libdir" "gio-2.0" "$LD_GTK_LIBRARY_PATH")"
librsvg_libdir="$(get_pkgconf_variable "libdir" "librsvg-2.0" "$LD_GTK_LIBRARY_PATH")"
pango_libdir="$(get_pkgconf_variable "libdir" "pango" "$LD_GTK_LIBRARY_PATH")"
pangocairo_libdir="$(get_pkgconf_variable "libdir" "pangocairo" "$LD_GTK_LIBRARY_PATH")"
pangoft2_libdir="$(get_pkgconf_variable "libdir" "pangoft2" "$LD_GTK_LIBRARY_PATH")"
FIND_ARRAY=(
    "$gdk_libdir"        "libgdk_pixbuf-*.so*"
    "$gobject_libdir"    "libgobject-*.so*"
    "$gio_libdir"        "libgio-*.so*"
    "$librsvg_libdir"    "librsvg-*.so*"
    "$pango_libdir"      "libpango-*.so*"
    "$pangocairo_libdir" "libpangocairo-*.so*"
    "$pangoft2_libdir"   "libpangoft2-*.so*"
)
LIBRARIES=()
for (( i=0; i<${#FIND_ARRAY[@]}; i+=2 )); do
    directory=${FIND_ARRAY[i]}
    library=${FIND_ARRAY[i+1]}
    while IFS= read -r -d '' file; do
        LIBRARIES+=( "--library=$file" )
    done < <(find "$directory" \( -type l -o -type f \) -name "$library" -print0)
done

env LINUXDEPLOY_PLUGIN_MODE=1 "$LINUXDEPLOY" --appdir="$APPDIR" "${LIBRARIES[@]}"

# Create symbolic links as a workaround
# Details: https://github.com/linuxdeploy/linuxdeploy-plugin-gtk/issues/24#issuecomment-1030026529
echo "Manually setting rpath for GTK modules"
PATCH_ARRAY=(
    "$gtk3_immodulesdir"
    "$gtk3_printbackendsdir"
    "$gdk_pixbuf_moduledir"
)
for directory in "${PATCH_ARRAY[@]}"; do
    while IFS= read -r -d '' file; do
        ln $verbose -sf "${file/$LD_GTK_LIBRARY_PATH\//}" "$APPDIR/usr/lib"
    done < <(find "$directory" -name '*.so' -print0)
done
```

---

### 📄 文件: `lwg-rs/Cargo.lock`

```toml
# This file is automatically @generated by Cargo.
# It is not intended for manual editing.
version = 4

[[package]]
name = "ansi_term"
version = "0.12.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "d52a9bb7ec0cf484c551830a7ce27bd20d67eac647e1befb56b0be4ee39a55d2"
dependencies = [
 "winapi",
]

[[package]]
name = "atty"
version = "0.2.14"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "d9b39be18770d11421cdb1b9947a45dd3f37e93092cbf377614828a319d5fee8"
dependencies = [
 "hermit-abi",
 "libc",
 "winapi",
]

[[package]]
name = "autocfg"
version = "1.5.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "c08606f8c3cbf4ce6ec8e28fb0014a2c086708fe954eaa885384a6165172e7e8"

[[package]]
name = "bincode"
version = "1.3.3"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "b1f45e9417d87227c7a56d22e471c6206462cba514c7590c09aff4cf6d1ddcad"
dependencies = [
 "serde",
]

[[package]]
name = "bitflags"
version = "1.3.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "bef38d45163c2f1dde094a7dfd33ccf595c92905c8f8f4fdc18d06fb1037718a"

[[package]]
name = "bitflags"
version = "2.11.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "843867be96c8daad0d758b57df9392b6d8d271134fce549de6ce169ff98a92af"

[[package]]
name = "bumpalo"
version = "3.20.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "5d20789868f4b01b2f2caec9f5c4e0213b41e3e5702a50157d699ae31ced2fcb"

[[package]]
name = "cairo-rs"
version = "0.19.4"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "b2ac2a4d0e69036cf0062976f6efcba1aaee3e448594e6514bb2ddf87acce562"
dependencies = [
 "bitflags 2.11.0",
 "cairo-sys-rs",
 "glib",
 "libc",
 "thiserror",
]

[[package]]
name = "cairo-sys-rs"
version = "0.19.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "fd3bb3119664efbd78b5e6c93957447944f16bdbced84c17a9f41c7829b81e64"
dependencies = [
 "glib-sys",
 "libc",
 "system-deps",
]

[[package]]
name = "cfg-expr"
version = "0.15.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "d067ad48b8650848b989a59a86c6c36a995d02d2bf778d45c3c5d57bc2718f02"
dependencies = [
 "smallvec",
 "target-lexicon",
]

[[package]]
name = "cfg-if"
version = "1.0.4"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "9330f8b2ff13f34540b44e946ef35111825727b38d33286ef986142615121801"

[[package]]
name = "clap"
version = "2.34.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "a0610544180c38b88101fecf2dd634b174a62eef6946f84dfc6a7127512b381c"
dependencies = [
 "ansi_term",
 "atty",
 "bitflags 1.3.2",
 "strsim",
 "textwrap",
 "unicode-width",
 "vec_map",
]

[[package]]
name = "dbus"
version = "0.9.10"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "21b3aa68d7e7abee336255bd7248ea965cc393f3e70411135a6f6a4b651345d4"
dependencies = [
 "libc",
 "libdbus-sys",
 "windows-sys 0.59.0",
]

[[package]]
name = "dbus-codegen"
version = "0.9.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "a49da9fdfbe872d4841d56605dc42efa5e6ca3291299b87f44e1cde91a28617c"
dependencies = [
 "clap",
 "dbus",
 "xml-rs",
]

[[package]]
name = "dbus-tree"
version = "0.9.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "f456e698ae8e54575e19ddb1f9b7bce2298568524f215496b248eb9498b4f508"
dependencies = [
 "dbus",
]

[[package]]
name = "directories"
version = "5.0.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "9a49173b84e034382284f27f1af4dcbbd231ffa358c0fe316541a7337f376a35"
dependencies = [
 "dirs-sys",
]

[[package]]
name = "dirs-sys"
version = "0.4.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "520f05a5cbd335fae5a99ff7a6ab8627577660ee5cfd6a94a6a929b52ff0321c"
dependencies = [
 "libc",
 "option-ext",
 "redox_users",
 "windows-sys 0.48.0",
]

[[package]]
name = "equivalent"
version = "1.0.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "877a4ace8713b0bcf2a4e7eec82529c029f1d0619886d18145fea96c3ffe5c0f"

[[package]]
name = "field-offset"
version = "0.3.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "38e2275cc4e4fc009b0669731a1e5ab7ebf11f469eaede2bab9309a5b4d6057f"
dependencies = [
 "memoffset",
 "rustc_version",
]

[[package]]
name = "flume"
version = "0.11.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "da0e4dd2a88388a1f4ccc7c9ce104604dab68d9f408dc34cd45823d5a9069095"
dependencies = [
 "futures-core",
 "futures-sink",
 "nanorand",
 "spin",
]

[[package]]
name = "fragile"
version = "2.0.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "28dd6caf6059519a65843af8fe2a3ae298b14b80179855aeb4adc2c1934ee619"

[[package]]
name = "futures"
version = "0.3.32"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "8b147ee9d1f6d097cef9ce628cd2ee62288d963e16fb287bd9286455b241382d"
dependencies = [
 "futures-channel",
 "futures-core",
 "futures-executor",
 "futures-io",
 "futures-sink",
 "futures-task",
 "futures-util",
]

[[package]]
name = "futures-channel"
version = "0.3.32"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "07bbe89c50d7a535e539b8c17bc0b49bdb77747034daa8087407d655f3f7cc1d"
dependencies = [
 "futures-core",
 "futures-sink",
]

[[package]]
name = "futures-core"
version = "0.3.32"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "7e3450815272ef58cec6d564423f6e755e25379b217b0bc688e295ba24df6b1d"

[[package]]
name = "futures-executor"
version = "0.3.32"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "baf29c38818342a3b26b5b923639e7b1f4a61fc5e76102d4b1981c6dc7a7579d"
dependencies = [
 "futures-core",
 "futures-task",
 "futures-util",
]

[[package]]
name = "futures-io"
version = "0.3.32"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "cecba35d7ad927e23624b22ad55235f2239cfa44fd10428eecbeba6d6a717718"

[[package]]
name = "futures-macro"
version = "0.3.32"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "e835b70203e41293343137df5c0664546da5745f82ec9b84d40be8336958447b"
dependencies = [
 "proc-macro2",
 "quote",
 "syn",
]

[[package]]
name = "futures-sink"
version = "0.3.32"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "c39754e157331b013978ec91992bde1ac089843443c49cbc7f46150b0fad0893"

[[package]]
name = "futures-task"
version = "0.3.32"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "037711b3d59c33004d3856fbdc83b99d4ff37a24768fa1be9ce3538a1cde4393"

[[package]]
name = "futures-util"
version = "0.3.32"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "389ca41296e6190b48053de0321d02a77f32f8a5d2461dd38762c0593805c6d6"
dependencies = [
 "futures-channel",
 "futures-core",
 "futures-io",
 "futures-macro",
 "futures-sink",
 "futures-task",
 "memchr",
 "pin-project-lite",
 "slab",
]

[[package]]
name = "gdk-pixbuf"
version = "0.19.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "624eaba126021103c7339b2e179ae4ee8cdab842daab419040710f38ed9f8699"
dependencies = [
 "gdk-pixbuf-sys",
 "gio",
 "glib",
 "libc",
]

[[package]]
name = "gdk-pixbuf-sys"
version = "0.19.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "4efa05a4f83c8cc50eb4d883787b919b85e5f1d8dd10b5a1df53bf5689782379"
dependencies = [
 "gio-sys",
 "glib-sys",
 "gobject-sys",
 "libc",
 "system-deps",
]

[[package]]
name = "gdk4"
version = "0.8.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "db265c9dd42d6a371e09e52deab3a84808427198b86ac792d75fd35c07990a07"
dependencies = [
 "cairo-rs",
 "gdk-pixbuf",
 "gdk4-sys",
 "gio",
 "glib",
 "libc",
 "pango",
]

[[package]]
name = "gdk4-sys"
version = "0.8.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "c9418fb4e8a67074919fe7604429c45aa74eb9df82e7ca529767c6d4e9dc66dd"
dependencies = [
 "cairo-sys-rs",
 "gdk-pixbuf-sys",
 "gio-sys",
 "glib-sys",
 "gobject-sys",
 "libc",
 "pango-sys",
 "pkg-config",
 "system-deps",
]

[[package]]
name = "getrandom"
version = "0.2.17"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "ff2abc00be7fca6ebc474524697ae276ad847ad0a6b3faa4bcb027e9a4614ad0"
dependencies = [
 "cfg-if",
 "js-sys",
 "libc",
 "wasi",
 "wasm-bindgen",
]

[[package]]
name = "gio"
version = "0.19.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "4c49f117d373ffcc98a35d114db5478bc223341cff53e39a5d6feced9e2ddffe"
dependencies = [
 "futures-channel",
 "futures-core",
 "futures-io",
 "futures-util",
 "gio-sys",
 "glib",
 "libc",
 "pin-project-lite",
 "smallvec",
 "thiserror",
]

[[package]]
name = "gio-sys"
version = "0.19.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "2cd743ba4714d671ad6b6234e8ab2a13b42304d0e13ab7eba1dcdd78a7d6d4ef"
dependencies = [
 "glib-sys",
 "gobject-sys",
 "libc",
 "system-deps",
 "windows-sys 0.52.0",
]

[[package]]
name = "glib"
version = "0.19.9"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "39650279f135469465018daae0ba53357942a5212137515777d5fdca74984a44"
dependencies = [
 "bitflags 2.11.0",
 "futures-channel",
 "futures-core",
 "futures-executor",
 "futures-task",
 "futures-util",
 "gio-sys",
 "glib-macros",
 "glib-sys",
 "gobject-sys",
 "libc",
 "memchr",
 "smallvec",
 "thiserror",
]

[[package]]
name = "glib-macros"
version = "0.19.9"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "4429b0277a14ae9751350ad9b658b1be0abb5b54faa5bcdf6e74a3372582fad7"
dependencies = [
 "heck",
 "proc-macro-crate",
 "proc-macro2",
 "quote",
 "syn",
]

[[package]]
name = "glib-sys"
version = "0.19.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "5c2dc18d3a82b0006d470b13304fbbb3e0a9bd4884cf985a60a7ed733ac2c4a5"
dependencies = [
 "libc",
 "system-deps",
]

[[package]]
name = "gobject-sys"
version = "0.19.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "2e697e252d6e0416fd1d9e169bda51c0f1c926026c39ca21fbe8b1bb5c3b8b9e"
dependencies = [
 "glib-sys",
 "libc",
 "system-deps",
]

[[package]]
name = "graphene-rs"
version = "0.19.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "f5fb86031d24d9ec0a2a15978fc7a65d545a2549642cf1eb7c3dda358da42bcf"
dependencies = [
 "glib",
 "graphene-sys",
 "libc",
]

[[package]]
name = "graphene-sys"
version = "0.19.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "2f530e0944bccba4b55065e9c69f4975ad691609191ebac16e13ab8e1f27af05"
dependencies = [
 "glib-sys",
 "libc",
 "pkg-config",
 "system-deps",
]

[[package]]
name = "gsk4"
version = "0.8.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "7563884bf6939f4468e5d94654945bdd9afcaf8c3ba4c5dd17b5342b747221be"
dependencies = [
 "cairo-rs",
 "gdk4",
 "glib",
 "graphene-rs",
 "gsk4-sys",
 "libc",
 "pango",
]

[[package]]
name = "gsk4-sys"
version = "0.8.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "23024bf2636c38bbd1f822f58acc9d1c25b28da896ff0f291a1a232d4272b3dc"
dependencies = [
 "cairo-sys-rs",
 "gdk4-sys",
 "glib-sys",
 "gobject-sys",
 "graphene-sys",
 "libc",
 "pango-sys",
 "system-deps",
]

[[package]]
name = "gtk4"
version = "0.8.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "b04e11319b08af11358ab543105a9e49b0c491faca35e2b8e7e36bfba8b671ab"
dependencies = [
 "cairo-rs",
 "field-offset",
 "futures-channel",
 "gdk-pixbuf",
 "gdk4",
 "gio",
 "glib",
 "graphene-rs",
 "gsk4",
 "gtk4-macros",
 "gtk4-sys",
 "libc",
 "pango",
]

[[package]]
name = "gtk4-macros"
version = "0.8.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "ec655a7ef88d8ce9592899deb8b2d0fa50bab1e6dd69182deb764e643c522408"
dependencies = [
 "proc-macro-crate",
 "proc-macro2",
 "quote",
 "syn",
]

[[package]]
name = "gtk4-sys"
version = "0.8.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "8c8aa86b7f85ea71d66ea88c1d4bae1cfacf51ca4856274565133838d77e57b5"
dependencies = [
 "cairo-sys-rs",
 "gdk-pixbuf-sys",
 "gdk4-sys",
 "gio-sys",
 "glib-sys",
 "gobject-sys",
 "graphene-sys",
 "gsk4-sys",
 "libc",
 "pango-sys",
 "system-deps",
]

[[package]]
name = "hashbrown"
version = "0.16.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "841d1cc9bed7f9236f321df977030373f4a4163ae1a7dbfe1a51a2c1a51d9100"

[[package]]
name = "heck"
version = "0.5.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "2304e00983f87ffb38b55b444b5e3b60a884b5d30c0fca7d82fe33449bbe55ea"

[[package]]
name = "hermit-abi"
version = "0.1.19"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "62b467343b94ba476dcb2500d242dadbb39557df889310ac77c5d99100aaac33"
dependencies = [
 "libc",
]

[[package]]
name = "indexmap"
version = "2.13.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "7714e70437a7dc3ac8eb7e6f8df75fd8eb422675fc7678aff7364301092b1017"
dependencies = [
 "equivalent",
 "hashbrown",
]

[[package]]
name = "itoa"
version = "1.0.17"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "92ecc6618181def0457392ccd0ee51198e065e016d1d527a7ac1b6dc7c1f09d2"

[[package]]
name = "js-sys"
version = "0.3.89"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "f4eacb0641a310445a4c513f2a5e23e19952e269c6a38887254d5f837a305506"
dependencies = [
 "once_cell",
 "wasm-bindgen",
]

[[package]]
name = "ksni"
version = "0.2.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "4934310bdd016e55725482b8d35ac0c16fd058c1b955d8959aa2d953b918c85b"
dependencies = [
 "dbus",
 "dbus-codegen",
 "dbus-tree",
 "thiserror",
]

[[package]]
name = "lazy_static"
version = "1.5.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "bbd2bcb4c963f2ddae06a2efc7e9f3591312473c50c6685e1f298068316e66fe"

[[package]]
name = "libadwaita"
version = "0.6.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "91b4990248b9e1ec5e72094a2ccaea70ec3809f88f6fd52192f2af306b87c5d9"
dependencies = [
 "gdk-pixbuf",
 "gdk4",
 "gio",
 "glib",
 "gtk4",
 "libadwaita-sys",
 "libc",
 "pango",
]

[[package]]
name = "libadwaita-sys"
version = "0.6.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "23a748e4e92be1265cd9e93d569c0b5dfc7814107985aa6743d670ab281ea1a8"
dependencies = [
 "gdk4-sys",
 "gio-sys",
 "glib-sys",
 "gobject-sys",
 "gtk4-sys",
 "libc",
 "pango-sys",
 "system-deps",
]

[[package]]
name = "libc"
version = "0.2.182"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "6800badb6cb2082ffd7b6a67e6125bb39f18782f793520caee8cb8846be06112"

[[package]]
name = "libdbus-sys"
version = "0.2.7"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "328c4789d42200f1eeec05bd86c9c13c7f091d2ba9a6ea35acdf51f31bc0f043"
dependencies = [
 "pkg-config",
]

[[package]]
name = "libredox"
version = "0.1.12"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "3d0b95e02c851351f877147b7deea7b1afb1df71b63aa5f8270716e0c5720616"
dependencies = [
 "bitflags 2.11.0",
 "libc",
]

[[package]]
name = "lock_api"
version = "0.4.14"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "224399e74b87b5f3557511d98dff8b14089b3dadafcab6bb93eab67d3aace965"
dependencies = [
 "scopeguard",
]

[[package]]
name = "log"
version = "0.4.29"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "5e5032e24019045c762d3c0f28f5b6b8bbf38563a65908389bf7978758920897"

[[package]]
name = "lwg-core"
version = "0.1.0"
dependencies = [
 "directories",
 "serde",
 "serde_json",
 "thiserror",
 "tokio",
]

[[package]]
name = "lwg-ipc"
version = "0.1.0"
dependencies = [
 "bincode",
 "serde",
 "tokio",
 "uds",
]

[[package]]
name = "lwg-tray"
version = "0.1.0"
dependencies = [
 "ksni",
 "lwg-ipc",
 "tokio",
]

[[package]]
name = "lwg-ui"
version = "0.1.0"
dependencies = [
 "gtk4",
 "lwg-core",
 "relm4",
 "tokio",
 "tracing-subscriber",
]

[[package]]
name = "memchr"
version = "2.8.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "f8ca58f447f06ed17d5fc4043ce1b10dd205e060fb3ce5b979b8ed8e59ff3f79"

[[package]]
name = "memoffset"
version = "0.9.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "488016bfae457b036d996092f6cb448677611ce4449e970ceaf42695203f218a"
dependencies = [
 "autocfg",
]

[[package]]
name = "mio"
version = "1.1.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "a69bcab0ad47271a0234d9422b131806bf3968021e5dc9328caf2d4cd58557fc"
dependencies = [
 "libc",
 "wasi",
 "windows-sys 0.61.2",
]

[[package]]
name = "nanorand"
version = "0.7.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "6a51313c5820b0b02bd422f4b44776fbf47961755c74ce64afc73bfad10226c3"
dependencies = [
 "getrandom",
]

[[package]]
name = "nu-ansi-term"
version = "0.50.3"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "7957b9740744892f114936ab4a57b3f487491bbeafaf8083688b16841a4240e5"
dependencies = [
 "windows-sys 0.61.2",
]

[[package]]
name = "once_cell"
version = "1.21.3"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "42f5e15c9953c5e4ccceeb2e7382a716482c34515315f7b03532b8b4e8393d2d"

[[package]]
name = "option-ext"
version = "0.2.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "04744f49eae99ab78e0d5c0b603ab218f515ea8cfe5a456d7629ad883a3b6e7d"

[[package]]
name = "pango"
version = "0.19.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "3f0d328648058085cfd6897c9ae4272884098a926f3a833cd50c8c73e6eccecd"
dependencies = [
 "gio",
 "glib",
 "libc",
 "pango-sys",
]

[[package]]
name = "pango-sys"
version = "0.19.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "ff03da4fa086c0b244d4a4587d3e20622a3ecdb21daea9edf66597224c634ba0"
dependencies = [
 "glib-sys",
 "gobject-sys",
 "libc",
 "system-deps",
]

[[package]]
name = "pin-project-lite"
version = "0.2.16"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "3b3cff922bd51709b605d9ead9aa71031d81447142d828eb4a6eba76fe619f9b"

[[package]]
name = "pkg-config"
version = "0.3.32"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "7edddbd0b52d732b21ad9a5fab5c704c14cd949e5e9a1ec5929a24fded1b904c"

[[package]]
name = "proc-macro-crate"
version = "3.4.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "219cb19e96be00ab2e37d6e299658a0cfa83e52429179969b0f0121b4ac46983"
dependencies = [
 "toml_edit 0.23.10+spec-1.0.0",
]

[[package]]
name = "proc-macro2"
version = "1.0.106"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "8fd00f0bb2e90d81d1044c2b32617f68fcb9fa3bb7640c23e9c748e53fb30934"
dependencies = [
 "unicode-ident",
]

[[package]]
name = "quote"
version = "1.0.44"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "21b2ebcf727b7760c461f091f9f0f539b77b8e87f2fd88131e7f1b433b3cece4"
dependencies = [
 "proc-macro2",
]

[[package]]
name = "redox_users"
version = "0.4.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "ba009ff324d1fc1b900bd1fdb31564febe58a8ccc8a6fdbb93b543d33b13ca43"
dependencies = [
 "getrandom",
 "libredox",
 "thiserror",
]

[[package]]
name = "relm4"
version = "0.8.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "e6e0e187b58db367305e8486d3228158251da1c8ba1e18baa9de61894e822649"
dependencies = [
 "flume",
 "fragile",
 "futures",
 "gtk4",
 "libadwaita",
 "once_cell",
 "relm4-macros",
 "tokio",
 "tracing",
]

[[package]]
name = "relm4-macros"
version = "0.8.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "0774e846889823aa5766f5b62cface3189a5b36280e65b2faaa6df0319da1726"
dependencies = [
 "proc-macro2",
 "quote",
 "syn",
]

[[package]]
name = "rustc_version"
version = "0.4.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "cfcb3a22ef46e85b45de6ee7e79d063319ebb6594faafcf1c225ea92ab6e9b92"
dependencies = [
 "semver",
]

[[package]]
name = "rustversion"
version = "1.0.22"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "b39cdef0fa800fc44525c84ccb54a029961a8215f9619753635a9c0d2538d46d"

[[package]]
name = "scopeguard"
version = "1.2.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "94143f37725109f92c262ed2cf5e59bce7498c01bcc1502d7b9afe439a4e9f49"

[[package]]
name = "semver"
version = "1.0.27"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "d767eb0aabc880b29956c35734170f26ed551a859dbd361d140cdbeca61ab1e2"

[[package]]
name = "serde"
version = "1.0.228"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "9a8e94ea7f378bd32cbbd37198a4a91436180c5bb472411e48b5ec2e2124ae9e"
dependencies = [
 "serde_core",
 "serde_derive",
]

[[package]]
name = "serde_core"
version = "1.0.228"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "41d385c7d4ca58e59fc732af25c3983b67ac852c1a25000afe1175de458b67ad"
dependencies = [
 "serde_derive",
]

[[package]]
name = "serde_derive"
version = "1.0.228"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "d540f220d3187173da220f885ab66608367b6574e925011a9353e4badda91d79"
dependencies = [
 "proc-macro2",
 "quote",
 "syn",
]

[[package]]
name = "serde_json"
version = "1.0.149"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "83fc039473c5595ace860d8c4fafa220ff474b3fc6bfdb4293327f1a37e94d86"
dependencies = [
 "itoa",
 "memchr",
 "serde",
 "serde_core",
 "zmij",
]

[[package]]
name = "serde_spanned"
version = "0.6.9"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "bf41e0cfaf7226dca15e8197172c295a782857fcb97fad1808a166870dee75a3"
dependencies = [
 "serde",
]

[[package]]
name = "sharded-slab"
version = "0.1.7"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "f40ca3c46823713e0d4209592e8d6e826aa57e928f09752619fc696c499637f6"
dependencies = [
 "lazy_static",
]

[[package]]
name = "slab"
version = "0.4.12"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "0c790de23124f9ab44544d7ac05d60440adc586479ce501c1d6d7da3cd8c9cf5"

[[package]]
name = "smallvec"
version = "1.15.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "67b1b7a3b5fe4f1376887184045fcf45c69e92af734b7aaddc05fb777b6fbd03"

[[package]]
name = "socket2"
version = "0.6.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "86f4aa3ad99f2088c990dfa82d367e19cb29268ed67c574d10d0a4bfe71f07e0"
dependencies = [
 "libc",
 "windows-sys 0.60.2",
]

[[package]]
name = "spin"
version = "0.9.8"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "6980e8d7511241f8acf4aebddbb1ff938df5eebe98691418c4468d0b72a96a67"
dependencies = [
 "lock_api",
]

[[package]]
name = "strsim"
version = "0.8.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "8ea5119cdb4c55b55d432abb513a0429384878c15dde60cc77b1c99de1a95a6a"

[[package]]
name = "syn"
version = "2.0.117"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "e665b8803e7b1d2a727f4023456bbbbe74da67099c585258af0ad9c5013b9b99"
dependencies = [
 "proc-macro2",
 "quote",
 "unicode-ident",
]

[[package]]
name = "system-deps"
version = "6.2.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "a3e535eb8dded36d55ec13eddacd30dec501792ff23a0b1682c38601b8cf2349"
dependencies = [
 "cfg-expr",
 "heck",
 "pkg-config",
 "toml",
 "version-compare",
]

[[package]]
name = "target-lexicon"
version = "0.12.16"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "61c41af27dd6d1e27b1b16b489db798443478cef1f06a660c96db617ba5de3b1"

[[package]]
name = "textwrap"
version = "0.11.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "d326610f408c7a4eb6f51c37c330e496b08506c9457c9d34287ecc38809fb060"
dependencies = [
 "unicode-width",
]

[[package]]
name = "thiserror"
version = "1.0.69"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "b6aaf5339b578ea85b50e080feb250a3e8ae8cfcdff9a461c9ec2904bc923f52"
dependencies = [
 "thiserror-impl",
]

[[package]]
name = "thiserror-impl"
version = "1.0.69"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "4fee6c4efc90059e10f81e6d42c60a18f76588c3d74cb83a0b242a2b6c7504c1"
dependencies = [
 "proc-macro2",
 "quote",
 "syn",
]

[[package]]
name = "thread_local"
version = "1.1.9"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "f60246a4944f24f6e018aa17cdeffb7818b76356965d03b07d6a9886e8962185"
dependencies = [
 "cfg-if",
]

[[package]]
name = "tokio"
version = "1.49.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "72a2903cd7736441aac9df9d7688bd0ce48edccaadf181c3b90be801e81d3d86"
dependencies = [
 "libc",
 "mio",
 "pin-project-lite",
 "socket2",
 "tokio-macros",
 "windows-sys 0.61.2",
]

[[package]]
name = "tokio-macros"
version = "2.6.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "af407857209536a95c8e56f8231ef2c2e2aff839b22e07a1ffcbc617e9db9fa5"
dependencies = [
 "proc-macro2",
 "quote",
 "syn",
]

[[package]]
name = "toml"
version = "0.8.23"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "dc1beb996b9d83529a9e75c17a1686767d148d70663143c7854d8b4a09ced362"
dependencies = [
 "serde",
 "serde_spanned",
 "toml_datetime 0.6.11",
 "toml_edit 0.22.27",
]

[[package]]
name = "toml_datetime"
version = "0.6.11"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "22cddaf88f4fbc13c51aebbf5f8eceb5c7c5a9da2ac40a13519eb5b0a0e8f11c"
dependencies = [
 "serde",
]

[[package]]
name = "toml_datetime"
version = "0.7.5+spec-1.1.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "92e1cfed4a3038bc5a127e35a2d360f145e1f4b971b551a2ba5fd7aedf7e1347"
dependencies = [
 "serde_core",
]

[[package]]
name = "toml_edit"
version = "0.22.27"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "41fe8c660ae4257887cf66394862d21dbca4a6ddd26f04a3560410406a2f819a"
dependencies = [
 "indexmap",
 "serde",
 "serde_spanned",
 "toml_datetime 0.6.11",
 "winnow",
]

[[package]]
name = "toml_edit"
version = "0.23.10+spec-1.0.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "84c8b9f757e028cee9fa244aea147aab2a9ec09d5325a9b01e0a49730c2b5269"
dependencies = [
 "indexmap",
 "toml_datetime 0.7.5+spec-1.1.0",
 "toml_parser",
 "winnow",
]

[[package]]
name = "toml_parser"
version = "1.0.9+spec-1.1.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "702d4415e08923e7e1ef96cd5727c0dfed80b4d2fa25db9647fe5eb6f7c5a4c4"
dependencies = [
 "winnow",
]

[[package]]
name = "tracing"
version = "0.1.44"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "63e71662fa4b2a2c3a26f570f037eb95bb1f85397f3cd8076caed2f026a6d100"
dependencies = [
 "pin-project-lite",
 "tracing-attributes",
 "tracing-core",
]

[[package]]
name = "tracing-attributes"
version = "0.1.31"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "7490cfa5ec963746568740651ac6781f701c9c5ea257c58e057f3ba8cf69e8da"
dependencies = [
 "proc-macro2",
 "quote",
 "syn",
]

[[package]]
name = "tracing-core"
version = "0.1.36"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "db97caf9d906fbde555dd62fa95ddba9eecfd14cb388e4f491a66d74cd5fb79a"
dependencies = [
 "once_cell",
 "valuable",
]

[[package]]
name = "tracing-log"
version = "0.2.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "ee855f1f400bd0e5c02d150ae5de3840039a3f54b025156404e34c23c03f47c3"
dependencies = [
 "log",
 "once_cell",
 "tracing-core",
]

[[package]]
name = "tracing-subscriber"
version = "0.3.22"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "2f30143827ddab0d256fd843b7a66d164e9f271cfa0dde49142c5ca0ca291f1e"
dependencies = [
 "nu-ansi-term",
 "sharded-slab",
 "smallvec",
 "thread_local",
 "tracing-core",
 "tracing-log",
]

[[package]]
name = "uds"
version = "0.4.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "885c31f06fce836457fe3ef09a59f83fe8db95d270b11cd78f40a4666c4d1661"
dependencies = [
 "libc",
]

[[package]]
name = "unicode-ident"
version = "1.0.24"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "e6e4313cd5fcd3dad5cafa179702e2b244f760991f45397d14d4ebf38247da75"

[[package]]
name = "unicode-width"
version = "0.1.14"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "7dd6e30e90baa6f72411720665d41d89b9a3d039dc45b8faea1ddd07f617f6af"

[[package]]
name = "valuable"
version = "0.1.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "ba73ea9cf16a25df0c8caa16c51acb937d5712a8429db78a3ee29d5dcacd3a65"

[[package]]
name = "vec_map"
version = "0.8.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "f1bddf1187be692e79c5ffeab891132dfb0f236ed36a43c7ed39f1165ee20191"

[[package]]
name = "version-compare"
version = "0.2.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "03c2856837ef78f57382f06b2b8563a2f512f7185d732608fd9176cb3b8edf0e"

[[package]]
name = "wasi"
version = "0.11.1+wasi-snapshot-preview1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "ccf3ec651a847eb01de73ccad15eb7d99f80485de043efb2f370cd654f4ea44b"

[[package]]
name = "wasm-bindgen"
version = "0.2.112"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "05d7d0fce354c88b7982aec4400b3e7fcf723c32737cef571bd165f7613557ee"
dependencies = [
 "cfg-if",
 "once_cell",
 "rustversion",
 "wasm-bindgen-macro",
 "wasm-bindgen-shared",
]

[[package]]
name = "wasm-bindgen-macro"
version = "0.2.112"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "55839b71ba921e4f75b674cb16f843f4b1f3b26ddfcb3454de1cf65cc021ec0f"
dependencies = [
 "quote",
 "wasm-bindgen-macro-support",
]

[[package]]
name = "wasm-bindgen-macro-support"
version = "0.2.112"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "caf2e969c2d60ff52e7e98b7392ff1588bffdd1ccd4769eba27222fd3d621571"
dependencies = [
 "bumpalo",
 "proc-macro2",
 "quote",
 "syn",
 "wasm-bindgen-shared",
]

[[package]]
name = "wasm-bindgen-shared"
version = "0.2.112"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "0861f0dcdf46ea819407495634953cdcc8a8c7215ab799a7a7ce366be71c7b30"
dependencies = [
 "unicode-ident",
]

[[package]]
name = "winapi"
version = "0.3.9"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "5c839a674fcd7a98952e593242ea400abe93992746761e38641405d28b00f419"
dependencies = [
 "winapi-i686-pc-windows-gnu",
 "winapi-x86_64-pc-windows-gnu",
]

[[package]]
name = "winapi-i686-pc-windows-gnu"
version = "0.4.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "ac3b87c63620426dd9b991e5ce0329eff545bccbbb34f3be09ff6fb6ab51b7b6"

[[package]]
name = "winapi-x86_64-pc-windows-gnu"
version = "0.4.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "712e227841d057c1ee1cd2fb22fa7e5a5461ae8e48fa2ca79ec42cfc1931183f"

[[package]]
name = "windows-link"
version = "0.2.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "f0805222e57f7521d6a62e36fa9163bc891acd422f971defe97d64e70d0a4fe5"

[[package]]
name = "windows-sys"
version = "0.48.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "677d2418bec65e3338edb076e806bc1ec15693c5d0104683f2efe857f61056a9"
dependencies = [
 "windows-targets 0.48.5",
]

[[package]]
name = "windows-sys"
version = "0.52.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "282be5f36a8ce781fad8c8ae18fa3f9beff57ec1b52cb3de0789201425d9a33d"
dependencies = [
 "windows-targets 0.52.6",
]

[[package]]
name = "windows-sys"
version = "0.59.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "1e38bc4d79ed67fd075bcc251a1c39b32a1776bbe92e5bef1f0bf1f8c531853b"
dependencies = [
 "windows-targets 0.52.6",
]

[[package]]
name = "windows-sys"
version = "0.60.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "f2f500e4d28234f72040990ec9d39e3a6b950f9f22d3dba18416c35882612bcb"
dependencies = [
 "windows-targets 0.53.5",
]

[[package]]
name = "windows-sys"
version = "0.61.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "ae137229bcbd6cdf0f7b80a31df61766145077ddf49416a728b02cb3921ff3fc"
dependencies = [
 "windows-link",
]

[[package]]
name = "windows-targets"
version = "0.48.5"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "9a2fa6e2155d7247be68c096456083145c183cbbbc2764150dda45a87197940c"
dependencies = [
 "windows_aarch64_gnullvm 0.48.5",
 "windows_aarch64_msvc 0.48.5",
 "windows_i686_gnu 0.48.5",
 "windows_i686_msvc 0.48.5",
 "windows_x86_64_gnu 0.48.5",
 "windows_x86_64_gnullvm 0.48.5",
 "windows_x86_64_msvc 0.48.5",
]

[[package]]
name = "windows-targets"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "9b724f72796e036ab90c1021d4780d4d3d648aca59e491e6b98e725b84e99973"
dependencies = [
 "windows_aarch64_gnullvm 0.52.6",
 "windows_aarch64_msvc 0.52.6",
 "windows_i686_gnu 0.52.6",
 "windows_i686_gnullvm 0.52.6",
 "windows_i686_msvc 0.52.6",
 "windows_x86_64_gnu 0.52.6",
 "windows_x86_64_gnullvm 0.52.6",
 "windows_x86_64_msvc 0.52.6",
]

[[package]]
name = "windows-targets"
version = "0.53.5"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "4945f9f551b88e0d65f3db0bc25c33b8acea4d9e41163edf90dcd0b19f9069f3"
dependencies = [
 "windows-link",
 "windows_aarch64_gnullvm 0.53.1",
 "windows_aarch64_msvc 0.53.1",
 "windows_i686_gnu 0.53.1",
 "windows_i686_gnullvm 0.53.1",
 "windows_i686_msvc 0.53.1",
 "windows_x86_64_gnu 0.53.1",
 "windows_x86_64_gnullvm 0.53.1",
 "windows_x86_64_msvc 0.53.1",
]

[[package]]
name = "windows_aarch64_gnullvm"
version = "0.48.5"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "2b38e32f0abccf9987a4e3079dfb67dcd799fb61361e53e2882c3cbaf0d905d8"

[[package]]
name = "windows_aarch64_gnullvm"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "32a4622180e7a0ec044bb555404c800bc9fd9ec262ec147edd5989ccd0c02cd3"

[[package]]
name = "windows_aarch64_gnullvm"
version = "0.53.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "a9d8416fa8b42f5c947f8482c43e7d89e73a173cead56d044f6a56104a6d1b53"

[[package]]
name = "windows_aarch64_msvc"
version = "0.48.5"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "dc35310971f3b2dbbf3f0690a219f40e2d9afcf64f9ab7cc1be722937c26b4bc"

[[package]]
name = "windows_aarch64_msvc"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "09ec2a7bb152e2252b53fa7803150007879548bc709c039df7627cabbd05d469"

[[package]]
name = "windows_aarch64_msvc"
version = "0.53.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "b9d782e804c2f632e395708e99a94275910eb9100b2114651e04744e9b125006"

[[package]]
name = "windows_i686_gnu"
version = "0.48.5"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "a75915e7def60c94dcef72200b9a8e58e5091744960da64ec734a6c6e9b3743e"

[[package]]
name = "windows_i686_gnu"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "8e9b5ad5ab802e97eb8e295ac6720e509ee4c243f69d781394014ebfe8bbfa0b"

[[package]]
name = "windows_i686_gnu"
version = "0.53.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "960e6da069d81e09becb0ca57a65220ddff016ff2d6af6a223cf372a506593a3"

[[package]]
name = "windows_i686_gnullvm"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "0eee52d38c090b3caa76c563b86c3a4bd71ef1a819287c19d586d7334ae8ed66"

[[package]]
name = "windows_i686_gnullvm"
version = "0.53.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "fa7359d10048f68ab8b09fa71c3daccfb0e9b559aed648a8f95469c27057180c"

[[package]]
name = "windows_i686_msvc"
version = "0.48.5"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "8f55c233f70c4b27f66c523580f78f1004e8b5a8b659e05a4eb49d4166cca406"

[[package]]
name = "windows_i686_msvc"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "240948bc05c5e7c6dabba28bf89d89ffce3e303022809e73deaefe4f6ec56c66"

[[package]]
name = "windows_i686_msvc"
version = "0.53.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "1e7ac75179f18232fe9c285163565a57ef8d3c89254a30685b57d83a38d326c2"

[[package]]
name = "windows_x86_64_gnu"
version = "0.48.5"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "53d40abd2583d23e4718fddf1ebec84dbff8381c07cae67ff7768bbf19c6718e"

[[package]]
name = "windows_x86_64_gnu"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "147a5c80aabfbf0c7d901cb5895d1de30ef2907eb21fbbab29ca94c5b08b1a78"

[[package]]
name = "windows_x86_64_gnu"
version = "0.53.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "9c3842cdd74a865a8066ab39c8a7a473c0778a3f29370b5fd6b4b9aa7df4a499"

[[package]]
name = "windows_x86_64_gnullvm"
version = "0.48.5"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "0b7b52767868a23d5bab768e390dc5f5c55825b6d30b86c844ff2dc7414044cc"

[[package]]
name = "windows_x86_64_gnullvm"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "24d5b23dc417412679681396f2b49f3de8c1473deb516bd34410872eff51ed0d"

[[package]]
name = "windows_x86_64_gnullvm"
version = "0.53.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "0ffa179e2d07eee8ad8f57493436566c7cc30ac536a3379fdf008f47f6bb7ae1"

[[package]]
name = "windows_x86_64_msvc"
version = "0.48.5"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "ed94fce61571a4006852b7389a063ab983c02eb1bb37b47f8272ce92d06d9538"

[[package]]
name = "windows_x86_64_msvc"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "589f6da84c646204747d1270a2a5661ea66ed1cced2631d546fdfb155959f9ec"

[[package]]
name = "windows_x86_64_msvc"
version = "0.53.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "d6bbff5f0aada427a1e5a6da5f1f98158182f26556f345ac9e04d36d0ebed650"

[[package]]
name = "winnow"
version = "0.7.14"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "5a5364e9d77fcdeeaa6062ced926ee3381faa2ee02d3eb83a5c27a8825540829"
dependencies = [
 "memchr",
]

[[package]]
name = "xml-rs"
version = "0.8.28"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "3ae8337f8a065cfc972643663ea4279e04e7256de865aa66fe25cec5fb912d3f"

[[package]]
name = "zmij"
version = "1.0.21"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "b8848ee67ecc8aedbaf3e4122217aff892639231befc6a1b58d29fff4c2cabaa"

```

---

### 📄 文件: `lwg-rs/Cargo.toml`

```toml
[workspace]
members = [
    "crates/lwg-ipc",
    "crates/lwg-core",
    "crates/lwg-ui",
    "crates/lwg-tray",
]
resolver = "2" # Rust 2021 版本解析器

```

---

### 📄 文件: `lwg-rs/crates/lwg-core/Cargo.toml`

```toml
[package]
name = "lwg-core"
version = "0.1.0"
edition = "2021"

[dependencies]
# 序列化框架，用于读写 JSON
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
# 用于获取 Linux 标准配置路径 (如 ~/.config/lwg/)
directories = "5.0"
# 错误处理
thiserror = "1.0"
# 异步运行时 (与 lwg-ui 保持一致)
tokio = { version = "1", features = ["fs"] }

```

---

### 📄 文件: `lwg-rs/crates/lwg-core/src/config.rs`

```rust
use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[error("JSON parse error: {0}")]
    Json(#[from] serde_json::Error),
}

/// 核心配置结构体
/// 对应 Python 版本的 config.py 中的类
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")] // 保持与 Python 版可能存在的 camelCase 兼容
pub struct AppConfig {
    /// 是否允许开机自启
    #[serde(default = "default_true")]
    pub auto_start: bool,
    
    /// Steam Workshop 的路径
    #[serde(default)]
    pub workshop_path: Option<String>,
    
    /// 当前选中的壁纸 ID
    #[serde(default)]
    pub current_wallpaper_id: Option<String>,

    // 在这里添加更多 Python 版本中有的字段...
    // 比如 audio_volume, playback_speed 等
}

fn default_true() -> bool { true }

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            auto_start: true,
            workshop_path: None,
            current_wallpaper_id: None,
        }
    }
}

impl AppConfig {
    /// 获取配置文件的完整路径
    /// Linux: ~/.config/lwg/settings.json
    pub fn get_config_path() -> Result<PathBuf, ConfigError> {
        let proj_dirs = directories::ProjectDirs::from("com", "github", "lwg")
            .ok_or_else(|| std::io::Error::new(std::io::ErrorKind::NotFound, "Config dir not found"))?;
        
        let config_dir = proj_dirs.config_dir().to_path_buf();
        
        // 确保目录存在
        if !config_dir.exists() {
            std::fs::create_dir_all(&config_dir)?;
        }
        
        Ok(config_dir.join("settings.json"))
    }

    /// 从文件加载配置
    pub async fn load() -> Result<Self, ConfigError> {
        let path = Self::get_config_path()?;
        
        if !path.exists() {
            // 如果文件不存在，返回默认配置并保存
            let default_config = Self::default();
            default_config.save().await?;
            return Ok(default_config);
        }

        let content = tokio::fs::read_to_string(path).await?;
        let config: AppConfig = serde_json::from_str(&content)?;
        Ok(config)
    }

    /// 保存配置到文件
    pub async fn save(&self) -> Result<(), ConfigError> {
        let path = Self::get_config_path()?;
        let content = serde_json::to_string_pretty(self)?;
        tokio::fs::write(path, content).await?;
        Ok(())
    }
}

```

---

### 📄 文件: `lwg-rs/crates/lwg-core/src/lib.rs`

```rust
pub mod config;

// 重新导出常用类型，方便其他 crate 使用
pub use config::AppConfig;

```

---

### 📄 文件: `lwg-rs/crates/lwg-ipc/Cargo.toml`

```toml
[package]
name = "lwg-ipc"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
# 使用 bincode 进行二进制序列化，比 JSON 更快
bincode = "1.3" 
# 使用这个库方便处理 Abstract Socket (Linux 特有)
uds = "0.4" 
tokio = { version = "1", features = ["net"] }

```

---

### 📄 文件: `lwg-rs/crates/lwg-ipc/src/lib.rs`

```rust
use serde::{Deserialize, Serialize};

/// IPC 消息枚举
/// 对应 Python 中的 CLI 命令和 Tray 通信
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum Command {
    /// 显示窗口
    Show,
    /// 隐藏窗口
    Hide,
    /// 切换显示/隐藏
    Toggle,
    /// 随机切换壁纸
    Random,
    /// 停止壁纸
    Stop,
    /// 应用上一个壁纸
    ApplyLast,
    /// 刷新壁纸库
    Refresh,
    /// 退出程序
    Quit,
    // 未来扩展：ApplySpecific(u64) 等
}

/// Abstract Socket 路径常量
/// Python 版本可能用了动态路径，这里我们固定下来
pub const SOCKET_PATH: &str = "linux-wallpaperengine-gui.sock";

// 简单的测试
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_serialize() {
        let cmd = Command::Random;
        let encoded = bincode::serialize(&cmd).unwrap();
        let decoded: Command = bincode::deserialize(&encoded).unwrap();
        assert_eq!(cmd, decoded);
    }
}

```

---

### 📄 文件: `lwg-rs/crates/lwg-tray/Cargo.toml`

```toml
[package]
name = "lwg-tray"
version = "0.1.0"
edition = "2021"

[dependencies]
lwg-ipc = { path = "../lwg-ipc" }
ksni = "0.2" # 托盘库
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }

```

---

### 📄 文件: `lwg-rs/crates/lwg-tray/src/main.rs`

```rust
// 这是一个临时的占位文件，后续我们会移植真正的托盘逻辑
fn main() {
    println!("Linux Wallpaper GUI Tray (Rust) initialized.");
}

```

---

### 📄 文件: `lwg-rs/crates/lwg-ui/Cargo.toml`

```toml
[package]
name = "lwg-ui"
version = "0.1.0"
edition = "2021"

[dependencies]
lwg-core = { path = "../lwg-core" }
# 1. 必须保留 gtk4 依赖
gtk4 = "0.8"
relm4 = { version = "0.8", features = ["libadwaita"] }
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
tracing-subscriber = "0.3"

```

---

### 📄 文件: `lwg-rs/crates/lwg-ui/src/main.rs`

```rust
use relm4::prelude::*;
use gtk4::prelude::*;
use gtk4::ApplicationWindow; // 移除了 Label，因为在 view! 里用的是 gtk::Label
use lwg_core::AppConfig;

// 1. 定义消息枚举
#[derive(Debug)]
enum AppInput {
    ConfigLoaded(Result<AppConfig, String>),
}

struct AppModel {
    config: Option<AppConfig>,
    error: Option<String>,
}

#[relm4::component]
impl SimpleComponent for AppModel {
    type Init = ();
    type Input = AppInput;
    type Output = ();

    view! {
        ApplicationWindow {
            set_title: Some("Linux Wallpaper Engine GUI (Rust)"),
            set_default_size: (800, 600),

            gtk::Box {
                set_orientation: gtk4::Orientation::Vertical,
                set_spacing: 5,
                set_margin_all: 10,

                gtk::Label {
                    // 2. 动态显示文本
                    #[watch]
                    set_text: &match (&model.config, &model.error) {
                        (Some(cfg), None) => {
                            format!("配置加载成功！\nWorkshop路径: {:?}", cfg.workshop_path)
                        },
                        (None, Some(err)) => {
                            format!("错误: {}", err)
                        },
                        _ => "正在加载配置...".to_string()
                    },
                }
            }
        }
    }

    fn init(_init: Self::Init, root: Self::Root, sender: ComponentSender<Self>) -> ComponentParts<Self> {
        let model = Self { 
            config: None, 
            error: None 
        };

        // 修正：加上 ||，表示这是一个闭包，该闭包返回 async 块
        sender.spawn_oneshot_command(|| async move {
            let result = AppConfig::load().await;
            
            match result {
                Ok(cfg) => AppInput::ConfigLoaded(Ok(cfg)),
                Err(e) => AppInput::ConfigLoaded(Err(e.to_string())),
            }
        });

        let widgets = view_output!();
        ComponentParts { model, widgets }
    }


    fn update(&mut self, message: Self::Input, _sender: ComponentSender<Self>) {
        match message {
            AppInput::ConfigLoaded(result) => {
                match result {
                    Ok(cfg) => {
                        println!("配置加载完成: {:?}", cfg);
                        self.config = Some(cfg);
                        self.error = None;
                    }
                    Err(e) => {
                        eprintln!("加载失败: {}", e);
                        self.error = Some(e);
                        self.config = None;
                    }
                }
            }
        }
    }
}

fn main() {
    tracing_subscriber::fmt::init();
    let app = RelmApp::new("com.github.Suhoiyis.lwg-ui");
    app.run::<AppModel>(());
}

```

---

### 📄 文件: `pic/icons/GUI.png`

```
[文件过大 (>5MB)，已跳过读取]
```

---

### 📄 文件: `pic/icons/GUI_glass.png`

```
[文件过大 (>5MB)，已跳过读取]
```

---

### 📄 文件: `pic/icons/GUI_rounded.png`

```
[文件过大 (>5MB)，已跳过读取]
```

---

### 📄 文件: `pic/icons/gui_tray.png`

```
[无法读取：可能是二进制文件或编码不支持]
```

---

### 📄 文件: `pic/icons/gui_tray_glass.png`

```
[无法读取：可能是二进制文件或编码不支持]
```

---

### 📄 文件: `pic/icons/gui_tray_rounded-stopped.png`

```
[无法读取：可能是二进制文件或编码不支持]
```

---

### 📄 文件: `pic/icons/gui_tray_rounded.png`

```
[无法读取：可能是二进制文件或编码不支持]
```

---

### 📄 文件: `py_GUI/__init__.py`

```python

```

---

### 📄 文件: `py_GUI/const.py`

```python
import os

# Application constants
APP_ID = "com.wallpaperengine.gui"
VERSION = "1.0.0-pre"

# Configuration Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.expanduser("~/.config/linux-wallpaperengine-gui")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
WORKSHOP_PATH = os.path.expanduser(
    "~/.local/share/Steam/steamapps/workshop/content/431960"
)
ASSETS_PATH = os.path.expanduser(
    "~/.local/share/Steam/steamapps/common/wallpaper_engine/assets"
)
ICON_PATH = os.path.join(PROJECT_ROOT, "pic/icons/gui_tray_rounded.png")

DEFAULT_CONFIG = {
    "fps": 30,
    "volume": 0,
    "scaling": "default",
    "silence": True,
    "noFullscreenPause": False,
    "disableMouse": False,
    "noautomute": False,
    "noAudioProcessing": False,
    "disableParallax": False,
    "disableParticles": False,
    "clamping": "clamp",
    "lastWallpaper": None,
    "lastScreen": None,
    "wallpaperProperties": {},
    "screenshotDelay": 20,
    "screenshotRes": "3840x2160",
    "preferXvfb": True,
    "active_monitors": {},
    "cycleEnabled": False,
    "cycleInterval": 15,
    "cycleOrder": "random",  # random, title, size, type, id
    "assetsPath": None,  # Custom assets directory (None = auto-detect)
    "wayland_only_active": False,
    "wayland_ignore_appids": "",
    "compact_mode": False,  # Compact preview mode for tiling WMs
}

# CSS Styling
CSS_STYLE = """
/* Global */
window {
    background-color: @window_bg_color;
}

/* Top navigation bar */
.nav-bar {
    background: alpha(@window_bg_color, 0.3);
    border-radius: 12px;
    padding: 4px;
    margin: 10px 20px;
    border: none;
    border-bottom: none;
}

/* Toggle button defaults */
togglebutton {
    border: none;
    box-shadow: none;
    outline: none;
    border-bottom: none;
}

togglebutton:focus-visible {
    outline: 2px solid @accent_bg_color;
    outline-offset: 2px;
}

.nav-btn {
    background: alpha(@theme_fg_color, 0.08);
    color: @theme_fg_color;
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 600;
    border: 1px solid alpha(@theme_fg_color, 0.1);
    min-height: 36px;
    transition: all 0.2s;
    box-shadow: none;
    outline: none;
}

.nav-btn:hover {
    background: alpha(@theme_fg_color, 0.12);
    border-color: alpha(@theme_fg_color, 0.2);
}

.nav-btn.active, .nav-btn:checked {
    background: @accent_bg_color;
    color: @accent_fg_color;
    box-shadow: 0 4px 12px alpha(@accent_bg_color, 0.3);
    border: none;
    border-bottom: none;
}

.nav-btn:focus, .nav-btn:focus-visible {
    outline: 2px solid @accent_bg_color;
    outline-offset: 2px;
    box-shadow: 0 0 0 2px alpha(@accent_bg_color, 0.4);
}

/* Fix for MenuButton & DropDown double-layer look and hit-box */
menubutton.nav-btn, dropdown.nav-btn {
    background: transparent;
    border: none;
    box-shadow: none;
    outline: none;
    padding: 0;
    margin: 0;
    border-radius: inherit;
}

menubutton.nav-btn > button, dropdown.nav-btn > button {
    background: alpha(@theme_fg_color, 0.08);
    color: @theme_fg_color;
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 600;
    border: 1px solid alpha(@theme_fg_color, 0.1);
    min-height: 36px;
    transition: all 0.2s;
    box-shadow: none;
    margin: 0;
}

menubutton.nav-btn > button:focus-visible, dropdown.nav-btn > button:focus-visible {
    outline: 2px solid @accent_bg_color;
    outline-offset: 2px;
    box-shadow: 0 0 0 2px alpha(@accent_bg_color, 0.4);
}

menubutton.nav-btn > button:hover, dropdown.nav-btn > button:hover {
    background: alpha(@theme_fg_color, 0.12);
    border-color: alpha(@theme_fg_color, 0.2);
}

menubutton.nav-btn > button:active,
menubutton.nav-btn > button:checked,
dropdown.nav-btn > button:active {
    background: @accent_bg_color;
    color: @accent_fg_color;
    box-shadow: 0 4px 12px alpha(@accent_bg_color, 0.3);
    border: none;
    border-bottom: none;
}

/* Toolbar */
.toolbar {
    background: alpha(@window_bg_color, 0.3);
    border-radius: 20px;
    padding: 6px 15px;
    margin: 0 20px 10px 20px;
}

.status-label {
    color: alpha(@theme_fg_color, 0.4);
    font-weight: 600;
    font-size: 0.85em;
    letter-spacing: 0.5px;
}

.status-value {
    color: @accent_bg_color;
    font-weight: 700;
    text-transform: uppercase;
}

.status-value-yellow {
    color: alpha(@theme_fg_color, 0.6);
    font-weight: 700;
    text-transform: uppercase;
}

.search-entry {
    min-height: 20px;
    padding: 0px 6px;
    font-size: 0.85em;
}

.mode-btn {
    background: alpha(@theme_fg_color, 0.08);
    color: @theme_fg_color;
    border-radius: 10px;
    padding: 6px 6px;
    border: 1px solid alpha(@theme_fg_color, 0.1);
    min-height: 36px;
    min-width: 36px;
    font-size: 1.2em;
    transition: all 0.2s;
}

.mode-btn:hover {
    background: alpha(@theme_fg_color, 0.12);
    border-color: alpha(@theme_fg_color, 0.2);
}

.mode-btn.active, .mode-btn:checked {
    background: @accent_bg_color;
    color: @accent_fg_color;
    border-color: @accent_bg_color;
}

.stop-btn {
    background: alpha(@theme_fg_color, 0.08);
    color: #ef4444;
    border: 1px solid alpha(@theme_fg_color, 0.1);
}

.stop-btn image {
    color: #ef4444;
}

.stop-btn:hover {
    background: #450a0a;
    color: #f87171;
}

/* Wallpaper card - Grid view */
.wallpaper-card {
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.wallpaper-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
}

.wallpaper-item {
    background: alpha(@window_bg_color, 0.5);
    border-radius: 5px;
    border: 3px solid transparent;
    transition: all 0.2s ease-out;
    padding: 0;
}

.wallpaper-item:hover {
    border-color: alpha(@accent_bg_color, 0.5);
    box-shadow: 0 0 15px alpha(@accent_bg_color, 0.7);
}

.wallpaper-item.selected {
    border-color: @accent_bg_color;
    box-shadow: 0 0 15px alpha(@accent_bg_color, 0.7);
}

.wallpaper-name {
    background: alpha(@window_bg_color, 0.9);
    color: @theme_fg_color;
    border-radius: 20px;
    padding: 4px 14px;
    border: 1px solid alpha(@accent_bg_color, 0.3);
    box-shadow: 0 0 12px alpha(@accent_bg_color, 0.4);
    font-weight: 500;
    font-size: 0.85em;
}

/* Wallpaper list - List view */
.list-item {
    background: alpha(@window_bg_color, 0.5);
    border-radius: 12px;
    border: 1px solid alpha(@theme_fg_color, 0.08);
    box-shadow: 0 1px 3px alpha(@theme_fg_color, 0.05);
    padding: 12px;
    margin: 4px 0;
    transition: all 0.2s;
}

.list-item:hover {
    background: alpha(@theme_fg_color, 0.15);
    border-color: alpha(@theme_fg_color, 0.15);
}

.list-item.selected {
    border-color: @accent_bg_color;
    background: alpha(@accent_bg_color, 0.1);
}

.list-title {
    font-weight: 600;
    font-size: 1.1em;
}

.heading {
    font-weight: 600;
    font-size: 1.1em;
}

.list-type {
    color: #7dd3fc;
    font-size: 0.85em;
}

.list-tags {
    color: #a78bfa;
    font-size: 0.85em;
}

.list-size {
    color: #4ade80;
    font-weight: 600;
    font-size: 0.85em;
}

.list-index {
    color: #facc15;
    font-weight: 600;
    font-size: 0.85em;
}

.list-folder {
    color: #86efac;
    font-size: 0.85em;
}

/* Sidebar */
.sidebar {
    background: alpha(@window_bg_color, 0.8);
    border-radius: 15px;
    margin: 20px;
    margin-left: 0;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.3);
    min-width: 320px;
    max-width: 320px;
    width: 320px;
}

.sidebar-preview {
    border-radius: 10px;
    margin: 20px;
}

.sidebar-title {
    font-size: 1.3em;
    font-weight: bold;
    margin: 0 20px;
}

.sidebar-subtitle {
    color: alpha(@theme_fg_color, 0.6);
    font-size: 0.9em;
    margin: 5px 20px;
}

.sidebar-section {
    font-weight: 600;
    font-size: 0.9em;
    color: alpha(@theme_fg_color, 0.6);
    margin: 15px 20px 5px 20px;
    padding-bottom: 5px;
    border-bottom: 1px solid alpha(@theme_fg_color, 0.08);
}

.sidebar-desc {
    font-size: 0.9em;
    color: alpha(@theme_fg_color, 0.8);
    margin: 0 20px;
    line-height: 1.4;
}

.tag-chip {
    background: alpha(@theme_fg_color, 0.1);
    border-radius: 15px;
    padding: 4px 6px;
    font-size: 0.85em;
    margin: 2px;
}

.folder-chip {
    background: alpha(@accent_bg_color, 0.15);
    border: 1px solid alpha(@accent_bg_color, 0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-weight: 800;
    color: @accent_bg_color;
    font-size: 0.85em;
    margin: 5px 0 5px 20px;
}

.size-chip {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-weight: 600;
    color: #22c55e;
    font-size: 0.85em;
    margin: 5px 0 5px 0;
}

.index-chip {
    background: rgba(234, 179, 8, 0.15);
    border: 1px solid rgba(234, 179, 8, 0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-weight: 600;
    color: #eab308;
    font-size: 0.85em;
    margin: 5px 0 5px 0;
}

.sidebar-btn {
    background: @accent_bg_color;
    color: @accent_fg_color;
    border-radius: 25px;
    font-weight: bold;
    padding: 10px 20px;
    border: none;
    margin: 10px 20px;
}

.sidebar-btn:hover {
    background: alpha(@accent_bg_color, 0.8);
}

.sidebar-btn.secondary {
    background: transparent;
    border: 1px solid alpha(@theme_fg_color, 0.2);
}

.sidebar-btn.secondary:hover {
    background: alpha(@theme_fg_color, 0.1);
}

# .sidebar-btn.danger {
#     background: #dc2626;
#     color: white;
# }

# .sidebar-btn.danger:hover {
#     background: #ef4444;
# }

/* Settings page */
.settings-container {
    background: alpha(@window_bg_color, 0.5);
    border-radius: 16px;
    border: 1px solid alpha(@theme_fg_color, 0.08);
    margin: 20px;
}

.settings-sidebar {
    background: alpha(@window_bg_color, 0.6);
    border-right: 1px solid alpha(@theme_fg_color, 0.08);
    padding: 32px 16px;
}

.settings-header {
    font-size: 1.5em;
    font-weight: 800;
    margin-bottom: 8px;
}

.settings-subheader {
    color: alpha(@theme_fg_color, 0.4);
    font-size: 0.85em;
}

.settings-nav-item {
    background: alpha(@window_bg_color, 0.4);
    color: alpha(@theme_fg_color, 0.5);
    border-radius: 10px;
    padding: 12px 16px;
    font-weight: 500;
    border: 1px solid alpha(@theme_fg_color, 0.12);
    margin: 2px 0;
    transition: all 0.2s ease;
}

.settings-nav-item:hover {
    background: alpha(@theme_fg_color, 0.1);
    color: @theme_fg_color;
    border-color: alpha(@theme_fg_color, 0.2);
}

.settings-nav-item.active, .settings-nav-item:checked {
    background: @accent_bg_color;
    color: @accent_fg_color;
    border-color: transparent;
    box-shadow: 0 4px 12px alpha(@accent_bg_color, 0.3);
}

.settings-section-title {
    font-size: 1.4em;
    font-weight: 700;
    margin-bottom: 8px;
}

.settings-section-desc {
    color: alpha(@theme_fg_color, 0.5);
    font-size: 0.9em;
    margin-bottom: 20px;
}

.setting-row {
    background: alpha(@window_bg_color, 0.5);
    border-radius: 12px;
    padding: 16px;
    margin: 0px 0;
    border: 1px solid alpha(@theme_fg_color, 0.08);
    box-shadow: 0 1px 3px alpha(@theme_fg_color, 0.05);
}

.setting-label {
    font-weight: 500;
}

.setting-desc {
    color: alpha(@theme_fg_color, 0.5);
    font-size: 0.85em;
}

.action-btn {
    border-radius: 10px;
    padding: 12px;
    font-weight: 600;
    border: none;
}

.action-btn.primary {
    background: @accent_bg_color;
    color: @accent_fg_color;
}

.action-btn.primary:hover {
    background: alpha(@accent_bg_color, 0.8);
}

.action-btn.secondary {
    background: alpha(@window_bg_color, 0.4);
    border: 1px solid alpha(@theme_fg_color, 0.08);
}

.action-btn.secondary:hover {
    background: alpha(@theme_fg_color, 0.15);
}

.action-btn.danger {
    background: transparent;
    color: #ef4444;
}

.status-panel {
    margin-top: 5px;
    margin-bottom: 5px;
}

.action-btn.danger:hover {
    background: rgba(255, 77, 77, 0.1);
}

/* Scrollbar - thin & elegant */
scrollbar {
    background: transparent;
    opacity: 0.5;
    transition: opacity 200ms ease-in-out;
}

scrollbar:hover {
    opacity: 1;
}

scrollbar trough {
    background: transparent;
    border: none;
    box-shadow: none;
    outline: none;
    min-width: 3px;
    min-height: 3px;
}

scrollbar slider {
    background: alpha(@theme_fg_color, 0.3);
    border-radius: 9999px;
    min-width: 3px;
    min-height: 3px;
    margin: 0;
    padding: 0;
    transition: all 200ms ease-in-out;
}

scrollbar slider:hover {
    background: alpha(@theme_fg_color, 0.5);
}

/* Common */
.text-muted {
    color: alpha(@theme_fg_color, 0.4);
}

.card {
    background: alpha(@window_bg_color, 0.4);
    border-radius: 12px;
    border: 1px solid alpha(@theme_fg_color, 0.08);
    box-shadow: 0 1px 3px alpha(@theme_fg_color, 0.05);
    padding: 8px;
}

spinbutton {
    background: alpha(@window_bg_color, 0.4);
    border-radius: 8px;
    border: 1px solid alpha(@theme_fg_color, 0.08);
}

entry {
    background: alpha(@window_bg_color, 0.4);
    border-radius: 8px;
    border: 1px solid alpha(@theme_fg_color, 0.08);
    padding: 8px 12px;
}

switch {
    background: alpha(@theme_fg_color, 0.2);
    border-radius: 9999px;
    min-width: 42px;
    min-height: 22px;
    border: 1px solid alpha(@theme_fg_color, 0.3);
}

switch:checked {
    background: @accent_bg_color;
    border-color: @accent_bg_color;
}

switch slider {
    background: @theme_fg_color;
    border-radius: 9999px;
    min-width: 18px;
    min-height: 18px;
    margin: 2px;
    box-shadow: 0 1px 3px alpha(@theme_fg_color, 0.3);
}

switch:checked slider {
    background: @accent_fg_color;
}

dropdown button {
    background: alpha(@window_bg_color, 0.4);
    border-radius: 8px;
    border: 1px solid alpha(@theme_fg_color, 0.08);
}

/* Boxed Expander */
.boxed-expander {
    background: alpha(@window_bg_color, 0.5);
    border: 1px solid alpha(@theme_fg_color, 0.08);
    border-radius: 12px;
    margin: 4px 0;
    padding: 2px;
    box-shadow: 0 1px 3px alpha(@theme_fg_color, 0.05);
}

.boxed-expander title {
    border-radius: 8px;
    padding: 8px;
}

.boxed-expander:checked {
    background: alpha(@theme_fg_color, 0.05);
    border-color: alpha(@theme_fg_color, 0.15);
}

/* Nickname Support */
.nickname-text {
    font-style: italic;
    font-weight: bold;
    color: alpha(@theme_fg_color, 0.9);
}

.original-name-text {
    font-size: 0.85em;
    color: alpha(@theme_fg_color, 0.7);
    margin: 0 20px 5px 20px;
}

/* Popover Menu Buttons */
.popover-btn {
    padding: 4px 8px;
    margin: 0px;
    border-radius: 6px;
    background: transparent;
    border: none;
    box-shadow: none;
    transition: background 0.2s;
}

.popover-btn:hover {
    background: alpha(@theme_fg_color, 0.1);
}

.popover-btn label {
    margin: 0;
}
"""

```

---

### 📄 文件: `py_GUI/core/__init__.py`

```python

```

---

### 📄 文件: `py_GUI/core/config.py`

```python
import os
import json
from typing import Dict
from py_GUI.const import CONFIG_DIR, CONFIG_FILE, DEFAULT_CONFIG

class ConfigManager:
    def __init__(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        self.config = self.load()

    def load(self) -> Dict:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    cfg = json.load(f)
                    return {**DEFAULT_CONFIG, **cfg}
            except Exception:
                pass
        return DEFAULT_CONFIG.copy()

    def save(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default=None):
        val = self.config.get(key)
        return val if val is not None else default

    def set(self, key: str, value):
        self.config[key] = value
        self.save()

```

---

### 📄 文件: `py_GUI/core/controller.py`

```python
import subprocess
import os
import shutil
import re
from typing import Optional, Callable, List, Tuple, Dict, TextIO
from py_GUI.core.config import ConfigManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.logger import LogManager

from py_GUI.core.screen import ScreenManager
from py_GUI.core.performance import PerformanceMonitor

class WallpaperController:
    def __init__(self, config: ConfigManager, prop_manager: PropertiesManager, 
                 log_manager: LogManager, screen_manager: ScreenManager):
        self.config = config
        self.prop_manager = prop_manager
        self.log_manager = log_manager
        self.screen_manager = screen_manager
        self.current_proc: Optional[subprocess.Popen[bytes]] = None
        self.show_toast: Callable[[str], None] = lambda msg: None
        self._last_command: List[str] = []
        self.history_manager = None
        self.wp_manager = None
        self.engine_log: Optional[TextIO] = None
        
        self.perf_monitor = PerformanceMonitor(config=config)
        
        if shutil.which("xvfb-run"):
            self.log_manager.add_info("Xvfb detected: Silent screenshots enabled", "Controller")
        else:
            self.log_manager.add_info("Xvfb not found: Screenshots will spawn a window", "Controller")

    def set_toast_callback(self, callback: Callable[[str], None]):
        self.show_toast = callback

    def apply(self, wp_id: str, screen: Optional[str] = None, screens: Optional[List[str]] = None):
        """Apply wallpaper (Multi-monitor support)"""
        
        target_screens = []
        if screens:
            target_screens = screens
        elif screen:
            target_screens = [screen]
        else:
            last = self.config.get("lastScreen")
            if not last or last == "None":
                last = self.screen_manager.get_primary_screen() or self.screen_manager.get_first_screen() or "eDP-1"
            target_screens = [last]

        active_monitors = dict(self.config.get("active_monitors", {}) or {})
        
        for s in target_screens:
            active_monitors[s] = wp_id
            
        self.config.set("active_monitors", active_monitors)
        self.config.set("lastWallpaper", wp_id)
        
        if len(target_screens) == 1:
            self.config.set("lastScreen", target_screens[0])

        self.log_manager.add_info(f"Applying wallpaper {wp_id} to {target_screens}", "Controller")
        
        # Record wallpaper in history if HistoryManager is available
        if self.history_manager:
            try:
                wp_details = self.wp_manager.get_wallpaper(wp_id)
                if wp_details:
                    title = wp_details.get('title', 'Unknown')
                    preview = wp_details.get('preview', '')
                    self.history_manager.add(wp_id, title, preview)
            except Exception as e:
                self.log_manager.add_error(f"Failed to record wallpaper in history: {e}", "Controller")
        
        self.restart_wallpapers()

    def stop_screen(self, screen: str):
        """Stop wallpaper on a specific screen"""
        active_monitors = dict(self.config.get("active_monitors", {}) or {})
        if screen in active_monitors:
            del active_monitors[screen]
            self.config.set("active_monitors", active_monitors)
            self.log_manager.add_info(f"Stopped wallpaper on {screen}", "Controller")
            
            if not active_monitors:
                self.stop()
            else:
                self.restart_wallpapers()

    def restart_wallpapers(self):
        """Restart the engine with current active_monitors configuration"""
        self.stop()
        
        # Validate screens
        active_monitors = dict(self.config.get("active_monitors", {}) or {})
        connected_screens = self.screen_manager.get_screens()
        
        # Filter out disconnected screens
        valid_monitors = {scr: wid for scr, wid in active_monitors.items() if scr in connected_screens}
        
        # If monitors were removed, update config
        if len(valid_monitors) != len(active_monitors):
            self.log_manager.add_info(f"Removing disconnected screens from config. Valid: {list(valid_monitors.keys())}", "Controller")
            self.config.set("active_monitors", valid_monitors)
            active_monitors = valid_monitors

        if not active_monitors:
            self.log_manager.add_info("No active wallpapers for connected screens.", "Controller")
            return

        cmd = ["linux-wallpaperengine"]
        
        # Add screens
        for scr, wid in active_monitors.items():
            cmd.extend(["--screen-root", scr, "--bg", str(wid)])

        # Global args
        cmd.extend(["-f", str(self.config.get("fps", 30))])

        # Strict boolean check with default True for None
        silence_cfg = self.config.get("silence")
        is_silent_mode = True if silence_cfg is None else bool(silence_cfg)
        
        self.log_manager.add_debug(f"Building command. Silence mode: {is_silent_mode} (Raw: {silence_cfg})", "Controller")

        if is_silent_mode:
            cmd.append("--silent")
        else:
            cmd.extend(["--volume", str(self.config.get("volume", 50))])

        scaling = str(self.config.get("scaling") or "default")
        if scaling != "default":
            cmd.extend(["--scaling", scaling])

        if self.config.get("noFullscreenPause", False):
            cmd.append("--no-fullscreen-pause")

        if self.config.get("disableMouse", False):
            cmd.append("--disable-mouse")

        if self.config.get("noautomute", False):
            cmd.append("--noautomute")

        if self.config.get("noAudioProcessing", False):
            cmd.append("--no-audio-processing")

        if self.config.get("disableParallax", False):
            cmd.append("--disable-parallax")

        if self.config.get("disableParticles", False):
            cmd.append("--disable-particles")

        clamp = str(self.config.get("clamping", "clamp") or "clamp")
        if clamp != "clamp":
            cmd.extend(["--clamp", clamp])

        if self.config.get("wayland_only_active", False):
            cmd.append("--fullscreen-pause-only-active")
            
        ignore_ids = (self.config.get("wayland_ignore_appids") or "").strip()
        if ignore_ids:
            for appid in ignore_ids.split(','):
                if appid.strip():
                    cmd.extend(["--fullscreen-pause-ignore-appid", appid.strip()])

        assets_path = self.config.get("assetsPath")
        if assets_path:
            cmd.extend(["--assets-dir", assets_path])

        # Properties (Apply for all active wallpapers)
        audio_props = {'musicvolume', 'music', 'bellvolume', 'sound', 'soundsettings', 'volume'}
        
        for wid in set(active_monitors.values()):
            user_props = self.prop_manager._user_properties.get(wid, {})
            for prop_name, prop_value in user_props.items():
                if is_silent_mode and prop_name.lower() in audio_props:
                    continue
                prop_type = self.prop_manager.get_property_type(wid, prop_name)
                formatted_value = self.prop_manager.format_property_value(prop_type, prop_value)
                cmd.extend(["--set-property", f"{prop_name}={formatted_value}"])

        self._last_command = cmd
        self.log_manager.add_debug(f"Executing: {' '.join(cmd)}", "Controller")

        try:
            # Fix potential deadlock by redirecting stdout/stderr to a log file instead of PIPE
            from py_GUI.const import CONFIG_DIR
            log_path = os.path.join(CONFIG_DIR, "engine_last.log")
            self.engine_log = open(log_path, "w")

            self.current_proc = subprocess.Popen(
                cmd,
                stdout=self.engine_log,
                stderr=self.engine_log
            )

            import time
            time.sleep(0.5)
            if self.current_proc.poll() is not None:
                self.engine_log.close()
                with open(log_path, "r") as f:
                    output = f.read()
                
                error_msg = f"Process exited immediately!\nOutput:\n{output}"
                self.log_manager.add_error(error_msg, "Engine")
                self.show_toast("❌ Wallpaper engine failed to start - check logs")
                return

            self.log_manager.add_info("Engine started successfully", "Controller")

            # Start Performance Monitoring
            if self.current_proc and self.current_proc.pid:
                self.perf_monitor.stop_all_backends()
                self.perf_monitor.start_monitoring("backend", self.current_proc.pid)

            colors_script = os.path.expanduser("~/niri/scripts/sync_colors.sh")
            if os.path.exists(colors_script):
                try:
                    subprocess.run(["bash", colors_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                except Exception:
                    pass

        except Exception as e:
            self.log_manager.add_error(f"Failed to start engine: {e}", "Controller")
            self.show_toast(f"❌ Failed to start engine: {e}")

    def take_screenshot(self, wp_id: str, output_path: str, delay: Optional[int] = None):
        """Take a high-resolution screenshot of a specific wallpaper"""
        if delay is None:
            delay = self.config.get("screenshotDelay", 20)

        default_res = "3840x2160"
        res_raw = self.config.get("screenshotRes", default_res)
        res = res_raw if isinstance(res_raw, str) else default_res
        res = res.strip()
        if not re.fullmatch(r"\d+[xX]\d+", res):
            res = default_res
        else:
            res = res.lower()
        
        # Check for xvfb-run dynamically and preference
        xvfb_path = shutil.which("xvfb-run")
        prefer_xvfb = self.config.get("preferXvfb", True)
        has_xvfb = (xvfb_path is not None) and prefer_xvfb
        
        # Base command for the engine
        engine_cmd = [
            "linux-wallpaperengine",
            "--screenshot", output_path,
            "--screenshot-delay", str(delay),
            "--silent",
            "-f", "60",
            str(wp_id)
        ]

        assets_path = self.config.get("assetsPath")
        if assets_path:
            engine_cmd.extend(["--assets-dir", assets_path])

        if has_xvfb:
            assert xvfb_path is not None
            # Wrap in xvfb-run
            # Important: The server args must be a single string for -s
            xvfb_args = ["-a", "-s", f"-screen 0 {res}x24 +extension GLX"]
            
            # Combine commands
            # Even in Xvfb, we MUST force the engine to create a window of the target resolution
            # Otherwise it might default to 640x480 or 800x600
            cmd = [xvfb_path] + xvfb_args + engine_cmd + ["--window", f"0x0x{res}"]
            mode_msg = f"Silent (Xvfb) at {res}"
        else:
            # Fallback: Force window size
            cmd = engine_cmd + ["--window", f"0x0x{res}"]
            mode_msg = f"Windowed at {res} (Xvfb not found)"
        
        self.log_manager.add_info(f"Starting screenshot: {mode_msg}", "Controller")
        self.log_manager.add_info(f"Raw command: {cmd}", "Controller")
        
        # Prepare environment: Force X11/Xvfb usage by stripping Wayland vars
        env = os.environ.copy()
        if has_xvfb:
            # Aggressively strip Wayland indicators
            env.pop("WAYLAND_DISPLAY", None)
            env["XDG_SESSION_TYPE"] = "x11"
            env["SDL_VIDEODRIVER"] = "x11"
            env["GDK_BACKEND"] = "x11"
            # Ensure software rendering fallback if hardware GL fails in Xvfb
            env["LIBGL_ALWAYS_SOFTWARE"] = "1" 
        
        # Run asynchronously with a new session so we can kill the whole group
        # Redirect stderr to a temp file for debugging crashes
        err_log = open("/tmp/wallpaper_screenshot_error.log", "w")
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=err_log, start_new_session=True, env=env)
        
        tracker = self.perf_monitor.start_task("screenshot", proc.pid)
        return proc, tracker

    def stop(self):
        """Stop wallpaper"""
        self.log_manager.add_info("Stopping wallpaper", "Controller")
        
        self.perf_monitor.stop_all_backends()
        
        if self.current_proc:
            self.current_proc.terminate()
            self.current_proc = None
            
            # Close log file handle if open
            if hasattr(self, 'engine_log') and self.engine_log and not self.engine_log.closed:
                try:
                    self.engine_log.close()
                except Exception:
                    pass
        subprocess.run(
            ["pkill", "-f", "linux-wallpaperengine"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

    def get_current_command(self) -> str:
        if not self._last_command:
            return ""
        return " ".join(self._last_command)

```

---

### 📄 文件: `py_GUI/core/history.py`

```python
import os
import json
from typing import List, Dict
from datetime import datetime
from py_GUI.const import CONFIG_DIR


class HistoryManager:
    """
    Manages wallpaper playback history with persistence.
    
    - Stores up to 30 entries in history.json
    - Deduplicates by wp_id (moves existing to top)
    - Saves automatically on modifications
    """
    
    MAX_ENTRIES = 30
    
    def __init__(self, config_manager):
        """
        Initialize HistoryManager.
        
        Args:
            config_manager: ConfigManager instance (for future extensibility)
        """
        self.history_file = os.path.join(CONFIG_DIR, "history.json")
        self.history: List[Dict] = self._load()
    
    def add(self, wp_id: str, title: str, preview: str) -> None:
        self.history = [e for e in self.history if e.get("id") != wp_id]
        
        entry = {
            "id": wp_id,
            "title": title,
            "preview": preview,
            "timestamp": datetime.now().isoformat()
        }
        
        self.history.insert(0, entry)
        self.history = self.history[:self.MAX_ENTRIES]
        self._save()
    
    def get_all(self) -> List[Dict]:
        """
        Get all history entries in order.
        
        Returns:
            List of history entries (most recent first)
        """
        return self.history.copy()
    
    def has_history(self) -> bool:
        """
        Check if history has any entries.
        
        Returns:
            True if history is not empty, False otherwise
        """
        return len(self.history) > 0
    
    def clear(self) -> None:
        """
        Clear all history and save.
        """
        self.history = []
        self._save()
    
    def _load(self) -> List[Dict]:
        """
        Load history from JSON file.
        
        Returns:
            List of history entries, or empty list if file doesn't exist
        """
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save(self) -> None:
        """
        Save history to JSON file.
        """
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

```

---

### 📄 文件: `py_GUI/core/integrations.py`

```python
import os
import sys
import stat
import shutil
import base64
import subprocess

from py_GUI.const import APP_ID

# 【神级优化】：在程序刚启动、虚拟文件系统(FUSE)绝对健康的时候，就把图标吃进内存！
# 坚决不在运行时去读文件。
try:
    from py_GUI.embedded_icon import ICON_DATA
    RAM_ICON_CACHE = ICON_DATA
    print("✅ Start loading: Successfully retrieved Base64 icon from memory.")
except Exception as e:
    print(f"⚠️ Startup prompt: Embedded icon module not found (source code development environment is normal): {e}")
    RAM_ICON_CACHE = None


class AppIntegrator:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(os.path.dirname(current_dir))
        
        self.script_path = os.path.join(self.project_root, "run_gui.py")
        self.icon_path = os.path.join(self.project_root, "pic/icons/GUI_rounded.png")
        self.python_exe = sys.executable
        
        self.app_dir = os.path.expanduser("~/.local/share/applications")
        self.autostart_dir = os.path.expanduser("~/.config/autostart")
        self.desktop_filename = f"{APP_ID}.desktop"

    def _generate_content(self, hidden=False):
        appimage_path = os.environ.get("APPIMAGE")
        
        if appimage_path:
            exec_cmd = f"\"{appimage_path}\""
            path_str = ""
        elif self.project_root.startswith("/usr/share/"):
            exec_cmd = "linux-wallpaperengine-gui"
            path_str = ""
        else:
            exec_cmd = f"{self.python_exe} \"{self.script_path}\""
            path_str = f"Path={self.project_root}\n"
        
        icon_str = APP_ID
        
        if hidden:
            exec_cmd += " --hidden"
            
        return f"""[Desktop Entry]
Type=Application
Name=Linux Wallpaper Engine
Comment=Wallpaper Engine for Linux (GUI)
Exec={exec_cmd}
Icon={icon_str}
{path_str}Terminal=false
Categories=Utility;Graphics;
StartupNotify=true
StartupWMClass={APP_ID}
X-GNOME-Autostart-enabled=true
"""

    def _install_icon(self):
        """完全从内存写入，与物理磁盘 100% 解耦"""
        dest_dir = os.path.expanduser("~/.local/share/icons/hicolor/512x512/apps")
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, f"{APP_ID}.png")
        
        icon_installed = False

        # ── 策略 A：内存直接吐出 (AppImage 专属，极速且无视 FUSE) ──
        if RAM_ICON_CACHE:
            try:
                with open(dest_path, "wb") as f:
                    f.write(base64.b64decode(RAM_ICON_CACHE))
                print(f"✅ SUCCESS: Icon materialized from RAM to {dest_path}")
                icon_installed = True
            except Exception as e:
                print(f"❌ ERROR writing RAM icon: {e}")

        # ── 策略 B：传统复制 (源码环境备用) ──
        if not icon_installed:
            candidates = [
                self.icon_path,
                os.path.join(self.project_root, "pic/icons/GUI_rounded.png"),
                os.path.join(self.project_root, "pic/icons/gui_tray_rounded.png")
            ]
            for src in candidates:
                if os.path.exists(src):
                    try:
                        shutil.copy(src, dest_path)
                        print(f"✅ SUCCESS: Icon copied from local file to {dest_path}")
                        icon_installed = True
                        break
                    except Exception as e:
                        print(f"❌ ERROR copying {src}: {e}")

        # ── 刷新缓存 ──
        if icon_installed:
            try:
                # 【终极修复】不使用 os.getcwd() 和 os.chdir()！
                # 直接通过 cwd 参数，让子进程在安全的用户主目录下运行，彻底隔离 FUSE
                subprocess.run(
                    ["/usr/bin/gtk-update-icon-cache", "-f", "-t", os.path.expanduser("~/.local/share/icons/hicolor")],
                    stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=False,
                    cwd=os.path.expanduser("~")  # <--- 让子进程降落在这里
                )
                print("✅ SUCCESS: Icon cache officially updated.")
            except Exception as e:
                print(f"⚠️ Refresh icon cache skip (non-fatal): {e}")
        else:
            print("⚠️ CRITICAL: All icon extraction strategies failed!")

    def create_menu_shortcut(self):
        self._install_icon()
        os.makedirs(self.app_dir, exist_ok=True)
        path = os.path.join(self.app_dir, self.desktop_filename)
        self._write_file(path, self._generate_content(hidden=False))
        return path

    def create_desktop_entry(self):
        try:
            path = self.create_menu_shortcut()
            return True, f"Desktop entry created at: {path}"
        except Exception as e:
            return False, f"Failed to create desktop entry: {str(e)}"

    def set_autostart(self, enabled: bool, hidden: bool = True):
        os.makedirs(self.autostart_dir, exist_ok=True)
        path = os.path.join(self.autostart_dir, self.desktop_filename)
        if enabled:
            self._install_icon()
            self._write_file(path, self._generate_content(hidden=hidden))
        else:
            if os.path.exists(path):
                os.remove(path)

    def is_autostart_enabled(self) -> bool:
        path = os.path.join(self.autostart_dir, self.desktop_filename)
        return os.path.exists(path)

    def check_and_update_shortcut(self):
        path = os.path.join(self.app_dir, self.desktop_filename)
        if not os.path.exists(path):
            return False
        try:
            with open(path, "r") as f:
                existing_content = f.read()
        except Exception:
            return False
        
        expected_content = self._generate_content(hidden=False)
        if existing_content == expected_content:
            return False
        
        try:
            self._install_icon()
            self._write_file(path, expected_content)
            return True
        except Exception:
            return False

    def _write_file(self, path, content):
        with open(path, "w") as f:
            f.write(content)
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)
```

---

### 📄 文件: `py_GUI/core/logger.py`

```python
from datetime import datetime
from typing import List, Dict

class LogManager:
    def __init__(self, max_entries: int = 500):
        self._logs: List[Dict] = []
        self._max_entries = max_entries
        self._callbacks: List[callable] = []

    def add(self, level: str, message: str, source: str = "GUI"):
        """Add a log entry"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "source": source,
            "message": message
        }
        self._logs.append(log_entry)

        # Limit log size
        if len(self._logs) > self._max_entries:
            self._logs = self._logs[-self._max_entries:]

        # Notify listeners
        for callback in self._callbacks:
            try:
                callback(log_entry)
            except Exception as e:
                print(f"[LOG] Callback error: {e}")

    def add_debug(self, message: str, source: str = "GUI"):
        self.add("DEBUG", message, source)

    def add_info(self, message: str, source: str = "GUI"):
        self.add("INFO", message, source)

    def add_warning(self, message: str, source: str = "GUI"):
        self.add("WARNING", message, source)

    def add_error(self, message: str, source: str = "GUI"):
        self.add("ERROR", message, source)

    def get_logs(self) -> List[Dict]:
        """Get all logs"""
        return self._logs.copy()

    def clear(self):
        """Clear logs"""
        self._logs.clear()

    def register_callback(self, callback: callable):
        """Register log update callback"""
        self._callbacks.append(callback)

```

---

### 📄 文件: `py_GUI/core/nickname.py`

```python
from typing import Dict, Optional, List, Tuple
from py_GUI.core.config import ConfigManager


class NicknameManager:
    """Manage wallpaper nicknames stored in config.json"""
    
    def __init__(self, config: ConfigManager):
        self._config = config
        self._nicknames: Dict[str, str] = {}
        self.load_from_config()
    
    def load_from_config(self):
        """Load nicknames from config"""
        nicknames_data = self._config.get("wallpaperNicknames", {})
        self._nicknames = nicknames_data.copy()
    
    def save_to_config(self):
        """Save nicknames to config"""
        self._config.set("wallpaperNicknames", self._nicknames)
    
    def get(self, wp_id: str) -> Optional[str]:
        """Get nickname for wallpaper, return None if not set"""
        return self._nicknames.get(wp_id)
    
    def set(self, wp_id: str, nickname: str):
        """
        Set nickname for wallpaper.
        - Trim whitespace
        - If empty after trim -> delete
        - Max length 100 chars (truncate if longer)
        - Save to config
        """
        trimmed = nickname.strip()
        
        if not trimmed:
            # Empty after trim, delete if exists
            if wp_id in self._nicknames:
                del self._nicknames[wp_id]
        else:
            # Truncate to 100 chars
            trimmed = trimmed[:100]
            self._nicknames[wp_id] = trimmed
        
        self.save_to_config()
    
    def delete(self, wp_id: str):
        """Remove nickname for wallpaper"""
        if wp_id in self._nicknames:
            del self._nicknames[wp_id]
            self.save_to_config()
    
    def get_all(self) -> Dict[str, str]:
        """Return all nicknames as a copy"""
        return self._nicknames.copy()
    
    def has(self, wp_id: str) -> bool:
        """Check if wallpaper has a nickname"""
        return wp_id in self._nicknames
    
    def cleanup(self, valid_ids: List[str]):
        """Remove entries for invalid wp_ids (ids not in valid_ids)"""
        valid_set = set(valid_ids)
        to_delete = [wp_id for wp_id in self._nicknames if wp_id not in valid_set]
        
        for wp_id in to_delete:
            del self._nicknames[wp_id]
        
        if to_delete:
            self.save_to_config()
    
    def get_display_name(self, wp: Dict) -> Tuple[str, Optional[str]]:
        """
        Get display name for a wallpaper.
        
        Returns:
            Tuple of (display_name, secondary_text)
            - If nickname exists: (nickname, original_title)
            - Otherwise: (original_title, None)
        """
        wp_id = str(wp.get('id', ''))
        nickname = self.get(wp_id)
        title = wp.get('title', 'Unknown')
        
        if nickname:
            return (nickname, title)
        else:
            return (title, None)

```

---

### 📄 文件: `py_GUI/core/performance.py`

```python
import psutil
import time
import threading
import os
from collections import deque
from typing import Callable, Protocol, TypedDict, cast

HISTORY_SIZE = 60

def _format_cpu(val: float) -> str:
    return f"{int(val)}%" if val == int(val) else f"{val:.1f}%"

def _format_mem(val: float) -> str:
    return f"{int(val)} MB" if val == int(val) else f"{val:.1f} MB"

def _get_thread_names(pid: int) -> list[str]:
    names: list[str] = []
    task_dir = f"/proc/{pid}/task"
    try:
        for tid in os.listdir(task_dir):
            try:
                with open(f"{task_dir}/{tid}/comm") as f:
                    names.append(f.read().strip())
            except (IOError, OSError):
                pass
    except (IOError, OSError):
        pass
    return names

SCREENSHOT_HISTORY_LIMIT = 10


class _Config(Protocol):
    def get(self, key: str, default: object = ...) -> object:
        ...

    def set(self, key: str, value: object) -> None:
        ...


class TaskTracker(TypedDict):
    category: str
    start_time: float
    pid: int
    initial_cpu_time: float


class _HistoryPayload(TypedDict):
    cpu: list[float]
    memory_mb: list[float]


class _DetailPayload(TypedDict):
    pid: int
    name: str
    cpu: float
    cpu_fmt: str
    memory_mb: float
    memory_fmt: str
    threads: int
    status: str
    history: _HistoryPayload


class _TotalPayload(TypedDict):
    cpu: float
    cpu_fmt: str
    memory_mb: float
    memory_fmt: str
    threads: int
    history: _HistoryPayload
    thread_names: dict[str, list[str]]


class _StatsPayload(TypedDict):
    total: _TotalPayload
    details: dict[str, _DetailPayload]


class PerformanceMonitor:
    def __init__(self, config: _Config | None = None):
        self._stop_event: threading.Event = threading.Event()
        self._thread: threading.Thread | None = None
        self._callbacks: list[Callable[[_StatsPayload], None]] = []
        self._interval: float = 1.0
        
        self._processes: dict[str, psutil.Process] = {}
        self._history: dict[str, dict[str, deque[float]]] = {}
        self._cpu_count: int = psutil.cpu_count() or 1
        self._config: _Config | None = config
        _ = self._add_process("frontend", psutil.Process().pid)

    def _init_history(self, category: str) -> None:
        self._history[category] = {
            "cpu": deque(maxlen=HISTORY_SIZE),
            "memory_mb": deque(maxlen=HISTORY_SIZE)
        }

    def _find_real_process(self, pid: int, timeout: float = 0.0) -> psutil.Process | None:

        def _try_find_child(proc: psutil.Process) -> psutil.Process | None:
            try:
                children = proc.children(recursive=True)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return None

            for child in children:
                try:
                    if child.name() == "linux-wallpaperengine":
                        return child
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return None

        try:
            proc = psutil.Process(pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

        try:
            if proc.name() == "linux-wallpaperengine":
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

        real = _try_find_child(proc)
        if real is not None:
            return real

        if timeout and timeout > 0:
            poll_interval = 0.1
            deadline = time.monotonic() + timeout
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                time.sleep(min(poll_interval, remaining))

                try:
                    proc = psutil.Process(pid)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return None

                try:
                    if proc.name() == "linux-wallpaperengine":
                        return proc
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return None

                real = _try_find_child(proc)
                if real is not None:
                    return real

        return proc

    def _add_process(self, category: str, pid: int) -> bool:
        # For backend and screenshot, find the real linux-wallpaperengine process
        proc = None
        if category in ("backend", "screenshot"):
            poll_timeout = 0.2 if threading.current_thread() is threading.main_thread() else 1.0
            proc = self._find_real_process(pid, timeout=poll_timeout)
        if proc is None:
            try:
                proc = psutil.Process(pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return False
        # Initialize CPU usage counter
        try:
            _ = proc.cpu_percent(interval=None)
        except Exception:
            pass
            
        self._processes[category] = proc
        self._init_history(category)
        return True

    def start_monitoring(self, category: str, pid: int):
        if self._add_process(category, pid):
            self._ensure_thread_running()

    def stop_monitoring(self, category: str):
        _ = self._processes.pop(category, None)
        _ = self._history.pop(category, None)

    def stop_all_backends(self):
        keys = [k for k in self._processes.keys() if k not in ("frontend", "tray")]
        for k in keys:
            del self._processes[k]
            _ = self._history.pop(k, None)

    def start_task(self, category: str, pid: int) -> TaskTracker:
        """Start tracking a specific task. Returns a tracker object (dict)."""
        self.start_monitoring(category, pid)
        
        initial_cpu_time = 0.0
        if category in self._processes:
            try:
                proc = self._processes[category]
                cpu_times = proc.cpu_times()
                initial_cpu_time = cpu_times.user + cpu_times.system
            except Exception:
                pass

        return {
            "category": category,
            "start_time": time.time(),
            "pid": pid,
            "initial_cpu_time": initial_cpu_time
        }

    def stop_task(self, tracker: TaskTracker) -> dict[str, float]:
        """Stop tracking a task and return stats."""
        category = tracker["category"]
        start_time = tracker["start_time"]
        initial_cpu_time = tracker["initial_cpu_time"]
        duration = time.time() - start_time
        
        if category in self._processes:
            try:
                proc = self._processes[category]
                with proc.oneshot():
                    cpu = proc.cpu_percent(interval=None) / self._cpu_count
                    
                    if initial_cpu_time > 0:
                        try:
                            curr_times = proc.cpu_times()
                            delta_cpu = (curr_times.user + curr_times.system) - initial_cpu_time
                            if delta_cpu > 0 and duration > 0:
                                avg_cpu = min((delta_cpu / duration) * 100 / self._cpu_count, 100.0)
                                if cpu == 0:
                                    cpu = avg_cpu
                        except Exception:
                            pass

                    rss = cast(int, proc.memory_info().rss)
                    mem_mb = rss / (1024 * 1024)
                    
                if category in self._history:
                    self._history[category]["cpu"].append(cpu)
                    self._history[category]["memory_mb"].append(mem_mb)
            except Exception:
                pass

        stats = {
            "duration": duration,
            "max_cpu": 0.0,
            "max_mem": 0.0,
            "avg_cpu": 0.0,
            "avg_mem": 0.0
        }
        
        if category in self._history:
            cpu_hist = list(self._history[category]["cpu"])
            mem_hist = list(self._history[category]["memory_mb"])
            
            if cpu_hist:
                stats["max_cpu"] = min(max(cpu_hist), 100.0)
                stats["avg_cpu"] = min(sum(cpu_hist) / len(cpu_hist), 100.0)
            
            if mem_hist:
                stats["max_mem"] = max(mem_hist)
                stats["avg_mem"] = sum(mem_hist) / len(mem_hist)
                
        self.stop_monitoring(category)
        return stats


    def add_screenshot_history(self, wp_id: str, output_path: str, stats: dict[str, float]) -> None:
        if not self._config:
            return
        raw_existing = self._config.get("screenshot_history", [])
        if isinstance(raw_existing, list):
            history: list[dict[str, object]] = []
            for item in cast(list[object], raw_existing):
                if isinstance(item, dict):
                    history.append(cast(dict[str, object], item))
        else:
            history = []
        record: dict[str, object] = {
            "timestamp": time.time(),
            "wp_id": str(wp_id),
            "output_path": output_path,
            "duration": stats.get("duration", 0),
            "max_cpu": stats.get("max_cpu", 0),
            "max_mem": stats.get("max_mem", 0),
            "avg_cpu": stats.get("avg_cpu", 0),
            "avg_mem": stats.get("avg_mem", 0),
        }
        history.append(record)
        if len(history) > SCREENSHOT_HISTORY_LIMIT:
            history = history[-SCREENSHOT_HISTORY_LIMIT:]
        self._config.set("screenshot_history", history)

    def get_screenshot_history(self) -> list[dict[str, object]]:
        if not self._config:
            return []
        # Return a copy to prevent modification during iteration
        raw_history = self._config.get("screenshot_history", [])
        if not isinstance(raw_history, list):
            return []
        out: list[dict[str, object]] = []
        for item in cast(list[object], raw_history):
            if isinstance(item, dict):
                out.append(dict(cast(dict[str, object], item)))
        return out

    def clear_screenshot_history(self):
        if self._config:
            self._config.set("screenshot_history", [])

    def _ensure_thread_running(self):
        if not self._thread or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._monitor_loop, name="PerfMonitor", daemon=True)
            self._thread.start()

    def add_callback(self, callback: Callable[[_StatsPayload], None]) -> None:
        self._callbacks.append(callback)
        self._ensure_thread_running()

    def _monitor_loop(self):
        while not self._stop_event.is_set():
            stats: _StatsPayload = {
                "total": {
                    "cpu": 0.0,
                    "cpu_fmt": _format_cpu(0.0),
                    "memory_mb": 0.0,
                    "memory_fmt": _format_mem(0.0),
                    "threads": 0,
                    "history": {"cpu": [], "memory_mb": []},
                    "thread_names": {},
                },
                "details": {},
            }
            
            if "total" not in self._history:
                self._init_history("total")

            for category, proc in list(self._processes.items()):
                try:
                    # Upgrade wrapper process to real engine if available
                    if category in ("backend", "screenshot") and proc.name() != "linux-wallpaperengine":
                        real = self._find_real_process(proc.pid)
                        if real and real.name() == "linux-wallpaperengine":
                            _ = real.cpu_percent(interval=None)
                            self._processes[category] = real
                            proc = real
                    
                    with proc.oneshot():
                        cpu = proc.cpu_percent(interval=None) / self._cpu_count
                        rss = cast(int, proc.memory_info().rss)
                        mem_mb = rss / (1024 * 1024)
                        threads = int(proc.num_threads())
                        status = str(proc.status())
                        name = str(proc.name())

                    if category not in self._history:
                        self._init_history(category)
                    
                    self._history[category]["cpu"].append(cpu)
                    self._history[category]["memory_mb"].append(mem_mb)

                    stats["details"][category] = {
                        "pid": proc.pid,
                        "name": name,
                        "cpu": round(cpu, 1),
                        "cpu_fmt": _format_cpu(round(cpu, 1)),
                        "memory_mb": round(mem_mb, 1),
                        "memory_fmt": _format_mem(round(mem_mb, 1)),
                        "threads": threads,
                        "status": status,
                        "history": {
                            "cpu": list(self._history[category]["cpu"]),
                            "memory_mb": list(self._history[category]["memory_mb"])
                        }
                    }
                    
                    stats["total"]["cpu"] += cpu
                    stats["total"]["memory_mb"] += mem_mb
                    stats["total"]["threads"] += threads

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    if category != "frontend":
                        _ = self._processes.pop(category, None)
            
            total_cpu = round(float(stats["total"]["cpu"]), 1)
            total_mem = round(float(stats["total"]["memory_mb"]), 1)
            
            self._history["total"]["cpu"].append(total_cpu)
            self._history["total"]["memory_mb"].append(total_mem)
            
            stats["total"]["cpu"] = total_cpu
            stats["total"]["cpu_fmt"] = _format_cpu(total_cpu)
            stats["total"]["memory_mb"] = total_mem
            stats["total"]["memory_fmt"] = _format_mem(total_mem)
            stats["total"]["history"] = {
                "cpu": list(self._history["total"]["cpu"]),
                "memory_mb": list(self._history["total"]["memory_mb"])
            }
            
            all_thread_names = {}
            for category, proc in list(self._processes.items()):
                try:
                    names = _get_thread_names(proc.pid)
                    all_thread_names[category] = names
                except Exception:
                    all_thread_names[category] = []
            stats["total"]["thread_names"] = all_thread_names

            self._notify(stats)
            
            interval = self._interval
            if "screenshot" in self._processes:
                interval = 0.1
            time.sleep(interval)

    def _notify(self, stats: _StatsPayload) -> None:
        for cb in self._callbacks:
            try:
                cb(stats)
            except Exception as e:
                print(f"[PerformanceMonitor] Callback error: {e}")

```

---

### 📄 文件: `py_GUI/core/properties.py`

```python
import subprocess
from typing import List, Dict, Optional
from py_GUI.core.config import ConfigManager

class PropertiesManager:
    def __init__(self, config: ConfigManager):
        self._properties_cache: Dict[str, List[Dict]] = {}
        self._property_types: Dict[str, Dict[str, str]] = {}
        self._user_properties: Dict[str, Dict] = {}
        self._config = config
        self.load_from_config()

    def parse_properties_output(self, output: str) -> List[Dict]:
        """Parse --list-properties output"""
        properties = []
        lines = output.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or 'Running with:' in line:
                i += 1
                continue

            if ' - ' in line:
                parts = line.split(' - ', 1)
                name = parts[0].strip()
                prop_type = parts[1].strip()

                prop = {
                    'name': name,
                    'type': prop_type,
                    'text': '',
                    'value': None,
                    'min': 0,
                    'max': 100,
                    'step': 1,
                    'options': []
                }

                i += 1
                while i < len(lines):
                    subline = lines[i].strip()
                    if not subline:
                        i += 1
                        continue
                    if ' - ' in subline:
                        i -= 1
                        break

                    if subline.startswith('Text:'):
                        prop['text'] = subline[5:].strip()
                    elif subline.startswith('Value:'):
                        value_str = subline[6:].strip()
                        if prop_type == 'color':
                            prop['value'] = self._parse_color(value_str)
                        elif prop_type == 'boolean':
                            prop['value'] = value_str == '1'
                        else:
                            try:
                                prop['value'] = float(value_str)
                                if prop['value'] == int(prop['value']):
                                    prop['value'] = int(prop['value'])
                            except Exception:
                                prop['value'] = value_str
                    elif subline.startswith('Min:'):
                        prop['min'] = float(subline[4:].strip())
                    elif subline.startswith('Max:'):
                        prop['max'] = float(subline[5:].strip())
                    elif subline.startswith('Step:'):
                        prop['step'] = float(subline[5:].strip())
                    elif subline.startswith('Values:'):
                        i += 1
                        while i < len(lines) and '\t\t' in lines[i]:
                            opt_line = lines[i].strip()
                            if '=' in opt_line:
                                label, val = opt_line.split('=', 1)
                                prop['options'].append({'label': label.strip(), 'value': val.strip()})
                            i += 1
                        continue

                    i += 1
                properties.append(prop)
            else:
                i += 1
        return properties

    def _parse_color(self, value_str: str) -> tuple:
        """Parse color string "r,g,b" """
        parts = [p.strip() for p in value_str.split(',')]
        return (float(parts[0]), float(parts[1]), float(parts[2]))

    def get_properties(self, wp_id: str) -> List[Dict]:
        """Get wallpaper properties"""
        if wp_id in self._properties_cache:
            return self._properties_cache[wp_id]

        try:
            result = subprocess.run(
                ['linux-wallpaperengine', '--list-properties', wp_id],
                capture_output=True,
                text=True,
                timeout=5
            )
            properties = self.parse_properties_output(result.stdout)

            # Filter irrelevant properties
            properties = self._filter_properties(properties)

            self._properties_cache[wp_id] = properties
            # Store types
            self._property_types[wp_id] = {p['name']: p['type'] for p in properties}
            return properties
        except Exception as e:
            print(f"[PROPERTIES] Failed to get properties for {wp_id}: {e}")
            return []

    def _filter_properties(self, properties: List[Dict]) -> List[Dict]:
        """Filter out internal/UI properties"""
        filtered = []
        ui_keywords = ['ui_', 'ui_browse', 'scheme_']
        audio_keywords = ['volume', 'music', 'sound', 'bell']

        for prop in properties:
            name = prop.get('name', '').lower()
            text = prop.get('text', '').lower()

            should_hide = any(keyword in name or keyword in text for keyword in ui_keywords)
            is_audio_prop = any(keyword in name for keyword in audio_keywords)

            if not should_hide and not is_audio_prop:
                filtered.append(prop)
            else:
                pass 

        return filtered

    def get_property_type(self, wp_id: str, prop_name: str) -> str:
        if wp_id in self._property_types and prop_name in self._property_types[wp_id]:
            return self._property_types[wp_id][prop_name]
        return 'unknown'

    def load_from_config(self):
        props_data = self._config.get("wallpaperProperties", {})
        self._user_properties = props_data


    def save_to_config(self):
        self._config.set("wallpaperProperties", self._user_properties)

    def get_user_property(self, wp_id: str, prop_name: str):
        if wp_id in self._user_properties and prop_name in self._user_properties[wp_id]:
            return self._user_properties[wp_id][prop_name]
        return None

    def set_user_property(self, wp_id: str, prop_name: str, value):
        if wp_id not in self._user_properties:
            self._user_properties[wp_id] = {}
        self._user_properties[wp_id][prop_name] = value
        self.save_to_config()

    def format_property_value(self, prop_type: str, value) -> str:
        if isinstance(value, (tuple, list)):
            return ",".join(map(str, value))
        elif isinstance(value, bool):
            return '1' if value else '0'
        elif isinstance(value, float):
            return f"{value:.6f}"
        return str(value)

```

---

### 📄 文件: `py_GUI/core/screen.py`

```python
import subprocess
from typing import List, Optional

class ScreenManager:
    def __init__(self):
        self._screens_cache: Optional[List[str]] = None

    def get_screens(self) -> List[str]:
        """Get list of available screens"""
        if self._screens_cache is not None:
            return self._screens_cache

        screens = []
        try:
            result = subprocess.run(
                ['xrandr', '--query'],
                capture_output=True,
                text=True,
                timeout=5
            )
            for line in result.stdout.split('\n'):
                if ' connected' in line:
                    screen_name = line.split()[0]
                    screens.append(screen_name)
        except Exception as e:
            print(f"[SCREEN] Failed to get screens: {e}")

        self._screens_cache = screens
        return screens

    def get_first_screen(self) -> Optional[str]:
        """Get the first detected screen.
        
        Returns:
            First screen name if available, None otherwise.
        """
        screens = self.get_screens()
        return screens[0] if screens else None

    def get_primary_screen(self) -> Optional[str]:
        """Get the primary screen via xrandr, falling back to first screen.
        
        Returns:
            Primary screen name if available, first screen if primary not found,
            None if no screens available.
        """
        try:
            result = subprocess.run(
                ['xrandr', '--query'],
                capture_output=True,
                text=True,
                timeout=5
            )
            for line in result.stdout.split('\n'):
                if ' connected primary' in line:
                    return line.split()[0]
        except Exception as e:
            print(f"[SCREEN] Failed to get primary screen: {e}")
        
        # Fallback to first screen
        return self.get_first_screen()

    def refresh(self):
        """Refresh screen list"""
        self._screens_cache = None
        return self.get_screens()

```

---

### 📄 文件: `py_GUI/core/updater.py`

```python
import json
import threading
import urllib.request
import urllib.error
from typing import Callable, Optional


class UpdateChecker:
    """Check for updates from GitHub releases."""
    
    GITHUB_API_URL = "https://api.github.com/repos/Suhoiyis/gui-for-linux-wallpaperengine/releases/latest"
    TIMEOUT = 5
    
    def check_update(self, current_version: str, callback: Callable[[Optional[str], Optional[str], bool], None]) -> None:
        """
        Check for updates in a background thread.
        
        Args:
            current_version: Current version string (e.g., "0.10.3" or "v0.10.3")
            callback: Function called with (latest_version, release_url, has_update)
                     - latest_version: Version from GitHub tag_name or None on error
                     - release_url: URL to the release page or None on error
                     - has_update: True if update available, False otherwise
        """
        thread = threading.Thread(
            target=self._check_update_thread,
            args=(current_version, callback),
            daemon=True
        )
        thread.start()
    
    def _check_update_thread(self, current_version: str, callback: Callable[[Optional[str], Optional[str], bool], None]) -> None:
        """Background thread worker for checking updates."""
        try:
            req = urllib.request.Request(
                self.GITHUB_API_URL,
                headers={'User-Agent': 'Linux-Wallpaper-Engine-GUI/UpdateChecker'}
            )
            with urllib.request.urlopen(req, timeout=self.TIMEOUT) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            tag_name = data.get('tag_name', '')
            release_url = data.get('html_url', '')
            
            latest_version = self._normalize_version(tag_name)
            current_normalized = self._normalize_version(current_version)
            
            has_update = self._compare_versions(current_normalized, latest_version)
            
            callback(latest_version, release_url, has_update)
            
        except urllib.error.HTTPError as e:
            if e.code == 404:
                callback("0.0.0", "", False)
            elif e.code == 403:
                callback("ERROR:RATE_LIMIT", None, False)
            else:
                callback(None, None, False)
        except (urllib.error.URLError, json.JSONDecodeError, Exception):
            callback(None, None, False)
    
    @staticmethod
    def _normalize_version(version: str) -> str:
        """Remove 'v' prefix from version string."""
        if version.startswith('v'):
            return version[1:]
        return version
    
    @staticmethod
    def _compare_versions(current: str, latest: str) -> bool:
        try:
            def parse_numeric_parts(version_str):
                base_version = version_str.split('-')[0].split('+')[0]
                return [int(part) for part in base_version.split('.')]
            
            current_parts = parse_numeric_parts(current)
            latest_parts = parse_numeric_parts(latest)
            
            max_len = max(len(current_parts), len(latest_parts))
            current_parts.extend([0] * (max_len - len(current_parts)))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            
            for curr_val, lat_val in zip(current_parts, latest_parts):
                if lat_val > curr_val:
                    return True
                elif lat_val < curr_val:
                    return False
            
            return False
        except (ValueError, AttributeError, IndexError):
            return False

```

---

### 📄 文件: `py_GUI/core/wallpaper.py`

```python
import os
import json
import gc
import shutil
import io
from typing import Dict, Optional, List
import gi

gi.require_version('Gdk', '4.0')
from gi.repository import Gdk, GdkPixbuf, GLib

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from py_GUI.const import WORKSHOP_PATH
from py_GUI.utils import get_folder_size

import re

class WallpaperManager:
    def __init__(self, workshop_path: str = WORKSHOP_PATH):
        self.workshop_path = workshop_path
        self._wallpapers: Dict[str, Dict] = {}
        self._texture_cache: Dict[str, Gdk.Texture] = {}
        self._cache_max_size = 80
        self.last_scan_error: Optional[str] = None
        self.scan_errors: List[str] = []
        # Try to locate Steam appworkshop manifest
        self.manifest_path = self._find_manifest_path()

    def _find_manifest_path(self) -> Optional[str]:
        # Typical paths for appworkshop_431960.acf
        # 1. Same level as workshop/content/431960 -> workshop/appworkshop_431960.acf
        if not self.workshop_path:
            return None
            
        # workshop_path is usually .../workshop/content/431960
        # We need to go up two levels to .../workshop/
        try:
            content_dir = os.path.dirname(self.workshop_path) # .../content
            workshop_dir = os.path.dirname(content_dir)       # .../workshop
            
            manifest = os.path.join(workshop_dir, "appworkshop_431960.acf")
            if os.path.exists(manifest):
                return manifest
        except Exception:
            pass
            
        return None

    def _remove_from_manifest(self, folder_id: str) -> bool:
        """Remove item from appworkshop_431960.acf to prevent Steam re-download"""
        if not self.manifest_path or not os.path.exists(self.manifest_path):
            return False
            
        try:
            with open(self.manifest_path, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            skip = False
            brace_count = 0
            
            # Simple ACF parser/modifier
            # We look for "folder_id" key and remove its block
            
            i = 0
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()
                
                # Check for item ID block start
                if f'"{folder_id}"' in stripped:
                    # Found the item, skip this line and the following block
                    skip = True
                    brace_count = 0
                    
                    # If line has opening brace, increment
                    if '{' in stripped:
                        brace_count += 1
                    
                    # If block starts on next line
                    if brace_count == 0:
                        # Check next line for brace
                        if i + 1 < len(lines) and '{' in lines[i+1]:
                            i += 1
                            brace_count += 1
                            
                    i += 1
                    continue
                
                if skip:
                    if '{' in stripped:
                        brace_count += 1
                    if '}' in stripped:
                        brace_count -= 1
                    
                    # If braces balanced back to 0, we are done skipping
                    if brace_count == 0:
                        skip = False
                    
                    i += 1
                    continue
                
                new_lines.append(line)
                i += 1
            
            # Write back
            with open(self.manifest_path, 'w') as f:
                f.writelines(new_lines)
                
            return True
        except Exception as e:
            print(f"[ERROR] Failed to update manifest: {e}")
            return False

    def get_wallpaper(self, wallpaper_id: str) -> Optional[Dict]:
        return self._wallpapers.get(str(wallpaper_id))

    def get_sorted_wallpapers(self, sort_mode: str = "random", reverse: bool = False) -> List[str]:
        """Get sorted list of wallpaper IDs"""
        if not self._wallpapers:
            return []
            
        # "random" implies shuffling, but typically for sequential cycling we just shuffle once or pick randomly.
        # However, for consistency with the UI dropdown, "random" usually means "pick random next", 
        # but if we want a "randomized playlist" we'd return a shuffled list.
        # The prompt asks for "Random" as an option in the dropdown alongside Size/Title.
        # If sort_mode is 'random', we can just return keys (or shuffled keys). 
        # But 'random' cycling in App is usually stateless.
        # Let's support the explicit sorts here.

        items = list(self._wallpapers.items())
        
        if sort_mode == "title":
            items.sort(key=lambda x: x[1].get('title', '').lower(), reverse=reverse)
        elif sort_mode == "size":
            # Default to largest first (descending) if direction not specified?
            # Actually, standard sort usually means smallest first (ascending).
            # If the user wants descending, we need a flag or separate option.
            # But here we only have "Size" option. Let's default to Small -> Large (Ascending) 
            # as is standard for lists, UNLESS 'reverse' is True.
            items.sort(key=lambda x: x[1].get('size', 0), reverse=reverse)
        elif sort_mode == "size_desc":
             items.sort(key=lambda x: x[1].get('size', 0), reverse=True)
        elif sort_mode == "type":
            items.sort(key=lambda x: x[1].get('type', '').lower(), reverse=reverse)
        elif sort_mode == "id":
            items.sort(key=lambda x: x[0], reverse=reverse)
        # For 'random', we don't really sort, caller handles it.
        
        return [item[0] for item in items]

    def scan(self) -> Dict[str, Dict]:
        self._wallpapers.clear()
        self.last_scan_error = None
        self.scan_errors = []
        
        if not os.path.exists(self.workshop_path):
            self.last_scan_error = f"Workshop directory not found: {self.workshop_path}"
            return self._wallpapers
        
        if not os.path.isdir(self.workshop_path):
            self.last_scan_error = f"Workshop path is not a directory: {self.workshop_path}"
            return self._wallpapers

        entries = []
        try:
            entries = sorted(os.listdir(self.workshop_path))
        except PermissionError:
            self.last_scan_error = f"Permission denied: {self.workshop_path}"
            return self._wallpapers
        except OSError as e:
            self.last_scan_error = f"Cannot read directory: {e}"
            return self._wallpapers

        for folder in entries:
            json_path = os.path.join(self.workshop_path, folder, "project.json")
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r') as f:
                        data = json.load(f)
                        preview_file = data.get("preview", "preview.jpg")
                        folder_path = os.path.join(self.workshop_path, folder)
                        self._wallpapers[folder] = {
                            "id": folder,
                            "title": data.get("title", "Unknown"),
                            "preview": os.path.join(folder_path, preview_file),
                            "description": data.get("description", ""),
                            "type": data.get("type", "Scene"),
                            "tags": data.get("tags", []),
                            "file": data.get("file", ""),
                            "contentrating": data.get("contentrating", ""),
                            "version": data.get("version", ""),
                            "size": get_folder_size(folder_path),
                        }
                except json.JSONDecodeError as e:
                    self.scan_errors.append(f"Invalid JSON in {folder}: {e}")
                except Exception as e:
                    self.scan_errors.append(f"Error reading {folder}: {e}")
        
        if not self._wallpapers and not self.last_scan_error:
            self.last_scan_error = f"No wallpapers found in: {self.workshop_path}"
        
        return self._wallpapers

    def get_texture(self, path: str, size: int = 170) -> Optional[Gdk.Texture]:
        """Get thumbnail texture with LRU cache"""
        cache_key = f"{path}_{size}"
        if cache_key in self._texture_cache:
            return self._texture_cache[cache_key]

        if not os.path.exists(path):
            return None

        if path.lower().endswith('.gif'):
            try:
                pixbuf = None
                if HAS_PIL:
                    with Image.open(path) as img:
                        n_frames = getattr(img, 'n_frames', 1)
                        target_frame = min(15, n_frames - 1) if n_frames > 1 else 0
                        img.seek(target_frame)
                        
                        thumb_img = img.convert("RGBA")
                        thumb_img.thumbnail((size, size), Image.Resampling.LANCZOS)
                        
                        buf = io.BytesIO()
                        thumb_img.save(buf, format="PNG")
                        data = buf.getvalue()
                        
                        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
                        loader.write(data)
                        loader.close()
                        pixbuf = loader.get_pixbuf()
                else:
                    anim = GdkPixbuf.PixbufAnimation.new_from_file(path)
                    pixbuf = anim.get_static_image()
                
                if pixbuf:
                    scaled = pixbuf.scale_simple(size, size, GdkPixbuf.InterpType.BILINEAR)
                    texture = Gdk.Texture.new_for_pixbuf(scaled)
                    self._texture_cache[cache_key] = texture
                    return texture
            except Exception:
                pass

        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, size, size, True)
            texture = Gdk.Texture.new_for_pixbuf(pixbuf)
            del pixbuf  # Immediate release

            # LRU Cache: clear half if full
            if len(self._texture_cache) >= self._cache_max_size:
                keys = list(self._texture_cache.keys())[:self._cache_max_size // 2]
                for k in keys:
                    del self._texture_cache[k]
                gc.collect()

            self._texture_cache[cache_key] = texture
            return texture
        except Exception:
            return None

    def clear_cache(self):
        """Clear texture cache"""
        self._texture_cache.clear()

    def delete_wallpaper(self, folder_id: str) -> bool:
        """Delete wallpaper folder"""
        if folder_id not in self._wallpapers:
            return False

        folder_path = os.path.join(self.workshop_path, folder_id)
        if not os.path.exists(folder_path):
            return False

        try:
            # 1. Update manifest to prevent re-download
            # self._remove_from_manifest(folder_id)
            
            # 2. Get preview path before deletion for cache clearing
            preview_path = self._wallpapers[folder_id].get('preview', '')

            # 3. Delete folder and contents
            shutil.rmtree(folder_path)

            # 4. Remove from list
            del self._wallpapers[folder_id]

            # 5. Clear from cache
            if preview_path:
                cache_keys_to_remove = [k for k in self._texture_cache.keys() if k.startswith(preview_path)]
                for key in cache_keys_to_remove:
                    del self._texture_cache[key]
            
            gc.collect()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to delete wallpaper {folder_id}: {e}")
            return False

```

---

### 📄 文件: `py_GUI/main.py`

```python
#!/usr/bin/env python3
from py_GUI.ui.app import main

if __name__ == '__main__':
    main()

```

---

### 📄 文件: `py_GUI/ui/__init__.py`

```python

```

---

### 📄 文件: `py_GUI/ui/app.py`

```python
import sys
import os
import platform
import shutil
import html
import gi

import socket
import threading

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, Gdk, GLib

from py_GUI.const import CSS_STYLE, APP_ID, WORKSHOP_PATH, VERSION
from py_GUI.core.config import ConfigManager
from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.screen import ScreenManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.logger import LogManager
from py_GUI.core.nickname import NicknameManager
from py_GUI.core.history import HistoryManager
from py_GUI.utils import markdown_to_pango

from py_GUI.ui.components.navbar import NavBar
from py_GUI.ui.components.history_dialog import HistoryDialog
from py_GUI.ui.components.welcome_dialog import WelcomeDialog
from py_GUI.ui.pages.wallpapers import WallpapersPage
from py_GUI.ui.pages.settings import SettingsPage
from py_GUI.ui.pages.performance import PerformancePage
from py_GUI.ui.tray import TrayIcon
from py_GUI.ui.compact_window import CompactWindow
from py_GUI.core.updater import UpdateChecker
from py_GUI.core.integrations import AppIntegrator


def get_debug_info():
    import platform, sys, shutil, os
    from gi.repository import Gtk, Adw
    
    info = []
    info.append("System Environment")
    info.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    try:
        os_info = f"{platform.system()} {platform.release()}"
        info.append(f"OS: {os_info}")
    except Exception:
        info.append("OS: Unknown")
    
    try:
        py_version = sys.version.split()[0]
        info.append(f"Python: {py_version}")
    except Exception:
        info.append("Python: Unknown")
    
    try:
        gtk_version = f"{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}"
        info.append(f"GTK: {gtk_version}")
    except Exception:
        info.append("GTK: Unknown")
    
    try:
        adw_version = f"{Adw.get_major_version()}.{Adw.get_minor_version()}.{Adw.get_micro_version()}"
        info.append(f"Libadwaita: {adw_version}")
    except Exception:
        info.append("Libadwaita: Unknown")
    
    try:
        display_server = os.environ.get('XDG_SESSION_TYPE', 'unknown').capitalize()
        info.append(f"Display Server: {display_server}")
    except Exception:
        info.append("Display Server: Unknown")
    
    try:
        backend_found = shutil.which('linux-wallpaperengine') is not None
        backend_status = "✓ Found" if backend_found else "✗ Not found"
        info.append(f"Backend (linux-wallpaperengine): {backend_status}")
    except Exception:
        info.append("Backend: Unknown")
    
    return "\n".join(info)

def get_latest_changelog():
    import os
    import re
    changelog_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs/CHANGELOG.md")
    if not os.path.exists(changelog_path):
        return "<p>No changelog found.</p>"

    try:
        with open(changelog_path, "r", encoding="utf-8") as f:
            content = f.read()

        sections = re.split(r'\n## ', content)
        for section in sections:
            section = section.strip()
            if not section:
                continue

            is_version = section.startswith('v')
            is_latest = "最新更新" in section

            if is_version or is_latest:
                lines = section.split('\n')
                header = lines[0].strip()
                body_lines = lines[1:]

                processed_lines = []
                in_list = False

                for line in body_lines:
                    line = line.strip()
                    if line.startswith('---'):
                        break

                    if not line:
                        continue

                    if line.startswith('###'):
                        if in_list:
                            processed_lines.append("</ul>")
                            in_list = False
                        # Escape the text content before wrapping in tags
                        section_title = html.escape(line.replace('###', '').strip())
                        processed_lines.append(f"<p><em>{section_title}</em></p>")
                    elif line.startswith('-'):
                        if not in_list:
                            processed_lines.append("<ul>")
                            in_list = True
                        item_text = line.replace('-', '', 1).strip()
                        # Escape raw text first, then apply formatting
                        item_text = html.escape(item_text)
                        item_text = item_text.replace('**', '<em>', 1).replace('**', '</em>', 1)
                        processed_lines.append(f"  <li>{item_text}</li>")
                    else:
                        if in_list:
                            processed_lines.append("</ul>")
                            in_list = False
                        # Escape the paragraph text
                        escaped_line = html.escape(line)
                        processed_lines.append(f"<p>{escaped_line}</p>")

                if in_list:
                    processed_lines.append("</ul>")

                content_html = "\n".join(processed_lines)
                if not content_html.strip() or content_html.strip() == "(暂无)":
                    continue

                # Escape header before wrapping in tags
                escaped_header = html.escape(header)
                return f"<p><em>{escaped_header}</em></p>" + content_html
    except Exception as e:
        return f"<p>Error reading changelog: {str(e)}</p>"

    return "<p>Check CHANGELOG.md for details.</p>"


class WallpaperApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )
        self.config = ConfigManager()
        self.log_manager = LogManager()
        self.history_manager = HistoryManager(self.config)
        
        workshop_path = self.config.get("workshopPath", WORKSHOP_PATH)
        self.wp_manager = WallpaperManager(workshop_path)
        self.prop_manager = PropertiesManager(self.config)
        self.screen_manager = ScreenManager()
        self.nickname_manager = NicknameManager(self.config)
        self.controller = WallpaperController(self.config, self.prop_manager, self.log_manager, self.screen_manager)
        self.controller.wp_manager = self.wp_manager
        self.controller.nickname_manager = self.nickname_manager
        self.controller.history_manager = self.history_manager

        self.start_hidden = False
        self.cli_actions = []
        self.initialized = False
        self._is_first_activation = True
        self.cycle_timer_id = None
        
        self.app_integrator = AppIntegrator()
        self.update_checker = UpdateChecker()
        
        self.tray = TrayIcon(self)

    def do_command_line(self, command_line):
        argv = command_line.get_arguments()[1:]
        for arg in argv:
            if arg in ("--minimized", "--hidden"):
                if self.initialized:
                    self.cli_actions.append("hide")
                else:
                    self.start_hidden = True
            elif arg == "--show":
                self.cli_actions.append("show")
            elif arg == "--hide":
                self.cli_actions.append("hide")
            elif arg == "--toggle":
                self.cli_actions.append("toggle")
            elif arg == "--refresh":
                self.cli_actions.append("refresh")
            elif arg == "--apply-last":
                self.cli_actions.append("apply-last")
            elif arg == "--stop":
                self.cli_actions.append("stop")
            elif arg == "--random":
                self.cli_actions.append("random")
            elif arg == "--quit":
                self.cli_actions.append("quit")
        
        self.activate()
        return 0

    def do_activate(self):
        if self.initialized:
            if self._is_first_activation and not self.start_hidden:
                self.show_window()
            self._is_first_activation = False
            self.start_hidden = False
            self.consume_cli_actions()

            GLib.timeout_add(1500, self.update_tray_status)
            return

        # Load CSS
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS_STYLE.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Setup Icon Theme
        display = Gdk.Display.get_default()
        icon_theme = Gtk.IconTheme.get_for_display(display)
        
        # Add 'pic' directory to icon search path
        # py_GUI/ui/app.py -> .../linux-wallpaperengine-gui/
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        pic_path = os.path.join(base_path, "pic/icons")
        
        if os.path.exists(pic_path):
            icon_theme.add_search_path(pic_path)

        self.win = Gtk.ApplicationWindow(application=self)
        self.win.set_title("Linux Wallpaper Engine GUI")
        self.win.set_icon_name(APP_ID) # Matches GUI_rounded.png in pic/icons/
        self.win.set_default_size(1200, 800)
        self.win.set_size_request(1000, 700)
        self.win.connect("close-request", self.on_window_close)

        # Setup Actions
        self.setup_actions()

        self.toast_overlay = Adw.ToastOverlay()
        self.win.set_child(self.toast_overlay)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.toast_overlay.set_child(main_box)

        # Stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_vexpand(True)
        
        # Navbar
        screens = self.screen_manager.get_screens()
        selected_screen = (
            self.config.get("lastScreen")
            or self.screen_manager.get_primary_screen()
            or "eDP-1"
        )
        initial_link_state = (self.config.get("apply_mode") == "same")
        initial_compact_state = bool(self.config.get("compact_mode"))
        
        self.navbar = NavBar(
            self.stack, 
            screens=screens,
            selected_screen=selected_screen,
            on_home_enter=self.on_home_enter,
            on_screen_changed=self.on_navbar_screen_changed,
            on_link_toggled=self.on_navbar_link_toggled,
            on_restart_app=self.restart_app,
            on_compact_mode_toggled=self.on_compact_mode_toggled,
            initial_link_state=initial_link_state,
            initial_compact_state=initial_compact_state
        )
        main_box.append(self.navbar)
        main_box.append(self.stack)
        
        # Pages
        self.wallpapers_page = WallpapersPage(
            self.win, self.config, self.wp_manager,
            self.prop_manager, self.controller, self.log_manager,
            self.screen_manager, self.nickname_manager, self.show_toast
        )
        self.stack.add_named(self.wallpapers_page, "wallpapers")

        # Performance Page
        self.performance_page = PerformancePage(self.controller)
        self.stack.add_named(self.performance_page, "performance")

        self.settings_page = SettingsPage(
            self.win, self.config, self.screen_manager, self.log_manager, 
            self.controller, self.wp_manager, self.nickname_manager,
            on_cycle_changed=self.setup_cycle_timer,
            show_toast=self.show_toast
        )
        self.stack.add_named(self.settings_page, "settings")

        self.controller.set_toast_callback(self.show_toast)

        self.compact_win = CompactWindow(
            app=self,
            wp_manager=self.wp_manager,
            controller=self.controller,
            config=self.config,
            log_manager=self.log_manager,
            screen_manager=self.screen_manager,
            nickname_manager=self.nickname_manager,
            show_toast=self.show_toast,
            on_compact_mode_toggled=self.on_compact_mode_toggled,
            on_restart_app=self.restart_app
        )
        self.compact_win.set_icon_name("GUI")

        self.wp_manager.scan()
        self.nickname_manager.cleanup(list(self.wp_manager._wallpapers.keys()))
        self.wallpapers_page.refresh_wallpaper_grid()
        
        if self.wp_manager.last_scan_error:
            GLib.timeout_add(500, lambda: self.show_toast(f"⚠️ {self.wp_manager.last_scan_error}") or False)

        # Restore last session wallpapers
        active_monitors = self.config.get("active_monitors") or {}
        screens = self.screen_manager.get_screens()

        # Ensure lastScreen always points to a connected screen (fallback to first/primary)
        last_screen = self.config.get("lastScreen")
        if not last_screen or last_screen not in screens:
            last_screen = self.screen_manager.get_primary_screen() or (screens[0] if screens else "eDP-1")
            self.config.set("lastScreen", last_screen)

        if active_monitors:
            # Fill in missing lastWallpaper for CLI/apply-last correctness
            if not self.config.get("lastWallpaper"):
                if last_screen in active_monitors:
                    self.config.set("lastWallpaper", active_monitors[last_screen])
                elif active_monitors:
                    self.config.set("lastWallpaper", next(iter(active_monitors.values())))

            # Re-launch wallpapers using saved mapping
            self.controller.restart_wallpapers()
            GLib.timeout_add(300, self.wallpapers_page.update_active_wallpaper_label)
            # Do not override user selection; only select current if none
            GLib.timeout_add(350, lambda: self.wallpapers_page.show_current_wallpaper_in_sidebar(False))
        else:
            # Legacy fallback: apply last single wallpaper
            last_wp = self.config.get("lastWallpaper")
            if last_wp:
                self.wallpapers_page.select_wallpaper(last_wp)
                GLib.timeout_add(500, lambda: self.auto_apply(last_wp))

        if self.start_hidden:
            self.win.set_visible(False)
            self.compact_win.set_visible(False)
        elif initial_compact_state:
            self.win.set_visible(False)
            wp_ids = self.wallpapers_page._current_wp_ids
            self.compact_win.sync_from_main(wp_ids, None)
            self.compact_win.set_visible(True)
            self.compact_win.present()
            GLib.timeout_add(100, lambda: self.compact_win.present() or False)
        else:
            self.win.set_visible(True)
            self.win.present()
            GLib.timeout_add(100, lambda: self.win.present() or False)
        self.start_hidden = False
        
        self.initialized = True
        self._is_first_activation = False
        self.check_onboarding()
        self._check_shortcut_updates()
        self.setup_cycle_timer()

        self.start_ipc_server()

        self.tray.start()
        
        if self.tray.process and self.tray.process.pid:
            self.controller.perf_monitor.start_monitoring("tray", self.tray.process.pid)
        
        self.consume_cli_actions()

        # 1. 延迟 1.5 秒发送初始状态
        GLib.timeout_add(1500, self.update_tray_status)
        
        # 2. 开启 1 秒一次的智能心跳守护线程 (通过 or True 强制保持循环)
        # 无论用户通过什么刁钻的方式在内部换了壁纸，托盘绝对会在 1 秒内发现并跟上！
        if not hasattr(self, '_tray_loop_started'):
            self._tray_loop_started = True
            GLib.timeout_add_seconds(1, lambda: self.update_tray_status() or True)

    def start_ipc_server(self):
        """监听来自 Rust 托盘的极速 Abstract Socket 指令 (0 文件残留)"""
        socket_name = os.getenv('LWG_IPC_SOCKET', f"lwg-ipc-{os.getuid()}")
        abstract_addr = f"\x00{socket_name}"

        def _server_thread():
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as srv:
                try:
                    # 🛡️ Copilot 建议的保护罩：防止多开应用时因地址被占用导致线程脏崩溃
                    srv.bind(abstract_addr)
                    srv.listen(5)
                except OSError as e:
                    # 将错误安全地抛给主线程的日志管理器，然后体面地结束这个冗余线程
                    GLib.idle_add(lambda: self.log_manager.add_info(f"IPC Server 绑定失败 (可能已有一个实例正在运行): {e}", "App"))
                    return

                while True:
                    try:
                        conn, _ = srv.accept()
                        with conn:
                            data = conn.recv(1024).decode().strip()
                            if not data: continue
                            
                            if data == "--show":
                                GLib.idle_add(self.show_window)
                            elif data == "--toggle":
                                GLib.idle_add(self.toggle_window)
                            elif data == "--stop":
                                GLib.idle_add(self.stop_wallpaper)
                            elif data == "--apply-last":
                                GLib.idle_add(self.apply_last_from_cli)
                            elif data == "--random":
                                GLib.idle_add(self.random_wallpaper)
                            elif data == "--quit":
                                GLib.idle_add(self.quit_app)
                    except Exception:
                        pass

        t = threading.Thread(target=_server_thread, daemon=True)
        t.start()

    def auto_apply(self, wp_id):
        if wp_id:
            self.controller.apply(wp_id)
            # Update UI state
            self.wallpapers_page.active_wp = wp_id
            wp = self.wp_manager._wallpapers.get(wp_id)
            if wp:
                self.wallpapers_page.active_wp_label.set_markup(markdown_to_pango(wp['title']))
            
            # 【新增】确保自动应用壁纸时激活计时器
            self.setup_cycle_timer()
        GLib.timeout_add(500, self.update_tray_status)
        return False

    def on_window_close(self, win):
        self.hide_window()
        return True

    def show_window(self):
        is_compact = self.config.get("compact_mode", False)
        if is_compact:
            self.compact_win.set_visible(True)
            self.compact_win.present()
            # 加上这句：给 WM 100ms 的反应时间后，再强行夺取一次焦点
            GLib.timeout_add(100, lambda: self.compact_win.present() or False)
        else:
            self.win.set_visible(True)
            self.win.present()
            # 加上这句：给 WM 100ms 的反应时间后，再强行夺取一次焦点
            GLib.timeout_add(100, lambda: self.win.present() or False)

    def show_toast(self, message: str, timeout: int = 3):
        if hasattr(self, 'toast_overlay'):
            toast = Adw.Toast.new(message)
            toast.set_timeout(timeout)
            self.toast_overlay.add_toast(toast)

    def hide_window(self):
        self.win.set_visible(False)
        if hasattr(self, 'compact_win'):
            self.compact_win.set_visible(False)

    def toggle_window(self):
        """智能 Toggle 逻辑 (Smart Toggle)"""
        is_compact = self.config.get("compact_mode", False)
        
        # 确定当前应该操作哪个窗口
        target_win = getattr(self, 'compact_win', None) if is_compact else self.win

        if not target_win:
            self.show_window()
            return

        # 核心逻辑：
        # is_active() 能够判断该窗口是否是当前桌面系统里“正在被聚焦/置顶”的活跃窗口
        if target_win.get_visible() and target_win.is_active():
            # 状态 1：窗口已打开，并且就在最前面（拥有焦点） -> 隐藏它
            self.hide_window()
        else:
            # 状态 2：窗口被关了，或者被别的窗口挡住了，或者在别的工作区 -> 唤醒并置顶！
            self.show_window()

    def on_home_enter(self):
        try:
            self.wallpapers_page.update_active_wallpaper_label()
            self.wallpapers_page.show_current_wallpaper_in_sidebar(False)
        except Exception:
            pass

    def on_navbar_screen_changed(self, screen: str):
        self.config.set("lastScreen", screen)
        if hasattr(self, 'wallpapers_page'):
            self.wallpapers_page.selected_screen = screen
            self.wallpapers_page.update_active_wallpaper_label()

    def on_navbar_link_toggled(self, is_linked: bool):
        mode = "same" if is_linked else "diff"
        self.config.set("apply_mode", mode)
        if hasattr(self, 'wallpapers_page'):
            self.wallpapers_page.apply_mode = mode
            self.log_manager.add_info(f"Apply mode changed to: {mode}", "App")

    def on_compact_mode_toggled(self, is_compact: bool):
        self.config.set("compact_mode", is_compact)
        
        if is_compact:
            self.win.set_visible(False)
            wp_ids = self.wallpapers_page._current_wp_ids
            selected_wp = self.wallpapers_page.selected_wp
            self.compact_win.sync_from_main(wp_ids, selected_wp)
            self.compact_win.set_visible(True)
            self.compact_win.present()
        else:
            self.compact_win.set_visible(False)
            self.win.set_visible(True)
            self.win.present()
            self.navbar.set_compact_active(False)
        
        self.log_manager.add_info(f"Compact mode: {'enabled' if is_compact else 'disabled'}", "App")

    def refresh_from_cli(self):
        self.wallpapers_page.on_reload_wallpapers(None)

    def apply_last_from_cli(self):
        last_wp = self.config.get("lastWallpaper")
        if last_wp:
            self.auto_apply(last_wp)

    def consume_cli_actions(self):
        if not self.cli_actions: return
        actions = list(self.cli_actions)
        self.cli_actions.clear()
        
        for action in actions:
            if action == "show": self.show_window()
            elif action == "hide": self.hide_window()
            elif action == "toggle": self.toggle_window()
            elif action == "refresh": self.refresh_from_cli()
            elif action == "apply-last": self.apply_last_from_cli()
            elif action == "stop": self.stop_wallpaper()
            elif action == "random": self.random_wallpaper()
            elif action == "quit": self.quit_app()

    def stop_wallpaper(self):
        # Tray stop means STOP ALL
        self.controller.stop()
        self.config.set("active_monitors", {})
        self.wallpapers_page.update_active_wallpaper_label()

        # 【新增】停止播放时，顺便把轮换计时器也停掉
        self.setup_cycle_timer()

        GLib.timeout_add(500, self.update_tray_status)

    def update_tray_status(self):
        """利用 Pango Markup 增强多屏 ToolTip，并附带状态 Flag 让 Rust 切换图标"""
        import html
        try:
            active = self.config.get("active_monitors", {})
            text = "Stopped"
            state_flag = "STOPPED"  # 👈 默认状态为停止
            
            if active:
                state_flag = "ACTIVE"  # 👈 如果有壁纸，状态改为运行
                if len(active) == 1:
                    ui_name = self.wallpapers_page.active_wp_label.get_text()
                    if not ui_name or ui_name in ["-", "None"]:
                        ui_name = "Loading..."
                    safe_name = html.escape(ui_name)
                    text = f"<b>Running:</b> <i>{safe_name}</i>"
                else:
                    # ... (这里的多屏遍历拼接逻辑保持完全不变) ...
                    names = []
                    for screen_name, wp_id in active.items():
                        display_name = wp_id
                        wp = getattr(self, 'wp_manager', None) and self.wp_manager._wallpapers.get(wp_id)
                        if wp:
                            try:
                                res = self.nickname_manager.get_display_name(wp)
                                display_name = res[0] if isinstance(res, tuple) else res
                            except Exception:
                                display_name = wp.get("title", wp_id)
                        
                        if len(display_name) > 18:
                            display_name = display_name[:17] + "…"
                        
                        safe_screen = html.escape(screen_name)
                        safe_display = html.escape(display_name)
                        names.append(f"  • <b>{safe_screen}</b>: <i>{safe_display}</i>")
                    
                    joined_names = "\n".join(names)
                    text = f"<b>Running:</b>\n{joined_names}"
            
            # ✨ 核心改动：把状态和文本用 "|" 拼起来一起发过去
            payload = f"{state_flag}|{text}"
            
            if getattr(self, '_last_tray_text', None) != payload:
                self.tray.update_tooltip(payload)
                self._last_tray_text = payload

        except Exception as e:
            from py_GUI.ui.tray import log_main
            log_main(f"Error computing tray status: {e}")

        return False

    def random_wallpaper(self):
        # Triggered by cycle timer or CLI or Menu
        # Cycle order logic
        cycle_order = self.config.get("cycleOrder") or "random"
        active_monitors = dict(self.config.get("active_monitors", {}) or {})

        screens = self.screen_manager.get_screens()
         
        # If no monitors active, activate on the last used screen or first available
        if not active_monitors:
            target = (
                self.config.get("lastScreen") 
                or self.screen_manager.get_primary_screen() 
                or (screens[0] if screens else "eDP-1")
            )
            active_monitors[target] = None # Placeholder
            
        all_wps = list(self.wp_manager._wallpapers.keys())
        if not all_wps: return

        import random
        new_monitors = {}
        
        # Get sorted list if needed
        sorted_ids = []
        if cycle_order != "random":
             sorted_ids = self.wp_manager.get_sorted_wallpapers(cycle_order)
             # Fallback to random if sort fails or empty
             if not sorted_ids:
                 sorted_ids = all_wps
                 cycle_order = "random"

        for scr in active_monitors.keys():
            if scr in screens:
                if cycle_order == "random":
                    wp_id = random.choice(all_wps)
                else:
                    # Sequential logic
                    current_wp = active_monitors.get(scr)
                    next_index = 0
                    if current_wp and current_wp in sorted_ids:
                        current_index = sorted_ids.index(current_wp)
                        next_index = (current_index + 1) % len(sorted_ids)
                    else:
                        # If current not found or None, start from 0
                        next_index = 0
                    
                    wp_id = sorted_ids[next_index]

                new_monitors[scr] = wp_id
        
        if new_monitors:
            self.config.set("active_monitors", new_monitors)
            # Update lastScreen/lastWallpaper for proper restore & tray apply-last
            primary_screen = self.config.get("lastScreen")
            if primary_screen not in new_monitors:
                primary_screen = next(iter(new_monitors.keys()))
                self.config.set("lastScreen", primary_screen)

            self.config.set("lastWallpaper", new_monitors.get(primary_screen))

            self.controller.restart_wallpapers()
            self.wallpapers_page.update_active_wallpaper_label()
            
            self.log_manager.add_info(f"Cycled wallpaper ({cycle_order})", "App")
            
            # 【新增】每次切完随机壁纸，重置/启动一轮新的倒计时
            self.setup_cycle_timer()

        GLib.timeout_add(500, self.update_tray_status)

    def on_cycle_trigger(self):
        self.log_manager.add_info("Cycling wallpaper...", "App")
        self.random_wallpaper()
        
        # 【终极修复】必须返回 False！
        # 因为 random_wallpaper 内部会调用 setup_cycle_timer 创建全新的计时器。
        # 如果这里返回 True，旧计时器就会被 GLib 强行复活，变成无法被 stop 杀掉的幽灵！
        return False

    def setup_cycle_timer(self):
        if self.cycle_timer_id:
            GLib.source_remove(self.cycle_timer_id)
            self.cycle_timer_id = None
            
        # 获取当前正在播放的显示器字典
        active_monitors = self.config.get("active_monitors", {})
            
        # 只有在设置开启，且当前确有壁纸在播放时，才启动计时器
        if self.config.get("cycleEnabled") and active_monitors:
            interval_mins = self.config.get("cycleInterval") or 15
            # Minimum 1 minute safety
            interval_mins = max(1, interval_mins)
            self.cycle_timer_id = GLib.timeout_add_seconds(
                interval_mins * 60, 
                self.on_cycle_trigger
            )
            self.log_manager.add_info(f"Wallpaper cycling enabled (every {interval_mins} mins)", "App")
        else:
            # 打印更精准的日志状态
            state = "disabled" if not self.config.get("cycleEnabled") else "paused (no active wallpaper)"
            self.log_manager.add_info(f"Wallpaper cycling {state}", "App")

    def check_onboarding(self):
        needs_onboarding = not self.config.get("onboarding_completed", False) and not self.history_manager.has_history()
        if needs_onboarding:
            self.show_welcome_wizard()

    def _check_shortcut_updates(self):
        try:
            self.app_integrator.check_and_update_shortcut()
            self.log_manager.add_info("App shortcuts updated", "App")
        except Exception as e:
            self.log_manager.add_info(f"Shortcut update check skipped: {str(e)}", "App")

    def quit_app(self):
        self.controller.stop()
        self.tray.stop()
        self.quit()

    def restart_app(self):
        self.log_manager.add_info("Restarting application...", "App")
        self.controller.stop()
        self.tray.stop()
        
        import os
        import sys
        import subprocess
        
        # 提取去掉首位脚本名和隐藏参数后的干净参数
        args = [arg for arg in sys.argv[1:] if arg not in ("--hidden", "--minimized")]
        
        appimage_path = os.environ.get("APPIMAGE")
        if appimage_path:
            # 【AppImage 环境重启】
            # 使用外部文件的绝对路径，启动一个完全独立的新会话 (start_new_session=True)
            # 这样新进程就不会受当前进程 FUSE 销毁的影响
            cmd = [appimage_path] + args
            subprocess.Popen(cmd, start_new_session=True, cwd=os.path.expanduser("~"))
            self.quit()
            sys.exit(0)
        else:
            # 【源码环境重启】
            # 传统的进程替换方式
            cmd = [sys.executable, sys.argv[0]] + args
            os.execv(sys.executable, cmd)

    def setup_actions(self):
        action_apply = Gio.SimpleAction.new("apply", GLib.VariantType.new("s"))
        action_apply.connect("activate", self.on_action_apply)
        self.win.add_action(action_apply)

        action_stop = Gio.SimpleAction.new("stop", None)
        action_stop.connect("activate", self.on_action_stop)
        self.win.add_action(action_stop)

        action_delete = Gio.SimpleAction.new("delete", GLib.VariantType.new("s"))
        action_delete.connect("activate", self.on_action_delete)
        self.win.add_action(action_delete)
        
        action_open_folder = Gio.SimpleAction.new("open_folder", GLib.VariantType.new("s"))
        action_open_folder.connect("activate", self.on_action_open_folder)
        self.win.add_action(action_open_folder)
        
        action_refresh = Gio.SimpleAction.new("refresh", None)
        action_refresh.connect("activate", self.on_action_refresh)
        self.win.add_action(action_refresh)
        
        action_restart = Gio.SimpleAction.new("restart", None)
        action_restart.connect("activate", self.on_action_restart)
        self.win.add_action(action_restart)
        
        action_about = Gio.SimpleAction.new("about", None)
        action_about.connect("activate", self.on_action_about)
        self.win.add_action(action_about)
        
        action_quit_app = Gio.SimpleAction.new("quit_app", None)
        action_quit_app.connect("activate", self.on_action_quit_request)
        self.win.add_action(action_quit_app)
        
        action_show_history = Gio.SimpleAction.new("show_history", None)
        action_show_history.connect("activate", self.on_action_show_history)
        self.win.add_action(action_show_history)
        
        action_welcome = Gio.SimpleAction.new("welcome", None)
        action_welcome.connect("activate", self.on_action_welcome)
        self.win.add_action(action_welcome)
        
        action_check_update = Gio.SimpleAction.new("check_update", None)
        action_check_update.connect("activate", self.on_action_check_update)
        self.win.add_action(action_check_update)

    def on_action_apply(self, action, param):
        wp_id = param.get_string()
        if wp_id:
            self.wallpapers_page.select_wallpaper(wp_id)
            self.wallpapers_page.apply_wallpaper(wp_id)
            self.setup_cycle_timer()

            GLib.timeout_add(500, self.update_tray_status)

    def on_action_stop(self, action, param):
        self.stop_wallpaper()

    def on_action_delete(self, action, param):
        wp_id = param.get_string()
        if wp_id:
            self.wallpapers_page.delete_wallpaper(wp_id)
            
    def on_action_open_folder(self, action, param):
        wp_id = param.get_string()
        if wp_id:
            self.wallpapers_page.open_wallpaper_folder(wp_id)

    def on_action_refresh(self, action, param):
        self.refresh_from_cli()

    def on_action_restart(self, action, param):
        self.restart_app()

    def on_action_about(self, action, param):
        try:
            dialog = Adw.AboutDialog(
                application_name="Linux Wallpaper Engine GUI",
                application_icon=APP_ID,
                version=VERSION,
                developer_name="Suhoiyis",
                comments="A modern GTK4 GUI for managing dynamic wallpapers from Steam Workshop on Linux, based on linux-wallpaperengine.",
                license_type=Gtk.License.GPL_3_0,
                website="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine",
                issue_url="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues",
                copyright="© 2026 Suhoiyis",
                release_notes=get_latest_changelog(),
                debug_info=get_debug_info(),
                debug_info_filename="wallpaperengine-gui-debug.txt"
            )
            dialog.present(self.win)
        except Exception as e:
            self.show_toast(f"Error opening About dialog: {str(e)}")

    def on_action_show_history(self, action, param):
        try:
            dialog = HistoryDialog(self.win, self.history_manager, self.wp_manager, self.controller, self.nickname_manager)
            dialog.present()
        except Exception as e:
            self.show_toast(f"Error opening history: {str(e)}")
    
    def on_action_welcome(self, action, param):
        try:
            dialog = WelcomeDialog(self.win, self.config, self.app_integrator)
            dialog.present()
        except Exception as e:
            self.show_toast(f"Error opening welcome dialog: {str(e)}")
    
    def on_action_check_update(self, action, param):
        try:
            def on_update_callback(latest_version, release_url, has_update):
                GLib.idle_add(lambda: self._handle_update_result(latest_version, release_url, has_update))
                
            self.update_checker.check_update(VERSION, on_update_callback)
            self.show_toast("Checking for updates...")
        except Exception as e:
            self.show_toast(f"Error checking for updates: {str(e)}")

    def _handle_update_result(self, latest_version, release_url, has_update):
        if has_update and latest_version:
            dialog = Adw.MessageDialog(
                transient_for=self.win,
                heading="Update Available",
                body=f"A new version ({latest_version}) is available on GitHub."
            )
            dialog.add_response("cancel", "Cancel")
            dialog.add_response("download", "Download")
            dialog.set_response_appearance("download", Adw.ResponseAppearance.SUGGESTED)
            
            def on_response(d, response):
                if response == "download":
                    import webbrowser
                    webbrowser.open(release_url)
                d.close()
                
            dialog.connect("response", on_response)
            dialog.present()
        elif latest_version == "ERROR:RATE_LIMIT":
            self.show_toast("GitHub API rate limit exceeded. Please try again later.")
        elif latest_version is None:
            self.show_toast("Failed to check for updates. Please check your connection.")
        else:
            self.show_toast(f"You are up to date (v{VERSION})")

    def show_welcome_wizard(self):
        self.on_action_welcome(None, None)


    def on_action_quit_request(self, action, param):
        dialog = Adw.MessageDialog.new(self.win)
        dialog.set_heading("Quit Application?")
        dialog.set_body("This will stop all running wallpapers and exit the application.")
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("quit", "Quit")
        dialog.set_response_appearance("quit", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.connect("response", self.on_quit_dialog_response)
        dialog.present()

    def on_quit_dialog_response(self, dialog, response):
        if response == "quit":
             self.quit_app()



def main():
    # Set program name for WM class matching - must match the .desktop filename
    GLib.set_prgname(APP_ID)
    app = WallpaperApp()
    app.run(sys.argv)

```

---

### 📄 文件: `py_GUI/ui/compact_window.py`

```python
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf

from typing import Callable, Optional, List

from py_GUI.utils import markdown_to_pango, format_size
from py_GUI.ui.components.animated_preview import AnimatedPreview


class CompactWindow(Gtk.ApplicationWindow):
    def __init__(self, app, wp_manager, controller, config, log_manager, 
                 screen_manager, nickname_manager, show_toast: Callable[[str], None],
                 on_compact_mode_toggled: Callable[[bool], None],
                 on_restart_app: Callable[[], None]):
        super().__init__(application=app)
        
        self.app = app
        self.wp_manager = wp_manager
        self.controller = controller
        self.config = config
        self.log_manager = log_manager
        self.screen_manager = screen_manager
        self.nickname_manager = nickname_manager
        self.show_toast = show_toast
        self.on_compact_mode_toggled_cb = on_compact_mode_toggled
        self.on_restart_app_cb = on_restart_app
        
        self.selected_wp: Optional[str] = None
        self._wallpaper_ids: List[str] = []
        self._thumb_cache = {}
        self.thumb_buttons: List[Gtk.Button] = []
        self.target_screen = self.config.get("lastScreen") or self.screen_manager.get_primary_screen() or self.screen_manager.get_first_screen() or "eDP-1"
        
        self.set_title("Wallpaper Preview")
        self.set_default_size(300, 700)
        self.set_resizable(True)
        self.connect("close-request", self._on_close_request)
        
        self._build_ui()
        self._setup_key_controller()
    
    def _build_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(main_box)
        
        navbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        navbar.add_css_class("nav-bar")
        navbar.set_margin_start(10)
        navbar.set_margin_end(10)
        main_box.append(navbar)
        
        self.btn_toggle = Gtk.Button()
        self.btn_toggle.set_icon_name("view-fullscreen-symbolic")
        self.btn_toggle.set_tooltip_text("Exit Compact Mode")
        self.btn_toggle.add_css_class("nav-btn")
        self.btn_toggle.connect("clicked", self._on_toggle_clicked)
        navbar.append(self.btn_toggle)
        
        spacer_left = Gtk.Box()
        spacer_left.set_hexpand(True)
        navbar.append(spacer_left)
        
        self.screen_dd = Gtk.DropDown.new_from_strings(self.screen_manager.get_screens())
        self.screen_dd.set_tooltip_text("Select Monitor")
        
        screens = self.screen_manager.get_screens()
        if self.target_screen in screens:
            self.screen_dd.set_selected(screens.index(self.target_screen))
        
        self.screen_dd.connect("notify::selected", self._on_screen_changed)
        navbar.append(self.screen_dd)
        
        spacer_right = Gtk.Box()
        spacer_right.set_hexpand(True)
        navbar.append(spacer_right)
        
        btn_restart = Gtk.Button()
        btn_restart.set_icon_name("system-reboot-symbolic")
        btn_restart.set_tooltip_text("Restart Application")
        btn_restart.add_css_class("nav-btn")
        btn_restart.connect("clicked", lambda _: self.on_restart_app_cb())
        navbar.append(btn_restart)
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        main_box.append(scroll)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        content.set_margin_start(15)
        content.set_margin_end(15)
        content.set_margin_top(10)
        content.set_margin_bottom(10)
        scroll.set_child(content)
        
        top_section = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        top_section.set_halign(Gtk.Align.CENTER)
        content.append(top_section)

        preview_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_container.set_size_request(200, 200)
        preview_container.add_css_class("sidebar-preview")
        top_section.append(preview_container)
        
        jump_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        jump_box.set_valign(Gtk.Align.START)
        jump_box.set_margin_start(4)
        top_section.append(jump_box)
        
        jump_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        jump_box.append(jump_row)
        
        self.entry_jump = Gtk.Entry()
        self.entry_jump.set_has_frame(False)
        self.entry_jump.set_placeholder_text("#")
        self.entry_jump.set_max_length(5)
        self.entry_jump.set_width_chars(1)
        self.entry_jump.set_max_width_chars(4)
        self.entry_jump.set_alignment(1.0)
        self.entry_jump.set_tooltip_text("Jump to Index")
        self.entry_jump.connect("activate", self._on_jump_entry_activate)
        jump_row.append(self.entry_jump)
        
        self.lbl_jump_total = Gtk.Label(label="/0")
        self.lbl_jump_total.add_css_class("dim-label")
        jump_row.append(self.lbl_jump_total)

        self.btn_stop = Gtk.Button()
        self.btn_stop.set_size_request(34, 34)
        self.btn_stop.set_icon_name("media-playback-stop-symbolic")
        self.btn_stop.add_css_class("circular")
        self.btn_stop.add_css_class("stop-btn")
        self.btn_stop.set_tooltip_text("Stop Wallpaper")
        self.btn_stop.connect("clicked", self._on_stop_clicked)
        jump_box.append(self.btn_stop)
        
        self.btn_lucky = Gtk.Button()
        self.btn_lucky.set_size_request(34, 34)
        self.btn_lucky.set_icon_name("media-playlist-shuffle-symbolic")
        self.btn_lucky.add_css_class("circular")
        self.btn_lucky.set_tooltip_text("I'm feeling lucky")
        self.btn_lucky.connect("clicked", self._on_lucky_clicked)
        jump_box.append(self.btn_lucky)
        
        self.btn_jump = Gtk.Button()
        self.btn_jump.set_size_request(34, 34)
        self.btn_jump.set_icon_name("go-home-symbolic")
        self.btn_jump.add_css_class("circular")
        self.btn_jump.set_tooltip_text("Jump to current wallpaper")
        self.btn_jump.connect("clicked", self._on_jump_clicked)
        jump_box.append(self.btn_jump)
        
        preview_scroll = Gtk.ScrolledWindow()
        preview_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        preview_scroll.set_size_request(200, 200)
        preview_container.append(preview_scroll)
        
        self.preview_image = AnimatedPreview(size_request=(200, 200))
        preview_scroll.set_child(self.preview_image)
        
        self.lbl_title = Gtk.Label(label="Select a Wallpaper")
        self.lbl_title.add_css_class("sidebar-title")
        self.lbl_title.set_margin_start(0)
        self.lbl_title.set_use_markup(True)
        self.lbl_title.set_halign(Gtk.Align.START)
        self.lbl_title.set_wrap(True)
        self.lbl_title.set_max_width_chars(30)
        content.append(self.lbl_title)
        
        info_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        info_row.set_halign(Gtk.Align.START)
        info_row.set_margin_start(0)
        content.append(info_row)
        
        self.lbl_id = Gtk.Label(label="")
        self.lbl_id.add_css_class("folder-chip")
        self.lbl_id.set_margin_start(0)
        self.lbl_id.set_tooltip_text("Click to copy ID")
        self.lbl_id.set_cursor_from_name("pointer")
        info_row.append(self.lbl_id)
        
        id_click = Gtk.GestureClick.new()
        id_click.connect("released", lambda gesture, n, x, y: self._on_id_clicked())
        self.lbl_id.add_controller(id_click)
        
        self.lbl_size = Gtk.Label(label="")
        self.lbl_size.add_css_class("size-chip")
        info_row.append(self.lbl_size)
        
        self.lbl_index = Gtk.Label(label="")
        self.lbl_index.add_css_class("index-chip")
        info_row.append(self.lbl_index)
        
        type_tags_grid = Gtk.Grid()
        type_tags_grid.set_row_spacing(2)
        type_tags_grid.set_column_spacing(12)
        type_tags_grid.set_margin_top(0)
        type_tags_grid.set_margin_start(0)
        content.append(type_tags_grid)
        
        type_header = Gtk.Label(label="Type")
        type_header.add_css_class("sidebar-section")
        type_header.set_margin_top(2)
        type_header.set_margin_start(2)
        type_header.set_xalign(0)
        type_header.set_halign(Gtk.Align.START)
        type_tags_grid.attach(type_header, 0, 0, 1, 1)
        
        self.lbl_type = Gtk.Label(label="-")
        self.lbl_type.add_css_class("tag-chip")
        self.lbl_type.set_margin_start(0)
        self.lbl_type.set_xalign(0)
        self.lbl_type.set_halign(Gtk.Align.START)
        type_tags_grid.attach(self.lbl_type, 0, 1, 1, 1)
        
        tags_header = Gtk.Label(label="Tags")
        tags_header.add_css_class("sidebar-section")
        tags_header.set_margin_top(2)
        tags_header.set_margin_start(2)
        tags_header.set_xalign(0)
        tags_header.set_halign(Gtk.Align.START)
        type_tags_grid.attach(tags_header, 1, 0, 1, 1)
        
        self.tags_flow = Gtk.FlowBox()
        self.tags_flow.set_margin_start(0)
        self.tags_flow.set_selection_mode(Gtk.SelectionMode.NONE)
        self.tags_flow.set_max_children_per_line(3)
        self.tags_flow.set_min_children_per_line(1)
        self.tags_flow.set_hexpand(True)
        type_tags_grid.attach(self.tags_flow, 1, 1, 1, 1)
        
        self.btn_apply = Gtk.Button(label="Apply Wallpaper")
        self.btn_apply.add_css_class("sidebar-btn")
        self.btn_apply.add_css_class("suggested-action")
        self.btn_apply.set_margin_top(12)
        self.btn_apply.connect("clicked", self._on_apply_clicked)
        content.append(self.btn_apply)
        
        nav_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        nav_container.set_halign(Gtk.Align.CENTER)
        nav_container.set_margin_top(12)
        nav_container.set_margin_bottom(8)
        content.append(nav_container)
        
        btn_prev = Gtk.Button()
        btn_prev.set_size_request(30, 30)
        btn_prev.set_icon_name("go-previous-symbolic")
        btn_prev.add_css_class("flat")
        btn_prev.set_tooltip_text("Previous Wallpaper (Left Arrow)")
        btn_prev.connect("clicked", lambda _: self._navigate_wallpaper(-1))
        nav_container.append(btn_prev)
        
        self.thumb_grid = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        nav_container.append(self.thumb_grid)
        
        for _ in range(5):
            btn = Gtk.Button()
            btn.set_size_request(40, 40)
            btn.set_has_frame(False)
            
            pic = Gtk.Picture()
            pic.set_content_fit(Gtk.ContentFit.COVER)
            pic.set_size_request(40, 40)
            btn.set_child(pic)
            
            btn.connect("clicked", self._on_thumb_clicked)
            self.thumb_grid.append(btn)
            self.thumb_buttons.append(btn)
        
        btn_next = Gtk.Button()
        btn_next.set_size_request(30, 30)
        btn_next.set_icon_name("go-next-symbolic")
        btn_next.add_css_class("flat")
        btn_next.set_tooltip_text("Next Wallpaper (Right Arrow)")
        btn_next.connect("clicked", lambda _: self._navigate_wallpaper(1))
        nav_container.append(btn_next)
    
    def _on_jump_entry_activate(self, entry):
        text = entry.get_text().strip()
        if not text:
            return
            
        try:
            idx = int(text)
            total = len(self._wallpaper_ids)
            if total == 0:
                return
                
            if idx < 1: idx = 1
            if idx > total: idx = total
            
            self.select_wallpaper(self._wallpaper_ids[idx - 1])
        except ValueError:
            if self.selected_wp and self.selected_wp in self._wallpaper_ids:
                curr_idx = self._wallpaper_ids.index(self.selected_wp) + 1
                entry.set_text(str(curr_idx))
            else:
                entry.set_text("")
            entry.set_position(-1)

    def _on_close_request(self, win):
        self.on_compact_mode_toggled_cb(False)
        return True
    
    def _on_toggle_clicked(self, btn):
        self.on_compact_mode_toggled_cb(False)
    
    def _on_apply_clicked(self, btn):
        if self.selected_wp:
            self.controller.apply(self.selected_wp, screen=self.target_screen)
            self.config.set("lastScreen", self.target_screen)
    
    def _on_stop_clicked(self, btn):
        self.controller.stop_screen(self.target_screen)
    
    def _on_lucky_clicked(self, btn):
        import random
        if self._wallpaper_ids:
            wp_id = random.choice(self._wallpaper_ids)
            self.select_wallpaper(wp_id)
            self._on_apply_clicked(None)
    
    def _on_jump_clicked(self, btn):
        active_monitors = self.config.get("active_monitors") or {}
        current_wp_id = active_monitors.get(self.target_screen)
        
        if current_wp_id:
            self.select_wallpaper(current_wp_id)
        else:
            last_wp = self.config.get("lastWallpaper")
            if last_wp:
                self.select_wallpaper(last_wp)
    
    def _on_screen_changed(self, dd, pspec):
        selected_item = dd.get_selected_item()
        if selected_item:
            screen = selected_item.get_string()
            self.target_screen = screen
            
            active_monitors = self.config.get("active_monitors") or {}
            current_wp_id = active_monitors.get(screen)
            
            if current_wp_id:
                self.select_wallpaper(current_wp_id)
    
    def _on_id_clicked(self):
        if self.selected_wp:
            clipboard = Gdk.Display.get_default().get_clipboard()
            clipboard.set(self.selected_wp)
            self.show_toast(f"Copied ID: {self.selected_wp}")
            self.lbl_id.set_tooltip_markup("<span foreground='#22c55e' weight='bold'>Copied!</span>")
            GLib.timeout_add(1500, lambda: self.lbl_id.set_tooltip_text("Click to copy ID") or False)
    
    def _setup_key_controller(self):
        key_ctrl = Gtk.EventControllerKey.new()
        key_ctrl.connect("key-pressed", self._on_key_pressed)
        self.add_controller(key_ctrl)
    
    def _on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Left:
            self._navigate_wallpaper(-1)
            return True
        elif keyval == Gdk.KEY_Right:
            self._navigate_wallpaper(1)
            return True
        return False
    
    def _navigate_wallpaper(self, direction: int):
        if not self._wallpaper_ids or not self.selected_wp:
            return
        try:
            current_idx = self._wallpaper_ids.index(self.selected_wp)
            total = len(self._wallpaper_ids)
            if total == 0: return
            
            new_idx = (current_idx + direction) % total
            self.select_wallpaper(self._wallpaper_ids[new_idx])
        except ValueError:
            pass
    
    def set_wallpaper_ids(self, ids: List[str]):
        self._wallpaper_ids = ids
        if self.selected_wp:
            self._update_thumb_grid()
    
    def select_wallpaper(self, wp_id: str):
        self.selected_wp = wp_id
        
        if not wp_id:
            self._clear()
            return
        
        wp = self.wp_manager._wallpapers.get(wp_id)
        if not wp:
            self._clear()
            return
        
        path = wp.get('preview', '')
        self.preview_image.set_image_from_path(path, self.wp_manager)
        
        display_name, original_title = self.nickname_manager.get_display_name(wp)
        self.lbl_title.set_markup(markdown_to_pango(display_name))
        
        if original_title:
            tooltip_text = f"{display_name}\n({original_title})"
            self.lbl_title.set_tooltip_text(tooltip_text)
        else:
            self.lbl_title.set_tooltip_text(display_name)
        
        self.lbl_size.set_label(format_size(wp.get('size', 0)))
        
        self.lbl_id.set_label(str(wp_id))
        
        if self._wallpaper_ids and wp_id in self._wallpaper_ids:
            idx = self._wallpaper_ids.index(wp_id) + 1
            total = len(self._wallpaper_ids)
            self.lbl_index.set_label(f"{idx}/{total}")
            self.entry_jump.set_text(str(idx))
            self.lbl_jump_total.set_label(f"/{total}")
        else:
            self.lbl_index.set_label("")
            self.entry_jump.set_text("")
            self.lbl_jump_total.set_label("")
        
        self.lbl_type.set_label(wp.get('type', 'Unknown'))
        
        while True:
            child = self.tags_flow.get_first_child()
            if child is None:
                break
            self.tags_flow.remove(child)
        
        tags = wp.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        if not tags:
            lbl = Gtk.Label(label="None")
            lbl.add_css_class("text-muted")
            self.tags_flow.append(lbl)
        else:
            for tag in tags[:6]:
                chip = Gtk.Label(label=str(tag))
                chip.add_css_class("tag-chip")
                self.tags_flow.append(chip)
        
        self._update_thumb_grid()
    
    def _clear(self):
        self.selected_wp = None
        self.preview_image.set_image_from_path(None, None)
        self.lbl_title.set_label("Select a Wallpaper")
        self.lbl_size.set_label("")
        self.lbl_index.set_label("")
        self.lbl_id.set_label("")
        self.lbl_type.set_label("-")
        self.entry_jump.set_text("")
        self.lbl_jump_total.set_label("")
        
        while True:
            child = self.tags_flow.get_first_child()
            if child is None:
                break
            self.tags_flow.remove(child)
        
        for btn in self.thumb_buttons:
            btn.set_child(None)
            if hasattr(btn, 'wp_id'):
                del btn.wp_id
    
    def _update_thumb_grid(self):
        if not self.selected_wp or not self._wallpaper_ids:
            return
        
        try:
            current_idx = self._wallpaper_ids.index(self.selected_wp)
        except ValueError:
            return
        
        total = len(self._wallpaper_ids)
        if total == 0: return
        
        for i, offset in enumerate(range(-2, 3)):
            if i >= len(self.thumb_buttons): break
            
            idx = (current_idx + offset) % total
            wp_id = self._wallpaper_ids[idx]
            btn = self.thumb_buttons[i]
            
            btn.wp_id = wp_id
            
            if offset == 0:
                btn.add_css_class("suggested-action")
            else:
                btn.remove_css_class("suggested-action")
            
            wp = self.wp_manager._wallpapers.get(wp_id)
            if wp:
                if wp_id in self._thumb_cache:
                    texture = self._thumb_cache[wp_id]
                else:
                    texture = self.wp_manager.get_texture(wp.get('preview', ''), 40)
                    self._thumb_cache[wp_id] = texture
                
                child = btn.get_child()
                if not isinstance(child, Gtk.Picture):
                    child = Gtk.Picture()
                    child.set_content_fit(Gtk.ContentFit.COVER)
                    child.set_size_request(40, 40)
                    btn.set_child(child)
                
                child.set_paintable(texture)

    def _on_thumb_clicked(self, btn):
        if hasattr(btn, 'wp_id') and btn.wp_id:
            self.select_wallpaper(btn.wp_id)
    
    def sync_from_main(self, wallpaper_ids: List[str], selected_wp: Optional[str]):
        self._wallpaper_ids = wallpaper_ids
        if selected_wp:
            self.select_wallpaper(selected_wp)
        elif wallpaper_ids:
            self._on_jump_clicked(None)

```

---

### 📄 文件: `py_GUI/ui/components/__init__.py`

```python

```

---

### 📄 文件: `py_GUI/ui/components/animated_preview.py`

```python
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf

class AnimatedPreview(Gtk.Picture):
    def __init__(self, size_request=(200, 200)):
        super().__init__()
        self.set_content_fit(Gtk.ContentFit.COVER)
        self.set_size_request(*size_request)
        
        # Force fill behavior
        self.set_halign(Gtk.Align.FILL)
        self.set_valign(Gtk.Align.FILL)
        self.set_hexpand(False)
        self.set_vexpand(False)
        self.set_can_shrink(True)
        
        self.anim = None
        self.anim_iter = None
        self.anim_timer = None
        self.current_path = None

    def set_image_from_path(self, path: str, wp_manager):
        """
        Smartly sets the image. If it's a GIF, starts animation.
        If it's static, sets a static texture.
        """
        if self.current_path == path:
            return

        self.stop_animation()
        self.current_path = path
        
        if not path:
            self.set_paintable(None)
            return

        loaded_anim = False
        if path.lower().endswith('.gif'):
            try:
                self._start_animation(path)
                loaded_anim = True
            except Exception:
                loaded_anim = False
        
        if not loaded_anim:
            # Fallback to static texture
            texture = wp_manager.get_texture(path, self.get_width() or 200)
            self.set_paintable(texture)

    def _start_animation(self, path):
        self.anim = GdkPixbuf.PixbufAnimation.new_from_file(path)
        self.anim_iter = self.anim.get_iter(None)
        
        pixbuf = self.anim_iter.get_pixbuf()
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.set_paintable(texture)
        
        if not self.anim.is_static_image():
            self.anim_timer = GLib.timeout_add(
                self.anim_iter.get_delay_time(),
                self._on_animation_frame
            )

    def _on_animation_frame(self):
        if not hasattr(self, 'anim_iter') or not self.anim_iter:
            return False
        
        try:
            self.anim_iter.advance(None)
        except Exception:
            return False
        
        pixbuf = self.anim_iter.get_pixbuf()
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.set_paintable(texture)
        
        delay = self.anim_iter.get_delay_time()
        if delay <= 0:
            delay = 100
        
        self.anim_timer = GLib.timeout_add(delay, self._on_animation_frame)
        return False

    def stop_animation(self):
        if hasattr(self, 'anim_timer') and self.anim_timer:
            GLib.source_remove(self.anim_timer)
            self.anim_timer = None
        self.anim = None
        self.anim_iter = None
        self.current_path = None

```

---

### 📄 文件: `py_GUI/ui/components/dialogs.py`

```python
import gi
gi.require_version('Gtk', '4.0')
try:
    gi.require_version('Adw', '1')
except ValueError:
    pass
from gi.repository import Gtk, Adw, Gdk
from typing import Optional, Callable

def show_delete_dialog(parent_window, wp_id, on_confirm):
    dialog = Gtk.Dialog(
        transient_for=parent_window,
        modal=True,
        title="Delete Wallpaper"
    )
    dialog.add_button("Cancel", Gtk.ResponseType.NO)
    btn_del = dialog.add_button("Delete", Gtk.ResponseType.YES)
    btn_del.add_css_class("destructive-action")
    
    content = dialog.get_content_area()
    content.set_spacing(15)
    content.set_margin_top(20)
    content.set_margin_bottom(20)
    content.set_margin_start(20)
    content.set_margin_end(20)
    
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    content.append(box)
    
    icon = Gtk.Image.new_from_icon_name("dialog-warning-symbolic")
    icon.set_pixel_size(48)
    icon.add_css_class("warning")
    box.append(icon)
    
    msg_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    box.append(msg_box)
    
    lbl = Gtk.Label(label="Delete Wallpaper?")
    lbl.add_css_class("title-2")
    lbl.set_halign(Gtk.Align.START)
    msg_box.append(lbl)
    
    desc = Gtk.Label(label=f"Are you sure you want to delete wallpaper {wp_id}?\nThis action cannot be undone.")
    desc.set_halign(Gtk.Align.START)
    desc.add_css_class("body")
    msg_box.append(desc)

    def on_response(d, response):
        if response == Gtk.ResponseType.YES:
            on_confirm()
        d.destroy()

    dialog.connect("response", on_response)
    dialog.present()

def show_error_dialog(parent_window, title, message):
    dialog = Gtk.Dialog(
        transient_for=parent_window,
        modal=True,
        title=title
    )
    dialog.add_button("OK", Gtk.ResponseType.OK)
    
    content = dialog.get_content_area()
    content.set_spacing(15)
    content.set_margin_top(20)
    content.set_margin_bottom(20)
    content.set_margin_start(20)
    content.set_margin_end(20)
    
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    content.append(box)
    
    icon = Gtk.Image.new_from_icon_name("dialog-error-symbolic")
    icon.set_pixel_size(48)
    icon.add_css_class("error")
    box.append(icon)
    
    msg_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    box.append(msg_box)
    
    lbl = Gtk.Label(label=title)
    lbl.add_css_class("title-2")
    lbl.set_halign(Gtk.Align.START)
    msg_box.append(lbl)
    
    desc = Gtk.Label(label=message)
    desc.set_halign(Gtk.Align.START)
    desc.set_wrap(True)
    desc.set_max_width_chars(50)
    desc.add_css_class("body")
    msg_box.append(desc)
    
    dialog.connect("response", lambda d, r: d.destroy())
    dialog.present()

def show_screenshot_success_dialog(parent_window, file_path, stats=None, texture=None):
    import subprocess
    import os
    import shutil
    
    dialog = Gtk.Dialog(
        transient_for=parent_window,
        modal=True,
        title="Screenshot Saved"
    )
    dialog.add_button("Close", Gtk.ResponseType.CLOSE)
    dialog.add_button("Open Folder", 101)
    dialog.add_button("Open Image", 102)
    
    btn_img = dialog.get_widget_for_response(102)
    if btn_img:
        btn_img.add_css_class("suggested-action")
    
    content = dialog.get_content_area()
    content.set_spacing(15)
    content.set_margin_top(20)
    content.set_margin_bottom(10)
    content.set_margin_start(20)
    content.set_margin_end(20)
    
    main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    content.append(main_box)
    
    if texture:
        thumb = Gtk.Picture.new_for_paintable(texture)
        thumb.set_size_request(160, 90)
        thumb.set_content_fit(Gtk.ContentFit.COVER)
        thumb.add_css_class("thumbnail")
        main_box.append(thumb)
    else:
        icon = Gtk.Image.new_from_icon_name("camera-photo-symbolic")
        icon.set_pixel_size(64)
        main_box.append(icon)
    
    info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    info_box.set_hexpand(True)
    main_box.append(info_box)
    
    title_lbl = Gtk.Label(label="Screenshot Saved")
    title_lbl.add_css_class("title-1")
    title_lbl.set_halign(Gtk.Align.START)
    info_box.append(title_lbl)
    
    path_lbl = Gtk.Label(label=file_path)
    path_lbl.set_halign(Gtk.Align.START)
    path_lbl.set_wrap(True)
    path_lbl.set_max_width_chars(45)
    path_lbl.add_css_class("body")
    info_box.append(path_lbl)
    
    if stats:
        stats_lbl = Gtk.Label(label=stats)
        stats_lbl.set_halign(Gtk.Align.START)
        stats_lbl.add_css_class("body")
        info_box.append(stats_lbl)
    
    def on_response(d, response):
        if response == 101:
            try:
                folder = os.path.dirname(file_path)
                file_managers = [
                    "thunar", "nautilus", "dolphin", "nemo", "pcmanfm", 
                    "pcmanfm-qt", "caja", "index", "files"
                ]
                
                opened = False
                for fm in file_managers:
                    if shutil.which(fm):
                        try:
                            subprocess.Popen([fm, folder])
                            opened = True
                            break
                        except Exception: continue
                
                if not opened:
                    subprocess.Popen(['xdg-open', folder])
            except Exception: pass
        elif response == 102:
            try:
                subprocess.Popen(['xdg-open', file_path])
            except Exception: pass
        
        d.destroy()

    dialog.connect("response", on_response)
    dialog.present()

def show_nickname_dialog(parent, title: str, current_nickname: Optional[str], on_confirm: Callable[[str], None]):
    dialog = Adw.MessageDialog(
        transient_for=parent,
        heading="Set Nickname",
        body=f"Set a custom nickname for '{title}'"
    )
    
    dialog.add_response("cancel", "Cancel")
    dialog.add_response("save", "Save")
    dialog.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
    dialog.set_default_response("save")
    dialog.set_close_response("cancel")
    
    content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    content_box.set_margin_top(12)
    content_box.set_margin_bottom(12)
    content_box.set_margin_start(12)
    content_box.set_margin_end(12)
    
    entry = Gtk.Entry()
    entry.set_placeholder_text("Enter nickname...")
    if current_nickname:
        entry.set_text(current_nickname)
    entry.set_activates_default(True)
    content_box.append(entry)
    
    hint = Gtk.Label(label="Leave empty to remove nickname")
    hint.add_css_class("caption")
    hint.add_css_class("dim-label")
    content_box.append(hint)
    
    dialog.set_extra_child(content_box)
    
    def on_response(d, response):
        if response == "save":
            text = entry.get_text().strip()
            on_confirm(text)
        d.close()
        
    dialog.connect("response", on_response)
    dialog.present()

```

---

### 📄 文件: `py_GUI/ui/components/history_dialog.py`

```python
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib, Pango
from datetime import datetime
import os

class HistoryDialog(Gtk.Window):
    def __init__(self, parent, history_manager, wp_manager, controller, nickname_manager=None):
        super().__init__(title="Playback History")
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_default_size(500, 600)
        
        self.history_manager = history_manager
        self.wp_manager = wp_manager
        self.controller = controller
        self.nickname_manager = nickname_manager
        
        header = Gtk.HeaderBar()
        self.set_titlebar(header)
        
        clear_btn = Gtk.Button(label="Clear")
        clear_btn.add_css_class("destructive-action")
        clear_btn.connect("clicked", self.on_clear_clicked)
        header.pack_end(clear_btn)

        self.lbl_count = Gtk.Label(label="0/30")
        self.lbl_count.add_css_class("caption")
        self.lbl_count.add_css_class("dim-label")
        self.lbl_count.set_margin_end(10)
        header.pack_end(self.lbl_count)
        
        self.stack = Gtk.Stack()
        self.stack.set_vexpand(True)
        self.stack.set_hexpand(True)
        self.set_child(self.stack)
        
        empty_state = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        empty_state.set_valign(Gtk.Align.CENTER)
        empty_state.set_halign(Gtk.Align.CENTER)
        
        empty_icon = Gtk.Image.new_from_icon_name("document-open-recent-symbolic")
        empty_icon.set_pixel_size(64)
        empty_icon.add_css_class("dim-label")
        empty_label = Gtk.Label(label="No Recent Playback History")
        empty_label.add_css_class("title-4")
        empty_label.add_css_class("dim-label")
        empty_state.append(empty_icon)
        empty_state.append(empty_label)
        self.stack.add_named(empty_state, "empty")
        
        list_container = Gtk.ScrolledWindow()
        list_container.set_vexpand(True)
        list_container.set_hexpand(True)
        
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.list_box.add_css_class("rich-list")
        self.list_box.set_vexpand(True)
        self.list_box.set_show_separators(True)
        list_container.set_child(self.list_box)
        self.stack.add_named(list_container, "list")
        
        self._load_history()
        
    def _load_history(self):
        while True:
            row = self.list_box.get_first_child()
            if not row:
                break
            self.list_box.remove(row)
            
        history = self.history_manager.get_all()
        
        self.lbl_count.set_label(f"{len(history)}/30")
        
        if len(history) == 0:
            self.stack.set_visible_child_name("empty")
        else:
            self.stack.set_visible_child_name("list")
            for item in history:
                row = self._create_row(item)
                self.list_box.append(row)
            
    def _create_row(self, item):
        wp_id = item.get("id", "unknown")
        title = item.get("title", "Unknown Title")
        preview_path = item.get("preview", "")
        timestamp_str = item.get("timestamp", "")
        
        display_title = title
        if self.nickname_manager:
            dummy_wp = {"id": wp_id, "title": title}
            nickname, _ = self.nickname_manager.get_display_name(dummy_wp)
            if nickname != title:
                display_title = f"<i>{nickname}</i>"
            
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        box.set_margin_top(8)
        box.set_margin_bottom(8)
        box.set_margin_start(12)
        box.set_margin_end(12)
        
        texture = self.wp_manager.get_texture(preview_path, size=64)
        if texture:
            image = Gtk.Image.new_from_paintable(texture)
            image.set_pixel_size(64)
        else:
            image = Gtk.Image.new_from_icon_name("image-missing-symbolic")
            image.set_pixel_size(64)
        
        box.append(image)
        
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        text_box.set_valign(Gtk.Align.CENTER)
        text_box.set_hexpand(True)
        
        title_label = Gtk.Label()
        title_label.set_markup(display_title)
        title_label.set_xalign(0)
        title_label.set_ellipsize(Pango.EllipsizeMode.END)
        title_label.add_css_class("heading")
        
        id_label = Gtk.Label(label=f"ID: {wp_id}")
        id_label.set_xalign(0)
        id_label.add_css_class("caption")
        id_label.add_css_class("dim-label")
        
        text_box.append(title_label)
        text_box.append(id_label)
        box.append(text_box)
        
        action_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        action_box.set_valign(Gtk.Align.CENTER)
        
        time_str = ""
        if timestamp_str:
            try:
                dt = datetime.fromisoformat(timestamp_str)
                time_str = dt.strftime("%m-%d %H:%M")
            except ValueError:
                time_str = ""
        
        time_label = Gtk.Label(label=time_str)
        time_label.set_halign(Gtk.Align.END)
        time_label.add_css_class("caption")
        time_label.add_css_class("dim-label")
        
        play_btn = Gtk.Button(icon_name="media-playback-start-symbolic")
        play_btn.set_tooltip_text("Apply this wallpaper")
        play_btn.add_css_class("flat")
        play_btn.add_css_class("circular")
        play_btn.connect("clicked", lambda b: self.on_apply_clicked(wp_id))
        
        action_box.append(time_label)
        action_box.append(play_btn)
        
        box.append(action_box)
        
        return box

    def on_clear_clicked(self, button):
        self.history_manager.clear()
        self._load_history()
        
    def on_apply_clicked(self, wp_id):
        root = self.get_transient_for()
        if root and hasattr(root, 'activate_action'):
            root.activate_action("win.apply", GLib.Variant("s", wp_id))

```

---

### 📄 文件: `py_GUI/ui/components/navbar.py`

```python
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, GLib
from typing import Callable, Optional, List, Dict

class NavBar(Gtk.Box):
    def __init__(self, stack: Gtk.Stack, screens: List[str], selected_screen: str,
                 on_home_enter: Optional[Callable] = None,
                 on_screen_changed: Optional[Callable[[str], None]] = None,
                 on_link_toggled: Optional[Callable[[bool], None]] = None,
                 on_restart_app: Optional[Callable] = None,
                 on_compact_mode_toggled: Optional[Callable[[bool], None]] = None,
                 initial_link_state: bool = False,
                 initial_compact_state: bool = False):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.stack = stack
        self.on_home_enter = on_home_enter
        self.on_screen_changed_cb = on_screen_changed
        self.on_link_toggled_cb = on_link_toggled
        self.on_restart_app = on_restart_app
        self.on_compact_mode_toggled_cb = on_compact_mode_toggled
        self.screens = screens
        self.selected_screen = selected_screen
        self.is_linked = initial_link_state
        self.is_compact = initial_compact_state
        self._compact_mode = False
        self.add_css_class("nav-bar")
        self.build_ui()

    def build_ui(self):
        self.screen_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.screen_box.set_margin_start(15)
        self.append(self.screen_box)

        if len(self.screens) > 1:
            self.btn_link = Gtk.ToggleButton()
            self.btn_link.set_icon_name("link-symbolic" if self.is_linked else "unlink-symbolic")
            self.btn_link.set_active(self.is_linked)
            self.btn_link.set_tooltip_text("Link screens (Apply to All)" if self.is_linked else "Unlink screens (Apply to Single)")
            self.btn_link.add_css_class("nav-btn")
            self.btn_link.connect("toggled", self.on_link_toggled)
            self.screen_box.append(self.btn_link)

        icon_screen = Gtk.Image.new_from_icon_name("video-display-symbolic")
        icon_screen.add_css_class("status-label")
        self.screen_box.append(icon_screen)

        self.screen_dd = Gtk.DropDown.new_from_strings(self.screens)
        self.screen_dd.add_css_class("nav-btn")
        if self.selected_screen in self.screens:
            self.screen_dd.set_selected(self.screens.index(self.selected_screen))
        self.screen_dd.connect("notify::selected", self._on_screen_changed)
        self.screen_box.append(self.screen_dd)

        self.spacer_left = Gtk.Box()
        self.spacer_left.set_hexpand(True)
        self.append(self.spacer_left)

        self.nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.btn_home = Gtk.ToggleButton()
        self.btn_home.set_icon_name("user-home-symbolic")
        self.btn_home.set_tooltip_text("Home")
        self.btn_home.add_css_class("nav-btn")
        self.btn_home.set_active(True)
        self.btn_home.connect("toggled", self.on_home_toggled)
        self.nav_box.append(self.btn_home)

        self.btn_performance = Gtk.ToggleButton()
        self.btn_performance.set_icon_name("org.gnome.SystemMonitor-symbolic")
        self.btn_performance.set_tooltip_text("Performance")
        self.btn_performance.add_css_class("nav-btn")
        self.btn_performance.connect("toggled", self.on_performance_toggled)
        self.nav_box.append(self.btn_performance)

        self.btn_settings = Gtk.ToggleButton()
        self.btn_settings.set_icon_name("emblem-system-symbolic")
        self.btn_settings.set_tooltip_text("Settings")
        self.btn_settings.add_css_class("nav-btn")
        self.btn_settings.connect("toggled", self.on_settings_toggled)
        self.nav_box.append(self.btn_settings)

        self.append(self.nav_box)

        self.spacer_right = Gtk.Box()
        self.spacer_right.set_hexpand(True)
        self.append(self.spacer_right)
        
        self.btn_compact = Gtk.ToggleButton()
        self.btn_compact.set_icon_name("view-restore-symbolic")
        self.btn_compact.set_tooltip_text("Compact Preview Mode")
        self.btn_compact.add_css_class("nav-btn")
        self.btn_compact.set_active(self.is_compact)
        self.btn_compact.connect("toggled", self._on_compact_toggled)
        self.btn_compact.set_margin_end(6)
        self.append(self.btn_compact)
        
        self.btn_menu = Gtk.MenuButton()
        self.btn_menu.set_icon_name("open-menu-symbolic")
        self.btn_menu.set_tooltip_text("Menu")
        self.btn_menu.add_css_class("nav-btn")
        self.btn_menu.set_margin_end(15)
        
        self.menu_popover = Gtk.Popover()
        self.menu_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.menu_content.set_margin_start(2)
        self.menu_content.set_margin_end(2)
        self.menu_content.set_margin_top(4)
        self.menu_content.set_margin_bottom(4)
        self.menu_popover.set_child(self.menu_content)
        self.btn_menu.set_popover(self.menu_popover)
        
        self._add_menu_btn("Playback History", "win.show_history")
        self._add_menu_btn("Refresh Library", "win.refresh")
        self._add_menu_btn("Welcome / Setup Wizard", "win.welcome")
        self._add_menu_btn("Check for Updates", "win.check_update")
        self._add_menu_btn("About", "win.about")
        
        sep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep2.set_margin_top(4)
        sep2.set_margin_bottom(4)
        self.menu_content.append(sep2)
        
        self._add_menu_btn("Restart Application", "win.restart", bold=True)
        self._add_menu_btn("Quit Application", "win.quit_app", bold=True, destructive=True)

        self.append(self.btn_menu)

    def _add_menu_btn(self, label_text, action_name, param=None, bold=False, destructive=False, container=None):
        if container is None:
            container = self.menu_content

        btn = Gtk.Button()
        btn.add_css_class("flat")
        btn.add_css_class("popover-btn")
        btn.set_halign(Gtk.Align.FILL)
        
        lbl = Gtk.Label(xalign=0)
        
        weight = "bold" if bold else "normal"
        color_span_start = f"<span foreground='#ef4444'>" if destructive else ""
        color_span_end = "</span>" if destructive else ""
        
        markup = f"<span weight='{weight}'>{color_span_start}{label_text}{color_span_end}</span>"
        
        lbl.set_markup(markup)
        
        btn.set_child(lbl)
        
        def on_clicked(b):
            self.menu_popover.popdown()
            root = self.get_native()
            if root and hasattr(root, 'activate_action'):
                root.activate_action(action_name, param)
            else:
                print(f"[ERROR] NavBar: Could not find root window to activate {action_name}")
        
        btn.connect("clicked", on_clicked)
        container.append(btn)
        return btn

    def on_link_toggled(self, btn):
        self.is_linked = btn.get_active()
        btn.set_icon_name("link-symbolic" if self.is_linked else "unlink-symbolic")
        btn.set_tooltip_text("Link screens (Apply to All)" if self.is_linked else "Unlink screens (Apply to Single)")
        if callable(self.on_link_toggled_cb):
            self.on_link_toggled_cb(self.is_linked)

    def _on_screen_changed(self, dd, pspec):
        selected_item = dd.get_selected_item()
        if selected_item:
            screen = selected_item.get_string()
            self.selected_screen = screen
            if callable(self.on_screen_changed_cb):
                self.on_screen_changed_cb(screen)

    def get_selected_screen(self) -> str:
        return self.selected_screen

    def on_home_toggled(self, btn):
        if btn.get_active():
            self.btn_settings.set_active(False)
            self.btn_performance.set_active(False)
            self.stack.set_visible_child_name("wallpapers")
            try:
                if callable(self.on_home_enter):
                    self.on_home_enter()
            except Exception:
                pass

    def on_performance_toggled(self, btn):
        if btn.get_active():
            self.btn_home.set_active(False)
            self.btn_settings.set_active(False)
            self.stack.set_visible_child_name("performance")

    def on_settings_toggled(self, btn):
        if btn.get_active():
            self.btn_home.set_active(False)
            self.btn_performance.set_active(False)
            self.stack.set_visible_child_name("settings")

    def _on_compact_toggled(self, btn):
        self.is_compact = btn.get_active()
        if callable(self.on_compact_mode_toggled_cb):
            self.on_compact_mode_toggled_cb(self.is_compact)

    def set_compact_active(self, active: bool):
        self.is_compact = active
        self.btn_compact.set_active(active)

    def set_compact_mode(self, enabled: bool):
        self._compact_mode = enabled
        self.screen_box.set_visible(not enabled)
        self.nav_box.set_visible(not enabled)
        self.spacer_left.set_visible(not enabled)
        self.spacer_right.set_visible(not enabled)



```

---

### 📄 文件: `py_GUI/ui/components/nickname_manager_dialog.py`

```python
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, GLib, Pango
from typing import Dict, Tuple, List
from py_GUI.core.nickname import NicknameManager
from py_GUI.core.wallpaper import WallpaperManager

class NicknameManagerDialog(Gtk.Window):
    def __init__(self, parent, nickname_manager: NicknameManager, wp_manager: WallpaperManager, on_saved=None):
        super().__init__(modal=True)
        self.set_transient_for(parent)
        self.set_default_size(600, 500)
        self.set_title("Nickname Manager")
        
        self.nickname_manager = nickname_manager
        self.wp_manager = wp_manager
        self.on_saved_callback = on_saved
        self.rows: List[Tuple[str, Gtk.CheckButton, Gtk.Entry]] = [] 

        self._needs_library_refresh = False

        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(main_box)
        
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)
        main_box.append(header)
        
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        toolbar.set_margin_start(12)
        toolbar.set_margin_end(12)
        toolbar.set_margin_top(12)
        toolbar.set_margin_bottom(12)
        main_box.append(toolbar)
        
        btn_select_all = Gtk.Button(label="Select All")
        btn_select_all.add_css_class("flat")
        btn_select_all.connect("clicked", self.on_select_all)
        toolbar.append(btn_select_all)
        
        btn_deselect_all = Gtk.Button(label="Deselect All")
        btn_deselect_all.add_css_class("flat")
        btn_deselect_all.connect("clicked", self.on_deselect_all)
        toolbar.append(btn_deselect_all)
        
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        toolbar.append(spacer)
        
        btn_delete = Gtk.Button(label="Delete Selected")
        btn_delete.add_css_class("destructive-action")
        btn_delete.connect("clicked", self.on_delete_selected)
        toolbar.append(btn_delete)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_box.append(scrolled)
        
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.list_box.add_css_class("boxed-list")
        self.list_box.set_margin_top(10)
        self.list_box.set_margin_bottom(10)
        self.list_box.set_margin_start(20)
        self.list_box.set_margin_end(20)
        scrolled.set_child(self.list_box)
        
        bottom_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        bottom_bar.set_margin_start(16)
        bottom_bar.set_margin_end(16)
        bottom_bar.set_margin_top(16)
        bottom_bar.set_margin_bottom(16)
        bottom_bar.set_halign(Gtk.Align.END)
        main_box.append(bottom_bar)
        
        btn_cancel = Gtk.Button(label="Cancel")
        btn_cancel.connect("clicked", lambda _: self.close())
        bottom_bar.append(btn_cancel)
        
        btn_save = Gtk.Button(label="Save Changes")
        btn_save.add_css_class("suggested-action")
        btn_save.add_css_class("pill")
        btn_save.connect("clicked", self.on_save)
        bottom_bar.append(btn_save)

    def load_data(self):
        nicknames = self.nickname_manager.get_all()
        
        if not nicknames:
            row = Gtk.ListBoxRow()
            row.set_activatable(False)
            lbl = Gtk.Label(label="No nicknames set.")
            lbl.set_margin_start(20)
            lbl.set_margin_end(20)
            lbl.set_margin_top(20)
            lbl.set_margin_bottom(20)
            lbl.add_css_class("dim-label")
            row.set_child(lbl)
            self.list_box.append(row)
            return

        sorted_items = sorted(nicknames.items(), key=lambda x: x[1].lower())

        for wp_id, nick in sorted_items:
            row = Gtk.ListBoxRow()
            row.set_activatable(False)

            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            box.set_margin_start(8)
            box.set_margin_end(8)
            box.set_margin_top(8)
            box.set_margin_bottom(8)
            row.set_child(box)

            check = Gtk.CheckButton()
            check.set_valign(Gtk.Align.CENTER)
            box.append(check)

            wp_data = self.wp_manager.get_wallpaper(wp_id)
            title = "Unknown Wallpaper"

            if wp_data:
                preview_path = wp_data.get("preview")
                title = wp_data.get("title", "Unknown")

                texture = None
                if preview_path:
                    texture = self.wp_manager.get_texture(preview_path, 48)

                if texture:
                    img = Gtk.Picture.new_for_paintable(texture)
                    img.set_size_request(48, 48)
                    img.set_content_fit(Gtk.ContentFit.COVER)
                    img.add_css_class("card")
                    box.append(img)
                else:
                    self._add_placeholder_icon(box)
            else:
                title = f"ID: {wp_id}"
                self._add_placeholder_icon(box)

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            vbox.set_valign(Gtk.Align.CENTER)
            vbox.set_hexpand(True)
            box.append(vbox)

            lbl_title = Gtk.Label(label=title)
            lbl_title.set_halign(Gtk.Align.START)
            lbl_title.add_css_class("caption")
            lbl_title.add_css_class("dim-label")
            lbl_title.set_ellipsize(Pango.EllipsizeMode.END)
            lbl_title.set_max_width_chars(40)
            vbox.append(lbl_title)

            entry = Gtk.Entry()
            entry.set_text(nick)
            entry.set_placeholder_text("Nickname")
            vbox.append(entry)

            self.list_box.append(row)
            self.rows.append((wp_id, check, entry))

    def _add_placeholder_icon(self, box):
        icon = Gtk.Image.new_from_icon_name("image-missing-symbolic")
        icon.set_pixel_size(32)
        icon.set_size_request(48, 48)
        box.append(icon)

    def on_select_all(self, btn):
        for _, check, _ in self.rows:
            check.set_active(True)

    def on_deselect_all(self, btn):
        for _, check, _ in self.rows:
            check.set_active(False)

    def on_delete_selected(self, btn):
        count = 0
        for _, check, entry in self.rows:
            if check.get_active():
                entry.set_text("")
                count += 1

        if count > 0:
            self._needs_library_refresh = True


    def on_save(self, btn):
        for wp_id, _, entry in self.rows:
            new_nick = entry.get_text()
            self.nickname_manager.set(wp_id, new_nick)

        if self.on_saved_callback:
            self.on_saved_callback(getattr(self, '_needs_library_refresh', False))

        self.close()

```

---

### 📄 文件: `py_GUI/ui/components/sidebar.py`

```python
import threading
import webbrowser
from typing import Dict, List, Optional, Callable
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, GLib, Adw, GdkPixbuf, Pango

from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.logger import LogManager
from py_GUI.utils import markdown_to_pango, bbcode_to_pango, format_size
from py_GUI.ui.components.animated_preview import AnimatedPreview

class Sidebar(Gtk.Box):
    def __init__(self, wp_manager: WallpaperManager, prop_manager: PropertiesManager, 
                 controller: WallpaperController, log_manager: LogManager, nickname_manager=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.wp_manager = wp_manager
        self.prop_manager = prop_manager
        self.controller = controller
        self.log_manager = log_manager
        self.nickname_manager = nickname_manager
        
        self.selected_wp: Optional[str] = None
        
        self.available_screens: List[str] = []
        self.get_current_screen: Callable[[], str] = lambda: ""
        self.get_apply_mode: Callable[[], str] = lambda: "diff"
        
        self.add_css_class("sidebar")
        self.set_size_request(370, -1)
        self.set_hexpand(False)
        self.set_halign(Gtk.Align.END)
        
        self._compact_mode = False
        
        self.build_ui()

    def set_available_screens(self, screens: List[str]):
        self.available_screens = screens
        self.update_apply_button_state()

    def set_current_screen_callback(self, cb: Callable[[], str]):
        self.get_current_screen = cb

    def set_apply_mode_callback(self, cb: Callable[[], str]):
        self.get_apply_mode = cb

    def update_apply_button_mode(self, mode: str):
        self.update_apply_button_state()

    def update_apply_button_state(self):
        while True:
            child = self.apply_btn_container.get_first_child()
            if child is None: break
            self.apply_btn_container.remove(child)
            
        mode = self.get_apply_mode()
        screen_count = len(self.available_screens)
        
        use_split = (screen_count >= 3) and (mode == "diff")
        
        if use_split:
            self.btn_apply = Adw.SplitButton(label="Apply Wallpaper")
            self.btn_apply.add_css_class("sidebar-btn")
            self.btn_apply.add_css_class("suggested-action")
            self.btn_apply.set_hexpand(True)
            self.btn_apply.connect("clicked", self.on_apply_clicked)
            
            menu_popover = Gtk.Popover()
            menu_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            menu_content.set_margin_top(12)
            menu_content.set_margin_bottom(12)
            menu_content.set_margin_start(12)
            menu_content.set_margin_end(12)
            menu_popover.set_child(menu_content)
            
            self.btn_apply.set_popover(menu_popover)
            menu_popover.connect("map", self.on_popover_map)
            self.popover_box = menu_content
            
            self.apply_btn_container.append(self.btn_apply)
        else:
            self.btn_apply = Gtk.Button(label="Apply Wallpaper")
            self.btn_apply.add_css_class("sidebar-btn")
            self.btn_apply.set_hexpand(True)
            self.btn_apply.connect("clicked", self.on_apply_clicked)
            self.apply_btn_container.append(self.btn_apply)

    def build_ui(self):
        # Scrollable area
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_hexpand(False)
        self.append(scroll)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content.set_hexpand(False)
        content.set_size_request(370, -1)
        scroll.set_child(content)

        # Preview Image
        preview_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_container.set_size_request(280, 280)
        preview_container.set_hexpand(False)
        preview_container.set_halign(Gtk.Align.CENTER)
        preview_container.add_css_class("sidebar-preview")

        preview_scroll = Gtk.ScrolledWindow()
        preview_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        preview_scroll.set_size_request(280, 280)
        preview_container.append(preview_scroll)

        self.preview_image = AnimatedPreview(size_request=(280, 280))
        self.preview_image.set_hexpand(False)
        preview_scroll.set_child(self.preview_image)
        content.append(preview_container)

        # Title Section
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        title_box.set_margin_start(20)
        title_box.set_margin_end(20)
        content.append(title_box)

        self.lbl_title = Gtk.Label(label="Select a Wallpaper")
        self.lbl_title.add_css_class("sidebar-title")
        self.lbl_title.set_use_markup(True)
        self.lbl_title.set_halign(Gtk.Align.START)
        self.lbl_title.set_wrap(True)
        self.lbl_title.set_max_width_chars(25)
        self.lbl_title.set_xalign(0)
        title_box.append(self.lbl_title)

        self.lbl_original_name = Gtk.Label(label="")
        self.lbl_original_name.add_css_class("original-name-text")
        self.lbl_original_name.set_halign(Gtk.Align.START)
        self.lbl_original_name.set_wrap(True)
        self.lbl_original_name.set_max_width_chars(30)
        self.lbl_original_name.set_xalign(0)
        self.lbl_original_name.set_visible(False)
        title_box.append(self.lbl_original_name)

        # Info Row (Chips + Edit Button)
        folder_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        folder_row.set_halign(Gtk.Align.FILL)
        folder_row.set_margin_start(20)
        folder_row.set_margin_end(20)
        content.append(folder_row)

        self.lbl_folder = Gtk.Label(label="")
        self.lbl_folder.add_css_class("folder-chip")
        self.lbl_folder.set_tooltip_text("Click to copy ID")
        self.lbl_folder.set_cursor_from_name("pointer")
        self.lbl_folder.set_ellipsize(Pango.EllipsizeMode.END)
        self.lbl_folder.set_max_width_chars(12)
        folder_row.append(self.lbl_folder)

        self.lbl_size = Gtk.Label(label="")
        self.lbl_size.add_css_class("size-chip")
        folder_row.append(self.lbl_size)

        self.lbl_index = Gtk.Label(label="")
        self.lbl_index.add_css_class("index-chip")
        folder_row.append(self.lbl_index)

        # Spacer to push button to far right
        row_spacer = Gtk.Box()
        row_spacer.set_hexpand(True)
        folder_row.append(row_spacer)

        self.btn_edit_nickname = Gtk.Button()
        self.btn_edit_nickname.set_icon_name("document-edit-symbolic")
        self.btn_edit_nickname.add_css_class("flat")
        self.btn_edit_nickname.add_css_class("circular")
        self.btn_edit_nickname.set_tooltip_text("Edit Nickname")
        self.btn_edit_nickname.set_valign(Gtk.Align.CENTER)
        self.btn_edit_nickname.set_visible(False)
        folder_row.append(self.btn_edit_nickname)

        # Folder click to copy
        folder_click = Gtk.GestureClick.new()
        folder_click.connect("released", self.on_folder_clicked)
        self.lbl_folder.add_controller(folder_click)

        # Type
        self.type_header = Gtk.Label(label="Type")
        self.type_header.add_css_class("sidebar-section")
        self.type_header.set_halign(Gtk.Align.START)
        self.type_header.set_margin_start(20)
        self.type_header.set_margin_end(20)
        content.append(self.type_header)

        self.type_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.type_container.set_margin_start(20)
        self.type_container.set_margin_end(20)
        content.append(self.type_container)

        self.lbl_type = Gtk.Label(label="-")
        self.lbl_type.add_css_class("tag-chip")
        self.lbl_type.set_halign(Gtk.Align.START)
        self.type_container.append(self.lbl_type)

        # Tags
        self.tags_header = Gtk.Label(label="Tags")
        self.tags_header.add_css_class("sidebar-section")
        self.tags_header.set_halign(Gtk.Align.START)
        self.tags_header.set_margin_start(20)
        self.tags_header.set_margin_end(20)
        content.append(self.tags_header)

        self.tags_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.tags_container.set_hexpand(False)
        self.tags_container.set_margin_start(20)
        self.tags_container.set_margin_end(20)
        content.append(self.tags_container)

        self.tags_flow = Gtk.FlowBox()
        self.tags_flow.set_selection_mode(Gtk.SelectionMode.NONE)
        self.tags_flow.set_max_children_per_line(4)
        self.tags_flow.set_hexpand(False)
        self.tags_flow.set_column_spacing(4)
        self.tags_flow.set_row_spacing(4)
        self.tags_container.append(self.tags_flow)

        # Description
        self.desc_header = Gtk.Label(label="Description")
        self.desc_header.add_css_class("sidebar-section")
        self.desc_header.set_halign(Gtk.Align.START)
        self.desc_header.set_margin_start(20)
        self.desc_header.set_margin_end(20)
        content.append(self.desc_header)

        self.lbl_desc = Gtk.Label(label="No description.")
        self.lbl_desc.add_css_class("sidebar-desc")
        self.lbl_desc.set_halign(Gtk.Align.START)
        self.lbl_desc.set_xalign(0)
        self.lbl_desc.set_wrap(True)
        self.lbl_desc.set_use_markup(True)
        self.lbl_desc.set_max_width_chars(30)
        self.lbl_desc.set_selectable(True)
        self.lbl_desc.set_margin_start(20)
        self.lbl_desc.set_margin_end(20)
        content.append(self.lbl_desc)

        # Bottom Buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        btn_box.set_margin_top(20)
        btn_box.set_margin_bottom(20)
        self.append(btn_box)

        # Apply Button Container
        self.apply_btn_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.apply_btn_container.set_halign(Gtk.Align.FILL)
        btn_box.append(self.apply_btn_container)
        
        # Initial button setup
        self.update_apply_button_state()

        self.btn_workshop = Gtk.Button(label="Open in Workshop")
        self.btn_workshop.add_css_class("sidebar-btn")
        self.btn_workshop.add_css_class("secondary")
        self.btn_workshop.connect("clicked", self.on_workshop_clicked)
        btn_box.append(self.btn_workshop)

        self.thumb_grid = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.thumb_grid.set_halign(Gtk.Align.CENTER)
        self.thumb_grid.set_margin_top(10)
        self.thumb_grid.set_margin_bottom(10)
        self.thumb_grid.set_visible(False)
        self.append(self.thumb_grid)
        
        self.compact_actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.compact_actions.set_halign(Gtk.Align.CENTER)
        self.compact_actions.set_margin_bottom(10)
        self.compact_actions.set_visible(False)
        self.append(self.compact_actions)
        
        self.btn_compact_stop = Gtk.Button()
        self.btn_compact_stop.set_icon_name("media-playback-stop-symbolic")
        self.btn_compact_stop.add_css_class("circular")
        self.btn_compact_stop.set_tooltip_text("Stop Wallpaper")
        self.compact_actions.append(self.btn_compact_stop)
        
        self.btn_compact_lucky = Gtk.Button()
        self.btn_compact_lucky.set_icon_name("media-playlist-shuffle-symbolic")
        self.btn_compact_lucky.add_css_class("circular")
        self.btn_compact_lucky.set_tooltip_text("I'm feeling lucky")
        self.compact_actions.append(self.btn_compact_lucky)
        
        self.btn_compact_jump = Gtk.Button()
        self.btn_compact_jump.set_icon_name("go-home-symbolic")
        self.btn_compact_jump.add_css_class("circular")
        self.btn_compact_jump.set_tooltip_text("Jump to current wallpaper")
        self.compact_actions.append(self.btn_compact_jump)
        
        self._thumb_cache = {}
        self._wallpaper_ids = []
        self._on_thumb_clicked_cb = None
        self._on_stop_cb = None
        self._on_lucky_cb = None
        self._on_jump_cb = None
        
        self.btn_compact_stop.connect("clicked", lambda b: self._on_stop_cb() if callable(self._on_stop_cb) else None)
        self.btn_compact_lucky.connect("clicked", lambda b: self._on_lucky_cb() if callable(self._on_lucky_cb) else None)
        self.btn_compact_jump.connect("clicked", lambda b: self._on_jump_cb() if callable(self._on_jump_cb) else None)

    def on_popover_map(self, popover):
        while True:
            child = self.popover_box.get_first_child()
            if child is None: break
            self.popover_box.remove(child)
            
        lbl = Gtk.Label(label="Apply to specific screens:")
        lbl.add_css_class("heading")
        lbl.set_halign(Gtk.Align.START)
        self.popover_box.append(lbl)
        
        self.screen_checks = {}
        current = self.get_current_screen()
        
        for screen in self.available_screens:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            chk = Gtk.CheckButton()
            chk.set_active(screen == current)
            self.screen_checks[screen] = chk
            row.append(chk)
            
            lbl_scr = Gtk.Label(label=screen)
            if screen == current:
                lbl_scr.set_markup(f"<b>{screen}</b> (Current)")
            else:
                lbl_scr.set_label(screen)
            row.append(lbl_scr)
            self.popover_box.append(row)
            
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_top(6)
        sep.set_margin_bottom(6)
        self.popover_box.append(sep)
        
        btn_confirm = Gtk.Button(label="Apply to Selected")
        btn_confirm.add_css_class("suggested-action")
        btn_confirm.connect("clicked", lambda b: self.on_advanced_apply(popover))
        self.popover_box.append(btn_confirm)

    def on_advanced_apply(self, popover):
        if not self.selected_wp: return
        
        selected_screens = []
        for screen, chk in self.screen_checks.items():
            if chk.get_active():
                selected_screens.append(screen)
                
        if selected_screens:
            self.controller.apply(self.selected_wp, screens=selected_screens)
            popover.popdown()
        else:
            pass

    def update(self, wp_id: Optional[str], index: int = 0, total: int = 0):
        self.selected_wp = wp_id
        if not wp_id:
            self.clear()
            return

        wp = self.wp_manager._wallpapers.get(wp_id)
        if not wp:
            self.clear()
            return

        self.preview_image.set_image_from_path(wp['preview'], self.wp_manager)

        # Nickname Logic
        original_title = wp.get('title', 'Unknown')
        display_title = original_title
        has_nickname = False
        
        if self.nickname_manager:
            display_title, returned_original = self.nickname_manager.get_display_name(wp)
            if returned_original is not None:
                original_title = returned_original
            if display_title != original_title:
                has_nickname = True
        
        self.lbl_title.set_markup(markdown_to_pango(display_title))
        
        if has_nickname:
            self.lbl_title.add_css_class("nickname-text")
            self.lbl_original_name.set_label(original_title)
            self.lbl_original_name.set_visible(True)
        else:
            self.lbl_title.remove_css_class("nickname-text")
            self.lbl_original_name.set_visible(False)
            
        self.btn_edit_nickname.set_visible(True)

        self.lbl_folder.set_label(f"{wp['id']}")
        self.lbl_size.set_label(format_size(wp.get('size', 0)))
        
        self.lbl_index.set_label(f"{index}/{total}")
        
        self.lbl_type.set_label(wp.get('type', 'Unknown'))
        
        desc = wp.get('description', '')
        self.lbl_desc.set_markup(bbcode_to_pango(desc) or 'No description.')

        while True:
            child = self.tags_flow.get_first_child()
            if child is None: break
            self.tags_flow.remove(child)

        tags = wp.get('tags', [])
        if isinstance(tags, str): tags = [tags]

        if not tags:
            lbl = Gtk.Label(label="None")
            lbl.add_css_class("text-muted")
            self.tags_flow.append(lbl)
        else:
            for tag in tags[:8]:
                chip = Gtk.Label(label=str(tag))
                chip.add_css_class("tag-chip")
                self.tags_flow.append(chip)

    def clear(self):
        self.selected_wp = None
        self.preview_image.set_image_from_path(None, None)
        self.lbl_title.set_label("Select a Wallpaper")
        self.lbl_title.remove_css_class("nickname-text")
        self.lbl_original_name.set_visible(False)
        self.btn_edit_nickname.set_visible(False)
        self.lbl_folder.set_label("")
        self.lbl_size.set_label("")
        self.lbl_index.set_label("")
        self.lbl_type.set_label("-")
        self.lbl_desc.set_label("No description.")
        
        while True:
            child = self.tags_flow.get_first_child()
            if child is None: break
            self.tags_flow.remove(child)

    def on_apply_clicked(self, btn):
        if self.selected_wp:
            mode = self.get_apply_mode()
            
            if mode == "same" and self.available_screens:
                self.controller.apply(self.selected_wp, screens=self.available_screens)
                self.log_manager.add_info(f"Applied wallpaper {self.selected_wp} to ALL screens: {self.available_screens}", "Sidebar")
            else:
                current_screen = self.get_current_screen()
                self.controller.apply(self.selected_wp, screen=current_screen)

    def on_workshop_clicked(self, btn):
        if self.selected_wp:
            url = f"steam://url/CommunityFilePage/{self.selected_wp}"
            webbrowser.open(url)

    def on_folder_clicked(self, gesture, n_press, x, y):
        if self.selected_wp:
            clipboard = Gdk.Display.get_default().get_clipboard()
            clipboard.set(self.selected_wp)
            self.log_manager.add_info(f"Copied ID to clipboard: {self.selected_wp}", "GUI")
            
            # Temporary green tooltip feedback
            self.lbl_folder.set_tooltip_markup("<span foreground='#22c55e' weight='bold'>Copied!</span>")
            
            def reset_tooltip():
                self.lbl_folder.set_tooltip_text("Click to copy ID")
                return False
                
            GLib.timeout_add(2000, reset_tooltip)

    def set_compact_mode(self, enabled: bool):
        self._compact_mode = enabled
        self.lbl_folder.set_visible(not enabled)
        self.desc_header.set_visible(not enabled)
        self.lbl_desc.set_visible(not enabled)
        self.btn_workshop.set_visible(not enabled)
        self.thumb_grid.set_visible(enabled)
        self.compact_actions.set_visible(enabled)
        if enabled:
            self._update_thumb_grid()

    def set_wallpaper_ids(self, ids: list):
        self._wallpaper_ids = ids

    def set_thumb_clicked_callback(self, cb):
        self._on_thumb_clicked_cb = cb

    def set_compact_callbacks(self, on_stop=None, on_lucky=None, on_jump=None):
        self._on_stop_cb = on_stop
        self._on_lucky_cb = on_lucky
        self._on_jump_cb = on_jump

    def _update_thumb_grid(self):
        while True:
            child = self.thumb_grid.get_first_child()
            if child is None:
                break
            self.thumb_grid.remove(child)

        if not self.selected_wp or not self._wallpaper_ids:
            return

        try:
            current_idx = self._wallpaper_ids.index(self.selected_wp)
        except ValueError:
            return

        start_idx = max(0, current_idx - 2)
        end_idx = min(len(self._wallpaper_ids), current_idx + 3)
        
        for idx in range(start_idx, end_idx):
            wp_id = self._wallpaper_ids[idx]
            thumb = self._create_thumbnail(wp_id, is_current=(idx == current_idx))
            self.thumb_grid.append(thumb)

    def _create_thumbnail(self, wp_id: str, is_current: bool) -> Gtk.Widget:
        btn = Gtk.Button()
        btn.set_size_request(50, 50)
        btn.set_has_frame(False)
        
        wp = self.wp_manager._wallpapers.get(wp_id)
        if wp:
            if wp_id in self._thumb_cache:
                texture = self._thumb_cache[wp_id]
            else:
                texture = self.wp_manager.get_texture(wp['preview'], 50)
                self._thumb_cache[wp_id] = texture
            
            picture = Gtk.Picture()
            picture.set_paintable(texture)
            picture.set_content_fit(Gtk.ContentFit.COVER)
            picture.set_size_request(50, 50)
            btn.set_child(picture)
        
        if is_current:
            btn.add_css_class("suggested-action")
        
        btn.connect("clicked", lambda b, wid=wp_id: self._on_thumb_click(wid))
        return btn

    def _on_thumb_click(self, wp_id: str):
        if callable(self._on_thumb_clicked_cb):
            self._on_thumb_clicked_cb(wp_id)

```

---

### 📄 文件: `py_GUI/ui/components/sparkline.py`

```python
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib
import cairo

class Sparkline(Gtk.DrawingArea):
    def __init__(self, color=(0.2, 0.6, 1.0), height=60, title="", max_points=60):
        super().__init__()
        self.set_content_height(height)
        self.set_vexpand(False)
        self.set_hexpand(True)
        self.set_draw_func(self.on_draw)
        
        self.data = []
        self.max_val = 100.0
        self.color = color
        self.title = title
        self.unit = ""
        self.max_points = max_points
        
        # Margins
        self.margin_left = 35
        self.margin_right = 10
        self.margin_top = 15
        self.margin_bottom = 15

    def set_data(self, data, max_val=None, unit=""):
        self.data = list(data) # Copy data
        self.unit = unit
        if max_val is not None:
            self.max_val = max_val
        elif data:
            self.max_val = max(max(data) * 1.2, 1.0)
        self.queue_draw()

    def set_color(self, color):
        self.color = color
        self.queue_draw()

    def on_draw(self, area, ctx, width, height):
        # Calculate plotting area
        graph_width = width - self.margin_left - self.margin_right
        graph_height = height - self.margin_top - self.margin_bottom
        
        # Draw Background Grid
        ctx.set_line_width(1.0)
        ctx.set_source_rgba(1, 1, 1, 0.05)
        
        # Horizontal lines (0%, 25%, 50%, 75%, 100%)
        ctx.set_font_size(9)
        for i in [0, 0.25, 0.5, 0.75, 1.0]:
            y_rel = graph_height * (1 - i)
            y = self.margin_top + y_rel
            
            # Draw grid line
            ctx.move_to(self.margin_left, y)
            ctx.line_to(width - self.margin_right, y)
            
            # Draw label
            if self.max_val > 0:
                val = int(self.max_val * i)
                label = f"{val}{self.unit}"
                ctx.set_source_rgba(1, 1, 1, 0.4)
                extents = ctx.text_extents(label)
                # Align right vertically centered
                ctx.move_to(self.margin_left - extents.width - 5, y + extents.height/2 - 1)
                ctx.show_text(label)
                
            # Reset for line drawing
            ctx.set_source_rgba(1, 1, 1, 0.05)
        
        # Vertical lines (60s, 45s, 30s, 15s, 0s)
        for i in [0.25, 0.5, 0.75]:
            x = self.margin_left + graph_width * i
            ctx.move_to(x, self.margin_top)
            ctx.line_to(x, height - self.margin_bottom)
            
        ctx.stroke()

        # Labels (Title, Time)
        ctx.set_source_rgba(1, 1, 1, 0.5)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(10)
        
        # Title
        if self.title:
            ctx.move_to(self.margin_left, 10)
            ctx.show_text(self.title)
            
        # Time Labels
        ctx.set_font_size(9)
        ctx.move_to(self.margin_left, height - 2)
        ctx.show_text("60s")
        
        ctx.move_to(self.margin_left + graph_width * 0.5 - 10, height - 2)
        ctx.show_text("30s")
        
        ctx.move_to(width - self.margin_right - 20, height - 2)
        ctx.show_text("Now")

        if not self.data:
            return

        ctx.set_line_width(2.0)
        ctx.set_source_rgba(*self.color, 1.0)

        # Scale calculation
        # Always use max_points - 1 to calculate step, ensuring 60s scale
        step_x = graph_width / (self.max_points - 1)
        scale_y = graph_height / self.max_val if self.max_val > 0 else 1.0
        
        # Calculate start x (align right if fewer points)
        points_count = len(self.data)
        start_offset = (self.max_points - points_count) * step_x

        # Draw path
        # Clamp values to avoid drawing outside
        first_val = min(self.data[0], self.max_val)
        ctx.move_to(self.margin_left + start_offset, 
                   self.margin_top + graph_height - (first_val * scale_y))
        
        for i, val in enumerate(self.data[1:], 1):
            val = min(val, self.max_val)
            x = self.margin_left + start_offset + i * step_x
            y = self.margin_top + graph_height - (val * scale_y)
            ctx.line_to(x, y)
        
        ctx.stroke_preserve()

        # Fill under line
        ctx.line_to(self.margin_left + start_offset + (points_count - 1) * step_x, 
                   self.margin_top + graph_height)
        ctx.line_to(self.margin_left + start_offset, 
                   self.margin_top + graph_height)
        ctx.close_path()
        ctx.set_source_rgba(*self.color, 0.1)
        ctx.fill()

```

---

### 📄 文件: `py_GUI/ui/components/welcome_dialog.py`

```python
import os
import gi
gi.require_version('Gtk', '4.0')
try:
    gi.require_version('Adw', '1')
except ValueError:
    pass
from gi.repository import Gtk, Adw, Gdk, Gio

class WelcomeDialog(Gtk.Window):
    def __init__(self, parent, config, integrator):
        super().__init__(transient_for=parent, modal=True)
        self.config = config
        self.integrator = integrator
        
        self.set_title("Welcome")
        self.set_default_size(500, 450)
        self.set_resizable(False)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=32)
        main_box.set_margin_top(40)
        main_box.set_margin_bottom(40)
        main_box.set_margin_start(40)
        main_box.set_margin_end(40)
        self.set_child(main_box)
        
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        main_box.append(header_box)
        
        # 尝试获取自定义 Logo
        logo_path = self._resolve_logo_path()
        
        if logo_path:
            # 如果找到了图片文件，就加载文件
            icon = Gtk.Image.new_from_file(logo_path)
        else:
            # 找不到就回退到系统图标，防止界面空白
            icon = Gtk.Image.new_from_icon_name("preferences-desktop-wallpaper")
            icon.add_css_class("accent")
            
        icon.set_pixel_size(100)
        header_box.append(icon)
        
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        header_box.append(title_box)
        
        title = Gtk.Label(label="Welcome to Linux Wallpaper Engine")
        title.add_css_class("title-1")
        title_box.append(title)
        
        subtitle = Gtk.Label(label="Let's get you set up in just a few steps.")
        subtitle.add_css_class("body")
        subtitle.add_css_class("dim-label")
        title_box.append(subtitle)
        
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        main_box.append(content_box)
        
        step1_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        content_box.append(step1_box)
        
        lbl_path = Gtk.Label(label="Steam Workshop Path")
        lbl_path.set_halign(Gtk.Align.START)
        lbl_path.add_css_class("heading")
        step1_box.append(lbl_path)
        
        path_input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        step1_box.append(path_input_box)
        
        current_path = self.config.get('workshopPath', '')
        self.path_entry = Gtk.Entry()
        self.path_entry.set_placeholder_text("/path/to/steamapps/workshop/content/431960")
        if current_path:
            self.path_entry.set_text(current_path)
        self.path_entry.set_hexpand(True)
        path_input_box.append(self.path_entry)
        
        btn_browse = Gtk.Button(icon_name="folder-open-symbolic")
        btn_browse.set_tooltip_text("Browse Folder")
        btn_browse.connect("clicked", self.on_browse_clicked)
        path_input_box.append(btn_browse)
        
        path_desc = Gtk.Label(label="Select the folder where Wallpaper Engine wallpapers are installed (ID: 431960).")
        path_desc.set_halign(Gtk.Align.START)
        path_desc.add_css_class("caption")
        path_desc.add_css_class("dim-label")
        path_desc.set_wrap(True)
        path_desc.set_max_width_chars(50)
        step1_box.append(path_desc)
        
        step2_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        content_box.append(step2_box)
        
        vbox_auto = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox_auto.set_hexpand(True)
        step2_box.append(vbox_auto)
        
        lbl_auto = Gtk.Label(label="Start with System")
        lbl_auto.set_halign(Gtk.Align.START)
        lbl_auto.add_css_class("heading")
        vbox_auto.append(lbl_auto)
        
        desc_auto = Gtk.Label(label="Automatically start in background when you log in.")
        desc_auto.set_halign(Gtk.Align.START)
        desc_auto.add_css_class("caption")
        desc_auto.add_css_class("dim-label")
        vbox_auto.append(desc_auto)
        
        self.switch_auto = Gtk.Switch()
        self.switch_auto.set_valign(Gtk.Align.CENTER)
        if self.integrator.is_autostart_enabled():
            self.switch_auto.set_active(True)
        step2_box.append(self.switch_auto)
        
        footer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        footer_box.set_valign(Gtk.Align.END)
        footer_box.set_vexpand(True)
        main_box.append(footer_box)
        
        self.btn_start = Gtk.Button(label="Start Using App")
        self.btn_start.add_css_class("suggested-action")
        self.btn_start.add_css_class("pill")
        self.btn_start.set_size_request(200, 44)
        self.btn_start.set_halign(Gtk.Align.CENTER)
        self.btn_start.connect("clicked", self.on_start_clicked)
        footer_box.append(self.btn_start)

    def _resolve_logo_path(self):
        """
        智能查找 Logo 图片路径，兼容源码、AppImage 和系统安装包
        """
        candidates = []
        filename = "pic/icons/GUI_rounded.png"

        # 1. AppImage 环境优先 (检测 APPDIR 环境变量)
        appdir = os.getenv('APPDIR')
        if appdir:
            # 对应 build 脚本中的安装路径
            candidates.append(os.path.join(appdir, "usr/share/linux-wallpaperengine-gui", filename))

        # 2. 系统/Arch 包安装路径
        candidates.append(os.path.join("/usr/share/linux-wallpaperengine-gui", filename))

        # 3. 源码开发环境 (相对于当前文件的位置)
        # 当前文件在 py_GUI/ui/welcome_dialog.py
        # 项目根目录是往上推 3 级
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            candidates.append(os.path.join(base_path, filename))
        except Exception:
            pass

        # 遍历检查，返回第一个存在的路径
        for path in candidates:
            if os.path.exists(path):
                return path
        return None

    def on_browse_clicked(self, button):
        dialog = Gtk.FileChooserNative(
            title="Select Workshop Folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        
        dialog.set_modal(True)
        
        def on_response(d, response):
            if response == Gtk.ResponseType.ACCEPT:
                file = d.get_file()
                path = file.get_path()
                if path:
                    self.path_entry.set_text(path)
            d.destroy()
            
        dialog.connect("response", on_response)
        dialog.show()

    def on_start_clicked(self, button):
        path = self.path_entry.get_text().strip()
        if path:
            self.config.set('workshopPath', path)
            
        enable_autostart = self.switch_auto.get_active()
        try:
            self.integrator.set_autostart(enable_autostart)
        except Exception as e:
            print(f"Failed to set autostart: {e}")
            
        self.config.set('onboarding_completed', True)
        
        self.destroy()

```

---

### 📄 文件: `py_GUI/ui/pages/__init__.py`

```python

```

---

### 📄 文件: `py_GUI/ui/pages/performance.py`

```python
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib, Pango

import time
from typing import Dict, List
from py_GUI.core.controller import WallpaperController
from py_GUI.ui.components.sparkline import Sparkline

class PerformancePage(Gtk.Box):
    def __init__(self, controller: WallpaperController):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.controller = controller
        
        # Inject Custom CSS
        provider = Gtk.CssProvider()
        css = """
        .memory-text {
            color: #2980b9;
            font-weight: bold;
        }
        """
        provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.append(scroll)
        
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
        self.content_box.set_margin_top(40)
        self.content_box.set_margin_bottom(40)
        self.content_box.set_margin_start(40)
        self.content_box.set_margin_end(40)
        scroll.set_child(self.content_box)

        self.build_ui()
        
        self.controller.perf_monitor.add_callback(self.on_perf_update)

    def build_ui(self):
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.content_box.append(title_box)
        
        t = Gtk.Label(label="System Monitor")
        t.add_css_class("settings-header")
        t.set_halign(Gtk.Align.START)
        title_box.append(t)

        desc = Gtk.Label(label="Real-time resource usage of Wallpaper Engine components.")
        desc.add_css_class("settings-subheader")
        desc.set_halign(Gtk.Align.START)
        title_box.append(desc)

        self.overview_grid = Gtk.Grid()
        self.overview_grid.set_column_spacing(20)
        self.overview_grid.set_row_spacing(20)
        self.overview_grid.set_halign(Gtk.Align.FILL)
        self.content_box.append(self.overview_grid)

        self.total_labels = {}
        self.create_overview_card("Total CPU", "cpu", 0, 0, unit="%")
        self.create_overview_card("Total Memory", "memory_mb", 0, 1, unit=" MB")
        self.create_overview_card("Active Threads", "threads", 0, 2)
        
        # Total Charts Row
        total_charts_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.content_box.append(total_charts_row)
        
        # Total CPU Chart
        cpu_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        cpu_card.add_css_class("card")
        cpu_card.set_hexpand(True)
        self.total_cpu_chart = Sparkline(color=(0.937, 0.267, 0.267), height=150, title="Total CPU History")
        cpu_card.append(self.total_cpu_chart)
        total_charts_row.append(cpu_card)
        
        # Total Mem Chart
        mem_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        mem_card.add_css_class("card")
        mem_card.set_hexpand(True)
        self.total_mem_chart = Sparkline(color=(0.16, 0.5, 0.73), height=150, title="Total Memory History")
        mem_card.append(self.total_mem_chart)
        total_charts_row.append(mem_card)

        self.content_box.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))
        
        table_label = Gtk.Label(label="Process Details")
        table_label.add_css_class("settings-section-title")
        table_label.set_halign(Gtk.Align.START)
        self.content_box.append(table_label)

        self.process_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.content_box.append(self.process_list)
        
        self.process_widgets = {}
        
        self.build_screenshot_history_panel()

    def create_overview_card(self, title, key, row, col, unit=""):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        card.add_css_class("card")
        card.add_css_class("setting-row")
        card.set_hexpand(True)
        card.set_margin_top(5)
        card.set_margin_bottom(5)
        card.set_margin_start(10)
        card.set_margin_end(10)
        
        lbl_title = Gtk.Label(label=title)
        lbl_title.add_css_class("setting-desc")
        lbl_title.set_halign(Gtk.Align.START)
        card.append(lbl_title)
        
        lbl_val = Gtk.Label(label="-")
        lbl_val.add_css_class("settings-header")
        lbl_val.set_halign(Gtk.Align.START)
        card.append(lbl_val)
        
        self.overview_grid.attach(card, col, row, 1, 1)
        self.total_labels[key] = (lbl_val, unit)


    def on_perf_update(self, stats: Dict):
        GLib.idle_add(lambda: self._update_ui(stats))

    def _update_ui(self, stats: Dict):
        total = stats.get("total", {})
        for key, (lbl, unit) in self.total_labels.items():
            fmt_key = f"{key}_fmt"
            if fmt_key in total:
                lbl.set_label(total[fmt_key])
            else:
                val = total.get(key, 0)
                lbl.set_label(f"{val}{unit}")
            
            if key == "cpu":
                lbl.remove_css_class("success")
                lbl.remove_css_class("warning")
                lbl.remove_css_class("error")
                cpu_val = total.get("cpu", 0)
                if cpu_val < 20:
                    lbl.add_css_class("success")
                elif cpu_val < 40:
                    lbl.add_css_class("warning")
                else:
                    lbl.add_css_class("error")
            elif key == "memory_mb":
                lbl.add_css_class("memory-text")
        
        history = total.get("history", {})
        if "cpu" in history:
            cpu_data = history["cpu"]
            max_cpu = max(max(cpu_data) * 1.2, 10.0) if cpu_data else 10.0
            max_cpu = min(max_cpu, 100.0)
            self.total_cpu_chart.set_data(cpu_data, max_val=max_cpu, unit="%")
            
            current_cpu = cpu_data[-1] if cpu_data else 0
            if current_cpu < 20:
                self.total_cpu_chart.set_color((0.18, 0.76, 0.49))
            elif current_cpu < 40:
                self.total_cpu_chart.set_color((0.96, 0.62, 0.04))
            else:
                self.total_cpu_chart.set_color((0.88, 0.11, 0.14))
            
        if "memory_mb" in history:
            self.total_mem_chart.set_data(history["memory_mb"], unit=" MB")
        
        thread_names = total.get("thread_names", {})

        # Update Process List
        details = stats.get("details", {})
        
        # Remove stale
        current_pids = set(d['pid'] for d in details.values())
        tracked_pids = set(self.process_widgets.keys())
        
        for pid in tracked_pids - current_pids:
            row = self.process_widgets.pop(pid)
            self.process_list.remove(row)

        # Update/Add
        for category, data in details.items():
            pid = data['pid']
            if pid not in self.process_widgets:
                row = self._create_process_row(category, data)
                self.process_list.append(row)
                self.process_widgets[pid] = row
            
            self._update_process_row(self.process_widgets[pid], category, data, thread_names.get(category, []))
        
        history = self.controller.perf_monitor.get_screenshot_history()
        latest_ts = history[-1].get("timestamp", 0) if history else 0
        if latest_ts != self._last_screenshot_ts:
            self._last_screenshot_ts = latest_ts
            self._refresh_screenshot_history()


    def _clean_thread_name(self, name: str) -> str:
        name = name.strip()
        
        # Mapping for known truncated/ugly names
        mapping = {
            "linux-w:disk$0": "Disk I/O 0",
            "linux-w:disk$1": "Disk I/O 1",
            "linux-w:disk$2": "Disk I/O 2",
            "linux-w:disk$3": "Disk I/O 3",
            "linux-wa:gdrv0": "Graphics Drv 0",
            "SDLPwAudioPlug": "Audio (SDL)",
            "gly-global-exec": "GStreamer Exec",
            "gmain": "GLib Main",
            "gdbus": "GDBus Worker",
            "dconf worker": "DConf Worker",
            "pool-spawner": "GStreamer Pool",
            "videoconvert0:s": "Video Convert",
            "Thread-1(_moni": "PerfMonitor",
        }
        
        if name in mapping:
            return mapping[name]
            
        # Generic cleanups
        if name.startswith("Thread-") and "(_" in name:
            try:
                # Try to extract function name: Thread-1(_monitor_loop) -> Monitor Loop
                func = name.split("(_")[1].split(")")[0]
                # Handle truncated case like "_moni"
                if func == "_moni": return "PerfMonitor"
                return func.replace("_", " ").title().strip()
            except Exception:
                pass
                
        return name

    def _create_process_row(self, category: str, data: Dict) -> Gtk.Box:
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        main_box.add_css_class("list-item")
        
        # Header Row (Icon + Info + Current Stats)
        header_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        main_box.append(header_row)
        
        # Icon/Type
        icon_name = "application-x-executable-symbolic"
        if category == "frontend": icon_name = "preferences-desktop-wallpaper-symbolic"
        elif category == "backend": icon_name = "video-display-symbolic"
        elif category == "tray": icon_name = "system-run-symbolic"
        
        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(32)
        header_row.append(icon)

        # Info
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info_box.set_hexpand(True)
        header_row.append(info_box)

        name_lbl = Gtk.Label(label=f"{category.title()} ({data['pid']})")
        name_lbl.add_css_class("list-title")
        name_lbl.set_halign(Gtk.Align.START)
        info_box.append(name_lbl)

        cmd_lbl = Gtk.Label(label=data['name'])
        cmd_lbl.add_css_class("text-muted")
        cmd_lbl.set_halign(Gtk.Align.START)
        cmd_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        info_box.append(cmd_lbl)

        # Current Stats
        stats_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        header_row.append(stats_box)

        main_box.cpu_lbl = Gtk.Label()
        main_box.cpu_lbl.add_css_class("error")
        main_box.mem_lbl = Gtk.Label()
        main_box.mem_lbl.add_css_class("memory-text")
        main_box.status_lbl = Gtk.Label()
        
        # CPU
        b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        b.set_size_request(80, -1)
        b.append(main_box.cpu_lbl)
        l = Gtk.Label(label="CPU")
        l.add_css_class("text-muted")
        b.append(l)
        stats_box.append(b)

        # MEM
        b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        b.set_size_request(100, -1)
        b.append(main_box.mem_lbl)
        l = Gtk.Label(label="Memory")
        l.add_css_class("text-muted")
        b.append(l)
        stats_box.append(b)

        # Status
        b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        b.set_size_request(80, -1)
        b.append(main_box.status_lbl)
        l = Gtk.Label(label="Status")
        l.add_css_class("text-muted")
        b.append(l)
        stats_box.append(b)

        # Charts Row
        charts_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        charts_row.set_margin_start(52) # Align with text
        main_box.append(charts_row)
        
        # CPU Chart
        cpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        cpu_box.set_hexpand(True)
        main_box.cpu_chart = Sparkline(color=(0.937, 0.267, 0.267), height=120, title="CPU Usage")
        cpu_box.append(main_box.cpu_chart)
        charts_row.append(cpu_box)
        
        # Mem Chart
        mem_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        mem_box.set_hexpand(True)
        main_box.mem_chart = Sparkline(color=(0.16, 0.5, 0.73), height=120, title="Memory Usage")
        mem_box.append(main_box.mem_chart)
        charts_row.append(mem_box)
        
        # Spacer to match status column
        spacer = Gtk.Box()
        spacer.set_size_request(80, -1)
        charts_row.append(spacer)

        # Wallpaper Details Expander (Backend only)
        if category == "backend":
            main_box.details_expander = Gtk.Expander(label="Wallpaper Details")
            main_box.details_expander.add_css_class("boxed-expander")
            main_box.details_expander.set_margin_start(52)
            main_box.details_expander.set_visible(False)
            
            main_box.details_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            main_box.details_box.set_margin_top(5)
            main_box.details_box.set_margin_bottom(10)
            main_box.details_expander.set_child(main_box.details_box)
            
            main_box.append(main_box.details_expander)
            main_box.last_monitors_hash = None

        # Thread Details Expander (All processes)
        main_box.threads_expander = Gtk.Expander(label="Thread Details")
        main_box.threads_expander.add_css_class("boxed-expander")
        main_box.threads_expander.set_margin_start(52)
        main_box.threads_expander.set_expanded(False)
        
        main_box.threads_grid = Gtk.Grid()
        main_box.threads_grid.set_column_spacing(20)
        main_box.threads_grid.set_row_spacing(6)
        main_box.threads_grid.set_column_homogeneous(True)
        main_box.threads_grid.set_margin_top(5)
        main_box.threads_grid.set_margin_bottom(10)
        
        main_box.threads_expander.set_child(main_box.threads_grid)
        main_box.append(main_box.threads_expander)

        return main_box

    def _update_process_row(self, row, category, data, thread_names: List[str]):
        cpu_val = data.get('cpu', 0)
        row.cpu_lbl.set_label(data.get('cpu_fmt', f"{cpu_val}%"))
        
        # Colorize CPU Label
        row.cpu_lbl.remove_css_class("success")
        row.cpu_lbl.remove_css_class("warning")
        row.cpu_lbl.remove_css_class("error")
        
        if cpu_val < 20:
            row.cpu_lbl.add_css_class("success")
            cpu_color = (0.18, 0.76, 0.49) # Green
        elif cpu_val < 40:
            row.cpu_lbl.add_css_class("warning")
            cpu_color = (0.96, 0.62, 0.04) # Orange
        else:
            row.cpu_lbl.add_css_class("error")
            cpu_color = (0.88, 0.11, 0.14) # Red
            
        row.mem_lbl.set_label(data.get('memory_fmt', f"{data['memory_mb']} MB"))
        row.status_lbl.set_label(data['status'].upper())
        
        history = data.get("history", {})
        if "cpu" in history:
            # Auto-scale CPU chart (min 10% to prevent flatline at very low usage)
            cpu_data = history["cpu"]
            max_cpu = max(max(cpu_data) * 1.2, 10.0) if cpu_data else 10.0
            max_cpu = min(max_cpu, 100.0) # Cap at 100%
            row.cpu_chart.set_data(cpu_data, max_val=max_cpu, unit="%")
            row.cpu_chart.set_color(cpu_color)
            
        if "memory_mb" in history:
            # Auto-scale memory chart
            row.mem_chart.set_data(history["memory_mb"], unit=" MB")

        while row.threads_grid.get_first_child():
            row.threads_grid.remove(row.threads_grid.get_first_child())
            
        if thread_names:
            row.threads_expander.set_label(f"Thread Details ({len(thread_names)})")
            for i, name in enumerate(thread_names):
                clean_name = self._clean_thread_name(name)
                row_idx = i // 3
                col_idx = i % 3
                lbl = Gtk.Label(label=f"• {clean_name}")
                lbl.set_halign(Gtk.Align.START)
                lbl.add_css_class("text-muted")
                lbl.set_ellipsize(Pango.EllipsizeMode.END)
                row.threads_grid.attach(lbl, col_idx, row_idx, 1, 1)
        else:
            row.threads_expander.set_label("Thread Details (0)")

        # Update Wallpaper Details (Backend only)
        if category == "backend" and hasattr(row, 'details_expander'):
            try:
                active_monitors = self.controller.config.get("active_monitors", {})
                current_hash = str(active_monitors)
                
                if current_hash != row.last_monitors_hash:
                    row.last_monitors_hash = current_hash
                    
                    if active_monitors:
                        row.details_expander.set_visible(True)
                        
                        while row.details_box.get_first_child():
                            row.details_box.remove(row.details_box.get_first_child())
                        
                        for screen, wp_id in active_monitors.items():
                            display_name = "Unknown"
                            secondary_text = None
                            preview_path = None
                            clean_id = str(wp_id).strip()
                            
                            if hasattr(self.controller, 'wp_manager'):
                                wp = self.controller.wp_manager.get_wallpaper(clean_id)
                                if wp:
                                    if hasattr(self.controller, 'nickname_manager'):
                                        display_name, secondary_text = self.controller.nickname_manager.get_display_name(wp)
                                    else:
                                        display_name = wp.get("title", "Untitled")
                                    preview_path = wp.get("preview")
                            
                            s_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
                            s_row.set_margin_top(5)
                            s_row.set_margin_bottom(5)
                            row.details_box.append(s_row)
                            
                            if preview_path and hasattr(self.controller, 'wp_manager'):
                                texture = self.controller.wp_manager.get_texture(preview_path, size=64)
                                if texture:
                                    thumb = Gtk.Picture.new_for_paintable(texture)
                                    thumb.set_size_request(64, 36)
                                    thumb.set_content_fit(Gtk.ContentFit.COVER)
                                    thumb.add_css_class("thumbnail")
                                    s_row.append(thumb)
                                else:
                                    placeholder = Gtk.Image.new_from_icon_name("image-missing-symbolic")
                                    placeholder.set_pixel_size(36)
                                    s_row.append(placeholder)
                            else:
                                placeholder = Gtk.Image.new_from_icon_name("video-display-symbolic")
                                placeholder.set_pixel_size(36)
                                s_row.append(placeholder)
                            
                            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
                            info_box.set_valign(Gtk.Align.CENTER)
                            s_row.append(info_box)
                            
                            screen_lbl = Gtk.Label(label=screen)
                            screen_lbl.set_halign(Gtk.Align.START)
                            screen_lbl.add_css_class("heading")
                            info_box.append(screen_lbl)
                            
                            title_lbl = Gtk.Label(label=display_name)
                            title_lbl.set_halign(Gtk.Align.START)
                            title_lbl.set_ellipsize(Pango.EllipsizeMode.END)
                            title_lbl.set_max_width_chars(40)
                            info_box.append(title_lbl)
                            
                            if secondary_text:
                                subtitle_lbl = Gtk.Label(label=secondary_text)
                                subtitle_lbl.add_css_class("text-muted")
                                subtitle_lbl.set_halign(Gtk.Align.START)
                                subtitle_lbl.set_ellipsize(Pango.EllipsizeMode.END)
                                subtitle_lbl.set_max_width_chars(40)
                                info_box.append(subtitle_lbl)
                            
                            id_lbl = Gtk.Label(label=f"ID: {wp_id}")
                            id_lbl.add_css_class("text-muted")
                            id_lbl.set_halign(Gtk.Align.START)
                            info_box.append(id_lbl)
                    else:
                        row.details_expander.set_visible(False)
            except Exception as e:
                print(f"[Performance] Backend details error: {e}")

    def build_screenshot_history_panel(self):
        self.content_box.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))
        
        header_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.content_box.append(header_row)
        
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        header_box.set_hexpand(True)
        header_row.append(header_box)
        
        header = Gtk.Label(label="Screenshot History")
        header.add_css_class("settings-section-title")
        header.set_halign(Gtk.Align.START)
        header_box.append(header)
        
        desc = Gtk.Label(label="Resource usage from recent screenshot captures (last 10).")
        desc.add_css_class("text-muted")
        desc.set_halign(Gtk.Align.START)
        header_box.append(desc)
        
        clear_btn = Gtk.Button(label="Clear")
        clear_btn.set_tooltip_text("Clear all screenshot history")
        clear_btn.connect("clicked", self._on_clear_history_clicked)
        clear_btn.set_valign(Gtk.Align.CENTER)
        header_row.append(clear_btn)
        
        self.screenshot_history_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.content_box.append(self.screenshot_history_box)
        
        self._last_screenshot_ts = 0
        self._refresh_screenshot_history()

    def _refresh_screenshot_history(self):
        while self.screenshot_history_box.get_first_child():
            self.screenshot_history_box.remove(self.screenshot_history_box.get_first_child())
        
        history = self.controller.perf_monitor.get_screenshot_history()
        
        if not history:
            empty_label = Gtk.Label(label="No screenshots taken yet.")
            empty_label.add_css_class("text-muted")
            empty_label.set_halign(Gtk.Align.START)
            self.screenshot_history_box.append(empty_label)
            return
        
        for record in reversed(history):
            row = self._create_screenshot_history_row(record)
            self.screenshot_history_box.append(row)

    def _on_clear_history_clicked(self, btn):
        self.controller.perf_monitor.clear_screenshot_history()
        self._last_screenshot_ts = 0
        self._refresh_screenshot_history()

    def _create_screenshot_history_row(self, record: Dict) -> Gtk.Box:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        row.add_css_class("list-item")
        row.set_margin_top(5)
        row.set_margin_bottom(5)
        
        wp_id = record.get("wp_id", "Unknown")
        output_path = record.get("output_path", "")
        display_name = None
        secondary_text = None
        thumbnail_added = False
        
        if hasattr(self.controller, 'wp_manager'):
            wp = self.controller.wp_manager.get_wallpaper(str(wp_id))
            if wp:
                # Use nickname_manager to get display name
                if hasattr(self.controller, 'nickname_manager'):
                    display_name, secondary_text = self.controller.nickname_manager.get_display_name(wp)
                else:
                    display_name = wp.get("title")
                
                if wp.get("preview"):
                    texture = self.controller.wp_manager.get_texture(wp["preview"], size=48)
                    if texture:
                        thumb = Gtk.Picture.new_for_paintable(texture)
                        thumb.set_size_request(48, 27)
                        thumb.set_content_fit(Gtk.ContentFit.COVER)
                        thumb.add_css_class("thumbnail")
                        row.append(thumb)
                        thumbnail_added = True
        
        if not thumbnail_added:
            icon = Gtk.Image.new_from_icon_name("camera-photo-symbolic")
            icon.set_pixel_size(24)
            row.append(icon)
        
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info_box.set_hexpand(True)
        row.append(info_box)
        
        timestamp = record.get("timestamp", 0)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        
        # Use display_name from nickname_manager, or fallback
        if not display_name:
            display_name = f"Wallpaper {wp_id}"
        
        title_lbl = Gtk.Label(label=display_name)
        title_lbl.add_css_class("list-title")
        title_lbl.set_halign(Gtk.Align.START)
        title_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        title_lbl.set_max_width_chars(30)
        info_box.append(title_lbl)
        
        time_lbl = Gtk.Label(label=time_str)
        time_lbl.add_css_class("text-muted")
        time_lbl.set_halign(Gtk.Align.START)
        info_box.append(time_lbl)
        
        stats_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.append(stats_box)
        
        duration = record.get("duration", 0)
        max_cpu = record.get("max_cpu", 0)
        max_mem = record.get("max_mem", 0)
        
        self._add_stat_column(stats_box, f"{duration:.1f}s", "Duration", 70)
        self._add_stat_column(stats_box, f"{max_cpu:.1f}%", "Max CPU", 70)
        self._add_stat_column(stats_box, f"{max_mem:.1f} MB", "Max Mem", 80)
        
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        row.append(actions_box)
        
        open_folder_btn = Gtk.Button()
        open_folder_btn.set_icon_name("folder-open-symbolic")
        open_folder_btn.add_css_class("flat")
        open_folder_btn.set_tooltip_text("Open folder")
        open_folder_btn.connect("clicked", lambda _: self._open_screenshot_folder(output_path))
        actions_box.append(open_folder_btn)
        
        open_image_btn = Gtk.Button()
        open_image_btn.set_icon_name("image-x-generic-symbolic")
        open_image_btn.add_css_class("flat")
        open_image_btn.set_tooltip_text("Open image")
        open_image_btn.connect("clicked", lambda _: self._open_screenshot_image(output_path))
        actions_box.append(open_image_btn)
        
        return row

    def _open_screenshot_folder(self, path: str):
        import subprocess
        import shutil
        import os
        if not path or not os.path.exists(path):
            return
        
        folder = os.path.dirname(path)
        file_managers = [
            "thunar", "nautilus", "dolphin", "nemo",
            "pcmanfm", "pcmanfm-qt", "caja", "index", "files"
        ]
        
        for fm in file_managers:
            if shutil.which(fm):
                try:
                    subprocess.Popen([fm, folder])
                    return
                except Exception:
                    continue
        
        try:
            subprocess.Popen(["xdg-open", folder])
        except Exception:
            pass

    def _open_screenshot_image(self, path: str):
        import subprocess
        import os
        if path and os.path.exists(path):
            subprocess.Popen(["xdg-open", path])

    def _add_stat_column(self, parent: Gtk.Box, value: str, label: str, width: int):
        col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        col.set_size_request(width, -1)
        
        val_lbl = Gtk.Label(label=value)
        val_lbl.add_css_class("heading")
        col.append(val_lbl)
        
        lbl = Gtk.Label(label=label)
        lbl.add_css_class("text-muted")
        col.append(lbl)
        
        parent.append(col)

```

---

### 📄 文件: `py_GUI/ui/pages/settings.py`

```python
from typing import Dict, Callable
import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, GLib, Gdk, Adw, Gio

from py_GUI.const import WORKSHOP_PATH, ASSETS_PATH
from py_GUI.core.config import ConfigManager
from py_GUI.core.screen import ScreenManager
from py_GUI.core.logger import LogManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.integrations import AppIntegrator

class SettingsPage(Gtk.Box):
    def __init__(self, window, config: ConfigManager, screen_manager: ScreenManager, 
                 log_manager: LogManager, controller: WallpaperController,
                 wp_manager: WallpaperManager, nickname_manager, on_cycle_changed=None,
                 show_toast: Callable[[str], None] = None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        
        self.window = window
        self.config = config
        self.screen_manager = screen_manager
        self.log_manager = log_manager
        self.controller = controller
        self.wp_manager = wp_manager
        self.nickname_manager = nickname_manager
        self.integrator = AppIntegrator()
        self.on_cycle_settings_changed = on_cycle_changed
        self.show_toast = show_toast or (lambda msg: None)
        
        self.current_filter = "All"
        
        self.add_css_class("settings-container")
        self.build_ui()

    def build_ui(self):
        # Sidebar
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar.add_css_class("settings-sidebar")
        sidebar.set_size_request(280, -1)
        self.append(sidebar)

        # Headers
        header = Gtk.Label(label="Settings")
        header.add_css_class("settings-header")
        header.set_halign(Gtk.Align.START)
        header.set_margin_start(16)
        sidebar.append(header)

        subheader = Gtk.Label(label="Configure your experience")
        subheader.add_css_class("settings-subheader")
        subheader.set_halign(Gtk.Align.START)
        subheader.set_margin_start(16)
        subheader.set_margin_bottom(32)
        sidebar.append(subheader)

        # Nav Buttons
        nav_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        nav_box.set_vexpand(True)
        sidebar.append(nav_box)

        sections = [
            ("general", "General", "preferences-system-symbolic"),
            ("audio", "Audio", "audio-volume-high-symbolic"),
            ("advanced", "Advanced", "preferences-other-symbolic"),
            ("logs", "Logs", "text-x-generic-symbolic"),
        ]

        self.nav_btns = {}
        for section_id, label, icon in sections:
            btn = Gtk.ToggleButton()
            content = Adw.ButtonContent()
            content.set_icon_name(icon)
            content.set_label(label)
            btn.set_child(content)
            
            btn.add_css_class("settings-nav-item")
            nav_box.append(btn)
            self.nav_btns[section_id] = btn

        # Content Area - Stack directly without shared ScrolledWindow
        # Each tab manages its own scrolling to avoid showing scrollbar on short content
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_hexpand(True)
        self.stack.set_vexpand(True)
        self.stack.set_vhomogeneous(False)  # Allow different heights per page
        self.append(self.stack)

        # Build sub-pages
        self.build_general()
        self.build_audio()
        self.build_advanced()
        self.build_logs()

        # Connect signals
        for section_id, _, _ in sections:
            btn = self.nav_btns[section_id]
            btn.connect("toggled", self.on_nav_toggled, section_id)

        self.nav_btns["general"].set_active(True)

        # Bottom Actions
        actions = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        actions.set_margin_top(24)
        sidebar.append(actions)

        save_btn = Gtk.Button(label="Save Changes")
        save_btn.add_css_class("action-btn")
        save_btn.add_css_class("primary")
        save_btn.connect("clicked", self.on_save)
        actions.append(save_btn)

        refresh_btn = Gtk.Button(label="Reload Wallpapers")
        refresh_btn.add_css_class("action-btn")
        refresh_btn.add_css_class("secondary")
        refresh_btn.connect("clicked", self.on_reload)
        actions.append(refresh_btn)

        stop_btn = Gtk.Button(label="Stop Wallpaper")
        stop_btn.add_css_class("action-btn")
        stop_btn.add_css_class("danger")

        stop_btn.connect("clicked", self.on_stop_clicked)
        actions.append(stop_btn)

    def on_stop_clicked(self, _button):
        """安全停止壁纸，防止 window 或 app 为 None 导致崩溃"""
        if self.window is not None:
            app = self.window.get_application()
            if app is not None and hasattr(app, "stop_wallpaper"):
                app.stop_wallpaper()

    def on_nav_toggled(self, btn, section_id):
        if btn.get_active():
            for sid, b in self.nav_btns.items():
                if sid != section_id:
                    b.set_active(False)
            self.stack.set_visible_child_name(section_id)
            # No dynamic scroll policy needed

    def create_row(self, label, desc):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add_css_class("setting-row")
        
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info.set_hexpand(True)
        row.append(info)

        l = Gtk.Label(label=label)
        l.add_css_class("setting-label")
        l.set_halign(Gtk.Align.START)
        info.append(l)

        d = Gtk.Label(label=desc)
        d.add_css_class("setting-desc")
        d.set_halign(Gtk.Align.START)
        d.set_wrap(True)
        d.set_max_width_chars(50)
        info.append(d)
        
        return row

    def build_general(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.stack.add_named(scroll, "general")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        scroll.set_child(box)

        # Titles
        t = Gtk.Label(label="General")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        box.append(t)
        
        # Nicknames
        r = self.create_row("Wallpaper Nicknames", "Manage custom names for wallpapers.")
        box.append(r)
        
        btn_manage_nicks = Gtk.Button(label="Manage")
        btn_manage_nicks.set_valign(Gtk.Align.CENTER)
        btn_manage_nicks.connect("clicked", self.on_manage_nicknames)
        r.append(btn_manage_nicks)
        
        # FPS
        r = self.create_row("FPS Limit", "Target frames per second.")
        box.append(r)
        self.fps_spin = Gtk.SpinButton()
        self.fps_spin.set_range(1, 144)
        self.fps_spin.set_increments(1, 10)
        self.fps_spin.set_value(self.config.get("fps", 30))
        r.append(self.fps_spin)


        # Scaling
        r = self.create_row("Scaling Mode", "How the wallpaper fits.")
        box.append(r)
        scaling_opts = ["default", "stretch", "fit", "fill"]
        self.scaling_dd = Gtk.DropDown.new_from_strings(scaling_opts)
        curr = str(self.config.get("scaling") or "default")
        if curr in scaling_opts:
            self.scaling_dd.set_selected(scaling_opts.index(curr))
        r.append(self.scaling_dd)

        # Pause
        r = self.create_row("No Fullscreen Pause", "Keep running in fullscreen.")
        box.append(r)
        self.pause_sw = Gtk.Switch()
        self.pause_sw.set_active(self.config.get("noFullscreenPause", False))
        self.pause_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.pause_sw)

        # Mouse
        r = self.create_row("Disable Mouse", "Ignore mouse interaction.")
        box.append(r)
        self.mouse_sw = Gtk.Switch()
        self.mouse_sw.set_active(self.config.get("disableMouse", False))
        self.mouse_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.mouse_sw)

        # Parallax
        r = self.create_row("Disable Parallax", "Disable background movement with mouse.")
        box.append(r)
        self.parallax_sw = Gtk.Switch()
        self.parallax_sw.set_active(self.config.get("disableParallax", False))
        self.parallax_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.parallax_sw)

        # Particles
        r = self.create_row("Disable Particles", "Turn off fire, rain, and other particles.")
        box.append(r)
        self.particles_sw = Gtk.Switch()
        self.particles_sw.set_active(self.config.get("disableParticles", False))
        self.particles_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.particles_sw)

        # Clamping
        r = self.create_row("Clamping Mode", "Texture wrap mode at edges.")
        box.append(r)
        clamp_opts = ["clamp", "border", "repeat"]
        self.clamp_dd = Gtk.DropDown.new_from_strings(clamp_opts)
        curr_clamp = self.config.get("clamping", "clamp")
        if curr_clamp in clamp_opts:
            self.clamp_dd.set_selected(clamp_opts.index(curr_clamp))
        r.append(self.clamp_dd)

        # Automation
        t = Gtk.Label(label="Automation")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        t.set_margin_top(10)
        box.append(t)

        # Wallpaper Cycling
        r = self.create_row("Enable Wallpaper Cycling", "Automatically change wallpapers periodically.")
        box.append(r)
        self.cycle_sw = Gtk.Switch()
        self.cycle_sw.set_active(self.config.get("cycleEnabled", False))
        self.cycle_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.cycle_sw)

        # Interval
        r = self.create_row("Cycle Interval (Minutes)", "Time between wallpaper changes.")
        box.append(r)
        self.cycle_spin = Gtk.SpinButton()
        self.cycle_spin.set_range(1, 1440) # 1 min to 24 hours
        self.cycle_spin.set_increments(5, 30)
        self.cycle_spin.set_value(self.config.get("cycleInterval", 15))
        r.append(self.cycle_spin)

        # Order
        r = self.create_row("Cycle Order", "Order in which wallpapers are cycled.")
        box.append(r)
        order_opts = ["Random", "Title", "Size ↑", "Size ↓", "Type", "ID"]
        self.cycle_order_dd = Gtk.DropDown.new_from_strings(order_opts)
        
        curr_order = (self.config.get("cycleOrder") or "random").lower()
        # Find index
        idx = 0
        if curr_order == "size": 
             curr_order = "size ↑"
        elif curr_order == "size_desc":
             curr_order = "size ↓"

        for i, opt in enumerate(order_opts):
            if opt.lower() == curr_order:
                idx = i
                break
        self.cycle_order_dd.set_selected(idx)
        r.append(self.cycle_order_dd)

        # Wayland Tweaks
        t = Gtk.Label(label="Wayland Tweaks")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        t.set_margin_top(10)
        box.append(t)

        is_wayland = os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
        
        status_label = "✅ Wayland Session Detected" if is_wayland else "⚠️ X11 Session"
        desc = "Wayland-specific pause strategies."
        if not is_wayland:
            desc += " (Options disabled in X11)"
            
        r = self.create_row("Session Check", desc)
        box.append(r)
        
        lbl_status = Gtk.Label(label=status_label)
        lbl_status.add_css_class("status-value")
        if not is_wayland:
            lbl_status.add_css_class("text-muted")
        r.append(lbl_status)

        r = self.create_row("Pause Only When Active", "Only pause when fullscreen window is focused.")
        box.append(r)
        self.wl_active_sw = Gtk.Switch()
        self.wl_active_sw.set_active(self.config.get("wayland_only_active", False))
        self.wl_active_sw.set_valign(Gtk.Align.CENTER)
        if not is_wayland: self.wl_active_sw.set_sensitive(False)
        r.append(self.wl_active_sw)

        r = self.create_row("Ignore App IDs", "Comma-separated list of App IDs to ignore (e.g. dock,bar).")
        r.set_orientation(Gtk.Orientation.VERTICAL)
        box.append(r)
        
        self.wl_ignore_entry = Gtk.Entry()
        self.wl_ignore_entry.set_text(self.config.get("wayland_ignore_appids", ""))
        self.wl_ignore_entry.set_placeholder_text("app_id1, app_id2")
        if not is_wayland: self.wl_ignore_entry.set_sensitive(False)
        r.append(self.wl_ignore_entry)

    def build_audio(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.stack.add_named(scroll, "audio")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        scroll.set_child(box)

        t = Gtk.Label(label="Audio")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        box.append(t)

        # Silence
        r = self.create_row("Silence Wallpaper", "Mute all audio.")
        box.append(r)
        self.silence_sw = Gtk.Switch()
        self.silence_sw.set_active(self.config.get("silence", True))
        self.silence_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.silence_sw)

        # Volume
        r = self.create_row("Volume", "Master volume (0-100).")
        box.append(r)
        self.vol_spin = Gtk.SpinButton()
        self.vol_spin.set_range(0, 100)
        self.vol_spin.set_increments(5, 10)
        self.vol_spin.set_value(self.config.get("volume", 50))
        r.append(self.vol_spin)

        # No Auto Mute
        r = self.create_row("Disable Auto Mute", "Prevent automatic muting when other apps play sound.")
        box.append(r)
        self.noautomute_sw = Gtk.Switch()
        self.noautomute_sw.set_active(self.config.get("noautomute", False))
        self.noautomute_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.noautomute_sw)

        # No Audio Processing
        r = self.create_row("Disable Audio Processing", "Disable sound spectrum analysis (saves CPU).")
        box.append(r)
        self.noaudioproc_sw = Gtk.Switch()
        self.noaudioproc_sw.set_active(self.config.get("noAudioProcessing", False))
        self.noaudioproc_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.noaudioproc_sw)

    def build_advanced(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.stack.add_named(scroll, "advanced")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        scroll.set_child(box)

        t = Gtk.Label(label="Advanced")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        box.append(t)

        # Path
        r = self.create_row("Workshop Directory", "Path to Steam Workshop content (431960).")
        r.set_orientation(Gtk.Orientation.VERTICAL)
        box.append(r)
        
        workshop_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.path_entry = Gtk.Entry()
        self.path_entry.set_text(self.config.get("workshopPath") or WORKSHOP_PATH)
        self.path_entry.set_hexpand(True)
        workshop_box.append(self.path_entry)
        
        browse_workshop_btn = Gtk.Button(label="Browse")
        browse_workshop_btn.add_css_class("action-btn")
        browse_workshop_btn.add_css_class("secondary")
        browse_workshop_btn.connect("clicked", self.on_browse_workshop)
        workshop_box.append(browse_workshop_btn)
        r.append(workshop_box)

        # Assets Directory
        r = self.create_row("Assets Directory", "Wallpaper Engine assets folder (leave empty for auto-detect).")
        r.set_orientation(Gtk.Orientation.VERTICAL)
        box.append(r)
        
        assets_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.assets_entry = Gtk.Entry()
        assets_path = self.config.get("assetsPath", None)
        self.assets_entry.set_text(assets_path if assets_path else "")
        self.assets_entry.set_placeholder_text("Auto-detect from Steam installation")
        self.assets_entry.set_hexpand(True)
        assets_box.append(self.assets_entry)
        
        browse_assets_btn = Gtk.Button(label="Browse")
        browse_assets_btn.add_css_class("action-btn")
        browse_assets_btn.add_css_class("secondary")
        browse_assets_btn.connect("clicked", self.on_browse_assets)
        assets_box.append(browse_assets_btn)
        r.append(assets_box)

        # Screen
        r = self.create_row("Screen Root", "Select a monitor.")
        box.append(r)
        
        screens = self.screen_manager.get_screens()
        curr_screen = self.config.get("lastScreen") or self.screen_manager.get_primary_screen() or self.screen_manager.get_first_screen() or "eDP-1"
        if curr_screen not in screens:
            screens = screens + [curr_screen]
        
        self.screen_dd = Gtk.DropDown.new_from_strings(screens)
        self.screen_dd.set_hexpand(True)
        if curr_screen and curr_screen in screens:
            self.screen_dd.set_selected(screens.index(str(curr_screen)))
        r.append(self.screen_dd)

        btn = Gtk.Button()
        content = Adw.ButtonContent()
        content.set_icon_name("view-refresh-symbolic")
        content.set_label("Refresh Screens")
        btn.set_child(content)
        
        btn.add_css_class("action-btn")
        btn.add_css_class("secondary")
        btn.connect("clicked", self.on_refresh_screens)
        box.append(btn)

        # System Integration
        t = Gtk.Label(label="System Integration")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        t.set_margin_top(10)
        box.append(t)

        # Desktop Entry
        r = self.create_row("Desktop Shortcut", "Create app icon in system menu.")
        box.append(r)
        self.btn_create_desktop = Gtk.Button(label="Create")
        self.btn_create_desktop.set_valign(Gtk.Align.CENTER)
        self.btn_create_desktop.connect("clicked", self.on_create_desktop_entry)
        r.append(self.btn_create_desktop)

        # Autostart
        r = self.create_row("Run on Startup", "Launch automatically on login.")
        box.append(r)
        self.autostart_sw = Gtk.Switch()
        self.autostart_sw.set_active(self.integrator.is_autostart_enabled())
        self.autostart_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.autostart_sw)

        # Start Hidden
        r = self.create_row("Start Hidden", "Start in tray without showing window.")
        box.append(r)
        self.start_hidden_sw = Gtk.Switch()
        self.start_hidden_sw.set_active(True)
        self.start_hidden_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.start_hidden_sw)

        t_ss = Gtk.Label(label="Screenshot")
        t_ss.add_css_class("settings-section-title")
        t_ss.set_halign(Gtk.Align.START)
        t_ss.set_margin_top(10)
        box.append(t_ss)

        # Screenshot Delay
        r = self.create_row("Screenshot Delay", "Frames to wait before capture (use higher for web wallpapers).")
        box.append(r)
        self.screenshot_delay_spin = Gtk.SpinButton()
        self.screenshot_delay_spin.set_range(1, 600)
        self.screenshot_delay_spin.set_increments(5, 50)
        self.screenshot_delay_spin.set_value(self.config.get("screenshotDelay", 20))
        r.append(self.screenshot_delay_spin)

        # Screenshot Resolution
        r = self.create_row("Screenshot Resolution", "Target resolution (e.g. 1920x1080, 3840x2160).")
        box.append(r)
        self.screenshot_res_entry = Gtk.Entry()
        self.screenshot_res_entry.set_text(self.config.get("screenshotRes") or "3840x2160")
        self.screenshot_res_entry.set_hexpand(False)
        self.screenshot_res_entry.set_width_chars(15)
        r.append(self.screenshot_res_entry)

        # Xvfb Status Check
        import shutil
        has_xvfb = shutil.which("xvfb-run") is not None
        
        status_label = "✅ Xvfb Installed (Silent Mode)" if has_xvfb else "⚠️ Xvfb Not Found (Window Mode)"
        status_desc = "Silent capture using virtual framebuffer."
        
        r = self.create_row("Capture Backend", status_desc)
        box.append(r)
        
        status_val = Gtk.Label(label=status_label)
        status_val.add_css_class("status-value")
        if not has_xvfb:
            status_val.add_css_class("text-muted") 
        
        r.append(status_val)

        # Prefer Xvfb Switch
        r = self.create_row("Prefer Silent Capture", "Use Xvfb if installed to avoid popup windows.")
        box.append(r)
        self.xvfb_sw = Gtk.Switch()
        self.xvfb_sw.set_active(self.config.get("preferXvfb", True))
        self.xvfb_sw.set_valign(Gtk.Align.CENTER)
        if not has_xvfb:
            self.xvfb_sw.set_tooltip_text("Xvfb is not installed on this system.")
        r.append(self.xvfb_sw)

    def on_browse_workshop(self, btn):
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Workshop Directory")
        dialog.select_folder(self.get_root(), None, self._on_workshop_folder_selected)

    def _on_workshop_folder_selected(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                path = folder.get_path()
                self.path_entry.set_text(path)
        except GLib.Error:
            pass

    def on_browse_assets(self, btn):
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Assets Directory")
        dialog.select_folder(self.get_root(), None, self._on_assets_folder_selected)

    def _on_assets_folder_selected(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                path = folder.get_path()
                self.assets_entry.set_text(path)
        except GLib.Error:
            pass

    def on_create_desktop_entry(self, btn):
        success, msg = self.integrator.create_desktop_entry()
        if success:
            self.show_toast("Desktop entry created successfully")
        else:
            self.show_toast(f"Failed to create desktop entry: {msg}")

    def on_refresh_screens(self, btn):
        self.screen_manager.detect_screens()
        screens = self.screen_manager.get_screens()
        
        # Preserve selection if possible
        selected = self.screen_dd.get_selected_item()
        selected_str = selected.get_string() if selected else None
        
        self.screen_dd.set_model(Gtk.StringList.new(screens))
        
        if selected_str and selected_str in screens:
            self.screen_dd.set_selected(screens.index(selected_str))
        elif screens:
            self.screen_dd.set_selected(0)
            
        self.show_toast(f"Screens refreshed: {', '.join(screens)}")

    def build_logs(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        self.stack.add_named(box, "logs")

        # Header with Filter
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.append(header_box)

        t = Gtk.Label(label="Logs")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        t.set_hexpand(True)
        header_box.append(t)

        # Filter Dropdown
        filter_opts = ["All", "Controller", "Engine", "GUI"]
        self.filter_dd = Gtk.DropDown.new_from_strings(filter_opts)
        self.filter_dd.set_valign(Gtk.Align.CENTER)
        self.filter_dd.connect("notify::selected", self.on_filter_changed)
        header_box.append(self.filter_dd)

        # Log View
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        box.append(scroll)

        self.log_view = Gtk.TextView()
        self.log_view.set_editable(False)
        self.log_view.set_cursor_visible(False)
        self.log_view.set_monospace(True)
        self.log_view.set_left_margin(8)
        self.log_view.set_right_margin(8)
        scroll.set_child(self.log_view)

        self.log_buffer = self.log_view.get_buffer()
        self.setup_log_tags()

        # Buttons
        btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btns.set_halign(Gtk.Align.END)
        box.append(btns)

        clr_btn = Gtk.Button(label="Clear Logs")
        clr_btn.add_css_class("action-btn")
        clr_btn.add_css_class("secondary")
        clr_btn.connect("clicked", lambda _: self.clear_logs())
        btns.append(clr_btn)

        copy_btn = Gtk.Button(label="Copy Logs")
        copy_btn.add_css_class("action-btn")
        copy_btn.add_css_class("secondary")
        copy_btn.connect("clicked", self.copy_logs)
        btns.append(copy_btn)

        ref_btn = Gtk.Button(label="Refresh")
        ref_btn.add_css_class("action-btn")
        ref_btn.add_css_class("primary")
        ref_btn.connect("clicked", lambda _: self.refresh_logs())
        btns.append(ref_btn)

        self.log_manager.register_callback(self.on_log_update)
        self.refresh_logs()

    def on_filter_changed(self, dd, pspec):
        selected = dd.get_selected_item()
        if selected:
            self.current_filter = selected.get_string()
            self.refresh_logs()

    def setup_log_tags(self):
        tbl = self.log_buffer.get_tag_table()
        
        def add_tag(name, color):
            tag = Gtk.TextTag(name=name)
            tag.set_property("foreground", color)
            tag.set_property("size-points", 12)
            tbl.add(tag)

        add_tag("timestamp", "#6b7280")
        add_tag("debug", "#6b7280")
        add_tag("info", "#3b82f6")
        add_tag("warning", "#f59e0b")
        add_tag("error", "#ef4444")
        add_tag("source", "#a855f7")
        
        msg_tag = Gtk.TextTag(name="message")
        msg_tag.set_property("foreground", "#e5e7eb")
        msg_tag.set_property("size-points", 12)
        tbl.add(msg_tag)
        
        line_tag = Gtk.TextTag(name="line")
        line_tag.set_property("pixels-above-lines", 8)
        tbl.add(line_tag)

    def on_log_update(self, entry):
        GLib.idle_add(lambda: self.append_log(entry))

    def append_log(self, entry):
        ts = entry.get("timestamp", "")
        lvl = entry.get("level", "")
        src = entry.get("source", "")
        msg = entry.get("message", "")

        if self.current_filter != "All":
            if self.current_filter == "GUI":
                if src in ["Controller", "Engine"]:
                    return
            elif src != self.current_filter:
                return

        end = self.log_buffer.get_end_iter()
        
        self.log_buffer.insert_with_tags_by_name(end, f"[{ts}] ", "timestamp")
        
        lvl_tag = "debug"
        if lvl == "INFO": lvl_tag = "info"
        elif lvl == "WARNING": lvl_tag = "warning"
        elif lvl == "ERROR": lvl_tag = "error"
        
        self.log_buffer.insert_with_tags_by_name(end, f"[{lvl}] ", lvl_tag)
        self.log_buffer.insert_with_tags_by_name(end, f"[{src}] ", "source")
        self.log_buffer.insert_with_tags_by_name(end, f"{msg}\n", "message", "line")

        self.log_view.scroll_to_mark(
            self.log_buffer.create_mark("end", self.log_buffer.get_end_iter(), False),
            0.0, False, 0.0, 0.0
        )

    def refresh_logs(self):
        self.log_buffer.set_text("")
        for entry in self.log_manager.get_logs():
            self.append_log(entry)

    def clear_logs(self):
        self.log_manager.clear()
        self.log_buffer.set_text("")

    def copy_logs(self, btn):
        start = self.log_buffer.get_start_iter()
        end = self.log_buffer.get_end_iter()
        text = self.log_buffer.get_text(start, end, False)
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(text)
        
        orig = btn.get_label()
        btn.set_label("Copied!")
        GLib.timeout_add(2000, lambda: btn.set_label(orig) and False)

    def on_manage_nicknames(self, btn):
        try:
            from py_GUI.ui.components.nickname_manager_dialog import NicknameManagerDialog
            root = self.window
            
            if root:
                def on_nicknames_saved(needs_refresh=False):
                    app = Gio.Application.get_default()
                    if app and hasattr(app, 'wallpapers_page'):
                        if needs_refresh:
                            # 如果执行了删除并保存，调用全局刷新（相当于点击菜单栏的 Refresh Library）
                            app.refresh_from_cli()
                        else:
                            # 如果只是普通修改，仅更新 UI 即可，避免不必要的性能消耗
                            app.wallpapers_page.refresh_wallpaper_grid()
                            app.wallpapers_page.update_active_wallpaper_label()
                dialog = NicknameManagerDialog(root, self.nickname_manager, self.wp_manager, on_saved=on_nicknames_saved)
                dialog.present()
            else:
                print("[ERROR] Nickname Manager: Could not find parent window.")
        except Exception as e:
            print(f"[ERROR] Nickname Manager Error: {e}")
            import traceback
            traceback.print_exc()

    def on_save(self, btn):
        try:
            # General
            self.config.set("fps", int(self.fps_spin.get_value()))
            
            scaling_opts = ["default", "stretch", "fit", "fill"]
            idx = self.scaling_dd.get_selected()
            if 0 <= idx < len(scaling_opts):
                self.config.set("scaling", scaling_opts[idx])
                
            self.config.set("noFullscreenPause", self.pause_sw.get_active())
            self.config.set("disableMouse", self.mouse_sw.get_active())
            self.config.set("disableParallax", self.parallax_sw.get_active())
            self.config.set("disableParticles", self.particles_sw.get_active())
            
            clamp_opts = ["clamp", "border", "repeat"]
            idx = self.clamp_dd.get_selected()
            if 0 <= idx < len(clamp_opts):
                self.config.set("clamping", clamp_opts[idx])

            # Automation
            self.config.set("cycleEnabled", self.cycle_sw.get_active())
            self.config.set("cycleInterval", int(self.cycle_spin.get_value()))
            
            cycle_opts = ["random", "title", "size", "size_desc", "type", "id"]
            # Map UI index to config value
            # UI: ["Random", "Title", "Size ↑", "Size ↓", "Type", "ID"]
            sel_idx = self.cycle_order_dd.get_selected()
            if 0 <= sel_idx < len(cycle_opts):
                self.config.set("cycleOrder", cycle_opts[sel_idx])
            
            self.config.set("wayland_only_active", self.wl_active_sw.get_active())
            self.config.set("wayland_ignore_appids", self.wl_ignore_entry.get_text())

            # Audio
            self.config.set("silence", self.silence_sw.get_active())
            self.config.set("volume", int(self.vol_spin.get_value()))
            self.config.set("noautomute", self.noautomute_sw.get_active())
            self.config.set("noAudioProcessing", self.noaudioproc_sw.get_active())

            # Advanced
            self.config.set("workshopPath", self.path_entry.get_text())
            
            assets_path = self.assets_entry.get_text().strip()
            self.config.set("assetsPath", assets_path if assets_path else None)
            
            # Screen Root
            screens = self.screen_manager.get_screens()
            sel_idx = self.screen_dd.get_selected()
            # If screens list changed since build, this might be risky, but refresh updates model
            # Re-fetch model from dropdown?
            model = self.screen_dd.get_model()
            if model and 0 <= sel_idx < model.get_n_items():
                selected_screen = model.get_item(sel_idx).get_string()
                self.config.set("lastScreen", selected_screen)

            # Autostart
            self.integrator.set_autostart(
                self.autostart_sw.get_active(),
                hidden=self.start_hidden_sw.get_active()
            )

            # Screenshot
            self.config.set("screenshotDelay", int(self.screenshot_delay_spin.get_value()))
            self.config.set("screenshotRes", self.screenshot_res_entry.get_text())
            self.config.set("preferXvfb", self.xvfb_sw.get_active())

            new_path = self.config.get("workshopPath")
            if new_path and new_path != self.wp_manager.workshop_path:
                self.wp_manager.workshop_path = new_path
                self.wp_manager.manifest_path = self.wp_manager._find_manifest_path()
                self.wp_manager.scan()
            
            # Trigger cycle timer update if needed
            if self.on_cycle_settings_changed:
                self.on_cycle_settings_changed()

            self.show_toast("Settings saved successfully")
            
            # Restart if active to apply immediate changes (like FPS/Scaling)
            # Optional: Ask user? Or just do it.
            # self.controller.restart_wallpapers() 
            
        except Exception as e:
            self.show_toast(f"Error saving settings: {e}")
            print(f"Save error: {e}")

    def on_reload(self, btn):
        self.controller.restart_wallpapers()
        self.show_toast("Reloading wallpapers...")

```

---

### 📄 文件: `py_GUI/ui/pages/wallpapers.py`

```python
import random
import os
import signal
import time
from typing import Dict, Optional, Callable
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gdk, Gio, Pango, GLib

from py_GUI.ui.components.sidebar import Sidebar
from py_GUI.ui.components.dialogs import (
    show_delete_dialog,
    show_error_dialog,
    show_screenshot_success_dialog,
    show_nickname_dialog,
)
from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.config import ConfigManager
from py_GUI.core.logger import LogManager
from py_GUI.utils import markdown_to_pango, format_size

from py_GUI.core.screen import ScreenManager


class WallpapersPage(Gtk.Box):
    def __init__(
        self,
        window: Gtk.Window,
        config: ConfigManager,
        wp_manager: WallpaperManager,
        prop_manager: PropertiesManager,
        controller: WallpaperController,
        log_manager: LogManager,
        screen_manager: ScreenManager,
        nickname_manager,
        show_toast: Callable[[str], None] = None,
    ):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.window = window
        self.config = config
        self.wp_manager = wp_manager
        self.prop_manager = prop_manager
        self.controller = controller
        self.log_manager = log_manager
        self.nickname_manager = nickname_manager
        self.screen_manager = screen_manager
        self.show_toast = show_toast or (lambda msg: None)

        self.view_mode = "grid"
        self.search_query = ""
        self.sort_mode: str = self.config.get("sortMode", "title") or "title"
        self.sort_reverse: bool = bool(self.config.get("sortReverse", False))
        self.selected_wp: Optional[str] = None
        self.active_wp: Optional[str] = None  # Tracks running wallpaper

        # We need to track current screen selection
        self.selected_screen = self.config.get("lastScreen") or "eDP-1"
        self.apply_mode = self.config.get("apply_mode") or "diff"

        self._current_wp_ids = []

        # Cache for filtered wallpapers
        self._filtered_wallpapers: Optional[Dict] = None
        self._filter_cache_key: Optional[tuple] = None

        self.build_ui()
        self._setup_key_controller()

    def build_ui(self):
        # Toolbar
        self.build_toolbar()
        self.append(self.toolbar)

        # Content Box
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.content_box.set_vexpand(True)
        self.content_box.set_hexpand(True)
        self.append(self.content_box)

        # Left Area
        self.left_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.left_area.set_hexpand(True)
        self.content_box.append(self.left_area)

        # Status Panel
        self.build_status_panel(self.left_area)

        # Containers
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_halign(Gtk.Align.CENTER)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.set_row_spacing(5)
        self.flowbox.set_column_spacing(5)
        self.flowbox.set_margin_top(20)
        self.flowbox.set_margin_bottom(20)
        self.flowbox.set_margin_start(20)
        self.flowbox.set_margin_end(20)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.set_margin_top(20)
        self.listbox.set_margin_bottom(20)
        self.listbox.set_margin_start(20)
        self.listbox.set_margin_end(20)

        # Dual ScrolledWindow architecture for grid/list views
        self.grid_scroll = Gtk.ScrolledWindow()
        self.grid_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.grid_scroll.set_vexpand(True)
        self.grid_scroll.set_child(self.flowbox)

        self.list_scroll = Gtk.ScrolledWindow()
        self.list_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.list_scroll.set_vexpand(True)
        self.list_scroll.set_child(self.listbox)

        # Stack to manage view visibility
        self.view_stack = Gtk.Stack()
        self.view_stack.add_named(self.grid_scroll, "grid")
        self.view_stack.add_named(self.list_scroll, "list")
        self.left_area.append(self.view_stack)

        # Sidebar
        self.sidebar = Sidebar(
            self.wp_manager,
            self.prop_manager,
            self.controller,
            self.log_manager,
            self.nickname_manager,
        )

        screens = self.screen_manager.get_screens()
        self.sidebar.set_available_screens(screens)
        self.sidebar.set_current_screen_callback(lambda: self.selected_screen)
        self.sidebar.set_apply_mode_callback(
            lambda: getattr(self, "apply_mode", "diff")
        )
        self.sidebar.set_thumb_clicked_callback(self.select_wallpaper)
        self.sidebar.set_compact_callbacks(
            on_stop=self.on_stop_clicked,
            on_lucky=lambda: self.on_feeling_lucky(None),
            on_jump=lambda: self.on_currently_using_clicked(),
        )
        self.sidebar.btn_edit_nickname.connect(
            "clicked",
            lambda _: (
                self.on_edit_nickname(self.selected_wp) if self.selected_wp else None
            ),
        )

        self.content_box.append(self.sidebar)

    def build_toolbar(self):
        self.toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.toolbar.add_css_class("toolbar")

        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.toolbar.append(search_box)

        icon_search = Gtk.Image.new_from_icon_name("system-search-symbolic")
        icon_search.add_css_class("status-label")
        search_box.append(icon_search)

        self.search_entry = Gtk.Entry()
        self.search_entry.add_css_class("search-entry")
        self.search_entry.set_placeholder_text("Search wallpapers...")
        self.search_entry.set_width_chars(50)
        self.search_entry.connect("changed", self.on_search_changed)
        self.search_entry.connect("activate", self.on_search_activate)
        search_box.append(self.search_entry)

        sort_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.toolbar.append(sort_box)

        icon_sort = Gtk.Image.new_from_icon_name("view-sort-ascending-symbolic")
        icon_sort.add_css_class("status-label")
        sort_box.append(icon_sort)

        sort_options = ["Title", "Size ↓", "Size ↑", "Type", "ID"]
        self.sort_dd = Gtk.DropDown.new_from_strings(sort_options)

        initial_idx = 0
        if self.sort_mode == "size" and self.sort_reverse:
            initial_idx = 1
        elif self.sort_mode == "size":
            initial_idx = 2
        elif self.sort_mode == "type":
            initial_idx = 3
        elif self.sort_mode == "id":
            initial_idx = 4
        self.sort_dd.set_selected(initial_idx)

        self.sort_dd.connect("notify::selected", self.on_sort_changed)
        sort_box.append(self.sort_dd)

        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        self.toolbar.append(spacer)

        # Actions
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.toolbar.append(actions_box)

        stop_btn = Gtk.Button()
        stop_btn.set_icon_name("media-playback-stop-symbolic")
        stop_btn.add_css_class("flat")
        stop_btn.add_css_class("mode-btn")
        stop_btn.add_css_class("stop-btn")
        stop_btn.set_tooltip_text("Stop Wallpaper")
        stop_btn.connect("clicked", lambda _: self.on_stop_clicked())
        actions_box.append(stop_btn)

        lucky_btn = Gtk.Button()
        lucky_btn.set_icon_name("media-playlist-shuffle-symbolic")
        lucky_btn.add_css_class("flat")
        lucky_btn.add_css_class("mode-btn")
        lucky_btn.set_tooltip_text("I'm feeling lucky")
        lucky_btn.connect("clicked", self.on_feeling_lucky)
        actions_box.append(lucky_btn)

        self.btn_screenshot = Gtk.Button()
        self.btn_screenshot.add_css_class("flat")
        self.btn_screenshot.add_css_class("mode-btn")
        self.btn_screenshot.set_tooltip_text("Take Screenshot of current wallpaper")

        self.screenshot_stack = Gtk.Stack()
        self.screenshot_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)

        icon = Gtk.Image.new_from_icon_name("camera-photo-symbolic")
        self.screenshot_stack.add_named(icon, "icon")

        self.screenshot_spinner = Gtk.Spinner()
        self.screenshot_spinner.set_size_request(24, 24)
        self.screenshot_stack.add_named(self.screenshot_spinner, "spinner")

        self.screenshot_stack.set_visible_child_name("icon")
        self.btn_screenshot.set_child(self.screenshot_stack)

        self.btn_screenshot.connect("clicked", lambda _: self.on_screenshot_clicked())
        actions_box.append(self.btn_screenshot)

        # View Toggle
        view_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        view_box.set_margin_start(10)
        self.toolbar.append(view_box)

        self.btn_grid = Gtk.ToggleButton()
        self.btn_grid.set_icon_name("view-grid-symbolic")
        self.btn_grid.set_tooltip_text("Grid View")
        self.btn_grid.add_css_class("flat")
        self.btn_grid.add_css_class("mode-btn")
        self.btn_grid.set_active(True)
        self._grid_signal_id = self.btn_grid.connect("toggled", self.on_view_grid)
        view_box.append(self.btn_grid)

        self.btn_list = Gtk.ToggleButton()
        self.btn_list.set_icon_name("view-list-symbolic")
        self.btn_list.set_tooltip_text("List View")
        self.btn_list.add_css_class("flat")
        self.btn_list.add_css_class("mode-btn")
        self._list_signal_id = self.btn_list.connect("toggled", self.on_view_list)
        view_box.append(self.btn_list)

    def build_status_panel(self, parent: Gtk.Box):
        status_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        status_box.add_css_class("status-panel")
        status_box.set_margin_start(20)
        status_box.set_margin_end(10)
        status_box.set_margin_top(2)
        status_box.set_margin_bottom(2)

        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title_row.set_halign(Gtk.Align.FILL)

        left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title_row.append(left_box)

        title = Gtk.Label(label="CURRENTLY USING")
        title.add_css_class("status-label")
        title.set_halign(Gtk.Align.START)
        left_box.append(title)

        self.copy_cmd_btn = Gtk.Button()
        self.copy_cmd_btn.set_icon_name("edit-copy-symbolic")
        self.copy_cmd_btn.add_css_class("flat")
        self.copy_cmd_btn.set_tooltip_text("Copy command")
        self.copy_cmd_btn.connect("clicked", self.on_copy_command_clicked)
        left_box.append(self.copy_cmd_btn)

        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        title_row.append(spacer)

        self.jump_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.jump_box.set_halign(Gtk.Align.END)
        title_row.append(self.jump_box)

        self.entry_jump = Gtk.Entry()
        self.entry_jump.set_has_frame(False)
        self.entry_jump.set_width_chars(1)
        self.entry_jump.set_max_width_chars(4)
        self.entry_jump.set_alignment(1.0)
        self.entry_jump.add_css_class("status-value-yellow")
        self.entry_jump.set_tooltip_text("Type number and Enter to jump")
        self.entry_jump.connect("activate", self._on_jump_entry_activate)
        self.jump_box.append(self.entry_jump)

        self.lbl_jump_total = Gtk.Label(label="/0")
        self.lbl_jump_total.add_css_class("status-value-yellow")
        self.jump_box.append(self.lbl_jump_total)

        status_box.append(title_row)

        self.active_wp_label = Gtk.Label(label="-")
        self.active_wp_label.add_css_class("status-value")
        self.active_wp_label.set_use_markup(True)
        self.active_wp_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.active_wp_label.set_halign(Gtk.Align.START)
        try:
            self.active_wp_label.set_tooltip_text("Show current wallpaper details")
            self.active_wp_label.set_cursor_from_name("pointer")
        except Exception:
            pass
        click = Gtk.GestureClick.new()
        click.set_button(Gdk.BUTTON_PRIMARY)
        click.connect("released", lambda *_: self.on_currently_using_clicked())
        self.active_wp_label.add_controller(click)
        status_box.append(self.active_wp_label)

        parent.append(status_box)

    def update_active_wallpaper_label(self):
        active_monitors = self.config.get("active_monitors") or {}
        current_wp_id = active_monitors.get(self.selected_screen)

        if current_wp_id:
            wp = self.wp_manager._wallpapers.get(current_wp_id)
            if wp:
                display_name, _ = self.nickname_manager.get_display_name(wp)
                title = display_name
            else:
                title = current_wp_id
            self.active_wp_label.set_markup(markdown_to_pango(title))
        else:
            self.active_wp_label.set_label("None")

        cmd = self.controller.get_current_command()
        if cmd:
            escaped_cmd = GLib.markup_escape_text(cmd)
            self.copy_cmd_btn.set_tooltip_markup(
                f"<b><i>Click to copy:</i></b>\n<tt>{escaped_cmd}</tt>"
            )
            self.copy_cmd_btn.set_sensitive(True)
        else:
            self.copy_cmd_btn.set_tooltip_text("No command running")
            self.copy_cmd_btn.set_sensitive(False)

        self.update_counter_label()

    def update_counter_label(self):
        filtered = self.get_filtered_wallpapers()
        total = len(filtered)

        if total == 0:
            self.entry_jump.set_text("0")
            self.lbl_jump_total.set_label("/0")
            return

        active_monitors = self.config.get("active_monitors") or {}
        current_wp_id = active_monitors.get(self.selected_screen)

        self.lbl_jump_total.set_label(f"/{total}")

        if current_wp_id and current_wp_id in filtered:
            wp_index = list(filtered.keys()).index(current_wp_id) + 1
            self.entry_jump.set_text(str(wp_index))
        else:
            self.entry_jump.set_text("-")

    def _on_jump_entry_activate(self, entry):
        text = entry.get_text().strip()
        if not text:
            return

        try:
            self._jump_to_index(int(text))
        except ValueError:
            self.update_counter_label()

    def _jump_to_index(self, idx: int):
        filtered = self.get_filtered_wallpapers()
        total = len(filtered)
        if total == 0:
            return

        if idx < 1:
            idx = 1
        if idx > total:
            idx = total

        ids = list(filtered.keys())
        wp_id = ids[idx - 1]
        self.select_wallpaper(wp_id)

    def show_current_wallpaper_in_sidebar(self, force: bool = False):
        # Only auto-select if user hasn't selected another wallpaper, unless forced
        if not force and self.selected_wp is not None:
            return False
        active_monitors = self.config.get("active_monitors") or {}
        current_wp_id = active_monitors.get(self.selected_screen)
        if current_wp_id:
            # Highlight and show details
            self.select_wallpaper(current_wp_id)
            # Sidebar updates inside select_wallpaper
            return True
        return False

    def on_currently_using_clicked(self):
        if not self.show_current_wallpaper_in_sidebar(force=True):
            last_wp = self.config.get("lastWallpaper")
            if last_wp:
                self.select_wallpaper(last_wp)

    def on_copy_command_clicked(self, btn):
        cmd = self.controller.get_current_command()
        if not cmd:
            self.show_toast("No command to copy")
            return

        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(cmd)
        self.show_toast("📋 Command copied to clipboard")

    def on_view_grid(self, btn):
        # Only set toggle start time if an actual change will occur
        if not btn.get_active():
            # 用户点击已选中的按钮，阻止它变成未选中
            # 使用 handler_block 来防止递归触发
            signal_id = getattr(self, "_grid_signal_id", None)
            if signal_id:
                btn.handler_block(signal_id)
                btn.set_active(True)
                btn.handler_unblock(signal_id)
            else:
                btn.set_active(True)
            # Early return without setting toggle timer
            return
        self._toggle_start_time = time.perf_counter()

        # 正常切换到 Grid 视图
        # 阻止 list 按钮的信号，避免它的 toggled 处理器误认为是用户点击
        list_signal_id = getattr(self, "_list_signal_id", None)
        if list_signal_id:
            self.btn_list.handler_block(list_signal_id)
            self.btn_list.set_active(False)
            self.btn_list.handler_unblock(list_signal_id)
        else:
            self.btn_list.set_active(False)
        self.view_mode = "grid"
        self.refresh_wallpaper_grid()

    def on_view_list(self, btn):
        # Only set toggle start time if an actual change will occur
        if not btn.get_active():
            # 用户点击已选中的按钮，阻止它变成未选中
            # 使用 handler_block 来防止递归触发
            signal_id = getattr(self, "_list_signal_id", None)
            if signal_id:
                btn.handler_block(signal_id)
                btn.set_active(True)
                btn.handler_unblock(signal_id)
            else:
                btn.set_active(True)
            # Early return without setting toggle timer
            return
        self._toggle_start_time = time.perf_counter()
        # 正常切换到 List 视图
        # 阻止 grid 按钮的信号，避免它的 toggled 处理器误认为是用户点击
        grid_signal_id = getattr(self, "_grid_signal_id", None)
        if grid_signal_id:
            self.btn_grid.handler_block(grid_signal_id)
            self.btn_grid.set_active(False)
            self.btn_grid.handler_unblock(grid_signal_id)
        else:
            self.btn_grid.set_active(False)
        self.view_mode = "list"
        self.refresh_wallpaper_grid()

    def on_search_changed(self, entry):
        self.search_query = entry.get_text().lower().strip()
        self._invalidate_filter_cache()
        self.refresh_wallpaper_grid()
        self.update_sidebar_index()

    def on_search_activate(self, entry):
        self.search_query = entry.get_text().lower().strip()
        self._invalidate_filter_cache()
        self.refresh_wallpaper_grid()
        self.update_sidebar_index()

    def update_sidebar_index(self):
        filtered = self.get_filtered_wallpapers()
        if self.selected_wp and self.selected_wp in filtered:
            index = list(filtered.keys()).index(self.selected_wp) + 1
            total = len(filtered)
            self.sidebar.update(self.selected_wp, index, total)
        else:
            self.sidebar.update(self.selected_wp)

    def on_sort_changed(self, dd, pspec):
        idx = dd.get_selected()
        sort_map = {
            0: ("title", False),
            1: ("size", True),
            2: ("size", False),
            3: ("type", False),
            4: ("id", False),
        }
        self.sort_mode, self.sort_reverse = sort_map.get(idx, ("title", False))
        self.config.set("sortMode", self.sort_mode)
        self.config.set("sortReverse", self.sort_reverse)
        self._invalidate_filter_cache()
        self.refresh_wallpaper_grid()
        self.update_sidebar_index()

    def on_stop_clicked(self):
        # 统一上报给 App 层，由 App 层负责停止壁纸、清空记录并掐断轮播计时器
        app = self.window.get_application()
        if app and hasattr(app, "stop_wallpaper"):
            app.stop_wallpaper()
        else:
            # Fallback (以防万一)
            self.controller.stop_screen(self.selected_screen)
            self.update_active_wallpaper_label()

    def on_reload_wallpapers(self, btn):
        self.wp_manager.clear_cache()
        self.wp_manager.workshop_path = self.config.get(
            "workshopPath", self.wp_manager.workshop_path
        )
        self.wp_manager.scan()

        if self.wp_manager.last_scan_error:
            self.show_toast(f"⚠️ {self.wp_manager.last_scan_error}")
        elif self.wp_manager.scan_errors:
            self.show_toast(
                f"⚠️ {len(self.wp_manager.scan_errors)} wallpaper(s) failed to load"
            )

        self._invalidate_filter_cache()
        self.refresh_wallpaper_grid()

    def on_feeling_lucky(self, btn):
        if not self.wp_manager._wallpapers:
            return
        wp_id = random.choice(list(self.wp_manager._wallpapers.keys()))
        self.select_wallpaper(wp_id)
        self.apply_wallpaper(wp_id)

    def on_screenshot_clicked(self):
        active_monitors = self.config.get("active_monitors") or {}
        target_id = active_monitors.get(self.selected_screen)

        if not target_id:
            show_error_dialog(
                self.window,
                "Screenshot Error",
                f"No wallpaper is currently running on {self.selected_screen}.\n\nPlease apply a wallpaper to this screen first.",
            )
            return

        # UI Feedback: Busy state
        self.btn_screenshot.set_sensitive(False)
        self.screenshot_stack.set_visible_child_name("spinner")
        self.screenshot_spinner.start()
        self.btn_screenshot.set_tooltip_text("Capturing... please wait")

        def reset_ui():
            self.screenshot_spinner.stop()
            self.screenshot_stack.set_visible_child_name("icon")
            self.btn_screenshot.set_sensitive(True)
            self.btn_screenshot.set_tooltip_text("Take Screenshot of current wallpaper")

        base_dir = os.path.expanduser("~/Pictures/wallpaperengine")
        save_dir = base_dir
        fallback_used = False

        if not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir, exist_ok=True)
            except Exception as e:
                save_dir = "/tmp"
                fallback_used = True
                self.log_manager.add_error(
                    f"Failed to create {base_dir}: {e}. Falling back to /tmp", "GUI"
                )

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"Screenshot_{target_id}_{timestamp}.png"
        output_path = os.path.join(save_dir, filename)

        try:
            # Smart Delay Logic
            wp = self.wp_manager._wallpapers.get(target_id)
            wp_type = wp.get("type", "Unknown").lower() if wp else "unknown"

            user_delay = self.config.get("screenshotDelay", 20)
            user_delay = int(user_delay)

            if wp_type == "video":
                delay_frames = 5
                self.log_manager.add_info(
                    "Smart Delay: Video wallpaper detected, using fast capture (5 frames)",
                    "GUI",
                )
            else:
                delay_frames = user_delay
                # Web wallpapers might need more time, user setting is respected

            self.log_manager.add_info(f"Taking screenshot to {output_path}...", "GUI")
            proc, tracker = self.controller.take_screenshot(
                target_id, output_path, delay=delay_frames
            )

            start_time = time.time()

            # Calculate max wait time (timeout)
            # Xvfb software rendering is slow.
            import shutil

            has_xvfb_bin = shutil.which("xvfb-run") is not None
            prefer_xvfb = self.config.get("preferXvfb", True)
            is_xvfb = has_xvfb_bin and prefer_xvfb

            # Massive timeout for Xvfb software rendering at 4K
            fps_target = 1.0 if is_xvfb else 60.0
            buffer_s = 20.0 if is_xvfb else 3.0

            kill_threshold_s = (delay_frames / fps_target) + buffer_s
            self.log_manager.add_info(
                f"Screenshot timeout: {kill_threshold_s:.1f}s (Xvfb={is_xvfb})", "GUI"
            )

            last_size = -1
            stable_ticks = 0

            def check_capture_status():
                nonlocal last_size, stable_ticks
                elapsed = time.time() - start_time

                # Debug logging every 1s
                if int(elapsed * 10) % 10 == 0:
                    fsize = (
                        os.path.getsize(output_path)
                        if os.path.exists(output_path)
                        else -1
                    )
                    self.log_manager.add_debug(
                        f"Capture status: T={elapsed:.1f}s, File={fsize} bytes", "GUI"
                    )

                # 1. Check if process is already dead (crashed or finished)
                if proc.poll() is not None:
                    # Process exited on its own. Check file.
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        show_success()
                    else:
                        # Read error log
                        err_msg = "Unknown error"
                        try:
                            with open("/tmp/wallpaper_screenshot_error.log", "r") as f:
                                err_msg = f.read().strip()
                        except Exception:
                            pass

                        self.log_manager.add_error(
                            f"Screenshot process crashed: {err_msg}", "GUI"
                        )
                        reset_ui()
                        show_error_dialog(
                            self.window,
                            "Screenshot Failed",
                            f"The engine crashed or exited early.\n\nBackend Error:\n{err_msg[-500:]}",
                        )
                    return False

                # 2. Check if file exists and is stable
                if os.path.exists(output_path):
                    try:
                        curr_size = os.path.getsize(output_path)
                        if curr_size > 0:
                            if curr_size == last_size:
                                stable_ticks += 1
                            else:
                                stable_ticks = 0
                            last_size = curr_size

                            # Stable for ~200ms -> Kill it
                            if stable_ticks >= 2:
                                kill_process()
                                # Wait a tiny bit for cleanup then show success
                                GLib.timeout_add(200, show_success)
                                return False
                    except OSError:
                        pass  # File might be locked or busy

                # 3. Timeout -> Force Kill (Trigger save-on-exit)
                if elapsed > kill_threshold_s:
                    kill_process()
                    # Give it 1s to flush on exit
                    GLib.timeout_add(1000, verify_after_kill)
                    return False

                return True  # Continue polling

            def kill_process():
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGINT)
                except Exception:
                    proc.terminate()

            def show_success():
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    self.log_manager.add_info(
                        f"Screenshot complete: {output_path}", "GUI"
                    )

                    stats = self.controller.perf_monitor.stop_task(tracker)
                    self.controller.perf_monitor.add_screenshot_history(
                        target_id, output_path, stats
                    )
                    stats_str = f"Duration: {stats['duration']:.2f}s | Max CPU: {stats['max_cpu']:.1f}% | Max Mem: {stats['max_mem']:.1f} MB"

                    texture = None
                    wp = self.wp_manager._wallpapers.get(target_id)
                    if wp and wp.get("preview"):
                        texture = self.wp_manager.get_texture(wp["preview"], size=120)

                    reset_ui()
                    show_screenshot_success_dialog(
                        self.window, output_path, stats_str, texture
                    )
                else:
                    # Rare race condition or save failed
                    verify_after_kill()
                return False

            def verify_after_kill():
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    show_success()
                else:
                    reset_ui()
                    show_error_dialog(
                        self.window,
                        "Screenshot Timeout",
                        "Capture timed out. Try increasing the delay in Settings.",
                    )
                return False

            # Start polling every 100ms
            GLib.timeout_add(100, check_capture_status)

        except Exception as e:
            reset_ui()
            show_error_dialog(
                self.window, "Screenshot Error", f"Failed to start process: {e}"
            )

    def refresh_wallpaper_grid(self):
        prev_cache_key = getattr(self, "_filter_cache_key", None)
        prev_ids = getattr(self, "_current_wp_ids", None)

        filtered = self.get_filtered_wallpapers()

        recomputed = self._filter_cache_key != prev_cache_key
        ids_changed = prev_ids != self._current_wp_ids

        self.sidebar.set_wallpaper_ids(self._current_wp_ids)

        if self.view_mode == "grid":
            self.view_stack.set_visible_child_name("grid")
            # Populate if: (1) filter was recomputed (cache miss), OR (2) container is empty
            # maybe it is not right, i dont know 790-793 and it, which one is right
            if recomputed or ids_changed or self.flowbox.get_first_child() is None:
                self.populate_grid()
        else:
            self.view_stack.set_visible_child_name("list")
            # Populate grid if any of the following are true:
            # (1) Filter was recomputed (cache miss),
            # (2) Wallpaper IDs have changed (e.g., due to external updates),
            # (3) Container is currently empty.
            if recomputed or ids_changed or self.listbox.get_first_child() is None:
                self.populate_list()

        self.update_counter_label()

        if hasattr(self, "_toggle_start_time") and self._toggle_start_time:
            elapsed = (time.perf_counter() - self._toggle_start_time) * 1000
            try:
                if self.config.get("debug", False):
                    self.log_manager.add_info(f"View toggle time: {elapsed:.1f} ms")
            except Exception:
                pass
            self._toggle_start_time = None

    def _invalidate_filter_cache(self):
        self._filtered_wallpapers = None
        self._filter_cache_key = None

    def get_filtered_wallpapers(self) -> Dict[str, Dict]:
        cache_key = (self.search_query, self.sort_mode, self.sort_reverse)
        if self._filter_cache_key != cache_key or self._filtered_wallpapers is None:
            self._filtered_wallpapers = self.filter_wallpapers()
            self._filter_cache_key = cache_key
            self._current_wp_ids = list(self._filtered_wallpapers.keys())
        return self._filtered_wallpapers

    def filter_wallpapers(self) -> Dict[str, Dict]:
        # Avoid spamming logs in hot path; only log when debug enabled
        try:
            if self.config.get("debug", False):
                self.log_manager.add_debug("filter_wallpapers called", "GUI")
        except Exception:
            pass
        if not self.search_query:
            result = dict(self.wp_manager._wallpapers)
        else:
            result = {}
            for wp_id, wp in self.wp_manager._wallpapers.items():
                title = wp.get("title", "").lower()
                desc = wp.get("description", "").lower()
                tags = " ".join(str(t).lower() for t in wp.get("tags", []))
                nickname = (
                    (self.nickname_manager.get(wp_id) or "").lower()
                    if self.nickname_manager
                    else ""
                )
                if (
                    self.search_query in title
                    or self.search_query in desc
                    or self.search_query in tags
                    or self.search_query in wp_id.lower()
                    or self.search_query in nickname
                ):
                    result[wp_id] = wp

        if self.sort_mode == "title":
            sorted_items = sorted(
                result.items(),
                key=lambda x: x[1].get("title", "").lower(),
                reverse=self.sort_reverse,
            )
        elif self.sort_mode == "size":
            sorted_items = sorted(
                result.items(),
                key=lambda x: x[1].get("size", 0),
                reverse=self.sort_reverse,
            )
        elif self.sort_mode == "type":
            sorted_items = sorted(
                result.items(),
                key=lambda x: x[1].get("type", "").lower(),
                reverse=self.sort_reverse,
            )
        else:
            sorted_items = sorted(
                result.items(), key=lambda x: x[0], reverse=self.sort_reverse
            )

        return dict(sorted_items)

    def populate_grid(self):
        while True:
            child = self.flowbox.get_first_child()
            if child is None:
                break
            self.flowbox.remove(child)

        # Clean up old widget references to prevent memory leaks
        for wp in self.wp_manager._wallpapers.values():
            if "_grid_btn" in wp:
                del wp["_grid_btn"]

        filtered = self._filtered_wallpapers or {}
        for folder_id, wp in filtered.items():
            card = self.create_grid_item(folder_id, wp)
            self.flowbox.append(card)

    def populate_list(self):
        while True:
            child = self.listbox.get_first_child()
            if child is None:
                break
            self.listbox.remove(child)

        # Clean up old widget references to prevent memory leaks
        for wp in self.wp_manager._wallpapers.values():
            if "_list_btn" in wp:
                del wp["_list_btn"]

        filtered = self._filtered_wallpapers or {}
        total = len(filtered)
        for idx, (folder_id, wp) in enumerate(filtered.items()):
            row = self.create_list_item(folder_id, wp, idx + 1, total)
            self.listbox.append(row)

    def create_grid_item(self, folder_id: str, wp: Dict) -> Gtk.Widget:
        display_name, original_title = self.nickname_manager.get_display_name(wp)
        is_nickname = original_title is not None

        btn = Gtk.Button()
        btn.add_css_class("wallpaper-item")
        btn.add_css_class("wallpaper-card")
        btn.set_size_request(170, 170)
        btn.set_has_frame(False)

        tooltip_text = markdown_to_pango(display_name)
        if is_nickname:
            tooltip_text += f"\n<span size='small' alpha='70%'>Original: {markdown_to_pango(wp.get('title', ''))}</span>"
        btn.set_tooltip_markup(tooltip_text)

        btn.connect("clicked", lambda _: self.select_wallpaper(folder_id))

        gesture = Gtk.GestureClick.new()
        gesture.set_button(Gdk.BUTTON_PRIMARY)
        gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        gesture.connect(
            "pressed", lambda g, n, x, y: self.on_item_activated(folder_id, n)
        )
        btn.add_controller(gesture)

        context = Gtk.GestureClick.new()
        context.set_button(Gdk.BUTTON_SECONDARY)
        context.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        context.connect(
            "pressed", lambda g, n, x, y: self.on_context_menu(btn, folder_id, x, y)
        )
        btn.add_controller(context)

        overlay = Gtk.Overlay()
        btn.set_child(overlay)

        texture = self.wp_manager.get_texture(wp["preview"], 170)
        if texture:
            pic = Gtk.Picture.new_for_paintable(texture)
            pic.set_content_fit(Gtk.ContentFit.COVER)
            pic.set_size_request(170, 170)
            overlay.set_child(pic)
        else:
            placeholder = Gtk.Box()
            placeholder.set_size_request(170, 170)
            lbl = Gtk.Label(label=wp["title"][:1].upper())
            lbl.set_halign(Gtk.Align.CENTER)
            lbl.set_valign(Gtk.Align.CENTER)
            placeholder.append(lbl)
            overlay.set_child(placeholder)

        name_box = Gtk.Box()
        name_box.set_halign(Gtk.Align.CENTER)
        name_box.set_valign(Gtk.Align.END)
        name_box.set_margin_bottom(10)

        lbl = Gtk.Label()
        lbl.set_use_markup(True)
        lbl.set_markup(markdown_to_pango(display_name))
        lbl.add_css_class("wallpaper-name")
        if is_nickname:
            lbl.add_css_class("nickname-text")
        lbl.set_ellipsize(Pango.EllipsizeMode.END)
        lbl.set_max_width_chars(15)
        name_box.append(lbl)
        overlay.add_overlay(name_box)

        wp["_grid_btn"] = btn
        if folder_id == self.selected_wp:
            btn.add_css_class("selected")

        return btn

    def create_list_item(
        self, folder_id: str, wp: Dict, index: int, total: int
    ) -> Gtk.Widget:
        display_name, original_title = self.nickname_manager.get_display_name(wp)
        is_nickname = original_title is not None

        btn = Gtk.Button()
        btn.add_css_class("list-item")
        btn.set_has_frame(False)

        tooltip_text = markdown_to_pango(display_name)
        if is_nickname:
            tooltip_text += f"\n<span size='small' alpha='70%'>Original: {markdown_to_pango(wp.get('title', ''))}</span>"
        btn.set_tooltip_markup(tooltip_text)

        btn.connect("clicked", lambda _: self.select_wallpaper(folder_id))

        gesture = Gtk.GestureClick.new()
        gesture.set_button(Gdk.BUTTON_PRIMARY)
        gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        gesture.connect(
            "pressed", lambda g, n, x, y: self.on_item_activated(folder_id, n)
        )
        btn.add_controller(gesture)

        context = Gtk.GestureClick.new()
        context.set_button(Gdk.BUTTON_SECONDARY)
        context.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        context.connect(
            "pressed", lambda g, n, x, y: self.on_context_menu(btn, folder_id, x, y)
        )
        btn.add_controller(context)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        btn.set_child(hbox)

        texture = self.wp_manager.get_texture(wp["preview"], 100)
        if texture:
            pic = Gtk.Picture.new_for_paintable(texture)
            pic.set_content_fit(Gtk.ContentFit.COVER)
            pic.set_size_request(100, 100)
            pic.add_css_class("card")
            hbox.append(pic)

        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info.set_valign(Gtk.Align.CENTER)
        info.set_hexpand(True)
        hbox.append(info)

        t = Gtk.Label()
        t.set_use_markup(True)
        t.set_markup(markdown_to_pango(display_name))
        t.add_css_class("list-title")
        if is_nickname:
            t.add_css_class("nickname-text")
        t.set_halign(Gtk.Align.START)
        t.set_ellipsize(Pango.EllipsizeMode.END)
        info.append(t)

        if is_nickname:
            orig_lbl = Gtk.Label()
            orig_lbl.set_use_markup(True)
            orig_lbl.set_markup(
                f"<span size='small' alpha='60%'>{markdown_to_pango(wp.get('title', ''))}</span>"
            )
            orig_lbl.set_halign(Gtk.Align.START)
            orig_lbl.set_ellipsize(Pango.EllipsizeMode.END)
            info.append(orig_lbl)

        sz = format_size(wp.get("size", 0))
        size_lbl = Gtk.Label(label=sz)
        size_lbl.add_css_class("list-size")
        size_lbl.set_halign(Gtk.Align.START)
        info.append(size_lbl)

        typ = Gtk.Label(label=f"Type: {wp.get('type', 'Unknown')}")
        typ.add_css_class("list-type")
        typ.set_halign(Gtk.Align.START)
        info.append(typ)

        tags = wp.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        tgs = ", ".join(str(x) for x in tags[:5]) if tags else "None"
        tl = Gtk.Label(label=f"Tags: {tgs}")
        tl.add_css_class("list-tags")
        tl.set_halign(Gtk.Align.START)
        tl.set_ellipsize(Pango.EllipsizeMode.END)
        info.append(tl)

        idx_lbl = Gtk.Label(label=f"{index}/{total}")
        idx_lbl.add_css_class("list-index")
        idx_lbl.set_halign(Gtk.Align.START)
        info.append(idx_lbl)

        wp["_list_btn"] = btn
        if folder_id == self.selected_wp:
            btn.add_css_class("selected")

        return btn

    def select_wallpaper(self, folder_id: str):
        # Deselect old
        if self.selected_wp and self.selected_wp in self.wp_manager._wallpapers:
            old = self.wp_manager._wallpapers[self.selected_wp]
            if "_grid_btn" in old:
                old["_grid_btn"].remove_css_class("selected")
            if "_list_btn" in old:
                old["_list_btn"].remove_css_class("selected")

        self.selected_wp = folder_id
        wp = self.wp_manager._wallpapers.get(folder_id)
        if wp:
            if "_grid_btn" in wp:
                wp["_grid_btn"].add_css_class("selected")
            if "_list_btn" in wp:
                wp["_list_btn"].add_css_class("selected")

        filtered = getattr(self, "_filtered_wallpapers", None)
        if filtered is None:
            filtered = self.get_filtered_wallpapers()
        if folder_id in filtered:
            index = list(filtered.keys()).index(folder_id) + 1
            total = len(filtered)
            self.sidebar.update(folder_id, index, total)
        else:
            self.sidebar.update(folder_id)

        if self.sidebar._compact_mode:
            self.sidebar._update_thumb_grid()

    def apply_wallpaper(self, wp_id: str):
        self.controller.apply(wp_id, self.selected_screen)
        self.update_active_wallpaper_label()

    def on_item_activated(self, folder_id: str, n_press: int):
        if n_press == 2:
            self.select_wallpaper(folder_id)
            self.apply_wallpaper(folder_id)

    def on_context_menu(self, widget, folder_id, x, y):
        # Create a custom Popover with manual buttons to allow full styling control (e.g. Red delete button)
        popover = Gtk.Popover()
        popover.set_parent(widget)
        popover.set_has_arrow(False)

        # Position at click coordinates
        rect = Gdk.Rectangle()
        rect.x = int(x)
        rect.y = int(y)
        rect.width = 1
        rect.height = 1
        popover.set_pointing_to(rect)

        # Menu Container
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        box.set_margin_top(6)
        box.set_margin_bottom(6)
        box.set_margin_start(6)
        box.set_margin_end(6)
        popover.set_child(box)

        def create_menu_item(label, action_name, target_value=None, is_danger=False):
            btn = Gtk.Button()
            btn.set_has_frame(False)  # Flat button

            # Left aligned label
            lbl = Gtk.Label(label=label)
            lbl.set_halign(Gtk.Align.START)
            btn.set_child(lbl)

            # Action
            btn.set_action_name(action_name)
            if target_value:
                btn.set_action_target_value(GLib.Variant.new_string(target_value))

            # Styling
            # Ensure it spans full width
            btn.set_halign(Gtk.Align.FILL)

            if is_danger:
                btn.add_css_class("destructive-action")  # Makes it red in Libadwaita

            # Close popover when clicked
            btn.connect("clicked", lambda *_: popover.popdown())

            return btn

        # Menu Items
        box.append(create_menu_item("Apply Wallpaper", "win.apply", folder_id))
        box.append(create_menu_item("Stop Wallpaper", "win.stop"))
        box.append(create_menu_item("Open Folder", "win.open_folder", folder_id))

        # Separator
        box.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        btn_edit = Gtk.Button()
        btn_edit.set_has_frame(False)
        lbl_edit = Gtk.Label(label="Set Nickname")
        lbl_edit.set_halign(Gtk.Align.START)
        btn_edit.set_child(lbl_edit)
        btn_edit.set_halign(Gtk.Align.FILL)
        btn_edit.connect(
            "clicked", lambda _: (self.on_edit_nickname(folder_id), popover.popdown())
        )
        box.append(btn_edit)

        # Danger Item
        box.append(
            create_menu_item(
                "Delete Wallpaper", "win.delete", folder_id, is_danger=True
            )
        )

        popover.popup()

    def delete_wallpaper(self, wp_id: str):
        show_delete_dialog(self.window, wp_id, lambda: self._perform_delete(wp_id))

    def _perform_delete(self, wp_id: str):
        if self.wp_manager.delete_wallpaper(wp_id):
            if self.active_wp == wp_id:
                self.on_stop_clicked()
            self._invalidate_filter_cache()
            self.refresh_wallpaper_grid()
        else:
            show_error_dialog(self.window, "Error", "Failed to delete wallpaper")

    def open_wallpaper_folder(self, wp_id: str):
        import subprocess
        import shutil

        wp = self.wp_manager._wallpapers.get(wp_id)
        if wp:
            folder_path = os.path.dirname(wp["preview"])

            # List of file managers to try in order of preference
            file_managers = [
                "thunar",  # XFCE (Preferred)
                "nautilus",  # GNOME
                "dolphin",  # KDE
                "nemo",  # Cinnamon
                "pcmanfm",  # LXDE
                "pcmanfm-qt",  # LXQt
                "caja",  # MATE
                "index",  # Maui
                "files",  # Elementary
            ]

            # Try to find an installed file manager
            opened = False
            for fm in file_managers:
                if shutil.which(fm):
                    try:
                        subprocess.Popen([fm, folder_path])
                        opened = True
                        break
                    except Exception:
                        continue

            # Fallback to xdg-open if no specific FM found or failed
            if not opened:
                try:
                    subprocess.Popen(["xdg-open", folder_path])
                except Exception as e:
                    self.log_manager.add_error(f"Failed to open folder: {e}", "GUI")

    def on_edit_nickname(self, wp_id: str):
        wp = self.wp_manager._wallpapers.get(wp_id)
        if not wp:
            return

        title = wp.get("title", "")
        current_nickname = (
            self.nickname_manager.get(wp_id) if self.nickname_manager else None
        )
        preview_path = wp.get("preview")

        def on_confirm(new_nick: str):
            if self.nickname_manager:
                self.nickname_manager.set(wp_id, new_nick)
                self._invalidate_filter_cache()
                self.refresh_wallpaper_grid()
                self.update_sidebar_index()
                self.update_active_wallpaper_label()

        show_nickname_dialog(self.window, title, current_nickname, on_confirm)

    def set_compact_mode(self, enabled: bool):
        self.left_area.set_visible(not enabled)
        self.toolbar.set_visible(not enabled)
        self.content_box.set_hexpand(not enabled)
        self.sidebar.set_compact_mode(enabled)
        if enabled:
            self.sidebar.grab_focus()

    def _setup_key_controller(self):
        key_ctrl = Gtk.EventControllerKey.new()
        key_ctrl.connect("key-pressed", self._on_key_pressed)
        self.add_controller(key_ctrl)

    def _on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Left:
            self._navigate_wallpaper(-1)
            return True
        elif keyval == Gdk.KEY_Right:
            self._navigate_wallpaper(1)
            return True
        return False

    def _navigate_wallpaper(self, direction: int):
        if not self._current_wp_ids or not self.selected_wp:
            return
        try:
            current_idx = self._current_wp_ids.index(self.selected_wp)
            new_idx = current_idx + direction
            if 0 <= new_idx < len(self._current_wp_ids):
                new_wp_id = self._current_wp_ids[new_idx]
                self.select_wallpaper(new_wp_id)
        except ValueError:
            pass

```

---

### 📄 文件: `py_GUI/ui/tray.py`

```python
import subprocess
import os
import time


def log_main(msg):
    if os.getenv("LWG_DEBUG") != "1":
        return

    try:
        log_dir = os.path.expanduser("~/.cache/linux-wallpaperengine-gui")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "tray_crash.log")
        
        if os.path.exists(log_path):
            try:
                if os.path.getsize(log_path) > 512 * 1024:
                    rotated = log_path + ".1"
                    if os.path.exists(rotated): os.remove(rotated)
                    os.replace(log_path, rotated)
            except OSError:
                pass
        
        with open(log_path, "a") as f:
            ts = time.strftime("%H:%M:%S")
            f.write(f"[{ts}] [MAIN] {msg}\n")
    except Exception:
        pass

class TrayIcon:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TrayIcon, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self, app):
        self.app = app
        if not self.initialized:
            self.process = None  # ✨ 干净利落，直接绑定在单例对象上
            log_main("TrayIcon Initialized")
            self.initialized = True

    # @property
    # def process(self): ...
    # @process.setter
    # def process(self, value): ...
    
    def _install_tray_icons(self):
        """核心黑魔法：将托盘图标释放到用户本地目录，彻底绕开 AppImage 的 FUSE 权限阻拦"""
        import shutil
        import os
        try:
            # 找到源码/AppDir内部的源图标
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            src_normal = os.path.join(base_dir, "pic", "icons", "gui_tray_rounded.png")
            src_stopped = os.path.join(base_dir, "pic", "icons", "gui_tray_rounded-stopped.png")
            
            # 目标本地 XDG 标准目录 (安全区)
            local_icon_dir = os.path.expanduser("~/.local/share/icons/hicolor/512x512/apps")
            os.makedirs(local_icon_dir, exist_ok=True)
            
            target_normal = os.path.join(local_icon_dir, "com.wallpaperengine.tray.png")
            target_stopped = os.path.join(local_icon_dir, "com.wallpaperengine.tray-stopped.png")
            
            # 如果源文件存在，且本地不存在或源文件较新，则进行覆盖拷贝
            for src, target in [(src_normal, target_normal), (src_stopped, target_stopped)]:
                if os.path.exists(src):
                    if not os.path.exists(target) or os.path.getmtime(src) > os.path.getmtime(target):
                        shutil.copy2(src, target)

            # ✨ 核心修复：返回这个位于安全区的【绝对路径】！
            # 仅在目标图标实际存在时返回路径，否则返回 None 以触发上层兜底逻辑
            if os.path.exists(target_normal):
                return target_normal
            return None
        except Exception as e:
            log_main(f"Failed to install local tray icons: {e}")
            return None

    def _resolve_icon(self):
        # 1. 释放到本地，拿回安全的绝对路径
        safe_path = self._install_tray_icons()
        
        # 2. 如果成功，直接把绝对路径扔给 Rust！
        # 桌面环境拿到绝对路径后，既不需要刷新缓存，又不会被 AppImage 拦截！
        if safe_path and os.path.exists(safe_path):
            return safe_path
            
        # 兜底
        return "com.wallpaperengine.tray"

    def start(self):
        if self.process is not None:
            if self.process.poll() is None:
                log_main(f"Tray (PID: {self.process.pid}) is alive. Skipping.")
                return
            else:
                self.process = None

        log_main("Initiating Tray Start Sequence...")
        import shutil

        # 定义统一的 Socket 路径
        socket_name = f"lwg-ipc-{os.getuid()}"
        
        # 获取各环境可能的路径
        appimage_tray_path = os.getenv('LWG_TRAY_BIN')
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        dev_path = os.path.join(base, 'tray_rs', 'target', 'release', 'tray-rs')

        rust_tray_path = None

        # 1. 最高优先级：AppImage/生产环境变量提供的路径
        if appimage_tray_path and os.path.exists(appimage_tray_path):
            rust_tray_path = appimage_tray_path
            os.environ.setdefault('LWG_IPC_SOCKET', socket_name)
            log_main(f"Using AppImage/env Rust tray: {rust_tray_path}")
            
        # 2. 次优级：本地源码编译出的开发版路径
        elif os.path.exists(dev_path):
            rust_tray_path = dev_path
            os.environ['LWG_IPC_SOCKET'] = socket_name
            log_main(f"Using dev Rust tray: {rust_tray_path}")
            
        # 3. 兜底策略：从系统 PATH 环境变量寻找
        else:
            rust_tray_path = shutil.which('tray-rs-bin')
            if rust_tray_path:
                os.environ.setdefault('LWG_IPC_SOCKET', socket_name)
                log_main(f"Using fallback system Rust tray: {rust_tray_path}")

        # 最终安全检查
        if not rust_tray_path or not os.path.exists(rust_tray_path):
            log_main("CRITICAL: tray-rs-bin missing.")
            return

        cmd = [rust_tray_path, self._resolve_icon(), str(os.getpid())]
        
        try:
            proc = subprocess.Popen(
                cmd, 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                start_new_session=True 
            )
            self.process = proc
            log_main(f"Rust Tray Spawned Successfully. PID: {proc.pid}")
        except Exception as e:
            log_main(f"Spawn Error: {e}")

    def stop(self):
        if self.process:
            log_main(f"Terminating tray (PID: {self.process.pid}) on app quit.")
            try:
                self.process.terminate()  # 温柔地发送 SIGTERM，让 Rust 有充足时间留下遗言
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
            except Exception:
                pass
            self.process = None

    def update_tooltip(self, text: str, retries: int = 3):
        """向 Rust 托盘发送提示文本，使用 Abstract Sockets"""
        try:
            import socket
            sock_name = f"lwg-tray-rx-{os.getuid()}"
            abstract_addr = f"\x00{sock_name}" # ✨ 拼接 \x00

            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                try:
                    # 尝试直接连接抽象套接字
                    s.connect(abstract_addr)
                    s.sendall((text + "\n").encode('utf-8'))
                except (ConnectionRefusedError, FileNotFoundError, socket.error):
                    # 如果被拒绝（Rust 还没准备好），则进行重试
                    if retries > 0:
                        import threading
                        import time
                        def _retry():
                            time.sleep(1)
                            self.update_tooltip(text, retries - 1)
                        threading.Thread(target=_retry, daemon=True).start()
                    else:
                        log_main("Tooltip update failed: RX Socket missing after max retries.")
        except Exception as e:
            log_main(f"Tooltip update failed: {e}")
```

---

### 📄 文件: `py_GUI/ui/tray_process.py`

```python
#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, AyatanaAppIndicator3, GLib
import subprocess
import signal
import sys
import os
import time

def log_crash(msg):
    try:
        import os, time
        log_dir = os.path.expanduser("~/.cache/linux-wallpaperengine-gui")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "tray_crash.log")
        with open(log_path, "a") as f:
            ts = time.strftime("%H:%M:%S")
            f.write(f"[{ts}] [TRAY] {msg}\n")
    except Exception:
        pass

class TrayProcess:
    def __init__(self, icon_path, parent_pid):
        self.icon_path = icon_path
        self.parent_pid = int(parent_pid) if parent_pid.isdigit() else None
        self.run_gui_path = self._find_run_gui()
        self.is_engine_running = False
        
        self.app_id = "com.wallpaperengine.gui"
        
        self.indicator = AyatanaAppIndicator3.Indicator.new(
            self.app_id,
            "preferences-desktop-wallpaper",
            AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        
        try: self.indicator.set_title("Wallpaper Engine GUI")
        except Exception: pass
        
        if self.icon_path and self.icon_path.startswith("/"):
            self.indicator.set_icon_full(self.icon_path, "Wallpaper Engine")
        else:
            self.indicator.set_icon_full(self.icon_path if self.icon_path else self.app_id, "Wallpaper Engine")
            
        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self._build_menu())

        import signal
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        
        GLib.timeout_add_seconds(2, self._poll_state)
        # Claude 提供的神级探针
        GLib.timeout_add_seconds(3, self._verify_registration)

    def _verify_registration(self):
        try:
            import subprocess
            result = subprocess.run(
                ["dbus-send", "--session", "--print-reply",
                 "--dest=org.freedesktop.DBus",
                 "/org/freedesktop/DBus",
                 "org.freedesktop.DBus.ListNames"],
                capture_output=True, text=True, timeout=3
            )
            if self.app_id in result.stdout or "StatusNotifier" in result.stdout:
                log_crash("DBus Verification: OK (Tray successfully registered to DBus)")
            else:
                log_crash("DBus Verification: FAILED (Tray is NOT in DBus names!)")
        except Exception as e:
            log_crash(f"DBus Verification Error: {e}")
        return False

    def _find_run_gui(self):
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        rel_path = os.path.join(base, 'run_gui.py')
        if os.path.exists(rel_path):
            return rel_path
        return "run_gui.py"

    def _poll_state(self):
        if self.parent_pid:
            try:
                os.kill(self.parent_pid, 0)
            except OSError:
                log_crash(f"Parent PID {self.parent_pid} died. Exiting.")
                Gtk.main_quit()
                return False

        running = False
        try:
            pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
            for pid in pids:
                try:
                    with open(os.path.join('/proc', pid, 'cmdline'), 'rb') as f:
                        cmdline = f.read().decode('utf-8', errors='ignore').replace('\0', ' ')
                        if 'linux-wallpaperengine' in cmdline and 'python' not in cmdline:
                            running = True
                            break
                except Exception: continue
        except Exception: pass
        
        self.is_engine_running = running
        return True

    def _build_menu(self):
        menu = Gtk.Menu()
        
        item_show = Gtk.MenuItem()
        label = Gtk.Label(label="<b>Show Window</b>")
        label.set_use_markup(True)
        item_show.add(label)
        item_show.connect("activate", lambda _: self._safe_cmd("--show"))
        menu.append(item_show)
        try: self.indicator.set_secondary_activate_target(item_show)
        except Exception: pass
            
        menu.append(Gtk.SeparatorMenuItem())
        
        item_toggle = Gtk.MenuItem(label="Play/Stop")
        item_toggle.connect("activate", self._on_toggle_click)
        menu.append(item_toggle)
        
        item_random = Gtk.MenuItem(label="Random Wallpaper")
        item_random.connect("activate", lambda _: self._safe_cmd("--random"))
        menu.append(item_random)
        
        menu.append(Gtk.SeparatorMenuItem())
        
        item_quit = Gtk.MenuItem(label="Quit Application")
        item_quit.connect("activate", lambda _: self._safe_cmd("--quit"))
        menu.append(item_quit)
        
        menu.show_all()
        return menu

    def _on_toggle_click(self, widget):
        if self.is_engine_running:
            self._safe_cmd("--stop")
        else:
            self._safe_cmd("--apply-last")

    def _safe_cmd(self, arg):
        GLib.timeout_add(100, self._exec_cmd, arg)

    def _exec_cmd(self, arg):
        try:
            cmd = ["python3", self.run_gui_path, arg]
            
            appdir = os.getenv('APPDIR')
            if appdir:
                launcher = os.path.join(appdir, "AppRun")
                if os.path.exists(launcher):
                    cmd = [launcher, arg]
            
            clean_env = os.environ.copy()
            clean_env.pop("DESKTOP_STARTUP_ID", None)
            clean_env.pop("GIO_LAUNCHED_DESKTOP_FILE", None)
            
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=clean_env
            )
        except Exception as e:
            log_crash(f"Cmd Error: {e}")
        return False

    def run(self):
        Gtk.main()

if __name__ == "__main__":
    try:
        icon = sys.argv[1] if len(sys.argv) > 1 else ""
        pid = sys.argv[2] if len(sys.argv) > 2 else "0"
        
        app = TrayProcess(icon, pid)
        app.run()
    except Exception as e:
        log_crash(f"Startup: {e}")
```

---

### 📄 文件: `py_GUI/utils.py`

```python
import os
import re
from gi.repository import GLib


def format_size(size_bytes: int) -> str:
    """
    Format bytes to human-readable size (KB, MB, GB).
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def get_folder_size(folder_path: str) -> int:
    """
    Calculate total size of a folder in bytes.
    """
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    pass
    except (OSError, PermissionError):
        pass
    return total_size

def markdown_to_pango(text: str) -> str:
    """
    Convert basic Markdown (*, **, ***) to Pango Markup (<i>, <b>, <b><i>).
    Handles XML escaping first.
    """
    if not text:
        return ""
        
    # 1. Escape XML characters first
    escaped = GLib.markup_escape_text(text)
    
    # 2. Bold+Italic ***text***
    escaped = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', escaped)
    
    # 3. Bold **text**
    escaped = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', escaped)
    
    # 4. Italic *text*
    escaped = re.sub(r'\*(.+?)\*', r'<i>\1</i>', escaped)
    
    return escaped

def bbcode_to_pango(text: str) -> str:
    """
    Convert Wallpaper Engine BBCode to Pango Markup.
    Strips images and handles basic formatting.
    """
    if not text:
        return ""

    # 1. Strip [img] tags entirely
    text = re.sub(r'\[img\].*?\[/img\]', '', text, flags=re.IGNORECASE)
    
    # 2. Handle [url=...]text[/url] -> text
    text = re.sub(r'\[url=.*?\](.*?)\[/url\]', r'\1', text, flags=re.IGNORECASE)
    
    # 3. Escape for Pango
    escaped = GLib.markup_escape_text(text)
    
    # 4. Basic formatting
    escaped = re.sub(r'\[b\](.*?)\[/b\]', r'<b>\1</b>', escaped, flags=re.IGNORECASE)
    escaped = re.sub(r'\[i\](.*?)\[/i\]', r'<i>\1</i>', escaped, flags=re.IGNORECASE)
    escaped = re.sub(r'\[h1\](.*?)\[/h1\]', r'<span size="large" weight="bold">\1</span>', escaped, flags=re.IGNORECASE)
    
    # 5. Clean up excessive whitespace/newlines
    escaped = escaped.replace('\r\n', '\n')
    lines = [line.strip() for line in escaped.split('\n')]
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        if line:
            cleaned_lines.append(line)
            prev_empty = False
        elif not prev_empty:
            cleaned_lines.append(line)
            prev_empty = True
            
    return '\n'.join(cleaned_lines).strip()

```

---

### 📄 文件: `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "linux-wallpaperengine-gui"
# 【关键】：必须保持这种格式，让 build_appimage.sh 能 grep 到
version = "1.0.0-pre"
description = "A modern GTK4 GUI for managing dynamic wallpapers from Steam Workshop on Linux"
readme = "README.md"
authors = [
    { name = "Suhoiyis" }
]
license = { text = "GPL-3.0-or-later" }
requires-python = ">=3.10"
dependencies = [
    "PyGObject",
    "Pillow"
]

[project.urls]
Homepage = "https://github.com/Suhoiyis/gui-for-linux-wallpaperengine"
Issues = "https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues"

# 【终极修复】显式声明非标准目录结构，防止未来别人打包时丢弃 pic 资源
[tool.setuptools]
py-modules = ["run_gui"]

[tool.setuptools.packages.find]
where = ["."]
include = ["py_GUI*"]

[tool.setuptools.package-data]
"*" = ["pic/**/*", "py_GUI/**/*.json", "py_GUI/**/*.css"]
```

---

### 📄 文件: `run_gui.py`

```python
#!/usr/bin/env python3
import sys
import os

# Ensure the current directory is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from py_GUI.main import main

if __name__ == '__main__':
    main()

```

---

### 📄 文件: `tray_rs/Cargo.lock`

```toml
# This file is automatically @generated by Cargo.
# It is not intended for manual editing.
version = 4

[[package]]
name = "ansi_term"
version = "0.12.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "d52a9bb7ec0cf484c551830a7ce27bd20d67eac647e1befb56b0be4ee39a55d2"
dependencies = [
 "winapi",
]

[[package]]
name = "atty"
version = "0.2.14"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "d9b39be18770d11421cdb1b9947a45dd3f37e93092cbf377614828a319d5fee8"
dependencies = [
 "hermit-abi",
 "libc",
 "winapi",
]

[[package]]
name = "bitflags"
version = "1.3.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "bef38d45163c2f1dde094a7dfd33ccf595c92905c8f8f4fdc18d06fb1037718a"

[[package]]
name = "clap"
version = "2.34.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "a0610544180c38b88101fecf2dd634b174a62eef6946f84dfc6a7127512b381c"
dependencies = [
 "ansi_term",
 "atty",
 "bitflags",
 "strsim",
 "textwrap",
 "unicode-width",
 "vec_map",
]

[[package]]
name = "dbus"
version = "0.9.10"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "21b3aa68d7e7abee336255bd7248ea965cc393f3e70411135a6f6a4b651345d4"
dependencies = [
 "libc",
 "libdbus-sys",
 "windows-sys",
]

[[package]]
name = "dbus-codegen"
version = "0.9.1"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "a49da9fdfbe872d4841d56605dc42efa5e6ca3291299b87f44e1cde91a28617c"
dependencies = [
 "clap",
 "dbus",
 "xml-rs",
]

[[package]]
name = "dbus-tree"
version = "0.9.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "f456e698ae8e54575e19ddb1f9b7bce2298568524f215496b248eb9498b4f508"
dependencies = [
 "dbus",
]

[[package]]
name = "hermit-abi"
version = "0.1.19"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "62b467343b94ba476dcb2500d242dadbb39557df889310ac77c5d99100aaac33"
dependencies = [
 "libc",
]

[[package]]
name = "ksni"
version = "0.2.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "4934310bdd016e55725482b8d35ac0c16fd058c1b955d8959aa2d953b918c85b"
dependencies = [
 "dbus",
 "dbus-codegen",
 "dbus-tree",
 "thiserror",
]

[[package]]
name = "libc"
version = "0.2.182"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "6800badb6cb2082ffd7b6a67e6125bb39f18782f793520caee8cb8846be06112"

[[package]]
name = "libdbus-sys"
version = "0.2.7"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "328c4789d42200f1eeec05bd86c9c13c7f091d2ba9a6ea35acdf51f31bc0f043"
dependencies = [
 "pkg-config",
]

[[package]]
name = "pkg-config"
version = "0.3.32"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "7edddbd0b52d732b21ad9a5fab5c704c14cd949e5e9a1ec5929a24fded1b904c"

[[package]]
name = "proc-macro2"
version = "1.0.106"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "8fd00f0bb2e90d81d1044c2b32617f68fcb9fa3bb7640c23e9c748e53fb30934"
dependencies = [
 "unicode-ident",
]

[[package]]
name = "quote"
version = "1.0.44"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "21b2ebcf727b7760c461f091f9f0f539b77b8e87f2fd88131e7f1b433b3cece4"
dependencies = [
 "proc-macro2",
]

[[package]]
name = "strsim"
version = "0.8.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "8ea5119cdb4c55b55d432abb513a0429384878c15dde60cc77b1c99de1a95a6a"

[[package]]
name = "syn"
version = "2.0.117"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "e665b8803e7b1d2a727f4023456bbbbe74da67099c585258af0ad9c5013b9b99"
dependencies = [
 "proc-macro2",
 "quote",
 "unicode-ident",
]

[[package]]
name = "textwrap"
version = "0.11.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "d326610f408c7a4eb6f51c37c330e496b08506c9457c9d34287ecc38809fb060"
dependencies = [
 "unicode-width",
]

[[package]]
name = "thiserror"
version = "1.0.69"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "b6aaf5339b578ea85b50e080feb250a3e8ae8cfcdff9a461c9ec2904bc923f52"
dependencies = [
 "thiserror-impl",
]

[[package]]
name = "thiserror-impl"
version = "1.0.69"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "4fee6c4efc90059e10f81e6d42c60a18f76588c3d74cb83a0b242a2b6c7504c1"
dependencies = [
 "proc-macro2",
 "quote",
 "syn",
]

[[package]]
name = "tray-rs"
version = "1.0.0"
dependencies = [
 "ksni",
 "libc",
]

[[package]]
name = "unicode-ident"
version = "1.0.24"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "e6e4313cd5fcd3dad5cafa179702e2b244f760991f45397d14d4ebf38247da75"

[[package]]
name = "unicode-width"
version = "0.1.14"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "7dd6e30e90baa6f72411720665d41d89b9a3d039dc45b8faea1ddd07f617f6af"

[[package]]
name = "vec_map"
version = "0.8.2"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "f1bddf1187be692e79c5ffeab891132dfb0f236ed36a43c7ed39f1165ee20191"

[[package]]
name = "winapi"
version = "0.3.9"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "5c839a674fcd7a98952e593242ea400abe93992746761e38641405d28b00f419"
dependencies = [
 "winapi-i686-pc-windows-gnu",
 "winapi-x86_64-pc-windows-gnu",
]

[[package]]
name = "winapi-i686-pc-windows-gnu"
version = "0.4.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "ac3b87c63620426dd9b991e5ce0329eff545bccbbb34f3be09ff6fb6ab51b7b6"

[[package]]
name = "winapi-x86_64-pc-windows-gnu"
version = "0.4.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "712e227841d057c1ee1cd2fb22fa7e5a5461ae8e48fa2ca79ec42cfc1931183f"

[[package]]
name = "windows-sys"
version = "0.59.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "1e38bc4d79ed67fd075bcc251a1c39b32a1776bbe92e5bef1f0bf1f8c531853b"
dependencies = [
 "windows-targets",
]

[[package]]
name = "windows-targets"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "9b724f72796e036ab90c1021d4780d4d3d648aca59e491e6b98e725b84e99973"
dependencies = [
 "windows_aarch64_gnullvm",
 "windows_aarch64_msvc",
 "windows_i686_gnu",
 "windows_i686_gnullvm",
 "windows_i686_msvc",
 "windows_x86_64_gnu",
 "windows_x86_64_gnullvm",
 "windows_x86_64_msvc",
]

[[package]]
name = "windows_aarch64_gnullvm"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "32a4622180e7a0ec044bb555404c800bc9fd9ec262ec147edd5989ccd0c02cd3"

[[package]]
name = "windows_aarch64_msvc"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "09ec2a7bb152e2252b53fa7803150007879548bc709c039df7627cabbd05d469"

[[package]]
name = "windows_i686_gnu"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "8e9b5ad5ab802e97eb8e295ac6720e509ee4c243f69d781394014ebfe8bbfa0b"

[[package]]
name = "windows_i686_gnullvm"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "0eee52d38c090b3caa76c563b86c3a4bd71ef1a819287c19d586d7334ae8ed66"

[[package]]
name = "windows_i686_msvc"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "240948bc05c5e7c6dabba28bf89d89ffce3e303022809e73deaefe4f6ec56c66"

[[package]]
name = "windows_x86_64_gnu"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "147a5c80aabfbf0c7d901cb5895d1de30ef2907eb21fbbab29ca94c5b08b1a78"

[[package]]
name = "windows_x86_64_gnullvm"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "24d5b23dc417412679681396f2b49f3de8c1473deb516bd34410872eff51ed0d"

[[package]]
name = "windows_x86_64_msvc"
version = "0.52.6"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "589f6da84c646204747d1270a2a5661ea66ed1cced2631d546fdfb155959f9ec"

[[package]]
name = "xml-rs"
version = "0.8.28"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "3ae8337f8a065cfc972643663ea4279e04e7256de865aa66fe25cec5fb912d3f"

```

---

### 📄 文件: `tray_rs/Cargo.toml`

```toml
[package]
name = "tray-rs"
version = "1.0.0"    # 完美对齐你的主项目版本！
edition = "2021"      # 锁定 2021 语法世代，确保绝对的兼容性和稳定性

[dependencies]
# 纯 Rust 的托盘库，直接走 DBus，彻底抛弃 C 语言和 GTK3 依赖！
ksni = "0.2" 
libc = "0.2"  # ✅ 新增：用于捕获 SIGTERM 信号
# 极其高效的跨平台系统进程扫描库
# sysinfo = "0.30"
# 用于简化错误处理
# anyhow = "1.0"

[profile.release]
opt-level = "z"       # 最小化体积优化
lto = true            # 开启链接时优化 (Link Time Optimization)
codegen-units = 1     # 单线程死磕，追求极致的体积压缩
strip = true          # 剔除所有的调试符号，给二进制文件“疯狂瘦身”
```

---

### 📄 文件: `tray_rs/src/main.rs`

```rust
use ksni::{menu::*, Icon, Tray, TrayService, ToolTip};
use std::env;
use std::fs;
use std::path::Path;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;
use std::time::Duration;
use std::os::unix::net::UnixListener;
use std::io::{Write, BufRead, BufReader};

use std::os::linux::net::SocketAddrExt;
use std::os::unix::net::SocketAddr;

static SHOULD_EXIT: AtomicBool = AtomicBool::new(false);

extern "C" fn handle_sigterm(_: libc::c_int) {
    SHOULD_EXIT.store(true, Ordering::Relaxed);
}

fn get_uid() -> u32 { unsafe { libc::getuid() } }

struct WallpaperTray {
    icon_path: String,
    socket_path: String,
    current_tooltip: String, // ✅ 新增：用于存储动态显示的文本
    is_running: bool, // 👈 新增：用来记住当前的运行状态
}

impl Tray for WallpaperTray {
    fn title(&self) -> String { "Wallpaper Engine GUI".into() }

    // fn tool_tip(&self) -> ToolTip {
    //     ToolTip {
    //         title: "Linux Wallpaper Engine GUI".into(),
    //         // ✅ 动态读取当前的壁纸状态
    //         description: self.current_tooltip.clone(),
    //         icon_name: "".into(),
    //         icon_pixmap: vec![],
    //     }
    // }

    fn tool_tip(&self) -> ToolTip {
        ToolTip {
            // 💡 绝杀：直接把动态状态拼接到主标题里，利用 \n 强制换行！
            // 这样不管什么桌面环境，都绝对拦截不了我们的状态显示！
            title: format!("<b>Wallpaper Engine GUI</b>\n{}", self.current_tooltip),
            description: "".into(),
            icon_name: "".into(),
            icon_pixmap: vec![],
        }
    }

    fn icon_pixmap(&self) -> Vec<Icon> { vec![] } 

    fn icon_name(&self) -> String {
        if !self.is_running {
            // 如果传来的是绝对路径 (兼容老模式)
            if self.icon_path.starts_with('/') {
                let stopped_path = self.icon_path.replace(".png", "-stopped.png");
                if std::path::Path::new(&stopped_path).exists() {
                    return stopped_path;
                }
            } else {
                // ✨ 核心修复：如果传来的是干净的名字 "com.wallpaperengine.tray"
                // 直接凭借 DE 规范，加上 "-stopped" 发送给桌面环境！
                return format!("{}-stopped", self.icon_path);
            }
            return "media-playback-stop".into();
        }

        // 运行状态：直接原样返回（无论是路径还是名字）
        self.icon_path.clone()
    }

    // ✨ 捕获左键单击（Activate）事件
    fn activate(&mut self, _x: i32, _y: i32) {
        // 左键点击时，直接向 Python 发送 --toggle 指令！
        self.exec("--toggle");
    }


    fn menu(&self) -> Vec<MenuItem<Self>> {
        vec![
            MenuItem::Standard(StandardItem {
                label: "Show Window".into(),
                activate: Box::new(|tray: &mut Self| tray.exec("--show")),
                ..Default::default()
            }),
            MenuItem::Separator,
            MenuItem::Standard(StandardItem {
                label: "Play/Stop".into(),
                activate: Box::new(move |tray: &mut Self| {
                    if is_engine_running() {
                        tray.exec("--stop");
                    } else {
                        tray.exec("--apply-last");
                    }
                }),
                ..Default::default()
            }),
            MenuItem::Standard(StandardItem {
                label: "Random Wallpaper".into(),
                activate: Box::new(|tray: &mut Self| tray.exec("--random")),
                ..Default::default()
            }),
            MenuItem::Separator,
            MenuItem::Standard(StandardItem {
                label: "Quit Application".into(),
                activate: Box::new(|tray: &mut Self| tray.exec("--quit")),
                ..Default::default()
            }),
        ]
    }
}

impl WallpaperTray {
    fn exec(&self, arg: &str) {
        let socket_name = self.socket_path.clone(); // 这里现在存的是名字，不是路径
        let cmd_str = arg.to_string();
        
        thread::spawn(move || {
            // ✨ 利用 Linux 专属 API 生成抽象地址
            if let Ok(addr) = SocketAddr::from_abstract_name(socket_name.as_bytes()) {
                match std::os::unix::net::UnixStream::connect_addr(&addr) {
                    Ok(mut stream) => {
                        if let Err(e) = stream.write_all(format!("{}\n", cmd_str).as_bytes()) {
                            log(&format!(
                                "Failed to send command '{}' to IPC socket {}: {}",
                                cmd_str, socket_name, e
                            ));
                        }
                    }
                    Err(e) => log(&format!("Failed to connect to IPC socket {}: {}", socket_name, e)),
                }
            }
        });
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let icon_path = args.get(1).cloned().unwrap_or_default();
    let parent_pid: u32 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(0);

    let socket_path = std::env::var("LWG_IPC_SOCKET").unwrap_or_else(|_| {
        format!("lwg-ipc-{}", get_uid()) // 不再带 /tmp/
    });

    log(&format!("Starting. icon={icon_path} parent_pid={parent_pid} socket={socket_path}"));

    unsafe {
        libc::signal(libc::SIGTERM, handle_sigterm as *const () as usize);
    }
    SHOULD_EXIT.store(false, Ordering::Relaxed);

    // ✨ 建立 RX 管道：完全存在于内存中
    let rx_name = format!("lwg-tray-rx-{}", get_uid());
    let addr = SocketAddr::from_abstract_name(rx_name.as_bytes()).expect("Failed to create abstract address");
    
    // 🗑️ 删除了所有的 fs::remove_file 垃圾清理代码！
    let listener = match UnixListener::bind_addr(&addr) {
        Ok(l) => l,
        Err(e) => {
            log(&format!("Failed to bind abstract RX socket {}: {}", rx_name, e));
            std::process::exit(1);
        }
    };

    let service = TrayService::new(WallpaperTray {
        icon_path,
        socket_path,
        current_tooltip: "Waiting for status...".into(),
        is_running: false, // 👈 初始默认没运行
    });

    let handle = service.handle();
    service.spawn();

    let handle_clone = handle.clone();
    thread::spawn(move || {
        for stream in listener.incoming() {
            match stream {
                Ok(stream) => {
                    let reader = BufReader::new(stream);
                    for line in reader.lines() {
                        if let Ok(text) = line {
                            handle_clone.update(|tray: &mut WallpaperTray| {
                                // ✨ 解析 Python 发来的 "ACTIVE|<b>Running...</b>"
                                if let Some((state, tooltip)) = text.split_once('|') {
                                    tray.is_running = state == "ACTIVE";
                                    tray.current_tooltip = tooltip.to_string();
                                } else {
                                    // 兼容老格式（防挂）
                                    tray.is_running = false;
                                    tray.current_tooltip = text;
                                }
                            });
                        }
                    }
                }
                Err(e) => log(&format!("RX socket accept error: {}", e)),
            }
        }
    });

    loop {
        thread::sleep(Duration::from_millis(500));

        if SHOULD_EXIT.load(Ordering::Relaxed) {
            log("Received SIGTERM. Exiting gracefully...");
            // let _ = fs::remove_file(&rx_socket_path);
            thread::sleep(Duration::from_millis(500));
            log("Graceful exit complete.");
            std::process::exit(0);
        }

        if parent_pid > 0 && !pid_exists(parent_pid) {
            log("Parent process died. Exiting gracefully...");
            // let _ = fs::remove_file(&rx_socket_path);
            thread::sleep(Duration::from_millis(500)); 
            std::process::exit(0);
        }
    }
}

fn pid_exists(pid: u32) -> bool { Path::new(&format!("/proc/{pid}")).exists() }

fn is_engine_running() -> bool {
    let Ok(entries) = fs::read_dir("/proc") else { return false; };
    for entry in entries.flatten() {
        let name = entry.file_name();
        let name = name.to_string_lossy();
        if !name.chars().all(|c| c.is_ascii_digit()) { continue; }
        
        let exe_path = entry.path().join("exe");
        if let Ok(target) = fs::read_link(&exe_path) {
            if let Some(fname) = target.file_name().and_then(|s| s.to_str()) {
                if fname == "linux-wallpaperengine" { return true; }
            }
        } else {
            let cmdline_path = entry.path().join("cmdline");
            if let Ok(bytes) = fs::read(&cmdline_path) {
                if let Some(pos) = bytes.iter().position(|&b| b == 0) {
                    let exec_path = String::from_utf8_lossy(&bytes[..pos]);
                    let exec_name = Path::new(exec_path.as_ref())
                        .file_name()
                        .and_then(|s| s.to_str())
                        .unwrap_or("");
                    if exec_name == "linux-wallpaperengine" { return true; }
                }
            }
        }
    }
    false
}

fn log(msg: &str) {
    if std::env::var("LWG_DEBUG").unwrap_or_default() != "1" {
        return;
    }
    use std::io::Write;
    let dir = dirs_next();
    let _ = fs::create_dir_all(&dir);
    let path = format!("{dir}/tray_crash.log");
    if let Ok(mut f) = fs::OpenOptions::new().append(true).create(true).open(&path) {
        let ts = chrono_now();
        let _ = writeln!(f, "[{ts}] [TRAY-RS] {msg}");
    }
}

fn dirs_next() -> String {
    env::var("HOME").unwrap_or_else(|_| "/tmp".into()) + "/.cache/linux-wallpaperengine-gui"
}

fn chrono_now() -> String {
    std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs().to_string()
}
```

---

