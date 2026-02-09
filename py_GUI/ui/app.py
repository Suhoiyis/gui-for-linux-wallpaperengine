import sys
import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, Gdk, GLib

from py_GUI.const import CSS_STYLE, APP_ID, WORKSHOP_PATH, VERSION
from py_GUI.core.config import ConfigManager
from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.screen import ScreenManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.logger import LogManager
from py_GUI.core.nickname import NicknameManager
from py_GUI.utils import markdown_to_pango

from py_GUI.ui.components.navbar import NavBar
from py_GUI.ui.pages.wallpapers import WallpapersPage
from py_GUI.ui.pages.settings import SettingsPage
from py_GUI.ui.pages.performance import PerformancePage
from py_GUI.ui.tray import TrayIcon
from py_GUI.ui.compact_window import CompactWindow

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
        self.nickname_manager = NicknameManager(self.config)
        self.controller = WallpaperController(self.config, self.prop_manager, self.log_manager, self.screen_manager)
        self.controller.wp_manager = self.wp_manager
        self.controller.nickname_manager = self.nickname_manager

        self.start_hidden = False
        self.cli_actions = []
        self.initialized = False
        self._is_first_activation = True
        self.cycle_timer_id = None
        
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

        # Setup Icon Theme
        display = Gdk.Display.get_default()
        icon_theme = Gtk.IconTheme.get_for_display(display)
        
        # Add 'pic' directory to icon search path
        # py_GUI/ui/app.py -> .../linux-wallpaperengine-gui/
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        pic_path = os.path.join(base_path, "pic")
        
        if os.path.exists(pic_path):
            icon_theme.add_search_path(pic_path)

        self.win = Gtk.ApplicationWindow(application=self)
        self.win.set_title("Linux Wallpaper Engine GUI")
        self.win.set_icon_name("GUI") # Matches GUI_rounded.png in pic/
        self.win.set_default_size(1200, 800)
        self.win.set_size_request(1000, 700)
        self.win.connect("close-request", self.on_window_close)

        # Setup Actions
        self.setup_actions()

        self.toast_overlay = Adw.ToastOverlay()
        self.win.set_child(self.toast_overlay)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.toast_overlay.set_child(main_box)

        # Stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_vexpand(True)

        # Navbar
        screens = self.screen_manager.get_screens()
        selected_screen = self.config.get("lastScreen", screens[0] if screens else "eDP-1")
        initial_link_state = (self.config.get("apply_mode", "diff") == "same")
        initial_compact_state = bool(self.config.get("compact_mode", False))
        
        self.navbar = NavBar(
            self.stack, 
            screens=screens,
            selected_screen=selected_screen,
            on_home_enter=self.on_home_enter,
            on_screen_changed=self.on_navbar_screen_changed,
            on_link_toggled=self.on_navbar_link_toggled,
            on_restart_app=self.restart_app,
            on_compact_mode_toggled=self.on_compact_mode_toggled,
            initial_link_state=initial_link_state,
            initial_compact_state=initial_compact_state
        )
        main_box.append(self.navbar)
        main_box.append(self.stack)

        # Pages
        self.wallpapers_page = WallpapersPage(
            self.win, self.config, self.wp_manager, 
            self.prop_manager, self.controller, self.log_manager,
            self.screen_manager, self.nickname_manager, self.show_toast
        )
        self.stack.add_named(self.wallpapers_page, "wallpapers")

        # Performance Page
        self.performance_page = PerformancePage(self.controller)
        self.stack.add_named(self.performance_page, "performance")

        self.settings_page = SettingsPage(
            self.win, self.config, self.screen_manager, self.log_manager, 
            self.controller, self.wp_manager, self.nickname_manager,
            on_cycle_changed=self.setup_cycle_timer,
            show_toast=self.show_toast
        )
        self.stack.add_named(self.settings_page, "settings")

        self.controller.set_toast_callback(self.show_toast)

        self.compact_win = CompactWindow(
            app=self,
            wp_manager=self.wp_manager,
            controller=self.controller,
            config=self.config,
            log_manager=self.log_manager,
            screen_manager=self.screen_manager,
            nickname_manager=self.nickname_manager,
            show_toast=self.show_toast,
            on_compact_mode_toggled=self.on_compact_mode_toggled,
            on_restart_app=self.restart_app
        )
        self.compact_win.set_icon_name("GUI")

        self.wp_manager.scan()
        self.nickname_manager.cleanup(list(self.wp_manager._wallpapers.keys()))
        self.wallpapers_page.refresh_wallpaper_grid()
        
        if self.wp_manager.last_scan_error:
            GLib.timeout_add(500, lambda: self.show_toast(f"⚠️ {self.wp_manager.last_scan_error}") or False)

        # Restore last session wallpapers
        active_monitors = self.config.get("active_monitors", {})
        screens = self.screen_manager.get_screens()

        # Ensure lastScreen always points to a connected screen (fallback to first/primary)
        last_screen = self.config.get("lastScreen")
        if not last_screen or last_screen not in screens:
            last_screen = screens[0] if screens else "eDP-1"
            self.config.set("lastScreen", last_screen)

        if active_monitors:
            # Fill in missing lastWallpaper for CLI/apply-last correctness
            if not self.config.get("lastWallpaper"):
                if last_screen in active_monitors:
                    self.config.set("lastWallpaper", active_monitors[last_screen])
                elif active_monitors:
                    self.config.set("lastWallpaper", next(iter(active_monitors.values())))

            # Re-launch wallpapers using saved mapping
            self.controller.restart_wallpapers()
            GLib.timeout_add(300, self.wallpapers_page.update_active_wallpaper_label)
            # Do not override user selection; only select current if none
            GLib.timeout_add(350, lambda: self.wallpapers_page.show_current_wallpaper_in_sidebar(False))
        else:
            # Legacy fallback: apply last single wallpaper
            last_wp = self.config.get("lastWallpaper")
            if last_wp:
                self.wallpapers_page.select_wallpaper(last_wp)
                GLib.timeout_add(500, lambda: self.auto_apply(last_wp))

        if self.start_hidden:
            self.win.set_visible(False)
            self.compact_win.set_visible(False)
        elif initial_compact_state:
            self.win.set_visible(False)
            wp_ids = self.wallpapers_page._current_wp_ids
            self.compact_win.sync_from_main(wp_ids, None)
            self.compact_win.set_visible(True)
            self.compact_win.present()
            GLib.timeout_add(100, lambda: self.compact_win.present() or False)
        else:
            self.win.set_visible(True)
            self.win.present()
            GLib.timeout_add(100, lambda: self.win.present() or False)
        self.start_hidden = False
        
        self.initialized = True
        self._is_first_activation = False
        self.setup_cycle_timer()
        self.tray.start()
        
        if self.tray.process and self.tray.process.pid:
            self.controller.perf_monitor.start_monitoring("tray", self.tray.process.pid)
        
        self.consume_cli_actions()

    def auto_apply(self, wp_id):
        if wp_id:
            self.controller.apply(wp_id)
            # Update UI state
            self.wallpapers_page.active_wp = wp_id
            wp = self.wp_manager._wallpapers.get(wp_id)
            if wp:
                self.wallpapers_page.active_wp_label.set_markup(markdown_to_pango(wp['title']))
        return False

    def on_window_close(self, win):
        self.hide_window()
        return True

    def show_window(self):
        is_compact = self.config.get("compact_mode", False)
        if is_compact:
            self.compact_win.set_visible(True)
            self.compact_win.present()
        else:
            self.win.set_visible(True)
            self.win.present()

    def show_toast(self, message: str, timeout: int = 3):
        if hasattr(self, 'toast_overlay'):
            toast = Adw.Toast.new(message)
            toast.set_timeout(timeout)
            self.toast_overlay.add_toast(toast)

    def hide_window(self):
        self.win.set_visible(False)
        if hasattr(self, 'compact_win'):
            self.compact_win.set_visible(False)

    def toggle_window(self):
        is_compact = self.config.get("compact_mode", False)
        if is_compact:
            if self.compact_win.get_visible():
                self.hide_window()
            else:
                self.show_window()
        else:
            if self.win.get_visible():
                self.hide_window()
            else:
                self.show_window()

    def on_home_enter(self):
        try:
            self.wallpapers_page.update_active_wallpaper_label()
            self.wallpapers_page.show_current_wallpaper_in_sidebar(False)
        except Exception:
            pass

    def on_navbar_screen_changed(self, screen: str):
        self.config.set("lastScreen", screen)
        if hasattr(self, 'wallpapers_page'):
            self.wallpapers_page.selected_screen = screen
            self.wallpapers_page.update_active_wallpaper_label()

    def on_navbar_link_toggled(self, is_linked: bool):
        mode = "same" if is_linked else "diff"
        self.config.set("apply_mode", mode)
        if hasattr(self, 'wallpapers_page'):
            self.wallpapers_page.apply_mode = mode
            self.log_manager.add_info(f"Apply mode changed to: {mode}", "App")

    def on_compact_mode_toggled(self, is_compact: bool):
        self.config.set("compact_mode", is_compact)
        
        if is_compact:
            self.win.set_visible(False)
            wp_ids = self.wallpapers_page._current_wp_ids
            selected_wp = self.wallpapers_page.selected_wp
            self.compact_win.sync_from_main(wp_ids, selected_wp)
            self.compact_win.set_visible(True)
            self.compact_win.present()
        else:
            self.compact_win.set_visible(False)
            self.win.set_visible(True)
            self.win.present()
            self.navbar.set_compact_active(False)
        
        self.log_manager.add_info(f"Compact mode: {'enabled' if is_compact else 'disabled'}", "App")

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
        # Tray stop means STOP ALL
        self.controller.stop()
        self.config.set("active_monitors", {})
        self.wallpapers_page.update_active_wallpaper_label()
    
    def random_wallpaper(self):
        # Triggered by cycle timer or CLI or Menu
        # Cycle order logic
        cycle_order = self.config.get("cycleOrder", "random")
        
        active_monitors = self.config.get("active_monitors", {})
        screens = self.screen_manager.get_screens()
        
        # If no monitors active, activate on the last used screen or first available
        if not active_monitors:
            target = self.config.get("lastScreen", screens[0] if screens else "eDP-1")
            active_monitors[target] = None # Placeholder
            
        all_wps = list(self.wp_manager._wallpapers.keys())
        if not all_wps: return

        import random
        new_monitors = {}
        
        # Get sorted list if needed
        sorted_ids = []
        if cycle_order != "random":
             sorted_ids = self.wp_manager.get_sorted_wallpapers(cycle_order)
             # Fallback to random if sort fails or empty
             if not sorted_ids:
                 sorted_ids = all_wps
                 cycle_order = "random"

        for scr in active_monitors.keys():
            if scr in screens:
                if cycle_order == "random":
                    wp_id = random.choice(all_wps)
                else:
                    # Sequential logic
                    current_wp = active_monitors.get(scr)
                    next_index = 0
                    if current_wp and current_wp in sorted_ids:
                        current_index = sorted_ids.index(current_wp)
                        next_index = (current_index + 1) % len(sorted_ids)
                    else:
                        # If current not found or None, start from 0
                        next_index = 0
                    
                    wp_id = sorted_ids[next_index]

                new_monitors[scr] = wp_id
        
        if new_monitors:
            self.config.set("active_monitors", new_monitors)
            # Update lastScreen/lastWallpaper for proper restore & tray apply-last
            primary_screen = self.config.get("lastScreen")
            if primary_screen not in new_monitors:
                primary_screen = next(iter(new_monitors.keys()))
                self.config.set("lastScreen", primary_screen)

            self.config.set("lastWallpaper", new_monitors.get(primary_screen))

            self.controller.restart_wallpapers()
            self.wallpapers_page.update_active_wallpaper_label()
            
            self.log_manager.add_info(f"Cycled wallpaper ({cycle_order})", "App")

    def on_cycle_trigger(self):
        self.log_manager.add_info("Cycling wallpaper...", "App")
        self.random_wallpaper()
        return True # Keep running

    def setup_cycle_timer(self):
        if self.cycle_timer_id:
            GLib.source_remove(self.cycle_timer_id)
            self.cycle_timer_id = None
            
        if self.config.get("cycleEnabled", False):
            interval_mins = self.config.get("cycleInterval", 15)
            # Minimum 1 minute safety
            interval_mins = max(1, interval_mins)
            self.cycle_timer_id = GLib.timeout_add_seconds(
                interval_mins * 60, 
                self.on_cycle_trigger
            )
            self.log_manager.add_info(f"Wallpaper cycling enabled (every {interval_mins} mins)", "App")
        else:
            self.log_manager.add_info("Wallpaper cycling disabled", "App")

    def quit_app(self):
        self.controller.stop()
        self.tray.stop()
        self.quit()

    def restart_app(self):
        self.log_manager.add_info("Restarting application...", "App")
        self.controller.stop()
        self.tray.stop()
        
        import os
        import sys
        
        args = [arg for arg in sys.argv if arg not in ("--hidden", "--minimized")]
        os.execv(sys.executable, [sys.executable] + args)

    def setup_actions(self):
        action_apply = Gio.SimpleAction.new("apply", GLib.VariantType.new("s"))
        action_apply.connect("activate", self.on_action_apply)
        self.win.add_action(action_apply)

        action_stop = Gio.SimpleAction.new("stop", None)
        action_stop.connect("activate", self.on_action_stop)
        self.win.add_action(action_stop)

        action_delete = Gio.SimpleAction.new("delete", GLib.VariantType.new("s"))
        action_delete.connect("activate", self.on_action_delete)
        self.win.add_action(action_delete)
        
        action_open_folder = Gio.SimpleAction.new("open_folder", GLib.VariantType.new("s"))
        action_open_folder.connect("activate", self.on_action_open_folder)
        self.win.add_action(action_open_folder)
        
        action_refresh = Gio.SimpleAction.new("refresh", None)
        action_refresh.connect("activate", self.on_action_refresh)
        self.win.add_action(action_refresh)
        
        action_restart = Gio.SimpleAction.new("restart", None)
        action_restart.connect("activate", self.on_action_restart)
        self.win.add_action(action_restart)
        
        action_about = Gio.SimpleAction.new("about", None)
        action_about.connect("activate", self.on_action_about)
        self.win.add_action(action_about)
        
        action_quit_app = Gio.SimpleAction.new("quit_app", None)
        action_quit_app.connect("activate", self.on_action_quit_request)
        self.win.add_action(action_quit_app)

    def on_action_apply(self, action, param):
        wp_id = param.get_string()
        if wp_id:
            self.wallpapers_page.select_wallpaper(wp_id)
            self.wallpapers_page.apply_wallpaper(wp_id)
            self.setup_cycle_timer()

    def on_action_stop(self, action, param):
        self.stop_wallpaper()

    def on_action_delete(self, action, param):
        wp_id = param.get_string()
        if wp_id:
            self.wallpapers_page.delete_wallpaper(wp_id)
            
    def on_action_open_folder(self, action, param):
        wp_id = param.get_string()
        if wp_id:
            self.wallpapers_page.open_wallpaper_folder(wp_id)

    def on_action_refresh(self, action, param):
        self.refresh_from_cli()

    def on_action_restart(self, action, param):
        self.restart_app()

    def on_action_about(self, action, param):
        try:
            dialog = Adw.AboutDialog(
                application_name="Linux Wallpaper Engine GUI",
                application_icon="GUI_rounded",
                version=VERSION,
                developer_name="Suhoiyis",
                license_type=Gtk.License.GPL_3_0,
                website="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine",
                issue_url="https://github.com/Suhoiyis/gui-for-linux-wallpaperengine/issues",
                copyright="© 2026 Suhoiyis"
            )
            dialog.present(self.win)
        except Exception as e:
            self.show_toast(f"Error opening About dialog: {str(e)}")

    def on_action_quit_request(self, action, param):
        dialog = Adw.MessageDialog.new(self.win)
        dialog.set_heading("Quit Application?")
        dialog.set_body("This will stop all running wallpapers and exit the application.")
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("quit", "Quit")
        dialog.set_response_appearance("quit", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.connect("response", self.on_quit_dialog_response)
        dialog.present()

    def on_quit_dialog_response(self, dialog, response):
        if response == "quit":
             self.quit_app()



def main():
    # Set program name for WM class matching - must match the .desktop filename
    GLib.set_prgname(APP_ID)
    app = WallpaperApp()
    app.run(sys.argv)
