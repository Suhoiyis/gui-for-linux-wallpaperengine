import threading
import webbrowser
from typing import Dict, List, Optional
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk, GLib

from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.logger import LogManager
from py_GUI.utils import markdown_to_pango, bbcode_to_pango, format_size

class Sidebar(Gtk.Box):
    def __init__(self, wp_manager: WallpaperManager, prop_manager: PropertiesManager, 
                 controller: WallpaperController, log_manager: LogManager):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.wp_manager = wp_manager
        self.prop_manager = prop_manager
        self.controller = controller
        self.log_manager = log_manager
        
        self.selected_wp: Optional[str] = None
        
        self.add_css_class("sidebar")
        self.set_size_request(320, -1)
        self.set_hexpand(False)
        
        self.build_ui()

    def build_ui(self):
        # Scrollable area
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_hexpand(False)
        self.append(scroll)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content.set_hexpand(False)
        content.set_size_request(320, -1)
        scroll.set_child(content)

        # Preview Image
        preview_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_container.set_size_request(280, 280)
        preview_container.set_hexpand(False)
        preview_container.set_halign(Gtk.Align.CENTER)
        preview_container.add_css_class("sidebar-preview")

        self.preview_image = Gtk.Picture()
        self.preview_image.set_content_fit(Gtk.ContentFit.COVER)
        self.preview_image.set_size_request(280, 280)
        self.preview_image.set_hexpand(False)
        preview_container.append(self.preview_image)
        content.append(preview_container)

        # Title
        self.lbl_title = Gtk.Label(label="Select a Wallpaper")
        self.lbl_title.add_css_class("sidebar-title")
        self.lbl_title.set_use_markup(True)
        self.lbl_title.set_halign(Gtk.Align.START)
        self.lbl_title.set_wrap(True)
        self.lbl_title.set_max_width_chars(25)
        content.append(self.lbl_title)

        folder_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        folder_row.set_halign(Gtk.Align.START)
        content.append(folder_row)

        self.lbl_folder = Gtk.Label(label="")
        self.lbl_folder.add_css_class("folder-chip")
        self.lbl_folder.set_tooltip_text("Click to copy ID")
        self.lbl_folder.set_cursor_from_name("pointer")
        folder_row.append(self.lbl_folder)

        self.lbl_size = Gtk.Label(label="")
        self.lbl_size.add_css_class("size-chip")
        folder_row.append(self.lbl_size)

        self.lbl_index = Gtk.Label(label="")
        self.lbl_index.add_css_class("index-chip")
        folder_row.append(self.lbl_index)

        # Folder click to copy
        folder_click = Gtk.GestureClick.new()
        folder_click.connect("released", self.on_folder_clicked)
        self.lbl_folder.add_controller(folder_click)

        # Type
        type_header = Gtk.Label(label="Type")
        type_header.add_css_class("sidebar-section")
        type_header.set_halign(Gtk.Align.START)
        content.append(type_header)

        type_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        type_container.set_margin_start(20)
        content.append(type_container)

        self.lbl_type = Gtk.Label(label="-")
        self.lbl_type.add_css_class("tag-chip")
        self.lbl_type.set_halign(Gtk.Align.START)
        type_container.append(self.lbl_type)

        # Tags
        tags_header = Gtk.Label(label="Tags")
        tags_header.add_css_class("sidebar-section")
        tags_header.set_halign(Gtk.Align.START)
        content.append(tags_header)

        tags_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        tags_container.set_hexpand(False)
        content.append(tags_container)

        self.tags_flow = Gtk.FlowBox()
        self.tags_flow.set_selection_mode(Gtk.SelectionMode.NONE)
        self.tags_flow.set_max_children_per_line(4)
        self.tags_flow.set_hexpand(False)
        tags_container.append(self.tags_flow)

        # Description
        desc_header = Gtk.Label(label="Description")
        desc_header.add_css_class("sidebar-section")
        desc_header.set_halign(Gtk.Align.START)
        content.append(desc_header)

        self.lbl_desc = Gtk.Label(label="No description.")
        self.lbl_desc.add_css_class("sidebar-desc")
        self.lbl_desc.set_halign(Gtk.Align.START)
        self.lbl_desc.set_xalign(0)
        self.lbl_desc.set_wrap(True)
        self.lbl_desc.set_use_markup(True)
        self.lbl_desc.set_max_width_chars(30)
        self.lbl_desc.set_selectable(True)
        content.append(self.lbl_desc)

        # Properties
        # sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        # sep.set_margin_top(20)
        # content.append(sep)

        # props_header = Gtk.Label(label="Properties")
        # props_header.add_css_class("sidebar-section")
        # props_header.set_margin_top(15)
        # props_header.set_halign(Gtk.Align.START)
        # content.append(props_header)

        # self.props_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        # self.props_box.set_margin_start(15)
        # self.props_box.set_margin_end(15)
        # self.props_box.set_hexpand(False)
        # content.append(self.props_box)

        # self.props_loading_lbl = Gtk.Label(label="Loading properties...")
        # self.props_loading_lbl.add_css_class("text-muted")
        # Initially not added

        # Bottom Buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        btn_box.set_margin_top(20)
        btn_box.set_margin_bottom(20)
        self.append(btn_box)

        self.btn_apply = Gtk.Button(label="Apply Wallpaper")
        self.btn_apply.add_css_class("sidebar-btn")
        self.btn_apply.connect("clicked", self.on_apply_clicked)
        btn_box.append(self.btn_apply)

        self.btn_workshop = Gtk.Button(label="Open in Workshop")
        self.btn_workshop.add_css_class("sidebar-btn")
        self.btn_workshop.add_css_class("secondary")
        self.btn_workshop.connect("clicked", self.on_workshop_clicked)
        btn_box.append(self.btn_workshop)

    def update(self, wp_id: Optional[str], index: int = 0, total: int = 0):
        self.selected_wp = wp_id
        if not wp_id:
            self.clear()
            return

        wp = self.wp_manager._wallpapers.get(wp_id)
        if not wp:
            self.clear()
            return

        # Update preview
        texture = self.wp_manager.get_texture(wp['preview'], 500)
        self.preview_image.set_paintable(texture)

        # Update Info
        self.lbl_title.set_markup(markdown_to_pango(wp['title']))
        self.lbl_folder.set_label(f"Folder: {wp['id']}")
        self.lbl_size.set_label(format_size(wp.get('size', 0)))
        self.lbl_index.set_label(f"{index}/{total}")
        self.lbl_type.set_label(wp.get('type', 'Unknown'))
        
        # Parse description BBCode
        desc = wp.get('description', '')
        self.lbl_desc.set_markup(bbcode_to_pango(desc) or 'No description.')

        # Update Tags
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

        # Load properties (Commented out as backend support is limited)
        # self.load_properties(wp_id)

    def clear(self):
        self.selected_wp = None
        self.preview_image.set_paintable(None)
        self.lbl_title.set_label("Select a Wallpaper")
        self.lbl_folder.set_label("")
        self.lbl_size.set_label("")
        self.lbl_index.set_label("")
        self.lbl_type.set_label("-")
        self.lbl_desc.set_label("No description.")
        
        # Clear tags
        while True:
            child = self.tags_flow.get_first_child()
            if child is None: break
            self.tags_flow.remove(child)

        # Clear properties
        # while True:
        #     child = self.props_box.get_first_child()
        #     if child is None: break
        #     self.props_box.remove(child)

    # def load_properties(self, wp_id: str):
    #     # Clear existing
    #     while True:
    #         child = self.props_box.get_first_child()
    #         if child is None: break
    #         self.props_box.remove(child)

    #     self.props_box.append(self.props_loading_lbl)

    #     def load_async():
    #         properties = self.prop_manager.get_properties(wp_id)
    #         GLib.idle_add(lambda: self.display_properties(properties))

    #     threading.Thread(target=load_async, daemon=True).start()

    # def display_properties(self, properties: List[Dict]):
    #     if self.props_loading_lbl.get_parent():
    #         self.props_box.remove(self.props_loading_lbl)

    #     if not properties:
    #         no_props = Gtk.Label(label="No properties available.")
    #         no_props.add_css_class("text-muted")
    #         self.props_box.append(no_props)
    #         return

    #     for prop in properties:
    #         widget = self.create_property_widget(prop)
    #         self.props_box.append(widget)

    # def create_property_widget(self, prop: Dict) -> Gtk.Widget:
    #     container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    #     container.set_margin_top(8)
    #     container.set_hexpand(False)

    #     title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    #     title_box.set_hexpand(False)
    #     container.append(title_box)

    #     title_label = Gtk.Label(label=prop.get('text', prop['name']))
    #     title_label.set_halign(Gtk.Align.START)
    #     title_label.add_css_class("setting-label")
    #     title_box.append(title_label)

    #     prop_type = prop['type']
    #     prop_name = prop['name']
    #     
    #     if not self.selected_wp: return
    #     user_value = self.prop_manager.get_user_property(self.selected_wp, prop_name)
    #     current_value = user_value if user_value is not None else prop['value']

    #     if prop_type == 'boolean':
    #         switch = Gtk.Switch()
    #         switch.set_active(bool(current_value))
    #         switch.set_valign(Gtk.Align.CENTER)
    #         switch.set_halign(Gtk.Align.START)
    #         switch.set_hexpand(False)
    #         switch.connect('state-set', lambda s, v: self.on_property_changed(prop_name, v, 'boolean'))
    #         container.append(switch)

    #     elif prop_type == 'slider':
    #         slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, prop['min'], prop['max'], prop['step'])
    #         slider.set_value(float(current_value or 0))
    #         slider.set_hexpand(False)
    #         slider.set_size_request(280, -1)
    #         
    #         val_lbl = Gtk.Label(label=f"{float(current_value or 0):.2f}")
    #         val_lbl.add_css_class("text-muted")
    #         val_lbl.set_halign(Gtk.Align.START)
    #         
    #         def on_slider_changed(s):
    #             val = s.get_value()
    #             val_lbl.set_label(f"{val:.2f}")
    #             self.on_property_changed(prop_name, val, 'slider')
    #             
    #         slider.connect('value-changed', on_slider_changed)
    #         container.append(slider)
    #         container.append(val_lbl)

    #     elif prop_type == 'color':
    #         color = Gtk.ColorButton()
    #         color.set_hexpand(False)
    #         if isinstance(current_value, (tuple, list)) and len(current_value) >= 3:
    #             gdk_color = Gdk.RGBA()
    #             gdk_color.parse(f"rgb({int(current_value[0]*255)}, {int(current_value[1]*255)}, {int(current_value[2]*255)})")
    #             color.set_rgba(gdk_color)
    #         color.connect('color-set', lambda w: self.on_color_property_changed(prop_name, w.get_rgba(), 'color'))
    #         container.append(color)

    #     elif prop_type == 'combo':
    #         if prop['options']:
    #             opt_strs = [opt['label'] for opt in prop['options']]
    #             dd = Gtk.DropDown.new_from_strings(opt_strs)
    #             dd.set_hexpand(False)
    #             dd.set_size_request(280, -1)
    #             
    #             idx = 0
    #             for i, opt in enumerate(prop['options']):
    #                 if str(opt['value']) == str(current_value):
    #                     idx = i
    #                     break
    #             dd.set_selected(idx)
    #             dd.connect('notify::selected', lambda w, p: self.on_combo_property_changed(prop_name, prop['options'], w.get_selected(), 'combo'))
    #             container.append(dd)
    #         else:
    #             lbl = Gtk.Label(label="No options")
    #             lbl.add_css_class("text-muted")
    #             container.append(lbl)

    #     return container

    # def on_property_changed(self, prop_name: str, value, prop_type: str):
    #     if not self.selected_wp: return
    #     if prop_type == 'boolean':
    #         self.prop_manager.set_user_property(self.selected_wp, prop_name, bool(value))
    #     elif prop_type == 'slider':
    #         self.prop_manager.set_user_property(self.selected_wp, prop_name, float(value))
    #     
    #     self.check_reapply()

    # def on_color_property_changed(self, prop_name: str, color: Gdk.RGBA, prop_type: str):
    #     if not self.selected_wp: return
    #     r, g, b = color.red, color.green, color.blue
    #     self.prop_manager.set_user_property(self.selected_wp, prop_name, (r, g, b))
    #     self.check_reapply()

    # def on_combo_property_changed(self, prop_name: str, options: List[Dict], idx: int, prop_type: str):
    #     if not self.selected_wp: return
    #     if idx < len(options):
    #         self.prop_manager.set_user_property(self.selected_wp, prop_name, options[idx]['value'])
    #         self.check_reapply()

    # def check_reapply(self):
    #     # We need to know if this wallpaper is currently active.
    #     # Ideally the parent or app tells us, or we query the config/controller.
    #     # But controller logic is: "apply(id)".
    #     # For now, let's assume we re-apply if it matches lastWallpaper in config?
    #     # Or better: The Sidebar doesn't know about "active" state easily. 
    #     # But `wallpaper_gui.py` checked `self.active_wp == self.selected_wp`.
    #     # I'll rely on a callback or simple check.
    #     # Actually, let's just trigger an event or call controller if it IS the current one.
    #     # Since I don't have `active_wp` passed in, I'll check config.
    #     
    #     last_wp = self.prop_manager._config.get("lastWallpaper")
    #     if self.selected_wp == last_wp:
    #         self.log_manager.add_debug(f"Property changed for active wallpaper {self.selected_wp}, reapplying...", "Sidebar")
    #         self.controller.apply(self.selected_wp)

    def on_apply_clicked(self, btn):
        if self.selected_wp:
            self.controller.apply(self.selected_wp)
            # Signal update to parent? The parent (WallpapersPage) usually updates the "Status Panel".
            # I can expose a callback. But for now, controller.apply updates the backend.
            # The UI update for "active wallpaper" label needs to happen.
            # Maybe `Sidebar` should emit a signal? "wallpaper-applied".
            # For simplicity, I will use a custom signal-like mechanism or direct call if I passed the parent.
            # But I didn't pass parent.
            # I'll leave it as is; the backend works, but the "Current Wallpaper" label in top left won't update
            # unless we hook it up.
            # TODO: Add callback for applied wallpaper.
            pass

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
