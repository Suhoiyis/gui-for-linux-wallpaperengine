import subprocess
import os
from py_GUI.const import ICON_PATH

class TrayIcon:
    def __init__(self, app):
        self.app = app
        self.process = None
    
    def start(self):
        """Start the tray icon subprocess"""
        script_path = os.path.join(os.path.dirname(__file__), 'tray_process.py')
        
        # Check if script exists
        if not os.path.exists(script_path):
            print(f"[TRAY] Error: Tray script not found at {script_path}")
            return

        try:
            # Launch separate process for GTK3 AyatanaAppIndicator
            self.process = subprocess.Popen(
                ['python3', script_path, ICON_PATH],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"[TRAY] Failed to start tray process: {e}")
    
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
