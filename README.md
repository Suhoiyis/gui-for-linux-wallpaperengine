# Linux Wallpaper Engine GUI

一个现代化的 GTK4 图形界面，让你在 Linux 上轻松管理和应用 Steam Workshop 的动态壁纸。

> 基于 [linux-wallpaperengine](https://github.com/Almamu/linux-wallpaperengine) 后端，为 GNOME / Wayland 桌面环境优化

## 特性

- **轻量流畅**：纯 Python + GTK4 实现，内存占用约 250MB
- **现代设计**：使用 Libadwaita，深色主题，圆角阴影
- **系统托盘**：后台常驻，支持快捷操作
- **多屏支持**：为不同显示器设置独立壁纸
- **性能监控**：实时查看 CPU/内存占用与截图历史记录，带历史曲线图
- **自动化**：定时随机切换、开机自启、一键截图
- **排序与筛选**：支持按名称、大小、类型等多种方式排序壁纸
- **日志管理**：支持按模块过滤日志，快速定位问题
- **命令行控制**：支持无 GUI 后台运行和远程操作

## 快速开始

### 依赖安装

**Arch Linux:**
```bash
sudo pacman -S python-gobject gtk4 libadwaita libayatana-appindicator
```

**Ubuntu/Debian:**
```bash
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 libayatana-appindicator3-1
```

### 安装 linux-wallpaperengine 后端

本 GUI 需要配合 [linux-wallpaperengine](https://github.com/Almamu/linux-wallpaperengine) 使用：

```bash
# 参考后端项目的编译安装说明
# 确保 linux-wallpaperengine 可执行文件在 PATH 中
```

### 运行

```bash
# 启动 GUI
python3 run_gui.py

# 后台启动（仅托盘图标）
python3 run_gui.py --hidden

# 显示已运行的 GUI
python3 run_gui.py --show
```

## 基本使用

1. **浏览壁纸**：首次启动会自动扫描 Steam Workshop 壁纸库
2. **应用壁纸**：双击卡片或点击侧边栏的 "Apply" 按钮
3. **随机切换**：点击工具栏的 🎲 按钮或使用托盘菜单
4. **停止播放**：点击工具栏的 ⏹ 按钮
5. **多屏设置**：在顶栏下拉菜单选择目标显示器
6. **性能监控**：点击顶栏的监控图标，查看各进程资源占用和历史曲线

## 命令行控制

所有命令会发送到同一运行实例：

| 命令 | 功能 |
|------|------|
| `--show` | 显示窗口 |
| `--hide` | 隐藏窗口 |
| `--toggle` | 切换显示/隐藏 |
| `--random` | 随机切换壁纸 |
| `--stop` | 停止当前壁纸 |
| `--apply-last` | 应用上次壁纸 |
| `--quit` | 完全退出程序 |

**示例：**在 Niri/i3wm 中配置开机自启
```bash
# 后台启动并自动应用上次壁纸
python3 /path/to/run_gui.py --hidden
```

## 配置文件

位置：`~/.config/linux-wallpaperengine-gui/config.json`

包含以下设置：
- FPS 限制（1-144）
- 音量和静音选项
- 缩放模式（拉伸/适应/裁剪）
- 自动轮换间隔
- 最后应用的壁纸

可通过 GUI 的 Settings 页面修改。

## 已知限制

### 壁纸类型兼容性

| 类型 | 兼容性 | 说明 |
|------|--------|------|
| **Video** | ✅ 完美支持 | MP4/WebM 格式推荐 |
| **Web** | ⚠️ 部分支持 | 可显示但**属性调整失效**（后端限制） |
| **Scene** | ⚠️ 有限支持 | 复杂粒子/着色器可能花屏或失效 |

### Wayland 环境限制

- ❌ **鼠标交互失效**：无法获取全局鼠标位置，点击互动和鼠标拖尾无效
- ❌ **Web 属性无法注入**：后端 CEF 通信在 Wayland 下受限

详细兼容性说明请查看 [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md)

### 其他问题

- **内存泄漏**：长期运行 Web 壁纸可能导致内存缓慢增长（底层引擎问题），建议定期重启
- **开发环境**：在 Arch Linux + Niri 下测试，其他环境可能需要调整

## 文档

- [CHANGELOG.md](CHANGELOG.md) - 版本更新日志
- [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) - 详细兼容性说明
- [docs/ADVANCED.md](docs/ADVANCED.md) - 高级功能和配置

## 技术栈

- **语言**：Python 3.10+
- **UI 框架**：PyGObject (GTK4 + Libadwaita)
- **系统托盘**：libayatana-appindicator
- **后端**：linux-wallpaperengine（C++）

## 贡献

欢迎提交 Issue 与 Pull Request！

- 功能建议和 Bug 报告请开 Issue
- 代码贡献请遵循现有代码风格
- 文档改进同样欢迎

## 许可证

GPLv3

---

**当前版本**：v0.9.1
**最后更新**：2026-02-07

*这是一个 Vibe Coding 的尝试项目*
