基于 `settings.py` 的完整代码分析，结合我们确定的 **“4 组黄金方案”**（播放与性能、音频与显示、系统与工具、日志监控），以下是重新整理后的详细功能清单。

这份清单包含了**分组名称**、**下辖的具体设置项**、**对应的代码变量/函数**、**控件类型**、**默认值**、**取值范围**以及**核心功能逻辑**。

---

### 1. 🎬 播放与性能 (Playback & Performance)

> **对应原代码函数**: `build_general()`
> **核心目标**: 控制壁纸如何渲染、如何交互以及如何自动循环。

| 设置项 (中文/英文)                       | 代码变量/Key            | 控件类型          | 默认值    | 范围/选项                                            | 功能逻辑描述                                                                                        |
| :--------------------------------------- | :---------------------- | :---------------- | :-------- | :--------------------------------------------------- | :-------------------------------------------------------------------------------------------------- |
| **壁纸昵称管理**Wallpaper Nicknames      | `nickname_manager`      | Button (`Manage`) | -         | -                                                    | 打开 `NicknameManagerDialog`。保存后若需刷新库则调用 `app.refresh_from_cli()`，否则仅刷新 UI 网格。 |
| **帧率限制**FPS Limit                    | `fps`                   | SpinButton        | `30`      | `1` - `144`                                          | 限制壁纸渲染的最大帧率，平衡画质与 GPU 占用。                                                       |
| **缩放模式**Scaling Mode                 | `scaling`               | DropDown          | `default` | `default`, `stretch`, `fit`, `fill`                  | 控制壁纸在屏幕上的适配方式（拉伸、适应、填充等）。                                                  |
| **全屏不暂停**No Fullscreen Pause        | `noFullscreenPause`     | Switch            | `False`   | Boolean                                              | 启用后，即使检测到全屏应用，壁纸也不会暂停渲染。                                                    |
| **禁用鼠标交互**Disable Mouse            | `disableMouse`          | Switch            | `False`   | Boolean                                              | 忽略所有鼠标点击和悬停事件，壁纸变为纯背景。                                                        |
| **禁用视差效果**Disable Parallax         | `disableParallax`       | Switch            | `False`   | Boolean                                              | 关闭随鼠标移动产生的背景位移特效。                                                                  |
| **禁用粒子效果**Disable Particles        | `disableParticles`      | Switch            | `False`   | Boolean                                              | 关闭火焰、雨水等粒子系统以节省 CPU/GPU。                                                            |
| **纹理夹持模式**Clamping Mode            | `clamping`              | DropDown          | `clamp`   | `clamp`, `border`, `repeat`                          | 控制纹理超出边界时的处理方式（夹紧、边框、重复）。                                                  |
| **启用自动循环**Enable Cycling           | `cycleEnabled`          | Switch            | `False`   | Boolean                                              | 开启后按设定间隔自动切换壁纸。                                                                      |
| **循环间隔**Cycle Interval               | `cycleInterval`         | SpinButton        | `15`      | `1` - `1440` (分钟)                                  | 设置两次切换之间的等待时间。                                                                        |
| **循环排序规则**Cycle Order              | `cycleOrder`            | DropDown          | `random`  | `random`, `title`, `size`, `size_desc`, `type`, `id` | 决定切换顺序。UI 显示为 "Size ↑/↓"，保存时映射为 `size`/`size_desc`。                               |
| **Wayland 会话检测**Session Check        | `XDG_SESSION_TYPE`      | Label (Read-only) | -         | Wayland / X11                                        | 检测当前环境。若是 X11，下方 Wayland 特有选项会被禁用 (`set_sensitive(False)`)。                    |
| **仅在活动时暂停**Pause Only When Active | `wayland_only_active`   | Switch            | `False`   | Boolean                                              | **(Wayland Only)** 仅当全屏窗口获得焦点时才暂停壁纸。                                               |
| **忽略应用 ID**Ignore App IDs            | `wayland_ignore_appids` | Entry             | `""`      | 文本 (逗号分隔)                                      | **(Wayland Only)** 输入如 `dock,bar` 等 ID，使其不被视为全屏窗口从而触发暂停。                      |

---

### 2. 🔊 音频与显示 (Audio & Display)

> **对应原代码函数**: `build_audio()` + `build_advanced()` (部分)
> **核心目标**: 管理声音输出和屏幕选择。

| 设置项 (中文/英文)                       | 代码变量/Key        | 控件类型   | 默认值     | 范围/选项   | 功能逻辑描述                                                                              |
| :--------------------------------------- | :------------------ | :--------- | :--------- | :---------- | :---------------------------------------------------------------------------------------- |
| **静音壁纸**Silence Wallpaper            | `silence`           | Switch     | **`True`** | Boolean     | **默认开启**。完全关闭壁纸音频输出。                                                      |
| **主音量**Volume                         | `volume`            | SpinButton | `50`       | `0` - `100` | 控制壁纸音量大小。                                                                        |
| **禁用自动静音**Disable Auto Mute        | `noautomute`        | Switch     | `False`    | Boolean     | 防止当其他应用（如浏览器）播放声音时，壁纸自动静音。                                      |
| **禁用音频处理**Disable Audio Processing | `noAudioProcessing` | Switch     | `False`    | Boolean     | 关闭频谱分析功能，降低 CPU 占用。                                                         |
| **刷新屏幕列表**Refresh Screens          | -                   | Button     | -          | -           | 调用 `screen_manager.detect_screens()` 重新扫描显示器并更新下拉列表，尝试保留当前选中项。 |

