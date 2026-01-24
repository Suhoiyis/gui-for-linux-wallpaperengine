import threading
import os
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import GLib

try:
    os.environ['PYSTRAY_BACKEND'] = 'dbus'
    import pystray
    from PIL import Image
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

class TrayIcon:
    def __init__(self, app):
        self.app = app
        self.icon = None
        self.thread = None

    def start(self):
        if not TRAY_AVAILABLE:
            return
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        try:
            image = self._create_icon()
            menu = (
                pystray.MenuItem("Toggle Window", lambda: GLib.idle_add(self.app.toggle_window), default=True),
                pystray.MenuItem("Refresh", lambda: GLib.idle_add(self.app.refresh_from_cli)),
                pystray.MenuItem("Apply Last", lambda: GLib.idle_add(self.app.apply_last_from_cli)),
                pystray.MenuItem("Quit", lambda: GLib.idle_add(self.app.quit_app))
            )
            self.icon = pystray.Icon("wallpaper-engine-gui", image, "Linux Wallpaper Engine GUI", menu)
            self.icon.run()
        except Exception as e:
            print(f"[TRAY] Error: {e}")

    def _create_icon(self):
        try:
            size = 64
            image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            pixels = image.load()
            center = size // 2
            radius = size // 2 - 2
            for x in range(size):
                for y in range(size):
                    dx = x - center
                    dy = y - center
                    if dx*dx + dy*dy <= radius*radius:
                        pixels[x, y] = (0, 123, 255, 255)
            return image
        except:
            return Image.new('RGBA', (64, 64), (0, 0, 0, 0))

    def stop(self):
        if self.icon:
            self.icon.stop()
