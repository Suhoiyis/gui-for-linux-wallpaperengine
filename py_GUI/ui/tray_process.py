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
        
        # 【修复 1】Tooltip 名称修复
        # 第一个参数是 ID，通常会被用作 Tooltip
        self.app_id = "linux-wallpaperengine-gui"
        
        self.indicator = AyatanaAppIndicator3.Indicator.new(
            self.app_id,
            "preferences-desktop-wallpaper",
            AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        
        if self.icon_path and os.path.exists(self.icon_path):
            self.indicator.set_icon_full(os.path.abspath(self.icon_path), "Wallpaper Engine")
            # 显式设置 Title，增加兼容性
            try: self.indicator.set_title("Wallpaper Engine GUI")
            except Exception: pass
        
        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self._build_menu())
        
        # 忽略 SIGTERM，防止误杀
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        
        # 启动状态轮询（检查引擎状态 + 检查主程序是否存活）
        GLib.timeout_add_seconds(2, self._poll_state)

    # def _find_run_gui(self):

    #     appdir = os.getenv('APPDIR')
    #     if appdir:
    #         # 假设 run_gui.py 在 AppImage 的 usr/bin 或 usr/share 下
    #         # 这里的路径取决于稍后我们在 build 脚本里怎么放文件
    #         appimage_path = os.path.join(appdir, "usr/share/linux-wallpaperengine-gui/run_gui.py")
    #         if os.path.exists(appimage_path): return appimage_path

    #     sys_path = "/usr/share/linux-wallpaperengine-gui/run_gui.py"
    #     if os.path.exists(sys_path): return sys_path
    #     try:
    #         base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #         dev_path = os.path.join(base, 'run_gui.py')
    #         if os.path.exists(dev_path): return dev_path
    #     except Exception: pass
    #     return "run_gui.py"
    
    def _find_run_gui(self):
        # 抛弃写死的绝对路径，直接根据当前文件位置反推 run_gui.py 的位置
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        rel_path = os.path.join(base, 'run_gui.py')
        if os.path.exists(rel_path):
            return rel_path
        return "run_gui.py"


    def _poll_state(self):
        # 【修复 3】看门狗：如果主程序死了，托盘自动自杀
        if self.parent_pid:
            try:
                # 发送 0 信号检测进程是否存在
                os.kill(self.parent_pid, 0)
            except OSError:
                log_crash(f"Parent PID {self.parent_pid} died. Exiting.")
                Gtk.main_quit()
                return False

        # 检查壁纸引擎是否在运行 (用于 Play/Stop 逻辑)
        running = False
        try:
            pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
            for pid in pids:
                try:
                    with open(os.path.join('/proc', pid, 'cmdline'), 'rb') as f:
                        cmdline = f.read().decode('utf-8', errors='ignore').replace('\0', ' ')
                        # 检查是否有 linux-wallpaperengine 进程
                        if 'linux-wallpaperengine' in cmdline and 'python' not in cmdline:
                            running = True
                            break
                except Exception: continue
        except Exception: pass
        
        self.is_engine_running = running
        return True

    def _build_menu(self):
        menu = Gtk.Menu()
        
        # Show Window
        item_show = Gtk.MenuItem()
        label = Gtk.Label(label="<b>Show Window</b>")
        label.set_use_markup(True)
        item_show.add(label)
        item_show.connect("activate", lambda _: self._safe_cmd("--show"))
        menu.append(item_show)
        try: self.indicator.set_secondary_activate_target(item_show)
        except Exception: pass
            
        menu.append(Gtk.SeparatorMenuItem())
        
        # Play/Stop
        item_toggle = Gtk.MenuItem(label="Play/Stop")
        # 连接到逻辑函数，而不是直接发命令
        item_toggle.connect("activate", self._on_toggle_click)
        menu.append(item_toggle)
        
        # Random
        item_random = Gtk.MenuItem(label="Random Wallpaper")
        item_random.connect("activate", lambda _: self._safe_cmd("--random"))
        menu.append(item_random)
        
        menu.append(Gtk.SeparatorMenuItem())
        
        # Quit
        item_quit = Gtk.MenuItem(label="Quit Application")
        item_quit.connect("activate", lambda _: self._safe_cmd("--quit"))
        menu.append(item_quit)
        
        menu.show_all()
        return menu

    def _on_toggle_click(self, widget):
        # 【修复 2】Play/Stop 逻辑修复
        # 如果引擎在跑，就发 stop；没跑，就发 apply-last
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
            
            # 【终极核心修复】剥离 GTK 自动注入的环境变量，防止触发双开 Bug！
            clean_env = os.environ.copy()
            clean_env.pop("DESKTOP_STARTUP_ID", None)
            clean_env.pop("GIO_LAUNCHED_DESKTOP_FILE", None)
            
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=clean_env  # 👈 传入洗干净的环境变量
            )
        except Exception as e:
            log_crash(f"Cmd Error: {e}")
        return False

    def run(self):
        Gtk.main()

if __name__ == "__main__":
    try:
        # 接收参数: script.py <icon_path> <parent_pid>
        icon = sys.argv[1] if len(sys.argv) > 1 else ""
        pid = sys.argv[2] if len(sys.argv) > 2 else "0"
        
        app = TrayProcess(icon, pid)
        app.run()
    except Exception as e:
        log_crash(f"Startup: {e}")