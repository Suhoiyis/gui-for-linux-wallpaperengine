#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, AyatanaAppIndicator3, GLib
import subprocess
import signal
import sys
import os

class TrayProcess:
    def __init__(self, icon_path):
        self.icon_path = icon_path
        self.run_gui_path = self._find_run_gui()
        
        # Create Indicator
        self.indicator = AyatanaAppIndicator3.Indicator.new(
            "wallpaper-engine-gui",
            "preferences-desktop-wallpaper",
            AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        
        # Set custom icon if available
        if self.icon_path:
            abs_path = os.path.abspath(self.icon_path)
            if os.path.exists(abs_path):
                # print(f"Loading icon from: {abs_path}")
                self.indicator.set_icon_full(abs_path, "Wallpaper Engine")
            else:
                print(f"Icon not found at: {abs_path}")
        
        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self._build_menu())
        
        # Handle SIGTERM to exit cleanly
        signal.signal(signal.SIGTERM, lambda *_: Gtk.main_quit())
        
        # Start state poller (check every 2 seconds)
        GLib.timeout_add_seconds(2, self._poll_state)
    
    def _find_run_gui(self):
        # Locate run_gui.py relative to this file
        # this file: py_GUI/ui/tray_process.py
        # run_gui.py: ./run_gui.py (root)
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(base, 'run_gui.py')
    
    def _build_menu(self):
        menu = Gtk.Menu()
        
        # Show Window (First item, bold)
        item_show = Gtk.MenuItem()
        label = Gtk.Label(label="<b>显示窗口</b>")
        label.set_use_markup(True)
        item_show.add(label)
        item_show.connect("activate", lambda _: self._cmd("--show"))
        menu.append(item_show)
        
        # Set as secondary activate target (Middle click)
        try:
            self.indicator.set_secondary_activate_target(item_show)
        except:
            pass
            
        menu.append(Gtk.SeparatorMenuItem())
        
        # Toggle Wallpaper (Dynamic Label)
        self.toggle_item = Gtk.MenuItem(label="应用上次壁纸")
        self.toggle_item.connect("activate", self._on_toggle)
        menu.append(self.toggle_item)
        
        # Random Wallpaper
        item_random = Gtk.MenuItem(label="随机切换壁纸")
        item_random.connect("activate", lambda _: self._cmd("--random"))
        menu.append(item_random)
        
        menu.append(Gtk.SeparatorMenuItem())
        
        # Quit
        item_quit = Gtk.MenuItem(label="退出程序")
        item_quit.connect("activate", lambda _: self._cmd("--quit"))
        menu.append(item_quit)
        
        menu.show_all()
        return menu
    
    def _poll_state(self):
        running = False
        try:
            # Check if linux-wallpaperengine is running
            # Filter out python processes to avoid matching this script or the main GUI
            # shell=True required for pipes
            cmd = "pgrep -f linux-wallpaperengine | grep -v python"
            ret = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL)
            running = (ret == 0)
        except Exception as e:
            # print(f"Poll error: {e}")
            running = False
            
        current_label = self.toggle_item.get_label()
        if running:
            if current_label != "停止播放":
                self.toggle_item.set_label("停止播放")
        else:
            if current_label != "应用上次壁纸":
                self.toggle_item.set_label("应用上次壁纸")
        return True # Keep calling

    def _on_toggle(self, widget):
        label = widget.get_label()
        # print(f"Toggle clicked. Label: '{label}'")
        if label == "停止播放":
            self._cmd("--stop")
            # Optimistically update label immediately for better UX
            # The poller will correct it later if it failed
            self.toggle_item.set_label("应用上次壁纸")
        else:
            self._cmd("--apply-last")
            self.toggle_item.set_label("停止播放")

    def _cmd(self, arg):
        # Call the main app via CLI
        subprocess.Popen(['python3', self.run_gui_path, arg])
    
    def run(self):
        Gtk.main()

if __name__ == "__main__":
    icon = sys.argv[1] if len(sys.argv) > 1 else ""
    TrayProcess(icon).run()
