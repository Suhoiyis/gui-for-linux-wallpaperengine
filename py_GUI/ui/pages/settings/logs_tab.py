# pyright: reportAttributeAccessIssue=false

import os
import subprocess

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gdk

from py_GUI.const import CONFIG_DIR


def build_logs_tab(settings_page) -> Gtk.Widget:
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    box.set_margin_top(60)
    box.set_margin_bottom(60)
    box.set_margin_start(40)
    box.set_margin_end(40)
    settings_page.stack.add_named(box, "logs")

    header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    box.append(header_box)

    t = Gtk.Label(label="Logs")
    t.add_css_class("settings-section-title")
    t.set_halign(Gtk.Align.START)
    t.set_hexpand(True)
    header_box.append(t)

    filter_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    filter_box.set_valign(Gtk.Align.CENTER)
    header_box.append(filter_box)

    source_opts = ["All", "Controller", "Engine", "GUI"]
    settings_page.source_filter_dd = Gtk.DropDown.new_from_strings(source_opts)
    settings_page.source_filter_dd.set_valign(Gtk.Align.CENTER)
    settings_page.source_filter_dd.connect(
        "notify::selected", settings_page.on_filter_changed
    )
    filter_box.append(settings_page.source_filter_dd)

    level_opts = ["All Levels", "Debug", "Info", "Warning", "Error"]
    settings_page.level_filter_dd = Gtk.DropDown.new_from_strings(level_opts)
    settings_page.level_filter_dd.set_valign(Gtk.Align.CENTER)
    settings_page.level_filter_dd.connect(
        "notify::selected", settings_page.on_level_filter_changed
    )
    filter_box.append(settings_page.level_filter_dd)

    scroll = Gtk.ScrolledWindow()
    scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    scroll.set_vexpand(True)
    box.append(scroll)

    settings_page.log_view = Gtk.TextView()
    settings_page.log_view.set_editable(False)
    settings_page.log_view.set_cursor_visible(False)
    settings_page.log_view.set_monospace(True)
    settings_page.log_view.set_left_margin(8)
    settings_page.log_view.set_right_margin(8)
    scroll.set_child(settings_page.log_view)

    settings_page.log_buffer = settings_page.log_view.get_buffer()
    settings_page.setup_log_tags()

    entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    entry_box.set_margin_top(8)
    box.append(entry_box)

    settings_page.entry_count_lbl = Gtk.Label(label="0 entries")
    settings_page.entry_count_lbl.set_halign(Gtk.Align.START)
    settings_page.entry_count_lbl.add_css_class("dim-label")
    settings_page.entry_count_lbl.add_css_class("caption")
    entry_box.append(settings_page.entry_count_lbl)

    btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    btns.set_halign(Gtk.Align.END)
    btns.set_hexpand(True)
    entry_box.append(btns)

    clr_btn = Gtk.Button(label="Clear Logs")
    clr_btn.add_css_class("action-btn")
    clr_btn.add_css_class("secondary")
    clr_btn.connect("clicked", lambda _: settings_page.clear_logs())
    btns.append(clr_btn)

    copy_btn = Gtk.Button(label="Copy Logs")
    copy_btn.add_css_class("action-btn")
    copy_btn.add_css_class("secondary")
    copy_btn.connect("clicked", settings_page.copy_logs)
    btns.append(copy_btn)

    engine_btn = Gtk.Button(label="Open Engine Log")
    engine_btn.add_css_class("action-btn")
    engine_btn.add_css_class("secondary")
    engine_btn.connect("clicked", settings_page.open_engine_log)
    btns.append(engine_btn)

    ref_btn = Gtk.Button(label="Refresh")
    ref_btn.add_css_class("action-btn")
    ref_btn.add_css_class("primary")
    ref_btn.connect("clicked", lambda _: settings_page.refresh_logs())
    btns.append(ref_btn)

    settings_page.log_manager.register_callback(settings_page.on_log_update)
    settings_page.refresh_logs()

    return box


def on_filter_changed(settings_page, dd, _pspec):
    selected = dd.get_selected_item()
    if selected:
        settings_page.current_filter = selected.get_string()
        settings_page.refresh_logs()


