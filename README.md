# Linux Wallpaper Engine Python GUI

一个现代化的 GTK4/Libadwaita 图形界面，用于管理和应用 Linux Wallpaper Engine 的动态壁纸。

## 🎯 项目目标

- **轻量化**：相比 Electron 版本（社区开发者贡献的 `linux-wallpaperengine-gui`），内存占用更低（<150MB）
- **原生体验**：使用 GTK4 + Libadwaita，与 GNOME/现代 Linux 桌面环保
- **易用性**：提供直观的壁纸浏览、选择与应用界面
- **功能完整性**：逐步对标社区 GUI 的功能

## 🆕 最近更新 (2026-01-24)

- **系统托盘图标**：基于 `libayatana-appindicator` 实现，完美支持 Wayland (Niri/Sway/Hyprland) + Waybar 环境。
- **代码重构**：将单文件脚本拆分为模块化包结构 (`py_GUI/`)，分离逻辑与界面。
- **项目结构优化**：更名项目包为 `py_GUI`，新增启动脚本 `run_gui.py`。
- **性能优化**：改进了图片资源的加载与缓存机制。
- **稳定性修复**：修复了子进程输出导致的死锁问题，现在日志将重定向到文件而非管道。
- **UI 精简与交互优化**：
  - **隐藏失效属性栏**：鉴于 C++ 后端在 Wayland 环境下的局限性（Web/Scene 属性无法生效），暂时禁用了侧边栏 Properties 编辑区，提升了界面整洁度并避免功能误导（代码已注释保留）。
  - **样式统一**：壁纸显示类型（Type）现在使用与标签一致的胶囊（Capsule）样式，视觉体验更统一。
- **高级渲染与音频控制**：
  - **视觉管理**：新增禁用视差效果（Parallax）、禁用粒子系统（Particles）开关，以及纹理钳制（Clamping）模式选择。
  - **音频增强**：新增禁用自动静音（Auto Mute）、禁用音频处理逻辑（Audio Processing）开关。
- **截图功能大修 (v0.8)**：
  - **真·静默截图**：智能检测并利用 `Xvfb` 实现无窗口后台截图（支持开关切换）。
  - **真·4K 采样**：强制后端以 3840x2160 分辨率渲染，完美解决平铺窗口管理器（如 Niri）下的画面裁切问题。
  - **交互闭环**：截图按钮实时状态反馈（📸 -> ⏳），成功后提供“打开图片/文件夹”快捷入口。
  - **智能策略**：针对视频壁纸启用极速模式（5帧），针对 Web 壁纸自适应延长等待时间。

## ⚠️ 已知问题

- **❗ 不明内存泄漏风险**：目前观察到在长期运行（特别是使用复杂 Web 类型壁纸）时，可能会出现**原因不明的内存缓慢泄漏**。
  - 虽然我们已修复了核心的子进程死锁问题，但此泄漏可能源于底层 Chromium 渲染引擎、Python 绑定或 C++ 后端本身。
  - **建议**：如果长时间挂机，建议定期使用 `--stop` 停止壁纸或完全重启应用以释放资源。
- **多显示器支持限制**：当前仅支持单一屏幕，多屏幕独立壁纸功能尚待后端支持。

## 🧩 壁纸兼容性与后端限制

本 GUI 依赖 `linux-wallpaperengine` C++ 后端进行渲染。由于后端是通过逆向工程实现的（非官方移植），且 Linux 图形栈（特别是 Wayland）与 Windows 存在差异，部分壁纸可能无法完美显示。

### 1. 壁纸类型推荐
- ✅ **Video (.mp4, .webm)**: 支持最完美，推荐。
- ⚠️ **Web (.html)**: **部分支持**。
  - 渲染通常正常，能够显示画面。
  - **❌ 属性调整失效**：由于 C++ 后端在 Linux/Wayland 环境下的 CEF（网页内核）通信限制，**无法通过 GUI/CLI 动态调整 Web 壁纸属性**（如语言切换、音乐开关、实时数值变化等）。所有 Web 属性在应用时基本处于失效状态。
- ⚠️ **Scene (.pkg)**: **支持有限**。
  - 简单的 2D/3D 场景通常正常。
  - 包含复杂**粒子系统** (Particles)、**自定义着色器** (Shaders) 或**复杂脚本**的壁纸可能无法渲染。
  - **症状**：日志显示资源已加载（如 `Particle system loaded`），但屏幕上看不到粒子或特效。

### 2. Wayland 环境特别说明 (Niri/Hyprland/Sway)
如果您在使用 Wayland 混成器：
- **❌ 鼠标交互失效**：由于 Wayland 的安全隔离机制，作为壁纸层运行的应用通常**无法获取全局鼠标位置**。
  - **后果**：**鼠标拖尾 (Mouse Trails)**、点击互动效果将**无法使用**。即使在窗口模式下，部分依赖 Windows 特定 API 的交互脚本也可能失效。
