import subprocess
import os
import sys
import time

# ==============================================================================
# ☢️ 核弹级内嵌 Payload：直接寄生在内存中的 tray_process.py 代码,现在的 tray_process.py 实际上是无效的，暂时保留不删除
# ==============================================================================
TRAY_PROCESS_PAYLOAD = r'''#!/usr/bin/env python3
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
    def __init__(self, icon_path, parent_pid, run_gui_path):
        self.icon_path = icon_path
        self.parent_pid = int(parent_pid) if parent_pid.isdigit() else None
        self.run_gui_path = run_gui_path
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
            # 终极调用：判断是直接运行 AppImage 还是本地 py 脚本
            if self.run_gui_path.endswith('.py'):
                cmd = ["python3", self.run_gui_path, arg]
            else:
                cmd = [self.run_gui_path, arg]

            # 直接 Popen，不需要清理 env，因为如果是 AppImage，它自己会组装完整的运行环境！
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            log_crash(f"Executed command: {cmd}")
        except Exception as e:
            log_crash(f"Cmd Error: {e}")
        return False

    def run(self):
        Gtk.main()

if __name__ == "__main__":
    try:
        icon = sys.argv[1] if len(sys.argv) > 1 else ""
        pid = sys.argv[2] if len(sys.argv) > 2 else "0"
        # 接收第三个参数作为启动器路径
        run_gui = sys.argv[3] if len(sys.argv) > 3 else "run_gui.py"
        app = TrayProcess(icon, pid, run_gui)
        app.run()
    except Exception as e:
        log_crash(f"Startup: {e}")
'''
# ==============================================================================

def log_main(msg):
    try:
        import os, time
        log_dir = os.path.expanduser("~/.cache/linux-wallpaperengine-gui")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "tray_crash.log")
        with open(log_path, "a") as f:
            ts = time.strftime("%H:%M:%S")
            f.write(f"[{ts}] [MAIN] {msg}\n")
    except Exception:
        pass

class TrayIcon:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TrayIcon, cls).__new__(cls)
            cls._instance.process = None
        return cls._instance

    def __init__(self, app):
        self.app = app
        if not hasattr(self, 'process'):
            self.process = None

        try:
            import os
            log_dir = os.path.expanduser("~/.cache/linux-wallpaperengine-gui")
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, "tray_crash.log")
            # 用 'w' 模式打开并立即关闭，直接清空文件内容
            open(log_path, 'w').close()
        except Exception:
            pass
        
        log_main("TrayIcon Instance Accessed")

    def _extract_and_find_script(self):
        """将内置代码释放到宿主机缓存"""
        cache_dir = os.path.expanduser("~/.cache/linux-wallpaperengine-gui")
        os.makedirs(cache_dir, exist_ok=True)
        dest = os.path.join(cache_dir, 'tray_process.py')
        
        try:
            with open(dest, "w", encoding="utf-8") as f:
                f.write(TRAY_PROCESS_PAYLOAD)
            os.chmod(dest, 0o755)
            log_main(f"SUCCESS: Embedded payload successfully released to: {dest}")
            return dest
        except Exception as e:
            log_main(f"CRITICAL: Failed to write embedded payload: {e}")
            return None

    def _resolve_icon(self):
        try:
            from py_GUI.const import APP_ID
            safe_path = os.path.expanduser(f"~/.local/share/icons/hicolor/512x512/apps/{APP_ID}.png")
            if os.path.exists(safe_path):
                return safe_path
            return APP_ID
        except Exception:
            return "com.wallpaperengine.gui"

    def start(self):
        if self.process and self.process.poll() is None:
            return

        script_path = self._extract_and_find_script()

        if not script_path: 
            log_main("CRITICAL: Aborting tray start, script_path is None.")
            return

        real_icon_path = self._resolve_icon()
        parent_pid = str(os.getpid())
        
        # 【核心修复】：直接拿到 AppImage 文件的绝对物理路径！
        try:
            appimage = os.getenv('APPIMAGE')
            appdir = os.getenv('APPDIR')
            
            if appimage and os.path.exists(appimage):
                # 优先使用 .AppImage 文件本身 (完美解决右键点击无效的问题)
                run_gui_path = appimage
            elif appdir:
                # 备用方案：使用 AppRun
                run_gui_path = os.path.join(appdir, 'AppRun')
            else:
                # 本地开发环境回退
                base = os.path.dirname(os.path.abspath(__file__))
                run_gui_path = os.path.join(os.path.dirname(os.path.dirname(base)), 'run_gui.py')
        except Exception as e:
            log_main(f"Failed to calculate run_gui_path: {e}")
            run_gui_path = "run_gui.py"

        log_main(f"Target run_gui_path: {run_gui_path}")
        
        try:
            log_main(f"Spawning tray. Payload Script: {script_path}")
            
            # 将 run_gui_path 作为参数 3 传给 payload
            cmd = ["/usr/bin/python3", script_path, real_icon_path, parent_pid, run_gui_path]
            
            clean_env = os.environ.copy()
            clean_env.pop("DESKTOP_STARTUP_ID", None)
            clean_env.pop("GIO_LAUNCHED_DESKTOP_FILE", None)

            if os.getenv('APPDIR'):
                clean_env.pop("LD_LIBRARY_PATH", None)
                clean_env.pop("PYTHONPATH", None)
                clean_env.pop("APPDIR", None)
                clean_env.pop("APPIMAGE", None)
                clean_env.pop("GTK_PATH", None)
                clean_env.pop("GTK_EXE_PREFIX", None)
                clean_env.pop("GTK_DATA_PREFIX", None)
                clean_env.pop("GDK_BACKEND", None)      
                clean_env.pop("GDK_PIXBUF_MODULE_FILE", None)
                clean_env.pop("GDK_PIXBUF_MODULEDIR", None)
                clean_env.pop("GI_TYPELIB_PATH", None)  
                clean_env.pop("GSETTINGS_SCHEMA_DIR", None)
                clean_env.pop("XDG_DATA_DIRS", None)

            dbus_addr = clean_env.get("DBUS_SESSION_BUS_ADDRESS", "MISSING")
            log_main(f"DBUS Address: {dbus_addr}")

            self.process = subprocess.Popen(
                cmd, 
                stdout=subprocess.DEVNULL,
                stderr=None,
                env=clean_env,
                close_fds=True
            )
            log_main(f"Tray spawned successfully. PID: {self.process.pid}")
            
        except Exception as e:
            log_main(f"Start failed: {e}")
            self.process = None
    
    def stop(self):
        if self.process and self.process.poll() is None:
            try:
                # First try a graceful termination (SIGTERM on POSIX)
                self.process.terminate()
                try:
                    # Give the process a short time to exit gracefully
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # If SIGTERM is ignored or ineffective, force kill
                    self.process.kill()
                    try:
                        self.process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        log_main("TrayIcon.stop: process did not exit after SIGKILL")
            except Exception as e:
                log_main(f"TrayIcon.stop failed: {e}")
            finally:
                # Always drop the reference once we've attempted to stop it
                self.process = None
        else:
            self.process = None