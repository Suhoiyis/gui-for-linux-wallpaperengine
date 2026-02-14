# Linux Wallpaper Engine GUI - 测试与发布计划

**文档版本**: v1.3
**创建日期**: 2026-01-25
**项目当前版本**: v0.10.4
## 📋 项目现状概览

### 当前状态
- **版本**: v0.10.4 (2026-02-12)
- **完成度**: ~98%
- **核心功能**: ✅ 基本完善
- **测试覆盖**: ❌ 待建立
- **发布渠道**: ❌ 仅源码

### 已完成的核心功能
- ✅ 壁纸浏览和管理
- ✅ 多显示器支持 (Beta)
- ✅ 系统托盘集成
- ✅ 定时轮换功能
- ✅ 高质量截图
- ✅ 命令行控制
- ✅ 配置管理
- ✅ 系统集成 (自启动、桌面快捷方式)
- ✅ **性能监控** (v0.9.2 增强：线程拆分、准确率优化、截图历史)
- ✅ **日志管理增强** (v0.9.1 新增)

---

## 🧪 自动化测试体系建设计划

### 阶段1: 基础测试框架搭建 (第1周)

#### 1.1 环境准备
```bash
# 安装测试依赖
sudo pacman -S xorg-server-xvfb imagemagick  # Arch
# sudo apt install xvfb imagemagick  # Ubuntu

pip install pytest pytest-mock pytest-cov pillow dbus-python

# 创建测试目录结构
mkdir -p tests/{unit,integration,visual,functional}
touch tests/__init__.py
```

#### 1.2 测试配置
- 创建 `pytest.ini` 配置文件
- 设置覆盖率报告 (HTML + 终端输出)
- 配置虚拟显示器环境

#### 1.3 核心工具类单元测试
- `ConfigManager`: 配置读写逻辑
- `WallpaperController`: 核心应用逻辑
- `ScreenManager`: 多屏幕检测
- `Logger`: 日志管理

**预期成果**: 基础测试框架可用，核心工具类覆盖率 > 80%

---

### 阶段2: 视觉回归测试 (第2-3周)

#### 2.1 虚拟显示器测试方案

**核心思路**: 虚拟显示器 + 自动截图对比
- 在虚拟显示器中运行测试，不影响主桌面
- 自动截图验证壁纸显示效果
- 与基准图像对比，确保视觉效果一致

#### 2.2 测试实现

**测试文件结构**:
```
tests/visual/
├── test_wallpaper_display.py      # 壁纸显示测试
├── test_screenshot_quality.py     # 截图质量测试
├── test_multi_screen.py          # 多显示器测试
├── baselines/                     # 基准截图目录
└── results/                      # 测试结果截图
```

**关键功能**:
- 虚拟显示器自动创建和清理
- 壁纸应用后自动截图
- 图像相似度对比算法
- 空白屏幕检测
- 多种壁纸类型测试

#### 2.3 测试用例设计

1. **基础显示测试**
   - 验证不同类型壁纸 (Video/Web/Scene) 能否正确显示
   - 检测显示是否为空白或异常

2. **视觉效果回归测试**
   - 对比截图与基准图像
   - 相似度阈值: > 90%
   - 自动生成差异报告

3. **多显示器测试**
   - 测试不同显示器独立控制
   - 验证屏幕切换逻辑
   - 测试显示器断开/重连场景

**预期成果**: 视觉效果自动化验证，无需人工干预

---

### 阶段3: 功能集成测试 (第4周)

#### 3.1 真实环境集成测试

**测试内容**:
- 完整的用户操作流程
- 与真实 `linux-wallpaperengine` 后端集成
- 系统托盘功能测试
- 命令行接口测试

#### 3.2 性能测试
- 壁纸加载时间测试 (< 5秒)
- 内存使用监控
- CPU 占用检测
- 长时间运行稳定性测试

#### 3.3 兼容性测试
- 不同桌面环境测试 (GNOME/KDE/Niri/Sway/Hyprland)
- 不同发行版兼容性 (Arch/Ubuntu/Fedora)
- Wayland vs X11 环境差异测试

**预期成果**: 全面的功能验证，确保在各种环境下正常工作

---

### 阶段4: 持续集成 (第5-6周)

#### 4.1 GitHub Actions 设置