- **⚠️ OpenGL/GLX 兼容性**：部分旧式特效依赖 GLX (X11)，在纯 Wayland 环境下可能因 `Failed to initialize GLEW: No GLX display` 错误导致渲染层级异常或 **Web 属性注入失效**。
- **❌ Web 交互通信**：后端在尝试向 CEF 注入 JavaScript 以修改壁纸属性时，常因为环境不匹配或时机问题静默失败。

## ✅ 当前功能

### 核心功能
- ✅ **系统托盘**：常驻托盘图标，支持显示/隐藏、播放/停止（智能切换）、随机切换壁纸、退出程序
- ✅ **壁纸浏览**：从 Steam Workshop 自动扫描壁纸库
- ✅ **双视图模式**：Grid（网格）与 List（列表）视图切换
- ✅ **侧边栏详情**：显示壁纸大图、标题、类型、标签、描述
- ✅ **壁纸应用**：点击 Apply 按钮或双击卡片直接应用壁纸
- ✅ **右键菜单**：支持应用、停止、删除壁纸及打开所在文件夹
- ✅ **随机选择**：I'm feeling lucky 随机应用一张壁纸
- ✅ **快速刷新**：Refresh 按钮即时加载新下载的壁纸（无需重启）
- ✅ **自动应用**：启动时自动应用上次壁纸（读取 config.json 的 lastWallpaper/lastScreen）

### 进程管理
- ✅ **后端调用**：正确使用 `linux-wallpaperengine` 的参数格式
- ✅ **单实例控制**：应用前自动 pkill 旧进程，避免堆叠
- ✅ **参数整数化**：音量严格传递为整数字符串，防止浮点数崩溃

### 壁纸属性编辑（v0.3 - 暂时禁用）
- ⚠️ **功能保留但已隐藏**：由于后端环境限制，目前在侧边栏已隐藏此区域。底层逻辑仍保留，支持：
  - 调用 `--list-properties` 获取属性
  - 动态生成 Slider/Toggle/Color/Combo 控件
  - 属性值持久化与持久化恢复

### 多显示器支持（v0.8 Beta）
- ✅ **独立控制**：在主界面顶栏选择目标显示器，分别为不同屏幕设置不同壁纸。
- ✅ **状态自愈**：启动时自动检测屏幕连接状态，智能清理已断开屏幕的配置，防止后端报错。
- ✅ **全局管理**：托盘菜单的“随机播放”和“停止”操作会自动作用于所有活跃屏幕。

### 搜索功能（v0.3）
- ✅ **实时搜索**：顶部搜索框支持按关键词实时过滤壁纸
- ✅ **多字段匹配**：搜索范围包括
  - 壁纸标题
  - 描述文本
  - 标签（Tags）
  - 文件夹名称

### 辅助功能
- ✅ **一键截图**：集成在顶栏的截图按钮 (`--screenshot`)。
  - **静默模式**：自动检测 `xvfb`，实现无窗口后台截图（推荐安装 `xvfb`）。支持在设置中手动关闭以使用物理窗口模式。
  - **4K 采样**：强制以 3840x2160 分辨率渲染，解决平铺窗口管理器下的画面裁剪问题。
  - **智能回退**：若无 Xvfb，自动回退到物理窗口模式并自动关闭。
- ✅ **截图配置**：支持自定义截图延迟（解决动态壁纸加载慢）和目标分辨率。
- ✅ **截图管理**：自动保存至 `~/Pictures/wallpaperengine`，成功后可直接打开。

### 辅助功能
- ✅ **一键截图**：集成在顶栏的截图按钮 (`--screenshot`)。
  - **静默模式**：自动检测 `xvfb`，实现无窗口后台截图（推荐安装 `xvfb`）。支持在设置中手动关闭以使用物理窗口模式。
  - **4K 采样**：强制以 3840x2160 分辨率渲染，解决平铺窗口管理器下的画面裁剪问题。
  - **智能回退**：若无 Xvfb，自动回退到物理窗口模式并自动关闭。
- ✅ **截图配置**：支持自定义截图延迟（解决动态壁纸加载慢）和目标分辨率。
- ✅ **截图管理**：自动保存至 `~/Pictures/wallpaperengine`，成功后可直接打开。

### 配置管理
- ✅ **设置页面**：General、Audio、Advanced、Logs 四大类配置
- ✅ **FPS 限制**：1～144fps 可调
- ✅ **音频控制**：静音/音量/禁用自动静音/禁用音频分析
- ✅ **视觉管理**：缩放模式/边缘钳制/禁用视差/禁用粒子系统
- ✅ **运行优化**：全屏暂停/鼠标交互禁用开关
- ✅ **环境适配**：Advanced 中下拉选择屏幕名，支持 Workshop 路径自定义

### 日志面板（v0.5）
- ✅ **实时日志显示**：应用和壁纸引擎的日志实时显示
- ✅ **日志级别**：支持 DEBUG/INFO/WARNING/ERROR 级别
- ✅ **日志来源**：区分 Controller/Engine/GUI 来源
- ✅ **日志管理**：Clear/Refresh 按钮，自动限制最大500条
- ✅ **等宽字体**：便于阅读日志内容
- ✅ **颜色区分**：不同日志级别使用不同颜色
- ✅ **一键复制**：Copy Logs 按钮可将日志内容复制到系统剪贴板

