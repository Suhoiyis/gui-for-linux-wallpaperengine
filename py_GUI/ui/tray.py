import subprocess
import os
import sys
import time

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

    def _get_tray_binary_path(self) -> str:
        """
        终极逃生舱：尝试获取路径，如果被 FUSE 拦截，直接用子进程把它拽到 /tmp 下面运行！
        """
        import shutil
        import stat
        import subprocess

        # 1. 常规探测：先问 PATH 拿人
        src = shutil.which('tray-rs-bin')
        
        # 2. 备用探测：向 APPDIR 拿人
        if not src:
            appdir = os.getenv('APPDIR')
            if appdir:
                src = os.path.join(appdir, 'usr', 'bin', 'tray-rs-bin')
            else:
                base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                src = os.path.join(base, 'tray-rs-bin')

        # 3. 如果 Python 觉得存在，直接返回（源码开发模式通常走这里）
        if src and os.path.exists(src):
            log_main(f"[ESCAPE-POD] Direct access OK: {src}")
            return src

        # 4. 🚨 逃生舱启动：Python 看不见？让 Shell 子进程去拿！
        log_main(f"[ESCAPE-POD] Python stat failed for {src}. Deploying shell extraction to /tmp...")
        
        dest = f"/tmp/lwg-tray-rs-bin-{os.getuid()}"
        try:
            # 用系统的 cp 命令，跨越 Python 的命名空间障碍去拷贝
            r = subprocess.run(
                ['cp', src, dest],
                capture_output=True, text=True, timeout=5
            )
            if r.returncode == 0:
                os.chmod(dest, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)
                log_main(f"[ESCAPE-POD] Shell extraction SUCCESS! New path: {dest}")
                return dest
            else:
                log_main(f"[ESCAPE-POD] Shell extraction FAILED: {r.stderr.strip()}")
        except Exception as e:
            log_main(f"[ESCAPE-POD] Exception during extraction: {e}")

        return ""

    def start(self):
        if self.process and self.process.poll() is None:
            return

        import shutil
        import os

        # 【核心逻辑】读取由启动脚本在 FUSE 存活期预先复制好的临时路径
        # 这样即使 /tmp/.mount_xxx 消失了，/tmp/lwg-tray-rs-xxx 依然永久有效
        rust_tray_path = os.getenv('LWG_TRAY_BIN')

        # [回退方案] 如果是开发环境或环境变量丢失，尝试从 PATH 找
        if not rust_tray_path or not os.path.exists(rust_tray_path):
            rust_tray_path = shutil.which('tray-rs-bin')

        # 最终验证：如果都找不到，才放弃
        if not rust_tray_path or not os.path.exists(rust_tray_path):
            log_main(f"CRITICAL: tray-rs-bin not found. LWG_TRAY_BIN={os.getenv('LWG_TRAY_BIN')}")
            return

        log_main(f"Launching tray from: {rust_tray_path}")

        real_icon_path = self._resolve_icon()
        parent_pid = str(os.getpid())
        
        # 唤醒路径计算
        appdir = os.getenv('APPDIR')
        run_gui_path = os.path.join(appdir, 'AppRun') if appdir else 'run_gui.py'

        try:
            self.process = subprocess.Popen(
                [rust_tray_path, real_icon_path, parent_pid, run_gui_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
            log_main(f"Rust Tray spawned. PID: {self.process.pid}")
            
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