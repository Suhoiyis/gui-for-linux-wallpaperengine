# 🐛 常见后端日志与故障排查

本文档记录了 `linux-wallpaperengine` 后端常见的日志错误及其含义，帮助高级用户判断问题根源。

## 1. Wayland / OpenGL 相关

### `Failed to initialize GLEW: No GLX display`
- **现象**：壁纸能运行，但部分特效（如粒子、音频波形）不可见，或者控制台刷屏报错。
- **原因**：后端使用的 GLEW 库试图初始化 X11 的 GLX 扩展，但在纯 Wayland 环境下失败。虽然程序通常会回退到 EGL，但这可能导致某些高级渲染特性（混合模式、透明度）失效。
- **影响**：Scene 类型壁纸的复杂特效可能无法渲染。

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
