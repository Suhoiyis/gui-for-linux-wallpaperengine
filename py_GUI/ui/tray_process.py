#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, AyatanaAppIndicator3
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
        if os.path.exists(self.icon_path):
            self.indicator.set_icon_full(self.icon_path, "Wallpaper Engine")
        
        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self._build_menu())
        
        # Handle SIGTERM to exit cleanly
        signal.signal(signal.SIGTERM, lambda *_: Gtk.main_quit())
    
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
        # Note: Left click usually opens menu, but this item is at the top.
        try:
            self.indicator.set_secondary_activate_target(item_show)
        except:
            pass
            
        menu.append(Gtk.SeparatorMenuItem())
        
        # Stop Wallpaper
        item_stop = Gtk.MenuItem(label="停止播放")
        item_stop.connect("activate", lambda _: self._cmd("--stop"))
        menu.append(item_stop)
        
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
    
    def _cmd(self, arg):
        # Call the main app via CLI
        subprocess.Popen(['python3', self.run_gui_path, arg])
    
    def run(self):
        Gtk.main()

if __name__ == "__main__":
    icon = sys.argv[1] if len(sys.argv) > 1 else ""
    TrayProcess(icon).run()
