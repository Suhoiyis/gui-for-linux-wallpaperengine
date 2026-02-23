import subprocess
import os
import time


def log_main(msg):
    if os.getenv("LWG_DEBUG") != "1":
        return

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
            self.process = None  # ✨ 干净利落，直接绑定在单例对象上
            log_main("TrayIcon Initialized")
            self.initialized = True

    # @property
    # def process(self): ...
    # @process.setter
    # def process(self, value): ...
    
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

        # 【极其关键】：明确指定最新的双向通信版
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        dev_path = os.path.join(base, 'tray_rs', 'target', 'release', 'tray-rs')
        
        if os.path.exists(dev_path):
            rust_tray_path = dev_path
            os.environ['LWG_IPC_SOCKET'] = f"/tmp/lwg-ipc-{os.getuid()}.sock"
            log_main(f"Using dev Rust tray: {rust_tray_path}")
        else:
            rust_tray_path = os.getenv('LWG_TRAY_BIN')
            if not rust_tray_path or not os.path.exists(rust_tray_path):
                rust_tray_path = shutil.which('tray-rs-bin')
            log_main(f"Using fallback Rust tray: {rust_tray_path}")

        if not rust_tray_path or not os.path.exists(rust_tray_path):
            log_main("CRITICAL: tray-rs-bin missing.")
            return

        cmd = [rust_tray_path, self._resolve_icon(), str(os.getpid())]
        
        try:
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

    def update_tooltip(self, text: str):
        """向 Rust 托盘发送最新的悬浮提示文本，带有智能重试机制"""
        try:
            import socket
            sock_path = f"/tmp/lwg-tray-rx-{os.getuid()}.sock"
            
            # ✅ 修复 Bug 2：如果 Rust 还没建好管道，绝不静默放弃，等 1 秒后再试！
            if not os.path.exists(sock_path):
                import threading
                import time
                def _retry():
                    time.sleep(1)
                    self.update_tooltip(text)
                threading.Thread(target=_retry, daemon=True).start()
                return

            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                s.connect(sock_path)
                s.sendall((text + "\n").encode('utf-8'))
        except Exception as e:
            log_main(f"Tooltip update failed: {e}")