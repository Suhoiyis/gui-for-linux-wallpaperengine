# Linux Wallpaper Engine GUI - 测试与发布计划

**文档版本**: v1.0  
**创建日期**: 2026-01-25  
**项目当前版本**: v0.8.1

## 📋 项目现状概览

### 当前状态
- **版本**: v0.8.1 (2026-01-25)
- **完成度**: ~90%
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

### 3. 性能监控工具

#### 3.1 后端限制说明

**关键约束**: 壁纸渲染在 C++ 后端 `linux-wallpaperengine` 中执行，Python GUI 仅作为控制器。

**能够监控的**:
| 指标 | 方式 | 精度 |
|------|------|------|
| 后端进程 CPU 占用 | psutil | 进程级 |
| 后端进程内存使用 | psutil | 进程级 |
| 壁纸启动时间 | 时间戳差值 | 粗粒度（命令到进程启动）|
| 进程存活状态 | poll() | 实时 |
| 启动失败率 | 日志统计 | 精确 |

**无法监控的（后端不提供API）**:
| 指标 | 原因 |
|------|------|
| 真实 FPS | 需要后端暴露渲染帧率 |
| 渲染性能细节 | OpenGL/渲染管线内部 |
| 壁纸加载各阶段耗时 | 后端未提供分阶段信息 |
| GPU 使用率 | 需要后端或系统级接口 |

#### 3.2 可实现的简化版监控

**实现位置**: `py_GUI/core/performance.py`

```python
import psutil
import time

class RealisticPerformanceMonitor:
    def __init__(self):
        self.backend_process = None
        
    def track_wallpaper_start_time(self, wp_id):
        start = time.time()
        # 启动后端进程...
        return time.time() - start
    
    def get_backend_metrics(self):
        if self.backend_process and self.backend_process.poll() is None:
            try:
                proc = psutil.Process(self.backend_process.pid)
                return {
                    'memory_mb': proc.memory_info().rss / 1024 / 1024,
                    'cpu_percent': proc.cpu_percent(),
                    'status': proc.status(),
                    'runtime': time.time() - proc.create_time()
                }
            except:
                return None
        return None
```

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

**最后更新**: 2026-01-25 (更新至 v0.8.1)  
**负责人**: 开发团队  
**审核状态**: 待审核