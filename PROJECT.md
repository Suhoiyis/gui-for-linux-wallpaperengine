# LWG (Linux Wallpaper Engine) GUI Project

## 项目概述

这是一个 Linux Wallpaper Engine 的图形用户界面项目，使用 **Python + GTK4 + Libadwaita** 构建。项目提供了现代化的界面来管理和应用 Steam Workshop 上的动态壁纸。

### 核心目标

1. **轻量高效**：使用 GTK4 原生控件，内存占用远低于 Electron/Tauri 方案
2. **现代界面**：Libadwaita 提供自适应主题，完美融入 GNOME 桌面
3. **功能完整**：多显示器支持、播放列表、历史记录、昵称系统等

### 项目状态

| 组件 | 状态 | 说明 |
|------|------|------|
| `py_GUI/` | 🟢 主开发线 | Python GTK4 应用 |
| `lwg-rs/` | 🟡 可选依赖 | 独立 Rust 核心库 |
| `lwg-gui-tauri/` | 🔴 已归档 | Tauri 实验（因 WebKit 内存问题归档） |

> **归档说明**: Tauri 版本因 WebKitGTK 内存泄漏（启动后 ~3GB）而归档。GTK4 版本内存占用显著更优。

---

## 目录结构

```
suw/
├── py_GUI/                  # 🎯 主要开发区域 - Python GTK4 应用
│   ├── core/                # 核心业务逻辑
│   │   ├── config.py        # 配置管理
│   │   ├── controller.py    # 壁纸进程控制
│   │   ├── wallpaper.py     # 壁纸扫描与管理
│   │   ├── screen.py        # 多显示器管理
│   │   ├── state.py         # 应用状态与事件总线
│   │   ├── history.py       # 播放历史 (30条)
│   │   ├── nickname.py      # 壁纸昵称系统
│   │   ├── playlists.py     # 播放列表服务
│   │   ├── performance.py   # 性能监控
│   │   ├── logger.py        # 日志系统
│   │   ├── updater.py       # 更新检查
│   │   └── integrations.py  # 系统集成 (.desktop)
│   │
│   ├── ui/                  # 用户界面
│   │   ├── app.py           # 主应用窗口
│   │   ├── pages/           # 页面视图
│   │   │   ├── library.py   # 壁纸库主页面
│   │   │   ├── settings.py  # 设置页面
│   │   │   └── performance.py # 性能监控页面
│   │   ├── components/      # 可复用组件
│   │   ├── tray.py          # 系统托盘
│   │   └── compact_window.py # 紧凑预览模式
│   │
│   ├── main.py              # 应用入口
│   └── const.py             # 常量、版本、CSS样式
│
├── lwg-rs/                  # 📦 可选 Rust 核心库
│   └── crates/
│       └── lwg-core/        # 核心逻辑实现
│           ├── src/config.rs
│           ├── src/controller.rs
│           ├── src/wallpaper.rs
│           └── ...
│
├── lwg-gui-tauri/           # 🔴 已归档 - Tauri 实验
│   └── ...                  # 仅供参考，不再维护
│
└── .sisyphus/               # Agent 工作文件
    └── plans/               # 工作计划存储
```

---

## 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| **语言** | Python 3.10+ | 主要开发语言 |
| **UI 框架** | GTK4 + Libadwaita | 原生 Linux 桌面界面 |
| **系统托盘** | Rust (ksni) + Python sidecar | 托盘图标与菜单 |
| **后端引擎** | linux-wallpaperengine | 壁纸渲染 (外部 C++ 程序) |
| **可选核心** | lwg-rs | Rust 核心库 (可选) |

---

## 关键数据流

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
│  │         渲染 · 音频 · 截图                    ││
│  └──────────────────────────────────────────────┘│
│                                                  │
│  ┌─────────────────────────────────────────────┐ │
│  │         System Tray (Rust + Ksní)           │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

---

## 配置文件格式

### 1. 用户配置 (User Preferences)
位置: `~/.config/linux-wallpaperengine-gui/config.json`

```json
{
  "fps": 30,
  "volume": 0,
  "scaling": "default",
  "clamping": "clamp",
  "silence": true,
  "workshopPath": "/path/to/workshop",
  "wallpaperProperties": {},
  "wallpaperNicknames": {},
  "cycleEnabled": false,
  "cycleInterval": 15
}
```

