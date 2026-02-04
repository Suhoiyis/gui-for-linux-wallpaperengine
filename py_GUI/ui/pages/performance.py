import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Pango

from typing import Dict, List
from py_GUI.core.controller import WallpaperController

class PerformancePage(Gtk.Box):
    def __init__(self, controller: WallpaperController):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.controller = controller
        
        self.set_margin_top(40)
        self.set_margin_bottom(40)
        self.set_margin_start(40)
        self.set_margin_end(40)
        self.set_spacing(30)

        self.build_ui()
        
        # Connect to controller monitor
        self.controller.perf_monitor.add_callback(self.on_perf_update)

    def build_ui(self):
        # Title
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.append(title_box)
        
        t = Gtk.Label(label="System Monitor")
        t.add_css_class("settings-header")
        t.set_halign(Gtk.Align.START)
        title_box.append(t)

        desc = Gtk.Label(label="Real-time resource usage of Wallpaper Engine components.")
        desc.add_css_class("settings-subheader")
        desc.set_halign(Gtk.Align.START)
        title_box.append(desc)

        # Overview Cards
        self.overview_grid = Gtk.Grid()
        self.overview_grid.set_column_spacing(20)
        self.overview_grid.set_row_spacing(20)
        self.overview_grid.set_halign(Gtk.Align.FILL)
        self.append(self.overview_grid)

        self.total_labels = {}
        self.create_overview_card("Total CPU", "cpu", 0, 0, unit="%")
        self.create_overview_card("Total Memory", "memory_mb", 0, 1, unit=" MB")
        self.create_overview_card("Active Threads", "threads", 0, 2)

        # Process Table
        self.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))
        
        table_label = Gtk.Label(label="Process Details")
        table_label.add_css_class("settings-section-title")
        table_label.set_halign(Gtk.Align.START)
        self.append(table_label)

        # Scrolled List
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_min_content_height(300)
        self.append(scroll)

        self.process_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        scroll.set_child(self.process_list)
        
        self.process_widgets = {} # pid -> widget

    def create_overview_card(self, title, key, row, col, unit=""):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        card.add_css_class("card")
        card.add_css_class("setting-row")
        card.set_hexpand(True)
        
        lbl_title = Gtk.Label(label=title)
        lbl_title.add_css_class("setting-desc")
        lbl_title.set_halign(Gtk.Align.START)
        card.append(lbl_title)
        
        lbl_val = Gtk.Label(label="-")
        lbl_val.add_css_class("settings-header")
        lbl_val.set_halign(Gtk.Align.START)
        card.append(lbl_val)
        
        self.overview_grid.attach(card, col, row, 1, 1)
        self.total_labels[key] = (lbl_val, unit)

    def on_perf_update(self, stats: Dict):
        GLib.idle_add(lambda: self._update_ui(stats))

    def _update_ui(self, stats: Dict):
        # Update Overview
        total = stats.get("total", {})
        for key, (lbl, unit) in self.total_labels.items():
            val = total.get(key, 0)
            lbl.set_label(f"{val}{unit}")

        # Update Process List
        details = stats.get("details", {})
        
        # Remove stale
        current_pids = set(d['pid'] for d in details.values())
        tracked_pids = set(self.process_widgets.keys())
        
        for pid in tracked_pids - current_pids:
            row = self.process_widgets.pop(pid)
            self.process_list.remove(row)

        # Update/Add
        for category, data in details.items():
            pid = data['pid']
            if pid not in self.process_widgets:
                row = self._create_process_row(category, data)
                self.process_list.append(row)
                self.process_widgets[pid] = row
            
            self._update_process_row(self.process_widgets[pid], category, data)

    def _create_process_row(self, category: str, data: Dict) -> Gtk.Box:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add_css_class("list-item")
        
        # Icon/Type
        icon_name = "application-x-executable-symbolic"
        if category == "frontend": icon_name = "preferences-desktop-wallpaper-symbolic"
        elif category == "backend": icon_name = "video-display-symbolic"
        
        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(32)
        row.append(icon)

        # Info
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info_box.set_hexpand(True)
        row.append(info_box)

        name_lbl = Gtk.Label(label=f"{category.title()} ({data['pid']})")
        name_lbl.add_css_class("list-title")
        name_lbl.set_halign(Gtk.Align.START)
        info_box.append(name_lbl)

        cmd_lbl = Gtk.Label(label=data['name'])
        cmd_lbl.add_css_class("text-muted")
        cmd_lbl.set_halign(Gtk.Align.START)
        cmd_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        info_box.append(cmd_lbl)

        # Stats
        stats_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        row.append(stats_box)

        def add_stat(val, label, color_class):
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            v = Gtk.Label(label=val)
            v.add_css_class(color_class)
            box.append(v)
            l = Gtk.Label(label=label)
            l.add_css_class("text-muted")
            l.set_font_options(None) # smaller?
            box.append(l)
            stats_box.append(box)

        # Store references to update later using GObject data or children
        # Simplified: just recreate content or use a custom widget class?
        # For simplicity in this file, I'll store labels in the row object
        row.cpu_lbl = Gtk.Label()
        row.cpu_lbl.add_css_class("error") # Red for CPU?
        row.mem_lbl = Gtk.Label()
        row.mem_lbl.add_css_class("success") # Green for mem
        row.status_lbl = Gtk.Label()
        
        # Layout stats manually
        # CPU
        b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        b.set_size_request(80, -1)
        b.append(row.cpu_lbl)
        l = Gtk.Label(label="CPU")
        l.add_css_class("text-muted")
        b.append(l)
        stats_box.append(b)

        # MEM
        b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        b.set_size_request(100, -1)
        b.append(row.mem_lbl)
        l = Gtk.Label(label="Memory")
        l.add_css_class("text-muted")
        b.append(l)
        stats_box.append(b)

        # Status
        b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        b.set_size_request(80, -1)
        b.append(row.status_lbl)
        l = Gtk.Label(label="Status")
        l.add_css_class("text-muted")
        b.append(l)
        stats_box.append(b)

        return row

    def _update_process_row(self, row, category, data):
        row.cpu_lbl.set_label(f"{data['cpu']}%")
        row.mem_lbl.set_label(f"{data['memory_mb']} MB")
        row.status_lbl.set_label(data['status'].upper())