### UI/UX
- ✅ **现代深色主题**：圆角、阴影、悬停效果
- ✅ **窗口约束**：侧边栏固定 320px 宽度，不被图片撑宽
- ✅ **当前壁纸显示**：顶部工具栏显示当前应用的壁纸名称
- ✅ **右键菜单优化**：跟随鼠标位置弹出，支持点选或“按住-拖动-松手”的快速操作
- ✅ **Stop 按钮**：快速停止当前壁纸播放
- ✅ **后台保活窗口隐藏**：关闭窗口会隐藏到后台（进程保留）

### 后台/CLI 控制（v0.3）
- ✅ **后台启动**：支持 `--hidden/--minimized` 启动参数，启动后仅后台运行，无窗口显示
- ✅ **单实例 CLI 控制**：所有命令行动作发往同一运行实例（复用 GTK 主线程，避免多开）
- ✅ **显示/隐藏窗口**：
  - `--show`：显示窗口（若已运行则展示）
  - `--hide`：隐藏窗口（进程保持）
  - `--toggle`：切换显示/隐藏状态
- ✅ **快捷操作**：
  - `--refresh`：重新扫描并加载壁纸库
  - `--apply-last`：直接应用上次保存的壁纸
  - `--quit`：完全退出应用与后台进程

## ❌ 尚缺功能

### 优先级 P1（核心缺失）
- 暂无

### 优先级 P2（功能缺失）
- ❌ **自定义资源**：`--assets-dir` 自定义 assets 目录路径
- ⚠️ **自启动集成**：无 systemd 单元、桌面文件、AUR 打包

- ❌ **动态壁纸预览**：GIF 预览仅显示首帧（性能考虑暂未实现动画）
- ❌ **Wayland 专属优化**：`--fullscreen-pause-only-active` 等精细化控制


### 优先级 P3 (低频/复杂)
- ❌ **窗口模式**：`--window` (需 UI 支持自定义几何坐标)
- ❌ **播放列表**：`--playlist` (需 UI 支持列表管理)

## 🧭 后台/CLI 控制使用指南

### 启动方式

**前台启动（带 GUI）**：
```bash
python3 run_gui.py
```

**后台启动（无 GUI，仅保活进程）**：
```bash
python3 run_gui.py --hidden
# 或
python3 run_gui.py --minimized
```

### 命令行动作

所有以下命令都会发往**同一运行实例**，避免重复启动：

| 命令 | 效果 | 示例 |
|------|------|------|
| `--show` | 显示窗口（若已运行） | `python3 run_gui.py --show` |
| `--hide` | 隐藏窗口（进程保持） | `python3 run_gui.py --hide` |
| `--toggle` | 切换显示/隐藏状态 | `python3 run_gui.py --toggle` |
| `--refresh` | 重新扫描壁纸库 | `python3 run_gui.py --refresh` |
| `--apply-last` | 应用上次保存的壁纸 | `python3 run_gui.py --apply-last` |
| `--stop` | 停止当前播放 | `python3 run_gui.py --stop` |
| `--random` | 随机切换壁纸 | `python3 run_gui.py --random` |
| `--quit` | 完全退出应用与进程 | `python3 run_gui.py --quit` |

### Niri 配置示例

在 `~/.config/niri/config.kdl` 中添加自启动：

```kdl
// 后台启动壁纸引擎 GUI（带自动应用上次壁纸）
exec python3 /path/to/run_gui.py --hidden
```

在 niri 运行中，可用快捷键或脚本调用：

```bash
# 显示 GUI 以选择壁纸
python3 run_gui.py --show

# 快速应用上次壁纸
python3 run_gui.py --apply-last

# 隐藏回后台
python3 run_gui.py --hide
```

## 🛠️ 技术栈

- **语言**：Python 3.10+
- **UI 框架**：PyGObject (GTK4) + Libadwaita
- **系统托盘**：libayatana-appindicator (GTK3)
- **后端**：linux-wallpaperengine（C++ 实现）
- **依赖**：
  ```bash
  python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 libayatana-appindicator
  ```

## 🚀 快速开始

```bash
# 安装依赖
sudo apt-get install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 libayatana-appindicator
# Arch Linux:
# sudo pacman -S python-gobject gtk4 libadwaita libayatana-appindicator

# 运行
python3 run_gui.py
```

## 📝 配置文件

保存位置：`~/.config/linux-wallpaperengine-gui/config.json`

示例：
```json
{
  "fps": 30,
  "volume": 50,
  "scaling": "default",
  "silence": true,
  "noFullscreenPause": false,
  "disableMouse": false,
  "lastWallpaper": "3310692710",
  "lastScreen": "eDP-1",
  "wallpaperProperties": {
    "1828698678": {
      "music": "0",
      "atomic_info": "atomic_mass"
    }
  }
}
```

## 🤝 贡献

欢迎提交 Issue 与 PR！特别是以下方面：
- 新功能实现
- Bug 修复与性能优化
- 翻译与文档改进

## 📄 许可证

MIT License

---

**最后更新**：2026-01-24
**版本**：v0.7.0 (模块化重构版)
