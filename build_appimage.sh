#!/bin/bash
set -e

# ================= 配置区 =================
APP_NAME="linux-wallpaperengine-gui"
# 获取当前 Python 版本 (例如 3.10)
PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

# 从 pyproject.toml 自动提取版本号
if [ -f "pyproject.toml" ]; then
    VERSION=$(grep '^version[[:space:]]*=' pyproject.toml | head -n 1 | cut -d'"' -f2 | cut -d"'" -f2)
else
    VERSION="unknown"
fi
echo "📌 检测到当前版本号: v$VERSION"
# ==========================================

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
mkdir -p AppDir/usr/share/icons/hicolor/512x512/apps
mkdir -p AppDir/usr/share/linux-wallpaperengine-gui
# 创建专门存放 Python 依赖的目录
mkdir -p AppDir/usr/lib/python${PY_VER}/site-packages

# 3. 复制 Python 源码
echo "📦 正在复制源码..."
if [ -d "src/py_GUI" ]; then
    cp -r src/py_GUI src/pic src/run_gui.py AppDir/usr/share/linux-wallpaperengine-gui/
elif [ -d "py_GUI" ]; then
    cp -r py_GUI pic run_gui.py AppDir/usr/share/linux-wallpaperengine-gui/
else
    echo "❌ 找不到源码目录，请检查路径！"
    exit 1
fi

# ✅ 新增：清理可能残留在旧目录的幽灵文件！
rm -f AppDir/usr/share/linux-wallpaperengine-gui/tray-rs-bin

# ✅ 新增：现场编译 Rust 托盘并放入系统标准可执行目录
echo "🦀 正在现场编译 Rust 托盘引擎..."
cd tray_rs
if ! cargo build --release; then
    echo "❌ 致命错误: Rust 托盘引擎编译失败，请检查 Rust 环境或报错信息。"
    exit 1
fi
cd ..

if [ ! -f "tray_rs/target/release/tray-rs" ]; then
    echo "❌ 致命错误: 未找到已编译的托盘二进制文件。"
    exit 1
fi

# 将拷贝目标从 usr/share/... 改为 usr/bin/
cp tray_rs/target/release/tray-rs AppDir/usr/bin/tray-rs-bin
chmod +x AppDir/usr/bin/tray-rs-bin

# 【核弹级清理】彻底铲除所有 __pycache__ 和 .pyc，防止旧字节码污染 AppImage
echo "🧹 清除 Python 缓存幽灵..."
find AppDir -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find AppDir -name "*.pyc" -delete 2>/dev/null || true

# 4. 安装 Python 依赖到 AppDir 内部
echo "🐍 正在安装 Python 依赖..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt --target=AppDir/usr/lib/python${PY_VER}/site-packages --upgrade
else
    echo "⚠️ 警告: 没有找到 requirements.txt，只打包源码。"
fi

# 5. 【关键修补】强制植入托盘所需的 GTK3 和 Ayatana 依赖
echo "🔧 手动修补：植入托盘所需的 GTK3 和 Ayatana 依赖..."
mkdir -p AppDir/usr/lib/girepository-1.0

# # 拷贝 typelib 让 Python 能够 import 它们 (加 || true 防止 set -e 导致脚本意外中断)
# cp /usr/lib/girepository-1.0/Gtk-3.0.typelib AppDir/usr/lib/girepository-1.0/ 2>/dev/null || echo "⚠️ 未找到 GTK3 typelib"
# cp /usr/lib/girepository-1.0/Gdk-3.0.typelib AppDir/usr/lib/girepository-1.0/ 2>/dev/null || true
# cp /usr/lib/girepository-1.0/AyatanaAppIndicator3-0.1.typelib AppDir/usr/lib/girepository-1.0/ 2>/dev/null || echo "⚠️ 未找到 Ayatana typelib"

# # 拷贝底层的 Ayatana C语言动态库
# cp /usr/lib/libayatana-appindicator3.so* AppDir/usr/lib/ 2>/dev/null || echo "⚠️ 未找到 libayatana-appindicator3.so"

# 6. 【终极绝杀】将图标 Base64 内嵌进 Python 模块，彻底绕开 FUSE 路径问题
echo "🔐 正在将图标转码为 Python 内存数据..."
ICON_TO_EMBED="AppDir/usr/share/linux-wallpaperengine-gui/pic/icons/GUI_rounded.png"
EMBED_TARGET="AppDir/usr/share/linux-wallpaperengine-gui/py_GUI/embedded_icon.py"

python3 - <<PYEOF
import base64
try:
    with open("${ICON_TO_EMBED}", "rb") as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    with open("${EMBED_TARGET}", "w") as f:
        f.write("# Auto-generated at build time. DO NOT EDIT.\n")
        f.write("ICON_DATA = b\"\"\"" + data + "\"\"\"\n")
    print("✅ 图标 Base64 内嵌成功！")
except Exception as e:
    print(f"❌ 图标内嵌失败: {e}")
PYEOF

# 7. 创建启动 Wrapper
echo "📝 创建启动脚本..."
cat > AppDir/usr/bin/launch_gui <<'EOF'
#!/bin/bash

# 1. 确定 APPDIR 挂载点
if [ -z "$APPDIR" ]; then
    SCRIPT_REAL="$(readlink -f "${0}")"
    export APPDIR="$(dirname "$(dirname "$(dirname "$SCRIPT_REAL")")")"
fi

