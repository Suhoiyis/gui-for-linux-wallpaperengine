import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib, Pango
from datetime import datetime
import os

class HistoryDialog(Gtk.Window):
    def __init__(self, parent, history_manager, wp_manager, controller, nickname_manager=None):
        super().__init__(title="Playback History")
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_default_size(500, 600)
        
        self.history_manager = history_manager
        self.wp_manager = wp_manager
        self.controller = controller
        self.nickname_manager = nickname_manager
        
        header = Gtk.HeaderBar()
        self.set_titlebar(header)
        
        clear_btn = Gtk.Button(label="Clear")
        clear_btn.add_css_class("destructive-action")
        clear_btn.connect("clicked", self.on_clear_clicked)
        header.pack_end(clear_btn)

        self.lbl_count = Gtk.Label(label="0/30")
        self.lbl_count.add_css_class("caption")
        self.lbl_count.add_css_class("dim-label")
        self.lbl_count.set_margin_end(10)
        header.pack_end(self.lbl_count)
        
        self.stack = Gtk.Stack()
        self.stack.set_vexpand(True)
        self.stack.set_hexpand(True)
        self.set_child(self.stack)
        
        empty_state = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        empty_state.set_valign(Gtk.Align.CENTER)
        empty_state.set_halign(Gtk.Align.CENTER)
        
        empty_icon = Gtk.Image.new_from_icon_name("document-open-recent-symbolic")
        empty_icon.set_pixel_size(64)
        empty_icon.add_css_class("dim-label")
        empty_label = Gtk.Label(label="No Recent Playback History")
        empty_label.add_css_class("title-4")
        empty_label.add_css_class("dim-label")
        empty_state.append(empty_icon)
        empty_state.append(empty_label)
        self.stack.add_named(empty_state, "empty")
        
        list_container = Gtk.ScrolledWindow()
        list_container.set_vexpand(True)
        list_container.set_hexpand(True)
        
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.list_box.add_css_class("rich-list")
        self.list_box.set_vexpand(True)
        self.list_box.set_show_separators(True)
        list_container.set_child(self.list_box)
        self.stack.add_named(list_container, "list")
        
        self._load_history()
        
    def _load_history(self):
        while True:
            row = self.list_box.get_first_child()
            if not row:
                break
            self.list_box.remove(row)
            
        history = self.history_manager.get_all()
        
        self.lbl_count.set_label(f"{len(history)}/30")
        
        if len(history) == 0:
            self.stack.set_visible_child_name("empty")
        else:
            self.stack.set_visible_child_name("list")
            for item in history:
                row = self._create_row(item)
                self.list_box.append(row)
            
    def _create_row(self, item):
        wp_id = item.get("id", "unknown")
        title = item.get("title", "Unknown Title")
        preview_path = item.get("preview", "")
        timestamp_str = item.get("timestamp", "")
        
        display_title = title
        if self.nickname_manager:
            dummy_wp = {"id": wp_id, "title": title}
            nickname, _ = self.nickname_manager.get_display_name(dummy_wp)
            if nickname != title:
                display_title = f"<i>{nickname}</i>"
            
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

        box.set_margin_top(8)
        box.set_margin_bottom(8)
        box.set_margin_start(12)
        box.set_margin_end(12)
        
        texture = self.wp_manager.get_texture(preview_path, size=64)
        if texture:
            image = Gtk.Image.new_from_paintable(texture)
            image.set_pixel_size(64)
        else:
            image = Gtk.Image.new_from_icon_name("image-missing-symbolic")
            image.set_pixel_size(64)
        
        box.append(image)
        
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        text_box.set_valign(Gtk.Align.CENTER)
        text_box.set_hexpand(True)
        
        title_label = Gtk.Label()
        title_label.set_markup(display_title)
        title_label.set_xalign(0)
        title_label.set_ellipsize(Pango.EllipsizeMode.END)
        title_label.add_css_class("heading")
        
        id_label = Gtk.Label(label=f"ID: {wp_id}")
        id_label.set_xalign(0)
        id_label.add_css_class("caption")
        id_label.add_css_class("dim-label")
        
        text_box.append(title_label)
        text_box.append(id_label)
        box.append(text_box)
        
        action_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        action_box.set_valign(Gtk.Align.CENTER)
        
        time_str = ""
        if timestamp_str:
            try:
                dt = datetime.fromisoformat(timestamp_str)
                time_str = dt.strftime("%m-%d %H:%M")
            except ValueError:
                time_str = ""
        
        time_label = Gtk.Label(label=time_str)
        time_label.set_halign(Gtk.Align.END)
        time_label.add_css_class("caption")
        time_label.add_css_class("dim-label")
        
        play_btn = Gtk.Button(icon_name="media-playback-start-symbolic")
        play_btn.set_tooltip_text("Apply this wallpaper")
        play_btn.add_css_class("flat")
        play_btn.add_css_class("circular")
        play_btn.connect("clicked", lambda b: self.on_apply_clicked(wp_id))
        
        action_box.append(time_label)
        action_box.append(play_btn)
        
        box.append(action_box)
        
        return box

    def on_clear_clicked(self, button):
        self.history_manager.clear()
        self._load_history()
        
    def on_apply_clicked(self, wp_id):
        root = self.get_transient_for()
        if root and hasattr(root, 'activate_action'):
            root.activate_action("win.apply", GLib.Variant("s", wp_id))
