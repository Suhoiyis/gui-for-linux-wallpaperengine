# 壁纸兼容性说明

本文档详细说明 Linux Wallpaper Engine GUI 在不同环境下的兼容性和限制。

## 后端架构说明

本 GUI 依赖 `linux-wallpaperengine` C++ 后端进行渲染。该后端通过逆向工程实现（非官方移植），且 Linux 图形栈（特别是 Wayland）与 Windows 存在本质差异，因此部分壁纸可能无法完美显示。

## 壁纸类型兼容性

### ✅ Video 壁纸 (.mp4, .webm)

**兼容性**：完美支持

**说明**：
- 视频解码使用成熟的 FFmpeg/GStreamer 库
- 支持循环播放、音量控制
- 性能最优，资源占用最低
- **推荐优先使用 Video 类型壁纸**

**测试环境**：
- ✅ X11 (GNOME/KDE)
- ✅ Wayland (Niri/Sway/Hyprland)

---

### ⚠️ Web 壁纸 (.html)

**兼容性**：部分支持

**可用功能**：
- ✅ 基本渲染：能够显示网页内容和动画
- ✅ JavaScript 执行：动态效果正常运行
- ✅ 音频播放：背景音乐可以播放（受音量控制）

**已知问题**：
- ❌ **属性调整完全失效**：由于 C++ 后端在 Linux/Wayland 环境下的 CEF（Chromium Embedded Framework）通信限制，**无法通过 GUI/CLI 动态调整 Web 壁纸属性**
  - 例如：语言切换、音乐开关、颜色选择、实时数值变化等
  - 所有在 Windows 版本中可调整的属性在 Linux 下基本处于失效状态
  - 壁纸将以默认属性值运行

**技术原因**：
1. CEF 的 IPC（进程间通信）在 Linux 下与 Windows 实现不同
2. 后端尝试注入 JavaScript 来修改 `window.wallpaperPropertyListener` 时常因环境不匹配或时机问题静默失败
3. Wayland 的安全隔离机制进一步限制了跨进程通信

**解决方案**：
- 如需修改 Web 壁纸属性，可尝试手动编辑壁纸的 `project.json` 或 HTML 源文件（需要一定技术能力）
- 优先选择属性少或默认配置即可满足需求的 Web 壁纸

---

### ⚠️ Scene 壁纸 (.pkg)

**兼容性**：有限支持

**可用功能**：
- ✅ 简单 2D/3D 场景：基础模型、纹理、光照
- ✅ 基本动画：时间轴动画、相机运动
- ⚠️ 基础粒子系统：简单粒子可能正常

**已知问题**：
- ❌ **复杂粒子系统失效**：包含高级粒子特效的壁纸可能只显示静态场景
  - 症状：日志显示 `Particle system loaded` 但屏幕上看不到粒子效果
  - 原因：粒子系统依赖 Windows 特定的 DirectX API，OpenGL 转换可能不完整
  
- ❌ **自定义着色器失效或花屏**：使用 HLSL（DirectX 着色器语言）的壁纸可能出现：
  - 部分效果缺失
  - 画面撕裂或花屏
  - 完全无法渲染（黑屏）
  - 原因：HLSL 到 GLSL 的自动转换不完全支持所有语法特性

- ❌ **复杂脚本逻辑**：依赖 Windows 特定 API 的交互脚本无法执行

**推荐做法**：
- 下载前查看 Workshop 评论，寻找 Linux 用户的反馈
- 优先选择标注"简单"、"低配"的 Scene 壁纸
- 避免选择描述中提到大量粒子效果或高级着色器的壁纸

---

## Wayland 环境特别说明

如果您在使用 Wayland 混成器（Niri/Hyprland/Sway/GNOME Wayland），需要注意以下限制：

### ❌ 鼠标交互完全失效

**问题**：
- 鼠标拖尾（Mouse Trails）效果无法显示
- 点击互动（如点击切换场景、拖动物体）无法响应

**原因**：
- Wayland 的安全隔离机制要求应用必须获得焦点才能读取鼠标位置
- 作为壁纸层（Background Layer）运行的应用通常无法获取全局鼠标坐标
- 即使在窗口模式下，部分依赖 Windows 特定 API（`GetCursorPos`）的交互脚本也无法工作

**无解决方案**：这是架构层面的限制

---

### ⚠️ OpenGL/GLX 兼容性问题

**症状**：
- 日志中出现 `Failed to initialize GLEW: No GLX display`
- 部分特效渲染层级异常（如粒子显示在模型前面）
- Web 属性注入更容易失败

