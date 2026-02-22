#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, AyatanaAppIndicator3, GLib
import subprocess
import signal
import sys
import os
import time

def log_crash(msg):
    try:
        import os, time
        log_dir = os.path.expanduser("~/.cache/linux-wallpaperengine-gui")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "tray_crash.log")
        with open(log_path, "a") as f:
            ts = time.strftime("%H:%M:%S")
            f.write(f"[{ts}] [TRAY] {msg}\n")
    except Exception:
        pass

class TrayProcess:
    def __init__(self, icon_path, parent_pid):
        self.icon_path = icon_path
        self.parent_pid = int(parent_pid) if parent_pid.isdigit() else None
        self.run_gui_path = self._find_run_gui()
        self.is_engine_running = False
        
        self.app_id = "com.wallpaperengine.gui"
        
        self.indicator = AyatanaAppIndicator3.Indicator.new(
            self.app_id,
            "preferences-desktop-wallpaper",
            AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        
        try: self.indicator.set_title("Wallpaper Engine GUI")
        except Exception: pass
        
        if self.icon_path and self.icon_path.startswith("/"):
            self.indicator.set_icon_full(self.icon_path, "Wallpaper Engine")
        else:
            self.indicator.set_icon_full(self.icon_path if self.icon_path else self.app_id, "Wallpaper Engine")
            
        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self._build_menu())

        import signal
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        
        GLib.timeout_add_seconds(2, self._poll_state)
        # Claude 提供的神级探针
        GLib.timeout_add_seconds(3, self._verify_registration)

    def _verify_registration(self):
        try:
            import subprocess
            result = subprocess.run(
                ["dbus-send", "--session", "--print-reply",
                 "--dest=org.freedesktop.DBus",
                 "/org/freedesktop/DBus",
                 "org.freedesktop.DBus.ListNames"],
                capture_output=True, text=True, timeout=3
            )
            if self.app_id in result.stdout or "StatusNotifier" in result.stdout:
                log_crash("DBus Verification: OK (Tray successfully registered to DBus)")
            else:
                log_crash("DBus Verification: FAILED (Tray is NOT in DBus names!)")
        except Exception as e:
            log_crash(f"DBus Verification Error: {e}")
        return False

    def _find_run_gui(self):
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        rel_path = os.path.join(base, 'run_gui.py')
        if os.path.exists(rel_path):
            return rel_path
        return "run_gui.py"

    def _poll_state(self):
        if self.parent_pid:
            try:
                os.kill(self.parent_pid, 0)
            except OSError:
                log_crash(f"Parent PID {self.parent_pid} died. Exiting.")
                Gtk.main_quit()
                return False

        running = False
        try:
            pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
            for pid in pids:
                try:
                    with open(os.path.join('/proc', pid, 'cmdline'), 'rb') as f:
                        cmdline = f.read().decode('utf-8', errors='ignore').replace('\0', ' ')
                        if 'linux-wallpaperengine' in cmdline and 'python' not in cmdline:
                            running = True
                            break
                except Exception: continue
        except Exception: pass
        
        self.is_engine_running = running
        return True

    def _build_menu(self):
        menu = Gtk.Menu()
        
        item_show = Gtk.MenuItem()
        label = Gtk.Label(label="<b>Show Window</b>")
        label.set_use_markup(True)
        item_show.add(label)
        item_show.connect("activate", lambda _: self._safe_cmd("--show"))
        menu.append(item_show)
        try: self.indicator.set_secondary_activate_target(item_show)
        except Exception: pass
            
        menu.append(Gtk.SeparatorMenuItem())
        
        item_toggle = Gtk.MenuItem(label="Play/Stop")
        item_toggle.connect("activate", self._on_toggle_click)
        menu.append(item_toggle)
        
        item_random = Gtk.MenuItem(label="Random Wallpaper")
        item_random.connect("activate", lambda _: self._safe_cmd("--random"))
        menu.append(item_random)
        
        menu.append(Gtk.SeparatorMenuItem())
        
        item_quit = Gtk.MenuItem(label="Quit Application")
        item_quit.connect("activate", lambda _: self._safe_cmd("--quit"))
        menu.append(item_quit)
        
        menu.show_all()
        return menu

    def _on_toggle_click(self, widget):
        if self.is_engine_running:
            self._safe_cmd("--stop")
        else:
            self._safe_cmd("--apply-last")

    def _safe_cmd(self, arg):
        GLib.timeout_add(100, self._exec_cmd, arg)

    def _exec_cmd(self, arg):
        try:
            cmd = ["python3", self.run_gui_path, arg]
            
            appdir = os.getenv('APPDIR')
            if appdir:
                launcher = os.path.join(appdir, "AppRun")
                if os.path.exists(launcher):
                    cmd = [launcher, arg]
            
            clean_env = os.environ.copy()
            clean_env.pop("DESKTOP_STARTUP_ID", None)
            clean_env.pop("GIO_LAUNCHED_DESKTOP_FILE", None)
            
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=clean_env
            )
        except Exception as e:
            log_crash(f"Cmd Error: {e}")
        return False

    def run(self):
        Gtk.main()

if __name__ == "__main__":
    try:
        icon = sys.argv[1] if len(sys.argv) > 1 else ""
        pid = sys.argv[2] if len(sys.argv) > 2 else "0"
        
        app = TrayProcess(icon, pid)
        app.run()
    except Exception as e:
        log_crash(f"Startup: {e}")