---

### 3. ⚙️ 系统与工具 (System & Tools)

> **对应原代码函数**: `build_advanced()` (剩余部分)
> **核心目标**: 路径配置、系统集成及截图辅助工具。

| 设置项 (中文/英文)                    | 代码变量/Key      | 控件类型           | 默认值          | 范围/选项           | 功能逻辑描述                                                                             |
| :------------------------------------ | :---------------- | :----------------- | :-------------- | :------------------ | :--------------------------------------------------------------------------------------- |
| **Workshop 目录**Workshop Directory   | `workshopPath`    | Entry + Browse Btn | `WORKSHOP_PATH` | 文件夹路径          | 指定 Steam 创意工坊路径。**保存时若路径变化，立即触发 `wp_manager.scan()` 热更新**。     |
| **Assets 目录**Assets Directory       | `assetsPath`      | Entry + Browse Btn | `None` (Auto)   | 文件夹路径          | 指定资源文件夹。若留空，保存为 `None`，程序将尝试自动检测。                              |
| **创建桌面快捷方式**Desktop Shortcut  | -                 | Button (`Create`)  | -               | -                   | 调用 `integrator.create_desktop_entry()`。成功/失败均显示 Toast 提示。                   |
| **开机自启**Run on Startup            | -                 | Switch             | 系统状态        | Boolean             | 同步 `integrator.is_autostart_enabled()` 状态。保存时调用 `integrator.set_autostart()`。 |
| **启动时最小化**Start Hidden          | -                 | Switch             | **`True`**      | Boolean             | **硬编码默认为 True**。控制启动时是否直接隐藏到系统托盘。                                |
| **截图延迟**Screenshot Delay          | `screenshotDelay` | SpinButton         | `20`            | `1` - `600` (帧)    | 截图前等待的帧数，用于等待网页壁纸加载完成。                                             |
| **截图分辨率**Screenshot Resolution   | `screenshotRes`   | Entry              | `3840x2160`     | 文本 (如 1920x1080) | 设置截图的目标分辨率。                                                                   |
| **捕获后端检测**Capture Backend       | -                 | Label (Read-only)  | -               | 已安装/未安装       | 启动时检测 `shutil.which("xvfb-run")`。显示 🟢 (Silent Mode) 或 ⚪ (Window Mode)。       |
| **优先静默捕获**Prefer Silent Capture | `preferXvfb`      | Switch             | `True`          | Boolean             | 启用 `xvfb-run` 进行后台截图。**若未检测到 xvfb，此开关被禁用并显示 Tooltip**。          |

---

### 4. 📜 日志监控 (Logs)

> **对应原代码函数**: `build_logs()`
> **核心目标**: 独立的调试中心，实时查看、过滤和操作日志。

| 设置项 (中文/英文)       | 代码变量/Key     | 控件类型             | 默认值 | 范围/选项                            | 功能逻辑描述                                                                                                                         |
| :----------------------- | :--------------- | :------------------- | :----- | :----------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| **日志过滤器**Log Filter | `current_filter` | DropDown             | `All`  | `All`, `Controller`, `Engine`, `GUI` | 过滤显示来源。**特殊逻辑**: 选 "GUI" 时显式排除 "Controller" 和 "Engine" 日志。                                                      |
| **日志视图**Log View     | `log_view`       | TextView (Monospace) | -      | 只读文本                             | 实时追加日志。支持颜色标记：• Time: `#6b7280`• Info: `#3b82f6`• Warn: `#f59e0b`• Error: `#ef4444`• Source: `#a855f7`• Msg: `#e5e7eb` |
| **清除日志**Clear Logs   | -                | Button               | -      | -                                    | 调用 `log_manager.clear()` 并清空视图。                                                                                              |
| **复制日志**Copy Logs    | -                | Button               | -      | -                                    | 复制全部文本到剪贴板。按钮文字暂时变为 "Copied!" (2秒后恢复)。                                                                       |
| **手动刷新**Refresh      | -                | Button               | -      | -                                    | 重新从 `log_manager` 拉取日志并渲染。                                                                                                |
| **实时回调**Log Callback | -                | Internal Signal      | -      | -                                    | 通过 `log_manager.register_callback(self.on_log_update)` 实现日志实时上屏。                                                          |

---

### 💡 底部全局操作栏 (Global Actions)

位于侧边栏底部，对所有分组生效：

1.  **Save Changes**: 收集所有上述配置写入 `config`，触发热更新逻辑，显示 Toast。
2.  **Reload Wallpapers**: 调用 `controller.restart_wallpapers()` 重启渲染。
3.  **Stop Wallpaper**: 调用 `app.stop_wallpaper()` 停止壁纸。

这个结构既保留了所有代码细节，又符合用户直觉，解决了原来 `Advanced` 页面杂乱的问题，同时让日志拥有了独立的“大屏”空间。

侧栏：

```
+-----------------------+
|  🎬 Playback & Perf   |  <-- 最常用，调整画质和循环
+-----------------------+
|  🔊 Audio & Display   |  <-- 调整声音和屏幕
+-----------------------+
|  ⚙️ System & Tools    |  <-- 配置路径、自启、截图
+-----------------------+
|  📜 Logs              |  <-- 独立的大块区域，查错专用
+-----------------------+
|                       |
|   [ Save Changes ]    |
|   [ Reload Wallpaper ]|
|   [ Stop Wallpaper ]  |
+-----------------------+
```
