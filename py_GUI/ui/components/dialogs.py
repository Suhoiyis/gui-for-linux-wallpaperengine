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
