# lwg-rs 完整审计报告

> 生成日期：2026-02-25  
> 审计范围：`lwg-rs/` 全部 crate，与 `py_GUI/` 逐模块对照  
> **结论：实际完成度约 30-35%，绝大多数 UI 组件是纯框架/占位**

---

## 1. 总体完成度速览

| Crate | 评估完成度 | 备注 |
|-------|-----------|------|
| `lwg-core` | **~70%** | 核心逻辑基本齐全，性能监控除外 |
| `lwg-ipc` | **~90%** | 基本可用 |
| `lwg-ui` | **~25%** | 几乎全是框架/占位，主窗口是计数器 demo |
| `lwg-tray` (in lwg-rs) | **~5%** | 只有 26 行，无任何托盘功能 |

---

## 2. `lwg-core` — 逐文件状态

### ✅ `config.rs` — 完成
- `ConfigManager` / `AppConfig` 实现完整
- 正确处理 `volume=0` 等 falsy-but-valid 值
- 与 Python 版 `config.json` 格式兼容

### ✅ `wallpaper.rs` — 完成
- `Wallpaper` 结构体 + `WallpaperManager`
- Steam Workshop 扫描、`project.json` 解析
- 搜索、排序（title/size/type/id/random）、删除

### ✅ `controller.rs` — 完成
- `WallpaperController`：`apply()` / `apply_to_screens()` / `stop_screen()` / `restart_wallpapers()` / `stop()`
- 完整命令行参数构建（FPS/音量/缩放/静音/鼠标/视差/粒子/Wayland 参数/属性注入）
- `ScreenshotManager`：支持 Xvfb 静默截图

### ✅ `history.rs` — 完成
- 30 条上限、去重、持久化

### ✅ `nickname.rs` — 完成
- CRUD、100 字符限制、`get_display_name()`

### ✅ `properties.rs` — **基本完成（比预期好）**
- 正确调用 `linux-wallpaperengine --list-properties`
- 解析 Slider/Color/Boolean/Options 四种类型
- 有缓存机制、用户属性持久化
- ⚠️ 缺少：解析器对实际输出格式的鲁棒性测试（格式假设可能与真实输出不符）

### ✅ `screen.rs` — **基本完成**
- 支持 xrandr (X11) / wlr-randr (Wayland) / kscreen-doctor (KDE) 三种检测方式
- ⚠️ 缺少：Python 版的 `get_screens()` 返回纯名称列表接口；Rust 版只有 `names()` 方法，但 Python 版还有 `get_primary_screen()` — Rust 版对应的是 `primary().map(|d| d.name.clone())`，需确认接口对齐

### ❌ `performance.rs` — **框架，数据硬编码**
- `get_stats()` 返回 `cpu: 5.0, memory: 50.0`（硬编码示例值）
- Python 版 `PerformanceMonitor` 使用 `psutil` 读取真实进程数据，60秒历史环形缓冲区
- Rust 版虽有 `sysinfo` 依赖，但 **未实际调用**
- **缺少**：真实 CPU/内存读取、每进程独立监控（Frontend/Backend/Tray）、历史环形缓冲区

### ❌ `logger.py` → **Rust 中无对应模块**
- Python 版 `LogManager`：500条上限，4个级别（DEBUG/INFO/WARNING/ERROR），带 source 字段，支持 callback 订阅
- Rust 中使用 `tracing` crate 输出到 stderr，但没有专门的 `LogManager` 结构体
- **Settings 页的日志查看功能完全无法工作**（没有运行时日志收集 API）

### ❌ `integrations.py` → **Rust 中无对应模块**
- Python 版 `AppIntegrator`：`.desktop` 文件创建/更新、开机自启、应用图标安装（含 RAM 缓存策略）
- **完全缺失**

### ❌ `updater.py` → **Rust 中无对应模块**
- Python 版 `UpdateChecker`：GitHub API 检查、语义版本比较、速率限制处理
- **完全缺失**

---

## 3. `lwg-ipc` — 逐文件状态

### ✅ `protocol.rs` — 完成
- `IpcCommand`（Show/Hide/Toggle/Random/Stop/ApplyLast/Refresh/Quit/Apply）
- `IpcResponse` 枚举

### ✅ `server.rs` — 完成
- Abstract Socket 服务器，`bind_default()` 使用 `lwg-ipc-{uid}`
- 异步 accept loop

### ✅ `client.rs` — 完成（已有使用示例）

---

## 4. `lwg-ui` — 逐文件状态（最关键部分）

