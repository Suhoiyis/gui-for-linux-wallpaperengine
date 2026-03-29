import gi

gi.require_version("Gtk", "4.0")
try:
    gi.require_version("Adw", "1")
except ValueError:
    pass
from gi.repository import Gtk


def show_delete_dialog(parent_window, wp_id, on_confirm):
    dialog = Gtk.Dialog(
        transient_for=parent_window, modal=True, title="Delete Wallpaper"
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

    desc = Gtk.Label(
        label=f"Are you sure you want to delete wallpaper {wp_id}?\nThis action cannot be undone."
    )
    desc.set_halign(Gtk.Align.START)
    desc.add_css_class("body")
    msg_box.append(desc)

    def on_response(d, response):
        if response == Gtk.ResponseType.YES:
            on_confirm()
        d.destroy()

    dialog.connect("response", on_response)
    dialog.present()
