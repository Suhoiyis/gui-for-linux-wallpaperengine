import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib, Pango

import time
from typing import Dict, List
from py_GUI.core.controller import WallpaperController
from py_GUI.ui.components.sparkline import Sparkline

class PerformancePage(Gtk.Box):
    def __init__(self, controller: WallpaperController):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.controller = controller
        
        # Inject Custom CSS
        provider = Gtk.CssProvider()
        css = """
        .memory-text {
            color: #2980b9;
            font-weight: bold;
        }
        """
        provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.append(scroll)
        
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
        self.content_box.set_margin_top(40)
        self.content_box.set_margin_bottom(40)
        self.content_box.set_margin_start(40)
        self.content_box.set_margin_end(40)
        scroll.set_child(self.content_box)

        self.build_ui()
        
        self.controller.perf_monitor.add_callback(self.on_perf_update)

    def build_ui(self):
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.content_box.append(title_box)
        
        t = Gtk.Label(label="System Monitor")
        t.add_css_class("settings-header")
        t.set_halign(Gtk.Align.START)
        title_box.append(t)

        desc = Gtk.Label(label="Real-time resource usage of Wallpaper Engine components.")
        desc.add_css_class("settings-subheader")
        desc.set_halign(Gtk.Align.START)
        title_box.append(desc)

        self.overview_grid = Gtk.Grid()
        self.overview_grid.set_column_spacing(20)
        self.overview_grid.set_row_spacing(20)
        self.overview_grid.set_halign(Gtk.Align.FILL)
        self.content_box.append(self.overview_grid)

        self.total_labels = {}
        self.create_overview_card("Total CPU", "cpu", 0, 0, unit="%")
        self.create_overview_card("Total Memory", "memory_mb", 0, 1, unit=" MB")
        self.create_overview_card("Active Threads", "threads", 0, 2)
        
        # Total Charts Row
        total_charts_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.content_box.append(total_charts_row)
        
        # Total CPU Chart
        cpu_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        cpu_card.add_css_class("card")
        cpu_card.set_hexpand(True)
        self.total_cpu_chart = Sparkline(color=(0.937, 0.267, 0.267), height=150, title="Total CPU History")
        cpu_card.append(self.total_cpu_chart)
        total_charts_row.append(cpu_card)
        
        # Total Mem Chart
        mem_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        mem_card.add_css_class("card")
        mem_card.set_hexpand(True)
        self.total_mem_chart = Sparkline(color=(0.16, 0.5, 0.73), height=150, title="Total Memory History")
        mem_card.append(self.total_mem_chart)
        total_charts_row.append(mem_card)

        self.create_threads_expander()

        self.content_box.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))
        
        table_label = Gtk.Label(label="Process Details")
        table_label.add_css_class("settings-section-title")
        table_label.set_halign(Gtk.Align.START)
        self.content_box.append(table_label)

        self.process_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.content_box.append(self.process_list)
        
        self.process_widgets = {}
        
        self.build_screenshot_history_panel()

    def create_overview_card(self, title, key, row, col, unit=""):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        card.add_css_class("card")
        card.add_css_class("setting-row")
        card.set_hexpand(True)
        card.set_margin_top(5)
        card.set_margin_bottom(5)
        card.set_margin_start(10)
        card.set_margin_end(10)
        
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

    def create_threads_expander(self):
        expander = Gtk.Expander(label="Thread Details")
        expander.set_expanded(False)
        expander.add_css_class("card")
        self.content_box.append(expander)
        
        self.threads_list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.threads_list_box.set_margin_top(15)
        self.threads_list_box.set_margin_start(20)
        self.threads_list_box.set_margin_end(20)
        self.threads_list_box.set_margin_bottom(15)
        expander.set_child(self.threads_list_box)

    def on_perf_update(self, stats: Dict):
        GLib.idle_add(lambda: self._update_ui(stats))

    def _update_ui(self, stats: Dict):
        total = stats.get("total", {})
        for key, (lbl, unit) in self.total_labels.items():
            fmt_key = f"{key}_fmt"
            if fmt_key in total:
                lbl.set_label(total[fmt_key])
            else:
                val = total.get(key, 0)
                lbl.set_label(f"{val}{unit}")
            
            if key == "cpu":
                lbl.remove_css_class("success")
                lbl.remove_css_class("warning")
                lbl.remove_css_class("error")
                cpu_val = total.get("cpu", 0)
                if cpu_val < 20:
                    lbl.add_css_class("success")
                elif cpu_val < 40:
                    lbl.add_css_class("warning")
                else:
                    lbl.add_css_class("error")
            elif key == "memory_mb":
                lbl.add_css_class("memory-text")
        
        history = total.get("history", {})
        if "cpu" in history:
            cpu_data = history["cpu"]
            max_cpu = max(max(cpu_data) * 1.2, 10.0) if cpu_data else 10.0
            max_cpu = min(max_cpu, 100.0)
            self.total_cpu_chart.set_data(cpu_data, max_val=max_cpu, unit="%")
            
            current_cpu = cpu_data[-1] if cpu_data else 0
            if current_cpu < 20:
                self.total_cpu_chart.set_color((0.18, 0.76, 0.49))
            elif current_cpu < 40:
                self.total_cpu_chart.set_color((0.96, 0.62, 0.04))
            else:
                self.total_cpu_chart.set_color((0.88, 0.11, 0.14))
            
        if "memory_mb" in history:
            self.total_mem_chart.set_data(history["memory_mb"], unit=" MB")
        
        thread_names = total.get("thread_names", {})
        while self.threads_list_box.get_first_child():
            self.threads_list_box.remove(self.threads_list_box.get_first_child())
        
        for category, names in thread_names.items():
            header = Gtk.Label(label=f"{category.title()} ({len(names)})")
            header.set_halign(Gtk.Align.START)
            header.add_css_class("heading")
            self.threads_list_box.append(header)
            
            grid = Gtk.Grid()
            grid.set_column_spacing(20)
            grid.set_row_spacing(6)
            grid.set_column_homogeneous(True)
            self.threads_list_box.append(grid)
            
            for i, name in enumerate(names):
                row_idx = i // 3
                col_idx = i % 3
                lbl = Gtk.Label(label=f"• {name}")
                lbl.set_halign(Gtk.Align.START)
                lbl.add_css_class("text-muted")
                lbl.set_ellipsize(Pango.EllipsizeMode.END)
                grid.attach(lbl, col_idx, row_idx, 1, 1)

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
        
        history = self.controller.perf_monitor.get_screenshot_history()
        latest_ts = history[-1].get("timestamp", 0) if history else 0
        if latest_ts != self._last_screenshot_ts:
            self._last_screenshot_ts = latest_ts
            self._refresh_screenshot_history()

    def _create_process_row(self, category: str, data: Dict) -> Gtk.Box:
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        main_box.add_css_class("list-item")
        
        # Header Row (Icon + Info + Current Stats)
        header_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        main_box.append(header_row)
        
        # Icon/Type
        icon_name = "application-x-executable-symbolic"
        if category == "frontend": icon_name = "preferences-desktop-wallpaper-symbolic"
        elif category == "backend": icon_name = "video-display-symbolic"
        elif category == "tray": icon_name = "system-run-symbolic"
        
        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(32)
        header_row.append(icon)

        # Info
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info_box.set_hexpand(True)
        header_row.append(info_box)

        name_lbl = Gtk.Label(label=f"{category.title()} ({data['pid']})")
        name_lbl.add_css_class("list-title")
        name_lbl.set_halign(Gtk.Align.START)
        info_box.append(name_lbl)

        cmd_lbl = Gtk.Label(label=data['name'])
        cmd_lbl.add_css_class("text-muted")
        cmd_lbl.set_halign(Gtk.Align.START)
        cmd_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        info_box.append(cmd_lbl)

        # Current Stats
        stats_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        header_row.append(stats_box)

        main_box.cpu_lbl = Gtk.Label()
        main_box.cpu_lbl.add_css_class("error")
        main_box.mem_lbl = Gtk.Label()
        main_box.mem_lbl.add_css_class("memory-text")
        main_box.status_lbl = Gtk.Label()
        
        # CPU
        b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        b.set_size_request(80, -1)
        b.append(main_box.cpu_lbl)
        l = Gtk.Label(label="CPU")
        l.add_css_class("text-muted")
        b.append(l)
        stats_box.append(b)

        # MEM
        b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        b.set_size_request(100, -1)
        b.append(main_box.mem_lbl)
        l = Gtk.Label(label="Memory")
        l.add_css_class("text-muted")
        b.append(l)
        stats_box.append(b)

        # Status
        b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        b.set_size_request(80, -1)
        b.append(main_box.status_lbl)
        l = Gtk.Label(label="Status")
        l.add_css_class("text-muted")
        b.append(l)
        stats_box.append(b)

        # Charts Row
        charts_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        charts_row.set_margin_start(52) # Align with text
        main_box.append(charts_row)
        
        # CPU Chart
        cpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        cpu_box.set_hexpand(True)
        main_box.cpu_chart = Sparkline(color=(0.937, 0.267, 0.267), height=120, title="CPU Usage")
        cpu_box.append(main_box.cpu_chart)
        charts_row.append(cpu_box)
        
        # Mem Chart
        mem_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        mem_box.set_hexpand(True)
        main_box.mem_chart = Sparkline(color=(0.16, 0.5, 0.73), height=120, title="Memory Usage")
        mem_box.append(main_box.mem_chart)
        charts_row.append(mem_box)
        
        # Spacer to match status column
        spacer = Gtk.Box()
        spacer.set_size_request(80, -1)
        charts_row.append(spacer)

        # Wallpaper Details Expander (Backend only)
        if category == "backend":
            main_box.details_expander = Gtk.Expander(label="Wallpaper Details")
            main_box.details_expander.set_margin_start(52)
            main_box.details_expander.set_visible(False)
            
            main_box.details_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            main_box.details_box.set_margin_top(5)
            main_box.details_box.set_margin_bottom(10)
            main_box.details_expander.set_child(main_box.details_box)
            
            main_box.append(main_box.details_expander)
            main_box.last_monitors_hash = None

        return main_box

    def _update_process_row(self, row, category, data):
        cpu_val = data.get('cpu', 0)
        row.cpu_lbl.set_label(data.get('cpu_fmt', f"{cpu_val}%"))
        
        # Colorize CPU Label
        row.cpu_lbl.remove_css_class("success")
        row.cpu_lbl.remove_css_class("warning")
        row.cpu_lbl.remove_css_class("error")
        
        if cpu_val < 20:
            row.cpu_lbl.add_css_class("success")
            cpu_color = (0.18, 0.76, 0.49) # Green
        elif cpu_val < 40:
            row.cpu_lbl.add_css_class("warning")
            cpu_color = (0.96, 0.62, 0.04) # Orange
        else:
            row.cpu_lbl.add_css_class("error")
            cpu_color = (0.88, 0.11, 0.14) # Red
            
        row.mem_lbl.set_label(data.get('memory_fmt', f"{data['memory_mb']} MB"))
        row.status_lbl.set_label(data['status'].upper())
        
        history = data.get("history", {})
        if "cpu" in history:
            # Auto-scale CPU chart (min 10% to prevent flatline at very low usage)
            cpu_data = history["cpu"]
            max_cpu = max(max(cpu_data) * 1.2, 10.0) if cpu_data else 10.0
            max_cpu = min(max_cpu, 100.0) # Cap at 100%
            row.cpu_chart.set_data(cpu_data, max_val=max_cpu, unit="%")
            row.cpu_chart.set_color(cpu_color)
            
        if "memory_mb" in history:
            # Auto-scale memory chart
            row.mem_chart.set_data(history["memory_mb"], unit=" MB")

        # Update Wallpaper Details (Backend only)
        if category == "backend" and hasattr(row, 'details_expander'):
            try:
                active_monitors = self.controller.config.get("active_monitors", {})
                current_hash = str(active_monitors)
                
                if current_hash != row.last_monitors_hash:
                    row.last_monitors_hash = current_hash
                    
                    if active_monitors:
                        row.details_expander.set_visible(True)
                        
                        while row.details_box.get_first_child():
                            row.details_box.remove(row.details_box.get_first_child())
                        
                        for screen, wp_id in active_monitors.items():
                            title = "Unknown"
                            preview_path = None
                            clean_id = str(wp_id).strip()
                            
                            if hasattr(self.controller, 'wp_manager'):
                                wp = self.controller.wp_manager.get_wallpaper(clean_id)
                                if wp:
                                    title = wp.get("title", "Untitled")
                                    preview_path = wp.get("preview")
                            
                            s_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
                            s_row.set_margin_top(5)
                            s_row.set_margin_bottom(5)
                            row.details_box.append(s_row)
                            
                            if preview_path and hasattr(self.controller, 'wp_manager'):
                                texture = self.controller.wp_manager.get_texture(preview_path, size=64)
                                if texture:
                                    thumb = Gtk.Picture.new_for_paintable(texture)
                                    thumb.set_size_request(64, 36)
                                    thumb.set_content_fit(Gtk.ContentFit.COVER)
                                    thumb.add_css_class("thumbnail")
                                    s_row.append(thumb)
                                else:
                                    placeholder = Gtk.Image.new_from_icon_name("image-missing-symbolic")
                                    placeholder.set_pixel_size(36)
                                    s_row.append(placeholder)
                            else:
                                placeholder = Gtk.Image.new_from_icon_name("video-display-symbolic")
                                placeholder.set_pixel_size(36)
                                s_row.append(placeholder)
                            
                            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
                            info_box.set_valign(Gtk.Align.CENTER)
                            s_row.append(info_box)
                            
                            screen_lbl = Gtk.Label(label=screen)
                            screen_lbl.set_halign(Gtk.Align.START)
                            screen_lbl.add_css_class("heading")
                            info_box.append(screen_lbl)
                            
                            title_lbl = Gtk.Label(label=title)
                            title_lbl.set_halign(Gtk.Align.START)
                            title_lbl.set_ellipsize(Pango.EllipsizeMode.END)
                            title_lbl.set_max_width_chars(40)
                            info_box.append(title_lbl)
                            
                            id_lbl = Gtk.Label(label=f"ID: {wp_id}")
                            id_lbl.add_css_class("text-muted")
                            id_lbl.set_halign(Gtk.Align.START)
                            info_box.append(id_lbl)
                    else:
                        row.details_expander.set_visible(False)
            except Exception as e:
                print(f"[Performance] Backend details error: {e}")

    def build_screenshot_history_panel(self):
        self.content_box.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))
        
        header_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.content_box.append(header_row)
        
        header = Gtk.Label(label="Screenshot History")
        header.add_css_class("settings-section-title")
        header.set_halign(Gtk.Align.START)
        header.set_hexpand(True)
        header_row.append(header)
        
        clear_btn = Gtk.Button(label="Clear")
        clear_btn.add_css_class("flat")
        clear_btn.set_tooltip_text("Clear all screenshot history")
        clear_btn.connect("clicked", self._on_clear_history_clicked)
        header_row.append(clear_btn)
        
        desc = Gtk.Label(label="Resource usage from recent screenshot captures (last 10).")
        desc.add_css_class("text-muted")
        desc.set_halign(Gtk.Align.START)
        self.content_box.append(desc)
        
        self.screenshot_history_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.content_box.append(self.screenshot_history_box)
        
        self._last_screenshot_ts = 0
        self._refresh_screenshot_history()

    def _refresh_screenshot_history(self):
        while self.screenshot_history_box.get_first_child():
            self.screenshot_history_box.remove(self.screenshot_history_box.get_first_child())
        
        history = self.controller.perf_monitor.get_screenshot_history()
        
        if not history:
            empty_label = Gtk.Label(label="No screenshots taken yet.")
            empty_label.add_css_class("text-muted")
            empty_label.set_halign(Gtk.Align.START)
            self.screenshot_history_box.append(empty_label)
            return
        
        for record in reversed(history):
            row = self._create_screenshot_history_row(record)
            self.screenshot_history_box.append(row)

    def _on_clear_history_clicked(self, btn):
        self.controller.perf_monitor.clear_screenshot_history()
        self._last_screenshot_ts = 0
        self._refresh_screenshot_history()

    def _create_screenshot_history_row(self, record: Dict) -> Gtk.Box:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        row.add_css_class("list-item")
        row.set_margin_top(5)
        row.set_margin_bottom(5)
        
        wp_id = record.get("wp_id", "Unknown")
        output_path = record.get("output_path", "")
        wp_title = None
        thumbnail_added = False
        
        if hasattr(self.controller, 'wp_manager'):
            wp = self.controller.wp_manager.get_wallpaper(str(wp_id))
            if wp:
                wp_title = wp.get("title")
                if wp.get("preview"):
                    texture = self.controller.wp_manager.get_texture(wp["preview"], size=48)
                    if texture:
                        thumb = Gtk.Picture.new_for_paintable(texture)
                        thumb.set_size_request(48, 27)
                        thumb.set_content_fit(Gtk.ContentFit.COVER)
                        thumb.add_css_class("thumbnail")
                        row.append(thumb)
                        thumbnail_added = True
        
        if not thumbnail_added:
            icon = Gtk.Image.new_from_icon_name("camera-photo-symbolic")
            icon.set_pixel_size(24)
            row.append(icon)
        
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        info_box.set_hexpand(True)
        row.append(info_box)
        
        timestamp = record.get("timestamp", 0)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        
        display_name = wp_title if wp_title else f"Wallpaper {wp_id}"
        title_lbl = Gtk.Label(label=display_name)
        title_lbl.add_css_class("list-title")
        title_lbl.set_halign(Gtk.Align.START)
        title_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        title_lbl.set_max_width_chars(30)
        info_box.append(title_lbl)
        
        time_lbl = Gtk.Label(label=time_str)
        time_lbl.add_css_class("text-muted")
        time_lbl.set_halign(Gtk.Align.START)
        info_box.append(time_lbl)
        
        stats_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.append(stats_box)
        
        duration = record.get("duration", 0)
        max_cpu = record.get("max_cpu", 0)
        max_mem = record.get("max_mem", 0)
        
        self._add_stat_column(stats_box, f"{duration:.1f}s", "Duration", 70)
        self._add_stat_column(stats_box, f"{max_cpu:.1f}%", "Max CPU", 70)
        self._add_stat_column(stats_box, f"{max_mem:.1f} MB", "Max Mem", 80)
        
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        row.append(actions_box)
        
        open_folder_btn = Gtk.Button()
        open_folder_btn.set_icon_name("folder-open-symbolic")
        open_folder_btn.add_css_class("flat")
        open_folder_btn.set_tooltip_text("Open folder")
        open_folder_btn.connect("clicked", lambda _: self._open_screenshot_folder(output_path))
        actions_box.append(open_folder_btn)
        
        open_image_btn = Gtk.Button()
        open_image_btn.set_icon_name("image-x-generic-symbolic")
        open_image_btn.add_css_class("flat")
        open_image_btn.set_tooltip_text("Open image")
        open_image_btn.connect("clicked", lambda _: self._open_screenshot_image(output_path))
        actions_box.append(open_image_btn)
        
        return row

    def _open_screenshot_folder(self, path: str):
        import subprocess
        import shutil
        import os
        if not path or not os.path.exists(path):
            return
        
        folder = os.path.dirname(path)
        file_managers = [
            "thunar", "nautilus", "dolphin", "nemo",
            "pcmanfm", "pcmanfm-qt", "caja", "index", "files"
        ]
        
        for fm in file_managers:
            if shutil.which(fm):
                try:
                    subprocess.Popen([fm, folder])
                    return
                except:
                    continue
        
        try:
            subprocess.Popen(["xdg-open", folder])
        except:
            pass

    def _open_screenshot_image(self, path: str):
        import subprocess
        import os
        if path and os.path.exists(path):
            subprocess.Popen(["xdg-open", path])

    def _add_stat_column(self, parent: Gtk.Box, value: str, label: str, width: int):
        col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        col.set_size_request(width, -1)
        
        val_lbl = Gtk.Label(label=value)
        val_lbl.add_css_class("heading")
        col.append(val_lbl)
        
        lbl = Gtk.Label(label=label)
        lbl.add_css_class("text-muted")
        col.append(lbl)
        
        parent.append(col)
