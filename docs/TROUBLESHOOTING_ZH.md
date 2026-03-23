[English](TROUBLESHOOTING.md)

# 🐛 故障排除指南 (Tauri v2.0.0)

本指南旨在帮助您解决 LWG (Linux Wallpaper Engine) GUI 及其后端常见的各种问题。

## 常见问题

本节涵盖了用户最常遇到的问题。

- **壁纸未显示**：请确保已安装 `linux-wallpaperengine` 且 Assets 路径设置正确。
- **系统托盘图标缺失**：检查您的桌面环境是否支持 AppIndicators（请参阅系统托盘章节）。
- **多显示器同步**：使用“链接/独立”按钮来同时控制所有屏幕。
- **Wayland 性能问题**：如果壁纸出现卡顿，请尝试在设置中降低帧率限制 (FPS limit)。

---

## 1. 常见安装问题

### 后端要求
GUI 仅作为一个控制器，需要安装核心渲染引擎才能正常工作。
- **问题**：“壁纸引擎启动失败”或“找不到命令”。
- **解决方案**：确保已安装 `linux-wallpaperengine` 并且其路径已包含在您的 `PATH` 环境变量中。
  - Arch Linux: `yay -S linux-wallpaperengine`
  - 其他发行版：请从 [Almamu/linux-wallpaperengine](https://github.com/Almamu/linux-wallpaperengine) 源码构建。

### 系统依赖
- **Tauri 运行时**：需要 `webkit2gtk`。大多数发行版都已包含此组件，但如果 GUI 无法启动，请确保已安装。
- **显示器检测**：本应用使用以下工具链来检测显示器：
  1. `xrandr` (X11)
  2. `wlr-randr` (Wayland/wlroots)
  3. `kscreen-doctor` (KDE Plasma)
  如果您的显示器未显示，请确保已安装适用于您环境的相应工具。

### 路径配置
- **Workshop 路径**：必须指向 Steam Workshop 文件夹（通常以 `431960` 结尾）。
- **Assets 路径**：必须指向 `linux-wallpaperengine` 的 `assets` 文件夹。
- **修复方法**：前往 **设置 > 系统与工具** 验证并更新这些路径。

---

## 2. 壁纸无法播放

### 查看日志
如果壁纸启动失败，第一步通常是查看日志。
1. 打开 **设置 > 日志监控**。
2. 寻找红色的 `ERROR` 条目。
3. 常见错误：
   - `Failed to initialize GLEW`：OpenGL/GLX 环境问题。
   - `Cannot find a valid assets folder`：设置中的 Assets 路径不正确。
   - `Process exited immediately`：后端崩溃；请检查 `Engine` 来源的日志以获取详细信息。

### 损坏的壁纸
- **现象**：部分壁纸可以加载，而另一些不行。
- **解决方案**：右键点击壁纸并选择“在文件管理器中打开”。检查 `project.json` 是否存在且有效。您可能需要在 Steam 上重新订阅该壁纸。

---

## 3. 系统托盘图标未显示

系统托盘的实现取决于您的桌面环境对 StatusNotifierItem (SNI) 的支持。

- **GNOME**：安装 **"AppIndicator and KStatusNotifierItem Support"** 扩展。
- **KDE Plasma**：通常开箱即用。
- **Waybar (Sway/Hyprland)**：确保您的 Waybar 配置中包含了 `tray` 模块。
- **i3/其他窗口管理器**：确保您正在运行系统托盘管理器（如 `nm-applet` 或 `pasystray`）。

---

## 4. 多显示器问题

### 独立壁纸
- **操作方法**：从顶栏的下拉菜单中选择目标显示器，然后应用壁纸。
- **链接/独立**：使用 🔗 图标在“所有屏幕使用相同壁纸”和“每个屏幕使用不同壁纸”之间切换。

### 屏幕名称不匹配
- **问题**：重启或重新连接显示器后，壁纸无法恢复。
- **原因**：如果您的操作系统更改了接口名称（例如从 `HDMI-A-1` 变为 `HDMI-A-2`），保存在 `state.json` 中的状态将无法匹配。
- **解决方案**：为新的屏幕名称重新应用壁纸。

---

## 5. Wayland 特定问题

### 协议限制
Wayland 的安全模型引入了一些限制：
- **无鼠标交互**：无法获取全局鼠标坐标。壁纸中的鼠标轨迹、视差效果和点击交互将无法工作。
- **无“主”显示器**：与 X11 不同，Wayland 合成器通常不会以命令行工具可以一致报告的方式定义“主”显示器。
- **Web 属性注入**：由于 GLX/OpenGL 上下文问题，CEF (Chromium) 属性注入在 Wayland 上经常失败。您可能需要手动编辑 `project.json` 来更改壁纸设置。

### 无害的日志错误
- `GLFW error 65548: Wayland: The platform does not support setting the window position`：这是协议限制，可以安全地忽略。

### Wayland 调整
在 **设置 > 播放与性能** 中，您可以找到 Wayland 特定的选项：
- **仅活动时暂停**：仅当*当前聚焦*的窗口全屏时才暂停壁纸。
- **忽略应用 ID**：防止特定应用（如 dock 或状态栏）触发自动暂停逻辑。

---

## 6. 日志收集方法

报告错误时，提供日志至关重要。

### 使用日志监控
1. 前往 **设置 > 日志监控**。
2. 使用 **过滤器** 下拉菜单来隔离问题：
   - `GUI`：界面或 Tauri 后端的问题。
   - `Engine`：`linux-wallpaperengine` 进程的问题。
   - `Controller`：壁纸管理逻辑的问题。
   - `Core`：内部库错误。
3. 点击 **复制** 将过滤后的日志复制到剪贴板。

### 深度调试
如果 GUI 完全无法打开，请从终端运行它以查看 `stderr` 输出：
```bash
# 如果使用二进制文件
./linux-wallpaperengine-gui

# 如果从源码运行
npm run tauri dev
```
检查终端输出中是否有任何 Rust panic 或 JavaScript 错误。
