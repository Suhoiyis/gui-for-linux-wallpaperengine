import os
import sys
import stat

class AppIntegrator:
    def __init__(self):
        # Resolve paths dynamically based on this file's location
        # this file is in py_GUI/core/integrations.py
        # root is ../../..
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(os.path.dirname(current_dir))
        
        self.script_path = os.path.join(self.project_root, "run_gui.py")
        self.icon_path = os.path.join(self.project_root, "pic/gui_tray.png")
        self.python_exe = sys.executable
        
        self.app_dir = os.path.expanduser("~/.local/share/applications")
        self.autostart_dir = os.path.expanduser("~/.config/autostart")
        self.desktop_filename = "linux-wallpaperengine-gui.desktop"

    def _generate_content(self, hidden=False):
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

    def _write_file(self, path, content):
        with open(path, "w") as f:
            f.write(content)
        # Make executable
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)
