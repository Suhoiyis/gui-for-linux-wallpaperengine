<a href="MIGRATION.md">English</a> | <strong>中文</strong>

# 迁移指南：从 Python 到 Tauri v2.0.0

本指南概述了从旧版 Python GTK 实现迁移到新版 Tauri React 架构的主要变化和迁移步骤。

## Python 到 Tauri

项目已从 Python/GTK 迁移到 Tauri/React。以下是您需要了解的关键变化。

## 架构变更：Python GTK → Tauri React

项目进行了全面的架构重组，以提高性能、类型安全性和用户体验。

| 功能     | 旧版 (Python)                    | 新版 (Tauri v2.0.0)                           |
| :------- | :------------------------------- | :-------------------------------------------- |
| **前端** | Python 3.10+ / GTK4 / Libadwaita | React / TypeScript / Tailwind CSS / shadcn/ui |
| **后端** | Python (子进程管理)              | Rust (`lwg-core` crate)                       |
| **引擎** | `linux-wallpaperengine` (C++)    | `linux-wallpaperengine` (C++)                 |
| **IPC**  | 抽象套接字 (系统托盘 <-> GUI)    | Tauri 命令与事件                              |
| **性能** | 解释器开销                       | 原生 Rust 性能                                |

## 配置文件变更：单文件 → 6 个独立文件

为了更好地遵循 XDG 规范并改进数据管理，配置已从单个 `config.json` 拆分为六个专门的 JSON 文件。

| 文件                        | 路径                                        | 用途                                  |
| :-------------------------- | :------------------------------------------ | :------------------------------------ |
| **config.json**             | `~/.config/linux-wallpaperengine-gui/`      | 主要应用程序设置（FPS、音量、路径）。 |
| **state.json**              | `~/.local/state/linux-wallpaperengine-gui/` | 运行时状态（屏幕与壁纸的映射）。      |
| **nicknames.json**          | `~/.local/share/linux-wallpaperengine-gui/` | 自定义壁纸别名。                      |
| **favorites.json**          | `~/.local/share/linux-wallpaperengine-gui/` | 收藏的壁纸 ID 列表。                  |
| **playback_history.json**   | `~/.cache/linux-wallpaperengine-gui/`       | 最近播放的 30 个壁纸的播放历史。      |
| **screenshot_history.json** | `~/.cache/linux-wallpaperengine-gui/`       | 最近 10 条截图记录的截图历史记录。    |

### 字段命名兼容性

新版本通过 Rust 的 `serde` 别名保持与旧版配置文件的向后兼容性。虽然前端使用 `camelCase`，但后端仍然可以解析旧的 `snake_case` 键。

| 旧版键名 (Python)       | 新版键名 (Tauri)      | 备注                                 |
| :---------------------- | :-------------------- | :----------------------------------- |
| `silence`               | `muteAudio`           | 静音所有壁纸音频。                   |
| `noautomute`            | `noAutomute`          | 防止在其他应用播放声音时自动静音。   |
| `wayland_only_active`   | `waylandOnlyActive`   | 仅当活动窗口全屏时暂停。             |
| `wayland_ignore_appids` | `waylandIgnoreAppids` | 暂停时忽略的应用 ID 列表。           |
| `compact_mode`          | `compactMode`         | 适用于平铺窗口管理器的紧凑预览模式。 |
| `active_monitors`       | `AppState`            | 现在存储在 `state.json` 中。         |

## 设置选项卡映射

设置界面经过重新组织，以使其更加清晰。

| Python 选项卡       | Tauri 选项卡        | 描述                                              |
| :------------------ | :------------------ | :------------------------------------------------ |
| **常规 (General)**  | **播放 (Playback)** | FPS、缩放、裁剪、视差、粒子、轮换、Wayland 微调。 |
| **音频 (Audio)**    | **显示 (Display)**  | 音量、静音、主题。                                |
| **高级 (Advanced)** | **系统 (System)**   | 路径、自启动、截图、别名、收藏。                  |
| **日志 (Logs)**     | **日志 (Logs)**     | 来自 GUI、核心、引擎和控制器的实时日志。          |

## 新功能

- **播放列表支持**：通过专用侧边栏创建、编辑和循环切换自定义壁纸集合。
- **收藏系统**：一键收藏，快速访问最常用的壁纸。
- **批量操作**：改进了别名和播放列表的管理。
- **现代 UI**：使用 React 和 Tailwind CSS 构建的更快速、响应更灵敏的界面。
- **增强的性能监控**：带有各进程细分（前端、后端、系统托盘）的实时 CPU/内存图表。
- **Tauri v2.0.0**：利用最新的 Tauri 功能，实现更好的操作系统集成和安全性。
