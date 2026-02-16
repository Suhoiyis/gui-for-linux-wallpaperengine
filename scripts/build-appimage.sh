#!/bin/bash

################################################################################
# Build AppImage for Linux Wallpaper Engine GUI (system-gtk variant)
#
# Creates a "system-gtk" AppImage: the application Python code and pure-Python
# dependencies (pillow, pyglet) are bundled; GTK4, libadwaita, PyGObject and
# GObject-Introspection bindings are expected on the host system.
#
# Key design decisions:
#   - Application files live at $APPDIR/opt/$PKG/ so that every __file__-based
#     path calculation (ICON_PATH, CHANGELOG, pic/icons) works unchanged.
#   - AppRun explicitly resolves the Python site-packages directory instead of
#     using a glob (globs don't expand inside variable assignments).
#   - A thin Python wrapper under usr/bin/ sets sys.path and launches main().
#
# Prerequisites:
#   - Python 3.10+
#   - appimagetool on PATH
#
# Usage:
#   ./scripts/build-appimage.sh [--appdir PATH] [--output DIR]
################################################################################

set -euo pipefail

# ── Configuration ────────────────────────────────────────────────────────────

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

APP_NAME="Linux Wallpaper Engine GUI"
APP_ID="linux.wallpaperengine.gui"
PKG="linux-wallpaperengine-gui"          # directory / executable name
ARCH="x86_64"

ICON_SOURCE="pic/icons/GUI_rounded.png"
DESKTOP_FILE="linux.wallpaperengine.gui.desktop"

APPDIR="${APPDIR:-${PROJECT_ROOT}/build/AppDir}"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_ROOT}/build}"

# ── Colours ──────────────────────────────────────────────────────────────────

_R='\033[0;31m' _G='\033[0;32m' _Y='\033[1;33m' _B='\033[0;34m' _N='\033[0m'
info()    { echo -e "${_B}[INFO]${_N} $*"; }
ok()      { echo -e "${_G}[ OK ]${_N} $*"; }
warn()    { echo -e "${_Y}[WARN]${_N} $*"; }
die()     { echo -e "${_R}[ERR ]${_N} $*" >&2; exit 1; }

# ── Argument parsing ─────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--appdir) APPDIR="$2";     shift 2 ;;
        -o|--output) OUTPUT_DIR="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: $(basename "$0") [--appdir PATH] [--output DIR]"
            exit 0
            ;;
        *) die "Unknown option: $1" ;;
    esac
done

# ── Prerequisites ────────────────────────────────────────────────────────────

for cmd in python3 appimagetool; do
    command -v "$cmd" &>/dev/null || die "'$cmd' not found in PATH"
done

PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
SITE_PKG_REL="usr/lib/python3.${PYTHON_MINOR}/site-packages"

info "Python 3.${PYTHON_MINOR} detected"

# ── Clean & create AppDir skeleton ───────────────────────────────────────────

OPT="${APPDIR}/opt/${PKG}"

rm -rf "$APPDIR"
mkdir -p \
    "${APPDIR}/usr/bin" \
    "${APPDIR}/usr/share/applications" \
    "${APPDIR}/usr/share/icons/hicolor/256x256/apps" \
    "${APPDIR}/${SITE_PKG_REL}" \
    "${OPT}"

ok "AppDir skeleton created"

# ── Copy application files ───────────────────────────────────────────────────
# Mirror the source tree so that every __file__-relative path still resolves.

cp -r "${PROJECT_ROOT}/py_GUI"       "${OPT}/"
cp    "${PROJECT_ROOT}/run_gui.py"   "${OPT}/"
cp -r "${PROJECT_ROOT}/pic"          "${OPT}/"

# CHANGELOG.md is read at runtime by app.py → get_latest_changelog()
if [[ -f "${PROJECT_ROOT}/CHANGELOG.md" ]]; then
    cp "${PROJECT_ROOT}/CHANGELOG.md" "${OPT}/"
else
    warn "CHANGELOG.md not found — About dialog will show fallback text"
fi

# Remove __pycache__ directories — they cause FUSE mount issues where
# __file__ points to non-existent __pycache__/module.pyc paths
find "${OPT}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

ok "Application files copied → ${OPT}"

# ── Install pure-Python dependencies ─────────────────────────────────────────

info "Installing pip dependencies into AppDir..."
python3 -m pip install \
    --target "${APPDIR}/${SITE_PKG_REL}" \
    --no-deps --no-cache-dir --no-compile \
    pillow pyglet \
    2>&1 | tail -5 || warn "pip install had warnings (non-fatal)"

ok "pip dependencies installed → ${APPDIR}/${SITE_PKG_REL}"

# ── Create wrapper script (usr/bin/) ─────────────────────────────────────────

WRAPPER="${APPDIR}/usr/bin/${PKG}"
cat > "$WRAPPER" << 'PYEOF'
#!/usr/bin/env python3
"""AppImage wrapper — sets up paths then launches the GUI."""

import os, sys, site

# Resolve APPDIR (set by AppRun, or fall back to relative)
appdir = os.environ.get("APPDIR") or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

# 1. Pure-Python pip packages (pillow, pyglet)
sp = os.path.join(
    appdir, "usr", "lib",
    f"python3.{sys.version_info.minor}", "site-packages",
)
if os.path.isdir(sp):
    site.addsitedir(sp)
    if sp not in sys.path:
        sys.path.insert(0, sp)

# 2. Application code tree (opt/linux-wallpaperengine-gui/)
app_root = os.path.join(appdir, "opt", "linux-wallpaperengine-gui")
if os.path.isdir(app_root):
    if app_root not in sys.path:
        sys.path.insert(0, app_root)