# ╔═════════════════════════════════════════════════════════════╗
# ║  在 FUSE 挂载还 100% 存活时，提前把 Rust 二进制复制到 /tmp  ║
# ║  这是唯一能绕过 FUSE 挂载点在 Python 启动后可能被回收的方法 ║
# ╚═════════════════════════════════════════════════════════════╝
TRAY_SRC="$APPDIR/usr/bin/tray-rs-bin"
TRAY_DEST="/tmp/lwg-tray-rs-$(id -u)"

if [ -f "$TRAY_SRC" ]; then
    # 只有当目标不存在，或者 AppImage 里的源文件更新时才复制
    if [ ! -f "$TRAY_DEST" ] || [ "$TRAY_SRC" -nt "$TRAY_DEST" ]; then
        cp "$TRAY_SRC" "$TRAY_DEST" && chmod 755 "$TRAY_DEST"
    fi
    # 导出一个显式的环境变量，供 Python 直接使用
    export LWG_TRAY_BIN="$TRAY_DEST"
else
    echo "[launch_gui] WARNING: tray-rs-bin not found at $TRAY_SRC" >&2
fi

# 2. 设置标准环境变量
export PATH="$APPDIR/usr/bin:$PATH"
export PYTHONPATH="$APPDIR/usr/lib/python__PY_VER__/site-packages:$APPDIR/usr/share/linux-wallpaperengine-gui:$PYTHONPATH"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="/tmp/lwg-pycache-$(id -u)"

export LWG_IPC_SOCKET="lwg-ipc-$(id -u)"

cd "$APPDIR/usr/share/linux-wallpaperengine-gui"
exec python3 run_gui.py "$@"
EOF

# 替换版本号并赋予权限
sed -i "s/__PY_VER__/${PY_VER}/g" AppDir/usr/bin/launch_gui
chmod +x AppDir/usr/bin/launch_gui

# 8. 配置桌面文件
echo "🖼️ 处理图标 (缩放至 512x512)..."
ICON_DIR="AppDir/usr/share/icons/hicolor/512x512/apps"
mkdir -p "$ICON_DIR"
SOURCE_ICON="AppDir/usr/share/linux-wallpaperengine-gui/pic/icons/GUI_rounded.png"
TARGET_ICON="$ICON_DIR/${APP_NAME}.png"

if command -v ffmpeg >/dev/null; then
    ffmpeg -y -i "$SOURCE_ICON" -vf scale=512:512 "$TARGET_ICON" >/dev/null 2>&1
elif command -v convert >/dev/null; then
    convert "$SOURCE_ICON" -resize 512x512 "$TARGET_ICON"
else
    echo "⚠️ 警告: 没找到 ffmpeg 或 convert，无法缩放图标！"
    cp "$SOURCE_ICON" "$TARGET_ICON"
fi

echo "📦 植入托盘专用小图标..."
# 源文件路径
TRAY_SRC_SMALL="AppDir/usr/share/linux-wallpaperengine-gui/pic/icons/gui_tray_rounded.png"
TRAY_STOPPED_SMALL="AppDir/usr/share/linux-wallpaperengine-gui/pic/icons/gui_tray_rounded-stopped.png"

# 目标文件名 (注意命名要和 Python 代码里的逻辑一致)
cp "$TRAY_SRC_SMALL" "$ICON_DIR/com.wallpaperengine.tray.png"
cp "$TRAY_STOPPED_SMALL" "$ICON_DIR/com.wallpaperengine.tray-stopped.png"

# 满足 AppImage 根目录规范
cp "$TARGET_ICON" AppDir/${APP_NAME}.png
cp "$TARGET_ICON" AppDir/.DirIcon

cat > AppDir/usr/share/applications/${APP_NAME}.desktop <<EOF
[Desktop Entry]
Name=Wallpaper Engine GUI
Exec=launch_gui %U
Icon=${APP_NAME}
Type=Application
Categories=Utility;GTK;
StartupWMClass=com.wallpaperengine.gui
Terminal=false
EOF

# 9. 开始打包
echo "🚀 开始生成 AppImage..."
# export LINUXDEPLOY_PLUGIN_GTK_MODULES="canberra-gtk-module:canberra-gtk-module"
unset LINUXDEPLOY_PLUGIN_GTK_MODULES
export NO_STRIP=true
export DEPLOY_GTK_VERSION=4

# 通过环境变量 OUTPUT 强制规范 AppImage 的输出文件名
export OUTPUT="${APP_NAME}-${VERSION}-x86_64.AppImage"

ln -sf usr/bin/launch_gui AppDir/AppRun

# ... 前面的代码保持不变 ...

# ✅ 打包前验尸：确认文件真的进去了
echo "================= 打包前极度硬核验尸 ================="
ls -la AppDir/usr/bin/tray-rs-bin || echo "❌ 打包前就丢了！"

./linuxdeploy-x86_64.AppImage \
    --appdir AppDir \
    --plugin gtk \
    --desktop-file AppDir/usr/share/applications/${APP_NAME}.desktop \
    --icon-file "$TARGET_ICON" \
    --output appimage

# ✅ 打包后验尸：确认没有被 GTK 插件偷删
echo "================= 打包后极度硬核验尸 ================="
ls -la AppDir/usr/bin/tray-rs-bin 2>&1 || echo "❌ 卧槽！文件在打包后被 GTK 插件吃掉了！"

echo "✅ 打包完成！文件已生成: ${OUTPUT}"