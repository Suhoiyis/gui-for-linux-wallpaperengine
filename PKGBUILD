# Maintainer: Suhoiyis
pkgname=linux-wallpaperengine-gui
pkgver=0.11.2
pkgrel=1
pkgdesc="A modern GTK4 GUI for managing dynamic wallpapers from Steam Workshop on Linux"
arch=('any')
url="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine"
license=('GPL3')

# 【终极修复 1】补全了托盘生存必须的 gtk3 和 libayatana-appindicator
depends=('python' 'python-gobject' 'gtk4' 'libadwaita' 'python-pillow' 'linux-wallpaperengine')
makedepends=('git' 'cargo')

# 标准的 Arch 打包来源写法，直接拉取对应的 tag
source=("git+https://github.com/Suhoiyis/gui-for-linux-wallpaperengine.git#tag=v${pkgver}")
# source=("git+https://github.com/Suhoiyis/gui-for-linux-wallpaperengine.git#branch=feature/tray")
# source=()
sha256sums=('SKIP')

build() {
    cd "gui-for-linux-wallpaperengine/tray_rs"
    # 现场编译极致优化的 release 版本
    cargo build --release
}

package() {
    cd "gui-for-linux-wallpaperengine"

    # 1. 建立目录
    install -dm755 "$pkgdir/usr/share/$pkgname"
    install -dm755 "$pkgdir/usr/bin"
    install -dm755 "$pkgdir/usr/share/applications"
    install -dm755 "$pkgdir/usr/share/icons/hicolor/512x512/apps"

    # 2. 拷贝源码和资源 (已修复致命断行)
    cp -r py_GUI pic run_gui.py "$pkgdir/usr/share/$pkgname/"

    install -Dm755 tray_rs/target/release/tray-rs "$pkgdir/usr/bin/tray-rs-bin"

    # 3. 抹杀源码包自带的幽灵缓存 (已修复断行)
    find "$pkgdir/usr/share/$pkgname" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$pkgdir/usr/share/$pkgname" -name "*.pyc" -delete 2>/dev/null || true

    # 4. 创建带缓存重定向黑魔法和 IPC 通信的启动 Wrapper
    cat << EOF > "$pkgdir/usr/bin/$pkgname"
#!/bin/bash
export PYTHONPATH="/usr/share/$pkgname:\$PYTHONPATH"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="/tmp/${pkgname}-pycache-\$(id -u)"
export LWG_IPC_SOCKET="/tmp/lwg-ipc-\$(id -u).sock"

cd "/usr/share/$pkgname" || exit 1

# 绝不使用绝对路径，防止触发 pkill 自杀！
exec /usr/bin/python3 run_gui.py "\$@"
EOF

    chmod +x "$pkgdir/usr/bin/$pkgname"

    # 5. 配置桌面入口
    ## 1. 主程序图标 (大图，给 Dock 栏和应用列表用) - 保持不变
    install -Dm644 pic/icons/GUI_rounded.png "$pkgdir/usr/share/icons/hicolor/512x512/apps/com.wallpaperengine.gui.png"

    ## 2. 托盘图标 (小图，给系统托盘专用) - 改用小图文件！
    ## 注意：为了符合 Linux 规范，小图最好放到适合它的尺寸目录，比如 64x64，但放 512 也能用，为了稳妥先放 512 或者 scalable
    install -Dm644 pic/icons/gui_tray_rounded.png "$pkgdir/usr/share/icons/hicolor/512x512/apps/com.wallpaperengine.tray.png"
    
    ## 3. 托盘停止图标 (小图黑白版)
    install -Dm644 pic/icons/gui_tray_rounded-stopped.png "$pkgdir/usr/share/icons/hicolor/512x512/apps/com.wallpaperengine.tray-stopped.png"
    


    cat << EOF > "$pkgdir/usr/share/applications/com.wallpaperengine.gui.desktop"
[Desktop Entry]
Name=Wallpaper Engine GUI
Exec=$pkgname %U
Icon=com.wallpaperengine.gui
Type=Application
Categories=Utility;GTK;
StartupWMClass=com.wallpaperengine.gui
Terminal=false
EOF

    # (可选) 将协议和文档安装到系统标准路径
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}