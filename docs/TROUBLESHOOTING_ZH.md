# 🐛 常见错误与故障排除

[English](TROUBLESHOOTING.md) | [中文](TROUBLESHOOTING_ZH.md)

本文档记录了 GUI 和 `linux-wallpaperengine` 后端的常见错误及其含义。

## 1. GUI 用户提示

### ⚠️ Toast 通知
GUI 现在使用 Toast 通知提供即时错误反馈，无需检查日志：

#### 创意工坊/资源路径相关
- **`⚠️ Workshop path does not exist: /path/to/dir`**
  - **原因**：配置的创意工坊目录不存在或无法访问。
  - **解决方案**：检查路径是否正确，或使用“浏览”按钮选择正确的 `431960` 文件夹。

- **`⚠️ Assets path does not exist: /path/to/assets`**
  - **原因**：配置的资源 (Assets) 目录不存在或无法访问。
  - **解决方案**：检查路径是否正确，或使用“浏览”按钮选择 `wallpaper_engine/assets` 文件夹。

#### 壁纸扫描相关
- **`⚠️ Workshop directory not found: /path/to/workshop`**
  - **原因**：创意工坊目录路径不正确或未安装 Steam。
  - **解决方案**：在“设置”中选择正确的 Steam 创意工坊路径。

- **`⚠️ No wallpapers found in: /path/to/workshop`**
  - **原因**：目录存在但为空，或者不包含有效的壁纸文件夹。
  - **解决方案**：确保已通过 Steam 下载壁纸，或检查是否选择了正确的创意工坊路径。

- **`⚠️ X wallpaper(s) failed to load`**
  - **原因**：某些壁纸的 `project.json` 文件损坏或格式不正确。
  - **解决方案**：在 Steam 中重新订阅或验证这些壁纸的完整性。

#### 后端启动相关
- **`❌ Wallpaper engine failed to start - check logs`**
  - **原因**：`linux-wallpaperengine` 后端启动失败。
  - **解决方案**：检查“设置 > 日志”页面以获取详细的错误信息。

- **`❌ Failed to start engine: [error message]`**
  - **原因**：启动后端进程时发生致命错误。
  - **解决方案**：根据具体的错误消息进行故障排除。

### 查看详细日志
当 Toast 通知提到“check logs”时：

1. **打开日志页面**：设置 → 日志
2. **检查最新错误**：查找红色的 `ERROR` 条目。
3. **常见日志错误**：
   - `Cannot find a valid assets folder` → 资源路径配置错误。
   - `Failed to initialize GLEW` → OpenGL/GLX 环境问题。
   - `Permission denied` → 文件权限不足。
   - `Process exited immediately` → 后端启动失败；请检查详细输出。

---

## 2. 后端日志分析

### 截图速度慢 (5-10 秒)
- **症状**：点击截图后，需要几秒钟才会出现成功通知。
- **原因**：如果系统中安装了 `xvfb`，程序将使用 **CPU 软件渲染**来生成 4K 截图。虽然速度较慢，但此方法可确保：
  1. **无窗口弹出**：完全静默，不会中断您的工作。
  2. **完美 4K**：不受物理屏幕分辨率或平铺窗口管理器布局的限制。
- **建议**：这是正常现象，请耐心等待。

### `Failed to initialize GLEW: No GLX display`
- **症状**：
  1. 壁纸可以运行，但某些效果（如粒子、音频波形）不可见。
  2. **Web 壁纸属性失效**：通过 GUI 或 CLI 设置属性（如 `language=chinese`）后，日志显示 `Applying override value`，但视觉效果保持不变。
- **原因**：后端对 X11 的 GLX 扩展有硬编码依赖。在纯 Wayland 环境中，OpenGL 环境初始化不完整，导致 Chromium (CEF) 的 JavaScript 注入接口（用于修改 Web 属性）静默失败。
- **影响**：
  - **场景类型**：复杂效果无法渲染。
  - **Web 类型**：**交互功能完全瘫痪**，无法动态调整任何壁纸属性。

---

## 3. Web 壁纸特定错误

### 日志显示 `Applying override value` 但界面没有变化
- **症状**：在终端运行 `linux-wallpaperengine <ID> --set-property key=value` 显示成功应用日志，但壁纸仍处于默认状态。
- **根本原因**：
  1. **环境缺失**：参考上文的 `GLX display` 错误；异常的渲染上下文阻止了后端通过 `ExecuteJavaScript` 与网页通信。
  2. **初始化时序**：某些壁纸在 `DOMContentLoaded` 事件中注册属性监听器，而后端注入属性过早，导致命令在页面准备好之前丢失。
  3. **SSL 错误**：如果日志中出现 `handshake failed ... net_error -101`，表示外部资源（如 CDN 脚本）加载失败，这可能会阻止属性监听器的初始化。

---

## 4. 设置环境限制

### “禁用自动静音”无效
- **症状**：启用后，当其他应用播放声音时，壁纸仍然静音，或者该功能完全不起作用。
- **原因**：在 Wayland 下，受 PipeWire/Portal 安全机制限制，后端进程可能无法检测到全局音频流的状态。

### “禁用粒子”没有视觉变化
- **原因**：如果壁纸已经因为 `GLX display` 错误而无法渲染粒子系统，则此开关不会产生额外的视觉差异。
- **建议**：仅在 X11 环境或已知粒子系统能正常显示的壁纸上进行测试。

### “禁用视差” (待验证)
- **状态**：**尚未在具有 3D 效果的场景壁纸上进行充分测试。**
- **预期行为**：此开关应在鼠标移动时停止背景的视差摆动效果。

### “钳位模式” (Clamping Mode) 的作用
- 用于解决非标准分辨率下的边缘拉伸问题。如果壁纸显示正常，建议保持默认的 `clamp` 值。

### `GLFW error 65548: Wayland: The platform does not support setting the window position`
- **症状**：日志中出现此错误。
- **原因**：GLFW 尝试在 Wayland 下强制设置窗口坐标，但 Wayland 协议禁止客户端自行设置位置（由混成器/合成器管理）。
- **影响**：通常无害，但在某些情况下，可能表明窗口未能正确全屏或获得输入焦点。

---

## 5. 资源加载问题

### `Particle '...' max particles: ...` 但屏幕上没有任何内容
- **症状**：日志显示粒子系统已加载（例如 `Particle 'Getsuga Tenshou Mouse Trail'...`）并找到了纹理，但屏幕上没有任何内容。
- **原因**：
  1. **输入丢失**：粒子发射器依赖于鼠标位置，但在 Wayland 下无法获取全局鼠标坐标 (0,0)，因此永远不会发射粒子。
  2. **渲染层级错误**：粒子渲染在背景层之下（深度冲突或混合模式错误）。

### `Cannot find a valid assets folder`
- **症状**：启动失败，提示找不到资源文件夹。
- **解决方案**：确保您已安装 Steam 版本的 Wallpaper Engine，或者手动将 `assets` 文件夹复制到 `linux-wallpaperengine` 所在的目录。
