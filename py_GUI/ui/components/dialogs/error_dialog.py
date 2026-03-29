import gi

gi.require_version("Gtk", "4.0")
try:
    gi.require_version("Adw", "1")
except ValueError:
    pass
from gi.repository import Gtk


def show_error_dialog(parent_window, title, message):
    dialog = Gtk.Dialog(transient_for=parent_window, modal=True, title=title)
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
