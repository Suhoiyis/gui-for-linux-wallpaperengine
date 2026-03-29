# pyright: reportAttributeAccessIssue=false

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


SECTION_MARGIN_TOP = 60
SECTION_MARGIN_BOTTOM = 60
SECTION_MARGIN_START = 40
SECTION_MARGIN_END = 40


def create_row(label, desc):
    row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    row.add_css_class("setting-row")

    info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
    info.set_hexpand(True)
    row.append(info)

    l = Gtk.Label(label=label)
    l.add_css_class("setting-label")
    l.set_halign(Gtk.Align.START)
    info.append(l)

    d = Gtk.Label(label=desc)
    d.add_css_class("setting-desc")
    d.set_halign(Gtk.Align.START)
    d.set_wrap(True)
    d.set_max_width_chars(50)
    info.append(d)

    return row


def make_tab_scrolled_container(stack, name):
    scroll = Gtk.ScrolledWindow()
    scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    scroll.set_vexpand(True)
    stack.add_named(scroll, name)

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    box.set_margin_top(SECTION_MARGIN_TOP)
    box.set_margin_bottom(SECTION_MARGIN_BOTTOM)
    box.set_margin_start(SECTION_MARGIN_START)
    box.set_margin_end(SECTION_MARGIN_END)
    scroll.set_child(box)

    return box