**工作流程**:
```yaml
# .github/workflows/test.yml
name: Automated Testing
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Environment
        run: |
          sudo apt update
          sudo apt install xvfb imagemagick python3-gi gir1.2-gtk-4.0
      - name: Run Tests
        run: |
          xvfb-run -a pytest --cov=py_GUI --cov-report=xml
      - name: Upload Coverage
        uses: codecov/codecov-action@v3
```

#### 4.2 测试报告
- 覆盖率趋势图
- 视觉测试结果展示
- 性能基准报告
- 自动化测试通知

**预期成果**: 每次提交自动运行测试，及时发现问题

---

## 📦 发布与分发计划

### 1. 包管理系统支持

#### 1.1 Arch Linux AUR 包
**优先级**: 高 (Arch 用户多)

**任务清单**:
- [ ] 创建 `PKGBUILD` 文件
- [ ] 处理依赖关系 (python-gobject, gtk4, libadwaita等)
- [ ] 包含 `.desktop` 文件和图标
- [ ] 提交到 AUR 社区仓库

**PKGBUILD 示例**:
```bash
pkgname=linux-wallpaperengine-gui
pkgver=0.8.0
pkgrel=1
pkgdesc="Modern GTK4 GUI for managing Steam Workshop wallpapers on Linux"
arch=('any')
url="https://github.com/yourusername/linux-wallpaperengine-gui"
license=('GPL3')
depends=('python' 'python-gobject' 'gtk4' 'libadwaita' 'libayatana-appindicator')
optdepends=('linux-wallpaperengine: backend engine')
source=("$pkgname-$pkgver.tar.gz")
sha256sums=()
```

#### 1.2 Debian/Ubuntu 包
**优先级**: 中 (Ubuntu 用户基础大)

**任务清单**:
- [ ] 创建 `debian/` 目录结构
- [ ] 编写 `control`, `rules`, `changelog` 文件
- [ ] 处理 Python 包依赖
- [ ] 构建 `.deb` 包

#### 1.3 Fedora/CentOS RPM 包
**优先级**: 低
- [ ] 创建 `.spec` 文件
- [ ] 适配 Fedora 包管理规范

#### 1.4 Flatpak 包 (跨发行版)
**优先级**: 中 (沙盒化，安全性好)
- [ ] 创建 Flatpak manifest
- [ ] 处理权限和沙盒限制
- [ ] 提交到 Flathub

---

### 2. CI/CD 自动化构建

#### 2.1 多平台构建流水线
```yaml
# .github/workflows/build.yml
name: Build Packages
on:
  release:
    types: [published]
jobs:
  build-arch:
    runs-on: ubuntu-latest
    steps:
      - name: Build AUR package
        run: makepkg -s
  build-debian:
    runs-on: ubuntu-latest
    steps:
      - name: Build Debian package
        run: dpkg-buildpackage -us -uc
  build-flatpak:
    runs-on: ubuntu-latest
    steps:
      - name: Build Flatpak
        run: flatpak-builder build-dir com.example.wallpaper-gui.json
```

#### 2.2 自动发布流程
- 标签推送时自动构建包
- 生成安装脚本
- 更新文档和下载链接

---

### 3. 性能监控工具 ✅ **已完成 (v0.9.2)**

#### 3.1 实现概览

**实现位置**: `py_GUI/core/performance.py`, `py_GUI/ui/pages/performance.py`, `py_GUI/ui/components/sparkline.py`

**功能特性**:
| 功能 | 描述 |
|------|------|
| 总览卡片 | Total CPU、Total Memory、Active Threads 三项核心指标 |
| 历史曲线图 | 基于 Cairo 的 Sparkline 组件，显示最近 60 秒数据 |
| 进程详情 | Frontend/Backend/Tray 三个进程独立监控 |
| **线程拆分** | (v0.9.2) 每个进程独立的 "Thread Details" 下拉抽屉，包含完整线程名 |
| **截图历史** | (v0.9.2) 记录最近 10 次截图的耗时、资源占用，并提供快速查看/清除功能 |
| 动态着色 | CPU 根据负载变色（绿<20%、橙<40%、红≥40%），内存蓝色 |
| 壁纸详情 | Backend 进程可展开显示各显示器壁纸缩略图、标题、ID |

#### 3.2 技术实现

**核心类**: `PerformanceMonitor`
- 使用 `psutil` 进行进程级监控
- 1 秒采样间隔，60 秒历史缓冲
- 缓存 `psutil.Process` 对象避免重复查找
- 自动识别真正的后端进程（跳过 bash wrapper）

