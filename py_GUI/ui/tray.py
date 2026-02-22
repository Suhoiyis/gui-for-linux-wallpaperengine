import subprocess
import os
import sys
import time


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
            
            # --- 采用 Copilot 建议的日志轮转 (Log Rotation) ---
            max_log_size = 512 * 1024  # 最大 512KB
            if os.path.exists(log_path):
                try:
                    current_size = os.path.getsize(log_path)
                except OSError:
                    current_size = 0
                    
                if current_size > max_log_size:
                    rotated_path = log_path + ".1"
                    try:
                        if os.path.exists(rotated_path):
                            os.remove(rotated_path)
                        os.replace(log_path, rotated_path)
                    except OSError:
                        pass
            else:
                # 文件不存在时，创建一个空文件
                open(log_path, 'a').close()
                
        except Exception:
            pass
        
        log_main("TrayIcon Instance Accessed")

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

        # 1. 直接定位我们刚才编译的原生 Rust 托盘插件
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        rust_tray_path = os.path.join(base, 'tray-rs-bin')
        
        if not os.path.exists(rust_tray_path):
            log_main(f"CRITICAL: Rust tray binary not found at {rust_tray_path}")
            return

        # 2. 准备参数
        real_icon_path = self._resolve_icon()
        parent_pid = str(os.getpid())
        
        # 3. 计算 run_gui_path (完美保留了你的 AppImage 识别黑魔法)
        try:
            appimage = os.getenv('APPIMAGE')
            appdir = os.getenv('APPDIR')
            
            if appimage and os.path.exists(appimage):
                run_gui_path = appimage
            elif appdir:
                run_gui_path = os.path.join(appdir, 'AppRun')
            else:
                run_gui_path = os.path.join(base, 'run_gui.py')
        except Exception as e:
            log_main(f"Failed to calculate run_gui_path: {e}")
            run_gui_path = "run_gui.py"

        cmd = [rust_tray_path, real_icon_path, parent_pid, run_gui_path]
        
        # 4. 🚀 瞬间发射！不再需要清理环境，因为 Rust 里面已经清洗过了！
        try:
            self.process = subprocess.Popen(
                cmd, 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
            log_main(f"Rust Tray spawned successfully. PID: {self.process.pid}")
            
        except Exception as e:
            log_main(f"Start failed: {e}")
            self.process = None
    
    def stop(self):
        if self.process:
            try:
                self.process.kill()
            except Exception:
                pass
        self.process = None