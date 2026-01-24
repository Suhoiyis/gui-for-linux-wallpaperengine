import random
import os
from typing import Dict, Optional
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Gio', '2.0')
from gi.repository import Gtk, Gdk, Gio, Pango

from py_GUI.ui.components.sidebar import Sidebar
from py_GUI.ui.components.dialogs import show_delete_dialog, show_error_dialog
from py_GUI.core.wallpaper import WallpaperManager
from py_GUI.core.properties import PropertiesManager
from py_GUI.core.controller import WallpaperController
from py_GUI.core.config import ConfigManager
from py_GUI.core.logger import LogManager
from py_GUI.utils import markdown_to_pango

class WallpapersPage(Gtk.Box):
    def __init__(self, window: Gtk.Window, config: ConfigManager, 
                 wp_manager: WallpaperManager, prop_manager: PropertiesManager,
                 controller: WallpaperController, log_manager: LogManager):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        
        self.window = window
        self.config = config
        self.wp_manager = wp_manager
        self.prop_manager = prop_manager
        self.controller = controller
        self.log_manager = log_manager

        self.view_mode = "grid"
        self.search_query = ""
        self.selected_wp: Optional[str] = None
        self.active_wp: Optional[str] = None # Tracks running wallpaper

        self.build_ui()

    def build_ui(self):
        # Toolbar
        self.build_toolbar()
        self.append(self.toolbar)

        # Content Box
        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        content_box.set_vexpand(True)
        content_box.set_hexpand(True)
        self.append(content_box)

        # Left Area
        left_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_area.set_hexpand(True)
        content_box.append(left_area)

        # Status Panel
        self.build_status_panel(left_area)

        # Scroll Area
        self.wallpaper_scroll = Gtk.ScrolledWindow()
        self.wallpaper_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.wallpaper_scroll.set_vexpand(True)
        left_area.append(self.wallpaper_scroll)

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

        self.wallpaper_scroll.set_child(self.flowbox)

        # Sidebar
        self.sidebar = Sidebar(self.wp_manager, self.prop_manager, self.controller, self.log_manager)
        content_box.append(self.sidebar)

    def build_toolbar(self):
        self.toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.toolbar.add_css_class("toolbar")

        # Search
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.toolbar.append(search_box)
        
        lbl = Gtk.Label(label="🔍")
        lbl.add_css_class("status-label")
        search_box.append(lbl)

        self.search_entry = Gtk.Entry()
        self.search_entry.add_css_class("search-entry")
        self.search_entry.set_placeholder_text("Search wallpapers...")
        self.search_entry.set_width_chars(50)
        self.search_entry.connect('changed', self.on_search_changed)
        self.search_entry.connect('activate', self.on_search_activate)
        search_box.append(self.search_entry)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        self.toolbar.append(spacer)

        # Actions
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.toolbar.append(actions_box)

        stop_btn = Gtk.Button(label="⏹")
        stop_btn.add_css_class("mode-btn")
        stop_btn.add_css_class("stop-btn")
        stop_btn.set_tooltip_text("Stop Wallpaper")
        stop_btn.connect("clicked", lambda _: self.on_stop_clicked())
        actions_box.append(stop_btn)

        refresh_btn = Gtk.Button(label="⟳")
        refresh_btn.add_css_class("mode-btn")
        refresh_btn.set_tooltip_text("Refresh Wallpapers")
        refresh_btn.connect("clicked", self.on_reload_wallpapers)
        actions_box.append(refresh_btn)

        lucky_btn = Gtk.Button(label="🎲")
        lucky_btn.add_css_class("mode-btn")
        lucky_btn.set_tooltip_text("I'm feeling lucky")
        lucky_btn.connect("clicked", self.on_feeling_lucky)
        actions_box.append(lucky_btn)

        # View Toggle
        view_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        view_box.set_margin_start(10)
        self.toolbar.append(view_box)

        self.btn_grid = Gtk.ToggleButton(label="⊞")
        self.btn_grid.set_tooltip_text("Grid View")
        self.btn_grid.add_css_class("mode-btn")
        self.btn_grid.set_active(True)
        self.btn_grid.connect("toggled", self.on_view_grid)
        view_box.append(self.btn_grid)

        self.btn_list = Gtk.ToggleButton(label="☰")
        self.btn_list.set_tooltip_text("List View")
        self.btn_list.add_css_class("mode-btn")
        self.btn_list.connect("toggled", self.on_view_list)
        view_box.append(self.btn_list)

    def build_status_panel(self, parent: Gtk.Box):
        status_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        status_box.add_css_class("status-panel")
        status_box.set_margin_start(20)
        status_box.set_margin_end(10)
        status_box.set_margin_top(10)
        status_box.set_margin_bottom(10)

        title = Gtk.Label(label="CURRENTLY USING")
        title.add_css_class("status-label")
        title.set_halign(Gtk.Align.START)
        status_box.append(title)

        self.active_wp_label = Gtk.Label(label="-")
        self.active_wp_label.add_css_class("status-value")
        self.active_wp_label.set_use_markup(True)
        self.active_wp_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.active_wp_label.set_halign(Gtk.Align.START)
        status_box.append(self.active_wp_label)

        parent.append(status_box)

    def on_view_grid(self, btn):
        if btn.get_active():
            self.btn_list.set_active(False)
            self.view_mode = "grid"
            self.refresh_wallpaper_grid()

    def on_view_list(self, btn):
        if btn.get_active():
            self.btn_grid.set_active(False)
            self.view_mode = "list"
            self.refresh_wallpaper_grid()

    def on_search_changed(self, entry):
        self.search_query = entry.get_text().lower().strip()
        self.refresh_wallpaper_grid()

    def on_search_activate(self, entry):
        self.search_query = entry.get_text().lower().strip()
        self.refresh_wallpaper_grid()

    def on_stop_clicked(self):
        self.controller.stop()
        self.active_wp = None
        self.active_wp_label.set_label("None")

    def on_reload_wallpapers(self, btn):
        self.wp_manager.clear_cache()
        # Note: If path changed in settings, manager should be updated.
        # But we don't have direct access to settings page state here.
        # We assume manager is updated or we re-read config?
        # The main app orchestrates this usually. 
        # But for now, just scan.
        self.wp_manager.workshop_path = self.config.get("workshopPath", self.wp_manager.workshop_path)
        self.wp_manager.scan()
        self.refresh_wallpaper_grid()

    def on_feeling_lucky(self, btn):
        if not self.wp_manager._wallpapers:
            return
        wp_id = random.choice(list(self.wp_manager._wallpapers.keys()))
        self.select_wallpaper(wp_id)
        self.apply_wallpaper(wp_id)

    def refresh_wallpaper_grid(self):
        if self.view_mode == "grid":
            self.wallpaper_scroll.set_child(self.flowbox)
            self.populate_grid()
        else:
            self.wallpaper_scroll.set_child(self.listbox)
            self.populate_list()

    def filter_wallpapers(self) -> Dict[str, Dict]:
        if not self.search_query:
            return self.wp_manager._wallpapers
        
        filtered = {}
        for wp_id, wp in self.wp_manager._wallpapers.items():
            title = wp.get('title', '').lower()
            desc = wp.get('description', '').lower()
            tags = ' '.join(str(t).lower() for t in wp.get('tags', []))
            if (self.search_query in title or self.search_query in desc or 
                self.search_query in tags or self.search_query in wp_id.lower()):
                filtered[wp_id] = wp
        return filtered

    def populate_grid(self):
        while True:
            child = self.flowbox.get_first_child()
            if child is None: break
            self.flowbox.remove(child)

        filtered = self.filter_wallpapers()
        for folder_id, wp in filtered.items():
            card = self.create_grid_item(folder_id, wp)
            self.flowbox.append(card)

    def populate_list(self):
        while True:
            child = self.listbox.get_first_child()
            if child is None: break
            self.listbox.remove(child)

        filtered = self.filter_wallpapers()
        for folder_id, wp in filtered.items():
            row = self.create_list_item(folder_id, wp)
            self.listbox.append(row)

    def create_grid_item(self, folder_id: str, wp: Dict) -> Gtk.Widget:
        btn = Gtk.Button()
        btn.add_css_class("wallpaper-item")
        btn.add_css_class("wallpaper-card")
        btn.set_size_request(170, 170)
        btn.set_has_frame(False)
        btn.connect("clicked", lambda _: self.select_wallpaper(folder_id))

        gesture = Gtk.GestureClick.new()
        gesture.set_button(Gdk.BUTTON_PRIMARY)
        gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        gesture.connect("pressed", lambda g, n, x, y: self.on_item_activated(folder_id, n))
        btn.add_controller(gesture)

        context = Gtk.GestureClick.new()
        context.set_button(Gdk.BUTTON_SECONDARY)
        context.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        context.connect("pressed", lambda g, n, x, y: self.on_context_menu(btn, folder_id, x, y))
        btn.add_controller(context)

        overlay = Gtk.Overlay()
        btn.set_child(overlay)

        texture = self.wp_manager.get_texture(wp['preview'], 170)
        if texture:
            pic = Gtk.Picture.new_for_paintable(texture)
            pic.set_content_fit(Gtk.ContentFit.COVER)
            pic.set_size_request(170, 170)
            overlay.set_child(pic)
        else:
            placeholder = Gtk.Box()
            placeholder.set_size_request(170, 170)
            lbl = Gtk.Label(label=wp['title'][:1].upper())
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
        lbl.set_markup(markdown_to_pango(wp['title']))
        lbl.add_css_class("wallpaper-name")
        lbl.set_ellipsize(Pango.EllipsizeMode.END)
        lbl.set_max_width_chars(15)
        name_box.append(lbl)
        overlay.add_overlay(name_box)

        wp['_grid_btn'] = btn
        if folder_id == self.selected_wp:
            btn.add_css_class("selected")

        return btn

    def create_list_item(self, folder_id: str, wp: Dict) -> Gtk.Widget:
        btn = Gtk.Button()
        btn.add_css_class("list-item")
        btn.set_has_frame(False)
        btn.connect("clicked", lambda _: self.select_wallpaper(folder_id))

        gesture = Gtk.GestureClick.new()
        gesture.set_button(Gdk.BUTTON_PRIMARY)
        gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        gesture.connect("pressed", lambda g, n, x, y: self.on_item_activated(folder_id, n))
        btn.add_controller(gesture)

        context = Gtk.GestureClick.new()
        context.set_button(Gdk.BUTTON_SECONDARY)
        context.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        context.connect("pressed", lambda g, n, x, y: self.on_context_menu(btn, folder_id, x, y))
        btn.add_controller(context)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        btn.set_child(hbox)

        texture = self.wp_manager.get_texture(wp['preview'], 100)
        if texture:
            pic = Gtk.Picture.new_for_paintable(texture)
            pic.set_content_fit(Gtk.ContentFit.COVER)
            pic.set_size_request(100, 100)
            pic.add_css_class("card")
            hbox.append(pic)

        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info.set_hexpand(True)
        hbox.append(info)

        t = Gtk.Label()
        t.set_use_markup(True)
        t.set_markup(markdown_to_pango(wp['title']))
        t.add_css_class("list-title")
        t.set_halign(Gtk.Align.START)
        t.set_ellipsize(Pango.EllipsizeMode.END)
        info.append(t)

        typ = Gtk.Label(label=f"Type: {wp.get('type','Unknown')}")
        typ.add_css_class("list-type")
        typ.set_halign(Gtk.Align.START)
        info.append(typ)

        tags = wp.get('tags', [])
        if isinstance(tags, str): tags = [tags]
        tgs = ', '.join(str(x) for x in tags[:5]) if tags else 'None'
        tl = Gtk.Label(label=f"Tags: {tgs}")
        tl.add_css_class("list-tags")
        tl.set_halign(Gtk.Align.START)
        tl.set_ellipsize(Pango.EllipsizeMode.END)
        info.append(tl)

        wp['_list_btn'] = btn
        if folder_id == self.selected_wp:
            btn.add_css_class("selected")

        return btn

    def select_wallpaper(self, folder_id: str):
        # Deselect old
        if self.selected_wp and self.selected_wp in self.wp_manager._wallpapers:
            old = self.wp_manager._wallpapers[self.selected_wp]
            if '_grid_btn' in old: old['_grid_btn'].remove_css_class("selected")
            if '_list_btn' in old: old['_list_btn'].remove_css_class("selected")

        self.selected_wp = folder_id
        wp = self.wp_manager._wallpapers.get(folder_id)
        if wp:
            if '_grid_btn' in wp: wp['_grid_btn'].add_css_class("selected")
            if '_list_btn' in wp: wp['_list_btn'].add_css_class("selected")
        
        self.sidebar.update(folder_id)

    def apply_wallpaper(self, wp_id: str):
        self.controller.apply(wp_id)
        self.active_wp = wp_id
        wp = self.wp_manager._wallpapers.get(wp_id)
        if wp:
            self.active_wp_label.set_markup(markdown_to_pango(wp['title']))

    def on_item_activated(self, folder_id: str, n_press: int):
        if n_press == 2:
            self.select_wallpaper(folder_id)
            self.apply_wallpaper(folder_id)

    def on_context_menu(self, widget, folder_id, x, y):
        menu = Gtk.PopoverMenu()
        
        # Actions are handled by the main window application actions
        menu_model = Gio.Menu()
        menu_model.append_item(Gio.MenuItem.new("Apply Wallpaper", f"win.apply::{folder_id}"))
        menu_model.append_item(Gio.MenuItem.new("Stop Wallpaper", "win.stop"))
        menu_model.append_item(Gio.MenuItem.new("Open Folder", f"win.open_folder::{folder_id}"))
        menu_model.append_item(Gio.MenuItem.new("Delete Wallpaper", f"win.delete::{folder_id}"))

        menu.set_menu_model(menu_model)
        menu.set_parent(widget)
        
        rect = Gdk.Rectangle()
        rect.x = int(x)
        rect.y = int(y)
        rect.width = 1
        rect.height = 1
        menu.set_pointing_to(rect)
        
        menu.popup()

    def delete_wallpaper(self, wp_id: str):
        show_delete_dialog(self.window, wp_id, lambda: self._perform_delete(wp_id))

    def _perform_delete(self, wp_id: str):
        if self.wp_manager.delete_wallpaper(wp_id):
            if self.active_wp == wp_id:
                self.on_stop_clicked()
            self.refresh_wallpaper_grid()
        else:
            show_error_dialog(self.window, "Error", "Failed to delete wallpaper")
            
    def open_wallpaper_folder(self, wp_id: str):
        import subprocess
        import shutil
        
        wp = self.wp_manager._wallpapers.get(wp_id)
        if wp:
            folder_path = os.path.dirname(wp['preview'])
            
            # List of file managers to try in order of preference
            file_managers = [
                "thunar",     # XFCE (Preferred)
                "nautilus",   # GNOME
                "dolphin",    # KDE
                "nemo",       # Cinnamon
                "pcmanfm",    # LXDE
                "pcmanfm-qt", # LXQt
                "caja",       # MATE
                "index",      # Maui
                "files"       # Elementary
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
                    subprocess.Popen(['xdg-open', folder_path])
                except Exception as e:
                    self.log_manager.add_error(f"Failed to open folder: {e}", "GUI")
