"""
UI Module Import Tests
Tests that all refactored module paths resolve correctly.
"""

import unittest
import importlib.util
import sys


class TestModuleImports(unittest.TestCase):
    """Test that all UI module paths can be imported."""

    def _check_module(self, module_path: str, should_exist: bool = True):
        """Helper to check if a module path exists."""
        spec = importlib.util.find_spec(module_path)
        if should_exist:
            self.assertIsNotNone(spec, f"Module {module_path} should exist")
        return spec

    # === Old paths (backward compatibility) ===
    def test_old_components_dialogs(self):
        self._check_module("py_GUI.ui.components.dialogs")

    def test_old_components_navbar(self):
        self._check_module("py_GUI.ui.components.navbar")

    def test_old_components_sidebar(self):
        self._check_module("py_GUI.ui.components.sidebar")

    def test_old_pages_wallpapers(self):
        self._check_module("py_GUI.ui.pages.wallpapers")

    def test_old_pages_settings(self):
        self._check_module("py_GUI.ui.pages.settings")

    # === New paths (refactored structure) ===
    def test_new_components_layout_navbar(self):
        self._check_module("py_GUI.ui.components.layout.navbar")

    def test_new_components_library_sidebar(self):
        self._check_module("py_GUI.ui.components.library.sidebar")

    def test_new_components_common_animated_preview(self):
        self._check_module("py_GUI.ui.components.common.animated_preview")

    def test_new_components_common_command_palette(self):
        self._check_module("py_GUI.ui.components.common.command_palette")

    def test_new_components_performance_sparkline(self):
        self._check_module("py_GUI.ui.components.performance.sparkline")

    def test_new_components_dialogs_package(self):
        self._check_module("py_GUI.ui.components.dialogs")

    def test_new_components_dialogs_delete(self):
        self._check_module("py_GUI.ui.components.dialogs.delete_dialog")

    def test_new_components_dialogs_error(self):
        self._check_module("py_GUI.ui.components.dialogs.error_dialog")

    def test_new_pages_library(self):
        self._check_module("py_GUI.ui.pages.library")

    def test_new_pages_settings_package(self):
        self._check_module("py_GUI.ui.pages.settings")


class TestCompileAll(unittest.TestCase):
    """Test that all Python files compile without syntax errors."""

    def test_compileall_py_gui(self):
        import compileall
        import py_GUI

        result = compileall.compile_dir(py_GUI.__path__[0], force=True, quiet=1)
        # result is True if all files compiled successfully
        self.assertTrue(result, "All py_GUI files should compile without errors")


if __name__ == "__main__":
    unittest.main()
