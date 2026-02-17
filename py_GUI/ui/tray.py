import subprocess
import os
import sys
import time

def log_main(msg):
    try:
        with open("/tmp/tray_crash.log", "a") as f:
            ts = time.strftime("%H:%M:%S")
            f.write(f"[{ts}] [MAIN] {msg}\n")
    except:
        pass

class TrayIcon:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TrayIcon, cls).__new__(cls)
            # 初始化占位符，防止 app.py 访问报错
            cls._instance.process = None 
        return cls._instance

    def __init__(self, app):
        self.app = app
        log_main("TrayIcon Instance Accessed")
    
    def _find_script(self):
        sys_path = "/usr/share/linux-wallpaperengine-gui/py_GUI/ui/tray_process.py"
        if os.path.exists(sys_path): return sys_path
        
        # 开发环境回退
        try:
            base = os.path.dirname(os.path.abspath(__file__))
            rel_path = os.path.join(base, 'tray_process.py')
            if os.path.exists(rel_path): return rel_path
        except: pass
        return None

    def _resolve_icon(self):
        # 优先使用 const 定义
        icon_path = "pic/icons/GUI_rounded.png"
        try:
            from py_GUI.const import ICON_PATH
            icon_path = ICON_PATH
        except: pass

        # 转换为绝对路径 (解决图标空白问题)
        candidates = [
            os.path.join("/usr/share/linux-wallpaperengine-gui", icon_path),
            os.path.abspath(icon_path),
            "/usr/share/pixmaps/linux-wallpaperengine-gui.png" # 备用系统位置
        ]
        
        for p in candidates:
            if os.path.exists(p):
                return p
        return ""

    def start(self):
        """启动托盘"""
        # 如果已有进程且存活，不再启动
        if self.process and self.process.poll() is None:
            return

        script_path = self._find_script()
        if not script_path: return

        real_icon_path = self._resolve_icon()
        
        try:
            log_main(f"Starting tray with icon: {real_icon_path}")
            
            # 【关键修复】将 Popen 对象赋值给 self.process，解决 AttributeError
            self.process = subprocess.Popen(
                [sys.executable, script_path, real_icon_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True, # 关键：独立会话，防自杀
                close_fds=True
            )
            log_main(f"Tray spawned. PID: {self.process.pid}")
            
        except Exception as e:
            log_main(f"Start failed: {e}")
            self.process = None # 确保失败时为 None
    
    def stop(self):
        """
        这里的 stop 留空或者只做标记。
        因为我们使用了 start_new_session，主程序退出时托盘不会自动死。
        真正的清理工作交给托盘进程自己的 quit 菜单或系统清理。
        """
        pass