import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_GUI.utils.environment import EnvironmentDetector
from py_GUI.utils.path_manager import PathManager


class TestEnvironmentDetection(unittest.TestCase):
    """Test environment detection functionality"""
    
    def test_source_environment(self):
        """Test source environment detection"""
        # Mock no AppImage environment
        with patch.dict(os.environ, {}, clear=True):
            env_type = EnvironmentDetector.get_environment_type()
            self.assertEqual(env_type, 'source')
    
    def test_appimage_environment(self):
        """Test AppImage environment detection"""
        # Mock AppImage environment
        with patch.dict(os.environ, {'APPIMAGE': '/tmp/test.AppImage'}):
            env_type = EnvironmentDetector.get_environment_type()
            self.assertEqual(env_type, 'appimage')
            self.assertTrue(EnvironmentDetector.is_appimage())
    
    def test_arch_package_environment(self):
        """Test Arch package environment detection"""
        # Mock Arch package path
        with patch('py_GUI.utils.environment.os.path.abspath') as mock_abspath:
            mock_abspath.return_value = '/opt/linux-wallpaperengine-gui/py_GUI/utils/environment.py'
            env_type = EnvironmentDetector.get_environment_type()
            self.assertEqual(env_type, 'arch_package')


class TestPathManager(unittest.TestCase):
    """Test path manager functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.original_environ = os.environ.copy()
    
    def tearDown(self):
        """Clean up test fixtures"""
        os.environ.clear()
        os.environ.update(self.original_environ)
    
    def test_source_path_manager(self):
        """Test path manager in source environment"""
        # Clear environment for source mode
        with patch.dict(os.environ, {}, clear=True):
            pm = PathManager()
            self.assertEqual(pm.env_type, 'source')
            # Should point to project root
            self.assertTrue(pm.app_dir.endswith('suw'))
            self.assertTrue(os.path.exists(pm.get_icon_path('gui_tray_rounded.png')))
    
    def test_appimage_path_manager(self):
        """Test path manager in AppImage environment"""
        # Mock AppImage environment
        with patch.dict(os.environ, {'APPIMAGE': '/tmp/test.AppImage', 'APPDIR': '/tmp/appdir'}):
            pm = PathManager()
            self.assertEqual(pm.env_type, 'appimage')
            self.assertEqual(pm.app_dir, '/tmp/appdir')
            expected_icon_path = '/tmp/appdir/usr/share/linux-wallpaperengine-gui/pic/icons/gui_tray_rounded.png'
            self.assertEqual(pm.get_icon_path('gui_tray_rounded.png'), expected_icon_path)
    
    def test_config_paths(self):
        """Test configuration paths are always in user directory"""
        pm = PathManager()
        config_dir = pm.get_config_dir()
        config_file = pm.get_config_file()
        
        self.assertTrue(config_dir.startswith(os.path.expanduser('~/.config/')))
        self.assertTrue(config_file.endswith('config.json'))


if __name__ == '__main__':
    unittest.main()