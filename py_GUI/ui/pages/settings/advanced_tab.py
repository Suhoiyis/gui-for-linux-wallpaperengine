# pyright: reportAttributeAccessIssue=false

import shutil

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, GLib, Adw

from py_GUI.const import WORKSHOP_PATH

from .shared import create_row, make_tab_scrolled_container


def build_advanced_tab(settings_page) -> Gtk.Widget:
    box = make_tab_scrolled_container(settings_page.stack, "advanced")

    t = Gtk.Label(label="Advanced")
    t.add_css_class("settings-section-title")
    t.set_halign(Gtk.Align.START)
    box.append(t)

    r = create_row("Workshop Directory", "Path to Steam Workshop content (431960).")
    r.set_orientation(Gtk.Orientation.VERTICAL)
    box.append(r)

    workshop_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    settings_page.path_entry = Gtk.Entry()
    settings_page.path_entry.set_text(
        settings_page.config.get("workshopPath") or WORKSHOP_PATH
    )
    settings_page.path_entry.set_hexpand(True)
    workshop_box.append(settings_page.path_entry)

    browse_workshop_btn = Gtk.Button(label="Browse")
    browse_workshop_btn.add_css_class("action-btn")
    browse_workshop_btn.add_css_class("secondary")
    browse_workshop_btn.connect("clicked", settings_page.on_browse_workshop)
    workshop_box.append(browse_workshop_btn)
    r.append(workshop_box)

    r = create_row(
        "Assets Directory",
        "Wallpaper Engine assets folder (leave empty for auto-detect).",
    )
    r.set_orientation(Gtk.Orientation.VERTICAL)
    box.append(r)

    assets_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    settings_page.assets_entry = Gtk.Entry()
    assets_path = settings_page.config.get("assetsPath", None)
    settings_page.assets_entry.set_text(assets_path if assets_path else "")
    settings_page.assets_entry.set_placeholder_text(
        "Auto-detect from Steam installation"
    )
    settings_page.assets_entry.set_hexpand(True)
    assets_box.append(settings_page.assets_entry)

    browse_assets_btn = Gtk.Button(label="Browse")
    browse_assets_btn.add_css_class("action-btn")
    browse_assets_btn.add_css_class("secondary")
    browse_assets_btn.connect("clicked", settings_page.on_browse_assets)
    assets_box.append(browse_assets_btn)
    r.append(assets_box)

    r = create_row("Screen Root", "Select a monitor.")
    box.append(r)

    screens = settings_page.screen_manager.get_screens()
    curr_screen = (
        settings_page.controller.state.get_last_screen()
        or settings_page.screen_manager.get_primary_screen()
        or settings_page.screen_manager.get_first_screen()
        or "eDP-1"
    )
    if curr_screen not in screens:
        screens = screens + [curr_screen]

    settings_page.screen_dd = Gtk.DropDown.new_from_strings(screens)
    settings_page.screen_dd.set_hexpand(True)
    if curr_screen and curr_screen in screens:
        settings_page.screen_dd.set_selected(screens.index(str(curr_screen)))
    r.append(settings_page.screen_dd)

    btn = Gtk.Button()
    content = Adw.ButtonContent()
    content.set_icon_name("view-refresh-symbolic")
    content.set_label("Refresh Screens")
    btn.set_child(content)

    btn.add_css_class("action-btn")
    btn.add_css_class("secondary")
    btn.connect("clicked", settings_page.on_refresh_screens)
    box.append(btn)

    t = Gtk.Label(label="System Integration")
    t.add_css_class("settings-section-title")
    t.set_halign(Gtk.Align.START)
    t.set_margin_top(10)
    box.append(t)

    r = create_row("Desktop Shortcut", "Create app icon in system menu.")
    box.append(r)
    settings_page.btn_create_desktop = Gtk.Button(label="Create")
    settings_page.btn_create_desktop.set_valign(Gtk.Align.CENTER)
    settings_page.btn_create_desktop.connect(
        "clicked", settings_page.on_create_desktop_entry
    )
    r.append(settings_page.btn_create_desktop)

    r = create_row("Run on Startup", "Launch automatically on login.")
    box.append(r)
    settings_page.autostart_sw = Gtk.Switch()
    settings_page.autostart_sw.set_active(
        settings_page.integrator.is_autostart_enabled()
    )
    settings_page.autostart_sw.set_valign(Gtk.Align.CENTER)
    r.append(settings_page.autostart_sw)

    r = create_row("Start Hidden", "Start in tray without showing window.")
    box.append(r)
    settings_page.start_hidden_sw = Gtk.Switch()
    settings_page.start_hidden_sw.set_active(True)
    settings_page.start_hidden_sw.set_valign(Gtk.Align.CENTER)
    r.append(settings_page.start_hidden_sw)

    t_ss = Gtk.Label(label="Screenshot")
    t_ss.add_css_class("settings-section-title")
    t_ss.set_halign(Gtk.Align.START)
    t_ss.set_margin_top(10)
    box.append(t_ss)

    r = create_row(
        "Screenshot Delay",
        "Frames to wait before capture (use higher for web wallpapers).",
    )
    box.append(r)
    settings_page.screenshot_delay_spin = Gtk.SpinButton()
    settings_page.screenshot_delay_spin.set_range(1, 600)
    settings_page.screenshot_delay_spin.set_increments(5, 50)
    settings_page.screenshot_delay_spin.set_value(
        settings_page.config.get("screenshotDelay", 20)
    )
    r.append(settings_page.screenshot_delay_spin)

    r = create_row(
        "Screenshot Resolution", "Target resolution (e.g. 1920x1080, 3840x2160)."
    )
    box.append(r)
    settings_page.screenshot_res_entry = Gtk.Entry()
    settings_page.screenshot_res_entry.set_text(
        settings_page.config.get("screenshotRes") or "3840x2160"
    )
    settings_page.screenshot_res_entry.set_hexpand(False)
    settings_page.screenshot_res_entry.set_width_chars(15)
    r.append(settings_page.screenshot_res_entry)

    has_xvfb = shutil.which("xvfb-run") is not None

    status_label = (
        "✅ Xvfb Installed (Silent Mode)"
        if has_xvfb
        else "⚠️ Xvfb Not Found (Window Mode)"
    )
    status_desc = "Silent capture using virtual framebuffer."

    r = create_row("Capture Backend", status_desc)
    box.append(r)

    status_val = Gtk.Label(label=status_label)
    status_val.add_css_class("status-value")
    if not has_xvfb:
        status_val.add_css_class("text-muted")

    r.append(status_val)

    r = create_row(
        "Prefer Silent Capture", "Use Xvfb if installed to avoid popup windows."
    )
    box.append(r)
    settings_page.xvfb_sw = Gtk.Switch()
    settings_page.xvfb_sw.set_active(settings_page.config.get("preferXvfb", True))
    settings_page.xvfb_sw.set_valign(Gtk.Align.CENTER)
    if not has_xvfb:
        settings_page.xvfb_sw.set_tooltip_text("Xvfb is not installed on this system.")
    r.append(settings_page.xvfb_sw)

    return box


