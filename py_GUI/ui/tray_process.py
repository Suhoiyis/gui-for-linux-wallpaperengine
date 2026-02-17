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
import random

# === 终极调试日志 ===
def log_crash(msg):
    try:
        with open("/tmp/tray_crash.log", "a") as f:
            ts = time.strftime("%H:%M:%S")
            f.write(f"[{ts}] {msg}\n")
    except:
        pass

# 全局异常钩子：任何未捕获的错误都会被记录
def exception_hook(exctype, value, traceback):
    log_crash(f"UNCAUGHT EXCEPTION: {value}")
    sys.__excepthook__(exctype, value, traceback)

sys.excepthook = exception_hook

class TrayProcess:
    def __init__(self, icon_path):
        log_crash(f"Tray Init. PID: {os.getpid()}")
        self.icon_path = icon_path
        self.run_gui_path = self._find_run_gui()
        
        # 【关键修改】使用随机 ID，防止“单实例”冲突导致无法启动
        # 如果上一个进程还没完全退出，用新 ID 可以保证这个能活下来
        unique_id = f"wallpaper-engine-gui-{random.randint(1000, 9999)}"
        
        self.indicator = AyatanaAppIndicator3.Indicator.new(
            unique_id,
            "preferences-desktop-wallpaper",
            AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        
        if self.icon_path and os.path.exists(self.icon_path):
            self.indicator.set_icon_full(self.icon_path, "Wallpaper Engine")
        
        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self._build_menu())
        
# 忽略 SIGPIPE，防止主程序关闭管道导致的崩溃
        signal.signal(signal.SIGPIPE, signal.SIG_IGN)
        
        # 修改 SIGTERM 处理，增加一点延迟确认，或者在特定情况下忽略
        signal.signal(signal.SIGTERM, self._on_sigterm)

    def _on_sigterm(self, *args):
        # 只有当收到来自特定条件的信号才退出，这里可以先记录但不退出
        log_crash("Received SIGTERM - Ignoring to prevent accidental suicide.")
        # 如果你确实想让它能被杀死，可以取消下面这行的注释
        # Gtk.main_quit()

    def _keep_alive(self):
        return True
    
    def _find_run_gui(self):
        # 1. 绝对优先：系统安装路径
        sys_path = "/usr/share/linux-wallpaperengine-gui/run_gui.py"
        if os.path.exists(sys_path):
            return sys_path
            
        # 2. 相对路径回退
        try:
            base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            dev_path = os.path.join(base, 'run_gui.py')
            if os.path.exists(dev_path):
                 return dev_path
        except:
            pass
        return "run_gui.py"
    
    def _build_menu(self):
        menu = Gtk.Menu()
        
        # Helper to simplify menu creation
        def add_item(label, command, use_markup=False):
            item = Gtk.MenuItem()
            lbl = Gtk.Label(label=label)
            lbl.set_use_markup(use_markup)
            item.add(lbl)
            # 【关键修改】使用 timeout_add 代替 idle_add
            # 延迟 200ms 执行，让菜单先平稳关闭，防止 UI 线程冲突崩溃
            item.connect("activate", lambda _: GLib.timeout_add(200, self._safe_cmd, command))
            menu.append(item)
            return item

        show_item = add_item("<b>Show Window</b>", "--show", True)
        
        try:
            self.indicator.set_secondary_activate_target(show_item)
        except:
            pass
            
        menu.append(Gtk.SeparatorMenuItem())
        
        # Play/Stop 稍微复杂点，需要逻辑判断，但这里简化为命令发送
        # 我们假设 GUI 会处理逻辑，这里只管发信号
        item_toggle = Gtk.MenuItem(label="Play/Stop")
        # 同样延迟 200ms
        item_toggle.connect("activate", lambda _: GLib.timeout_add(200, self._on_toggle))
        menu.append(item_toggle)
        
        add_item("Random Wallpaper", "--random")
        
        menu.append(Gtk.SeparatorMenuItem())
        
        add_item("Quit Application", "--quit")
        
        menu.show_all()
        return menu

    def _on_toggle(self):
        # 简单的 toggle 逻辑：直接发 --toggle-play 或者类似的，
        # 这里为了稳健，我们直接发 --apply-last，让主程序决定
        # 或者发 --stop，取决于你想做什么。
        # 为了防崩溃，这里只做简单的命令转发
        self._safe_cmd("--random") # 暂时用 random 代替，或者你有专门的 toggle 命令
        return False

    def _safe_cmd(self, arg):
        try:
            log_crash(f"Command: {arg}")
            # close_fds=True 和 start_new_session=True 双重隔离
            subprocess.Popen(
                ['python3', self.run_gui_path, arg],
                start_new_session=True,
                close_fds=True, 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            log_crash(f"Cmd Error: {e}")
        return False # 停止定时器

    def run(self):
        try:
            Gtk.main()
        except Exception as e:
            log_crash(f"Main Loop Crash: {e}")

if __name__ == "__main__":
    try:
        icon = sys.argv[1] if len(sys.argv) > 1 else ""
        app = TrayProcess(icon)
        app.run()
    except Exception as e:
        log_crash(f"Startup Crash: {e}")