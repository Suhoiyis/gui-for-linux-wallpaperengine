# AppImage Build Quick Start

## One-Command Build

```bash
./scripts/build-appimage.sh
```

Output: `build/linux-wallpaperengine-gui-x86_64.AppImage`

## Prerequisites Checklist

- [ ] `appimagetool` installed (`appimagetool --help`)
- [ ] Python 3.10+ (`python3 --version`)
- [ ] System libs: `gtk4`, `libadwaita`, `python-gobject`
- [ ] `linux-wallpaperengine` backend (`which linux-wallpaperengine`)

## Installation

**Arch:**
```bash
sudo pacman -S appimagetool gtk4 libadwaita python-gobject python-pillow python-pyglet
```

**Ubuntu/Debian:**
```bash
sudo apt install appimagetool libgtk-4-dev libadwaita-1-dev python3-gi gir1.2-gtk-4.0 \
                 gir1.2-adw-1 python3-pil python3-pyglet
```

## Test Run

```bash
./build/linux-wallpaperengine-gui-x86_64.AppImage
```

## Install System-Wide

```bash
sudo cp build/linux-wallpaperengine-gui-x86_64.AppImage /usr/local/bin/
sudo chmod +x /usr/local/bin/linux-wallpaperengine-gui-x86_64.AppImage
```

## What Gets Built

| File | Contents |
|------|----------|
| AppRun | Entry point shell script |
| usr/bin/linux-wallpaperengine-gui | Python wrapper |
| usr/lib/python3.x/site-packages/ | Python dependencies (pillow, pyglet) |
| usr/share/applications/ | Desktop file |
| usr/share/icons/ | Application icon |
| opt/linux-wallpaperengine-gui/ | Application code |

## Troubleshooting

**appimagetool not found?**
- Install: `sudo pacman -S appimagetool` or manually download from GitHub

**Missing Python deps?**
- Script installs: pillow, pyglet
- System libs (gtk4, adwaita) must be installed separately

**Backend not working?**
- Install linux-wallpaperengine: https://github.com/Almamu/linux-wallpaperengine

## Full Documentation

See `scripts/README.md` for detailed information.
