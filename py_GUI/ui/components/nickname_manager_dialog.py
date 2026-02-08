import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, GLib, Pango
from typing import Dict, Tuple, List
from py_GUI.core.nickname import NicknameManager
from py_GUI.core.wallpaper import WallpaperManager

class NicknameManagerDialog(Gtk.Window):
    def __init__(self, parent, nickname_manager: NicknameManager, wp_manager: WallpaperManager, on_saved=None):
        super().__init__(modal=True)
        self.set_transient_for(parent)
        self.set_default_size(600, 500)
        self.set_title("Nickname Manager")
        
        self.nickname_manager = nickname_manager
        self.wp_manager = wp_manager
        self.on_saved_callback = on_saved
        self.rows: List[Tuple[str, Gtk.CheckButton, Gtk.Entry]] = [] 
        
        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(main_box)
        
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)
        main_box.append(header)
        
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        toolbar.set_margin_start(12)
        toolbar.set_margin_end(12)
        toolbar.set_margin_top(12)
        toolbar.set_margin_bottom(12)
        main_box.append(toolbar)
        
        btn_select_all = Gtk.Button(label="Select All")
        btn_select_all.add_css_class("flat")
        btn_select_all.connect("clicked", self.on_select_all)
        toolbar.append(btn_select_all)
        
        btn_deselect_all = Gtk.Button(label="Deselect All")
        btn_deselect_all.add_css_class("flat")
        btn_deselect_all.connect("clicked", self.on_deselect_all)
        toolbar.append(btn_deselect_all)
        
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        toolbar.append(spacer)
        
        btn_delete = Gtk.Button(label="Delete Selected")
        btn_delete.add_css_class("destructive-action")
        btn_delete.connect("clicked", self.on_delete_selected)
        toolbar.append(btn_delete)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_box.append(scrolled)
        
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.list_box.add_css_class("boxed-list")
        self.list_box.set_margin_top(10)
        self.list_box.set_margin_bottom(10)
        self.list_box.set_margin_start(20)
        self.list_box.set_margin_end(20)
        scrolled.set_child(self.list_box)
        
        bottom_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        bottom_bar.set_margin_start(16)
        bottom_bar.set_margin_end(16)
        bottom_bar.set_margin_top(16)
        bottom_bar.set_margin_bottom(16)
        bottom_bar.set_halign(Gtk.Align.END)
        main_box.append(bottom_bar)
        
        btn_cancel = Gtk.Button(label="Cancel")
        btn_cancel.connect("clicked", lambda _: self.close())
        bottom_bar.append(btn_cancel)
        
        btn_save = Gtk.Button(label="Save Changes")
        btn_save.add_css_class("suggested-action")
        btn_save.add_css_class("pill")
        btn_save.connect("clicked", self.on_save)
        bottom_bar.append(btn_save)

    def load_data(self):
        nicknames = self.nickname_manager.get_all()
        
        if not nicknames:
            row = Gtk.ListBoxRow()
            row.set_activatable(False)
            lbl = Gtk.Label(label="No nicknames set.")
            lbl.set_margin_start(20)
            lbl.set_margin_end(20)
            lbl.set_margin_top(20)
            lbl.set_margin_bottom(20)
            lbl.add_css_class("dim-label")
            row.set_child(lbl)
            self.list_box.append(row)
            return

        sorted_items = sorted(nicknames.items(), key=lambda x: x[1].lower())

        for wp_id, nick in sorted_items:
            row = Gtk.ListBoxRow()
            row.set_activatable(False)
            
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            box.set_margin_start(8)
            box.set_margin_end(8)
            box.set_margin_top(8)
            box.set_margin_bottom(8)
            row.set_child(box)
            
            check = Gtk.CheckButton()
            check.set_valign(Gtk.Align.CENTER)
            box.append(check)
            
            wp_data = self.wp_manager.get_wallpaper(wp_id)
            title = "Unknown Wallpaper"
            
            if wp_data:
                preview_path = wp_data.get("preview")
                title = wp_data.get("title", "Unknown")
                
                texture = None
                if preview_path:
                    texture = self.wp_manager.get_texture(preview_path, 48)
                    
                if texture:
                    img = Gtk.Picture.new_for_paintable(texture)
                    img.set_size_request(48, 48)
                    img.set_content_fit(Gtk.ContentFit.COVER)
                    img.add_css_class("card")
                    box.append(img)
                else:
                    self._add_placeholder_icon(box)
            else:
                title = f"ID: {wp_id}"
                self._add_placeholder_icon(box)
                
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            vbox.set_valign(Gtk.Align.CENTER)
            vbox.set_hexpand(True)
            box.append(vbox)
            
            lbl_title = Gtk.Label(label=title)
            lbl_title.set_halign(Gtk.Align.START)
            lbl_title.add_css_class("caption")
            lbl_title.add_css_class("dim-label")
            lbl_title.set_ellipsize(Pango.EllipsizeMode.END)
            lbl_title.set_max_width_chars(40)
            vbox.append(lbl_title)
            
            entry = Gtk.Entry()
            entry.set_text(nick)
            entry.set_placeholder_text("Nickname")
            vbox.append(entry)
            
            self.list_box.append(row)
            self.rows.append((wp_id, check, entry))

    def _add_placeholder_icon(self, box):
        icon = Gtk.Image.new_from_icon_name("image-missing-symbolic")
        icon.set_pixel_size(32)
        icon.set_size_request(48, 48)
        box.append(icon)

    def on_select_all(self, btn):
        for _, check, _ in self.rows:
            check.set_active(True)

    def on_deselect_all(self, btn):
        for _, check, _ in self.rows:
            check.set_active(False)

    def on_delete_selected(self, btn):
        count = 0
        for _, check, entry in self.rows:
            if check.get_active():
                entry.set_text("")
                count += 1


    def on_save(self, btn):
        for wp_id, _, entry in self.rows:
            new_nick = entry.get_text()
            self.nickname_manager.set(wp_id, new_nick)
        
        if self.on_saved_callback:
            self.on_saved_callback()
            
        self.close()
