# 🐛 常见后端日志与故障排查

本文档记录了 `linux-wallpaperengine` 后端常见的日志错误及其含义，帮助高级用户判断问题根源。

## 1. Wayland / OpenGL 相关

### `Failed to initialize GLEW: No GLX display`
- **现象**：
  1. 壁纸能运行，但部分特效（如粒子、音频波形）不可见。
  2. **Web 壁纸属性失效**：通过 GUI 或 CLI 设置属性（如 `language=chinese`）后，日志显示 `Applying override value`，但画面完全无变化。
- **原因**：后端硬编码依赖 X11 的 GLX 扩展。在纯 Wayland 环境下，OpenGL 环境初始化不完整，导致 Chromium (CEF) 的 JavaScript 注入接口（用于修改网页属性）静默失效。
- **影响**：
  - **Scene 类型**：复杂特效无法渲染。
  - **Web 类型**：**交互功能完全瘫痪**，无法动态调整任何壁纸属性。

## 2. Web 壁纸特有错误

### 日志显示 `Applying override value` 但界面没动
- **现象**：在终端运行 `linux-wallpaperengine <ID> --set-property key=value`，看到应用成功的日志，但壁纸依然显示默认状态。
- **根本原因**：
  1. **环境缺失**：参考上文的 `GLX display` 错误，渲染上下文异常导致后端无法通过 `ExecuteJavaScript` 与网页通信。
  2. **初始化时机**：部分壁纸将属性监听器注册在 `DOMContentLoaded` 事件中，而后端注入属性的时机过早，导致指令在网页准备好之前就已丢失。
  3. **SSL 报错**：日志中若出现 `handshake failed ... net_error -101`，说明网页依赖的外部资源（如 CDN 脚本）加载失败，可能阻塞了属性监听器的初始化。
- **结论**：这是后端（C++ 移植版）在 Linux 环境下的架构缺陷，目前在 Wayland 下基本无法通过正常手段解决。

### `GLFW error 65548: Wayland: The platform does not support setting the window position`
- **现象**：日志中出现此错误。
- **原因**：GLFW 试图在 Wayland 下强制设置窗口坐标，但 Wayland 协议禁止客户端自定位置（由混成器管理）。
- **影响**：通常无害，但在某些情况下可能暗示窗口未能正确全屏或获取输入焦点。

## 2. 资源加载相关

### `Particle '...' max particles: ...` 但屏幕无显示
- **现象**：日志显示粒子系统已加载（如 `Particle 'Getsuga Tenshou Mouse Trail'...`），纹理也找到了，但屏幕上什么都没有。
- **原因**：
  1. **输入丢失**：粒子发射器依赖鼠标位置，但在 Wayland 下获取不到全局鼠标坐标 (0,0)，导致粒子从未发射。
  2. **渲染层级错误**：粒子被渲染到了背景图层之下（Z-fighting 或混合模式错误）。

### `Cannot find a valid assets folder`
- **现象**：启动失败，提示找不到 assets。
- **解决**：确保你已安装 Steam 版 Wallpaper Engine，或者手动将 `assets` 文件夹复制到 `linux-wallpaperengine` 同级目录。