**UI 组件**: `Sparkline`
- 纯 Cairo 绘制，无外部依赖
- 自适应缩放（最小 10%，最大 100%）
- 右对齐模式（数据不足 60 秒时从右侧开始绘制）
- 网格线和刻度标签

**监控能力**:
| 指标 | 方式 | 精度 |
|------|------|------|
| 后端进程 CPU 占用 | psutil | 进程级 |
| 后端进程内存使用 | psutil | 进程级 |
| 进程存活状态 | psutil | 实时 |
| 线程名称 | /proc/{pid}/task | 实时 |
| 当前壁纸信息 | config + wp_manager | 实时 |

**无法监控的（后端不提供API）**:
| 指标 | 原因 |
|------|------|
| 真实 FPS | 需要后端暴露渲染帧率 |
| 渲染性能细节 | OpenGL/渲染管线内部 |
| GPU 使用率 | 需要后端或系统级接口 |

#### 3.3 性能基准测试
- 建立 Performance Regression 测试
- 不同壁纸类型的性能基准
- 长时间运行性能衰减监控

---

### 4. 用户反馈收集机制

#### 4.1 应用内反馈功能
**实现位置**: `py_GUI/ui/components/feedback_dialog.py`

**功能设计**:
- 快速反馈按钮 (菜单栏)
- 自动收集系统信息
- 错误日志自动附加
- 匿名使用统计 (可选)

#### 4.2 GitHub Issues 模板
创建标准化的 Issue 模板:
- Bug 报告模板
- 功能请求模板
- 兼容性问题模板

#### 4.3 使用统计收集
**隐私友好设计**:
- 匿名统计，不收集个人信息
- 用户可选择退出
- 透明公开收集的数据类型

**统计数据**:
- Linux 发行版分布
- 桌面环境使用情况
- 壁纸类型使用频率
- 功能使用统计

---

## 🚧 尚缺功能开发计划

### 优先级 P1 (核心缺失)
- **暂无** - 核心功能已基本完成

---

### 优先级 P2 (功能缺失)
> **注**: 自定义资源支持已在 v0.8.1 完成，移出此列表

#### 0. 滚动条样式优化 ⚠️ **搁置/待调研**
**描述**：滚动条视觉呈现两层结构（疑似 trough + slider 分离显示），尝试隐藏 trough 未完全生效

**当前状态**：
- 已优化：透明度淡入淡出、细化宽度（3px）、半透明白色
- 未解决：GTK4/Adwaita 主题下 scrollbar 仍显示双层结构，CSS `background: transparent` 未完全覆盖默认样式

**下一步**：
- 调研 GTK4 scrollbar 完整 CSS 节点（scrollbar > range > trough > slider）
- 尝试 `all: unset` 或 `-gtk-icon-source: none` 等强制重置
- 考虑是否为 Adwaita 主题特有行为

#### 1. 自定义资源支持 ✅ **已完成 (v0.8.1)**
**功能描述**: `--assets-dir` 自定义 assets 目录路径

**实现需求**:
- ✅ 修改配置文件结构，支持自定义资源路径
- ✅ 更新 CLI 参数解析
- ✅ UI 中添加路径选择器
- ✅ 资源验证和错误处理

**实现细节**:
- 配置字段: `assetsPath` (默认 None，自动检测)
- UI 组件: Settings 页面路径输入框 + 浏览按钮
- 后端集成: Controller 中传递 `--assets-dir` 参数
- 验证机制: 目录存在性 + materials/shaders 子目录检查
- 用户反馈: Toast 通知显示验证结果

**完成工作量**: 2天
**提交记录**: 
- `c303829` - 基础支持 (CLI 参数 + 配置 + UI 选择器)
- `783f2b9` - 错误反馈 (Toast 通知系统)
- `6811922` - 即时验证 (保存后路径验证反馈)

**技术验证**: 
- 后端期望: `materials/`, `shaders/`, `effects/` 子目录
- 实现验证: 检查 `materials/` 和 `shaders/` 存在性
- 兼容性: 与 linux-wallpaperengine v2.3+ 完全兼容

#### 2. 动态壁纸预览优化
**功能描述**: GIF 预览仅显示首帧，需要实现动画预览
**如果gif的第一帧是黑色的，现在gui里也直接显示为黑色，没法预览**

**技术挑战**:
- 性能优化: 避免大量 GIF 同时播放卡顿
- 内存控制: 限制同时播放的动画数量
- 用户体验: 提供播放/暂停控制

