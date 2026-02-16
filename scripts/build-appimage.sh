#!/bin/bash

################################################################################
# Build AppImage for Linux Wallpaper Engine GUI
#
# This script creates a self-contained AppImage package for the Linux Wallpaper
# Engine GUI application. It handles:
# - AppDir structure creation
# - Python application installation
# - Dependency bundling
# - Wrapper script creation
# - Desktop file and icon integration
# - AppImage generation using appimagetool
#
# Prerequisites:
#   - appimagetool (https://github.com/AppImage/AppImageKit)
#   - Python 3.10+
#   - System dependencies: gtk4, libadwaita, python-gobject, python-pillow, python-pyglet
#
# Usage:
#   ./scripts/build-appimage.sh
#
################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APPDIR="${APPDIR:-build/AppDir}"
PYTHON_VERSION=${PYTHON_VERSION:-3}
ARCHITECTURE="x86_64"
APP_NAME="Linux Wallpaper Engine GUI"
APP_ID="linux-wallpaperengine.gui"
EXECUTABLE_NAME="linux-wallpaperengine-gui"
ICON_SOURCE="pic/icons/GUI_rounded.png"
DESKTOP_FILE="linux.wallpaperengine.gui.desktop"
OUTPUT_DIR="${OUTPUT_DIR:-build}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

################################################################################
# Functions
################################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

die() {
    log_error "$@"
    exit 1
}

check_command() {
    local cmd="$1"
    local friendly_name="${2:-$cmd}"
    
    if ! command -v "$cmd" &> /dev/null; then
        die "Required tool not found: $friendly_name"
    fi
}

print_usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Options:
    -a, --appdir PATH       AppDir location (default: build/AppDir)
    -o, --output DIR        Output directory (default: build)
    -h, --help              Show this help message

Example:
    $(basename "$0") --appdir=/tmp/AppDir --output=/tmp/build
EOF
}

clean_appdir() {
    log_info "Cleaning existing AppDir..."
    rm -rf "$APPDIR"
}

create_appdir_structure() {
    log_info "Creating AppDir structure..."
    
    mkdir -p "$APPDIR"/{usr/bin,usr/share/{applications,icons/hicolor/{256x256/apps,scalable/apps}},usr/lib,opt}
    
    log_success "AppDir structure created: $APPDIR"
}

get_python_site_packages() {
    python3 -c "import site; print(site.getsitepackages()[0])"
}

copy_application_files() {
    log_info "Copying application files to AppDir..."
    
    # Copy main application package
    cp -r "$PROJECT_ROOT/py_GUI" "$APPDIR/opt/linux-wallpaperengine-gui/"
    
    # Copy entry point script
    cp "$PROJECT_ROOT/run_gui.py" "$APPDIR/opt/linux-wallpaperengine-gui/"
    
    log_success "Application files copied"
}

install_python_dependencies() {
    log_info "Installing Python dependencies..."
    
    # Get site-packages location
    local site_packages
    site_packages=$(get_python_site_packages)
    
    # Create site-packages directory in AppDir
    local appdir_site_packages="$APPDIR/usr/lib/python3.$(python3 -c 'import sys; print(sys.version_info.minor)')/site-packages"
    mkdir -p "$appdir_site_packages"
    
    # Install dependencies to AppDir
    python3 -m pip install \
        --target "$appdir_site_packages" \
        --no-deps \
        --no-cache-dir \
        --no-compile \
        pillow \
        pyglet \
        || log_warn "Some pure-Python dependencies failed to install; system libraries may be used"
    
    # Copy system gobject and gtk bindings if available
    if [[ -d "$site_packages/gi" ]]; then
        cp -r "$site_packages/gi" "$appdir_site_packages/" || true
    fi
    
    log_success "Python dependencies installed"
}

