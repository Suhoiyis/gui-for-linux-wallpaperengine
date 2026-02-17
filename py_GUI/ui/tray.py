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
            # 【关键修复】在对象创建的最早期，就强制定义 process 属性
            # 这样无论 __init__ 怎么跑，app.py 访问 self.tray.process 都不会报错
            cls._instance.process = None
        return cls._instance

    def __init__(self, app):
        self.app = app
        # 双重保险：如果 process 还没定义，定义它
        if not hasattr(self, 'process'):
            self.process = None
        log_main("TrayIcon Instance Accessed")
    
    def _find_script(self):

        appdir = os.getenv('APPDIR')
        if appdir:
            # 在 AppImage 中，我们通常把源码放在 /usr/src 或者 /usr/share 下
            # 这里假设安装到了 usr/share/linux-wallpaperengine-gui
            appimage_path = os.path.join(appdir, "usr/share/linux-wallpaperengine-gui/py_GUI/ui/tray_process.py")
            if os.path.exists(appimage_path): return appimage_path

        sys_path = "/usr/share/linux-wallpaperengine-gui/py_GUI/ui/tray_process.py"
        if os.path.exists(sys_path): return sys_path
        
        try:
            base = os.path.dirname(os.path.abspath(__file__))
            rel_path = os.path.join(base, 'tray_process.py')
            if os.path.exists(rel_path): return rel_path
        except: pass
        return None

    # def _resolve_icon(self):
    #     icon_path = "pic/icons/GUI_rounded.png"
    #     try:
    #         from py_GUI.const import ICON_PATH
    #         icon_path = ICON_PATH
    #     except: pass

    #     candidates = [
    #         os.path.join("/usr/share/linux-wallpaperengine-gui", icon_path),
    #         os.path.abspath(icon_path),
    #     ]
    #     for p in candidates:
    #         if os.path.exists(p): return p
    #     return ""

    def _resolve_icon(self):
        icon_path = "pic/icons/GUI_rounded.png"
        try:
            from py_GUI.const import ICON_PATH
            icon_path = ICON_PATH
        except: pass

        candidates = []

            # 【新增】AppImage 环境优先检查
            # 运行时 APPDIR 环境变量会自动指向 AppImage 的挂载点
        appdir = os.getenv('APPDIR')
        if appdir:
            candidates.append(os.path.join(appdir, "usr/share/linux-wallpaperengine-gui", icon_path))

        # 原有的检查逻辑
        candidates.append(os.path.join("/usr/share/linux-wallpaperengine-gui", icon_path))
        candidates.append(os.path.abspath(icon_path))

        # 备用：尝试直接从安装路径找
        candidates.append("/usr/share/pixmaps/linux-wallpaperengine-gui.png")

        for p in candidates:
            if os.path.exists(p): return p
        return ""

    def start(self):
        """启动托盘"""
        # 如果已有进程对象且还在运行，就不重复启动
        if self.process and self.process.poll() is None:
            return

        script_path = self._find_script()
        if not script_path: return

        real_icon_path = self._resolve_icon()
        # 获取主程序 PID 用于看门狗
        parent_pid = str(os.getpid())
        
        try:
            log_main(f"Spawning tray. Parent PID: {parent_pid}")
            
            # 【关键修复】启动后必须赋值给 self.process
            # 这样 app.py 才能读到 pid
            self.process = subprocess.Popen(
                [sys.executable, script_path, real_icon_path, parent_pid],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True, 
                close_fds=True
            )
            log_main(f"Tray spawned. PID: {self.process.pid}")
            
        except Exception as e:
            log_main(f"Start failed: {e}")
            self.process = None
    
    def stop(self):
        """
        由于我们依赖托盘进程自带的'看门狗'(parent_pid检查)来自动退出，
        这里只做简单的属性清理，不再暴力杀进程，防止误杀新启动的实例。
        """
        self.process = None