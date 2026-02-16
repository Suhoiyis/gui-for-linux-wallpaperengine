import subprocess
import os
from py_GUI.const import ICON_PATH


class TrayIcon:
    def __init__(self, app):
        self.app = app
        self.process = None

    def start(self):
        """Start the tray icon subprocess"""
        log_path = os.environ.get("LWG_TRAY_LOG")

        def log(msg):
            if not log_path:
                return
            try:
                with open(log_path, "a") as f:
                    f.write(f"{msg}\n")
            except Exception:
                pass

        script_path = os.environ.get(
            "LWG_TRAY_SCRIPT",
            os.path.join(os.path.dirname(__file__), "tray_process.py"),
        )
        icon_path = os.environ.get("LWG_TRAY_ICON", ICON_PATH)
        log(f"tray.start script={script_path} icon={icon_path}")

        if not os.path.exists(script_path):
            print(f"[TRAY] Error: Tray script not found at {script_path}")
            log(f"tray.start error=missing_script")
            return

        try:
            log_file = open(log_path, "a") if log_path else None
            self.process = subprocess.Popen(
                ["python3", script_path, icon_path],
                stdout=log_file or subprocess.DEVNULL,
                stderr=log_file or subprocess.DEVNULL,
            )
            log(f"tray.start pid={self.process.pid}")
        except Exception as e:
            print(f"[TRAY] Failed to start tray process: {e}")
            log(f"tray.start exception={e}")

    def stop(self):
        """Stop the tray icon subprocess"""
        if self.process:
            try:
                self.process.terminate()
                try:
                    self.process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    self.process.kill()
            except Exception as e:
                print(f"[TRAY] Error stopping tray: {e}")
            finally:
                self.process = None