**实现方案**:
```python
class AnimatedPreview:
    def __init__(self):
        self.active_animations = {}  # 限制同时播放数量
        self.animation_limit = 3
    
    def start_animation(self, wallpaper_id):
        if len(self.active_animations) < self.animation_limit:
            # 开始播放动画
            pass
        else:
            # 显示静态预览
            pass
```

**预期工作量**: 3-4天

#### 3. Wayland 专属优化
**功能描述**: `--fullscreen-pause-only-active` 等精细化控制

**技术要求**:
- 检测窗口焦点状态
- 实现智能暂停机制
- 优化 Wayland 环境下的资源使用

**预期工作量**: 4-5天

---

### 优先级 P2.5 (性能优化)

#### 1. 托盘进程 Go 重写
**功能描述**: 用 Go 重写系统托盘进程，大幅降低内存占用

**背景分析**:
- 当前 Python + GTK3 托盘进程占用 ~64MB RSS / ~26MB PSS
- 这是 Python 解释器 + GTK3 + AppIndicator 的固有开销
- 图标本身只有 7KB，与内存占用无关

**优化目标**:
| 指标 | 当前 (Python) | 目标 (Go) |
|------|---------------|-----------|
| RSS | ~64 MB | ~8-15 MB |
| PSS | ~26 MB | ~5-10 MB |
| 启动时间 | ~500ms | ~50ms |

**技术方案**:
- 使用 `github.com/getlantern/systray` 或 `fyne.io/systray` 库
- 编译为单一二进制文件，无运行时依赖
- 复用现有 CLI 通信方式 (`run_gui.py --show/--random/--stop/--quit`)
- 保持功能完全兼容

**实现内容**:
1. 创建 `tray_go/` 目录
2. 实现 Go 托盘程序 (~100 行代码)
3. 编译为 `wallpaper-tray` 二进制
4. 更新 `py_GUI/ui/tray.py` 调用新二进制
5. 保留 Python 版本作为 fallback

**菜单功能** (与 Python 版本一致):
- 显示窗口 (粗体，中键点击)
- 播放/停止 (检测后端运行状态)
- 随机切换壁纸
- 退出程序

**预期工作量**: 1-2 小时


##### 托盘实现方案对比
1. 接受现状（当前 Python + GTK3）
| 指标 | 值 |
|------|-----|
| 内存占用 | ~26 MB (PSS) / 64 MB (RSS) |
| 开发成本 | 零 |
| 维护成本 | 低 |
特点：
- ✅ 已经实现，代码成熟
- ✅ 与主程序共享 GTK 库（如果同时运行）
- ❌ Python 解释器开销不可避免
---
2. 用 Go 重写托盘进程
| 指标 | 预估值 |
|------|-----|
| 内存占用 | 3-8 MB |
| 开发成本 | 中等（1-2小时） |
| 维护成本 | 低 |
特点：
- ✅ 最省资源的可行方案
- ✅ 编译为单一二进制文件，无运行时依赖
- ✅ 使用 github.com/getlantern/systray 或 fyne.io/systray
- ✅ 启动速度极快（~50ms vs Python ~500ms）
- ❌ 需要 Go 开发环境
- ❌ 与主程序通信需要 IPC（可复用现有 CLI 方式）
示例代码结构：
// 约 80 行代码
func main() {
    systray.Run(onReady, onExit)
}
func onReady() {
    systray.SetIcon(icon)
    mShow := systray.AddMenuItem("显示窗口", "")
    go func() {
        for range mShow.ClickedCh {
            exec.Command("python3", "run_gui.py", "--show").Start()
        }
    }()
}
---
3. 用 C 重写托盘进程
| 指标 | 预估值 |
|------|-----|
| 内存占用 | 2-5 MB |
| 开发成本 | 高（2-4小时） |
| 维护成本 | 中 |
特点：
- ✅ 理论上最省内存
- ✅ 直接调用 libayatana-appindicator3
- ❌ 代码量大（~200 行）
- ❌ 需要处理 GLib 主循环、信号等
- ❌ 编译依赖管理麻烦
---
4. 合并托盘到主进程
| 指标 | 值 |
|------|-----|
| 内存占用 | 节省 ~15-20 MB（省去一个 Python 解释器） |
| 开发成本 | 低-中（需要处理 GTK3/GTK4 混用问题） |
| 维护成本 | 低 |
特点：
- ✅ 减少一个进程
- ❌ GTK 版本冲突：主程序用 GTK4，托盘用 GTK3（AppIndicator 只支持 GTK3）
- ❌ 如果主进程崩溃，托盘也消失
- ❌ 需要在同一进程中混用 GTK3 和 GTK4（技术上很难实现）
结论：由于 GTK 版本冲突，这个方案不推荐。
---
5. 换用 Qt 托盘
| 指标 | 预估值 |
|------|-----|
| 内存占用 | ~20-30 MB |
| 开发成本 | 中 |
| 维护成本 | 中 |
特点：
- ❌ 需要安装 PyQt5/6 依赖
- ❌ 内存占用与 GTK 差不多
- ❌ 增加项目依赖复杂度
- ✅ QSystemTrayIcon 更现代化
结论：没有明显优势，不推荐。
---
推荐排序
| 排名 | 方案 | 内存 | 推荐理由 |
|------|------|------|----------|
| 🥇 | Go 重写 | 3-8 MB | 最佳平衡：省内存、易开发、易维护 |
| 🥈 | 接受现状 | 26 MB | 零成本，现代系统无压力 |
| 🥉 | C 重写 | 2-5 MB | 最省但开发成本高 |
| ❌ | 合并到主进程 | - | GTK3/GTK4 冲突，不可行 |
| ❌ | Qt 托盘 | ~25 MB | 无明显优势 |
---



