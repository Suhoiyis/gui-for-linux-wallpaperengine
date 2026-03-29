import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GLib


class CommandPalette(Gtk.Window):
    def __init__(self, parent, items_provider, on_execute):
        super().__init__(transient_for=parent, modal=True)
        self.items_provider = items_provider
        self.on_execute = on_execute
        self.filtered_items = []

        self.set_title("Command Palette")
        self.set_default_size(640, 520)
        self.set_resizable(False)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        root.set_margin_top(12)
        root.set_margin_bottom(12)
        root.set_margin_start(12)
        root.set_margin_end(12)
        self.set_child(root)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text(
            "Search wallpapers, playlists, history, actions..."
        )
        self.entry.connect("changed", self.on_query_changed)
        self.entry.connect("activate", self.on_entry_activate)
        root.append(self.entry)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-activated", self.on_row_activated)
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroller.set_vexpand(True)
        scroller.set_child(self.listbox)
        root.append(scroller)

        key_ctrl = Gtk.EventControllerKey.new()
        key_ctrl.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_ctrl)

        self.refresh_items("")

    def present_with_focus(self):
        self.present()
        GLib.idle_add(lambda: self.entry.grab_focus() or False)

    def refresh_items(self, query: str):
        while True:
            child = self.listbox.get_first_child()
            if child is None:
                break
            self.listbox.remove(child)

        all_items = self.items_provider()
        q = query.strip().lower()
        if not q:
            self.filtered_items = all_items
        else:
            out = []
            for item in all_items:
                label = str(item.get("label", "")).lower()
                keywords = str(item.get("keywords", "")).lower()
                if q in label or q in keywords:
                    out.append(item)
            self.filtered_items = out

        for item in self.filtered_items:
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            box.set_margin_top(6)
            box.set_margin_bottom(6)
            box.set_margin_start(8)
            box.set_margin_end(8)
            label = Gtk.Label(label=str(item.get("label", "")))
            label.set_halign(Gtk.Align.START)
            label.set_hexpand(True)
            box.append(label)
            group = item.get("group")
            if group:
                tag = Gtk.Label(label=str(group))
                tag.add_css_class("dim-label")
                box.append(tag)
            row.set_child(box)
            row._palette_item = item
            self.listbox.append(row)

        first_row = self.listbox.get_row_at_index(0)
        if first_row:
            self.listbox.select_row(first_row)

    def execute_selected(self):
        row = self.listbox.get_selected_row()
        if not row:
            return
        item = getattr(row, "_palette_item", None)
        if not item:
            return
        self.on_execute(item)
        self.destroy()

    def on_query_changed(self, entry):
        self.refresh_items(entry.get_text())

    def on_entry_activate(self, entry):
        self.execute_selected()

    def on_row_activated(self, listbox, row):
        self.execute_selected()

    def on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.destroy()
            return True
        if keyval == Gdk.KEY_Down:
            row = self.listbox.get_selected_row()
            idx = row.get_index() if row else -1
            nxt = self.listbox.get_row_at_index(idx + 1)
            if nxt:
                self.listbox.select_row(nxt)
            return True
        if keyval == Gdk.KEY_Up:
            row = self.listbox.get_selected_row()
            idx = row.get_index() if row else 0
            prev = self.listbox.get_row_at_index(max(0, idx - 1))
            if prev:
                self.listbox.select_row(prev)
            return True
        if keyval == Gdk.KEY_Return:
            self.execute_selected()
            return True
        return False