def on_browse_workshop(settings_page, _btn):
    dialog = Gtk.FileDialog()
    dialog.set_title("Select Workshop Directory")
    dialog.select_folder(
        settings_page.get_root(), None, settings_page._on_workshop_folder_selected
    )


def _on_workshop_folder_selected(settings_page, dialog, result):
    try:
        folder = dialog.select_folder_finish(result)
        if folder:
            path = folder.get_path()
            settings_page.path_entry.set_text(path)
    except GLib.Error:
        pass


def on_browse_assets(settings_page, _btn):
    dialog = Gtk.FileDialog()
    dialog.set_title("Select Assets Directory")
    dialog.select_folder(
        settings_page.get_root(), None, settings_page._on_assets_folder_selected
    )


def _on_assets_folder_selected(settings_page, dialog, result):
    try:
        folder = dialog.select_folder_finish(result)
        if folder:
            path = folder.get_path()
            settings_page.assets_entry.set_text(path)
    except GLib.Error:
        pass


def on_create_desktop_entry(settings_page, _btn):
    success, msg = settings_page.integrator.create_desktop_entry()
    if success:
        settings_page.show_toast("Desktop entry created successfully")
    else:
        settings_page.show_toast(f"Failed to create desktop entry: {msg}")


def on_refresh_screens(settings_page, _btn):
    screens = settings_page.screen_manager.get_screens()

    selected = settings_page.screen_dd.get_selected_item()
    selected_str = selected.get_string() if selected else None

    settings_page.screen_dd.set_model(Gtk.StringList.new(screens))

    if selected_str and selected_str in screens:
        settings_page.screen_dd.set_selected(screens.index(selected_str))
    elif screens:
        settings_page.screen_dd.set_selected(0)

    settings_page.show_toast(f"Screens refreshed: {', '.join(screens)}")
