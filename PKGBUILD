# Maintainer: Suhoiyis <3218818428@qq.com>
pkgname=linux-wallpaperengine-gui
pkgver=0.10.6
pkgrel=1
pkgdesc="A modern GTK4 graphical interface for managing Steam Workshop live wallpapers"
arch=('any')
url="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine"
license=('GPL3')
depends=('python' 'python-gobject' 'gtk4' 'libadwaita' 'libayatana-appindicator' 'linux-wallpaperengine')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')
# source=("git+https://github.com/Suhoiyis/gui-for-linux-wallpaperengine.git")
# 注意文件名要和你刚才 tar 命令生成的一致
source=("linux-wallpaperengine-gui-0.10.6.tar.gz")
# 如果是在本地开发目录直接构建，可以忽略 source 的校验，或者使用 git 来源

sha256sums=('SKIP')

prepare() {
    # 如果有需要编译前的准备工作放在这里
    cd "$srcdir/.."
}

build() {
    cd "$srcdir/.."
    python -m build --wheel --no-isolation
}

package() {
    # 1. 创建程序的“家”目录
    # 我们把所有东西都放在 /usr/share/linux-wallpaperengine-gui 下
    local app_dir="/usr/share/$pkgname"
    mkdir -p "$pkgdir$app_dir"

    cd "$srcdir" # 确保进入源码目录

    # 2. 【关键】直接拷贝所有代码和资源文件
    # 这样 py_GUI 和 pic 就依然在一起，相对路径就不会报错了
    cp -r py_GUI pic run_gui.py "$pkgdir$app_dir/"

    # 3. 创建一个启动脚本 wrapper
    # 这个脚本会先 cd 到程序目录，然后再运行 python
    # 这完美解决了“找不到图片”的问题
    mkdir -p "$pkgdir/usr/bin"
    cat > "$pkgdir/usr/bin/$pkgname" <<EOF
#!/bin/sh
cd "$app_dir"
exec python3 run_gui.py "\$@"
EOF
    chmod +x "$pkgdir/usr/bin/$pkgname"

    # 4. 安装图标 (给桌面快捷方式用)
    install -Dm644 pic/icons/GUI_rounded.png "$pkgdir/usr/share/icons/hicolor/128x128/apps/$pkgname.png"

    # 5. 创建 .desktop 文件
    mkdir -p "$pkgdir/usr/share/applications"
    cat > "$pkgdir/usr/share/applications/$pkgname.desktop" <<EOF
[Desktop Entry]
Name=Linux Wallpaper Engine
Comment=Manage Steam Workshop live wallpapers
Exec=$pkgname --show
Icon=$pkgname
Terminal=false
Type=Application
Categories=Utility;GTK;
EOF
}