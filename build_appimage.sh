#!/bin/bash
set -e

# ================= 配置区 =================
APP_NAME="linux-wallpaperengine-gui"
# 获取当前 Python 版本 (例如 3.10)
PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
# ==========================================

# 如果是在 CI 环境下运行，自动下载工具
if [ "$CI" = "true" ]; then
    wget -c https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
    # wget -c https://raw.githubusercontent.com/linuxdeploy/linuxdeploy-plugin-gtk/master/linuxdeploy-plugin-gtk.sh
    chmod +x linuxdeploy-x86_64.AppImage linuxdeploy-plugin-gtk.sh
fi

# 1. 检查本地工具是否存在
if [ ! -f "./linuxdeploy-x86_64.AppImage" ] || [ ! -f "./linuxdeploy-plugin-gtk.sh" ]; then
    echo "❌ 错误: 找不到构建工具！"
    echo "请先在当前目录下载 'linuxdeploy-x86_64.AppImage' 和 'linuxdeploy-plugin-gtk.sh' 并赋予执行权限。"
    exit 1
fi

# 2. 准备 AppDir 目录
echo "📂 清理并创建 AppDir..."
rm -rf AppDir
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/128x128/apps
mkdir -p AppDir/usr/share/linux-wallpaperengine-gui
# 创建专门存放 Python 依赖的目录
mkdir -p AppDir/usr/lib/python${PY_VER}/site-packages

# 3. 复制 Python 源码
echo "📦 正在复制源码..."
# 确保复制的是 src 下的源码
if [ -d "src/py_GUI" ]; then
    cp -r src/py_GUI src/pic src/run_gui.py AppDir/usr/share/linux-wallpaperengine-gui/
elif [ -d "py_GUI" ]; then
    cp -r py_GUI pic run_gui.py AppDir/usr/share/linux-wallpaperengine-gui/
else
    echo "❌ 找不到源码目录，请检查路径！"
    exit 1
fi

# 4. 【关键】安装 Python 依赖到 AppDir 内部
echo "🐍 正在安装 Python 依赖..."
# 如果有 requirements.txt 就安装
if [ -f "requirements.txt" ]; then
    # --target 指定安装目录，让 pip 把库装进 AppDir 里
    python3 -m pip install -r requirements.txt --target=AppDir/usr/lib/python${PY_VER}/site-packages --upgrade
else
    echo "⚠️ 警告: 没有找到 requirements.txt，只打包源码。"
fi

# 5. 创建启动 Wrapper (关键修改：设置 PYTHONPATH)
echo "📝 创建启动脚本..."
cat > AppDir/usr/bin/launch_gui <<EOF
#!/bin/bash
# 获取 AppImage 挂载的根目录
HERE="\$(dirname "\$(readlink -f "\${0}")")"
export APPDIR="\${HERE}/../../"

# 【关键】把 AppDir 里的依赖库路径加入 PYTHONPATH
export PYTHONPATH="\$APPDIR/usr/lib/python${PY_VER}/site-packages:\$PYTHONPATH"

# 进入代码目录
cd "\$APPDIR/usr/share/linux-wallpaperengine-gui"

# 检查后端提示
if ! command -v linux-wallpaperengine &> /dev/null; then
    echo "⚠️ Warning: 'linux-wallpaperengine' backend not found in PATH."
fi

# 启动
exec python3 run_gui.py "\$@"
EOF
chmod +x AppDir/usr/bin/launch_gui
# 6. 配置桌面文件
echo "🖼️ 处理图标 (缩放至 512x512)..."

# 定义 512x512 的目标路径 (这是 AppImage 支持的最大标准尺寸)
ICON_DIR="AppDir/usr/share/icons/hicolor/512x512/apps"
mkdir -p "$ICON_DIR"

SOURCE_ICON="AppDir/usr/share/linux-wallpaperengine-gui/pic/icons/GUI_rounded.png"
TARGET_ICON="$ICON_DIR/${APP_NAME}.png"

# 使用 ffmpeg 进行缩放 (Arch 用户肯定有 ffmpeg)
if command -v ffmpeg >/dev/null; then
    ffmpeg -y -i "$SOURCE_ICON" -vf scale=512:512 "$TARGET_ICON" >/dev/null 2>&1
elif command -v convert >/dev/null; then
    # 如果有 ImageMagick 也可以用这个
    convert "$SOURCE_ICON" -resize 512x512 "$TARGET_ICON"
else
    echo "⚠️ 警告: 没找到 ffmpeg 或 convert，无法缩放图标！"
    echo "将尝试直接复制 (可能会再次报错)..."
    cp "$SOURCE_ICON" "$TARGET_ICON"
fi

# 生成 Desktop 文件
cat > AppDir/usr/share/applications/${APP_NAME}.desktop <<EOF
[Desktop Entry]
Name=Linux Wallpaper Engine
Exec=launch_gui
Icon=${APP_NAME}
Type=Application
Categories=Utility;GTK;
EOF

# 7. 开始打包
echo "🚀 开始生成 AppImage..."
export LINUXDEPLOY_PLUGIN_GTK_MODULES="canberra-gtk-module:canberra-gtk-module"
export NO_STRIP=true
export DEPLOY_GTK_VERSION=4

# 手动创建 AppRun 符号链接
ln -sf usr/bin/launch_gui AppDir/AppRun

# 【修改点】--icon-file 指向刚才缩放好的 512 图标
./linuxdeploy-x86_64.AppImage \
    --appdir AppDir \
    --plugin gtk \
    --desktop-file AppDir/usr/share/applications/${APP_NAME}.desktop \
    --icon-file "$TARGET_ICON" \
    --output appimage

echo "✅ 打包完成！"