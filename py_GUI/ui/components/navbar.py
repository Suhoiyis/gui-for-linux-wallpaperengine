import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from typing import Callable, Optional, List

class NavBar(Gtk.Box):
    def __init__(self, stack: Gtk.Stack, screens: List[str], selected_screen: str,
                 on_home_enter: Optional[Callable] = None,
                 on_screen_changed: Optional[Callable[[str], None]] = None,
                 on_link_toggled: Optional[Callable[[bool], None]] = None,
                 on_restart_app: Optional[Callable] = None,
                 initial_link_state: bool = False):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.stack = stack
        self.on_home_enter = on_home_enter
        self.on_screen_changed_cb = on_screen_changed
        self.on_link_toggled_cb = on_link_toggled
        self.on_restart_app = on_restart_app
        self.screens = screens
        self.selected_screen = selected_screen
        self.is_linked = initial_link_state
        self.add_css_class("nav-bar")
        self.build_ui()

    def build_ui(self):
        screen_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        screen_box.set_margin_start(15)
        self.append(screen_box)

        if len(self.screens) > 1:
            self.btn_link = Gtk.ToggleButton()
            self.btn_link.set_icon_name("link-symbolic" if self.is_linked else "unlink-symbolic")
            self.btn_link.set_active(self.is_linked)
            self.btn_link.set_tooltip_text("Link screens (Apply to All)" if self.is_linked else "Unlink screens (Apply to Single)")
            self.btn_link.add_css_class("flat")
            self.btn_link.connect("toggled", self.on_link_toggled)
            screen_box.append(self.btn_link)

        icon_screen = Gtk.Image.new_from_icon_name("video-display-symbolic")
        icon_screen.add_css_class("status-label")
        screen_box.append(icon_screen)

        self.screen_dd = Gtk.DropDown.new_from_strings(self.screens)
        if self.selected_screen in self.screens:
            self.screen_dd.set_selected(self.screens.index(self.selected_screen))
        self.screen_dd.connect("notify::selected", self._on_screen_changed)
        screen_box.append(self.screen_dd)

        spacer_left = Gtk.Box()
        spacer_left.set_hexpand(True)
        self.append(spacer_left)

        nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.btn_home = Gtk.ToggleButton()
        self.btn_home.set_icon_name("user-home-symbolic")
        self.btn_home.set_tooltip_text("Home")
        self.btn_home.add_css_class("nav-btn")
        self.btn_home.set_active(True)
        self.btn_home.connect("toggled", self.on_home_toggled)
        nav_box.append(self.btn_home)

        self.btn_performance = Gtk.ToggleButton()
        self.btn_performance.set_icon_name("org.gnome.SystemMonitor-symbolic")
        self.btn_performance.set_tooltip_text("Performance")
        self.btn_performance.add_css_class("nav-btn")
        self.btn_performance.connect("toggled", self.on_performance_toggled)
        nav_box.append(self.btn_performance)

        self.btn_settings = Gtk.ToggleButton()
        self.btn_settings.set_icon_name("emblem-system-symbolic")
        self.btn_settings.set_tooltip_text("Settings")
        self.btn_settings.add_css_class("nav-btn")
        self.btn_settings.connect("toggled", self.on_settings_toggled)
        nav_box.append(self.btn_settings)

        self.append(nav_box)

        spacer_right = Gtk.Box()
        spacer_right.set_hexpand(True)
        self.append(spacer_right)

        if self.on_restart_app:
            self.btn_restart = Gtk.Button()
            self.btn_restart.set_icon_name("system-reboot-symbolic")
            self.btn_restart.set_tooltip_text("Restart Application")
            self.btn_restart.add_css_class("nav-btn")
            self.btn_restart.set_margin_end(15)
            self.btn_restart.connect("clicked", lambda _: self.on_restart_app())
            self.append(self.btn_restart)

    def on_link_toggled(self, btn):
        self.is_linked = btn.get_active()
        btn.set_icon_name("link-symbolic" if self.is_linked else "unlink-symbolic")
        btn.set_tooltip_text("Link screens (Apply to All)" if self.is_linked else "Unlink screens (Apply to Single)")
        if callable(self.on_link_toggled_cb):
            self.on_link_toggled_cb(self.is_linked)

    def _on_screen_changed(self, dd, pspec):
        selected_item = dd.get_selected_item()
        if selected_item:
            screen = selected_item.get_string()
            self.selected_screen = screen
            if callable(self.on_screen_changed_cb):
                self.on_screen_changed_cb(screen)

    def get_selected_screen(self) -> str:
        return self.selected_screen

    def on_home_toggled(self, btn):
        if btn.get_active():
            self.btn_settings.set_active(False)
            self.btn_performance.set_active(False)
            self.stack.set_visible_child_name("wallpapers")
            try:
                if callable(self.on_home_enter):
                    self.on_home_enter()
            except Exception:
                pass

    def on_performance_toggled(self, btn):
        if btn.get_active():
            self.btn_home.set_active(False)
            self.btn_settings.set_active(False)
            self.stack.set_visible_child_name("performance")

    def on_settings_toggled(self, btn):
        if btn.get_active():
            self.btn_home.set_active(False)
            self.btn_performance.set_active(False)
            self.stack.set_visible_child_name("settings")