---

### 优先级 P3 (低频/复杂)

#### 1. 窗口模式支持
**功能描述**: `--window` (需 UI 支持自定义几何坐标)

**实现内容**:
- CLI 参数添加窗口选项
- UI 窗口大小和位置设置界面
- 窗口模式下的渲染优化
- 配置持久化

**预期工作量**: 5-6天

#### 2. 播放列表功能
**功能描述**: `--playlist` (需 UI 支持列表管理)

**功能设计**:
- 播放列表创建和编辑
- 多种播放模式 (顺序/随机/加权)
- 播放列表导入/导出
- 定时轮换与播放列表集成

**UI 组件设计**:
```python
class PlaylistManager:
    def __init__(self):
        self.playlists = {}
        self.current_playlist = None
        self.play_mode = "random"  # random, sequential, weighted
    
    def create_playlist(self, name, wallpaper_ids):
        """创建新播放列表"""
        pass
    
    def get_next_wallpaper(self):
        """获取下一个壁纸"""
        pass
```

**预期工作量**: 7-10天


#### 3.删除功能 ⚠️ **搁置/调研中**
**描述**：目前的右键壁纸删除功能仅仅能删除文件夹下的文件，启动steam联网后steam会自动下载回此前删除的壁纸
- **当前状态**：实现了本地文件删除。
- **遇到的问题**：Steam 会自动重新下载订阅的物品。
- **尝试的方案**：直接修改 `appworkshop_431960.acf` manifest 文件以移除订阅。
- **搁置原因**：直接修改 Steam manifest 文件存在风险（可能导致 Steam 库状态异常），且需要重启 Steam 才能生效。
- **下一步**：调研是否有更安全的方法（如 `steamcmd` 命令行工具或 Steam Web API）来以编程方式取消订阅 Workshop 物品。目前代码中保留了 manifest 修改逻辑但已注释。

#### 4.指令显示/复制 ✅ **已完成 (v0.8.2)**
**描述**：显示出应用当前壁纸时使用的指令，并且允许用户直接点击复制，相比于在logs里面显示的更加直观

**实现细节**:
- 在 "CURRENTLY USING" 壁纸标题旁边新增 📋 按钮
- 悬停按钮显示当前后端命令预览（截断至 80 字符）
- 点击按钮复制完整命令到剪贴板，Toast 提示"已复制"
- `WallpaperController` 新增 `get_current_command()` 方法

#### 5.显示大小 ✅ **已完成 (v0.8.2)**
**描述**：（在右侧栏）显示每个壁纸占用磁盘空间大小，方便用户把控

**实现细节**:
- 在 Folder ID 旁边显示绿色标签，格式如 "85.1 MB"
- 扫描时计算文件夹大小，无额外性能开销
- 新增 `format_size()` 和 `get_folder_size()` 工具函数

#### 6.排序方式 ✅ **已完成 (v0.8.2)**
**描述**：允许壁纸列表里不同的排序方式，如：文件大小，名称，载入顺序，订阅日期，最后更新时间等

