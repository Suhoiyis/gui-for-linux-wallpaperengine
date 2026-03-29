# pyright: reportAttributeAccessIssue=false

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .shared import create_row, make_tab_scrolled_container


def build_audio_tab(settings_page) -> Gtk.Widget:
    box = make_tab_scrolled_container(settings_page.stack, "audio")

    t = Gtk.Label(label="Audio")
    t.add_css_class("settings-section-title")
    t.set_halign(Gtk.Align.START)
    box.append(t)

    r = create_row("Silence Wallpaper", "Mute all audio.")
    box.append(r)
    settings_page.silence_sw = Gtk.Switch()
    settings_page.silence_sw.set_active(settings_page.config.get("silence", True))
    settings_page.silence_sw.set_valign(Gtk.Align.CENTER)
    r.append(settings_page.silence_sw)

    r = create_row("Volume", "Master volume (0-100).")
    box.append(r)
    settings_page.vol_spin = Gtk.SpinButton()
    settings_page.vol_spin.set_range(0, 100)
    settings_page.vol_spin.set_increments(5, 10)
    settings_page.vol_spin.set_value(settings_page.config.get("volume", 50))
    r.append(settings_page.vol_spin)

    r = create_row(
        "Disable Auto Mute", "Prevent automatic muting when other apps play sound."
    )
    box.append(r)
    settings_page.noautomute_sw = Gtk.Switch()
    settings_page.noautomute_sw.set_active(
        settings_page.config.get("noautomute", False)
    )
    settings_page.noautomute_sw.set_valign(Gtk.Align.CENTER)
    r.append(settings_page.noautomute_sw)

    r = create_row(
        "Disable Audio Processing", "Disable sound spectrum analysis (saves CPU)."
    )
    box.append(r)
    settings_page.noaudioproc_sw = Gtk.Switch()
    settings_page.noaudioproc_sw.set_active(
        settings_page.config.get("noAudioProcessing", False)
    )
    settings_page.noaudioproc_sw.set_valign(Gtk.Align.CENTER)
    r.append(settings_page.noaudioproc_sw)

    return box
