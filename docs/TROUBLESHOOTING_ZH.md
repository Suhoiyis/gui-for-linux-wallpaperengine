<a href="TROUBLESHOOTING.md">English</a> | <strong>中文</strong>

# 🐛 故障排除指南 (Tauri v2.0.0)

本指南旨在帮助您解决 LWG (Linux Wallpaper Engine) GUI 及其后端常见的各种问题。

## 常见问题

本节涵盖了用户最常遇到的问题。

- **壁纸未显示**：请确保已安装 `linux-wallpaperengine` 且 Assets 路径设置正确。
- **系统托盘图标缺失**：检查您的桌面环境是否支持 AppIndicators（请参阅系统托盘章节）。
- **多显示器**：使用顶栏的屏幕下拉菜单选择特定显示器或"All Screens"。
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
- **显示器检测**：应用直接读取 `/sys/class/drm` 来检测连接的显示器，无需外部工具。

### 路径配置

- **Workshop 路径**：必须指向 Steam Workshop 文件夹（通常以 `431960` 结尾）。
- **Assets 路径**：必须指向 `Wallpaper Engine` 的 `assets` 文件夹。
- **修复方法**：前往 **设置 > 系统** 验证并更新这些路径。

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
- **所有屏幕**：从下拉菜单中选择"All Screens"可将同一壁纸应用于所有显示器。

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

在 **设置 > 播放** 中，您可以找到 Wayland 特定的选项：

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

---

## 7. Toast 通知含义

GUI 使用 toast 通知提供即时错误反馈，无需查看日志。

### Workshop/Assets 路径错误

| Toast 消息 | 原因 | 解决方案 |
| --------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------ |
| `⚠️ Workshop path does not exist` | 配置的 Workshop 目录无法访问 | 验证路径或使用浏览按钮选择正确的 `431960` 文件夹 |
| `⚠️ Assets path does not exist` | 配置的 Assets 目录无法访问 | 在设置中选择正确的 `wallpaper_engine/assets` 文件夹 |
| `⚠️ Workshop directory not found` | 路径不正确或未安装 Steam | 在设置中选择正确的 Steam Workshop 路径 |

### 壁纸扫描错误

| Toast 消息 | 原因 | 解决方案 |
| ---------------------------------- | ------------------------------ | -------------------------------------------- |
| `⚠️ No wallpapers found` | 目录存在但为空 | 确保已通过 Steam 下载壁纸 |
| `⚠️ X wallpaper(s) failed to load` | `project.json` 文件损坏 | 在 Steam 上重新订阅或验证完整性 |

### 后端启动错误

| Toast 消息 | 原因 | 解决方案 |
| -------------------------------------- | ---------------------------- | ------------------------------------------------ |
| `❌ Wallpaper engine failed to start` | 后端进程崩溃 | 检查设置 → 日志以获取详细错误 |
| `❌ Failed to start engine: [message]` | 启动后端时发生致命错误 | 根据具体错误信息进行排查 |

---

## 8. 引擎日志分析

### 截图很慢（5-10 秒）

- **现象**：截图需要几秒钟才能完成。
- **原因**：如果安装了 `xvfb`，应用会使用 **CPU 软件渲染**进行静默 4K 截图。
- **优点**：无窗口弹出；无论屏幕分辨率如何都能保证一致的 4K 质量。
- **注意**：这是正常行为，请耐心等待。

### `Failed to initialize GLEW: No GLX display`

- **现象**：
  1. 壁纸运行但某些效果（粒子、音频波形）不可见
  2. Web 壁纸属性无法应用，尽管日志显示 `Applying override value`
- **原因**：后端硬编码依赖 X11 的 GLX 扩展。在纯 Wayland 环境中，OpenGL 初始化不完整。
- **影响**：
  - **Scene 类型**：复杂效果无法渲染
  - **Web 类型**：交互功能完全失效

### `Cannot find a valid assets folder`

- **现象**：启动失败并显示 assets 未找到消息。
- **解决方案**：确保已安装 Steam 版 Wallpaper Engine，或手动复制 `assets` 文件夹。

---

## 9. Web 壁纸特定错误

### 属性无法应用尽管日志显示成功

- **现象**：日志显示 `--set-property` 命令成功，但壁纸未更改。
- **根本原因**：
  1. **环境缺失**：GLX display 错误阻止 `ExecuteJavaScript` 通信
  2. **初始化时机**：属性在 `DOMContentLoaded` 事件之前注入
  3. **SSL 错误**：外部资源（CDN 脚本）加载失败（`handshake failed ... net_error -101`）

### 变通方法

手动编辑壁纸的 `project.json` 或 HTML 源文件来更改默认设置。

---

## 10. 设置限制

### `禁用自动静音` 无效

- **现象**：其他应用播放声音时壁纸仍然静音。
- **原因**：在 Wayland 下，PipeWire/Portal 安全机制可能阻止后端检测全局音频流。

### `禁用粒子效果` 无视觉变化

- **原因**：如果粒子已经因 GLX 错误无法渲染，此开关不会产生额外效果。
- **建议**：仅在 X11 或已知粒子系统正常工作的壁纸上测试。

### `GLFW error 65548: Wayland: Window position`

- **含义**：GLFW 尝试设置窗口坐标，但 Wayland 协议禁止客户端设置自己的位置。
- **影响**：通常无害；某些情况下可能表示窗口焦点问题。

---

## 11. 资源加载问题

### 粒子已加载但不可见

- **现象**：日志显示 `Particle '...' max particles: ...` 但屏幕上什么都没有。
- **原因**：
  1. **输入丢失**：粒子发射器依赖鼠标位置，但在 Wayland 下无法获取全局坐标 (0,0)
  2. **渲染层错误**：粒子渲染在背景层下方

### Assets 文件夹未找到

- **现象**：启动时报错 `Cannot find a valid assets folder`。
- **解决方案**：
  - 安装 Steam 版 Wallpaper Engine，或
  - 手动将 `assets` 文件夹复制到 `linux-wallpaperengine` 同目录

---

## 报告错误

提交错误报告时，请包含：

1. **系统信息**：`uname -a` 的输出
2. **桌面环境**：GNOME、KDE、Hyprland 等
3. **显示服务器**：X11 或 Wayland
4. **日志**：从设置 → 日志 → 复制
5. **壁纸详情**：ID 和类型（Video/Web/Scene）
6. **复现步骤**：详细步骤

提交到 [GitHub Issues](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues)。