### 2. 运行时状态 (Runtime State)
位置: `~/.local/state/linux-wallpaperengine-gui/state.json`

```json
{
  "active_monitors": {"HDMI-1": "2874425843"},
  "lastWallpaper": "2874425843",
  "lastScreen": "HDMI-1"
}
```

### 3. 字段命名约定

Python 内部使用 `snake_case`，但配置文件支持别名兼容：

| 内部名称 | 配置文件别名 | 说明 |
|----------|-------------|------|
| `silence` | `muteAudio` | 静音 |
| `wayland_only_active` | `waylandOnlyActive` | Wayland 仅活动窗口暂停 |
| `compact_mode` | `compactMode` | 紧凑模式 |

完整别名定义见 `py_GUI/core/schema.py`。

---

## 重要开发规则

### 1. 后端引擎参数传递

在 `py_GUI/core/controller.py` 中，参数按以下优先级传递：

| 配置项 | 引擎标志 | 说明 |
|--------|---------|------|
| `silence=True` | `--silent` | **最高优先级** |
| `volume` | `--volume` | 仅非静音时传递 |
| `fps` | `-f` | 帧率限制 |
| `scaling` | `--scaling` | 缩放模式 |
| `clamping` | `--clamp` | ⚠️ 是 `--clamp` 不是 `--clamping` |

### 2. 壁纸路径结构

```
{workshopPath}/{wallpaperId}/
├── project.json    # 壁纸元数据
├── preview.jpg     # 预览图
└── scene.json      # 场景文件 (或 index.html, video.mp4)
```

### 3. 事件总线

使用 `AppStateBus` 进行跨组件通信：

```python
bus = AppStateBus()
bus.emit("wallpaper-changed", wp_id)
bus.on("config-saved", callback)
```

---

## 常见任务

### 添加新的设置项

1. 在 `py_GUI/core/schema.py` 中添加字段和默认值
2. 在 `py_GUI/ui/pages/settings/` 中添加 UI 控件
3. 如需引擎参数，更新 `py_GUI/core/controller.py`

### 运行项目

#### 系统要求

- Python 3.10+
- GTK4 + Libadwaita
- linux-wallpaperengine (后端)

#### 系统依赖 (Arch Linux)

```bash
sudo pacman -S python-gobject gtk4 libadwaita libayatana-appindicator
```

#### 系统依赖 (Ubuntu/Debian)

```bash
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 libayatana-appindicator3-1
```

#### 开发模式

```bash
python3 py_GUI/main.py
```

#### 构建 AppImage

```bash
./build_appimage.sh
```

---

## 注意事项

### ⚠️ 引擎参数易错点

- 引擎使用 `--clamp` 不是 `--clamping`
- 引擎使用 `-f` 表示帧率，不是 `--fps`
- 开发时应参考 `py_GUI/core/controller.py`

### ⚠️ 配置文件兼容

配置文件需要保持向后兼容，修改前检查：
- `py_GUI/core/schema.py` 中的字段定义和别名

---

## 外部依赖

### linux-wallpaperengine

实际的壁纸渲染引擎，GUI 是其前端。

- **安装路径**: `/opt/linux-wallpaperengine/linux-wallpaperengine` 或 PATH 中
- **官方仓库**: https://github.com/Almamu/linux-wallpaperengine

### Steam Workshop

壁纸默认存储位置：

```
~/.local/share/Steam/steamapps/workshop/content/431960/{wallpaperId}/
```

---

## 调试技巧

1. **Python 日志**: 查看 `~/.cache/linux-wallpaperengine-gui/` 中的日志
2. **配置文件**: 手动编辑 `~/.config/linux-wallpaperengine-gui/config.json` 测试
3. **引擎测试**: 直接运行 `linux-wallpaperengine` 命令测试参数
4. **调试模式**: 设置环境变量 `LWG_DEBUG=1` 启用详细日志

---

## 🖼️ 系统托盘实现

- **实现方式**: Rust sidecar (`lwg-rs/crates/lwg-tray/`) 通过 Python 启动
- **通信方式**: Abstract Socket IPC
- **功能**:
  - 动态图标（播放/停止状态切换）
  - 左键切换主窗口
  - 右键菜单（快捷操作）
  - 多显示器状态显示

---

## 联系信息

- 项目路径: `/home/yua/suw`
- 主要开发分支: `main`
