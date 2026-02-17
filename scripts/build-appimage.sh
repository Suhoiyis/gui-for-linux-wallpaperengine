#!/bin/bash

# AppImage build script for Linux Wallpaper Engine GUI
# This script builds an AppImage package that works on most modern Linux distributions

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the project root
if [ ! -f "run_gui.py" ] || [ ! -d "py_GUI" ]; then
    print_error "This script must be run from the project root directory"
    exit 1
fi

# Get version from const.py
VERSION=$(python3 -c "from py_GUI.const import VERSION; print(VERSION)")

print_status "Building AppImage for Linux Wallpaper Engine GUI v$VERSION"

# Set architecture (required by appimagetool)
ARCH="${ARCH:-x86_64}"
export ARCH
print_status "Target architecture: $ARCH"

# Create build directory
BUILD_DIR="build"
APPDIR="$BUILD_DIR/AppDir"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/lib"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

print_status "Created AppDir structure"

# Copy application files
cp -r py_GUI "$APPDIR/usr/lib/"
cp -r pic "$APPDIR/usr/lib/"
cp run_gui.py "$APPDIR/usr/bin/linux-wallpaperengine-gui"

# Make the main script executable
chmod +x "$APPDIR/usr/bin/linux-wallpaperengine-gui"

print_status "Copied application files"

# Copy desktop file to AppDir root (required by appimagetool)
cp linux.wallpaperengine.gui.desktop "$APPDIR/"

# Also copy to usr/share/applications for system integration
cp linux.wallpaperengine.gui.desktop "$APPDIR/usr/share/applications/"

# Copy icon - must match the Icon= value in desktop file (linux-wallpaperengine-gui)
cp pic/icons/GUI_rounded.png "$APPDIR/usr/share/icons/hicolor/256x256/apps/linux-wallpaperengine-gui.png"
# Also copy to AppDir root with correct name for appimagetool
cp pic/icons/GUI_rounded.png "$APPDIR/linux-wallpaperengine-gui.png"

print_status "Copied desktop integration files"

# Create AppRun script with better error handling
cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "$0")")"
export PYTHONPATH="$HERE/usr/lib:$HERE:$PYTHONPATH"
export PATH="$HERE/usr/bin:$PATH"
export APPDIR="$HERE"

# Execute the application
exec python3 "$HERE/usr/bin/linux-wallpaperengine-gui" "$@"
EOF
chmod +x "$APPDIR/AppRun"

print_status "Created AppRun script"

# Download appimagetool if not present
if ! command -v appimagetool &> /dev/null; then
    print_warning "appimagetool not found, downloading..."
    wget -q https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage -O /tmp/appimagetool
    chmod +x /tmp/appimagetool
    APPIMAGETOOL="/tmp/appimagetool"
else
    APPIMAGETOOL="appimagetool"
fi

# Build AppImage
print_status "Building AppImage..."
$APPIMAGETOOL "$APPDIR" "$BUILD_DIR/linux-wallpaperengine-gui-$VERSION-x86_64.AppImage"

print_status "AppImage built successfully!"
print_status "Output: $BUILD_DIR/linux-wallpaperengine-gui-$VERSION-x86_64.AppImage"