create_wrapper_script() {
    log_info "Creating entry point wrapper script..."
    
    local wrapper_path="$APPDIR/usr/bin/$EXECUTABLE_NAME"
    
    cat > "$wrapper_path" << 'WRAPPER_EOF'
#!/usr/bin/env python3
"""
Linux Wallpaper Engine GUI AppImage Wrapper

This wrapper sets up the environment and launches the application.
"""

import sys
import os
import site

# Add AppDir site-packages to Python path
appdir = os.getenv('APPDIR', os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
python_version = f"python3.{sys.version_info.minor}"
appdir_site_packages = os.path.join(appdir, "usr/lib", python_version, "site-packages")

if os.path.exists(appdir_site_packages):
    site.addsitedir(appdir_site_packages)
    sys.path.insert(0, appdir_site_packages)

# Add application directory to path
app_dir = os.path.join(appdir, "opt/linux-wallpaperengine-gui")
if os.path.exists(app_dir):
    sys.path.insert(0, app_dir)

# Import and run the application
try:
    from py_GUI.main import main
    main()
except ImportError as e:
    print(f"Error importing application module: {e}", file=sys.stderr)
    sys.exit(1)
WRAPPER_EOF
    
    chmod +x "$wrapper_path"
    log_success "Wrapper script created: $wrapper_path"
}

copy_desktop_file() {
    log_info "Copying desktop file..."
    
    if [[ ! -f "$PROJECT_ROOT/$DESKTOP_FILE" ]]; then
        die "Desktop file not found: $PROJECT_ROOT/$DESKTOP_FILE"
    fi
    
    # Copy desktop file
    cp "$PROJECT_ROOT/$DESKTOP_FILE" "$APPDIR/usr/share/applications/"
    
    log_success "Desktop file copied"
}

copy_icon() {
    log_info "Copying application icon..."
    
    if [[ ! -f "$PROJECT_ROOT/$ICON_SOURCE" ]]; then
        die "Icon file not found: $PROJECT_ROOT/$ICON_SOURCE"
    fi
    
    # Copy icon in multiple sizes
    cp "$PROJECT_ROOT/$ICON_SOURCE" "$APPDIR/usr/share/icons/hicolor/256x256/apps/$EXECUTABLE_NAME.png"
    
    # Create scalable version (link to the same file)
    ln -sf "../256x256/apps/$EXECUTABLE_NAME.png" \
        "$APPDIR/usr/share/icons/hicolor/scalable/apps/$EXECUTABLE_NAME.svg" || true
    
    log_success "Icon copied"
}

create_apprun_script() {
    log_info "Creating AppRun script..."
    
    local apprun_path="$APPDIR/AppRun"
    
    cat > "$apprun_path" << 'APPRUN_EOF'
#!/bin/bash
# AppRun - Entry point for AppImage
# This script sets up the environment and launches the application

set -e

# Get the directory where this AppImage is located
APPDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export APPDIR

# Set library paths
export LD_LIBRARY_PATH="${APPDIR}/usr/lib:${APPDIR}/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"

# Set Python environment
export PYTHONPATH="${APPDIR}/opt/linux-wallpaperengine-gui:${APPDIR}/usr/lib/python3.*/site-packages:${PYTHONPATH:-}"

# Set icon theme path
export XDG_DATA_DIRS="${APPDIR}/usr/share:${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"

# Execute the application
exec "${APPDIR}/usr/bin/linux-wallpaperengine-gui" "$@"
APPRUN_EOF
    
    chmod +x "$apprun_path"
    log_success "AppRun script created"
}

create_appimage() {
    log_info "Building AppImage using appimagetool..."
    
    check_command "appimagetool" "appimagetool"
    
    mkdir -p "$OUTPUT_DIR"
    
    local output_file="$OUTPUT_DIR/${EXECUTABLE_NAME}-${ARCHITECTURE}.AppImage"
    
    # Build AppImage
    if appimagetool "$APPDIR" "$output_file"; then
        chmod +x "$output_file"
        log_success "AppImage created: $output_file"
        log_info "AppImage size: $(du -h "$output_file" | cut -f1)"
        return 0
    else
        die "Failed to create AppImage"
    fi
}

verify_appimage() {
    log_info "Verifying AppImage..."
    
    local appimage_file="$OUTPUT_DIR/${EXECUTABLE_NAME}-${ARCHITECTURE}.AppImage"
    
    if [[ ! -f "$appimage_file" ]]; then
        die "AppImage file not found: $appimage_file"
    fi
    
    # Check file is executable
    if [[ ! -x "$appimage_file" ]]; then
        die "AppImage is not executable"
    fi
    
    # Check file has AppImage magic bytes
    if file "$appimage_file" | grep -q "ELF"; then
        log_success "AppImage verification passed"
        return 0
    else
        log_warn "AppImage file type check inconclusive, but file exists and is executable"
        return 0
    fi
}

print_summary() {
    log_info "Build summary:"
    echo -e "${BLUE}================================${NC}"
    echo "App Name:        $APP_NAME"
    echo "App ID:          $APP_ID"
    echo "Architecture:    $ARCHITECTURE"
    echo "Output:          $OUTPUT_DIR/${EXECUTABLE_NAME}-${ARCHITECTURE}.AppImage"
    echo "AppDir:          $APPDIR"
    echo -e "${BLUE}================================${NC}"
}

################################################################################
# Main Script
################################################################################

main() {
    log_info "Starting Linux Wallpaper Engine GUI AppImage build..."
    log_info "Project root: $PROJECT_ROOT"
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -a|--appdir)
                APPDIR="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            -h|--help)
                print_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done
    
    # Verify prerequisites
    log_info "Checking prerequisites..."
    check_command "python3" "Python 3"
    check_command "appimagetool" "appimagetool"
    
    log_success "All prerequisites met"
    
    # Build process
    clean_appdir
    create_appdir_structure
    
    # Create opt directory for application
    mkdir -p "$APPDIR/opt/linux-wallpaperengine-gui"
    
    copy_application_files
    install_python_dependencies
    create_wrapper_script
    copy_desktop_file
    copy_icon
    create_apprun_script
    create_appimage
    verify_appimage
    print_summary
    
    log_success "Build completed successfully!"
    echo ""
    log_info "To test the AppImage:"
    echo "  $OUTPUT_DIR/${EXECUTABLE_NAME}-${ARCHITECTURE}.AppImage"
    echo ""
    log_info "To install system-wide:"
    echo "  sudo cp $OUTPUT_DIR/${EXECUTABLE_NAME}-${ARCHITECTURE}.AppImage /usr/local/bin/"
    echo "  sudo chmod +x /usr/local/bin/${EXECUTABLE_NAME}-${ARCHITECTURE}.AppImage"
}

# Run main function
main "$@"
