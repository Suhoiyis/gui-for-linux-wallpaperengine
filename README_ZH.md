<h1 align="center">
  <img src="pic/icons/GUI_rounded.png" alt="Logo" width="128" height="128" style="border-radius: 20px;"/><br>
  LINUX WALLPAPER ENGINE GUI
</h1>

<p align="center">一个现代化的桌面图形界面，用于在 Linux 上管理和应用 Steam Workshop 动态壁纸，基于 Tauri + React + Rust 构建。</p>

<p align="center">
  <a href="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases/latest">
    <img src="https://img.shields.io/github/v/release/Suhoiyis/gui-for-linux-wallpaperengine?color=success&label=Release&style=flat-square" alt="Latest Release">
  </a>
  <a href="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Suhoiyis/gui-for-linux-wallpaperengine?style=flat-square&color=blue" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Platform-Linux-lightgrey?style=flat-square&logo=linux" alt="Platform">
  <img src="https://img.shields.io/badge/Tauri-v2-24c8d8?style=flat-square&logo=tauri" alt="Tauri">
  <img src="https://img.shields.io/badge/React-19-61dafb?style=flat-square&logo=react" alt="React">
  <img src="https://img.shields.io/badge/Rust-1.75+-dea584?style=flat-square&logo=rust" alt="Rust">
</p>

<p align="center">
    <a href="README.md">English</a> | 
    <strong>简体中文</strong>
<p>

