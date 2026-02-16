#!/usr/bin/env python3
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AyatanaAppIndicator3", "0.1")
from gi.repository import Gtk, AyatanaAppIndicator3, GLib
import subprocess
import signal
import sys
import os


class TrayProcess:
    def __init__(self, icon_path):
        self.icon_path = icon_path
        self.run_gui_path = self._find_run_gui()
        self.is_running = False  # Track state locally

        # Create Indicator
        self.indicator = AyatanaAppIndicator3.Indicator.new(
            "wallpaper-engine-gui",
            "preferences-desktop-wallpaper",
            AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )

        # Set custom icon if available
        if self.icon_path:
            abs_path = os.path.abspath(self.icon_path)
            if os.path.exists(abs_path):
                # print(f"Loading icon from: {abs_path}")
                self.indicator.set_icon_full(abs_path, "Wallpaper Engine")
            else:
                print(f"Icon not found at: {abs_path}")

        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self._build_menu())

        # Handle SIGTERM to exit cleanly
        signal.signal(signal.SIGTERM, lambda *_: Gtk.main_quit())

        # Start state poller (check every 2 seconds)
        GLib.timeout_add_seconds(2, self._poll_state)

    def _find_run_gui(self):
        # Locate run_gui.py relative to this file
        # this file: py_GUI/ui/tray_process.py
        # run_gui.py: ./run_gui.py (root)
        base = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        return os.path.join(base, "run_gui.py")

    def _build_menu(self):
        self.menu = Gtk.Menu()

        # Show Window (First item, bold)
        item_show = Gtk.MenuItem()
        label = Gtk.Label(label="<b>Show Window</b>")
        label.set_use_markup(True)
        item_show.add(label)
        item_show.connect("activate", lambda _: self._cmd("--show"))
        self.menu.append(item_show)

        # Set as secondary activate target (Middle click)
        try:
            self.indicator.set_secondary_activate_target(item_show)
        except:
            pass

        self.menu.append(Gtk.SeparatorMenuItem())

        # Play/Stop Toggle Button
        item_toggle = Gtk.MenuItem(label="Play/Stop")
        item_toggle.connect("activate", self._on_toggle)
        self.menu.append(item_toggle)

        # Random Wallpaper
        item_random = Gtk.MenuItem(label="Random Wallpaper")
        item_random.connect("activate", lambda _: self._cmd("--random"))
        self.menu.append(item_random)

        self.menu.append(Gtk.SeparatorMenuItem())

        # Quit
        item_quit = Gtk.MenuItem(label="Quit Application")
        item_quit.connect("activate", lambda _: self._cmd("--quit"))
        self.menu.append(item_quit)

        self.menu.show_all()
        return self.menu

    def _poll_state(self):
        running = False
        try:
            # Check if linux-wallpaperengine is running
            # Check /proc manually to avoid shell pipe issues
            pids = [pid for pid in os.listdir("/proc") if pid.isdigit()]
            for pid in pids:
                try:
                    with open(os.path.join("/proc", pid, "cmdline"), "rb") as f:
                        cmdline = (
                            f.read().decode("utf-8", errors="ignore").replace("\0", " ")
                        )
                        if (
                            "linux-wallpaperengine" in cmdline
                            and "python" not in cmdline
                            and "grep" not in cmdline
                        ):
                            running = True
                            break
                except (IOError, OSError):
                    continue
        except Exception as e:
            print(f"Poll error: {e}")
            running = False

        self.is_running = running
        return True  # Keep calling

    def _on_toggle(self, widget):
        print(f"Toggle clicked. Current detected state is running={self.is_running}")
        if self.is_running:
            print("Action: Stopping")
            self._cmd("--stop")
        else:
            print("Action: Applying Last")
            self._cmd("--apply-last")

    def _cmd(self, arg):
        appdir = os.environ.get("APPDIR")
        if appdir:
            # Inside AppImage: invoke run_gui.py from the mounted AppDir
            # directly instead of re-launching the full AppImage binary.
            # Re-launching causes AppRun to overwrite runtime tray assets
            # and truncate the log file, killing the running tray process.
            run_gui = os.path.join(
                appdir, "opt", "linux-wallpaperengine-gui", "run_gui.py"
            )
            env = os.environ.copy()
            env["PYTHONPATH"] = (
                os.path.join(appdir, "opt", "linux-wallpaperengine-gui")
                + ":"
                + env.get("PYTHONPATH", "")
            )
            subprocess.Popen(["python3", run_gui, arg], env=env, cwd=appdir)
            return
        subprocess.Popen(["python3", self.run_gui_path, arg])

    def run(self):
        Gtk.main()


if __name__ == "__main__":
    icon = sys.argv[1] if len(sys.argv) > 1 else ""
    TrayProcess(icon).run()
