import os
from typing import Optional
from py_GUI.utils.environment import EnvironmentDetector

class PathManager:
    """Manage resource paths based on environment type"""
    
    def __init__(self):
        self.env_type = EnvironmentDetector.get_environment_type()
        self._setup_paths()
    
    def _setup_paths(self):
        """Setup paths based on environment type"""
        if self.env_type == 'appimage':
            # AppImage: resources are in APPDIR structure
            appdir = EnvironmentDetector.get_appimage_dir()
            if appdir:
                self.app_dir = appdir
                self.resources_dir = os.path.join(appdir, 'usr', 'share', 'linux-wallpaperengine-gui')
            else:
                # Fallback to source mode if APPDIR not available
                self._setup_source_paths()
        elif self.env_type == 'arch_package':
            # Arch package: installed in /opt/
            self.app_dir = '/opt/linux-wallpaperengine-gui'
            self.resources_dir = '/opt/linux-wallpaperengine-gui'
        elif self.env_type == 'system_install':
            # System install: find the actual installation path
            self.app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.resources_dir = self.app_dir
        else:
            # Source mode or unknown
            self._setup_source_paths()
    
    def _setup_source_paths(self):
        """Setup paths for source development mode"""
        # Navigate from py_GUI/utils/path_manager.py to project root
        current_file = os.path.abspath(__file__)
        utils_dir = os.path.dirname(current_file)
        py_gui_dir = os.path.dirname(utils_dir)
        project_root = os.path.dirname(py_gui_dir)
        self.app_dir = project_root
        self.resources_dir = project_root
    
    def get_icon_path(self, icon_name: str) -> str:
        """Get full path to an icon file"""
        return os.path.join(self.resources_dir, 'pic', 'icons', icon_name)
    
    def get_config_dir(self) -> str:
        """Get configuration directory (always in user's home)"""
        return os.path.expanduser('~/.config/linux-wallpaperengine-gui')
    
    def get_config_file(self) -> str:
        """Get configuration file path"""
        return os.path.join(self.get_config_dir(), 'config.json')
    
    def get_workshop_path(self) -> str:
        """Get default workshop path"""
        return os.path.expanduser('~/Steam/steamapps/workshop/content/431960')
    
    def get_assets_path(self) -> str:
        """Get default assets path"""
        return os.path.expanduser('~/Steam/steamapps/common/Wallpaper Engine/assets')