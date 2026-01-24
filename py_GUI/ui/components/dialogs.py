import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

def show_delete_dialog(parent_window, wp_id, on_confirm):
    dialog = Gtk.MessageDialog(
        transient_for=parent_window,
        modal=True,
        message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.YES_NO,
        text="Delete Wallpaper?"
    )
    dialog.set_property("secondary-text", f"Are you sure you want to delete wallpaper {wp_id}?\nThis action cannot be undone.")

    def on_response(d, response):
        if response == Gtk.ResponseType.YES:
            on_confirm()
        d.destroy()

    dialog.connect("response", on_response)
    dialog.present()

def show_error_dialog(parent_window, title, message):
    error_dialog = Gtk.MessageDialog(
        transient_for=parent_window,
        modal=True,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.OK,
        text=title
    )
    error_dialog.set_property("secondary-text", message)
    error_dialog.connect("response", lambda d, r: d.destroy())
    error_dialog.present()

def show_screenshot_success_dialog(parent_window, file_path):
    import subprocess
    import os
    import shutil
    
    dialog = Gtk.MessageDialog(
        transient_for=parent_window,
        modal=True,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.CLOSE,
        text="Screenshot Saved"
    )
    
    msg = f"Screenshot has been saved to:\n{file_path}"
    dialog.set_property("secondary-text", msg)
    
    # Add custom action buttons
    dialog.add_button("Open Folder", 101)
    dialog.add_button("Open Image", 102)
    
    # Set Open Image as suggested action
    btn_img = dialog.get_widget_for_response(102)
    if btn_img:
        btn_img.add_css_class("suggested-action")

    def on_response(d, response):
        if response == 101: # Open Folder
            try:
                folder = os.path.dirname(file_path)
                
                # Robust file manager detection (copied from WallpapersPage)
                file_managers = [
                    "thunar", "nautilus", "dolphin", "nemo", "pcmanfm", 
                    "pcmanfm-qt", "caja", "index", "files"
                ]
                
                opened = False
                for fm in file_managers:
                    if shutil.which(fm):
                        try:
                            subprocess.Popen([fm, folder])
                            opened = True
                            break
                        except: continue
                
                if not opened:
                    subprocess.Popen(['xdg-open', folder])
            except: pass
        elif response == 102: # Open Image
            try:
                subprocess.Popen(['xdg-open', file_path])
            except: pass
        
        d.destroy()

    dialog.connect("response", on_response)
    dialog.present()