**实现细节**:
- 工具栏新增 ⇅ 排序下拉菜单
- 支持 5 种排序：Title, Size ↓, Size ↑, Type, ID
- 排序选项自动保存到配置文件
- 注：订阅日期和更新时间因数据不可靠未实现

#### 7.多显示器指令优化 ❌ **不采用**
**描述**：YouTube 上有人使用多进程 + sleep 方式启动多显示器壁纸

**YouTube 方案**:
```bash
linux-wallpaperengine --silent --screen-root DP-1 11111111 &
sleep 1
linux-wallpaperengine --silent --screen-root HDMI-A-1 2222222 &
sleep 1
linux-wallpaperengine --silent --screen-root DP-2 333333 &
```

**当前方案**（单进程多参数）:
```bash
linux-wallpaperengine --screen-root DP-1 --bg 11111111 --screen-root HDMI-A-1 --bg 2222222 [全局参数]
```

**决定不采用的原因**:
1. **内存开销过大**：多进程方案 3 显示器 = 3 进程 = 600MB-1.2GB，单进程仅需 200-400MB
2. **当前方案是官方支持的用法**：linux-wallpaperengine 本身设计了 `--screen-root X --bg Y` 的单进程多屏语法
3. **YouTube 方案是 workaround**：可能是早期版本不支持单进程多屏时的变通办法
4. **进程管理复杂**：停止/随机切换时需要同步管理多个 PID

**结论**：维持现状，除非遇到启动竞争导致的黑屏问题再考虑

#### 8.托盘功能随机 ✅ **已修复 (v0.8.2)**
**描述**：gui窗口关闭时，使用托盘右键功能"随机切换壁纸"似乎会唤出gui窗口，这个逻辑似乎与正常用户逻辑不符

**修复细节**:
- 问题原因：应用初始化后 `_is_first_activation` 标志未重置为 `False`，导致后续 CLI 命令触发 `activate()` 时误判为"首次激活"并显示窗口
- 修复位置：`py_GUI/ui/app.py` 初始化完成后添加 `self._is_first_activation = False`

#### 9.标题栏 ✅ **已修复 (v0.8.2)**
**描述**：没有标题栏绘制，建议直接让系统默认绘制标题栏（niri、hyprland下不需要，kde下推荐使用ked插件wallpaper-engine-kde-plugin，但在别的环境下没有绘制的标题栏用户没法方便地最大化、最小化、关闭窗口）

**修复细节**:
- 使用 `Gtk.ApplicationWindow` 替代 `Adw.ApplicationWindow`
- 标题栏由窗口管理器决定（SSD 模式）
- niri/Hyprland 等平铺 WM 不显示标题栏
- GNOME/KDE 等传统桌面显示系统标题栏（含最大化/最小化/关闭按钮）

#### 10.RANDOM ✅ **已修复 (v0.8.2)**
**描述**：使用自动切换功能切换壁纸后wallpaper cycling的random的随机计时器应该重置（暂不清楚手动切换壁纸能否使random的计时器重置）总不能刚刚手动切完一个想要的壁纸然后就以为计时器时间到了就又被换掉了吧
**修复细节**:
- 在手动应用壁纸 (`on_action_apply`) 时强制调用 `setup_cycle_timer()`
- 这会重置定时器倒计时，确保用户手动选择壁纸后，会重新开始完整的计时周期，不会被即将到期的自动切换打断。

#### 11.顶栏 ✅ **已修复 (v0.8.2)**
~~**描述**：顶栏的“窗口选择器”，“Home”“Settings”这一栏三个按键胶囊的底下有一个统一绘制的黑框，但是这个黑框看起来并不美观，能不能去除（当然顶栏的第二排，搜索框，排列方式那一排底下也有黑框，但是这一排的底部黑框可以保留）~~
~~**修复细节**:~~
~~- 在 CSS 中为 `.nav-btn` 类添加 `box-shadow: none;` 和 `outline: none;`，移除了 GTK 默认绘制的阴影/边框效果。~~

似乎尚未生效，需要观察

#### 12.多显示器选择 ✅ **代码已就绪 (v0.8.5)**
**描述**：实现多屏幕壁纸同步（Same）和差异化（Diff）控制，以及灵活的多选功能。

**状态说明**:
- 功能代码已合并至 v0.8.5。
- **注意**：由于开发环境限制，多显示器物理渲染效果尚未在真机多屏环境下验证（待测试）。