> 基于 [Almamu/linux-wallpaperengine](https://github.com/Almamu/linux-wallpaperengine) 后端构建，针对 GNOME / Wayland 桌面环境进行了优化。

## ✨ 功能特性

### 核心功能

- 🎨 **浅色/深色主题自适应**: 适配系统的浅色或深色主题
- 🖥️ **多显示器支持**: 通过屏幕选择下拉框为每个显示器设置独立的壁纸
- ✏️ **别名系统**: 为壁纸分配自定义别名以便于识别
- ⭐ **收藏系统**: 标记您喜爱的壁纸以便快速访问（新功能）
- 📋 **播放列表**: 创建自定义壁纸集合，支持拖拽排序（新功能）
- 🔍 **搜索与排序**: 实时关键词搜索；支持按名称、大小或 ID 排序
- 📺 **系统托盘**: 原生托盘图标，支持播放/停止/随机切换控制

### 进阶功能

- 🪟 **紧凑模式**: 专为平铺式窗口管理器设计的迷你窗口
- 📊 **性能监控**: 实时 CPU/内存追踪，提供图表和进程明细
- 📸 **智能截图**: 通过 Xvfb 静默截取 4K 截图，支持截图历史
- 🔄 **定时轮换**: 按可配置的时间间隔自动切换壁纸
- 🎛️ **Wayland 微调**: 针对 Wayland 特定行为的精细化控制
- 📋 **日志管理**: 按来源过滤日志（GUI/Core/Engine/Controller）

## 🚀 安装指南

### 1. 安装后端（必须）

本 GUI 需要核心渲染引擎：

```bash
# Arch Linux
yay -S linux-wallpaperengine

# 其他发行版
# 请参考 https://github.com/Almamu/linux-wallpaperengine 的编译说明
```

验证安装：
```bash
which linux-wallpaperengine  # 应输出程序路径
```

### 2. 安装 GUI

从 [Releases 页面](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases) 下载 AppImage：

```bash
# 赋予执行权限
chmod +x lwg-gui-*-x86_64.AppImage

# 运行
./lwg-gui-*-x86_64.AppImage
```

### 系统要求

- Ubuntu 22.04+ 或同等发行版
- `webkit2gtk-4.1`（现代发行版通常已预装）

```bash
# Ubuntu/Debian
sudo apt install libwebkit2gtk-4.1-0
```

## 📖 基本用法

### 浏览与应用壁纸

1. **浏览**: 应用首次启动时会自动扫描您的 Steam Workshop 壁纸库
2. **应用**: 双击壁纸卡片或点击 **Apply** 按钮
3. **随机**: 点击 🎲 按钮或使用托盘菜单
4. **停止**: 点击 ⏹ 按钮
5. **多显示器**: 从顶栏下拉菜单中选择目标显示器

### 播放列表与收藏

- **创建播放列表**: 点击侧边栏的 "+" 按钮，或选择多个壁纸后创建新播放列表
- **添加收藏**: 点击任意壁纸卡片上的 ⭐ 图标
- **快速访问**: 收藏和播放列表会显示在侧边栏中

### 设置组织

设置分为 4 个标签页：

| 标签页 | 设置内容 |
|--------|----------|
| **播放** | FPS、缩放、裁剪、视差、粒子、轮换、Wayland 微调 |
| **显示** | 音量、静音、主题 |
| **系统** | 路径、自启动、截图、别名、收藏 |
| **日志** | 实时日志查看器，支持过滤 |

## 🚀 自启动

应用可以通过 **设置 → 系统 → 登录时运行** 配置开机自动启动。

如需启动时最小化到托盘，请启用 **设置 → 系统 → 隐藏启动**。

**示例:** 在 Niri 中自动启动
```bash
# 在 niri config.kdl 中
spawn-at-startup "path/to/linux-wallpaperengine-gui" "--hidden"
```

**示例:** 在 Hyprland 中自动启动
```ini
# 在 hyprland.conf 中
exec-once = path/to/linux-wallpaperengine-gui --hidden
```

**示例:** 在 i3 中自动启动
```
# 在 i3 config 中
exec --no-startup-id path/to/linux-wallpaperengine-gui --hidden
```

## ⚙️ 配置

配置文件遵循 XDG 规范：

| 文件 | 位置 | 用途 |
|------|------|------|
| `config.json` | `~/.config/linux-wallpaperengine-gui/` | 主设置 |
| `state.json` | `~/.local/state/linux-wallpaperengine-gui/` | 运行时状态 |
| `nicknames.json` | `~/.local/share/linux-wallpaperengine-gui/` | 自定义别名 |
| `favorites.json` | `~/.local/share/linux-wallpaperengine-gui/` | 收藏列表 |
| `playback_history.json` | `~/.cache/linux-wallpaperengine-gui/` | 播放历史 |
| `screenshot_history.json` | `~/.cache/linux-wallpaperengine-gui/` | 截图历史 |

完整配置参考请参阅 [docs/CONFIGURATION.md](docs/CONFIGURATION.md)。

## ⚠️ 已知限制

### 壁纸类型兼容性

| 类型 | 状态 | 备注 |
|------|------|------|
| **Video** | ✅ 完全支持 | 推荐使用 MP4/WebM |
| **Web** | ⚠️ 部分支持 | 属性调节可能无法工作 |
| **Scene** | ⚠️ 受限 | 复杂着色器可能出现故障 |

### Wayland 限制

- ❌ **禁用鼠标交互**: 无法获取全局光标位置
- ❌ **Web 属性注入受限**: CEF 通信受到限制

## ❓ 常见问题

### 如何降低内存占用？

1. 避免使用 Web 壁纸（它们内部使用 CEF/Chromium）
2. 启用定时轮换（设置 → 自动化）以定期重启后端
3. 降低 FPS（设置 → 播放）
4. 禁用音频处理（设置 → 播放）

### 紧凑预览窗口在我的平铺式窗口管理器中没有浮动

您需要在窗口管理器配置中添加窗口规则。Niri 和 Hyprland 的示例请参阅 [docs/old/ADVANCED.md](docs/old/ADVANCED.md#compact-preview-mode) 中的系统集成部分。

### 为什么截图很慢（5–10 秒）？

如果安装了 Xvfb，应用会使用 CPU 软件渲染来静默生成 4K 截图（无弹出窗口）。这虽然较慢，但无论您的物理屏幕分辨率或平铺式窗口管理器布局如何，都能保证一致的质量。您可以在"设置 → 系统"中禁用 Xvfb 模式以获得更快的（但会弹出窗口的）截图。

### 系统托盘图标不显示

1. GNOME 用户：安装 "AppIndicator Support" 扩展
2. Waybar 用户：确保已配置 `tray` 模块
3. i3/Sway 用户：您可能需要 `waybar` 或其他支持托盘的状态栏

### 如何为每个显示器设置不同的壁纸？

从顶栏下拉菜单中选择目标显示器（如 "eDP-1" 或 "HDMI-A-1"），然后浏览并应用壁纸。如需将同一壁纸应用于所有显示器，请选择 "All Screens"。

### 我可以使用 Flatpak 或 AppImage 吗？

**AppImage**: 完全支持。下载后赋予执行权限即可运行。

**Flatpak**: 目前尚未正式支持。文件访问和沙盒限制可能会影响功能。

### 如何报告错误？

1. 前往 设置 → 日志，点击 **Copy Logs**
2. 提交一个 [GitHub Issue](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues)
3. 包含：系统信息 (`uname -a`)、桌面环境、壁纸 ID/类型以及复制的日志

## 🔄 更新与卸载

### 更新

从 [Releases 页面](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases) 下载最新的 AppImage 并替换旧文件。您的配置和播放列表会保留在 `~/.config/linux-wallpaperengine-gui/` 中。

### 卸载

1. **AppImage**: 直接删除 AppImage 文件
2. **配置文件**（可选）：
   ```bash
   rm -rf ~/.config/linux-wallpaperengine-gui
   rm -rf ~/.local/state/linux-wallpaperengine-gui
   rm -rf ~/.local/share/linux-wallpaperengine-gui
   rm -rf ~/.cache/linux-wallpaperengine-gui
   ```

## 📚 文档

| 文档 | 描述 |
|------|------|
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | 快速入门指南 |
| [docs/CONFIGURATION.md](docs/CONFIGURATION.md) | 完整设置参考 |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | 常见问题与解决方案 |
| [docs/MIGRATION.md](docs/MIGRATION.md) | 从 Python 版本迁移指南 |
| [docs/old/](docs/old/) | 旧版 Python 文档 |

## 🏛️ 技术架构

### 项目结构

```
gui-for-linux-wallpaperengine/
├── lwg-gui-tauri/              # 主 Tauri 应用
│   ├── src/                     # React 前端
│   │   ├── components/          # UI 组件（library、settings、performance）
│   │   ├── pages/               # 页面视图（Library、Settings、Performance）
│   │   ├── store/               # Zustand 状态管理
│   │   └── api/                 # Tauri API 封装
│   └── src-tauri/               # Rust 后端
│       └── src/lib.rs           # Tauri 命令和业务逻辑
│
├── lwg-rs/                      # Rust 核心库
│   └── crates/lwg-core/         # 配置、控制器、壁纸管理
│
├── py_GUI/                      # 旧版 Python 版本（仅供参考）
├── docs/                        # 文档
│   ├── old/                     # 旧版 Python 文档
│   └── assets/                  # 截图和图片
└── pic/                         # 应用图标
```

### 架构概览

```
┌──────────────────────────────────────────────────┐
│           Tauri + React + TypeScript             │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ Library  │  │ Settings │  │  Performance   │  │
│  │   Page   │  │   Page   │  │    Monitor     │  │
│  └────┬─────┘  └────┬─────┘  └───────┬────────┘  │
│       │             │                │           │
│  ┌────┴─────────────┴────────────────┴─────────┐ │
│  │         lwg-core (Rust crate)               │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐ │ │
│  │  │ Config   │ │ State    │ │  History     │ │ │
│  │  │ Manager  │ │ Manager  │ │  Manager     │ │ │
│  │  └──────────┘ └──────────┘ └──────────────┘ │ │
│  └──────────────────┬──────────────────────────┘ │
│                     │ subprocess                 │
│  ┌──────────────────┴───────────────────────────┐│
│  │         linux-wallpaperengine (C++)          ││
│  │         渲染 · 音频 · 截图                    ││
│  └──────────────────────────────────────────────┘│
└──────────────────────────────────────────────────┘
```

### 关键设计决策

- **单实例架构**: 所有 CLI 命令都路由到运行中的应用，避免进程重复
- **混合保存策略**: 乐观 UI 更新配合防抖后端持久化
- **XDG 合规**: 配置、状态和缓存文件遵循 XDG 规范
- **类型安全 IPC**: Tauri 命令使用完整的 TypeScript 类型

## 🔧 技术栈

- **前端**: React 19 + TypeScript + Tailwind CSS + shadcn/ui
- **后端**: Tauri v2 + Rust (lwg-core crate)
- **引擎**: Almamu/linux-wallpaperengine (C++)
- **状态**: Zustand 配合乐观更新

## 🤝 贡献

欢迎贡献！

- 功能请求和错误报告 → [提交 Issue](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues)
- 代码贡献 → 提交 Pull Request

## 🙏 致谢

> 部分 UI 设计灵感源自 [AzPepoze/linux-wallpaperengine-gui](https://github.com/AzPepoze/linux-wallpaperengine-gui)。

## 📄 许可证

GPL-3.0 license

---

**当前版本**: v2.0.0

**最后更新**: 2026-03-23