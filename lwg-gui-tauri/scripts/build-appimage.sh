#!/usr/bin/env bash
# Build AppImage with WebKitGTK compatibility fix
# This script wraps the standard Tauri build and injects a custom AppRun
# to fix blank screen issues on rolling-release distros (Arch, Fedora 40+)

set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SRC_TAURI="$PROJECT_ROOT/src-tauri"

echo "🔨 Building Tauri AppImage..."
cd "$PROJECT_ROOT"
NO_STRIP=1 npm run tauri:build

# Find the AppDir
APPDIR=$(find "$SRC_TAURI/target/release/bundle/appimage" -name "*.AppDir" -type d 2>/dev/null | head -1)

if [ -z "$APPDIR" ]; then
    echo "❌ ERROR: AppDir not found after build"
    exit 1
fi

echo "📁 Found AppDir: $APPDIR"

# Inject custom AppRun script
echo "🔧 Injecting custom AppRun script..."
cp "$SCRIPT_DIR/appimage-webkit-fix.sh" "$APPDIR/AppRun"
chmod +x "$APPDIR/AppRun"

# Fix symlinks if needed
cd "$APPDIR"

if [ -L .DirIcon ]; then
    rm -f .DirIcon
    ICON=$(find usr/share/icons -name "*.png" -type f 2>/dev/null | sort -r | head -1)
    if [ -n "$ICON" ]; then
        ln -s "$ICON" .DirIcon
        echo "  Fixed .DirIcon symlink"
    fi
fi

DESKTOP_FILE=$(ls usr/share/applications/*.desktop 2>/dev/null | head -1)
if [ -n "$DESKTOP_FILE" ] && [ -L "$(basename "$DESKTOP_FILE")" ]; then
    rm -f "$(basename "$DESKTOP_FILE")"
    ln -s "$DESKTOP_FILE" "$(basename "$DESKTOP_FILE")"
    echo "  Fixed .desktop symlink"
fi

cd - > /dev/null

# Repackage AppImage using appimagetool
echo "📦 Repackaging AppImage with custom AppRun..."
ARCH=x86_64
APPIMAGETOOL="appimagetool-${ARCH}.AppImage"
APPIMAGE_TOOL_PATH="/tmp/${APPIMAGETOOL}"

if [ ! -f "$APPIMAGE_TOOL_PATH" ]; then
    echo "  Downloading appimagetool..."
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/${APPIMAGETOOL}" -O "$APPIMAGE_TOOL_PATH"
    chmod +x "$APPIMAGE_TOOL_PATH"
fi

# Find old AppImage and remove it
OLD_APPIMAGE=$(find "$SRC_TAURI/target/release/bundle/appimage" -name "*.AppImage" -type f | head -1)
if [ -n "$OLD_APPIMAGE" ]; then
    rm -f "$OLD_APPIMAGE"
fi

# Repackage
ARCH=x86_64 "$APPIMAGE_TOOL_PATH" --no-appstream "$APPDIR" "$OLD_APPIMAGE" 2>&1 || {
    echo "❌ Failed to repackage AppImage"
    exit 1
}

echo "✅ AppImage built with WebKitGTK compatibility fix!"
echo "   Location: $OLD_APPIMAGE"
echo "   Size: $(du -sh "$OLD_APPIMAGE" | cut -f1)"