import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class NavBar(Gtk.Box):
    def __init__(self, stack: Gtk.Stack):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.stack = stack
        self.set_halign(Gtk.Align.CENTER)
        self.add_css_class("nav-bar")
        self.build_ui()

    def build_ui(self):
        # Home Button
        self.btn_home = Gtk.ToggleButton(label="🏠 Home")
        self.btn_home.add_css_class("nav-btn")
        self.btn_home.set_active(True)
        self.btn_home.connect("toggled", self.on_home_toggled)
        self.append(self.btn_home)

        # Settings Button
        self.btn_settings = Gtk.ToggleButton(label="⚙️ Settings")
        self.btn_settings.add_css_class("nav-btn")
        self.btn_settings.connect("toggled", self.on_settings_toggled)
        self.append(self.btn_settings)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        self.append(spacer)

    def on_home_toggled(self, btn):
        if btn.get_active():
            self.btn_settings.set_active(False)
            self.stack.set_visible_child_name("wallpapers")

    def on_settings_toggled(self, btn):
        if btn.get_active():
            self.btn_home.set_active(False)
            self.stack.set_visible_child_name("settings")
