import os
import sys
import stat

from py_GUI.const import APP_ID

class AppIntegrator:
    def __init__(self):
        # Resolve paths dynamically based on this file's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(os.path.dirname(current_dir))
        
        self.script_path = os.path.join(self.project_root, "run_gui.py")
        self.icon_path = os.path.join(self.project_root, "pic/icons/GUI_rounded.png")
        self.python_exe = sys.executable
        
        self.app_dir = os.path.expanduser("~/.local/share/applications")
        self.autostart_dir = os.path.expanduser("~/.config/autostart")
        self.desktop_filename = f"{APP_ID}.desktop"

    def _generate_content(self, hidden=False):
        # Check if running inside AppImage
        appimage_path = os.environ.get("APPIMAGE")
        
        if appimage_path:
            # Running inside AppImage - use the AppImage executable itself
            exec_cmd = f"\"{appimage_path}\""
        else:
            # Running from source - use Python to execute run_gui.py
            exec_cmd = f"{self.python_exe} \"{self.script_path}\""
        
        if hidden:
            exec_cmd += " --hidden"
            
        return f"""[Desktop Entry]
Type=Application
Name=Linux Wallpaper Engine
Comment=Wallpaper Engine for Linux (GUI)
Exec={exec_cmd}
Icon={self.icon_path}
Path={self.project_root}
Terminal=false
Categories=Utility;Graphics;
StartupNotify=true
StartupWMClass=linux-wallpaperengine-gui
X-GNOME-Autostart-enabled=true
"""

    def create_menu_shortcut(self):
        """Create shortcut in Applications menu"""
        os.makedirs(self.app_dir, exist_ok=True)
        path = os.path.join(self.app_dir, self.desktop_filename)
        self._write_file(path, self._generate_content(hidden=False))
        return path

    def create_desktop_entry(self):
        """Wrapper for SettingsPage compatibility"""
        try:
            path = self.create_menu_shortcut()
            return True, f"Desktop entry created at: {path}"
        except Exception as e:
            return False, f"Failed to create desktop entry: {str(e)}"


    def set_autostart(self, enabled: bool, hidden: bool = True):
        """Enable or disable autostart"""
        os.makedirs(self.autostart_dir, exist_ok=True)
        path = os.path.join(self.autostart_dir, self.desktop_filename)
        
        if enabled:
            self._write_file(path, self._generate_content(hidden=hidden))
        else:
            if os.path.exists(path):
                os.remove(path)

    def is_autostart_enabled(self) -> bool:
        path = os.path.join(self.autostart_dir, self.desktop_filename)
        return os.path.exists(path)

    def check_and_update_shortcut(self):
        """
        Check if the desktop shortcut exists and update it if content differs.
        
        Returns:
            bool: True if file was updated, False if file missing or content matches.
        """
        path = os.path.join(self.app_dir, self.desktop_filename)
        
        # File doesn't exist
        if not os.path.exists(path):
            print(f"Shortcut file not found: {path}")
            return False
        
        # Read existing content
        try:
            with open(path, "r") as f:
                existing_content = f.read()
        except Exception as e:
            print(f"Error reading shortcut file {path}: {str(e)}")
            return False
        
        # Generate expected content
        expected_content = self._generate_content(hidden=False)
        
        # Compare content
        if existing_content == expected_content:
            print(f"Shortcut file is up to date: {path}")
            return False
        
        # Content differs, update the file
        try:
            self._write_file(path, expected_content)
            print(f"Shortcut file updated: {path}")
            return True
        except Exception as e:
            print(f"Error updating shortcut file {path}: {str(e)}")
            return False

    def _write_file(self, path, content):
        with open(path, "w") as f:
            f.write(content)
        # Make executable
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)
