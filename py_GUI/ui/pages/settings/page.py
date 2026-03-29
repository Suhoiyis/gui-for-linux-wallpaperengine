# pyright: reportAttributeAccessIssue=false, reportMissingImports=false

from typing import Callable

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gio, Adw

from py_GUI.core.config import ConfigManager
from py_GUI.core.screen import ScreenManager
from py_GUI.core.logger import LogManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.integrations import AppIntegrator
from py_GUI.core.playlists import PlaylistService

from .playback_tab import build_playback_tab
from .audio_tab import build_audio_tab
from .advanced_tab import (
    build_advanced_tab,
    on_browse_workshop as advanced_on_browse_workshop,
    _on_workshop_folder_selected as advanced_on_workshop_folder_selected,
    on_browse_assets as advanced_on_browse_assets,
    _on_assets_folder_selected as advanced_on_assets_folder_selected,
    on_create_desktop_entry as advanced_on_create_desktop_entry,
    on_refresh_screens as advanced_on_refresh_screens,
)
from .logs_tab import (
    build_logs_tab,
    on_filter_changed as logs_on_filter_changed,
    on_level_filter_changed as logs_on_level_filter_changed,
    setup_log_tags as logs_setup_log_tags,
    on_log_update as logs_on_log_update,
    append_log as logs_append_log,
    refresh_logs as logs_refresh_logs,
    clear_logs as logs_clear_logs,
    copy_logs as logs_copy_logs,
    open_engine_log as logs_open_engine_log,
)


