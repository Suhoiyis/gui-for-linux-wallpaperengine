import gi
import subprocess
import os
import shutil

gi.require_version("Gtk", "4.0")
try:
    gi.require_version("Adw", "1")
except ValueError:
    pass
from gi.repository import Gtk


def show_screenshot_success_dialog(parent_window, file_path, stats=None, texture=None):
    dialog = Gtk.Dialog(
        transient_for=parent_window, modal=True, title="Screenshot Saved"
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
                    "thunar",
                    "nautilus",
                    "dolphin",
                    "nemo",
                    "pcmanfm",
                    "pcmanfm-qt",
                    "caja",
                    "index",
                    "files",
                ]

                opened = False
                for fm in file_managers:
                    if shutil.which(fm):
                        try:
                            subprocess.Popen([fm, folder])
                            opened = True
                            break
                        except Exception:
                            continue

                if not opened:
                    subprocess.Popen(["xdg-open", folder])
            except Exception:
                pass
        elif response == 102:
            try:
                subprocess.Popen(["xdg-open", file_path])
            except Exception:
                pass

        d.destroy()

    dialog.connect("response", on_response)
    dialog.present()
