import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, Gdk, GLib

from py_GUI.const import CSS_STYLE, APP_ID, WORKSHOP_PATH
from py_GUI.core.config import ConfigManager
from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.screen import ScreenManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.logger import LogManager

from py_GUI.ui.components.navbar import NavBar
from py_GUI.ui.pages.wallpapers import WallpapersPage
from py_GUI.ui.pages.settings import SettingsPage
from py_GUI.ui.tray import TrayIcon

class WallpaperApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )
        self.config = ConfigManager()
        self.log_manager = LogManager()
        
        workshop_path = self.config.get("workshopPath", WORKSHOP_PATH)
        self.wp_manager = WallpaperManager(workshop_path)
        self.prop_manager = PropertiesManager(self.config)
        self.screen_manager = ScreenManager()
        self.controller = WallpaperController(self.config, self.prop_manager, self.log_manager)

        self.start_hidden = False
        self.cli_actions = []
        self.initialized = False
        self._is_first_activation = True
        
        self.tray = TrayIcon(self)

    def do_command_line(self, command_line):
        argv = command_line.get_arguments()[1:]
        for arg in argv:
            if arg in ("--minimized", "--hidden"):
                if self.initialized:
                    self.cli_actions.append("hide")
                else:
                    self.start_hidden = True
            elif arg == "--show":
                self.cli_actions.append("show")
            elif arg == "--hide":
                self.cli_actions.append("hide")
            elif arg == "--toggle":
                self.cli_actions.append("toggle")
            elif arg == "--refresh":
                self.cli_actions.append("refresh")
            elif arg == "--apply-last":
                self.cli_actions.append("apply-last")
            elif arg == "--stop":
                self.cli_actions.append("stop")
            elif arg == "--random":
                self.cli_actions.append("random")
            elif arg == "--quit":
                self.cli_actions.append("quit")
        
        self.activate()
        return 0

    def do_activate(self):
        if self.initialized:
            if self._is_first_activation and not self.start_hidden:
                self.show_window()
            self._is_first_activation = False
            self.start_hidden = False
            self.consume_cli_actions()
            return

        # Load CSS
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS_STYLE.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.win = Adw.ApplicationWindow(application=self)
        self.win.set_title("Linux Wallpaper Engine GUI")
        self.win.set_default_size(1200, 800)
        self.win.set_size_request(1000, 700)
        self.win.connect("close-request", self.on_window_close)

        # Main Layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.win.set_content(main_box)

        # Stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_vexpand(True)

        # Navbar
        self.navbar = NavBar(self.stack)
        main_box.append(self.navbar)
        main_box.append(self.stack)

        # Pages
        self.wallpapers_page = WallpapersPage(
            self.win, self.config, self.wp_manager, 
            self.prop_manager, self.controller, self.log_manager
        )
        self.stack.add_named(self.wallpapers_page, "wallpapers")

        self.settings_page = SettingsPage(
            self.config, self.screen_manager, self.log_manager, 
            self.controller, self.wp_manager
        )
        self.stack.add_named(self.settings_page, "settings")

        # Initial Load
        self.wp_manager.scan()
        self.wallpapers_page.refresh_wallpaper_grid()

        # Restore Last Wallpaper State (UI only)
        last_wp = self.config.get("lastWallpaper")
        if last_wp:
            self.wallpapers_page.select_wallpaper(last_wp)
            # Auto Apply
            GLib.timeout_add(500, lambda: self.auto_apply(last_wp))

        if self.start_hidden:
            self.win.set_visible(False)
        else:
            self.win.present()
        self.start_hidden = False
        
        self.initialized = True
        self.tray.start()
        self.consume_cli_actions()

    def auto_apply(self, wp_id):
        if wp_id:
            self.controller.apply(wp_id)
            # Update UI state
            self.wallpapers_page.active_wp = wp_id
            wp = self.wp_manager._wallpapers.get(wp_id)
            if wp:
                self.wallpapers_page.active_wp_label.set_label(wp['title'])
        return False

    def on_window_close(self, win):
        self.hide_window()
        return True

    def show_window(self):
        if self.win:
            self.win.set_visible(True)
            self.win.present()

    def hide_window(self):
        if self.win:
            self.win.set_visible(False)

    def toggle_window(self):
        if self.win:
            if self.win.get_visible():
                self.hide_window()
            else:
                self.show_window()

    def refresh_from_cli(self):
        self.wallpapers_page.on_reload_wallpapers(None)

    def apply_last_from_cli(self):
        last_wp = self.config.get("lastWallpaper")
        if last_wp:
            self.auto_apply(last_wp)

    def consume_cli_actions(self):
        if not self.cli_actions: return
        actions = list(self.cli_actions)
        self.cli_actions.clear()
        
        for action in actions:
            if action == "show": self.show_window()
            elif action == "hide": self.hide_window()
            elif action == "toggle": self.toggle_window()
            elif action == "refresh": self.refresh_from_cli()
            elif action == "apply-last": self.apply_last_from_cli()
            elif action == "stop": self.stop_wallpaper()
            elif action == "random": self.random_wallpaper()
            elif action == "quit": self.quit_app()

    def stop_wallpaper(self):
        self.wallpapers_page.on_stop_clicked()
    
    def random_wallpaper(self):
        self.wallpapers_page.on_feeling_lucky(None)

    def quit_app(self):
        self.controller.stop()
        self.tray.stop()
        self.quit()

def main():
    app = WallpaperApp()
    app.run(sys.argv)
