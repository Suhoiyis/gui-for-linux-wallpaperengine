from typing import Dict
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gdk

from py_GUI.const import WORKSHOP_PATH
from py_GUI.core.config import ConfigManager
from py_GUI.core.screen import ScreenManager
from py_GUI.core.logger import LogManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.wallpaper import WallpaperManager

class SettingsPage(Gtk.Box):
    def __init__(self, config: ConfigManager, screen_manager: ScreenManager, 
                 log_manager: LogManager, controller: WallpaperController,
                 wp_manager: WallpaperManager):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        
        self.config = config
        self.screen_manager = screen_manager
        self.log_manager = log_manager
        self.controller = controller
        self.wp_manager = wp_manager
        
        self.add_css_class("settings-container")
        self.build_ui()

    def build_ui(self):
        # Sidebar
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar.add_css_class("settings-sidebar")
        sidebar.set_size_request(280, -1)
        self.append(sidebar)

        # Headers
        header = Gtk.Label(label="Settings")
        header.add_css_class("settings-header")
        header.set_halign(Gtk.Align.START)
        header.set_margin_start(16)
        sidebar.append(header)

        subheader = Gtk.Label(label="Configure your experience")
        subheader.add_css_class("settings-subheader")
        subheader.set_halign(Gtk.Align.START)
        subheader.set_margin_start(16)
        subheader.set_margin_bottom(32)
        sidebar.append(subheader)

        # Nav Buttons
        nav_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        nav_box.set_vexpand(True)
        sidebar.append(nav_box)

        sections = [
            ("general", "🖥 General"),
            ("audio", "🔊 Audio"),
            ("advanced", "⚙️ Advanced"),
            ("logs", "📋 Logs"),
        ]

        self.nav_btns = {}
        for section_id, label in sections:
            btn = Gtk.ToggleButton(label=label)
            btn.add_css_class("settings-nav-item")
            nav_box.append(btn)
            self.nav_btns[section_id] = btn

        # Content Area
        content_scroll = Gtk.ScrolledWindow()
        content_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        content_scroll.set_hexpand(True)
        self.append(content_scroll)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        content_scroll.set_child(self.stack)

        # Build sub-pages
        self.build_general()
        self.build_audio()
        self.build_advanced()
        self.build_logs()

        # Connect signals
        for section_id, _ in sections:
            btn = self.nav_btns[section_id]
            btn.connect("toggled", self.on_nav_toggled, section_id)

        self.nav_btns["general"].set_active(True)

        # Bottom Actions
        actions = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        actions.set_margin_top(24)
        sidebar.append(actions)

        save_btn = Gtk.Button(label="Save Changes")
        save_btn.add_css_class("action-btn")
        save_btn.add_css_class("primary")
        save_btn.connect("clicked", self.on_save)
        actions.append(save_btn)

        refresh_btn = Gtk.Button(label="Reload Wallpapers")
        refresh_btn.add_css_class("action-btn")
        refresh_btn.add_css_class("secondary")
        refresh_btn.connect("clicked", self.on_reload)
        actions.append(refresh_btn)

        stop_btn = Gtk.Button(label="Stop Wallpaper")
        stop_btn.add_css_class("action-btn")
        stop_btn.add_css_class("danger")
        stop_btn.connect("clicked", lambda _: self.controller.stop())
        actions.append(stop_btn)

    def on_nav_toggled(self, btn, section_id):
        if btn.get_active():
            for sid, b in self.nav_btns.items():
                if sid != section_id:
                    b.set_active(False)
            self.stack.set_visible_child_name(section_id)

    def create_row(self, label, desc):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add_css_class("setting-row")
        
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info.set_hexpand(True)
        row.append(info)

        l = Gtk.Label(label=label)
        l.add_css_class("setting-label")
        l.set_halign(Gtk.Align.START)
        info.append(l)

        d = Gtk.Label(label=desc)
        d.add_css_class("setting-desc")
        d.set_halign(Gtk.Align.START)
        info.append(d)
        
        return row

    def build_general(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        self.stack.add_named(box, "general")

        # Titles
        t = Gtk.Label(label="General")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        box.append(t)
        
        # FPS
        r = self.create_row("FPS Limit", "Target frames per second.")
        box.append(r)
        self.fps_spin = Gtk.SpinButton()
        self.fps_spin.set_range(1, 144)
        self.fps_spin.set_increments(1, 10)
        self.fps_spin.set_value(self.config.get("fps", 30))
        r.append(self.fps_spin)

        # Scaling
        r = self.create_row("Scaling Mode", "How the wallpaper fits.")
        box.append(r)
        self.scaling_dd = Gtk.DropDown.new_from_strings(["default", "stretch", "fit", "fill"])
        curr = self.config.get("scaling", "default")
        opts = ["default", "stretch", "fit", "fill"]
        if curr in opts:
            self.scaling_dd.set_selected(opts.index(curr))
        r.append(self.scaling_dd)

        # Pause
        r = self.create_row("No Fullscreen Pause", "Keep running in fullscreen.")
        box.append(r)
        self.pause_sw = Gtk.Switch()
        self.pause_sw.set_active(self.config.get("noFullscreenPause", False))
        self.pause_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.pause_sw)

        # Mouse
        r = self.create_row("Disable Mouse", "Ignore mouse interaction.")
        box.append(r)
        self.mouse_sw = Gtk.Switch()
        self.mouse_sw.set_active(self.config.get("disableMouse", False))
        self.mouse_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.mouse_sw)

    def build_audio(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        self.stack.add_named(box, "audio")

        t = Gtk.Label(label="Audio")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        box.append(t)

        # Silence
        r = self.create_row("Silence Wallpaper", "Mute all audio.")
        box.append(r)
        self.silence_sw = Gtk.Switch()
        self.silence_sw.set_active(self.config.get("silence", True))
        self.silence_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.silence_sw)

        # Volume
        r = self.create_row("Volume", "Master volume (0-100).")
        box.append(r)
        self.vol_spin = Gtk.SpinButton()
        self.vol_spin.set_range(0, 100)
        self.vol_spin.set_increments(5, 10)
        self.vol_spin.set_value(self.config.get("volume", 50))
        r.append(self.vol_spin)

    def build_advanced(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        self.stack.add_named(box, "advanced")

        t = Gtk.Label(label="Advanced")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        box.append(t)

        # Path
        r = self.create_row("Workshop Directory", "Path to Workshop content.")
        r.set_orientation(Gtk.Orientation.VERTICAL)
        box.append(r)
        self.path_entry = Gtk.Entry()
        self.path_entry.set_text(self.config.get("workshopPath", WORKSHOP_PATH))
        self.path_entry.set_hexpand(True)
        r.append(self.path_entry)

        # Screen
        r = self.create_row("Screen Root", "Select a monitor.")
        box.append(r)
        
        screens = self.screen_manager.get_screens()
        curr_screen = self.config.get("lastScreen", "eDP-1")
        if curr_screen not in screens:
            screens = screens + [curr_screen]
        
        self.screen_dd = Gtk.DropDown.new_from_strings(screens)
        self.screen_dd.set_hexpand(True)
        if curr_screen in screens:
            self.screen_dd.set_selected(screens.index(curr_screen))
        r.append(self.screen_dd)

        btn = Gtk.Button(label="⟳ Refresh Screens")
        btn.add_css_class("action-btn")
        btn.add_css_class("secondary")
        btn.connect("clicked", self.on_refresh_screens)
        box.append(btn)

    def build_logs(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        self.stack.add_named(box, "logs")

        t = Gtk.Label(label="Logs")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        box.append(t)

        # Log View
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_size_request(-1, 500)
        box.append(scroll)

        self.log_view = Gtk.TextView()
        self.log_view.set_editable(False)
        self.log_view.set_cursor_visible(False)
        self.log_view.set_monospace(True)
        self.log_view.set_left_margin(8)
        self.log_view.set_right_margin(8)
        scroll.set_child(self.log_view)

        self.log_buffer = self.log_view.get_buffer()
        self.setup_log_tags()

        # Buttons
        btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btns.set_halign(Gtk.Align.END)
        box.append(btns)

        clr_btn = Gtk.Button(label="Clear Logs")
        clr_btn.add_css_class("action-btn")
        clr_btn.add_css_class("secondary")
        clr_btn.connect("clicked", lambda _: self.clear_logs())
        btns.append(clr_btn)

        copy_btn = Gtk.Button(label="Copy Logs")
        copy_btn.add_css_class("action-btn")
        copy_btn.add_css_class("secondary")
        copy_btn.connect("clicked", self.copy_logs)
        btns.append(copy_btn)

        ref_btn = Gtk.Button(label="Refresh")
        ref_btn.add_css_class("action-btn")
        ref_btn.add_css_class("primary")
        ref_btn.connect("clicked", lambda _: self.refresh_logs())
        btns.append(ref_btn)

        self.log_manager.register_callback(self.on_log_update)
        self.refresh_logs()

    def setup_log_tags(self):
        tbl = self.log_buffer.get_tag_table()
        
        def add_tag(name, color):
            tag = Gtk.TextTag(name=name)
            tag.set_property("foreground", color)
            tag.set_property("size-points", 12)
            tbl.add(tag)

        add_tag("timestamp", "#6b7280")
        add_tag("debug", "#6b7280")
        add_tag("info", "#3b82f6")
        add_tag("warning", "#f59e0b")
        add_tag("error", "#ef4444")
        add_tag("source", "#a855f7")
        
        msg_tag = Gtk.TextTag(name="message")
        msg_tag.set_property("foreground", "#e5e7eb")
        msg_tag.set_property("size-points", 12)
        tbl.add(msg_tag)
        
        line_tag = Gtk.TextTag(name="line")
        line_tag.set_property("pixels-above-lines", 8)
        tbl.add(line_tag)

    def on_log_update(self, entry):
        GLib.idle_add(lambda: self.append_log(entry))

    def append_log(self, entry):
        ts = entry.get("timestamp", "")
        lvl = entry.get("level", "")
        src = entry.get("source", "")
        msg = entry.get("message", "")

        end = self.log_buffer.get_end_iter()
        
        self.log_buffer.insert_with_tags_by_name(end, f"[{ts}] ", "timestamp")
        
        lvl_tag = "debug"
        if lvl == "INFO": lvl_tag = "info"
        elif lvl == "WARNING": lvl_tag = "warning"
        elif lvl == "ERROR": lvl_tag = "error"
        
        self.log_buffer.insert_with_tags_by_name(end, f"[{lvl}] ", lvl_tag)
        self.log_buffer.insert_with_tags_by_name(end, f"[{src}] ", "source")
        self.log_buffer.insert_with_tags_by_name(end, f"{msg}\n", "message", "line")

        self.log_view.scroll_to_mark(
            self.log_buffer.create_mark("end", self.log_buffer.get_end_iter(), False),
            0.0, False, 0.0, 0.0
        )

    def refresh_logs(self):
        self.log_buffer.set_text("")
        for entry in self.log_manager.get_logs():
            self.append_log(entry)

    def clear_logs(self):
        self.log_manager.clear()
        self.log_buffer.set_text("")

    def copy_logs(self, btn):
        start = self.log_buffer.get_start_iter()
        end = self.log_buffer.get_end_iter()
        text = self.log_buffer.get_text(start, end, False)
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(text)
        
        orig = btn.get_label()
        btn.set_label("Copied!")
        GLib.timeout_add(2000, lambda: btn.set_label(orig) and False)

    def on_save(self, btn):
        self.config.set("fps", int(self.fps_spin.get_value()))
        opts = ["default", "stretch", "fit", "fill"]
        self.config.set("scaling", opts[self.scaling_dd.get_selected()])
        self.config.set("noFullscreenPause", self.pause_sw.get_active())
        self.config.set("disableMouse", self.mouse_sw.get_active())
        self.config.set("silence", self.silence_sw.get_active())
        self.config.set("volume", int(self.vol_spin.get_value()))
        
        path = self.path_entry.get_text().strip()
        if path:
            self.config.set("workshopPath", path)

        screens = self.screen_manager.get_screens()
        idx = self.screen_dd.get_selected()
        if idx >= 0 and idx < len(screens):
            self.config.set("lastScreen", screens[idx])
        else:
            self.config.set("lastScreen", "eDP-1")
            
        self.log_manager.add_info("Settings saved", "GUI")
        
        # Check if we need to re-apply current wallpaper
        last_wp = self.config.get("lastWallpaper")
        if last_wp:
            self.log_manager.add_info(f"Re-applying wallpaper {last_wp}", "GUI")
            self.controller.apply(last_wp)

    def on_reload(self, btn):
        self.wp_manager.clear_cache()
        path = self.path_entry.get_text().strip()
        if path:
            self.wp_manager.workshop_path = path
        self.wp_manager.scan()
        # Note: WallpapersPage needs to refresh. We might need a global event bus or signal.
        # But for now, user has to go back to Home tab and click refresh there, or we can assume
        # next time they go there it's fine.
        # Ideally, `on_reload` should signal app to refresh wallpapers page.

    def on_refresh_screens(self, btn):
        screens = self.screen_manager.refresh()
        curr = self.config.get("lastScreen", "eDP-1")
        if curr not in screens: screens.append(curr)
        self.screen_dd.set_model(Gtk.StringList.new(screens))
        if curr in screens:
            self.screen_dd.set_selected(screens.index(curr))