### ❌ `app.rs` — **仅 counter demo，必须重写**
- 当前：一个 `counter` 字段，一个 Increment 按钮，窗口标题"Phase 1 完成!"
- 需要：集成所有子组件、三页面 Stack 导航、CSS 加载、图标主题、IPC 服务器启动、托盘启动、session 恢复、CLI 参数处理、cycle timer、onboarding 检查
- Python 版 `app.py` 共 950 行，Rust 版仅 99 行

### ⚠️ `toolbar.rs` — **框架，未连接数据**
- 有搜索框、排序下拉（5个选项）、视图切换按钮的 UI 结构
- **缺少**：连接真实壁纸数据、搜索回调、排序回调、随机/停止按钮功能

### ⚠️ `sidebar.rs` — **部分实现，大量占位**
- 有预览区域布局、标题/类型/大小/描述标签、昵称输入框、应用按钮
- **缺少**：
  - 实际缩略图加载（目前是图标占位）
  - 动态预览（AnimatedPreview 组件集成）
  - 属性编辑（`properties_group` 有框架但内容是占位文字）
  - 屏幕选择器
  - 右键菜单实际触发
  - 昵称输入框的 save 逻辑
  - update() 中不更新任何 Widget（只更新内部状态，Widget 不刷新）

### ❌ `grid_view.rs` — **框架（ListBox 而非 FlowBox，仅示例项）**
- 使用 `ListBox` 而非 `FlowBox`（Python 版是 `FlowBox` 实现真正的网格布局）
- 只有 1 个硬编码示例卡片
- **缺少**：连接 `WallpaperManager` 数据、缩略图加载、双击/右键事件、选中高亮

### ❌ `wallpaper_list.rs` — **refresh_list() 为空 TODO**
- `refresh_list()` 方法体为空

### ❌ `list_view.rs` — **框架（3个硬编码示例行）**
- 3 个硬编码 ListBoxRow，无真实数据绑定

### ⚠️ `navbar.rs` — **框架，屏幕列表硬编码**
- 有汉堡菜单按钮（含 History/About/Quit 菜单项）、历史按钮、屏幕选择器下拉、紧凑模式切换按钮、Link/Unlink 按钮
- 屏幕列表硬编码为 `["eDP-1", "DP-1", "HDMI-1"]`，未连接 `ScreenManager`
- 菜单动作均无回调实现

### ⚠️ `settings_page.rs` — **4个子页面框架，内容极少**
- General 子页：只有一个"开机自启"开关（但功能未实现）
- Audio 子页：空
- Advanced 子页：空
- Logs 子页：空
- Python 版 `settings.py` 共 877 行，Rust 版远未达到

### ⚠️ `performance_page.rs` — **仅 CPU/内存卡片占位**
- 2个 `ProgressBar` 占位（CPU/Memory）
- 无实时数据（依赖 `performance.rs` 的硬编码返回值）
- 无 sparkline 图表
- 无进程详情卡片（Frontend/Backend/Tray）
- Python 版 `performance.py` 共 691 行

### ⚠️ `sparkline.rs` — **降级为 ProgressBar**
- 用 `ProgressBar` 代替 Cairo 绘制的折线图
- Python 版有完整的 60 秒历史 Cairo sparkline，颜色阈值（绿<20%/橙<40%/红≥40%）
- **这是一个视觉上的明显差距**

### ✅ `status_panel.rs` — **相对完整**
- 状态指示器（● 圆点）、当前壁纸名 Label、停止/重新应用按钮
- Widget 直接更新方法存在

### ❌ `history_dialog.rs` — **仅占位文字**
- 显示"历史功能待实现"
- Python 版 `HistoryDialog`：30 条历史列表、缩略图、时间戳、一键回放、清空功能、昵称显示（斜体）

### ❌ `nickname_manager_dialog.rs` — **仅框架**
- `update()` 中 match 为空（所有分支均无操作）
- Python 版 `NicknameManagerDialog`：批量管理昵称、编辑/删除、搜索

### ❌ `animated_preview.rs` — **仅框架**
- 只有一个静态图标占位（`image-x-generic-symbolic`）
- `update()` 中只更新内部状态，不实际加载/播放任何媒体

### ❌ `properties_editor.rs` — **仅框架**
- 固定显示"选择 Web 壁纸后显示属性编辑器"占位文字
- 保存按钮无任何逻辑
- Python 版根据 `PropertyType` 动态生成 Slider/ColorButton/Switch/ComboBox

### ❌ `welcome_dialog.rs` — **仅数据结构，无 UI**
- 只有 `WelcomeDialogConfig` 数据结构和 `should_show()` 判断
- **没有任何 GTK Widget 代码**
- Python 版 `WelcomeDialog`：Logo 展示、Workshop 路径选择器、开机自启开关、onboarding_completed 标志写入