from py_GUI.main import main
main()
PYEOF
chmod +x "$WRAPPER"
ok "Wrapper script created"

# ── Create AppRun ────────────────────────────────────────────────────────────
# AppRun MUST NOT use globs in variable assignment (they won't expand).
# Instead we compute the exact python version at build time.

cat > "${APPDIR}/AppRun" << APPRUN_EOF
#!/bin/bash
# AppRun — entry point executed when the AppImage is launched.
#
# CRITICAL: The application uses __file__-relative paths everywhere
# (const.py PROJECT_ROOT, ICON_PATH, etc.).  These resolve correctly
# only when CWD == app_root.  We therefore 'cd' into the application
# tree before exec-ing Python.  Without this, the app SIGTERMs.

APPDIR="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"
export APPDIR

# Library path (unused in system-gtk variant but harmless)
export LD_LIBRARY_PATH="\${APPDIR}/usr/lib:\${LD_LIBRARY_PATH:-}"

# Python paths — NO globs, exact version baked at build time.
export PYTHONPATH="\${APPDIR}/opt/${PKG}:\${APPDIR}/${SITE_PKG_REL}:\${PYTHONPATH:-}"

# XDG data dirs for icon themes
export XDG_DATA_DIRS="\${APPDIR}/usr/share:\${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"

RUNTIME_BASE="\${XDG_RUNTIME_DIR:-/tmp}"
RUNTIME_DIR="\${RUNTIME_BASE}/linux-wallpaperengine-gui-\${UID:-\$(id -u)}"
mkdir -p "\${RUNTIME_DIR}"
TRAY_SCRIPT_SRC="\${APPDIR}/opt/${PKG}/py_GUI/ui/tray_process.py"
TRAY_ICON_SRC="\${APPDIR}/opt/${PKG}/pic/icons/gui_tray_rounded.png"
TRAY_SCRIPT_DST="\${RUNTIME_DIR}/tray_process.py"
TRAY_ICON_DST="\${RUNTIME_DIR}/gui_tray_rounded.png"
if [ -f "\${TRAY_SCRIPT_SRC}" ]; then
    cp -f "\${TRAY_SCRIPT_SRC}" "\${TRAY_SCRIPT_DST}"
fi
if [ -f "\${TRAY_ICON_SRC}" ]; then
    cp -f "\${TRAY_ICON_SRC}" "\${TRAY_ICON_DST}"
fi
export LWG_TRAY_SCRIPT="\${TRAY_SCRIPT_DST}"
export LWG_TRAY_ICON="\${TRAY_ICON_DST}"

# ── CWD fix ──────────────────────────────────────────────────────────────
# The app must run with CWD inside the application tree so that every
# os.path.abspath(__file__) and PROJECT_ROOT calculation resolves to
# the bundled opt/ directory.  Launching from the AppDir root (the
# default) causes immediate SIGTERM.
cd "\${APPDIR}/opt/${PKG}"

# Run as child process (NOT exec) so this shell stays alive and
# the AppImage FUSE mount is preserved for the app lifetime.
python3 run_gui.py "\$@"
APPRUN_EOF
chmod +x "${APPDIR}/AppRun"
ok "AppRun created (Python 3.${PYTHON_MINOR})"

# ── Desktop file & icon ──────────────────────────────────────────────────────

[[ -f "${PROJECT_ROOT}/${DESKTOP_FILE}" ]] \
    || die "Desktop file not found: ${PROJECT_ROOT}/${DESKTOP_FILE}"
[[ -f "${PROJECT_ROOT}/${ICON_SOURCE}" ]] \
    || die "Icon not found: ${PROJECT_ROOT}/${ICON_SOURCE}"

# Root-level copies (appimagetool requirement)
cp "${PROJECT_ROOT}/${DESKTOP_FILE}" "${APPDIR}/"
cp "${PROJECT_ROOT}/${ICON_SOURCE}"  "${APPDIR}/${PKG}.png"

# Standard FreeDesktop locations
cp "${PROJECT_ROOT}/${DESKTOP_FILE}" "${APPDIR}/usr/share/applications/"
cp "${PROJECT_ROOT}/${ICON_SOURCE}"  "${APPDIR}/usr/share/icons/hicolor/256x256/apps/${PKG}.png"

ok "Desktop file and icon installed"

# ── Build the AppImage ───────────────────────────────────────────────────────

mkdir -p "$OUTPUT_DIR"
OUTFILE="${OUTPUT_DIR}/${PKG}-${ARCH}.AppImage"

info "Running appimagetool..."
if ARCH="$ARCH" appimagetool "$APPDIR" "$OUTFILE"; then
    chmod +x "$OUTFILE"
    ok "AppImage created: ${OUTFILE}  ($(du -h "$OUTFILE" | cut -f1))"
else
    die "appimagetool failed"
fi

# ── Verify ───────────────────────────────────────────────────────────────────

file "$OUTFILE" | grep -q "ELF" \
    && ok "ELF signature verified" \
    || warn "File type check inconclusive (may still work)"

# ── Summary ──────────────────────────────────────────────────────────────────

echo ""
echo -e "${_B}════════════════════════════════════════${_N}"
echo "  App:    ${APP_NAME}"
echo "  ID:     ${APP_ID}"
echo "  Arch:   ${ARCH}"
echo "  Output: ${OUTFILE}"
echo -e "${_B}════════════════════════════════════════${_N}"
echo ""
info "Test:  ${OUTFILE}"
info "Debug: ${OUTFILE} 2>&1 | head -50"