**实现细节**:
- **Link/Unlink 开关**：顶栏新增 🔗 按钮（多屏时显示），切换 "Apply All" 和 "Apply Single" 模式。
- **高级选择抽屉**：侧边栏 Apply 按钮升级为 Split Button，下拉菜单支持勾选特定屏幕组合（满足 `2+1` 场景）。仅在屏幕>=3且为Diff模式时显示。
- **后端支持**：Controller 新增 `screens` 参数支持批量应用。后端指令逻辑遵循 P3-7 单进程多屏模式。

#### 13.预览图 ✅ **已完成 (v0.8.6)**
**描述**：解决 GIF 壁纸预览图全黑问题，并提供动态预览。

**实现细节**:
- **智能缩略图 (P3-13)**：使用 Pillow 自动提取 GIF 第 15 帧（或 20% 处）作为静态封面，避开开头黑屏。
- **动态详情图 (P2-2)**：在侧边栏选中 GIF 时，直接播放原图动画。
- **高质量缩放**：采用 LANCZOS 算法生成清晰缩略图。

#### 14.总数显示 ✅ **已完成 (v0.8.3)**
**描述**：在顶栏"CURRENTLY USING"右侧显示壁纸序号/总数（N/M）

**实现细节**:
- 在"CURRENTLY USING"标题行右侧添加计数器标签
- 显示格式：N/M（当前壁纸在过滤列表中的序号/总数）
- 使用与壁纸名字相同的样式（`status-value` CSS class）
- 自动更新场景：壁纸变化、屏幕切换、搜索/排序/重新加载

#### 15.Wayland 高级控制 (P3-15) ✅ **已完成 (v0.8.10)**
**描述**：支持 Wayland 特有的暂停策略控制。
- `--fullscreen-pause-only-active`: 仅当全屏窗口处于活动状态时暂停。
- `--fullscreen-pause-ignore-appid`: 忽略特定应用程序（如 Dock、Bar）的全屏状态判定。

**实现细节**:
- 设置页面新增 "Wayland Tweaks" 区域，自动检测会话类型。
- 提供 Switch 和 Entry 控件，非 Wayland 环境自动禁用。
- 后端 Controller 读取配置并动态追加参数。

#### 16.壁纸属性自定义 (P2-3)
**描述**：支持修改壁纸的自定义属性（如颜色、速度、特效开关）。
- 解析 `linux-wallpaperengine --list-properties` 的输出。
- 动态生成设置表单（Slider, Color Picker, Checkbox）。
- 应用时传递 `--set-property key=value`。

#### 17.窗口化预览 (P3-16)
**描述**：利用 `--window` 参数提供独立的壁纸预览窗口，无需直接应用到桌面即可查看动态效果。

#### 18.性能卡顿分析 🔍
##### 问题现象
- 初次切换 grid ↔ list：2-3 秒卡顿
- 后续切换：正常响应
根本原因（确定）
##### 1. 双重过滤调用 ⚠️ 主要原因
###### 第1次过滤（第748行）
def refresh_wallpaper_grid(self):
    self._current_wp_ids = list(self.filter_wallpapers().keys())  # ← 第1次
    ...
    self.populate_grid()  # 或 populate_list()
###### 第2次过滤（第815行/第827行）
def populate_grid(self):
    filtered = self.filter_wallpapers()  # ← 第2次
    for folder_id, wp in filtered.items():
        card = self.create_grid_item(...)
