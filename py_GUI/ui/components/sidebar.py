import threading
import webbrowser
from typing import Dict, List, Optional, Callable
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, GLib, Adw, GdkPixbuf, Pango

from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.logger import LogManager
from py_GUI.utils import markdown_to_pango, bbcode_to_pango, format_size
from py_GUI.ui.components.animated_preview import AnimatedPreview

class Sidebar(Gtk.Box):
    def __init__(self, wp_manager: WallpaperManager, prop_manager: PropertiesManager, 
                 controller: WallpaperController, log_manager: LogManager, nickname_manager=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.wp_manager = wp_manager
        self.prop_manager = prop_manager
        self.controller = controller
        self.log_manager = log_manager
        self.nickname_manager = nickname_manager
        
        self.selected_wp: Optional[str] = None
        
        self.available_screens: List[str] = []
        self.get_current_screen: Callable[[], str] = lambda: "eDP-1"
        self.get_apply_mode: Callable[[], str] = lambda: "diff"
        
        self.add_css_class("sidebar")
        self.set_size_request(370, -1)
        self.set_hexpand(False)
        self.set_halign(Gtk.Align.END)
        
        self._compact_mode = False
        
        self.build_ui()

    def set_available_screens(self, screens: List[str]):
        self.available_screens = screens
        self.update_apply_button_state()

    def set_current_screen_callback(self, cb: Callable[[], str]):
        self.get_current_screen = cb

    def set_apply_mode_callback(self, cb: Callable[[], str]):
        self.get_apply_mode = cb

    def update_apply_button_mode(self, mode: str):
        self.update_apply_button_state()

    def update_apply_button_state(self):
        while True:
            child = self.apply_btn_container.get_first_child()
            if child is None: break
            self.apply_btn_container.remove(child)
            
        mode = self.get_apply_mode()
        screen_count = len(self.available_screens)
        
        use_split = (screen_count >= 3) and (mode == "diff")
        
        if use_split:
            self.btn_apply = Adw.SplitButton(label="Apply Wallpaper")
            self.btn_apply.add_css_class("sidebar-btn")
            self.btn_apply.add_css_class("suggested-action")
            self.btn_apply.set_hexpand(True)
            self.btn_apply.connect("clicked", self.on_apply_clicked)
            
            menu_popover = Gtk.Popover()
            menu_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            menu_content.set_margin_top(12)
            menu_content.set_margin_bottom(12)
            menu_content.set_margin_start(12)
            menu_content.set_margin_end(12)
            menu_popover.set_child(menu_content)
            
            self.btn_apply.set_popover(menu_popover)
            menu_popover.connect("map", self.on_popover_map)
            self.popover_box = menu_content
            
            self.apply_btn_container.append(self.btn_apply)
        else:
            self.btn_apply = Gtk.Button(label="Apply Wallpaper")
            self.btn_apply.add_css_class("sidebar-btn")
            self.btn_apply.set_hexpand(True)
            self.btn_apply.connect("clicked", self.on_apply_clicked)
            self.apply_btn_container.append(self.btn_apply)

    def build_ui(self):
        # Scrollable area
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_hexpand(False)
        self.append(scroll)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content.set_hexpand(False)
        content.set_size_request(370, -1)
        scroll.set_child(content)

        # Preview Image
        preview_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_container.set_size_request(280, 280)
        preview_container.set_hexpand(False)
        preview_container.set_halign(Gtk.Align.CENTER)
        preview_container.add_css_class("sidebar-preview")

        preview_scroll = Gtk.ScrolledWindow()
        preview_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        preview_scroll.set_size_request(280, 280)
        preview_container.append(preview_scroll)

        self.preview_image = AnimatedPreview(size_request=(280, 280))
        self.preview_image.set_hexpand(False)
        preview_scroll.set_child(self.preview_image)
        content.append(preview_container)

        # Title Section
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        title_box.set_margin_start(20)
        title_box.set_margin_end(20)
        content.append(title_box)

        self.lbl_title = Gtk.Label(label="Select a Wallpaper")
        self.lbl_title.add_css_class("sidebar-title")
        self.lbl_title.set_use_markup(True)
        self.lbl_title.set_halign(Gtk.Align.START)
        self.lbl_title.set_wrap(True)
        self.lbl_title.set_max_width_chars(25)
        self.lbl_title.set_xalign(0)
        title_box.append(self.lbl_title)

        self.lbl_original_name = Gtk.Label(label="")
        self.lbl_original_name.add_css_class("original-name-text")
        self.lbl_original_name.set_halign(Gtk.Align.START)
        self.lbl_original_name.set_wrap(True)
        self.lbl_original_name.set_max_width_chars(30)
        self.lbl_original_name.set_xalign(0)
        self.lbl_original_name.set_visible(False)
        title_box.append(self.lbl_original_name)

        # Info Row (Chips + Edit Button)
        folder_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        folder_row.set_halign(Gtk.Align.FILL)
        folder_row.set_margin_start(20)
        folder_row.set_margin_end(20)
        content.append(folder_row)

        self.lbl_folder = Gtk.Label(label="")
        self.lbl_folder.add_css_class("folder-chip")
        self.lbl_folder.set_tooltip_text("Click to copy ID")
        self.lbl_folder.set_cursor_from_name("pointer")
        self.lbl_folder.set_ellipsize(Pango.EllipsizeMode.END)
        self.lbl_folder.set_max_width_chars(12)
        folder_row.append(self.lbl_folder)

        self.lbl_size = Gtk.Label(label="")
        self.lbl_size.add_css_class("size-chip")
        folder_row.append(self.lbl_size)

        self.lbl_index = Gtk.Label(label="")
        self.lbl_index.add_css_class("index-chip")
        folder_row.append(self.lbl_index)

        # Spacer to push button to far right
        row_spacer = Gtk.Box()
        row_spacer.set_hexpand(True)
        folder_row.append(row_spacer)

        self.btn_edit_nickname = Gtk.Button()
        self.btn_edit_nickname.set_icon_name("document-edit-symbolic")
        self.btn_edit_nickname.add_css_class("flat")
        self.btn_edit_nickname.add_css_class("circular")
        self.btn_edit_nickname.set_tooltip_text("Edit Nickname")
        self.btn_edit_nickname.set_valign(Gtk.Align.CENTER)
        self.btn_edit_nickname.set_visible(False)
        folder_row.append(self.btn_edit_nickname)

        # Folder click to copy
        folder_click = Gtk.GestureClick.new()
        folder_click.connect("released", self.on_folder_clicked)
        self.lbl_folder.add_controller(folder_click)

        # Type
        self.type_header = Gtk.Label(label="Type")
        self.type_header.add_css_class("sidebar-section")
        self.type_header.set_halign(Gtk.Align.START)
        self.type_header.set_margin_start(20)
        self.type_header.set_margin_end(20)
        content.append(self.type_header)

        self.type_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.type_container.set_margin_start(20)
        self.type_container.set_margin_end(20)
        content.append(self.type_container)

        self.lbl_type = Gtk.Label(label="-")
        self.lbl_type.add_css_class("tag-chip")
        self.lbl_type.set_halign(Gtk.Align.START)
        self.type_container.append(self.lbl_type)

        # Tags
        self.tags_header = Gtk.Label(label="Tags")
        self.tags_header.add_css_class("sidebar-section")
        self.tags_header.set_halign(Gtk.Align.START)
        self.tags_header.set_margin_start(20)
        self.tags_header.set_margin_end(20)
        content.append(self.tags_header)

        self.tags_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.tags_container.set_hexpand(False)
        self.tags_container.set_margin_start(20)
        self.tags_container.set_margin_end(20)
        content.append(self.tags_container)

        self.tags_flow = Gtk.FlowBox()
        self.tags_flow.set_selection_mode(Gtk.SelectionMode.NONE)
        self.tags_flow.set_max_children_per_line(4)
        self.tags_flow.set_hexpand(False)
        self.tags_flow.set_column_spacing(4)
        self.tags_flow.set_row_spacing(4)
        self.tags_container.append(self.tags_flow)

        # Description
        self.desc_header = Gtk.Label(label="Description")
        self.desc_header.add_css_class("sidebar-section")
        self.desc_header.set_halign(Gtk.Align.START)
        self.desc_header.set_margin_start(20)
        self.desc_header.set_margin_end(20)
        content.append(self.desc_header)

        self.lbl_desc = Gtk.Label(label="No description.")
        self.lbl_desc.add_css_class("sidebar-desc")
        self.lbl_desc.set_halign(Gtk.Align.START)
        self.lbl_desc.set_xalign(0)
        self.lbl_desc.set_wrap(True)
        self.lbl_desc.set_use_markup(True)
        self.lbl_desc.set_max_width_chars(30)
        self.lbl_desc.set_selectable(True)
        self.lbl_desc.set_margin_start(20)
        self.lbl_desc.set_margin_end(20)
        content.append(self.lbl_desc)

        # Bottom Buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        btn_box.set_margin_top(20)
        btn_box.set_margin_bottom(20)
        self.append(btn_box)

        # Apply Button Container
        self.apply_btn_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.apply_btn_container.set_halign(Gtk.Align.FILL)
        btn_box.append(self.apply_btn_container)
        
        # Initial button setup
        self.update_apply_button_state()

        self.btn_workshop = Gtk.Button(label="Open in Workshop")
        self.btn_workshop.add_css_class("sidebar-btn")
        self.btn_workshop.add_css_class("secondary")
        self.btn_workshop.connect("clicked", self.on_workshop_clicked)
        btn_box.append(self.btn_workshop)

        self.thumb_grid = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.thumb_grid.set_halign(Gtk.Align.CENTER)
        self.thumb_grid.set_margin_top(10)
        self.thumb_grid.set_margin_bottom(10)
        self.thumb_grid.set_visible(False)
        self.append(self.thumb_grid)
        
        self.compact_actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.compact_actions.set_halign(Gtk.Align.CENTER)
        self.compact_actions.set_margin_bottom(10)
        self.compact_actions.set_visible(False)
        self.append(self.compact_actions)
        
        self.btn_compact_stop = Gtk.Button()
        self.btn_compact_stop.set_icon_name("media-playback-stop-symbolic")
        self.btn_compact_stop.add_css_class("circular")
        self.btn_compact_stop.set_tooltip_text("Stop Wallpaper")
        self.compact_actions.append(self.btn_compact_stop)
        
        self.btn_compact_lucky = Gtk.Button()
        self.btn_compact_lucky.set_icon_name("media-playlist-shuffle-symbolic")
        self.btn_compact_lucky.add_css_class("circular")
        self.btn_compact_lucky.set_tooltip_text("I'm feeling lucky")
        self.compact_actions.append(self.btn_compact_lucky)
        
        self.btn_compact_jump = Gtk.Button()
        self.btn_compact_jump.set_icon_name("go-home-symbolic")
        self.btn_compact_jump.add_css_class("circular")
        self.btn_compact_jump.set_tooltip_text("Jump to current wallpaper")
        self.compact_actions.append(self.btn_compact_jump)
        
        self._thumb_cache = {}
        self._wallpaper_ids = []
        self._on_thumb_clicked_cb = None
        self._on_stop_cb = None
        self._on_lucky_cb = None
        self._on_jump_cb = None
        
        self.btn_compact_stop.connect("clicked", lambda b: self._on_stop_cb() if callable(self._on_stop_cb) else None)
        self.btn_compact_lucky.connect("clicked", lambda b: self._on_lucky_cb() if callable(self._on_lucky_cb) else None)
        self.btn_compact_jump.connect("clicked", lambda b: self._on_jump_cb() if callable(self._on_jump_cb) else None)

    def on_popover_map(self, popover):
        while True:
            child = self.popover_box.get_first_child()
            if child is None: break
            self.popover_box.remove(child)
            
        lbl = Gtk.Label(label="Apply to specific screens:")
        lbl.add_css_class("heading")
        lbl.set_halign(Gtk.Align.START)
        self.popover_box.append(lbl)
        
        self.screen_checks = {}
        current = self.get_current_screen()
        
        for screen in self.available_screens:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            chk = Gtk.CheckButton()
            chk.set_active(screen == current)
            self.screen_checks[screen] = chk
            row.append(chk)
            
            lbl_scr = Gtk.Label(label=screen)
            if screen == current:
                lbl_scr.set_markup(f"<b>{screen}</b> (Current)")
            else:
                lbl_scr.set_label(screen)
            row.append(lbl_scr)
            self.popover_box.append(row)
            
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.set_margin_top(6)
        sep.set_margin_bottom(6)
        self.popover_box.append(sep)
        
        btn_confirm = Gtk.Button(label="Apply to Selected")
        btn_confirm.add_css_class("suggested-action")
        btn_confirm.connect("clicked", lambda b: self.on_advanced_apply(popover))
        self.popover_box.append(btn_confirm)

    def on_advanced_apply(self, popover):
        if not self.selected_wp: return
        
        selected_screens = []
        for screen, chk in self.screen_checks.items():
            if chk.get_active():
                selected_screens.append(screen)
                
        if selected_screens:
            self.controller.apply(self.selected_wp, screens=selected_screens)
            popover.popdown()
        else:
            pass

    def update(self, wp_id: Optional[str], index: int = 0, total: int = 0):
        self.selected_wp = wp_id
        if not wp_id:
            self.clear()
            return

        wp = self.wp_manager._wallpapers.get(wp_id)
        if not wp:
            self.clear()
            return

        self.preview_image.set_image_from_path(wp['preview'], self.wp_manager)

        # Nickname Logic
        original_title = wp.get('title', 'Unknown')
        display_title = original_title
        has_nickname = False
        
        if self.nickname_manager:
            display_title, returned_original = self.nickname_manager.get_display_name(wp)
            if returned_original is not None:
                original_title = returned_original
            if display_title != original_title:
                has_nickname = True
        
        self.lbl_title.set_markup(markdown_to_pango(display_title))
        
        if has_nickname:
            self.lbl_title.add_css_class("nickname-text")
            self.lbl_original_name.set_label(original_title)
            self.lbl_original_name.set_visible(True)
        else:
            self.lbl_title.remove_css_class("nickname-text")
            self.lbl_original_name.set_visible(False)
            
        self.btn_edit_nickname.set_visible(True)

        self.lbl_folder.set_label(f"{wp['id']}")
        self.lbl_size.set_label(format_size(wp.get('size', 0)))
        
        self.lbl_index.set_label(f"{index}/{total}")
        
        self.lbl_type.set_label(wp.get('type', 'Unknown'))
        
        desc = wp.get('description', '')
        self.lbl_desc.set_markup(bbcode_to_pango(desc) or 'No description.')

        while True:
            child = self.tags_flow.get_first_child()
            if child is None: break
            self.tags_flow.remove(child)

        tags = wp.get('tags', [])
        if isinstance(tags, str): tags = [tags]

        if not tags:
            lbl = Gtk.Label(label="None")
            lbl.add_css_class("text-muted")
            self.tags_flow.append(lbl)
        else:
            for tag in tags[:8]:
                chip = Gtk.Label(label=str(tag))
                chip.add_css_class("tag-chip")
                self.tags_flow.append(chip)

    def clear(self):
        self.selected_wp = None
        self.preview_image.set_image_from_path(None, None)
        self.lbl_title.set_label("Select a Wallpaper")
        self.lbl_title.remove_css_class("nickname-text")
        self.lbl_original_name.set_visible(False)
        self.btn_edit_nickname.set_visible(False)
        self.lbl_folder.set_label("")
        self.lbl_size.set_label("")
        self.lbl_index.set_label("")
        self.lbl_type.set_label("-")
        self.lbl_desc.set_label("No description.")
        
        while True:
            child = self.tags_flow.get_first_child()
            if child is None: break
            self.tags_flow.remove(child)

    def on_apply_clicked(self, btn):
        if self.selected_wp:
            mode = self.get_apply_mode()
            
            if mode == "same" and self.available_screens:
                self.controller.apply(self.selected_wp, screens=self.available_screens)
                self.log_manager.add_info(f"Applied wallpaper {self.selected_wp} to ALL screens: {self.available_screens}", "Sidebar")
            else:
                current_screen = self.get_current_screen()
                self.controller.apply(self.selected_wp, screen=current_screen)

    def on_workshop_clicked(self, btn):
        if self.selected_wp:
            url = f"steam://url/CommunityFilePage/{self.selected_wp}"
            webbrowser.open(url)

    def on_folder_clicked(self, gesture, n_press, x, y):
        if self.selected_wp:
            clipboard = Gdk.Display.get_default().get_clipboard()
            clipboard.set(self.selected_wp)
            self.log_manager.add_info(f"Copied ID to clipboard: {self.selected_wp}", "GUI")
            
            # Temporary green tooltip feedback
            self.lbl_folder.set_tooltip_markup("<span foreground='#22c55e' weight='bold'>Copied!</span>")
            
            def reset_tooltip():
                self.lbl_folder.set_tooltip_text("Click to copy ID")
                return False
                
            GLib.timeout_add(2000, reset_tooltip)

    def set_compact_mode(self, enabled: bool):
        self._compact_mode = enabled
        self.lbl_folder.set_visible(not enabled)
        self.desc_header.set_visible(not enabled)
        self.lbl_desc.set_visible(not enabled)
        self.btn_workshop.set_visible(not enabled)
        self.thumb_grid.set_visible(enabled)
        self.compact_actions.set_visible(enabled)
        if enabled:
            self._update_thumb_grid()

    def set_wallpaper_ids(self, ids: list):
        self._wallpaper_ids = ids

    def set_thumb_clicked_callback(self, cb):
        self._on_thumb_clicked_cb = cb

    def set_compact_callbacks(self, on_stop=None, on_lucky=None, on_jump=None):
        self._on_stop_cb = on_stop
        self._on_lucky_cb = on_lucky
        self._on_jump_cb = on_jump

    def _update_thumb_grid(self):
        while True:
            child = self.thumb_grid.get_first_child()
            if child is None:
                break
            self.thumb_grid.remove(child)

        if not self.selected_wp or not self._wallpaper_ids:
            return

        try:
            current_idx = self._wallpaper_ids.index(self.selected_wp)
        except ValueError:
            return

        start_idx = max(0, current_idx - 2)
        end_idx = min(len(self._wallpaper_ids), current_idx + 3)
        
        for idx in range(start_idx, end_idx):
            wp_id = self._wallpaper_ids[idx]
            thumb = self._create_thumbnail(wp_id, is_current=(idx == current_idx))
            self.thumb_grid.append(thumb)

    def _create_thumbnail(self, wp_id: str, is_current: bool) -> Gtk.Widget:
        btn = Gtk.Button()
        btn.set_size_request(50, 50)
        btn.set_has_frame(False)
        
        wp = self.wp_manager._wallpapers.get(wp_id)
        if wp:
            if wp_id in self._thumb_cache:
                texture = self._thumb_cache[wp_id]
            else:
                texture = self.wp_manager.get_texture(wp['preview'], 50)
                self._thumb_cache[wp_id] = texture
            
            picture = Gtk.Picture()
            picture.set_paintable(texture)
            picture.set_content_fit(Gtk.ContentFit.COVER)
            picture.set_size_request(50, 50)
            btn.set_child(picture)
        
        if is_current:
            btn.add_css_class("suggested-action")
        
        btn.connect("clicked", lambda b, wid=wp_id: self._on_thumb_click(wid))
        return btn

    def _on_thumb_click(self, wp_id: str):
        if callable(self._on_thumb_clicked_cb):
            self._on_thumb_clicked_cb(wp_id)
