import gi
from typing import Optional, Callable

gi.require_version("Gtk", "4.0")
try:
    gi.require_version("Adw", "1")
except ValueError:
    pass
from gi.repository import Gtk, Adw


def show_nickname_dialog(
    parent,
    title: str,
    current_nickname: Optional[str],
    on_confirm: Callable[[str], None],
):
    dialog = Adw.MessageDialog(
        transient_for=parent,
        heading="Set Nickname",
        body=f"Set a custom nickname for '{title}'",
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