每次切换都调用 filter_wallpapers() 两次，包括：
- 遍历所有壁纸并转换为小写
- 排序整个列表（O(n log n)）
假设有 500+ 个壁纸，这就是 1000+ 次字符串转换 + 两次排序。
---
##### 2. 同步图像加载 ⚠️ 次要原因，累积效应
create_grid_item() 和 create_list_item() 中：
###### 第869行（grid）和第942行（list）
texture = self.wp_manager.get_texture(wp["preview"], 170)
- Grid 模式：170×170px，如果有 100 个壁纸 = 100 次图像加载
- List 模式：100×100px，加载较小但仍需 I/O
虽然有 LRU 缓存，但初次切换时缓存是冷的（第一次加载 grid 时缓存了 170×170，切到 list 时需要 100×100 的新尺寸 = 缓存 miss）。
---
##### 3. 为什么第一次慢，后续快？
| 操作 | 第1次切换 | 第2次切换 |
|------|---------|---------|
| 过滤 | 2次过滤 | 2次过滤（已排序，可优化但此次仍执行） |
| 缓存 | 冷缓存（0 条项） | 热缓存（已有 100+ 条） |
| 图像 I/O | 100+ 次磁盘读取 | 0 次（全部缓存命中） |
| GTK 布局 | 第一次渲染，可能堆积任务 | GTK 内部状态已热 |
关键：图像缓存是全局的，一旦加载过就永久保存。
---
哪个函数最耗时？
基于代码复杂度：
| 函数 | 耗时 | 原因 |
|------|------|------|
| filter_wallpapers() | 中等 | 两次排序 + 字符串转换 |
| get_texture() | 最高 | 同步 I/O + 图像解码（GIF 尤其慢） |
| populate_grid/list() | 低-中等 | 循环创建 GTK 对象，但 GTK 对象本身不贵 |
| GTK 布局计算 | 未知 | 可能在后台累积，但应该是异步 |
排序：get_texture() > filter_wallpapers() > populate_x()
---
GIF 处理额外成本
如果壁纸包含 GIF，get_texture() 中：
if path.lower().endswith('.gif'):
    # PIL Image.open() + seek(15) + convert("RGBA") + thumbnail() + save to PNG + PixbufLoader.write()
这是最重的操作。如果有 20-30 个 GIF 壁纸，就能解释 2-3 秒的延迟。
---
为什么 GTK 布局不是主要原因
- GTK4 FlowBox/ListBox 的 append() 应该是异步的
- 布局计算一般被推迟到下一个主循环迭代
- 但如果有 100+ 个复杂 widget，仍可能影响首帧延迟
---
##### 总结
初次切换 grid→list 的 2-3 秒延迟由以下累积：
1. filter_wallpapers() 被调用 2 次（冗余）
   → 遍历 500+ 壁纸、转小写、排序
2. get_texture() 缓存冷启动
   → 需要加载 100+ 张图（特别是 GIF 的解码很慢）
3. 可能的 GTK 布局堆积
   → 100+ 新 widget 加入容器，布局计算延迟
后续切换快的原因：
  - 图像已全部缓存在内存中 → get_texture() 返回秒级
  - filter_wallpapers() 仍被调用 2 次，但成本低（数据在内存，不涉及 I/O）

---

## 📅 实施时间表

### 第一阶段 (Week 1-2): 测试基础建设
- [x] 项目现状分析
- [x] 自定义资源支持实现 (v0.8.1) - 移出 P2 列表
- [ ] 测试框架搭建
- [ ] 核心类单元测试
- [ ] 虚拟显示器环境配置

### 第二阶段 (Week 3-4): 视觉测试实现
- [ ] 壁纸显示自动化验证
- [ ] 多显示器测试
- [ ] 性能基准测试
- [ ] 兼容性测试

### 第三阶段 (Week 5-6): 发布准备
- [ ] AUR 包创建和提交
- [ ] Debian 包构建
- [ ] CI/CD 流水线设置
- [ ] 文档完善

### 第四阶段 (Week 7-8): 功能完善
- [ ] P2 优先级功能开发
- [ ] 用户反馈机制实现
- [ ] 性能监控工具
- [ ] 社区反馈收集

### 第五阶段 (Week 9+): 长期维护
- [ ] P3 优先级功能 (按需)
- [ ] 社区贡献管理
- [ ] 版本迭代规划

---

## 🎯 成功指标

### 测试覆盖率目标
- 单元测试覆盖率: > 80%
- 集成测试覆盖率: > 70%
- 视觉测试成功率: > 95%

### 发布目标
- AUR 包成功发布并维护
- 至少 2 个 Linux 发行版包可用
- CI/CD 自动化覆盖率 100%
- 用户反馈收集机制运行良好

### 用户体验目标
- 新用户 5 分钟内完成安装和使用
- 壁纸加载时间 < 5 秒
- 应用启动时间 < 3 秒
- 内存占用 < 300MB

---

## 📝 备注

1. **测试优先**: 在开发新功能前，先建立完善的测试体系
2. **渐进发布**: 先建立基础发布渠道，再逐步完善
3. **社区驱动**: 重视用户反馈，基于实际需求调整优先级
4. **文档同步**: 每个功能都要有对应的用户文档
5. **质量第一**: 宁可功能少而精，不要功能多而乱

---

**最后更新**: 2026-02-12 (发布 v0.10.4)  
**负责人**: 开发团队  
**审核状态**: 待审核