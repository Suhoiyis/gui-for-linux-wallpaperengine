# Linux Wallpaper Engine Python GUI

一个现代化的 GTK4/Libadwaita 图形界面，用于管理和应用 Linux Wallpaper Engine 的动态壁纸。

## 🎯 项目目标

- **轻量化**：相比 Electron 版本 linux-wallpaperengine-gui，内存占用更低（<150MB）
- **原生体验**：使用 GTK4 + Libadwaita，与 GNOME/现代 Linux 桌面环保
- **易用性**：提供直观的壁纸浏览、选择与应用界面
- **功能完整性**：逐步对标官方 Electron GUI 的功能

## ✅ 当前功能

### 核心功能
- ✅ **壁纸浏览**：从 Steam Workshop 自动扫描壁纸库
- ✅ **双视图模式**：Grid（网格）与 List（列表）视图切换
- ✅ **侧边栏详情**：显示壁纸大图、标题、类型、标签、描述
- ✅ **壁纸应用**：点击 Apply 按钮或双击卡片直接应用壁纸
- ✅ **随机选择**：I'm feeling lucky 随机应用一张壁纸
- ✅ **快速刷新**：Refresh 按钮即时加载新下载的壁纸（无需重启）
- ✅ **自动应用**：启动时自动应用上次壁纸（读取 config.json 的 lastWallpaper/lastScreen）

### 进程管理
- ✅ **后端调用**：正确使用 `linux-wallpaperengine` 的参数格式
- ✅ **单实例控制**：应用前自动 pkill 旧进程，避免堆叠
- ✅ **参数整数化**：音量严格传递为整数字符串，防止浮点数崩溃

### 壁纸属性编辑（新增 v0.3）
- ✅ **属性自动加载**：调用 `--list-properties` 获取壁纸可编辑属性
- ✅ **动态控件生成**：根据属性类型自动生成对应控件
  - Slider（滑块）：调节数值范围
  - Toggle（开关）：布尔值切换
  - Color（颜色选择）：RGB 颜色选择器
  - Combo（下拉选择）：从预设选项中选择
- ✅ **属性值持久化**：用户修改的属性值保存到配置文件，下次应用时自动恢复
- ✅ **实时应用**：修改属性后立即生效（如果当前正在播放该壁纸）

### 多显示器支持（新增 v0.3）
- ✅ **自动检测屏幕**：使用 `xrandr --query` 自动获取可用显示器列表
- ✅ **下拉选择**：在 Advanced 设置中提供屏幕下拉选择，无需手工输入
- ✅ **屏幕刷新**：Refresh Screens 按钮可重新检测连接的显示器
- ⚠️ **未测试**：由于当前环境仅有一个显示器，功能未实际验证

### 搜索功能（新增 v0.3）
- ✅ **实时搜索**：顶部搜索框支持按关键词实时过滤壁纸
- ✅ **多字段匹配**：搜索范围包括
  - 壁纸标题
  - 描述文本
  - 标签（Tags）
  - 文件夹名称

### 配置管理
- ✅ **设置页面**：General、Audio、Advanced 三大类配置
- ✅ **FPS 限制**：1～144fps 可调
- ✅ **音频控制**：静音/音量 0～100 调节
- ✅ **缩放模式**：default/stretch/fit/fill 四种选项
- ✅ **全屏暂停**：toggle 全屏时暂停壁纸
- ✅ **鼠标禁用**：toggle 禁用鼠标交互
- ✅ **屏幕选择**：Advanced 中手工输入屏幕名（如 eDP-1）
- ✅ **Workshop 路径**：可自定义 Workshop 内容目录

### UI/UX
- ✅ **现代深色主题**：圆角、阴影、悬停效果
- ✅ **窗口约束**：侧边栏固定 320px 宽度，不被图片撑宽
- ✅ **当前壁纸显示**：顶部工具栏显示当前应用的壁纸名称
- ✅ **Stop 按钮**：快速停止当前壁纸播放
- ✅ **后台保活窗口隐藏**：最小化或关闭窗口会隐藏到后台（进程保留，暂无系统托盘图标）

### 后台/CLI 控制（新增 v0.3）
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

## ❌ 尚缺功能（对标 linux-wallpaperengine-gui）

### 优先级 P1（核心缺失）
- ❌ **系统托盘图标**：
  - 目标：在屏幕右上/下角显示托盘图标，可点击显示/隐藏、右键菜单刷新/应用/退出
  - 当前状态：尝试过 pystray 库，但 Wayland/niri 上不兼容（D-Bus 后端无法工作）
  - 方案评估：StatusNotifierItem 在某些 Wayland 桌面环境上不可靠；libnotify 通知栏可用但体验不同
  - **暂时保留 CLI 控制作为替代方案**（`--show/--hide/--toggle/--quit` 等）
- ⚠️ **systemd 用户服务与自启动**：已文档化需求，用户可自行在 niri 配置中加 `exec` 指令

### 优先级 P2（功能缺失）
- ⚠️ **多显示器独立壁纸**：当前仅支持单一屏幕，不支持同时为不同显示器设置不同壁纸（此功能需后端支持）

### 优先级 P3（增强功能）
- ❌ **原始 JSON 编辑**：无原始配置编辑界面
- ❌ **日志面板**：无 Logs 视图查看后端输出