class SettingsPage(Gtk.Box):
    def __init__(
        self,
        window,
        config: ConfigManager,
        screen_manager: ScreenManager,
        log_manager: LogManager,
        controller: WallpaperController,
        wp_manager: WallpaperManager,
        nickname_manager,
        playlists: PlaylistService,
        on_cycle_changed=None,
        show_toast: Callable[[str], None] | None = None,
    ):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)

        self.window = window
        self.config = config
        self.screen_manager = screen_manager
        self.log_manager = log_manager
        self.controller = controller
        self.wp_manager = wp_manager
        self.nickname_manager = nickname_manager
        self.playlists = playlists
        self.integrator = AppIntegrator()
        self.on_cycle_settings_changed = on_cycle_changed
        self.show_toast = show_toast or (lambda msg: None)

        self.current_filter = "All"
        self.current_level_filter = "All"
        self.visible_entries_count = 0

        self.add_css_class("settings-container")
        self.build_ui()

    def build_ui(self):
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar.add_css_class("settings-sidebar")
        sidebar.set_size_request(280, -1)
        self.append(sidebar)

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

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_hexpand(True)
        self.stack.set_vexpand(True)
        self.stack.set_vhomogeneous(False)
        self.append(self.stack)

        build_playback_tab(self)
        build_audio_tab(self)
        build_advanced_tab(self)
        build_logs_tab(self)

        for section_id, _, _ in sections:
            btn = self.nav_btns[section_id]
            btn.connect("toggled", self.on_nav_toggled, section_id)

        self.nav_btns["general"].set_active(True)

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
        stop_btn.connect("clicked", self.on_stop_clicked)
        actions.append(stop_btn)

    def on_stop_clicked(self, _button):
        if self.window is not None:
            app = self.window.get_application()
            if app is not None and hasattr(app, "stop_wallpaper"):
                app.stop_wallpaper()

    def on_nav_toggled(self, btn, section_id):
        if btn.get_active():
            for sid, b in self.nav_btns.items():
                if sid != section_id:
                    b.set_active(False)
            self.stack.set_visible_child_name(section_id)

    def on_browse_workshop(self, btn):
        advanced_on_browse_workshop(self, btn)

    def _on_workshop_folder_selected(self, dialog, result):
        advanced_on_workshop_folder_selected(self, dialog, result)

    def on_browse_assets(self, btn):
        advanced_on_browse_assets(self, btn)

    def _on_assets_folder_selected(self, dialog, result):
        advanced_on_assets_folder_selected(self, dialog, result)

    def on_create_desktop_entry(self, btn):
        advanced_on_create_desktop_entry(self, btn)

    def on_refresh_screens(self, btn):
        advanced_on_refresh_screens(self, btn)

    def on_filter_changed(self, dd, pspec):
        logs_on_filter_changed(self, dd, pspec)

    def on_level_filter_changed(self, dd, pspec):
        logs_on_level_filter_changed(self, dd, pspec)

    def setup_log_tags(self):
        logs_setup_log_tags(self)

    def on_log_update(self, entry):
        logs_on_log_update(self, entry)

    def append_log(self, entry):
        logs_append_log(self, entry)

    def refresh_logs(self):
        logs_refresh_logs(self)

    def clear_logs(self):
        logs_clear_logs(self)

    def copy_logs(self, btn):
        logs_copy_logs(self, btn)

    def open_engine_log(self, btn):
        logs_open_engine_log(self, btn)

    def on_manage_nicknames(self, _btn):
        try:
            from py_GUI.ui.components.dialogs.nickname_manager_dialog import (
                NicknameManagerDialog,
            )

            root = self.window

            if root:

                def on_nicknames_saved(needs_refresh=False):
                    app = Gio.Application.get_default()
                    if app and hasattr(app, "wallpapers_page"):
                        if needs_refresh:
                            app.refresh_from_cli()
                        else:
                            app.wallpapers_page.refresh_wallpaper_grid()
                            app.wallpapers_page.update_active_wallpaper_label()

                dialog = NicknameManagerDialog(
                    root,
                    self.nickname_manager,
                    self.wp_manager,
                    on_saved=on_nicknames_saved,
                )
                dialog.present()
            else:
                print("[ERROR] Nickname Manager: Could not find parent window.")
        except Exception as e:
            print(f"[ERROR] Nickname Manager Error: {e}")
            import traceback

            traceback.print_exc()

    def on_save(self, _btn):
        try:
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

            self.config.set("cycleEnabled", self.cycle_sw.get_active())
            self.config.set("cycleInterval", int(self.cycle_spin.get_value()))

            cycle_opts = ["random", "title", "size", "size_desc", "type", "id"]
            sel_idx = self.cycle_order_dd.get_selected()
            if 0 <= sel_idx < len(cycle_opts):
                self.config.set("cycleOrder", cycle_opts[sel_idx])

            playlist_sel_idx = self.cycle_playlist_dd.get_selected()
            if 0 <= playlist_sel_idx < len(self._cycle_playlist_values):
                self.config.set(
                    "cyclePlaylistId", self._cycle_playlist_values[playlist_sel_idx]
                )

            self.config.set("wayland_only_active", self.wl_active_sw.get_active())
            self.config.set("wayland_ignore_appids", self.wl_ignore_entry.get_text())

            self.config.set("silence", self.silence_sw.get_active())
            self.config.set("volume", int(self.vol_spin.get_value()))
            self.config.set("noautomute", self.noautomute_sw.get_active())
            self.config.set("noAudioProcessing", self.noaudioproc_sw.get_active())

            self.config.set("workshopPath", self.path_entry.get_text())

            assets_path = self.assets_entry.get_text().strip()
            self.config.set("assetsPath", assets_path if assets_path else None)

            sel_idx = self.screen_dd.get_selected()
            model = self.screen_dd.get_model()
            if model and 0 <= sel_idx < model.get_n_items():
                selected_screen = model.get_item(sel_idx).get_string()
                self.controller.state.set_last_screen(selected_screen)

            self.integrator.set_autostart(
                self.autostart_sw.get_active(), hidden=self.start_hidden_sw.get_active()
            )

            self.config.set(
                "screenshotDelay", int(self.screenshot_delay_spin.get_value())
            )
            self.config.set("screenshotRes", self.screenshot_res_entry.get_text())
            self.config.set("preferXvfb", self.xvfb_sw.get_active())

            new_path = self.config.get("workshopPath")
            if new_path and new_path != self.wp_manager.workshop_path:
                self.wp_manager.workshop_path = new_path
                self.wp_manager.manifest_path = self.wp_manager._find_manifest_path()
                self.wp_manager.scan()

            if self.on_cycle_settings_changed:
                self.on_cycle_settings_changed()

            self.show_toast("Settings saved successfully")
        except Exception as e:
            self.show_toast(f"Error saving settings: {e}")
            print(f"Save error: {e}")

    def on_reload(self, _btn):
        self.controller.restart_wallpapers()
        self.show_toast("Reloading wallpapers...")
