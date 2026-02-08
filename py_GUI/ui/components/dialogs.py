import gi
gi.require_version('Gtk', '4.0')
try:
    gi.require_version('Adw', '1')
except ValueError:
    pass
from gi.repository import Gtk, Adw, Gdk
from typing import Optional, Callable

def show_delete_dialog(parent_window, wp_id, on_confirm):
    dialog = Gtk.Dialog(
        transient_for=parent_window,
        modal=True,
        title="Delete Wallpaper"
    )
    dialog.add_button("Cancel", Gtk.ResponseType.NO)
    btn_del = dialog.add_button("Delete", Gtk.ResponseType.YES)
    btn_del.add_css_class("destructive-action")
    
    content = dialog.get_content_area()
    content.set_spacing(15)
    content.set_margin_top(20)
    content.set_margin_bottom(20)
    content.set_margin_start(20)
    content.set_margin_end(20)
    
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    content.append(box)
    
    icon = Gtk.Image.new_from_icon_name("dialog-warning-symbolic")
    icon.set_pixel_size(48)
    icon.add_css_class("warning")
    box.append(icon)
    
    msg_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    box.append(msg_box)
    
    lbl = Gtk.Label(label="Delete Wallpaper?")
    lbl.add_css_class("title-2")
    lbl.set_halign(Gtk.Align.START)
    msg_box.append(lbl)
    
    desc = Gtk.Label(label=f"Are you sure you want to delete wallpaper {wp_id}?\nThis action cannot be undone.")
    desc.set_halign(Gtk.Align.START)
    desc.add_css_class("body")
    msg_box.append(desc)

    def on_response(d, response):
        if response == Gtk.ResponseType.YES:
            on_confirm()
        d.destroy()

    dialog.connect("response", on_response)
    dialog.present()

def show_error_dialog(parent_window, title, message):
    dialog = Gtk.Dialog(
        transient_for=parent_window,
        modal=True,
        title=title
    )
    dialog.add_button("OK", Gtk.ResponseType.OK)
    
    content = dialog.get_content_area()
    content.set_spacing(15)
    content.set_margin_top(20)
    content.set_margin_bottom(20)
    content.set_margin_start(20)
    content.set_margin_end(20)
    
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    content.append(box)
    
    icon = Gtk.Image.new_from_icon_name("dialog-error-symbolic")
    icon.set_pixel_size(48)
    icon.add_css_class("error")
    box.append(icon)
    
    msg_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    box.append(msg_box)
    
    lbl = Gtk.Label(label=title)
    lbl.add_css_class("title-2")
    lbl.set_halign(Gtk.Align.START)
    msg_box.append(lbl)
    
    desc = Gtk.Label(label=message)
    desc.set_halign(Gtk.Align.START)
    desc.set_wrap(True)
    desc.set_max_width_chars(50)
    desc.add_css_class("body")
    msg_box.append(desc)
    
    dialog.connect("response", lambda d, r: d.destroy())
    dialog.present()

def show_screenshot_success_dialog(parent_window, file_path, stats=None, texture=None):
    import subprocess
    import os
    import shutil
    
    dialog = Gtk.Dialog(
        transient_for=parent_window,
        modal=True,
        title="Screenshot Saved"
    )
    dialog.add_button("Close", Gtk.ResponseType.CLOSE)
    dialog.add_button("Open Folder", 101)
    dialog.add_button("Open Image", 102)
    
    btn_img = dialog.get_widget_for_response(102)
    if btn_img:
        btn_img.add_css_class("suggested-action")
    
    content = dialog.get_content_area()
    content.set_spacing(15)
    content.set_margin_top(20)
    content.set_margin_bottom(10)
    content.set_margin_start(20)
    content.set_margin_end(20)
    
    main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    content.append(main_box)
    
    if texture:
        thumb = Gtk.Picture.new_for_paintable(texture)
        thumb.set_size_request(160, 90)
        thumb.set_content_fit(Gtk.ContentFit.COVER)
        thumb.add_css_class("thumbnail")
        main_box.append(thumb)
    else:
        icon = Gtk.Image.new_from_icon_name("camera-photo-symbolic")
        icon.set_pixel_size(64)
        main_box.append(icon)
    
    info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    info_box.set_hexpand(True)
    main_box.append(info_box)
    
    title_lbl = Gtk.Label(label="Screenshot Saved")
    title_lbl.add_css_class("title-1")
    title_lbl.set_halign(Gtk.Align.START)
    info_box.append(title_lbl)
    
    path_lbl = Gtk.Label(label=file_path)
    path_lbl.set_halign(Gtk.Align.START)
    path_lbl.set_wrap(True)
    path_lbl.set_max_width_chars(45)
    path_lbl.add_css_class("body")
    info_box.append(path_lbl)
    
    if stats:
        stats_lbl = Gtk.Label(label=stats)
        stats_lbl.set_halign(Gtk.Align.START)
        stats_lbl.add_css_class("body")
        info_box.append(stats_lbl)
    
    def on_response(d, response):
        if response == 101:
            try:
                folder = os.path.dirname(file_path)
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
        elif response == 102:
            try:
                subprocess.Popen(['xdg-open', file_path])
            except: pass
        
        d.destroy()

    dialog.connect("response", on_response)
    dialog.present()

def show_nickname_dialog(parent, wp_id: str, title: str, preview_path: Optional[str], current_nickname: Optional[str], on_confirm: Callable[[str], None]):
    dialog = Adw.MessageDialog(
        transient_for=parent,
        heading="Set Nickname",
        body=f"Set a custom nickname for '{title}'"
    )
    
    dialog.add_response("cancel", "Cancel")
    dialog.add_response("save", "Save")
    dialog.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
    dialog.set_default_response("save")
    dialog.set_close_response("cancel")
    
    content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    content_box.set_margin_top(12)
    content_box.set_margin_bottom(12)
    content_box.set_margin_start(12)
    content_box.set_margin_end(12)
    
    if preview_path:
        try:
            picture = Gtk.Picture.new_for_filename(preview_path)
            picture.set_size_request(100, 100)
            picture.set_content_fit(Gtk.ContentFit.COVER)
            picture.add_css_class("card")
            content_box.append(picture)
        except Exception:
            pass
            
    entry = Gtk.Entry()
    entry.set_placeholder_text("Enter nickname...")
    if current_nickname:
        entry.set_text(current_nickname)
    entry.set_activates_default(True)
    content_box.append(entry)
    
    hint = Gtk.Label(label="Leave empty to remove nickname")
    hint.add_css_class("caption")
    hint.add_css_class("dim-label")
    content_box.append(hint)
    
    dialog.set_extra_child(content_box)
    
    def on_response(d, response):
        if response == "save":
            text = entry.get_text().strip()
            on_confirm(text)
        d.close()
        
    dialog.connect("response", on_response)
    dialog.present()
