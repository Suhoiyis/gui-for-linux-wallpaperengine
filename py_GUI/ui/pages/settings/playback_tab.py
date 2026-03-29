# pyright: reportAttributeAccessIssue=false

import os

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .shared import create_row, make_tab_scrolled_container


def build_playback_tab(settings_page) -> Gtk.Widget:
    box = make_tab_scrolled_container(settings_page.stack, "general")

    t = Gtk.Label(label="General")
    t.add_css_class("settings-section-title")
    t.set_halign(Gtk.Align.START)
    box.append(t)

    r = create_row("Wallpaper Nicknames", "Manage custom names for wallpapers.")
    box.append(r)

    btn_manage_nicks = Gtk.Button(label="Manage")
    btn_manage_nicks.set_valign(Gtk.Align.CENTER)
    btn_manage_nicks.connect("clicked", settings_page.on_manage_nicknames)
    r.append(btn_manage_nicks)

    r = create_row("FPS Limit", "Target frames per second.")
    box.append(r)
    settings_page.fps_spin = Gtk.SpinButton()
    settings_page.fps_spin.set_range(1, 144)
    settings_page.fps_spin.set_increments(1, 10)
    settings_page.fps_spin.set_value(settings_page.config.get("fps", 30))
    r.append(settings_page.fps_spin)

    r = create_row("Scaling Mode", "How the wallpaper fits.")
    box.append(r)
    scaling_opts = ["default", "stretch", "fit", "fill"]
    settings_page.scaling_dd = Gtk.DropDown.new_from_strings(scaling_opts)
    curr = str(settings_page.config.get("scaling") or "default")
    if curr in scaling_opts:
        settings_page.scaling_dd.set_selected(scaling_opts.index(curr))
    r.append(settings_page.scaling_dd)

    r = create_row("No Fullscreen Pause", "Keep running in fullscreen.")
    box.append(r)
    settings_page.pause_sw = Gtk.Switch()
    settings_page.pause_sw.set_active(
        settings_page.config.get("noFullscreenPause", False)
    )
    settings_page.pause_sw.set_valign(Gtk.Align.CENTER)
    r.append(settings_page.pause_sw)

    r = create_row("Disable Mouse", "Ignore mouse interaction.")
    box.append(r)
    settings_page.mouse_sw = Gtk.Switch()
    settings_page.mouse_sw.set_active(settings_page.config.get("disableMouse", False))
    settings_page.mouse_sw.set_valign(Gtk.Align.CENTER)
    r.append(settings_page.mouse_sw)

    r = create_row("Disable Parallax", "Disable background movement with mouse.")
    box.append(r)
    settings_page.parallax_sw = Gtk.Switch()
    settings_page.parallax_sw.set_active(
        settings_page.config.get("disableParallax", False)
    )
    settings_page.parallax_sw.set_valign(Gtk.Align.CENTER)
    r.append(settings_page.parallax_sw)

    r = create_row("Disable Particles", "Turn off fire, rain, and other particles.")
    box.append(r)
    settings_page.particles_sw = Gtk.Switch()
    settings_page.particles_sw.set_active(
        settings_page.config.get("disableParticles", False)
    )
    settings_page.particles_sw.set_valign(Gtk.Align.CENTER)
    r.append(settings_page.particles_sw)

    r = create_row("Clamping Mode", "Texture wrap mode at edges.")
    box.append(r)
    clamp_opts = ["clamp", "border", "repeat"]
    settings_page.clamp_dd = Gtk.DropDown.new_from_strings(clamp_opts)
    curr_clamp = settings_page.config.get("clamping", "clamp")
    if curr_clamp in clamp_opts:
        settings_page.clamp_dd.set_selected(clamp_opts.index(curr_clamp))
    r.append(settings_page.clamp_dd)

    t = Gtk.Label(label="Automation")
    t.add_css_class("settings-section-title")
    t.set_halign(Gtk.Align.START)
    t.set_margin_top(10)
    box.append(t)

    r = create_row(
        "Enable Wallpaper Cycling", "Automatically change wallpapers periodically."
    )
    box.append(r)
    settings_page.cycle_sw = Gtk.Switch()
    settings_page.cycle_sw.set_active(settings_page.config.get("cycleEnabled", False))
    settings_page.cycle_sw.set_valign(Gtk.Align.CENTER)
    r.append(settings_page.cycle_sw)

    r = create_row("Cycle Interval (Minutes)", "Time between wallpaper changes.")
    box.append(r)
    settings_page.cycle_spin = Gtk.SpinButton()
    settings_page.cycle_spin.set_range(1, 1440)
    settings_page.cycle_spin.set_increments(5, 30)
    settings_page.cycle_spin.set_value(settings_page.config.get("cycleInterval", 15))
    r.append(settings_page.cycle_spin)

    r = create_row("Cycle Order", "Order in which wallpapers are cycled.")
    box.append(r)
    order_opts = ["Random", "Title", "Size ↑", "Size ↓", "Type", "ID"]
    settings_page.cycle_order_dd = Gtk.DropDown.new_from_strings(order_opts)

    curr_order = (settings_page.config.get("cycleOrder") or "random").lower()
    idx = 0
    if curr_order == "size":
        curr_order = "size ↑"
    elif curr_order == "size_desc":
        curr_order = "size ↓"

    for i, opt in enumerate(order_opts):
        if opt.lower() == curr_order:
            idx = i
            break
    settings_page.cycle_order_dd.set_selected(idx)
    r.append(settings_page.cycle_order_dd)

    r = create_row("Cycle Playlist", "Limit cycling to a selected playlist.")
    box.append(r)
    cycle_playlist_values: list[str | None] = [None]
    playlist_options = ["All Wallpapers"]
    for p in settings_page.playlists.get_playlists():
        pid = p.get("id")
        name = p.get("name")
        if pid is not None and name is not None:
            cycle_playlist_values.append(str(pid))
            playlist_options.append(str(name))
    settings_page._cycle_playlist_values = cycle_playlist_values
    settings_page.cycle_playlist_dd = Gtk.DropDown.new_from_strings(playlist_options)
    curr_playlist = settings_page.config.get("cyclePlaylistId")
    selected_idx = 0
    for i, pid in enumerate(cycle_playlist_values):
        if pid == curr_playlist:
            selected_idx = i
            break
    settings_page.cycle_playlist_dd.set_selected(selected_idx)
    r.append(settings_page.cycle_playlist_dd)

    t = Gtk.Label(label="Wayland Tweaks")
    t.add_css_class("settings-section-title")
    t.set_halign(Gtk.Align.START)
    t.set_margin_top(10)
    box.append(t)

    is_wayland = os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"

    status_label = "✅ Wayland Session Detected" if is_wayland else "⚠️ X11 Session"
    desc = "Wayland-specific pause strategies."
    if not is_wayland:
        desc += " (Options disabled in X11)"

    r = create_row("Session Check", desc)
    box.append(r)

    lbl_status = Gtk.Label(label=status_label)
    lbl_status.add_css_class("status-value")
    if not is_wayland:
        lbl_status.add_css_class("text-muted")
    r.append(lbl_status)

    r = create_row(
        "Pause Only When Active", "Only pause when fullscreen window is focused."
    )
    box.append(r)
    settings_page.wl_active_sw = Gtk.Switch()
    settings_page.wl_active_sw.set_active(
        settings_page.config.get("wayland_only_active", False)
    )
    settings_page.wl_active_sw.set_valign(Gtk.Align.CENTER)
    if not is_wayland:
        settings_page.wl_active_sw.set_sensitive(False)
    r.append(settings_page.wl_active_sw)

    r = create_row(
        "Ignore App IDs",
        "Comma-separated list of App IDs to ignore (e.g. dock,bar).",
    )
    r.set_orientation(Gtk.Orientation.VERTICAL)
    box.append(r)

    settings_page.wl_ignore_entry = Gtk.Entry()
    settings_page.wl_ignore_entry.set_text(
        settings_page.config.get("wayland_ignore_appids", "")
    )
    settings_page.wl_ignore_entry.set_placeholder_text("app_id1, app_id2")
    if not is_wayland:
        settings_page.wl_ignore_entry.set_sensitive(False)
    r.append(settings_page.wl_ignore_entry)

    return box
