import os
import gi
gi.require_version('Gtk', '4.0')
try:
    gi.require_version('Adw', '1')
except ValueError:
    pass
from gi.repository import Gtk, Adw, Gdk, Gio

class WelcomeDialog(Gtk.Window):
    def __init__(self, parent, config, integrator):
        super().__init__(transient_for=parent, modal=True)
        self.config = config
        self.integrator = integrator
        
        self.set_title("Welcome")
        self.set_default_size(500, 450)
        self.set_resizable(False)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=32)
        main_box.set_margin_top(40)
        main_box.set_margin_bottom(40)
        main_box.set_margin_start(40)
        main_box.set_margin_end(40)
        self.set_child(main_box)
        
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        main_box.append(header_box)
        
        icon = Gtk.Image.new_from_icon_name("preferences-desktop-wallpaper")
        icon.set_pixel_size(80)
        icon.add_css_class("accent")
        header_box.append(icon)
        
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        header_box.append(title_box)
        
        title = Gtk.Label(label="Welcome to Linux Wallpaper Engine")
        title.add_css_class("title-1")
        title_box.append(title)
        
        subtitle = Gtk.Label(label="Let's get you set up in just a few steps.")
        subtitle.add_css_class("body")
        subtitle.add_css_class("dim-label")
        title_box.append(subtitle)
        
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        main_box.append(content_box)
        
        step1_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        content_box.append(step1_box)
        
        lbl_path = Gtk.Label(label="Steam Workshop Path")
        lbl_path.set_halign(Gtk.Align.START)
        lbl_path.add_css_class("heading")
        step1_box.append(lbl_path)
        
        path_input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        step1_box.append(path_input_box)
        
        current_path = self.config.get('workshopPath', '')
        self.path_entry = Gtk.Entry()
        self.path_entry.set_placeholder_text("/path/to/steamapps/workshop/content/431960")
        if current_path:
            self.path_entry.set_text(current_path)
        self.path_entry.set_hexpand(True)
        path_input_box.append(self.path_entry)
        
        btn_browse = Gtk.Button(icon_name="folder-open-symbolic")
        btn_browse.set_tooltip_text("Browse Folder")
        btn_browse.connect("clicked", self.on_browse_clicked)
        path_input_box.append(btn_browse)
        
        path_desc = Gtk.Label(label="Select the folder where Wallpaper Engine wallpapers are installed (ID: 431960).")
        path_desc.set_halign(Gtk.Align.START)
        path_desc.add_css_class("caption")
        path_desc.add_css_class("dim-label")
        path_desc.set_wrap(True)
        path_desc.set_max_width_chars(50)
        step1_box.append(path_desc)
        
        step2_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        content_box.append(step2_box)
        
        vbox_auto = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox_auto.set_hexpand(True)
        step2_box.append(vbox_auto)
        
        lbl_auto = Gtk.Label(label="Start with System")
        lbl_auto.set_halign(Gtk.Align.START)
        lbl_auto.add_css_class("heading")
        vbox_auto.append(lbl_auto)
        
        desc_auto = Gtk.Label(label="Automatically start in background when you log in.")
        desc_auto.set_halign(Gtk.Align.START)
        desc_auto.add_css_class("caption")
        desc_auto.add_css_class("dim-label")
        vbox_auto.append(desc_auto)
        
        self.switch_auto = Gtk.Switch()
        self.switch_auto.set_valign(Gtk.Align.CENTER)
        if self.integrator.is_autostart_enabled():
            self.switch_auto.set_active(True)
        step2_box.append(self.switch_auto)
        
        footer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        footer_box.set_valign(Gtk.Align.END)
        footer_box.set_vexpand(True)
        main_box.append(footer_box)
        
        self.btn_start = Gtk.Button(label="Start Using App")
        self.btn_start.add_css_class("suggested-action")
        self.btn_start.add_css_class("pill")
        self.btn_start.set_size_request(200, 44)
        self.btn_start.set_halign(Gtk.Align.CENTER)
        self.btn_start.connect("clicked", self.on_start_clicked)
        footer_box.append(self.btn_start)

    def on_browse_clicked(self, button):
        dialog = Gtk.FileChooserNative(
            title="Select Workshop Folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        
        dialog.set_modal(True)
        
        def on_response(d, response):
            if response == Gtk.ResponseType.ACCEPT:
                file = d.get_file()
                path = file.get_path()
                if path:
                    self.path_entry.set_text(path)
            d.destroy()
            
        dialog.connect("response", on_response)
        dialog.show()

    def on_start_clicked(self, button):
        path = self.path_entry.get_text().strip()
        if path:
            self.config.set('workshopPath', path)
            
        enable_autostart = self.switch_auto.get_active()
        try:
            self.integrator.set_autostart(enable_autostart)
        except Exception as e:
            print(f"Failed to set autostart: {e}")
            
        self.config.set('onboarding_completed', True)
        
        self.destroy()
