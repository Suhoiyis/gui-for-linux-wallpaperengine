import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from typing import Callable, Optional, List

class NavBar(Gtk.Box):
    def __init__(self, stack: Gtk.Stack, screens: List[str], selected_screen: str,
                 on_home_enter: Optional[Callable] = None,
                 on_screen_changed: Optional[Callable[[str], None]] = None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.stack = stack
        self.on_home_enter = on_home_enter
        self.on_screen_changed_cb = on_screen_changed
        self.screens = screens
        self.selected_screen = selected_screen
        self.add_css_class("nav-bar")
        self.build_ui()

    def build_ui(self):
        screen_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        screen_box.set_margin_start(15)
        self.append(screen_box)

        lbl = Gtk.Label(label="🖥")
        lbl.add_css_class("status-label")
        screen_box.append(lbl)

        self.screen_dd = Gtk.DropDown.new_from_strings(self.screens)
        if self.selected_screen in self.screens:
            self.screen_dd.set_selected(self.screens.index(self.selected_screen))
        self.screen_dd.connect("notify::selected", self._on_screen_changed)
        screen_box.append(self.screen_dd)

        spacer_left = Gtk.Box()
        spacer_left.set_hexpand(True)
        self.append(spacer_left)

        nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.btn_home = Gtk.ToggleButton(label="🏠 Home")
        self.btn_home.add_css_class("nav-btn")
        self.btn_home.set_active(True)
        self.btn_home.connect("toggled", self.on_home_toggled)
        nav_box.append(self.btn_home)

        self.btn_settings = Gtk.ToggleButton(label="⚙️ Settings")
        self.btn_settings.add_css_class("nav-btn")
        self.btn_settings.connect("toggled", self.on_settings_toggled)
        nav_box.append(self.btn_settings)

        self.append(nav_box)

        spacer_right = Gtk.Box()
        spacer_right.set_hexpand(True)
        self.append(spacer_right)

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
            self.stack.set_visible_child_name("wallpapers")
            try:
                if callable(self.on_home_enter):
                    self.on_home_enter()
            except Exception:
                pass

    def on_settings_toggled(self, btn):
        if btn.get_active():
            self.btn_home.set_active(False)
            self.stack.set_visible_child_name("settings")
