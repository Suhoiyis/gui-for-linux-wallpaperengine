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
    
    def _install_tray_icons(self):
        """核心黑魔法：将托盘图标释放到用户本地目录，彻底绕开 AppImage 的 FUSE 权限阻拦"""
        import shutil
        import os
        try:
            # 找到源码/AppDir内部的源图标
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            src_normal = os.path.join(base_dir, "pic", "icons", "gui_tray_rounded.png")
            src_stopped = os.path.join(base_dir, "pic", "icons", "gui_tray_rounded-stopped.png")
            
            # 目标本地 XDG 标准目录 (安全区)
            local_icon_dir = os.path.expanduser("~/.local/share/icons/hicolor/512x512/apps")
            os.makedirs(local_icon_dir, exist_ok=True)
            
            target_normal = os.path.join(local_icon_dir, "com.wallpaperengine.tray.png")
            target_stopped = os.path.join(local_icon_dir, "com.wallpaperengine.tray-stopped.png")
            
            # 如果源文件存在，且本地不存在或源文件较新，则进行覆盖拷贝
            for src, target in [(src_normal, target_normal), (src_stopped, target_stopped)]:
                if os.path.exists(src):
                    if not os.path.exists(target) or os.path.getmtime(src) > os.path.getmtime(target):
                        shutil.copy2(src, target)
                        
            # ✨ 核心修复：返回这个位于安全区的【绝对路径】！
            return target_normal
            
        except Exception as e:
            log_main(f"Failed to install local tray icons: {e}")
            return None

    def _resolve_icon(self):
        # 1. 释放到本地，拿回安全的绝对路径
        safe_path = self._install_tray_icons()
        
        # 2. 如果成功，直接把绝对路径扔给 Rust！
        # 桌面环境拿到绝对路径后，既不需要刷新缓存，又不会被 AppImage 拦截！
        if safe_path and os.path.exists(safe_path):
            return safe_path
            
        # 兜底
        return "com.wallpaperengine.tray"

    def start(self):
        if self.process is not None:
            if self.process.poll() is None:
                log_main(f"Tray (PID: {self.process.pid}) is alive. Skipping.")
                return
            else:
                self.process = None

        log_main("Initiating Tray Start Sequence...")
        import shutil

        # 定义统一的 Socket 路径
        socket_path = f"/tmp/lwg-ipc-{os.getuid()}.sock"
        
        # 获取各环境可能的路径
        appimage_tray_path = os.getenv('LWG_TRAY_BIN')
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        dev_path = os.path.join(base, 'tray_rs', 'target', 'release', 'tray-rs')

        rust_tray_path = None

        # 1. 最高优先级：AppImage/生产环境变量提供的路径
        if appimage_tray_path and os.path.exists(appimage_tray_path):
            rust_tray_path = appimage_tray_path
            os.environ.setdefault('LWG_IPC_SOCKET', socket_path)
            log_main(f"Using AppImage/env Rust tray: {rust_tray_path}")
            
        # 2. 次优级：本地源码编译出的开发版路径
        elif os.path.exists(dev_path):
            rust_tray_path = dev_path
            os.environ['LWG_IPC_SOCKET'] = socket_path
            log_main(f"Using dev Rust tray: {rust_tray_path}")
            
        # 3. 兜底策略：从系统 PATH 环境变量寻找
        else:
            rust_tray_path = shutil.which('tray-rs-bin')
            if rust_tray_path:
                os.environ.setdefault('LWG_IPC_SOCKET', socket_path)
                log_main(f"Using fallback system Rust tray: {rust_tray_path}")

        # 最终安全检查
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

    def update_tooltip(self, text: str, retries: int = 3):  # 👈 增加 retries 参数
        """向 Rust 托盘发送最新的悬浮提示文本，带有防止无限递归的重试机制"""
        try:
            import socket
            sock_path = f"/tmp/lwg-tray-rx-{os.getuid()}.sock"
            
            if not os.path.exists(sock_path):
                if retries > 0:
                    import threading
                    import time
                    def _retry():
                        time.sleep(1)
                        self.update_tooltip(text, retries - 1)  # 👈 递减重试次数
                    threading.Thread(target=_retry, daemon=True).start()
                else:
                    log_main("Tooltip update failed: RX Socket missing after max retries.")
                return

            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                s.connect(sock_path)
                s.sendall((text + "\n").encode('utf-8'))
        except Exception as e:
            log_main(f"Tooltip update failed: {e}")