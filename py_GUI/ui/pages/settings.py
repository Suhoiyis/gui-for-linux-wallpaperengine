from typing import Dict, Callable
import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, GLib, Gdk, Adw

from py_GUI.const import WORKSHOP_PATH, ASSETS_PATH
from py_GUI.core.config import ConfigManager
from py_GUI.core.screen import ScreenManager
from py_GUI.core.logger import LogManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.integrations import AppIntegrator

class SettingsPage(Gtk.Box):
    def __init__(self, config: ConfigManager, screen_manager: ScreenManager, 
                 log_manager: LogManager, controller: WallpaperController,
                 wp_manager: WallpaperManager, on_cycle_changed=None,
                 show_toast: Callable[[str], None] = None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        
        self.config = config
        self.screen_manager = screen_manager
        self.log_manager = log_manager
        self.controller = controller
        self.wp_manager = wp_manager
        self.integrator = AppIntegrator()
        self.on_cycle_settings_changed = on_cycle_changed
        self.show_toast = show_toast or (lambda msg: None)
        
        self.current_filter = "All"
        
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
            ("general", "General", "preferences-system-symbolic"),
            ("audio", "Audio", "audio-volume-high-symbolic"),
            ("advanced", "Advanced", "preferences-other-symbolic"),
            ("logs", "Logs", "text-x-generic-symbolic"),
        ]

        self.nav_btns = {}
        for section_id, label, icon in sections:
            btn = Gtk.ToggleButton()
            content = Adw.ButtonContent()
            content.set_icon_name(icon)
            content.set_label(label)
            btn.set_child(content)
            
            btn.add_css_class("settings-nav-item")
            nav_box.append(btn)
            self.nav_btns[section_id] = btn

        # Content Area - Stack directly without shared ScrolledWindow
        # Each tab manages its own scrolling to avoid showing scrollbar on short content
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_hexpand(True)
        self.stack.set_vexpand(True)
        self.stack.set_vhomogeneous(False)  # Allow different heights per page
        self.append(self.stack)

        # Build sub-pages
        self.build_general()
        self.build_audio()
        self.build_advanced()
        self.build_logs()

        # Connect signals
        for section_id, _, _ in sections:
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
            # No dynamic scroll policy needed

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
        d.set_wrap(True)
        d.set_max_width_chars(50)
        info.append(d)
        
        return row

    def build_general(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.stack.add_named(scroll, "general")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        scroll.set_child(box)

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
        scaling_opts = ["default", "stretch", "fit", "fill"]
        self.scaling_dd = Gtk.DropDown.new_from_strings(scaling_opts)
        curr = str(self.config.get("scaling", "default"))
        if curr in scaling_opts:
            self.scaling_dd.set_selected(scaling_opts.index(curr))
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

        # Parallax
        r = self.create_row("Disable Parallax", "Disable background movement with mouse.")
        box.append(r)
        self.parallax_sw = Gtk.Switch()
        self.parallax_sw.set_active(self.config.get("disableParallax", False))
        self.parallax_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.parallax_sw)

        # Particles
        r = self.create_row("Disable Particles", "Turn off fire, rain, and other particles.")
        box.append(r)
        self.particles_sw = Gtk.Switch()
        self.particles_sw.set_active(self.config.get("disableParticles", False))
        self.particles_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.particles_sw)

        # Clamping
        r = self.create_row("Clamping Mode", "Texture wrap mode at edges.")
        box.append(r)
        clamp_opts = ["clamp", "border", "repeat"]
        self.clamp_dd = Gtk.DropDown.new_from_strings(clamp_opts)
        curr_clamp = self.config.get("clamping", "clamp")
        if curr_clamp in clamp_opts:
            self.clamp_dd.set_selected(clamp_opts.index(curr_clamp))
        r.append(self.clamp_dd)

        # Automation
        t = Gtk.Label(label="Automation")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        t.set_margin_top(10)
        box.append(t)

        # Wallpaper Cycling
        r = self.create_row("Enable Wallpaper Cycling", "Automatically change wallpapers periodically.")
        box.append(r)
        self.cycle_sw = Gtk.Switch()
        self.cycle_sw.set_active(self.config.get("cycleEnabled", False))
        self.cycle_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.cycle_sw)

        # Interval
        r = self.create_row("Cycle Interval (Minutes)", "Time between wallpaper changes.")
        box.append(r)
        self.cycle_spin = Gtk.SpinButton()
        self.cycle_spin.set_range(1, 1440) # 1 min to 24 hours
        self.cycle_spin.set_increments(5, 30)
        self.cycle_spin.set_value(self.config.get("cycleInterval", 15))
        r.append(self.cycle_spin)

        # Order
        r = self.create_row("Cycle Order", "Order in which wallpapers are cycled.")
        box.append(r)
        order_opts = ["Random", "Title", "Size ↑", "Size ↓", "Type", "ID"]
        self.cycle_order_dd = Gtk.DropDown.new_from_strings(order_opts)
        
        curr_order = self.config.get("cycleOrder", "random").lower()
        # Find index
        idx = 0
        if curr_order == "size": 
             curr_order = "size ↑"
        elif curr_order == "size_desc":
             curr_order = "size ↓"

        for i, opt in enumerate(order_opts):
            if opt.lower() == curr_order:
                idx = i
                break
        self.cycle_order_dd.set_selected(idx)
        r.append(self.cycle_order_dd)

        # Wayland Tweaks
        t = Gtk.Label(label="Wayland Tweaks")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        t.set_margin_top(10)
        box.append(t)

        is_wayland = os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
        
        status_label = "✅ Wayland Session Detected" if is_wayland else "⚠️ X11 Session"
        desc = "Wayland-specific pause strategies."
        if not is_wayland:
            desc += " (Options disabled in X11)"
            
        r = self.create_row("Session Check", desc)
        box.append(r)
        
        lbl_status = Gtk.Label(label=status_label)
        lbl_status.add_css_class("status-value")
        if not is_wayland:
            lbl_status.add_css_class("text-muted")
        r.append(lbl_status)

        r = self.create_row("Pause Only When Active", "Only pause when fullscreen window is focused.")
        box.append(r)
        self.wl_active_sw = Gtk.Switch()
        self.wl_active_sw.set_active(self.config.get("wayland_only_active", False))
        self.wl_active_sw.set_valign(Gtk.Align.CENTER)
        if not is_wayland: self.wl_active_sw.set_sensitive(False)
        r.append(self.wl_active_sw)

        r = self.create_row("Ignore App IDs", "Comma-separated list of App IDs to ignore (e.g. dock,bar).")
        r.set_orientation(Gtk.Orientation.VERTICAL)
        box.append(r)
        
        self.wl_ignore_entry = Gtk.Entry()
        self.wl_ignore_entry.set_text(self.config.get("wayland_ignore_appids", ""))
        self.wl_ignore_entry.set_placeholder_text("app_id1, app_id2")
        if not is_wayland: self.wl_ignore_entry.set_sensitive(False)
        r.append(self.wl_ignore_entry)

    def build_audio(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.stack.add_named(scroll, "audio")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        scroll.set_child(box)

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

        # No Auto Mute
        r = self.create_row("Disable Auto Mute", "Prevent automatic muting when other apps play sound.")
        box.append(r)
        self.noautomute_sw = Gtk.Switch()
        self.noautomute_sw.set_active(self.config.get("noautomute", False))
        self.noautomute_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.noautomute_sw)

        # No Audio Processing
        r = self.create_row("Disable Audio Processing", "Disable sound spectrum analysis (saves CPU).")
        box.append(r)
        self.noaudioproc_sw = Gtk.Switch()
        self.noaudioproc_sw.set_active(self.config.get("noAudioProcessing", False))
        self.noaudioproc_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.noaudioproc_sw)

    def build_advanced(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.stack.add_named(scroll, "advanced")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        scroll.set_child(box)

        t = Gtk.Label(label="Advanced")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        box.append(t)

        # Path
        r = self.create_row("Workshop Directory", "Path to Steam Workshop content (431960).")
        r.set_orientation(Gtk.Orientation.VERTICAL)
        box.append(r)
        
        workshop_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.path_entry = Gtk.Entry()
        self.path_entry.set_text(self.config.get("workshopPath", WORKSHOP_PATH))
        self.path_entry.set_hexpand(True)
        workshop_box.append(self.path_entry)
        
        browse_workshop_btn = Gtk.Button(label="Browse")
        browse_workshop_btn.add_css_class("action-btn")
        browse_workshop_btn.add_css_class("secondary")
        browse_workshop_btn.connect("clicked", self.on_browse_workshop)
        workshop_box.append(browse_workshop_btn)
        r.append(workshop_box)

        # Assets Directory
        r = self.create_row("Assets Directory", "Wallpaper Engine assets folder (leave empty for auto-detect).")
        r.set_orientation(Gtk.Orientation.VERTICAL)
        box.append(r)
        
        assets_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.assets_entry = Gtk.Entry()
        assets_path = self.config.get("assetsPath", None)
        self.assets_entry.set_text(assets_path if assets_path else "")
        self.assets_entry.set_placeholder_text("Auto-detect from Steam installation")
        self.assets_entry.set_hexpand(True)
        assets_box.append(self.assets_entry)
        
        browse_assets_btn = Gtk.Button(label="Browse")
        browse_assets_btn.add_css_class("action-btn")
        browse_assets_btn.add_css_class("secondary")
        browse_assets_btn.connect("clicked", self.on_browse_assets)
        assets_box.append(browse_assets_btn)
        r.append(assets_box)

        # Screen
        r = self.create_row("Screen Root", "Select a monitor.")
        box.append(r)
        
        screens = self.screen_manager.get_screens()
        curr_screen = self.config.get("lastScreen", "eDP-1")
        if curr_screen not in screens:
            screens = screens + [curr_screen]
        
        self.screen_dd = Gtk.DropDown.new_from_strings(screens)
        self.screen_dd.set_hexpand(True)
        if curr_screen and curr_screen in screens:
            self.screen_dd.set_selected(screens.index(str(curr_screen)))
        r.append(self.screen_dd)

        btn = Gtk.Button()
        content = Adw.ButtonContent()
        content.set_icon_name("view-refresh-symbolic")
        content.set_label("Refresh Screens")
        btn.set_child(content)
        
        btn.add_css_class("action-btn")
        btn.add_css_class("secondary")
        btn.connect("clicked", self.on_refresh_screens)
        box.append(btn)

        # System Integration
        t = Gtk.Label(label="System Integration")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        t.set_margin_top(10)
        box.append(t)

        # Desktop Entry
        r = self.create_row("Desktop Shortcut", "Create app icon in system menu.")
        box.append(r)
        self.btn_create_desktop = Gtk.Button(label="Create")
        self.btn_create_desktop.set_valign(Gtk.Align.CENTER)
        self.btn_create_desktop.connect("clicked", self.on_create_desktop_entry)
        r.append(self.btn_create_desktop)

        # Autostart
        r = self.create_row("Run on Startup", "Launch automatically on login.")
        box.append(r)
        self.autostart_sw = Gtk.Switch()
        self.autostart_sw.set_active(self.integrator.is_autostart_enabled())
        self.autostart_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.autostart_sw)

        # Start Hidden
        r = self.create_row("Start Hidden", "Start in tray without showing window.")
        box.append(r)
        self.start_hidden_sw = Gtk.Switch()
        self.start_hidden_sw.set_active(True)
        self.start_hidden_sw.set_valign(Gtk.Align.CENTER)
        r.append(self.start_hidden_sw)

        t_ss = Gtk.Label(label="Screenshot")
        t_ss.add_css_class("settings-section-title")
        t_ss.set_halign(Gtk.Align.START)
        t_ss.set_margin_top(10)
        box.append(t_ss)

        # Screenshot Delay
        r = self.create_row("Screenshot Delay", "Frames to wait before capture (use higher for web wallpapers).")
        box.append(r)
        self.screenshot_delay_spin = Gtk.SpinButton()
        self.screenshot_delay_spin.set_range(1, 600)
        self.screenshot_delay_spin.set_increments(5, 50)
        self.screenshot_delay_spin.set_value(self.config.get("screenshotDelay", 20))
        r.append(self.screenshot_delay_spin)

        # Screenshot Resolution
        r = self.create_row("Screenshot Resolution", "Target resolution (e.g. 1920x1080, 3840x2160).")
        box.append(r)
        self.screenshot_res_entry = Gtk.Entry()
        self.screenshot_res_entry.set_text(self.config.get("screenshotRes", "3840x2160"))
        self.screenshot_res_entry.set_hexpand(False)
        self.screenshot_res_entry.set_width_chars(15)
        r.append(self.screenshot_res_entry)

        # Xvfb Status Check
        import shutil
        has_xvfb = shutil.which("xvfb-run") is not None
        
        status_label = "✅ Xvfb Installed (Silent Mode)" if has_xvfb else "⚠️ Xvfb Not Found (Window Mode)"
        status_desc = "Silent capture using virtual framebuffer."
        
        r = self.create_row("Capture Backend", status_desc)
        box.append(r)
        
        status_val = Gtk.Label(label=status_label)
        status_val.add_css_class("status-value")
        if not has_xvfb:
            status_val.add_css_class("text-muted") 
        
        r.append(status_val)

        # Prefer Xvfb Switch
        r = self.create_row("Prefer Silent Capture", "Use Xvfb if installed to avoid popup windows.")
        box.append(r)
        self.xvfb_sw = Gtk.Switch()
        self.xvfb_sw.set_active(self.config.get("preferXvfb", True))
        self.xvfb_sw.set_valign(Gtk.Align.CENTER)
        if not has_xvfb:
            self.xvfb_sw.set_tooltip_text("Xvfb is not installed on this system.")
        r.append(self.xvfb_sw)

    def on_browse_workshop(self, btn):
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Workshop Directory")
        dialog.select_folder(self.get_root(), None, self._on_workshop_folder_selected)

    def _on_workshop_folder_selected(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                path = folder.get_path()
                self.path_entry.set_text(path)
        except GLib.Error:
            pass

    def on_browse_assets(self, btn):
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Assets Directory")
        dialog.select_folder(self.get_root(), None, self._on_assets_folder_selected)

    def _on_assets_folder_selected(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                path = folder.get_path()
                self.assets_entry.set_text(path)
        except GLib.Error:
            pass

    def on_create_desktop_entry(self, btn):
        success, msg = self.integrator.create_desktop_entry()
        if success:
            self.show_toast("Desktop entry created successfully")
        else:
            self.show_toast(f"Failed to create desktop entry: {msg}")

    def on_refresh_screens(self, btn):
        self.screen_manager.detect_screens()
        screens = self.screen_manager.get_screens()
        
        # Preserve selection if possible
        selected = self.screen_dd.get_selected_item()
        selected_str = selected.get_string() if selected else None
        
        self.screen_dd.set_model(Gtk.StringList.new(screens))
        
        if selected_str and selected_str in screens:
            self.screen_dd.set_selected(screens.index(selected_str))
        elif screens:
            self.screen_dd.set_selected(0)
            
        self.show_toast(f"Screens refreshed: {', '.join(screens)}")

    def build_logs(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(60)
        box.set_margin_bottom(60)
        box.set_margin_start(40)
        box.set_margin_end(40)
        self.stack.add_named(box, "logs")

        # Header with Filter
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.append(header_box)

        t = Gtk.Label(label="Logs")
        t.add_css_class("settings-section-title")
        t.set_halign(Gtk.Align.START)
        t.set_hexpand(True)
        header_box.append(t)

        # Filter Dropdown
        filter_opts = ["All", "Controller", "Engine", "GUI"]
        self.filter_dd = Gtk.DropDown.new_from_strings(filter_opts)
        self.filter_dd.set_valign(Gtk.Align.CENTER)
        self.filter_dd.connect("notify::selected", self.on_filter_changed)
        header_box.append(self.filter_dd)

        # Log View
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
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

    def on_filter_changed(self, dd, pspec):
        selected = dd.get_selected_item()
        if selected:
            self.current_filter = selected.get_string()
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

        if self.current_filter != "All":
            if self.current_filter == "GUI":
                if src in ["Controller", "Engine"]:
                    return
            elif src != self.current_filter:
                return

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
        try:
            # General
            self.config.set("fps", int(self.fps_spin.get_value()))
            
            scaling_opts = ["default", "stretch", "fit", "fill"]
            idx = self.scaling_dd.get_selected()
            if 0 <= idx < len(scaling_opts):
                self.config.set("scaling", scaling_opts[idx])
                
            self.config.set("noFullscreenPause", self.pause_sw.get_active())
            self.config.set("disableMouse", self.mouse_sw.get_active())
            self.config.set("disableParallax", self.parallax_sw.get_active())
            self.config.set("disableParticles", self.particles_sw.get_active())
            
            clamp_opts = ["clamp", "border", "repeat"]
            idx = self.clamp_dd.get_selected()
            if 0 <= idx < len(clamp_opts):
                self.config.set("clamping", clamp_opts[idx])

            # Automation
            self.config.set("cycleEnabled", self.cycle_sw.get_active())
            self.config.set("cycleInterval", int(self.cycle_spin.get_value()))
            
            cycle_opts = ["random", "title", "size", "size_desc", "type", "id"]
            # Map UI index to config value
            # UI: ["Random", "Title", "Size ↑", "Size ↓", "Type", "ID"]
            sel_idx = self.cycle_order_dd.get_selected()
            if 0 <= sel_idx < len(cycle_opts):
                self.config.set("cycleOrder", cycle_opts[sel_idx])
            
            self.config.set("wayland_only_active", self.wl_active_sw.get_active())
            self.config.set("wayland_ignore_appids", self.wl_ignore_entry.get_text())

            # Audio
            self.config.set("silence", self.silence_sw.get_active())
            self.config.set("volume", int(self.vol_spin.get_value()))
            self.config.set("noautomute", self.noautomute_sw.get_active())
            self.config.set("noAudioProcessing", self.noaudioproc_sw.get_active())

            # Advanced
            self.config.set("workshopPath", self.path_entry.get_text())
            
            assets_path = self.assets_entry.get_text().strip()
            self.config.set("assetsPath", assets_path if assets_path else None)
            
            # Screen Root
            screens = self.screen_manager.get_screens()
            sel_idx = self.screen_dd.get_selected()
            # If screens list changed since build, this might be risky, but refresh updates model
            # Re-fetch model from dropdown?
            model = self.screen_dd.get_model()
            if model and 0 <= sel_idx < model.get_n_items():
                selected_screen = model.get_item(sel_idx).get_string()
                self.config.set("lastScreen", selected_screen)

            # Autostart
            if self.autostart_sw.get_active():
                self.integrator.enable_autostart(hidden=self.start_hidden_sw.get_active())
            else:
                self.integrator.disable_autostart()

            # Screenshot
            self.config.set("screenshotDelay", int(self.screenshot_delay_spin.get_value()))
            self.config.set("screenshotRes", self.screenshot_res_entry.get_text())
            self.config.set("preferXvfb", self.xvfb_sw.get_active())

            self.wp_manager.set_workshop_path(self.config.get("workshopPath"))
            
            # Trigger cycle timer update if needed
            if self.on_cycle_settings_changed:
                self.on_cycle_settings_changed()

            self.show_toast("Settings saved successfully")
            
            # Restart if active to apply immediate changes (like FPS/Scaling)
            # Optional: Ask user? Or just do it.
            # self.controller.restart_wallpapers() 
            
        except Exception as e:
            self.show_toast(f"Error saving settings: {e}")
            print(f"Save error: {e}")

    def on_reload(self, btn):
        self.controller.restart_wallpapers()
        self.show_toast("Reloading wallpapers...")