### ❌ `dialogs.rs` — **仅返回字符串的 stub 函数**
- `show_delete_dialog_simple()` → 返回格式化字符串（不弹窗）
- `show_error_dialog_simple()` → 返回格式化字符串（不弹窗）
- `show_screenshot_success_dialog_simple()` → 返回格式化字符串（不弹窗）
- `show_nickname_dialog_simple()` → 直接返回入参（不弹窗）
- **所有对话框都是纯函数 stub，无任何 GTK 对话框代码**

### ⚠️ `context_menu.rs` — **菜单项定义存在，无动作绑定**
- `ContextMenuItem` 枚举定义完整（Apply/Stop/SetNickname/Separator/Delete/OpenFolder）
- `create_wallpaper_context_menu()` 创建了 `PopoverMenu` 并使用 GAction 名称
- **缺少**：GAction 的实际注册和回调绑定（菜单点击无效果）

### ✅ `thumbnail_cache.rs` — **较完整**
- LRU 缓存（80条）、JPG/PNG/GIF 支持
- GIF 智能提取第 15 帧逻辑实现
- ⚠️ `gif` crate 的 API 调用方式可能与实际版本不符（`next_frame_info()` vs `read_next_frame()`）

### ✅ `utils.rs` — **完整**
- `markdown_to_pango()`：**/**/BBCode [url=][color=] 转换
- `format_size()`：文件大小格式化
- 有完整单元测试

### ⚠️ `tray_manager.rs` — **可启动进程，状态同步缺失**
- 可以查找并启动 tray 二进制
- **缺少**：500ms tooltip 轮询、状态 payload 构建（`ACTIVE|<markup>` 格式）、向 Tray RX socket 发送状态

---

## 5. `lwg-tray` (in lwg-rs) — 状态

### ❌ 仅 26 行，无任何托盘功能
- 只有 `main()` 函数，读取 socket 路径环境变量
- 有一个 `--test` 参数发送 Toggle IPC 命令
- **无任何 systray 代码（无 ksni/appindicator/任何托盘库）**
- 这个 crate 与已完成的 `tray_rs/` 完全独立，用途不明
- **建议：确认此 crate 是否需要保留，还是直接复用 `tray_rs/`**

---

## 6. Python 中存在但 Rust 中完全缺失的功能

| Python 模块/功能 | 重要性 | 说明 |
|----------------|--------|------|
| `core/logger.py` → `LogManager` | 高 | 运行时日志收集 API，Settings 日志页依赖此模块 |
| `core/integrations.py` → `AppIntegrator` | 高 | `.desktop` 文件、开机自启、应用图标安装 |
| `core/updater.py` → `UpdateChecker` | 中 | GitHub 版本检查 |
| `ui/compact_window.py` → `CompactWindow` | 高 | 300×700 紧凑模式独立窗口，5个圆形缩略图，←→导航 |
| `app.py` → `cycle_timer` | 高 | 定时壁纸轮换（`cycleEnabled`/`cycleInterval`） |
| `app.py` → `session 恢复` | 高 | 启动时根据 `active_monitors` 恢复上次壁纸 |
| `app.py` → `show_toast()` / `Adw.ToastOverlay` | 中 | 全局 Toast 通知，多处依赖 |
| `app.py` → `About Dialog` | 低 | `Adw.AboutDialog`，含 changelog 和 debug 信息 |
| `app.py` → `Quit 确认对话框` | 低 | `Adw.MessageDialog` 确认后退出 |
| `app.py` → `Update 对话框` | 低 | 更新可用时的 `Adw.MessageDialog` |
| `app.py` → CSS 加载 | 高 | `CSS_STYLE` 常量注入到 GTK StyleContext |
| `app.py` → `AppImage` 重启逻辑 | 低 | AppImage 环境下的特殊重启处理 |

---

## 7. 关键接口问题（跨 Crate）

### 问题 1：`app.rs` 与子组件完全未连接
`toolbar.rs`、`sidebar.rs`、`grid_view.rs`、`navbar.rs`、`settings_page.rs`、`performance_page.rs` 全部实现了独立的 `relm4::Component`，但 `app.rs` 完全没有引用任何一个。

### 问题 2：Widget 刷新逻辑缺失
多个组件（`sidebar.rs`、`grid_view.rs`、`list_view.rs`）在 `update()` 中只更新内部模型状态，但不触发任何 Widget 的重绘（未使用 `widgets.xxx.set_label()` 等）。这在 relm4 中需要通过 `view!` macro 中的 `#[watch]` 或手动在 `update()` 中通过 `widgets` 参数更新 UI。

