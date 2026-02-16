# Maintainer: Your Name <your.email@example.com>
pkgname=linux-wallpaperengine-gui
pkgver=0.10.6
pkgrel=1
pkgdesc="Interactive wallpaper management for Linux using Wallpaper Engine assets"
arch=('x86_64')
url="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine"
license=('GPL3')
depends=(
    'gtk4'
    'libadwaita'
    'python>=3.10'
    'python-gobject'
    'python-pillow'
    'mpv'
)
optdepends=(
    'python-pyglet: for advanced rendering features'
    'wallpaper-engine-libwrap: backend support for live wallpapers'
)
makedepends=(
    'python-build'
    'python-installer'
    'python-wheel'
    'python-setuptools'
)
provides=("${pkgname}")
conflicts=("${pkgname}")
source=()
sha256sums=()

prepare() {
    # No source to extract, working with local project files
    :
}

build() {
    # Project is a script-based application, no build needed
    :
}

package() {
    # Create application directory
    install -d "$pkgdir/opt/linux-wallpaperengine-gui"
    
    # Install main application files
    install -Dm755 "${startdir}/run_gui.py" "$pkgdir/opt/linux-wallpaperengine-gui/run_gui.py"
    cp -r "${startdir}/py_GUI" "$pkgdir/opt/linux-wallpaperengine-gui/"
    cp -r "${startdir}/pic" "$pkgdir/opt/linux-wallpaperengine-gui/"
    
    # Install desktop file
    install -Dm644 "${startdir}/linux.wallpaperengine.gui.desktop" "$pkgdir/usr/share/applications/linux.wallpaperengine.gui.desktop"
    
    # Install icon
    install -Dm644 "${startdir}/pic/icons/GUI_rounded.png" "$pkgdir/usr/share/icons/hicolor/256x256/apps/linux-wallpaperengine-gui.png"
    
    # Install executable wrapper
    install -Dm755 /dev/stdin "$pkgdir/usr/bin/linux-wallpaperengine-gui" << 'EOF'
#!/usr/bin/env python3
import sys
import os

# Add application directory to Python path
sys.path.insert(0, '/opt/linux-wallpaperengine-gui')

# Run the application
from py_GUI.main import main
main()
EOF
}
