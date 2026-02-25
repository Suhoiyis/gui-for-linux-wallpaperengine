# Linux Wallpaper Engine GUI - Rust 版本
## 启动与打包指南

---

## 🚀 一、快速启动

### 1.1 开发环境运行

```bash
cd /home/yua/suw/lwg-rs

# 编译 Release 版本
cargo build --release

# 运行主程序
./target/release/lwg-gui

# 或运行托盘进程
./target/release/tray-rs
```

### 1.2 调试模式

```bash
# 启用调试日志
export LWG_DEBUG=1
cargo run --release --bin lwg-gui

# 查看详细日志
export RUST_LOG=debug
cargo run --release --bin lwg-gui
```

---

## 📦 二、Arch Linux 打包（AUR）

### 2.1 前置要求

```bash
sudo pacman -S rust cargo git base-devel gtk4 libadwaita
```

### 2.2 使用 PKGBUILD 打包

```bash
# 1. 进入目录
cd /home/yua/suw/lwg-rs

# 2. 构建包
makepkg -si

# 3. 安装后运行
lwg-gui
```

### 2.3 提交到 AUR

```bash
# 1. 克隆 AUR 仓库
git clone ssh://aur@aur.archlinux.org/linux-wallpaperengine-gui-rust.git
cd linux-wallpaperengine-gui-rust

# 2. 复制 PKGBUILD
cp /home/yua/suw/lwg-rs/PKGBUILD .

# 3. 生成 .SRCINFO
makepkg --printsrcinfo > .SRCINFO

# 4. 提交
git add PKGBUILD .SRCINFO
git commit -m "Initial package"
git push
```

---

## 🍎 三、AppImage 打包

### 3.1 下载工具

```bash
# 下载 linuxdeploy
wget https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
chmod +x linuxdeploy-x86_64.AppImage
```

### 3.2 创建构建脚本

```bash
cat > build-appimage.sh << 'SCRIPT'
#!/bin/bash
set -e

# 1. 编译
cd lwg-rs && cargo build --release && cd ..

# 2. 创建 AppDir
rm -rf AppDir
mkdir -p AppDir/usr/{bin,share/icons/hicolor/512x512/apps,share/applications}

# 3. 复制文件
cp lwg-rs/target/release/lwg-gui AppDir/usr/bin/
cp lwg-rs/target/release/tray-rs AppDir/usr/bin/

# 4. 复制资源
cp lwg-rs/resources/icon.png AppDir/usr/share/icons/hicolor/512x512/apps/
cp lwg-rs/resources/*.desktop AppDir/usr/share/applications/

# 5. 创建 AppRun
cat > AppDir/AppRun << 'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
exec "$HERE/usr/bin/lwg-gui" "$@"
EOF
chmod +x AppDir/AppRun

# 6. 复制桌面文件和图标到根目录
cp AppDir/usr/share/applications/*.desktop AppDir/
cp AppDir/usr/share/icons/hicolor/512x512/apps/*.png AppDir/

# 7. 打包
./linuxdeploy-x86_64.AppImage --appdir AppDir --output appimage

echo "✅ AppImage 构建完成"
SCRIPT

chmod +x build-appimage.sh
```

### 3.3 执行构建

```bash
./build-appimage.sh

# 输出
# Linux-Wallpaper-Engine-Gui-2.0.0-x86_64.AppImage

# 运行测试
chmod +x Linux-Wallpaper-Engine-Gui-2.0.0-x86_64.AppImage
./Linux-Wallpaper-Engine-Gui-2.0.0-x86_64.AppImage
```

---

## 🔧 四、依赖说明

### 运行时依赖
- gtk4
- libadwaita
- linux-wallpaperengine（后端）

### 构建时依赖
- rust >= 1.75
- cargo >= 1.75
- base-devel

---

## ✅ 五、验证安装

```bash
# 检查安装
which lwg-gui
which tray-rs

# 检查桌面文件
ls /usr/share/applications/com.wallpaperengine.gui.desktop

# 检查图标
ls /usr/share/icons/hicolor/512x512/apps/com.wallpaperengine.gui.png

# 功能测试
lwg-gui
```

---

## 🐛 六、故障排除

**托盘图标不显示**：
```bash
ps aux | grep tray-rs
tray-rs  # 手动启动
```

**GTK 主题警告**：
```bash
# 忽略警告，不影响功能
# 或安装主题
sudo pacman -S adwaita-icon-theme
```

**Wayland 问题**：
```bash
export GDK_BACKEND=x11
lwg-gui
```

---

Happy Wallpapering! 🎨
