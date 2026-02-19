import os
import sys
import stat

from py_GUI.const import APP_ID

class AppIntegrator:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(os.path.dirname(current_dir))
        
        self.script_path = os.path.join(self.project_root, "run_gui.py")
        self.icon_path = os.path.join(self.project_root, "pic/icons/GUI_rounded.png")
        self.python_exe = sys.executable
        
        self.app_dir = os.path.expanduser("~/.local/share/applications")
        self.autostart_dir = os.path.expanduser("~/.config/autostart")
        self.desktop_filename = f"{APP_ID}.desktop"

    def _generate_content(self, hidden=False):
        appimage_path = os.environ.get("APPIMAGE")
        
        # 针对不同环境适配 Exec, Icon 和 Path
        if appimage_path:
            # 1. AppImage 环境
            exec_cmd = f"\"{appimage_path}\""
            # AppImage 运行时，图标被映射到了系统环境，或者用户使用了 AppImageLauncher
            # 最好只写图标名称，不写绝对路径，避免指向 /tmp/.mount_...
            icon_str = "linux-wallpaperengine-gui"
            path_str = "" # AppImage 不需要指定 Path
            
        elif self.project_root.startswith("/usr/share/"):
            # 2. Arch Linux 安装包环境 (或者其他将代码放在 /usr/share 的包管理)
            # Arch 打包时已经在 /usr/bin 创建了全局命令，直接调用即可
            exec_cmd = "linux-wallpaperengine-gui"
            # Arch 打包时图标已经放到了 hicolor，可以直接用名称
            icon_str = "linux-wallpaperengine-gui"
            path_str = ""
            
        else:
            # 3. 源码直接运行环境
            exec_cmd = f"{self.python_exe} \"{self.script_path}\""
            icon_str = self.icon_path
            path_str = f"Path={self.project_root}\n"
        
        if hidden:
            exec_cmd += " --hidden"
            
        return f"""[Desktop Entry]
Type=Application
Name=Linux Wallpaper Engine
Comment=Wallpaper Engine for Linux (GUI)
Exec={exec_cmd}
Icon={icon_str}
{path_str}Terminal=false
Categories=Utility;Graphics;
StartupNotify=true
StartupWMClass={APP_ID}
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