### 优先级 P3（增强功能）
- ❌ **日志面板**：无 Logs 视图
- ❌ **自启动集成**：无 systemd 单元、桌面文件、AUR 打包
- ❌ **动态壁纸预览**：GIF 预览仅显示首帧（性能考虑暂未实现动画）

## 🗺️ 接下来的计划

### Phase 1：稳定化与 Bug 修复（暂缓）
- [ ] 修复 GTK4 兼容性问题（主题、渲染器警告）
- [ ] 优化内存占用，特别是纹理缓存策略
- [ ] 处理边界情况（空壁纸库、损坏 JSON、网络超时等）

### Phase 2：核心功能补全（已完成 ✅）
- [x] **壁纸属性管理**：
  - 在详情侧栏下新增"属性"折叠区
  - 调用 `linux-wallpaperengine --list-properties <id>` 获取可用属性
  - 根据属性类型（slider/toggle/color/combolist）生成动态控件
  - 应用时合成 `--set-property` 参数列表
- ⚠️ **系统托盘图标**（暂缓）：
  - 原计划使用 pystray/StatusNotifier，但 Wayland/niri 兼容性问题
  - 已用 CLI 方案替代（`--show/--hide/--toggle` 等）
  - 可在 X11 桌面重新启用 pystray 后端

### Phase 3：增强体验（部分已完成 ✅）
- [x] **多显示器支持**：自动检测屏幕列表，提供下拉选择而非手工输入
- [x] **搜索功能**：简单的关键词搜索和按标签筛选
- [ ] **快速设置**：右键菜单或快捷键快速调整常用参数

### Phase 4：打包与发布
- [ ] 编写 PKGBUILD（AUR）
- [ ] 生成桌面入口（.desktop）与自启动脚本
- [ ] 撰写完整的安装与使用文档

## 🧭 后台/CLI 控制使用指南

### 启动方式

**前台启动（带 GUI）**：
```bash
python3 wallpaper_gui.py
```

**后台启动（无 GUI，仅保活进程）**：
```bash
python3 wallpaper_gui.py --hidden
# 或
python3 wallpaper_gui.py --minimized
```

### 命令行动作

所有以下命令都会发往**同一运行实例**，避免重复启动：

| 命令 | 效果 | 示例 |
|------|------|------|
| `--show` | 显示窗口（若已运行） | `python3 wallpaper_gui.py --show` |
| `--hide` | 隐藏窗口（进程保持） | `python3 wallpaper_gui.py --hide` |
| `--toggle` | 切换显示/隐藏状态 | `python3 wallpaper_gui.py --toggle` |
| `--refresh` | 重新扫描壁纸库 | `python3 wallpaper_gui.py --refresh` |
| `--apply-last` | 应用上次保存的壁纸 | `python3 wallpaper_gui.py --apply-last` |
| `--quit` | 完全退出应用与进程 | `python3 wallpaper_gui.py --quit` |

### Niri 配置示例

在 `~/.config/niri/config.kdl` 中添加自启动：

```kdl
// 后台启动壁纸引擎 GUI（带自动应用上次壁纸）
exec python3 /home/yua/suw/wallpaper_gui.py --hidden
```

在 niri 运行中，可用快捷键或脚本调用：

```bash
# 显示 GUI 以选择壁纸
python3 wallpaper_gui.py --show

# 快速应用上次壁纸
python3 wallpaper_gui.py --apply-last

# 隐藏回后台
python3 wallpaper_gui.py --hide
```

## 🧭 系统托盘与后台常驻需求（旧文档，暂保留）

为对齐 linux-wallpaperengine-gui 的托盘体验，需要满足以下要求（目前**因 Wayland 兼容性问题暂未实现**，仅文档化约束）：

- **托盘协议**：实现 DBus StatusNotifierItem（AppIndicator 兼容）。GNOME 需安装 appindicator 支持（如 `gir1.2-appindicator3-0.1` 或 `libayatana-appindicator3`）。
- **托盘动作**：
  - 左键：显示/隐藏主窗口
  - 右键菜单：显示/隐藏窗口、Refresh、Apply last wallpaper、Quit
  - 可选中键：快速暂停/继续
- **启动行为**：支持 `--minimized/--hidden` 启动参数或配置项，允许开机自启动时仅托盘驻留。✅ **已实现 CLI 版本**
- **后台守护**：提供 systemd --user 单元，保持 python GUI 在后台运行；若进程退出可重启（`Restart=on-failure`）。⚠️ **用户自行配置 niri exec 替代**
- **显示会话适配**：Wayland/X11 均应工作；确保托盘依赖在 Wayland（GNOME/KDE）上可用。❌ **Wayland 不兼容，已转向 CLI 方案**

## 🛠️ 技术栈

- **语言**：Python 3.10+
- **UI 框架**：PyGObject (GTK4) + Libadwaita
- **后端**：linux-wallpaperengine（C++ 实现）
- **依赖**：
  ```bash
  python3-gi gir1.2-gtk-4.0 gir1.2-adw-1
  ```

## 🚀 快速开始

```bash
# 安装依赖
sudo apt-get install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1

# 运行
python3 wallpaper_gui.py
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
  "lastScreen": "eDP-1"
}
```

## 🤝 贡献

欢迎提交 Issue 与 PR！特别是以下方面：
- 新功能实现（属性编辑、多显示器支持等）
- Bug 修复与性能优化
- 翻译与文档改进

## 📄 许可证

MIT License

---

**最后更新**：2026-01-22
**版本**：0.4-beta（壁纸属性编辑实时应用、CLI --toggle 修复）
