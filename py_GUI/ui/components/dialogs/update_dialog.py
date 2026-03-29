import gi
from typing import Optional

gi.require_version("Gtk", "4.0")
try:
    gi.require_version("Adw", "1")
except ValueError:
    pass
from gi.repository import Gtk, Adw


def show_update_dialog(
    parent_window,
    current_version: str,
    latest_version: Optional[str],
    release_url: Optional[str],
    has_update: bool,
):
    if has_update and latest_version:
        dialog = Gtk.Dialog(
            transient_for=parent_window, modal=True, title="Found New Version"
        )
        dialog.add_button("Remind Later", Gtk.ResponseType.CANCEL)
        btn_download = dialog.add_button("Download", Gtk.ResponseType.YES)
        btn_download.add_css_class("suggested-action")

        content = dialog.get_content_area()
        content.set_spacing(15)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        content.append(box)

        icon = Gtk.Image.new_from_icon_name("folder-download-symbolic")
        icon.set_pixel_size(48)
        icon.add_css_class("accent")
        box.append(icon)

        msg_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.append(msg_box)

        lbl = Gtk.Label(label="Found New Version")
        lbl.add_css_class("title-2")
        lbl.set_halign(Gtk.Align.START)
        msg_box.append(lbl)

        version_lbl = Gtk.Label(
            label=f"Current: v{current_version}  →  Latest: v{latest_version}"
        )
        version_lbl.set_halign(Gtk.Align.START)
        version_lbl.add_css_class("body")
        msg_box.append(version_lbl)

        desc = Gtk.Label(label="Recommend updating to get new features and bug fixes.")
        desc.set_halign(Gtk.Align.START)
        desc.set_wrap(True)
        desc.set_max_width_chars(50)
        desc.add_css_class("body")
        desc.add_css_class("dim-label")
        msg_box.append(desc)

        def on_response(d, response):
            if response == Gtk.ResponseType.YES:
                import webbrowser

                if release_url:
                    webbrowser.open(release_url)
            d.destroy()

        dialog.connect("response", on_response)
        dialog.present()
    elif latest_version == "ERROR:RATE_LIMIT":
        dialog = Adw.MessageDialog(
            transient_for=parent_window,
            heading="Rate Limit Exceeded",
            body="GitHub API rate limit exceeded. Please try again later.",
        )
        dialog.add_response("ok", "OK")
        dialog.connect("response", lambda d, r: d.close())
        dialog.present()
    elif latest_version is None:
        dialog = Adw.MessageDialog(
            transient_for=parent_window,
            heading="Network Error",
            body="Unable to check for updates. Please check your network connection.",
        )
        dialog.add_response("ok", "OK")
        dialog.connect("response", lambda d, r: d.close())
        dialog.present()
    else:
        dialog = Adw.MessageDialog(
            transient_for=parent_window,
            heading="Up to Date",
            body="You are using the latest version.",
        )
        dialog.add_response("ok", "OK")
        dialog.connect("response", lambda d, r: d.close())
        dialog.present()
