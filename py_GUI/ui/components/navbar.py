import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, GLib
from typing import Callable, Optional, List, Dict

class NavBar(Gtk.Box):
    def __init__(self, stack: Gtk.Stack, screens: List[str], selected_screen: str,
                 on_home_enter: Optional[Callable] = None,
                 on_screen_changed: Optional[Callable[[str], None]] = None,
                 on_link_toggled: Optional[Callable[[bool], None]] = None,
                 on_restart_app: Optional[Callable] = None,
                 on_compact_mode_toggled: Optional[Callable[[bool], None]] = None,
                 initial_link_state: bool = False,
                 initial_compact_state: bool = False):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.stack = stack
        self.on_home_enter = on_home_enter
        self.on_screen_changed_cb = on_screen_changed
        self.on_link_toggled_cb = on_link_toggled
        self.on_restart_app = on_restart_app
        self.on_compact_mode_toggled_cb = on_compact_mode_toggled
        self.screens = screens
        self.selected_screen = selected_screen
        self.is_linked = initial_link_state
        self.is_compact = initial_compact_state
        self._compact_mode = False
        self.add_css_class("nav-bar")
        self.build_ui()

    def build_ui(self):
        self.screen_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.screen_box.set_margin_start(15)
        self.append(self.screen_box)

        if len(self.screens) > 1:
            self.btn_link = Gtk.ToggleButton()
            self.btn_link.set_icon_name("link-symbolic" if self.is_linked else "unlink-symbolic")
            self.btn_link.set_active(self.is_linked)
            self.btn_link.set_tooltip_text("Link screens (Apply to All)" if self.is_linked else "Unlink screens (Apply to Single)")
            self.btn_link.add_css_class("nav-btn")
            self.btn_link.connect("toggled", self.on_link_toggled)
            self.screen_box.append(self.btn_link)

        icon_screen = Gtk.Image.new_from_icon_name("video-display-symbolic")
        icon_screen.add_css_class("status-label")
        self.screen_box.append(icon_screen)

        self.screen_dd = Gtk.DropDown.new_from_strings(self.screens)
        self.screen_dd.add_css_class("nav-btn")
        if self.selected_screen in self.screens:
            self.screen_dd.set_selected(self.screens.index(self.selected_screen))
        self.screen_dd.connect("notify::selected", self._on_screen_changed)
        self.screen_box.append(self.screen_dd)

        self.spacer_left = Gtk.Box()
        self.spacer_left.set_hexpand(True)
        self.append(self.spacer_left)

        self.nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.btn_home = Gtk.ToggleButton()
        self.btn_home.set_icon_name("user-home-symbolic")
        self.btn_home.set_tooltip_text("Home")
        self.btn_home.add_css_class("nav-btn")
        self.btn_home.set_active(True)
        self.btn_home.connect("toggled", self.on_home_toggled)
        self.nav_box.append(self.btn_home)

        self.btn_performance = Gtk.ToggleButton()
        self.btn_performance.set_icon_name("org.gnome.SystemMonitor-symbolic")
        self.btn_performance.set_tooltip_text("Performance")
        self.btn_performance.add_css_class("nav-btn")
        self.btn_performance.connect("toggled", self.on_performance_toggled)
        self.nav_box.append(self.btn_performance)

        self.btn_settings = Gtk.ToggleButton()
        self.btn_settings.set_icon_name("emblem-system-symbolic")
        self.btn_settings.set_tooltip_text("Settings")
        self.btn_settings.add_css_class("nav-btn")
        self.btn_settings.connect("toggled", self.on_settings_toggled)
        self.nav_box.append(self.btn_settings)

        self.append(self.nav_box)

        self.spacer_right = Gtk.Box()
        self.spacer_right.set_hexpand(True)
        self.append(self.spacer_right)
        
        self.btn_compact = Gtk.ToggleButton()
        self.btn_compact.set_icon_name("view-restore-symbolic")
        self.btn_compact.set_tooltip_text("Compact Preview Mode")
        self.btn_compact.add_css_class("nav-btn")
        self.btn_compact.set_active(self.is_compact)
        self.btn_compact.connect("toggled", self._on_compact_toggled)
        self.btn_compact.set_margin_end(6)
        self.append(self.btn_compact)
        
        self.btn_menu = Gtk.MenuButton()
        self.btn_menu.set_icon_name("open-menu-symbolic")
        self.btn_menu.set_tooltip_text("Menu")
        self.btn_menu.add_css_class("nav-btn")
        self.btn_menu.set_margin_end(15)
        
        self.menu_popover = Gtk.Popover()
        self.menu_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.menu_content.set_margin_start(2)
        self.menu_content.set_margin_end(2)
        self.menu_content.set_margin_top(4)
        self.menu_content.set_margin_bottom(4)
        self.menu_popover.set_child(self.menu_content)
        self.btn_menu.set_popover(self.menu_popover)
        
        self._add_menu_btn("Playback History", "win.show_history")
        self._add_menu_btn("Refresh Library", "win.refresh")
        self._add_menu_btn("Welcome / Setup Wizard", "win.welcome")
        self._add_menu_btn("Check for Updates", "win.check_update")
        self._add_menu_btn("About", "win.about")
        
        sep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep2.set_margin_top(4)
        sep2.set_margin_bottom(4)
        self.menu_content.append(sep2)
        
        self._add_menu_btn("Restart Application", "win.restart", bold=True)
        self._add_menu_btn("Quit Application", "win.quit_app", bold=True, destructive=True)

        self.append(self.btn_menu)

    def _add_menu_btn(self, label_text, action_name, param=None, bold=False, destructive=False, container=None):
        if container is None:
            container = self.menu_content

        btn = Gtk.Button()
        btn.add_css_class("flat")
        btn.add_css_class("popover-btn")
        btn.set_halign(Gtk.Align.FILL)
        
        lbl = Gtk.Label(xalign=0)
        
        weight = "bold" if bold else "normal"
        color_span_start = f"<span foreground='#ef4444'>" if destructive else ""
        color_span_end = "</span>" if destructive else ""
        
        markup = f"<span weight='{weight}'>{color_span_start}{label_text}{color_span_end}</span>"
        
        lbl.set_markup(markup)
        
        btn.set_child(lbl)
        
        def on_clicked(b):
            self.menu_popover.popdown()
            root = self.get_native()
            if root and hasattr(root, 'activate_action'):
                root.activate_action(action_name, param)
            else:
                print(f"[ERROR] NavBar: Could not find root window to activate {action_name}")
        
        btn.connect("clicked", on_clicked)
        container.append(btn)
        return btn

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

    def _on_compact_toggled(self, btn):
        self.is_compact = btn.get_active()
        if callable(self.on_compact_mode_toggled_cb):
            self.on_compact_mode_toggled_cb(self.is_compact)

    def set_compact_active(self, active: bool):
        self.is_compact = active
        self.btn_compact.set_active(active)

    def set_compact_mode(self, enabled: bool):
        self._compact_mode = enabled
        self.screen_box.set_visible(not enabled)
        self.nav_box.set_visible(not enabled)
        self.spacer_left.set_visible(not enabled)
        self.spacer_right.set_visible(not enabled)


