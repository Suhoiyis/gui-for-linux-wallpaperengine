import os
import sys
from typing import Optional, Dict, Any

class EnvironmentDetector:
    """Detect the current running environment type"""
    
    @staticmethod
    def get_environment_type() -> str:
        """
        Detect current running environment.
        Returns: 'appimage', 'arch_package', 'source', or 'system_install'
        """
        # Check for AppImage first (most specific)
        if os.environ.get('APPIMAGE'):
            return 'appimage'
        
        # Check for Arch package installation
        current_path = os.path.abspath(__file__)
        if '/opt/linux-wallpaperengine-gui' in current_path:
            return 'arch_package'
            
        # Check for system installation (installed via pip or similar)
        if '/usr/local/' in current_path or '/usr/lib/' in current_path:
            return 'system_install'
            
        # Default to source mode
        return 'source'
    
    @staticmethod
    def is_appimage() -> bool:
        """Check if running in AppImage environment"""
        return os.environ.get('APPIMAGE') is not None
    
    @staticmethod
    def is_arch_package() -> bool:
        """Check if running as Arch package"""
        current_path = os.path.abspath(__file__)
        return '/opt/linux-wallpaperengine-gui' in current_path
    
    @staticmethod
    def get_appimage_dir() -> Optional[str]:
        """Get AppImage directory if running in AppImage"""
        if EnvironmentDetector.is_appimage():
            return os.environ.get('APPDIR')
        return None