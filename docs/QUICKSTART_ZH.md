<a href="QUICKSTART.md">English</a> | <strong>中文</strong>

# 快速入门指南

本指南将帮助您在系统上设置并开始使用 Linux Wallpaper Engine (LWG) GUI。

## 系统要求

LWG GUI 需要现代 Linux 发行版，如 Ubuntu 22.04 或更高版本。应用程序依赖 WebKitGTK 作为网页视图。

在 Ubuntu 或 Debian 上安装网页视图依赖：
```bash
sudo apt install libwebkit2gtk-4.1-0
```

**Arch Linux / Manjaro:**
```bash
sudo pacman -S webkit2gtk-4.1
```

## 安装

### 1. 安装后端

该 GUI 作为 `linux-wallpaperengine` 渲染引擎的控制器。在运行应用程序之前，您需要安装此后端。

**Arch Linux 用户**可以从 AUR 安装：
```bash
yay -S linux-wallpaperengine
```

**其他发行版**应遵循[官方仓库](https://github.com/Almamu/linux-wallpaperengine)中的说明。

**通过运行以下命令验证安装**：
```bash
which linux-wallpaperengine
```
该命令应返回类似 `/usr/bin/linux-wallpaperengine` 的路径。

### 2. 下载 GUI

从[发布页面](https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/releases)获取最新的 AppImage。下载名为 `linux-wallpaperengine-gui-v2.0.0-x86_64.AppImage` 的文件。

## 首次启动

找到您刚刚下载的 AppImage 文件。右键单击它并选择**属性**，然后启用**允许将文件作为程序执行**选项。您也可以使用终端：
```bash
chmod +x linux-wallpaperengine-gui-v2.0.0-x86_64.AppImage
```
双击文件启动应用程序。它会自动扫描您的 Steam Workshop 文件夹以查找壁纸。

## 基本使用流程

### 应用壁纸
打开**库**选项卡查看您的壁纸。点击任何卡片查看其详细信息，然后点击**应用**按钮。

### 多显示器设置
使用顶部的屏幕选择器下拉菜单选择特定屏幕，或选择"All Screens"将同一壁纸应用于所有显示器。

### 系统托盘
应用程序会在系统托盘中放置一个图标。右键单击它可以快速暂停、恢复或更换壁纸。
