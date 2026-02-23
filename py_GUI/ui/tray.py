import subprocess
import os
import time

_GLOBAL_TRAY_PROCESS = None

def log_main(msg):
    try:
        log_dir = os.path.expanduser("~/.cache/linux-wallpaperengine-gui")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "tray_crash.log")
        
        if os.path.exists(log_path):
            try:
                if os.path.getsize(log_path) > 512 * 1024:
                    rotated = log_path + ".1"
                    if os.path.exists(rotated): os.remove(rotated)
                    os.replace(log_path, rotated)
            except OSError:
                pass
        
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
            cls._instance.initialized = False
        return cls._instance

    def __init__(self, app):
        self.app = app
        if not self.initialized:
            log_main("TrayIcon Initialized")
            self.initialized = True

    @property
    def process(self):
        global _GLOBAL_TRAY_PROCESS
        return _GLOBAL_TRAY_PROCESS

    @process.setter
    def process(self, value):
        global _GLOBAL_TRAY_PROCESS
        _GLOBAL_TRAY_PROCESS = value

    def _resolve_icon(self):
        try:
            from py_GUI.const import APP_ID
            safe = os.path.expanduser(f"~/.local/share/icons/hicolor/512x512/apps/{APP_ID}.png")
            return safe if os.path.exists(safe) else APP_ID
        except Exception:
            return "com.wallpaperengine.gui"

    def start(self):
        if self.process is not None:
            if self.process.poll() is None:
                log_main(f"Tray (PID: {self.process.pid}) is alive. Skipping.")
                return
            else:
                self.process = None

        log_main("Initiating Tray Start Sequence...")
        import shutil

        # 1. 尝试使用 AppImage 环境提供的二进制
        rust_tray_path = os.getenv('LWG_TRAY_BIN')
        if not rust_tray_path or not os.path.exists(rust_tray_path):
            rust_tray_path = shutil.which('tray-rs-bin')

        # 2. 回退到开发源码目录
        if not rust_tray_path or not os.path.exists(rust_tray_path):
            base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            dev_path = os.path.join(base, 'tray_rs', 'target', 'release', 'tray-rs')
            if os.path.exists(dev_path):
                rust_tray_path = dev_path
                os.environ['LWG_IPC_SOCKET'] = f"/tmp/lwg-ipc-{os.getuid()}.sock"

        if not rust_tray_path or not os.path.exists(rust_tray_path):
            log_main("CRITICAL: tray-rs-bin missing.")
            return

        cmd = [rust_tray_path, self._resolve_icon(), str(os.getpid()), ""]
        
        try:
            # 去除所有的 Sleep 阻塞，光速启动！
            proc = subprocess.Popen(
                cmd, 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                start_new_session=True 
            )
            self.process = proc
            log_main(f"Rust Tray Spawned Successfully. PID: {proc.pid}")
        except Exception as e:
            log_main(f"Spawn Error: {e}")

    def stop(self):
        if self.process:
            log_main(f"Terminating tray (PID: {self.process.pid}) on app quit.")
            try:
                self.process.terminate()  # 温柔地发送 SIGTERM，让 Rust 有充足时间留下遗言
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
            except Exception:
                pass
            self.process = None