**原因**：
- 部分旧式特效依赖 GLX（X11 的 OpenGL 扩展）
- 纯 Wayland 环境下没有 GLX，只有 EGL

**解决方案**：
- 确保安装 `xorg-xwayland`（大多数发行版默认已安装）
- 在启动参数中尝试添加环境变量（实验性）：
  ```bash
  GDK_BACKEND=x11 python3 run_gui.py
  ```

---

### ❌ Web 交互通信受限

**问题**：
- Web 壁纸的属性注入成功率更低
- CEF 渲染偶尔出现黑屏或闪烁

**原因**：
- CEF 对 Wayland 的支持仍不成熟（依赖 Ozone 层）
- 跨进程通信的时序问题在 Wayland 下更严重

**缓解方法**：
- 在 Settings > Advanced 中禁用"禁用鼠标交互"（虽然无法交互，但保留鼠标支持可能提升 CEF 稳定性）
- 使用视频壁纸代替 Web 壁纸

---

## X11 环境兼容性

**总体**：X11 环境兼容性优于 Wayland

**已知问题**：
- ⚠️ 部分桌面环境（如 XFCE/LXDE）可能无法正确设置壁纸层级
- ⚠️ 使用混成器（Compton/Picom）时可能出现撕裂

**推荐桌面环境**：
- ✅ GNOME (X11)
- ✅ KDE Plasma (X11)
- ⚠️ i3/bspwm（需手动配置窗口规则）

---

## 硬件兼容性

### GPU 要求

**最低**：
- 支持 OpenGL 3.3 的显卡
- 集成显卡（Intel HD 4000+）可运行简单壁纸

**推荐**：
- 独立显卡（NVIDIA/AMD）
- OpenGL 4.5+ 支持

### 驱动问题

**NVIDIA**：
- ✅ 专有驱动（推荐）：兼容性最佳
- ⚠️ Nouveau 开源驱动：性能差，复杂场景可能卡顿

**AMD**：
- ✅ AMDGPU 驱动（Mesa）：现代显卡支持良好
- ⚠️ 旧显卡可能缺少部分 OpenGL 扩展

**Intel**：
- ✅ Mesa 驱动：集成显卡支持基本功能
- ⚠️ 复杂 Scene 壁纸可能性能不足

---

## 多显示器兼容性

**当前状态**：Beta 支持

**已知问题**：
- ⚠️ 屏幕断开连接后需要手动停止对应壁纸（GUI 会自动清理配置）
- ⚠️ 不同刷新率的显示器可能导致 FPS 不一致
- ⚠️ 旋转屏幕（竖屏）的壁纸缩放可能异常

---

## 性能与内存

### 预期资源占用

| 壁纸类型 | 内存占用 | CPU 占用 (30fps) | GPU 占用 |
|---------|---------|-----------------|---------|
| Video (1080p) | ~100MB | 5-10% | 低 |
| Web (简单) | ~200MB | 10-20% | 低-中 |
| Scene (简单) | ~150MB | 10-15% | 中 |
| Scene (复杂) | ~300MB | 20-40% | 高 |

### 已知内存泄漏

**症状**：
- 长期运行（8 小时以上）Web 壁纸可能导致内存缓慢增长
- 最终占用可能达到 500MB - 1GB

**原因**：
- 可能源于 CEF（Chromium 引擎）的内存管理问题
- 也可能是 C++ 后端或 Python 绑定的泄漏

**临时解决方案**：
- 在 Settings > Automation 中启用"定时轮换"，强制定期重启后端
- 使用系统 crontab 定期执行 `python3 run_gui.py --stop && python3 run_gui.py --apply-last`
- 避免长期使用复杂 Web 壁纸

---

## 测试环境

本项目主要在以下环境下开发和测试：

**主要测试环境**：
- 发行版：Arch Linux
- 窗口管理器：Niri (Wayland)
- GPU:Intel Irix Xe

**有限测试**：
- GNOME (Wayland/X11) ~计划中~


**未测试**：
- Ubuntu/Debian 系统
- 其他 Wayland 合成器（如 River/Labwc）
- 其他桌面环境（如 XFCE/Cinnamon）

如果您在其他环境下遇到问题，欢迎提交 Issue 并附上详细环境信息。

---

## 获取帮助

如遇到兼容性问题，请提供以下信息：

1. 发行版和版本（`cat /etc/os-release`）
2. 桌面环境/窗口管理器
3. 显示服务器（X11/Wayland）
4. GPU 和驱动版本（`glxinfo | grep OpenGL`）
5. 壁纸 ID 和类型
6. 日志输出（Settings > Logs 页面）

在 GitHub Issues 中提交问题：[项目 Issues 页面]