def on_level_filter_changed(settings_page, dd, _pspec):
    selected = dd.get_selected_item()
    if selected:
        settings_page.current_level_filter = selected.get_string()
        settings_page.refresh_logs()


def setup_log_tags(settings_page):
    tbl = settings_page.log_buffer.get_tag_table()

    def add_tag(name, color):
        tag = Gtk.TextTag(name=name)
        tag.set_property("foreground", color)
        tag.set_property("size-points", 12)
        tbl.add(tag)

    add_tag("timestamp", "#6b7280")
    add_tag("debug", "#6b7280")
    add_tag("info", "#3b82f6")
    add_tag("warning", "#f59e0b")
    add_tag("error", "#ef4444")
    add_tag("source", "#a855f7")

    msg_tag = Gtk.TextTag(name="message")
    msg_tag.set_property("foreground", "#e5e7eb")
    msg_tag.set_property("size-points", 12)
    tbl.add(msg_tag)

    line_tag = Gtk.TextTag(name="line")
    line_tag.set_property("pixels-above-lines", 8)
    tbl.add(line_tag)


def on_log_update(settings_page, entry):
    GLib.idle_add(lambda: settings_page.append_log(entry))


def append_log(settings_page, entry):
    ts = entry.get("timestamp", "")
    lvl = entry.get("level", "")
    src = entry.get("source", "")
    msg = entry.get("message", "")

    if settings_page.current_filter != "All":
        if settings_page.current_filter == "GUI":
            if src in ["Controller", "Engine"]:
                return
        elif src != settings_page.current_filter:
            return

    if settings_page.current_level_filter != "All Levels":
        filter_lvl = settings_page.current_level_filter.upper()
        if lvl != filter_lvl:
            return

    settings_page.visible_entries_count += 1
    settings_page.entry_count_lbl.set_label(
        f"{settings_page.visible_entries_count} entries"
    )

    end = settings_page.log_buffer.get_end_iter()

    settings_page.log_buffer.insert_with_tags_by_name(end, f"[{ts}] ", "timestamp")

    lvl_tag = "debug"
    if lvl == "INFO":
        lvl_tag = "info"
    elif lvl == "WARNING":
        lvl_tag = "warning"
    elif lvl == "ERROR":
        lvl_tag = "error"

    settings_page.log_buffer.insert_with_tags_by_name(end, f"[{lvl}] ", lvl_tag)
    settings_page.log_buffer.insert_with_tags_by_name(end, f"[{src}] ", "source")
    settings_page.log_buffer.insert_with_tags_by_name(
        end, f"{msg}\n", "message", "line"
    )

    settings_page.log_view.scroll_to_mark(
        settings_page.log_buffer.create_mark(
            "end", settings_page.log_buffer.get_end_iter(), False
        ),
        0.0,
        False,
        0.0,
        0.0,
    )


def refresh_logs(settings_page):
    settings_page.visible_entries_count = 0
    settings_page.log_buffer.set_text("")
    for entry in settings_page.log_manager.get_logs():
        settings_page.append_log(entry)
    settings_page.entry_count_lbl.set_label(
        f"{settings_page.visible_entries_count} entries"
    )


def clear_logs(settings_page):
    settings_page.log_manager.clear()
    settings_page.log_buffer.set_text("")


def copy_logs(settings_page, btn):
    start = settings_page.log_buffer.get_start_iter()
    end = settings_page.log_buffer.get_end_iter()
    text = settings_page.log_buffer.get_text(start, end, False)
    clipboard = Gdk.Display.get_default().get_clipboard()
    clipboard.set(text)

    orig = btn.get_label()
    btn.set_label("Copied!")
    GLib.timeout_add(2000, lambda: btn.set_label(orig) and False)


def open_engine_log(settings_page, _btn):
    log_path = os.path.join(CONFIG_DIR, "engine_last.log")
    if not os.path.exists(log_path):
        settings_page.show_toast("engine_last.log not found")
        return

    try:
        subprocess.Popen(["xdg-open", log_path])
    except Exception as e:
        settings_page.show_toast(f"Failed to open log: {e}")
