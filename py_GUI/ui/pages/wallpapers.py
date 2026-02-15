import random
import os
import signal
import time
from typing import Dict, Optional, Callable
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gdk, Gio, Pango, GLib

from py_GUI.ui.components.sidebar import Sidebar
from py_GUI.ui.components.dialogs import (
    show_delete_dialog,
    show_error_dialog,
    show_screenshot_success_dialog,
    show_nickname_dialog,
)
from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.config import ConfigManager
from py_GUI.core.logger import LogManager
from py_GUI.utils import markdown_to_pango, format_size

from py_GUI.core.screen import ScreenManager


class WallpapersPage(Gtk.Box):
    def __init__(
        self,
        window: Gtk.Window,
        config: ConfigManager,
        wp_manager: WallpaperManager,
        prop_manager: PropertiesManager,
        controller: WallpaperController,
        log_manager: LogManager,
        screen_manager: ScreenManager,
        nickname_manager,
        show_toast: Callable[[str], None] = None,
    ):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.window = window
        self.config = config
        self.wp_manager = wp_manager
        self.prop_manager = prop_manager
        self.controller = controller
        self.log_manager = log_manager
        self.nickname_manager = nickname_manager
        self.screen_manager = screen_manager
        self.show_toast = show_toast or (lambda msg: None)

        self.view_mode = "grid"
        self.search_query = ""
        self.sort_mode: str = self.config.get("sortMode", "title") or "title"
        self.sort_reverse: bool = bool(self.config.get("sortReverse", False))
        self.selected_wp: Optional[str] = None
        self.active_wp: Optional[str] = None  # Tracks running wallpaper

        # We need to track current screen selection
        self.selected_screen = self.config.get("lastScreen") or "eDP-1"
        self.apply_mode = self.config.get("apply_mode") or "diff"

        self._current_wp_ids = []

        # Cache for filtered wallpapers
        self._filtered_wallpapers: Optional[Dict] = None
        self._filter_cache_key: Optional[tuple] = None

        self.build_ui()
        self._setup_key_controller()

    def build_ui(self):
        # Toolbar
        self.build_toolbar()
        self.append(self.toolbar)

        # Content Box
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.content_box.set_vexpand(True)
        self.content_box.set_hexpand(True)
        self.append(self.content_box)

        # Left Area
        self.left_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.left_area.set_hexpand(True)
        self.content_box.append(self.left_area)

        # Status Panel
        self.build_status_panel(self.left_area)

        # Containers
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_halign(Gtk.Align.CENTER)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.set_row_spacing(5)
        self.flowbox.set_column_spacing(5)
        self.flowbox.set_margin_top(20)
        self.flowbox.set_margin_bottom(20)
        self.flowbox.set_margin_start(20)
        self.flowbox.set_margin_end(20)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.set_margin_top(20)
        self.listbox.set_margin_bottom(20)
        self.listbox.set_margin_start(20)
        self.listbox.set_margin_end(20)

        # Dual ScrolledWindow architecture for grid/list views
        self.grid_scroll = Gtk.ScrolledWindow()
        self.grid_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.grid_scroll.set_vexpand(True)
        self.grid_scroll.set_child(self.flowbox)

        self.list_scroll = Gtk.ScrolledWindow()
        self.list_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.list_scroll.set_vexpand(True)
        self.list_scroll.set_child(self.listbox)

        # Stack to manage view visibility
        self.view_stack = Gtk.Stack()
        self.view_stack.add_named(self.grid_scroll, "grid")
        self.view_stack.add_named(self.list_scroll, "list")
        self.left_area.append(self.view_stack)

        # Sidebar
        self.sidebar = Sidebar(
            self.wp_manager,
            self.prop_manager,
            self.controller,
            self.log_manager,
            self.nickname_manager,
        )

        screens = self.screen_manager.get_screens()
        self.sidebar.set_available_screens(screens)
        self.sidebar.set_current_screen_callback(lambda: self.selected_screen)
        self.sidebar.set_apply_mode_callback(
            lambda: getattr(self, "apply_mode", "diff")
        )
        self.sidebar.set_thumb_clicked_callback(self.select_wallpaper)
        self.sidebar.set_compact_callbacks(
            on_stop=self.on_stop_clicked,
            on_lucky=lambda: self.on_feeling_lucky(None),
            on_jump=lambda: self.on_currently_using_clicked(),
        )
        self.sidebar.btn_edit_nickname.connect(
            "clicked",
            lambda _: (
                self.on_edit_nickname(self.selected_wp) if self.selected_wp else None
            ),
        )

        self.content_box.append(self.sidebar)

    def build_toolbar(self):
        self.toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.toolbar.add_css_class("toolbar")

        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.toolbar.append(search_box)

        icon_search = Gtk.Image.new_from_icon_name("system-search-symbolic")
        icon_search.add_css_class("status-label")
        search_box.append(icon_search)

        self.search_entry = Gtk.Entry()
        self.search_entry.add_css_class("search-entry")
        self.search_entry.set_placeholder_text("Search wallpapers...")
        self.search_entry.set_width_chars(50)
        self.search_entry.connect("changed", self.on_search_changed)
        self.search_entry.connect("activate", self.on_search_activate)
        search_box.append(self.search_entry)

        sort_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.toolbar.append(sort_box)

        icon_sort = Gtk.Image.new_from_icon_name("view-sort-ascending-symbolic")
        icon_sort.add_css_class("status-label")
        sort_box.append(icon_sort)

        sort_options = ["Title", "Size ↓", "Size ↑", "Type", "ID"]
        self.sort_dd = Gtk.DropDown.new_from_strings(sort_options)

        initial_idx = 0
        if self.sort_mode == "size" and self.sort_reverse:
            initial_idx = 1
        elif self.sort_mode == "size":
            initial_idx = 2
        elif self.sort_mode == "type":
            initial_idx = 3
        elif self.sort_mode == "id":
            initial_idx = 4
        self.sort_dd.set_selected(initial_idx)

        self.sort_dd.connect("notify::selected", self.on_sort_changed)
        sort_box.append(self.sort_dd)

        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        self.toolbar.append(spacer)

        # Actions
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.toolbar.append(actions_box)

        stop_btn = Gtk.Button()
        stop_btn.set_icon_name("media-playback-stop-symbolic")
        stop_btn.add_css_class("flat")
        stop_btn.add_css_class("mode-btn")
        stop_btn.add_css_class("stop-btn")
        stop_btn.set_tooltip_text("Stop Wallpaper")
        stop_btn.connect("clicked", lambda _: self.on_stop_clicked())
        actions_box.append(stop_btn)

        lucky_btn = Gtk.Button()
        lucky_btn.set_icon_name("media-playlist-shuffle-symbolic")
        lucky_btn.add_css_class("flat")
        lucky_btn.add_css_class("mode-btn")
        lucky_btn.set_tooltip_text("I'm feeling lucky")
        lucky_btn.connect("clicked", self.on_feeling_lucky)
        actions_box.append(lucky_btn)

        self.btn_screenshot = Gtk.Button()
        self.btn_screenshot.add_css_class("flat")
        self.btn_screenshot.add_css_class("mode-btn")
        self.btn_screenshot.set_tooltip_text("Take Screenshot of current wallpaper")

        self.screenshot_stack = Gtk.Stack()
        self.screenshot_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)

        icon = Gtk.Image.new_from_icon_name("camera-photo-symbolic")
        self.screenshot_stack.add_named(icon, "icon")

        self.screenshot_spinner = Gtk.Spinner()
        self.screenshot_spinner.set_size_request(24, 24)
        self.screenshot_stack.add_named(self.screenshot_spinner, "spinner")

        self.screenshot_stack.set_visible_child_name("icon")
        self.btn_screenshot.set_child(self.screenshot_stack)

        self.btn_screenshot.connect("clicked", lambda _: self.on_screenshot_clicked())
        actions_box.append(self.btn_screenshot)

        # View Toggle
        view_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        view_box.set_margin_start(10)
        self.toolbar.append(view_box)

        self.btn_grid = Gtk.ToggleButton()
        self.btn_grid.set_icon_name("view-grid-symbolic")
        self.btn_grid.set_tooltip_text("Grid View")
        self.btn_grid.add_css_class("flat")
        self.btn_grid.add_css_class("mode-btn")
        self.btn_grid.set_active(True)
        self._grid_signal_id = self.btn_grid.connect("toggled", self.on_view_grid)
        view_box.append(self.btn_grid)

        self.btn_list = Gtk.ToggleButton()
        self.btn_list.set_icon_name("view-list-symbolic")
        self.btn_list.set_tooltip_text("List View")
        self.btn_list.add_css_class("flat")
        self.btn_list.add_css_class("mode-btn")
        self._list_signal_id = self.btn_list.connect("toggled", self.on_view_list)
        view_box.append(self.btn_list)

    def build_status_panel(self, parent: Gtk.Box):
        status_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        status_box.add_css_class("status-panel")
        status_box.set_margin_start(20)
        status_box.set_margin_end(10)
        status_box.set_margin_top(2)
        status_box.set_margin_bottom(2)

        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title_row.set_halign(Gtk.Align.FILL)

        left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title_row.append(left_box)

        title = Gtk.Label(label="CURRENTLY USING")
        title.add_css_class("status-label")
        title.set_halign(Gtk.Align.START)
        left_box.append(title)

        self.copy_cmd_btn = Gtk.Button()
        self.copy_cmd_btn.set_icon_name("edit-copy-symbolic")
        self.copy_cmd_btn.add_css_class("flat")
        self.copy_cmd_btn.set_tooltip_text("Copy command")
        self.copy_cmd_btn.connect("clicked", self.on_copy_command_clicked)
        left_box.append(self.copy_cmd_btn)

        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        title_row.append(spacer)

        self.jump_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.jump_box.set_halign(Gtk.Align.END)
        title_row.append(self.jump_box)

        self.entry_jump = Gtk.Entry()
        self.entry_jump.set_has_frame(False)
        self.entry_jump.set_width_chars(1)
        self.entry_jump.set_max_width_chars(4)
        self.entry_jump.set_alignment(1.0)
        self.entry_jump.add_css_class("status-value-yellow")
        self.entry_jump.set_tooltip_text("Type number and Enter to jump")
        self.entry_jump.connect("activate", self._on_jump_entry_activate)
        self.jump_box.append(self.entry_jump)

        self.lbl_jump_total = Gtk.Label(label="/0")
        self.lbl_jump_total.add_css_class("status-value-yellow")
        self.jump_box.append(self.lbl_jump_total)

        status_box.append(title_row)

        self.active_wp_label = Gtk.Label(label="-")
        self.active_wp_label.add_css_class("status-value")
        self.active_wp_label.set_use_markup(True)
        self.active_wp_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.active_wp_label.set_halign(Gtk.Align.START)
        try:
            self.active_wp_label.set_tooltip_text("Show current wallpaper details")
            self.active_wp_label.set_cursor_from_name("pointer")
        except Exception:
            pass
        click = Gtk.GestureClick.new()
        click.set_button(Gdk.BUTTON_PRIMARY)
        click.connect("released", lambda *_: self.on_currently_using_clicked())
        self.active_wp_label.add_controller(click)
        status_box.append(self.active_wp_label)

        parent.append(status_box)

    def update_active_wallpaper_label(self):
        active_monitors = self.config.get("active_monitors") or {}
        current_wp_id = active_monitors.get(self.selected_screen)

        if current_wp_id:
            wp = self.wp_manager._wallpapers.get(current_wp_id)
            if wp:
                display_name, _ = self.nickname_manager.get_display_name(wp)
                title = display_name
            else:
                title = current_wp_id
            self.active_wp_label.set_markup(markdown_to_pango(title))
        else:
            self.active_wp_label.set_label("None")

        cmd = self.controller.get_current_command()
        if cmd:
            escaped_cmd = GLib.markup_escape_text(cmd)
            self.copy_cmd_btn.set_tooltip_markup(
                f"<b><i>Click to copy:</i></b>\n<tt>{escaped_cmd}</tt>"
            )
            self.copy_cmd_btn.set_sensitive(True)
        else:
            self.copy_cmd_btn.set_tooltip_text("No command running")
            self.copy_cmd_btn.set_sensitive(False)

        self.update_counter_label()

    def update_counter_label(self):
        filtered = self.get_filtered_wallpapers()
        total = len(filtered)

        if total == 0:
            self.entry_jump.set_text("0")
            self.lbl_jump_total.set_label("/0")
            return

        active_monitors = self.config.get("active_monitors") or {}
        current_wp_id = active_monitors.get(self.selected_screen)

        self.lbl_jump_total.set_label(f"/{total}")

        if current_wp_id and current_wp_id in filtered:
            wp_index = list(filtered.keys()).index(current_wp_id) + 1
            self.entry_jump.set_text(str(wp_index))
        else:
            self.entry_jump.set_text("-")

    def _on_jump_entry_activate(self, entry):
        text = entry.get_text().strip()
        if not text:
            return

        try:
            self._jump_to_index(int(text))
        except ValueError:
            self.update_counter_label()

    def _jump_to_index(self, idx: int):
        filtered = self.get_filtered_wallpapers()
        total = len(filtered)
        if total == 0:
            return

        if idx < 1:
            idx = 1
        if idx > total:
            idx = total

        ids = list(filtered.keys())
        wp_id = ids[idx - 1]
        self.select_wallpaper(wp_id)

    def show_current_wallpaper_in_sidebar(self, force: bool = False):
        # Only auto-select if user hasn't selected another wallpaper, unless forced
        if not force and self.selected_wp is not None:
            return False
        active_monitors = self.config.get("active_monitors") or {}
        current_wp_id = active_monitors.get(self.selected_screen)
        if current_wp_id:
            # Highlight and show details
            self.select_wallpaper(current_wp_id)
            # Sidebar updates inside select_wallpaper
            return True
        return False

    def on_currently_using_clicked(self):
        if not self.show_current_wallpaper_in_sidebar(force=True):
            last_wp = self.config.get("lastWallpaper")
            if last_wp:
                self.select_wallpaper(last_wp)

    def on_copy_command_clicked(self, btn):
        cmd = self.controller.get_current_command()
        if not cmd:
            self.show_toast("No command to copy")
            return

        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(cmd)
        self.show_toast("📋 Command copied to clipboard")

    def on_view_grid(self, btn):
        # Only set toggle start time if an actual change will occur
        if not btn.get_active():
            # 用户点击已选中的按钮，阻止它变成未选中
            # 使用 handler_block 来防止递归触发
            signal_id = getattr(self, "_grid_signal_id", None)
            if signal_id:
                btn.handler_block(signal_id)
                btn.set_active(True)
                btn.handler_unblock(signal_id)
            else:
                btn.set_active(True)
            # Early return without setting toggle timer
            return
        self._toggle_start_time = time.perf_counter()
        if not btn.get_active():
            # 用户点击已选中的按钮，阻止它变成未选中
            # 使用 handler_block 来防止递归触发
            signal_id = getattr(self, "_grid_signal_id", None)
            if signal_id:
                btn.handler_block(signal_id)
                btn.set_active(True)
                btn.handler_unblock(signal_id)
            else:
                btn.set_active(True)
            return
        # 正常切换到 Grid 视图
        # 阻止 list 按钮的信号，避免它的 toggled 处理器误认为是用户点击
        list_signal_id = getattr(self, "_list_signal_id", None)
        if list_signal_id:
            self.btn_list.handler_block(list_signal_id)
            self.btn_list.set_active(False)
            self.btn_list.handler_unblock(list_signal_id)
        else:
            self.btn_list.set_active(False)
        self.view_mode = "grid"
        self.refresh_wallpaper_grid()

    def on_view_list(self, btn):
        # Only set toggle start time if an actual change will occur
        if not btn.get_active():
            # 用户点击已选中的按钮，阻止它变成未选中
            # 使用 handler_block 来防止递归触发
            signal_id = getattr(self, "_list_signal_id", None)
            if signal_id:
                btn.handler_block(signal_id)
                btn.set_active(True)
                btn.handler_unblock(signal_id)
            else:
                btn.set_active(True)
            # Early return without setting toggle timer
            return
        self._toggle_start_time = time.perf_counter()
        # 正常切换到 List 视图
        # 阻止 grid 按钮的信号，避免它的 toggled 处理器误认为是用户点击
        grid_signal_id = getattr(self, "_grid_signal_id", None)
        if grid_signal_id:
            self.btn_grid.handler_block(grid_signal_id)
            self.btn_grid.set_active(False)
            self.btn_grid.handler_unblock(grid_signal_id)
        else:
            self.btn_grid.set_active(False)
        self.view_mode = "list"
        self.refresh_wallpaper_grid()

    def on_search_changed(self, entry):
        self.search_query = entry.get_text().lower().strip()
        self._invalidate_filter_cache()
        self.refresh_wallpaper_grid()
        self.update_sidebar_index()

    def on_search_activate(self, entry):
        self.search_query = entry.get_text().lower().strip()
        self._invalidate_filter_cache()
        self.refresh_wallpaper_grid()
        self.update_sidebar_index()

    def update_sidebar_index(self):
        filtered = self.get_filtered_wallpapers()
        if self.selected_wp and self.selected_wp in filtered:
            index = list(filtered.keys()).index(self.selected_wp) + 1
            total = len(filtered)
            self.sidebar.update(self.selected_wp, index, total)
        else:
            self.sidebar.update(self.selected_wp)

    def on_sort_changed(self, dd, pspec):
        idx = dd.get_selected()
        sort_map = {
            0: ("title", False),
            1: ("size", True),
            2: ("size", False),
            3: ("type", False),
            4: ("id", False),
        }
        self.sort_mode, self.sort_reverse = sort_map.get(idx, ("title", False))
        self.config.set("sortMode", self.sort_mode)
        self.config.set("sortReverse", self.sort_reverse)
        self._invalidate_filter_cache()
        self.refresh_wallpaper_grid()
        self.update_sidebar_index()

    def on_stop_clicked(self):
        # Stop wallpaper on current screen
        self.controller.stop_screen(self.selected_screen)
        self.update_active_wallpaper_label()

    def on_reload_wallpapers(self, btn):
        self.wp_manager.clear_cache()
        self.wp_manager.workshop_path = self.config.get(
            "workshopPath", self.wp_manager.workshop_path
        )
        self.wp_manager.scan()

        if self.wp_manager.last_scan_error:
            self.show_toast(f"⚠️ {self.wp_manager.last_scan_error}")
        elif self.wp_manager.scan_errors:
            self.show_toast(
                f"⚠️ {len(self.wp_manager.scan_errors)} wallpaper(s) failed to load"
            )

        self._invalidate_filter_cache()
        self.refresh_wallpaper_grid()

    def on_feeling_lucky(self, btn):
        if not self.wp_manager._wallpapers:
            return
        wp_id = random.choice(list(self.wp_manager._wallpapers.keys()))
        self.select_wallpaper(wp_id)
        self.apply_wallpaper(wp_id)

    def on_screenshot_clicked(self):
        active_monitors = self.config.get("active_monitors") or {}
        target_id = active_monitors.get(self.selected_screen)

        if not target_id:
            show_error_dialog(
                self.window,
                "Screenshot Error",
                f"No wallpaper is currently running on {self.selected_screen}.\n\nPlease apply a wallpaper to this screen first.",
            )
            return

        # UI Feedback: Busy state
        self.btn_screenshot.set_sensitive(False)
        self.screenshot_stack.set_visible_child_name("spinner")
        self.screenshot_spinner.start()
        self.btn_screenshot.set_tooltip_text("Capturing... please wait")

        def reset_ui():
            self.screenshot_spinner.stop()
            self.screenshot_stack.set_visible_child_name("icon")
            self.btn_screenshot.set_sensitive(True)
            self.btn_screenshot.set_tooltip_text("Take Screenshot of current wallpaper")

        base_dir = os.path.expanduser("~/Pictures/wallpaperengine")
        save_dir = base_dir
        fallback_used = False

        if not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir, exist_ok=True)
            except Exception as e:
                save_dir = "/tmp"
                fallback_used = True
                self.log_manager.add_error(
                    f"Failed to create {base_dir}: {e}. Falling back to /tmp", "GUI"
                )

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"Screenshot_{target_id}_{timestamp}.png"
        output_path = os.path.join(save_dir, filename)

        try:
            # Smart Delay Logic
            wp = self.wp_manager._wallpapers.get(target_id)
            wp_type = wp.get("type", "Unknown").lower() if wp else "unknown"

            user_delay = self.config.get("screenshotDelay", 20)
            user_delay = int(user_delay)

            if wp_type == "video":
                delay_frames = 5
                self.log_manager.add_info(
                    "Smart Delay: Video wallpaper detected, using fast capture (5 frames)",
                    "GUI",
                )
            else:
                delay_frames = user_delay
                # Web wallpapers might need more time, user setting is respected

            self.log_manager.add_info(f"Taking screenshot to {output_path}...", "GUI")
            proc, tracker = self.controller.take_screenshot(
                target_id, output_path, delay=delay_frames
            )

            start_time = time.time()

            # Calculate max wait time (timeout)
            # Xvfb software rendering is slow.
            import shutil

            has_xvfb_bin = shutil.which("xvfb-run") is not None
            prefer_xvfb = self.config.get("preferXvfb", True)
            is_xvfb = has_xvfb_bin and prefer_xvfb

            # Massive timeout for Xvfb software rendering at 4K
            fps_target = 1.0 if is_xvfb else 60.0
            buffer_s = 20.0 if is_xvfb else 3.0

            kill_threshold_s = (delay_frames / fps_target) + buffer_s
            self.log_manager.add_info(
                f"Screenshot timeout: {kill_threshold_s:.1f}s (Xvfb={is_xvfb})", "GUI"
            )

            last_size = -1
            stable_ticks = 0

            def check_capture_status():
                nonlocal last_size, stable_ticks
                elapsed = time.time() - start_time

                # Debug logging every 1s
                if int(elapsed * 10) % 10 == 0:
                    fsize = (
                        os.path.getsize(output_path)
                        if os.path.exists(output_path)
                        else -1
                    )
                    self.log_manager.add_debug(
                        f"Capture status: T={elapsed:.1f}s, File={fsize} bytes", "GUI"
                    )

                # 1. Check if process is already dead (crashed or finished)
                if proc.poll() is not None:
                    # Process exited on its own. Check file.
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        show_success()
                    else:
                        # Read error log
                        err_msg = "Unknown error"
                        try:
                            with open("/tmp/wallpaper_screenshot_error.log", "r") as f:
                                err_msg = f.read().strip()
                        except:
                            pass

                        self.log_manager.add_error(
                            f"Screenshot process crashed: {err_msg}", "GUI"
                        )
                        reset_ui()
                        show_error_dialog(
                            self.window,
                            "Screenshot Failed",
                            f"The engine crashed or exited early.\n\nBackend Error:\n{err_msg[-500:]}",
                        )
                    return False

                # 2. Check if file exists and is stable
                if os.path.exists(output_path):
                    try:
                        curr_size = os.path.getsize(output_path)
                        if curr_size > 0:
                            if curr_size == last_size:
                                stable_ticks += 1
                            else:
                                stable_ticks = 0
                            last_size = curr_size

                            # Stable for ~200ms -> Kill it
                            if stable_ticks >= 2:
                                kill_process()
                                # Wait a tiny bit for cleanup then show success
                                GLib.timeout_add(200, show_success)
                                return False
                    except OSError:
                        pass  # File might be locked or busy

                # 3. Timeout -> Force Kill (Trigger save-on-exit)
                if elapsed > kill_threshold_s:
                    kill_process()
                    # Give it 1s to flush on exit
                    GLib.timeout_add(1000, verify_after_kill)
                    return False

                return True  # Continue polling

            def kill_process():
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGINT)
                except:
                    proc.terminate()

            def show_success():
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    self.log_manager.add_info(
                        f"Screenshot complete: {output_path}", "GUI"
                    )

                    stats = self.controller.perf_monitor.stop_task(tracker)
                    self.controller.perf_monitor.add_screenshot_history(
                        target_id, output_path, stats
                    )
                    stats_str = f"Duration: {stats['duration']:.2f}s | Max CPU: {stats['max_cpu']:.1f}% | Max Mem: {stats['max_mem']:.1f} MB"

                    texture = None
                    wp = self.wp_manager._wallpapers.get(target_id)
                    if wp and wp.get("preview"):
                        texture = self.wp_manager.get_texture(wp["preview"], size=120)

                    reset_ui()
                    show_screenshot_success_dialog(
                        self.window, output_path, stats_str, texture
                    )
                else:
                    # Rare race condition or save failed
                    verify_after_kill()
                return False

            def verify_after_kill():
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    show_success()
                else:
                    reset_ui()
                    show_error_dialog(
                        self.window,
                        "Screenshot Timeout",
                        "Capture timed out. Try increasing the delay in Settings.",
                    )
                return False

            # Start polling every 100ms
            GLib.timeout_add(100, check_capture_status)

        except Exception as e:
            reset_ui()
            show_error_dialog(
                self.window, "Screenshot Error", f"Failed to start process: {e}"
            )

    def refresh_wallpaper_grid(self):
        cache_key = (self.search_query, self.sort_mode, self.sort_reverse)

        # Save previous IDs to detect changes
        prev_ids = getattr(self, "_current_wp_ids", None)

        # Track whether filter was recomputed
        recomputed = (cache_key != self._filter_cache_key) or (
            self._filtered_wallpapers is None
        )
        if recomputed:
            self._filtered_wallpapers = self.filter_wallpapers()
            self._filter_cache_key = cache_key
            self._current_wp_ids = list(self._filtered_wallpapers.keys())
            # Debug log for verification - only when debug mode enabled
            try:
                if self.config.get("debug", False):
                    self.log_manager.add_debug(
                        f"Filter recomputed: {len(self._filtered_wallpapers)} matches, "
                        f"prev_ids length: {len(prev_ids or [])}",
                        "GUI",
                    )
            except Exception:
                # Defensive: config may not be available in rare test contexts
                pass

        self.sidebar.set_wallpaper_ids(self._current_wp_ids)

        # Detect if ID list changed (determines whether UI rebuild is needed)
        ids_changed = prev_ids != self._current_wp_ids

        if self.view_mode == "grid":
            self.view_stack.set_visible_child_name("grid")
            # Populate if: (1) filter was recomputed AND IDs changed, OR (2) container is empty
            if recomputed or ids_changed or self.flowbox.get_first_child() is None:
                self.populate_grid()
        else:
            self.view_stack.set_visible_child_name("list")
            # Populate if: (1) filter was recomputed AND IDs changed, OR (2) container is empty
            if recomputed or ids_changed or self.listbox.get_first_child() is None:
                self.populate_list()

        self.update_counter_label()

        if hasattr(self, "_toggle_start_time") and self._toggle_start_time:
            elapsed = (time.perf_counter() - self._toggle_start_time) * 1000
            try:
                if self.config.get("debug", False):
                    self.log_manager.add_info(f"View toggle time: {elapsed:.1f} ms")
            except Exception:
                pass
            self._toggle_start_time = None

    def _invalidate_filter_cache(self):
        self._filtered_wallpapers = None
        self._filter_cache_key = None

    def get_filtered_wallpapers(self) -> Dict[str, Dict]:
        cache_key = (self.search_query, self.sort_mode, self.sort_reverse)
        if self._filter_cache_key != cache_key or self._filtered_wallpapers is None:
            self._filtered_wallpapers = self.filter_wallpapers()
            self._filter_cache_key = cache_key
            self._current_wp_ids = list(self._filtered_wallpapers.keys())
        return self._filtered_wallpapers

    def filter_wallpapers(self) -> Dict[str, Dict]:
        # Avoid spamming logs in hot path; only log when debug enabled
        try:
            if self.config.get("debug", False):
                self.log_manager.add_debug("filter_wallpapers called", "GUI")
        except Exception:
            pass
        if not self.search_query:
            result = dict(self.wp_manager._wallpapers)
        else:
            result = {}
            for wp_id, wp in self.wp_manager._wallpapers.items():
                title = wp.get("title", "").lower()
                desc = wp.get("description", "").lower()
                tags = " ".join(str(t).lower() for t in wp.get("tags", []))
                nickname = (
                    (self.nickname_manager.get(wp_id) or "").lower()
                    if self.nickname_manager
                    else ""
                )
                if (
                    self.search_query in title
                    or self.search_query in desc
                    or self.search_query in tags
                    or self.search_query in wp_id.lower()
                    or self.search_query in nickname
                ):
                    result[wp_id] = wp

        if self.sort_mode == "title":
            sorted_items = sorted(
                result.items(),
                key=lambda x: x[1].get("title", "").lower(),
                reverse=self.sort_reverse,
            )
        elif self.sort_mode == "size":
            sorted_items = sorted(
                result.items(),
                key=lambda x: x[1].get("size", 0),
                reverse=self.sort_reverse,
            )
        elif self.sort_mode == "type":
            sorted_items = sorted(
                result.items(),
                key=lambda x: x[1].get("type", "").lower(),
                reverse=self.sort_reverse,
            )
        else:
            sorted_items = sorted(
                result.items(), key=lambda x: x[0], reverse=self.sort_reverse
            )

        return dict(sorted_items)

    def populate_grid(self):
        while True:
            child = self.flowbox.get_first_child()
            if child is None:
                break
            self.flowbox.remove(child)

        # Clean up old widget references to prevent memory leaks
        for wp in self.wp_manager._wallpapers.values():
            if "_grid_btn" in wp:
                del wp["_grid_btn"]

        filtered = self._filtered_wallpapers or {}
        for folder_id, wp in filtered.items():
            card = self.create_grid_item(folder_id, wp)
            self.flowbox.append(card)

    def populate_list(self):
        while True:
            child = self.listbox.get_first_child()
            if child is None:
                break
            self.listbox.remove(child)

        # Clean up old widget references to prevent memory leaks
        for wp in self.wp_manager._wallpapers.values():
            if "_list_btn" in wp:
                del wp["_list_btn"]

        filtered = self._filtered_wallpapers or {}
        total = len(filtered)
        for idx, (folder_id, wp) in enumerate(filtered.items()):
            row = self.create_list_item(folder_id, wp, idx + 1, total)
            self.listbox.append(row)

    def create_grid_item(self, folder_id: str, wp: Dict) -> Gtk.Widget:
        display_name, original_title = self.nickname_manager.get_display_name(wp)
        is_nickname = original_title is not None

        btn = Gtk.Button()
        btn.add_css_class("wallpaper-item")
        btn.add_css_class("wallpaper-card")
        btn.set_size_request(170, 170)
        btn.set_has_frame(False)

        tooltip_text = markdown_to_pango(display_name)
        if is_nickname:
            tooltip_text += f"\n<span size='small' alpha='70%'>Original: {markdown_to_pango(wp.get('title', ''))}</span>"
        btn.set_tooltip_markup(tooltip_text)

        btn.connect("clicked", lambda _: self.select_wallpaper(folder_id))

        gesture = Gtk.GestureClick.new()
        gesture.set_button(Gdk.BUTTON_PRIMARY)
        gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        gesture.connect(
            "pressed", lambda g, n, x, y: self.on_item_activated(folder_id, n)
        )
        btn.add_controller(gesture)

        context = Gtk.GestureClick.new()
        context.set_button(Gdk.BUTTON_SECONDARY)
        context.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        context.connect(
            "pressed", lambda g, n, x, y: self.on_context_menu(btn, folder_id, x, y)
        )
        btn.add_controller(context)

        overlay = Gtk.Overlay()
        btn.set_child(overlay)

        texture = self.wp_manager.get_texture(wp["preview"], 170)
        if texture:
            pic = Gtk.Picture.new_for_paintable(texture)
            pic.set_content_fit(Gtk.ContentFit.COVER)
            pic.set_size_request(170, 170)
            overlay.set_child(pic)
        else:
            placeholder = Gtk.Box()
            placeholder.set_size_request(170, 170)
            lbl = Gtk.Label(label=wp["title"][:1].upper())
            lbl.set_halign(Gtk.Align.CENTER)
            lbl.set_valign(Gtk.Align.CENTER)
            placeholder.append(lbl)
            overlay.set_child(placeholder)

        name_box = Gtk.Box()
        name_box.set_halign(Gtk.Align.CENTER)
        name_box.set_valign(Gtk.Align.END)
        name_box.set_margin_bottom(10)

        lbl = Gtk.Label()
        lbl.set_use_markup(True)
        lbl.set_markup(markdown_to_pango(display_name))
        lbl.add_css_class("wallpaper-name")
        if is_nickname:
            lbl.add_css_class("nickname-text")
        lbl.set_ellipsize(Pango.EllipsizeMode.END)
        lbl.set_max_width_chars(15)
        name_box.append(lbl)
        overlay.add_overlay(name_box)

        wp["_grid_btn"] = btn
        if folder_id == self.selected_wp:
            btn.add_css_class("selected")

        return btn

    def create_list_item(
        self, folder_id: str, wp: Dict, index: int, total: int
    ) -> Gtk.Widget:
        display_name, original_title = self.nickname_manager.get_display_name(wp)
        is_nickname = original_title is not None

        btn = Gtk.Button()
        btn.add_css_class("list-item")
        btn.set_has_frame(False)

        tooltip_text = markdown_to_pango(display_name)
        if is_nickname:
            tooltip_text += f"\n<span size='small' alpha='70%'>Original: {markdown_to_pango(wp.get('title', ''))}</span>"
        btn.set_tooltip_markup(tooltip_text)

        btn.connect("clicked", lambda _: self.select_wallpaper(folder_id))

        gesture = Gtk.GestureClick.new()
        gesture.set_button(Gdk.BUTTON_PRIMARY)
        gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        gesture.connect(
            "pressed", lambda g, n, x, y: self.on_item_activated(folder_id, n)
        )
        btn.add_controller(gesture)

        context = Gtk.GestureClick.new()
        context.set_button(Gdk.BUTTON_SECONDARY)
        context.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        context.connect(
            "pressed", lambda g, n, x, y: self.on_context_menu(btn, folder_id, x, y)
        )
        btn.add_controller(context)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        btn.set_child(hbox)

        texture = self.wp_manager.get_texture(wp["preview"], 100)
        if texture:
            pic = Gtk.Picture.new_for_paintable(texture)
            pic.set_content_fit(Gtk.ContentFit.COVER)
            pic.set_size_request(100, 100)
            pic.add_css_class("card")
            hbox.append(pic)

        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info.set_valign(Gtk.Align.CENTER)
        info.set_hexpand(True)
        hbox.append(info)

        t = Gtk.Label()
        t.set_use_markup(True)
        t.set_markup(markdown_to_pango(display_name))
        t.add_css_class("list-title")
        if is_nickname:
            t.add_css_class("nickname-text")
        t.set_halign(Gtk.Align.START)
        t.set_ellipsize(Pango.EllipsizeMode.END)
        info.append(t)

        if is_nickname:
            orig_lbl = Gtk.Label()
            orig_lbl.set_use_markup(True)
            orig_lbl.set_markup(
                f"<span size='small' alpha='60%'>{markdown_to_pango(wp.get('title', ''))}</span>"
            )
            orig_lbl.set_halign(Gtk.Align.START)
            orig_lbl.set_ellipsize(Pango.EllipsizeMode.END)
            info.append(orig_lbl)

        sz = format_size(wp.get("size", 0))
        size_lbl = Gtk.Label(label=sz)
        size_lbl.add_css_class("list-size")
        size_lbl.set_halign(Gtk.Align.START)
        info.append(size_lbl)

        typ = Gtk.Label(label=f"Type: {wp.get('type', 'Unknown')}")
        typ.add_css_class("list-type")
        typ.set_halign(Gtk.Align.START)
        info.append(typ)

        tags = wp.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        tgs = ", ".join(str(x) for x in tags[:5]) if tags else "None"
        tl = Gtk.Label(label=f"Tags: {tgs}")
        tl.add_css_class("list-tags")
        tl.set_halign(Gtk.Align.START)
        tl.set_ellipsize(Pango.EllipsizeMode.END)
        info.append(tl)

        idx_lbl = Gtk.Label(label=f"{index}/{total}")
        idx_lbl.add_css_class("list-index")
        idx_lbl.set_halign(Gtk.Align.START)
        info.append(idx_lbl)

        wp["_list_btn"] = btn
        if folder_id == self.selected_wp:
            btn.add_css_class("selected")

        return btn

    def select_wallpaper(self, folder_id: str):
        # Deselect old
        if self.selected_wp and self.selected_wp in self.wp_manager._wallpapers:
            old = self.wp_manager._wallpapers[self.selected_wp]
            if "_grid_btn" in old:
                old["_grid_btn"].remove_css_class("selected")
            if "_list_btn" in old:
                old["_list_btn"].remove_css_class("selected")

        self.selected_wp = folder_id
        wp = self.wp_manager._wallpapers.get(folder_id)
        if wp:
            if "_grid_btn" in wp:
                wp["_grid_btn"].add_css_class("selected")
            if "_list_btn" in wp:
                wp["_list_btn"].add_css_class("selected")

        filtered = getattr(self, "_filtered_wallpapers", None)
        if filtered is None:
            filtered = self.get_filtered_wallpapers()
        if folder_id in filtered:
            index = list(filtered.keys()).index(folder_id) + 1
            total = len(filtered)
            self.sidebar.update(folder_id, index, total)
        else:
            self.sidebar.update(folder_id)

        if self.sidebar._compact_mode:
            self.sidebar._update_thumb_grid()

    def apply_wallpaper(self, wp_id: str):
        self.controller.apply(wp_id, self.selected_screen)
        self.update_active_wallpaper_label()

    def on_item_activated(self, folder_id: str, n_press: int):
        if n_press == 2:
            self.select_wallpaper(folder_id)
            self.apply_wallpaper(folder_id)

    def on_context_menu(self, widget, folder_id, x, y):
        # Create a custom Popover with manual buttons to allow full styling control (e.g. Red delete button)
        popover = Gtk.Popover()
        popover.set_parent(widget)
        popover.set_has_arrow(False)

        # Position at click coordinates
        rect = Gdk.Rectangle()
        rect.x = int(x)
        rect.y = int(y)
        rect.width = 1
        rect.height = 1
        popover.set_pointing_to(rect)

        # Menu Container
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        box.set_margin_top(6)
        box.set_margin_bottom(6)
        box.set_margin_start(6)
        box.set_margin_end(6)
        popover.set_child(box)

        def create_menu_item(label, action_name, target_value=None, is_danger=False):
            btn = Gtk.Button()
            btn.set_has_frame(False)  # Flat button

            # Left aligned label
            lbl = Gtk.Label(label=label)
            lbl.set_halign(Gtk.Align.START)
            btn.set_child(lbl)

            # Action
            btn.set_action_name(action_name)
            if target_value:
                btn.set_action_target_value(GLib.Variant.new_string(target_value))

            # Styling
            # Ensure it spans full width
            btn.set_halign(Gtk.Align.FILL)

            if is_danger:
                btn.add_css_class("destructive-action")  # Makes it red in Libadwaita

            # Close popover when clicked
            btn.connect("clicked", lambda *_: popover.popdown())

            return btn

        # Menu Items
        box.append(create_menu_item("Apply Wallpaper", "win.apply", folder_id))
        box.append(create_menu_item("Stop Wallpaper", "win.stop"))
        box.append(create_menu_item("Open Folder", "win.open_folder", folder_id))

        # Separator
        box.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        btn_edit = Gtk.Button()
        btn_edit.set_has_frame(False)
        lbl_edit = Gtk.Label(label="Set Nickname")
        lbl_edit.set_halign(Gtk.Align.START)
        btn_edit.set_child(lbl_edit)
        btn_edit.set_halign(Gtk.Align.FILL)
        btn_edit.connect(
            "clicked", lambda _: (self.on_edit_nickname(folder_id), popover.popdown())
        )
        box.append(btn_edit)

        # Danger Item
        box.append(
            create_menu_item(
                "Delete Wallpaper", "win.delete", folder_id, is_danger=True
            )
        )

        popover.popup()

    def delete_wallpaper(self, wp_id: str):
        show_delete_dialog(self.window, wp_id, lambda: self._perform_delete(wp_id))

    def _perform_delete(self, wp_id: str):
        if self.wp_manager.delete_wallpaper(wp_id):
            if self.active_wp == wp_id:
                self.on_stop_clicked()
            self._invalidate_filter_cache()
            self.refresh_wallpaper_grid()
        else:
            show_error_dialog(self.window, "Error", "Failed to delete wallpaper")

    def open_wallpaper_folder(self, wp_id: str):
        import subprocess
        import shutil

        wp = self.wp_manager._wallpapers.get(wp_id)
        if wp:
            folder_path = os.path.dirname(wp["preview"])

            # List of file managers to try in order of preference
            file_managers = [
                "thunar",  # XFCE (Preferred)
                "nautilus",  # GNOME
                "dolphin",  # KDE
                "nemo",  # Cinnamon
                "pcmanfm",  # LXDE
                "pcmanfm-qt",  # LXQt
                "caja",  # MATE
                "index",  # Maui
                "files",  # Elementary
            ]

            # Try to find an installed file manager
            opened = False
            for fm in file_managers:
                if shutil.which(fm):
                    try:
                        subprocess.Popen([fm, folder_path])
                        opened = True
                        break
                    except:
                        continue

            # Fallback to xdg-open if no specific FM found or failed
            if not opened:
                try:
                    subprocess.Popen(["xdg-open", folder_path])
                except Exception as e:
                    self.log_manager.add_error(f"Failed to open folder: {e}", "GUI")

    def on_edit_nickname(self, wp_id: str):
        wp = self.wp_manager._wallpapers.get(wp_id)
        if not wp:
            return

        title = wp.get("title", "")
        current_nickname = (
            self.nickname_manager.get(wp_id) if self.nickname_manager else None
        )
        preview_path = wp.get("preview")

        def on_confirm(new_nick: str):
            if self.nickname_manager:
                self.nickname_manager.set(wp_id, new_nick)
                self._invalidate_filter_cache()
                self.refresh_wallpaper_grid()
                self.update_sidebar_index()
                self.update_active_wallpaper_label()

        show_nickname_dialog(self.window, title, current_nickname, on_confirm)

    def set_compact_mode(self, enabled: bool):
        self.left_area.set_visible(not enabled)
        self.toolbar.set_visible(not enabled)
        self.content_box.set_hexpand(not enabled)
        self.sidebar.set_compact_mode(enabled)
        if enabled:
            self.sidebar.grab_focus()

    def _setup_key_controller(self):
        key_ctrl = Gtk.EventControllerKey.new()
        key_ctrl.connect("key-pressed", self._on_key_pressed)
        self.add_controller(key_ctrl)

    def _on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Left:
            self._navigate_wallpaper(-1)
            return True
        elif keyval == Gdk.KEY_Right:
            self._navigate_wallpaper(1)
            return True
        return False

    def _navigate_wallpaper(self, direction: int):
        if not self._current_wp_ids or not self.selected_wp:
            return
        try:
            current_idx = self._current_wp_ids.index(self.selected_wp)
            new_idx = current_idx + direction
            if 0 <= new_idx < len(self._current_wp_ids):
                new_wp_id = self._current_wp_ids[new_idx]
                self.select_wallpaper(new_wp_id)
        except ValueError:
            pass
