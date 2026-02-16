import subprocess
import os
from py_GUI.const import ICON_PATH


class TrayIcon:
    def __init__(self, app):
        self.app = app
        self.process = None

    def start(self):
        """Start the tray icon subprocess"""
        script_path = os.path.join(os.path.dirname(__file__), "tray_process.py")

        # Debug: print path resolution
        print(f"[TRAY] Debug: __file__ = {__file__}")
        print(f"[TRAY] Debug: dirname(__file__) = {os.path.dirname(__file__)}")
        print(f"[TRAY] Debug: script_path = {script_path}")
        print(f"[TRAY] Debug: ICON_PATH = {ICON_PATH}")

        # Check if script exists
        if not os.path.exists(script_path):
            print(f"[TRAY] Error: Tray script not found at {script_path}")
            # List directory contents for debugging
            try:
                dir_contents = os.listdir(os.path.dirname(__file__))
                print(f"[TRAY] Debug: Directory contents: {dir_contents}")
            except Exception as e:
                print(f"[TRAY] Debug: Failed to list directory: {e}")
            return

        # Check if ICON_PATH exists
        if not os.path.exists(ICON_PATH):
            print(f"[TRAY] Warning: Icon not found at {ICON_PATH}")

        try:
            # Launch separate process for GTK3 AyatanaAppIndicator
            # Enable stdout/stderr for debugging
            self.process = subprocess.Popen(
                ["python3", script_path, ICON_PATH],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(f"[TRAY] Tray process started with PID: {self.process.pid}")
        except Exception as e:
            print(f"[TRAY] Failed to start tray process: {e}")
            import traceback

            traceback.print_exc()

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
