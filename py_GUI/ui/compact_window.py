import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf

from typing import Callable, Optional, List

from py_GUI.utils import markdown_to_pango, format_size


class CompactWindow(Gtk.ApplicationWindow):
    def __init__(self, app, wp_manager, controller, config, log_manager, 
                 screen_manager, show_toast: Callable[[str], None],
                 on_compact_mode_toggled: Callable[[bool], None],
                 on_restart_app: Callable[[], None]):
        super().__init__(application=app)
        
        self.app = app
        self.wp_manager = wp_manager
        self.controller = controller
        self.config = config
        self.log_manager = log_manager
        self.screen_manager = screen_manager
        self.show_toast = show_toast
        self.on_compact_mode_toggled_cb = on_compact_mode_toggled
        self.on_restart_app_cb = on_restart_app
        
        self.selected_wp: Optional[str] = None
        self._wallpaper_ids: List[str] = []
        self._thumb_cache = {}
        
        self.set_title("Wallpaper Preview")
        self.set_default_size(300, 800)
        self.set_resizable(True)
        self.connect("close-request", self._on_close_request)
        
        self._build_ui()
    
    def _build_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(main_box)
        
        navbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        navbar.add_css_class("nav-bar")
        navbar.set_margin_start(10)
        navbar.set_margin_end(10)
        main_box.append(navbar)
        
        self.btn_toggle = Gtk.Button()
        self.btn_toggle.set_icon_name("view-restore-symbolic")
        self.btn_toggle.set_tooltip_text("Exit Compact Mode")
        self.btn_toggle.add_css_class("nav-btn")
        self.btn_toggle.connect("clicked", self._on_toggle_clicked)
        navbar.append(self.btn_toggle)
        
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        navbar.append(spacer)
        
        btn_restart = Gtk.Button()
        btn_restart.set_icon_name("system-reboot-symbolic")
        btn_restart.set_tooltip_text("Restart Application")
        btn_restart.add_css_class("nav-btn")
        btn_restart.connect("clicked", lambda _: self.on_restart_app_cb())
        navbar.append(btn_restart)
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        main_box.append(scroll)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        content.set_margin_start(15)
        content.set_margin_end(15)
        content.set_margin_top(10)
        content.set_margin_bottom(10)
        scroll.set_child(content)
        
        preview_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_container.set_size_request(200, 200)
        preview_container.set_halign(Gtk.Align.CENTER)
        preview_container.add_css_class("sidebar-preview")
        content.append(preview_container)
        
        self.preview_image = Gtk.Picture()
        self.preview_image.set_content_fit(Gtk.ContentFit.COVER)
        self.preview_image.set_size_request(200, 200)
        preview_container.append(self.preview_image)
        
        self.lbl_title = Gtk.Label(label="Select a Wallpaper")
        self.lbl_title.add_css_class("sidebar-title")
        self.lbl_title.set_use_markup(True)
        self.lbl_title.set_halign(Gtk.Align.START)
        self.lbl_title.set_wrap(True)
        self.lbl_title.set_max_width_chars(30)
        content.append(self.lbl_title)
        
        info_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        info_row.set_halign(Gtk.Align.START)
        content.append(info_row)
        
        self.lbl_id = Gtk.Label(label="")
        self.lbl_id.add_css_class("folder-chip")
        self.lbl_id.set_tooltip_text("Click to copy ID")
        self.lbl_id.set_cursor_from_name("pointer")
        info_row.append(self.lbl_id)
        
        id_click = Gtk.GestureClick.new()
        id_click.connect("released", lambda gesture, n, x, y: self._on_id_clicked())
        self.lbl_id.add_controller(id_click)
        
        self.lbl_size = Gtk.Label(label="")
        self.lbl_size.add_css_class("size-chip")
        info_row.append(self.lbl_size)
        
        self.lbl_index = Gtk.Label(label="")
        self.lbl_index.add_css_class("index-chip")
        info_row.append(self.lbl_index)
        
        type_tags_grid = Gtk.Grid()
        type_tags_grid.set_row_spacing(4)
        type_tags_grid.set_column_spacing(12)
        type_tags_grid.set_margin_top(8)
        content.append(type_tags_grid)
        
        type_header = Gtk.Label(label="Type")
        type_header.add_css_class("sidebar-section")
        type_header.set_halign(Gtk.Align.START)
        type_tags_grid.attach(type_header, 0, 0, 1, 1)
        
        self.lbl_type = Gtk.Label(label="-")
        self.lbl_type.add_css_class("tag-chip")
        self.lbl_type.set_halign(Gtk.Align.START)
        type_tags_grid.attach(self.lbl_type, 0, 1, 1, 1)
        
        tags_header = Gtk.Label(label="Tags")
        tags_header.add_css_class("sidebar-section")
        tags_header.set_halign(Gtk.Align.START)
        type_tags_grid.attach(tags_header, 1, 0, 1, 1)
        
        self.tags_flow = Gtk.FlowBox()
        self.tags_flow.set_selection_mode(Gtk.SelectionMode.NONE)
        self.tags_flow.set_max_children_per_line(3)
        self.tags_flow.set_min_children_per_line(1)
        self.tags_flow.set_hexpand(True)
        type_tags_grid.attach(self.tags_flow, 1, 1, 1, 1)
        
        self.btn_apply = Gtk.Button(label="Apply Wallpaper")
        self.btn_apply.add_css_class("sidebar-btn")
        self.btn_apply.add_css_class("suggested-action")
        self.btn_apply.set_margin_top(12)
        self.btn_apply.connect("clicked", self._on_apply_clicked)
        content.append(self.btn_apply)
        
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        actions_box.set_halign(Gtk.Align.CENTER)
        actions_box.set_margin_top(8)
        content.append(actions_box)
        
        self.btn_stop = Gtk.Button()
        self.btn_stop.set_size_request(34, 34)
        self.btn_stop.set_icon_name("media-playback-stop-symbolic")
        self.btn_stop.add_css_class("circular")
        self.btn_stop.set_tooltip_text("Stop Wallpaper")
        self.btn_stop.connect("clicked", self._on_stop_clicked)
        actions_box.append(self.btn_stop)
        
        self.btn_lucky = Gtk.Button()
        self.btn_lucky.set_size_request(34, 34)
        self.btn_lucky.set_icon_name("media-playlist-shuffle-symbolic")
        self.btn_lucky.add_css_class("circular")
        self.btn_lucky.set_tooltip_text("I'm feeling lucky")
        self.btn_lucky.connect("clicked", self._on_lucky_clicked)
        actions_box.append(self.btn_lucky)
        
        self.btn_jump = Gtk.Button()
        self.btn_jump.set_size_request(34, 34)
        self.btn_jump.set_icon_name("go-home-symbolic")
        self.btn_jump.add_css_class("circular")
        self.btn_jump.set_tooltip_text("Jump to current wallpaper")
        self.btn_jump.connect("clicked", self._on_jump_clicked)
        actions_box.append(self.btn_jump)
        
        nav_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        nav_container.set_halign(Gtk.Align.CENTER)
        nav_container.set_margin_top(12)
        nav_container.set_margin_bottom(8)
        content.append(nav_container)
        
        btn_prev = Gtk.Button()
        btn_prev.set_size_request(30, 30)
        btn_prev.set_icon_name("go-previous-symbolic")
        btn_prev.add_css_class("flat")
        btn_prev.set_tooltip_text("Previous Wallpaper (Left Arrow)")
        btn_prev.connect("clicked", lambda _: self._navigate_wallpaper(-1))
        nav_container.append(btn_prev)
        
        self.thumb_grid = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        nav_container.append(self.thumb_grid)
        
        btn_next = Gtk.Button()
        btn_next.set_size_request(30, 30)
        btn_next.set_icon_name("go-next-symbolic")
        btn_next.add_css_class("flat")
        btn_next.set_tooltip_text("Next Wallpaper (Right Arrow)")
        btn_next.connect("clicked", lambda _: self._navigate_wallpaper(1))
        nav_container.append(btn_next)
        
        self.anim = None
        self.anim_iter = None
        self.anim_timer = None
    
    def _on_close_request(self, win):
        self.on_compact_mode_toggled_cb(False)
        return True
    
    def _on_toggle_clicked(self, btn):
        self.on_compact_mode_toggled_cb(False)
    
    def _on_apply_clicked(self, btn):
        if self.selected_wp:
            screen = self.config.get("lastScreen", "eDP-1")
            apply_mode = self.config.get("apply_mode", "diff")
            screens = self.screen_manager.get_screens()
            
            if apply_mode == "same" and screens:
                self.controller.apply(self.selected_wp, screens=screens)
            else:
                self.controller.apply(self.selected_wp, screen=screen)
    
    def _on_stop_clicked(self, btn):
        screen = self.config.get("lastScreen", "eDP-1")
        self.controller.stop_screen(screen)
    
    def _on_lucky_clicked(self, btn):
        import random
        if self._wallpaper_ids:
            wp_id = random.choice(self._wallpaper_ids)
            self.select_wallpaper(wp_id)
            self._on_apply_clicked(None)
    
    def _on_jump_clicked(self, btn):
        screen = self.config.get("lastScreen", "eDP-1")
        active_monitors = self.config.get("active_monitors", {})
        current_wp_id = active_monitors.get(screen)
        
        if current_wp_id:
            self.select_wallpaper(current_wp_id)
        else:
            last_wp = self.config.get("lastWallpaper")
            if last_wp:
                self.select_wallpaper(last_wp)
    
    def _on_id_clicked(self):
        if self.selected_wp:
            clipboard = Gdk.Display.get_default().get_clipboard()
            clipboard.set(self.selected_wp)
            self.show_toast(f"Copied ID: {self.selected_wp}")
            self.lbl_id.set_tooltip_markup("<span foreground='#22c55e' weight='bold'>Copied!</span>")
            GLib.timeout_add(1500, lambda: self.lbl_id.set_tooltip_text("Click to copy ID") or False)
    
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
        if not self._wallpaper_ids or not self.selected_wp:
            return
        try:
            current_idx = self._wallpaper_ids.index(self.selected_wp)
            total = len(self._wallpaper_ids)
            if total == 0: return
            
            new_idx = (current_idx + direction) % total
            self.select_wallpaper(self._wallpaper_ids[new_idx])
        except ValueError:
            pass
    
    def set_wallpaper_ids(self, ids: List[str]):
        self._wallpaper_ids = ids
        if self.selected_wp:
            self._update_thumb_grid()
    
    def select_wallpaper(self, wp_id: str):
        self.stop_animation()
        self.selected_wp = wp_id
        
        if not wp_id:
            self._clear()
            return
        
        wp = self.wp_manager._wallpapers.get(wp_id)
        if not wp:
            self._clear()
            return
        
        path = wp.get('preview', '')
        loaded_anim = False
        
        if path.lower().endswith('.gif'):
            try:
                self._start_animation(path)
                loaded_anim = True
            except Exception:
                loaded_anim = False
        
        if not loaded_anim:
            texture = self.wp_manager.get_texture(path, 500)
            self.preview_image.set_paintable(texture)
        
        self.lbl_title.set_markup(markdown_to_pango(wp.get('title', 'Unknown')))
        self.lbl_size.set_label(format_size(wp.get('size', 0)))
        
        self.lbl_id.set_label(str(wp_id))
        
        if self._wallpaper_ids and wp_id in self._wallpaper_ids:
            idx = self._wallpaper_ids.index(wp_id) + 1
            total = len(self._wallpaper_ids)
            self.lbl_index.set_label(f"{idx}/{total}")
        else:
            self.lbl_index.set_label("")
        
        self.lbl_type.set_label(wp.get('type', 'Unknown'))
        
        while True:
            child = self.tags_flow.get_first_child()
            if child is None:
                break
            self.tags_flow.remove(child)
        
        tags = wp.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        if not tags:
            lbl = Gtk.Label(label="None")
            lbl.add_css_class("text-muted")
            self.tags_flow.append(lbl)
        else:
            for tag in tags[:6]:
                chip = Gtk.Label(label=str(tag))
                chip.add_css_class("tag-chip")
                self.tags_flow.append(chip)
        
        self._update_thumb_grid()
    
    def _clear(self):
        self.stop_animation()
        self.selected_wp = None
        self.preview_image.set_paintable(None)
        self.lbl_title.set_label("Select a Wallpaper")
        self.lbl_size.set_label("")
        self.lbl_index.set_label("")
        self.lbl_id.set_label("")
        self.lbl_type.set_label("-")
        
        while True:
            child = self.tags_flow.get_first_child()
            if child is None:
                break
            self.tags_flow.remove(child)
        
        while True:
            child = self.thumb_grid.get_first_child()
            if child is None:
                break
            self.thumb_grid.remove(child)
    
    def _start_animation(self, path):
        self.anim = GdkPixbuf.PixbufAnimation.new_from_file(path)
        self.anim_iter = self.anim.get_iter(None)
        
        pixbuf = self.anim_iter.get_pixbuf()
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.preview_image.set_paintable(texture)
        
        if not self.anim.is_static_image():
            self.anim_timer = GLib.timeout_add(
                self.anim_iter.get_delay_time(),
                self._on_animation_frame
            )
    
    def _on_animation_frame(self):
        if not hasattr(self, 'anim_iter') or not self.anim_iter:
            return False
        
        try:
            self.anim_iter.advance(None)
        except:
            return False
        
        pixbuf = self.anim_iter.get_pixbuf()
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.preview_image.set_paintable(texture)
        
        delay = self.anim_iter.get_delay_time()
        if delay <= 0:
            delay = 100
        
        self.anim_timer = GLib.timeout_add(delay, self._on_animation_frame)
        return False
    
    def stop_animation(self):
        if hasattr(self, 'anim_timer') and self.anim_timer:
            GLib.source_remove(self.anim_timer)
            self.anim_timer = None
        self.anim = None
        self.anim_iter = None
    
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
        
        total = len(self._wallpaper_ids)
        if total == 0: return
        
        for offset in range(-2, 3):
            idx = (current_idx + offset) % total
            wp_id = self._wallpaper_ids[idx]
            
            thumb = self._create_thumbnail(wp_id, is_current=(offset == 0))
            self.thumb_grid.append(thumb)
    
    def _create_thumbnail(self, wp_id: str, is_current: bool) -> Gtk.Widget:
        btn = Gtk.Button()
        btn.set_size_request(40, 40)
        btn.set_has_frame(False)
        
        wp = self.wp_manager._wallpapers.get(wp_id)
        if wp:
            if wp_id in self._thumb_cache:
                texture = self._thumb_cache[wp_id]
            else:
                texture = self.wp_manager.get_texture(wp.get('preview', ''), 40)
                self._thumb_cache[wp_id] = texture
            
            picture = Gtk.Picture()
            picture.set_paintable(texture)
            picture.set_content_fit(Gtk.ContentFit.COVER)
            picture.set_size_request(40, 40)
            btn.set_child(picture)
        
        if is_current:
            btn.add_css_class("suggested-action")
        
        btn.connect("clicked", lambda b, wid=wp_id: self.select_wallpaper(wid))
        return btn
    
    def sync_from_main(self, wallpaper_ids: List[str], selected_wp: Optional[str]):
        self._wallpaper_ids = wallpaper_ids
        if selected_wp:
            self.select_wallpaper(selected_wp)
        elif wallpaper_ids:
            self._on_jump_clicked(None)