### 问题 3：`performance.rs` 硬编码数据
`PerformanceMonitor::get_stats()` 返回 `cpu: 5.0, memory: 50.0`，`performance_page.rs` 调用此接口，导致性能页永远显示假数据。

### 问题 4：`LogManager` 缺失导致 Settings 日志页无法工作
`settings_page.rs` 中日志子页面完全为空，且整个项目没有运行时可查询的日志 API。

### 问题 5：`lwg-tray` crate 定位不明
`lwg-rs/crates/lwg-tray/` 只有 26 行的空壳，与根目录 `tray_rs/`（已完成的托盘）的关系和分工不明确。

---

## 8. 优先级排序（按阻塞关系）

### P0 — 解除主窗口阻塞（必须先做）
1. **`app.rs` 重写** — 集成三页面 Stack、NavBar、CSS 加载、IPC 启动、托盘启动  
   *阻塞几乎所有其他 UI 工作*

2. **`LogManager` Rust 实现** — 运行时可查询的日志 API  
   *阻塞 Settings 日志页*

3. **`PerformanceMonitor` 真实实现** — 用 `sysinfo` 替换硬编码数据  
   *阻塞性能页所有功能*

### P1 — 核心 UI 功能
4. **`GridView` 连接真实数据** — FlowBox、`WallpaperManager` 数据绑定、缩略图加载  
5. **`Sidebar` 完整实现** — 缩略图显示、属性编辑、昵称保存逻辑、屏幕选择  
6. **`HistoryDialog` 实现** — 历史列表、缩略图、回放  
7. **`NicknameManagerDialog` 实现** — 批量管理界面  
8. **`PropertiesEditor` 动态实现** — 根据类型生成 Slider/ColorButton/Switch  
9. **`Dialogs` 实现** — 真实 GTK 对话框（删除确认、错误、截图成功、昵称输入）

### P2 — 重要功能
10. **`Settings` 所有子页面** — General（路径选择）/ Audio / Advanced / Logs  
11. **Sparkline Cairo 实现** — 替换 ProgressBar 降级方案  
12. **`TrayManager` 状态轮询** — 500ms tooltip 更新  
13. **Cycle Timer** — 定时壁纸轮换逻辑  
14. **Session 恢复** — 启动时根据 `active_monitors` 恢复

### P3 — 完善功能
15. **`CompactWindow` 实现** — 独立紧凑模式窗口（300×700）  
16. **`WelcomeDialog` UI** — 向导界面  
17. **`AppIntegrator` 实现** — `.desktop` 文件、开机自启  
18. **`UpdateChecker` 实现** — GitHub 版本检查  
19. **`lwg-tray` crate 定位澄清** — 保留/删除/与 tray_rs 合并的决策

---

## 9. 已完成的工作（值得肯定）

- `lwg-core` 的核心业务逻辑覆盖相当完整，`properties.rs` 比预期好很多
- `ThumbnailCache` 的 GIF 第 15 帧提取逻辑是对 Python 版的忠实移植
- `utils.rs` 的 Pango markup 转换完整且有测试
- `lwg-ipc` 基本可用，Protocol 设计清晰
- 整个项目可编译（仅 warnings），技术栈选型合理

---

## 10. 参考文件速查

| Rust 文件 | 对应 Python 参考 |
|----------|----------------|
| `lwg-ui/src/app.rs` | `py_GUI/ui/app.py`（950行） |
| `lwg-ui/src/grid_view.rs` + `list_view.rs` | `py_GUI/ui/pages/wallpapers.py`（1307行） |
| `lwg-ui/src/sidebar.rs` | `py_GUI/ui/pages/wallpapers.py` 侧边栏部分 |
| `lwg-ui/src/settings_page.rs` | `py_GUI/ui/pages/settings.py`（877行） |
| `lwg-ui/src/performance_page.rs` + `sparkline.rs` | `py_GUI/ui/pages/performance.py`（691行） |
| `lwg-ui/src/history_dialog.rs` | `py_GUI/ui/components/history_dialog.py` |
| `lwg-ui/src/navbar.rs` | `py_GUI/ui/components/navbar.py` |
| `lwg-ui/src/welcome_dialog.rs` | `py_GUI/ui/components/welcome_dialog.py` |
| `lwg-core/src/performance.rs` | `py_GUI/utils/performance.py` |
| *(缺失)* | `py_GUI/core/logger.py` |
| *(缺失)* | `py_GUI/core/integrations.py` |
| *(缺失)* | `py_GUI/core/updater.py` |
| *(缺失)* | `py_GUI/ui/compact_window.py` |
