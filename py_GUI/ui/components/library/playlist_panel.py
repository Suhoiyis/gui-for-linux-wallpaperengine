import gi
from typing import Optional, Callable, Any

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk, GLib

from py_GUI.core.playlists import FAVORITES_PLAYLIST_ID


class PlaylistPanel(Gtk.Box):
    """
    Three-state playlist panel: Minimized, Floating, Locked

    States:
    - MINIMIZED: 48px icon column only
    - FLOATING: 220px floating panel with auto-close
    - LOCKED: 220px fixed inline panel
    """

    def __init__(
        self,
        playlists: Any,
        on_playlist_selected: Callable[[Optional[str]], None],
        on_create_playlist: Callable[[], None],
        on_rename_playlist: Callable[[str], None],
        on_delete_playlist: Callable[[str], None],
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.playlists = playlists
        self.on_playlist_selected = on_playlist_selected
        self.on_create_playlist = on_create_playlist
        self.on_rename_playlist = on_rename_playlist
        self.on_delete_playlist = on_delete_playlist

        self._state = "minimized"
        self._selected_playlist_id: Optional[str] = None
        self._hover_timer_id: Optional[int] = None
        self._close_timer_id: Optional[int] = None

        self._state_stack = Gtk.Stack()
        self._state_stack.set_transition_type(Gtk.StackTransitionType.NONE)
        self.append(self._state_stack)

        self._build_icon_column()
        self._build_floating_panel()
        self._build_locked_panel()

        self._state_stack.add_named(self.icon_column, "icon")
        self._state_stack.add_named(self.locked_panel, "locked")

        self.set_state("minimized")

    def _build_icon_column(self):
        self.icon_column = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.icon_column.set_size_request(48, -1)
        self.icon_column.add_css_class("playlist-icon-column")

        header_spacer = Gtk.Box()
        header_spacer.set_size_request(-1, 44)
        self.icon_column.append(header_spacer)

        self.icon_all = Gtk.Button()
        self.icon_all.set_icon_name("emblem-music-symbolic")
        self.icon_all.set_tooltip_text("All Wallpapers")
        self.icon_all.add_css_class("flat")
        self.icon_all.add_css_class("playlist-icon-btn")
        self.icon_all.set_size_request(36, 36)
        self.icon_all.connect("clicked", self._on_icon_clicked, None)
        self.icon_column.append(self.icon_all)

        self.icon_favorites = Gtk.Button()
        self.icon_favorites.set_icon_name("starred-symbolic")
        self.icon_favorites.set_tooltip_text("Favorites")
        self.icon_favorites.add_css_class("flat")
        self.icon_favorites.add_css_class("playlist-icon-btn")
        self.icon_favorites.set_size_request(36, 36)
        self.icon_favorites.connect(
            "clicked", self._on_icon_clicked, FAVORITES_PLAYLIST_ID
        )
        self.icon_column.append(self.icon_favorites)

        self.icon_playlists_container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=4
        )
        self.icon_column.append(self.icon_playlists_container)

        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        self.icon_column.append(spacer)

        btn_new = Gtk.Button()
        btn_new.set_icon_name("list-add-symbolic")
        btn_new.set_tooltip_text("New Playlist")
        btn_new.add_css_class("flat")
        btn_new.add_css_class("playlist-icon-btn")
        btn_new.set_size_request(36, 36)
        btn_new.connect("clicked", lambda _: self.on_create_playlist())
        self.icon_column.append(btn_new)

        hover_controller = Gtk.EventControllerMotion.new()
        hover_controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        hover_controller.connect("enter", self._on_icon_column_enter)
        hover_controller.connect("motion", self._on_icon_column_motion)
        hover_controller.connect("leave", self._on_icon_column_leave)
        self.icon_column.add_controller(hover_controller)

    def _build_floating_panel(self):
        self.floating_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.floating_panel.set_size_request(220, -1)
        self.floating_panel.add_css_class("card")
        self.floating_panel.add_css_class("playlist-floating-panel")

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.set_margin_top(8)
        header.set_margin_start(8)
        header.set_margin_end(8)

        title = Gtk.Label(label="Playlists")
        title.add_css_class("heading")
        title.set_halign(Gtk.Align.START)
        title.set_hexpand(True)
        header.append(title)

        self.btn_pin_floating = Gtk.Button()
        self.btn_pin_floating.set_icon_name("view-pin-symbolic")
        self.btn_pin_floating.set_tooltip_text("Pin panel")
        self.btn_pin_floating.add_css_class("flat")
        self.btn_pin_floating.connect("clicked", self._on_pin_clicked)
        header.append(self.btn_pin_floating)

        self.floating_panel.append(header)

        self.floating_list = Gtk.ListBox()
        self.floating_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.floating_list.connect("row-selected", self._on_playlist_selected)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_child(self.floating_list)
        self.floating_panel.append(scroll)

        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        footer.set_margin_start(8)
        footer.set_margin_end(8)
        footer.set_margin_bottom(8)

        btn_new = Gtk.Button(label="New")
        btn_new.add_css_class("action-btn")
        btn_new.add_css_class("secondary")
        btn_new.connect("clicked", lambda _: self.on_create_playlist())
        footer.append(btn_new)

        btn_rename = Gtk.Button(label="Rename")
        btn_rename.add_css_class("action-btn")
        btn_rename.add_css_class("secondary")
        btn_rename.connect("clicked", self._on_rename_clicked)
        footer.append(btn_rename)

        btn_delete = Gtk.Button(label="Delete")
        btn_delete.add_css_class("action-btn")
        btn_delete.add_css_class("danger")
        btn_delete.connect("clicked", self._on_delete_clicked)
        footer.append(btn_delete)

        self.floating_panel.append(footer)

        hover_controller = Gtk.EventControllerMotion.new()
        hover_controller.connect("enter", self._on_floating_enter)
        hover_controller.connect("leave", self._on_floating_leave)
        self.floating_panel.add_controller(hover_controller)

        self.floating_panel_popover = Gtk.Popover()
        self.floating_panel_popover.set_has_arrow(False)
        self.floating_panel_popover.set_autohide(False)
        self.floating_panel_popover.set_child(self.floating_panel)
        self.floating_panel_popover.set_parent(self.icon_column)

    def _build_locked_panel(self):
        self.locked_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.locked_panel.set_size_request(220, -1)
        self.locked_panel.add_css_class("card")
        self.locked_panel.add_css_class("playlist-locked-panel")

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.set_margin_top(8)
        header.set_margin_start(8)
        header.set_margin_end(8)

        title = Gtk.Label(label="Playlists")
        title.add_css_class("heading")
        title.set_halign(Gtk.Align.START)
        title.set_hexpand(True)
        header.append(title)

        self.btn_unpin_locked = Gtk.Button()
        self.btn_unpin_locked.set_icon_name("view-pin-symbolic")
        self.btn_unpin_locked.set_tooltip_text("Unpin panel")
        self.btn_unpin_locked.add_css_class("flat")
        self.btn_unpin_locked.connect("clicked", self._on_unpin_clicked)
        header.append(self.btn_unpin_locked)

        self.locked_panel.append(header)

        self.locked_list = Gtk.ListBox()
        self.locked_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.locked_list.connect("row-selected", self._on_playlist_selected)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_child(self.locked_list)
        self.locked_panel.append(scroll)

        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        footer.set_margin_start(8)
        footer.set_margin_end(8)
        footer.set_margin_bottom(8)

        btn_new = Gtk.Button(label="New")
        btn_new.add_css_class("action-btn")
        btn_new.add_css_class("secondary")
        btn_new.connect("clicked", lambda _: self.on_create_playlist())
        footer.append(btn_new)

        btn_rename = Gtk.Button(label="Rename")
        btn_rename.add_css_class("action-btn")
        btn_rename.add_css_class("secondary")
        btn_rename.connect("clicked", self._on_rename_clicked)
        footer.append(btn_rename)

        btn_delete = Gtk.Button(label="Delete")
        btn_delete.add_css_class("action-btn")
        btn_delete.add_css_class("danger")
        btn_delete.connect("clicked", self._on_delete_clicked)
        footer.append(btn_delete)

        self.locked_panel.append(footer)

        self.locked_panel.set_visible(True)

    def set_state(self, state: str):
        self._state = state

        if state == "minimized":
            self._state_stack.set_visible_child_name("icon")
            if hasattr(self, "floating_panel_popover"):
                self.floating_panel_popover.popdown()
        elif state == "floating":
            self._state_stack.set_visible_child_name("icon")
            if hasattr(self, "floating_panel_popover"):
                self.floating_panel_popover.popup()
        elif state == "locked":
            self._state_stack.set_visible_child_name("locked")
            if hasattr(self, "floating_panel_popover"):
                self.floating_panel_popover.popdown()

    def get_state(self) -> str:
        return self._state

    def refresh(self):
        self._populate_icon_column()
        self._populate_list(self.floating_list)
        self._populate_list(self.locked_list)

    def _populate_icon_column(self):
        while True:
            child = self.icon_playlists_container.get_first_child()
            if child is None:
                break
            self.icon_playlists_container.remove(child)

        for playlist in self.playlists.get_playlists():
            pid = playlist.get("id")
            if pid == FAVORITES_PLAYLIST_ID:
                continue

            btn = Gtk.Button()
            btn.set_icon_name("folder-music-symbolic")
            btn.set_tooltip_text(playlist.get("name", "Unnamed"))
            btn.add_css_class("flat")
            btn.add_css_class("playlist-icon-btn")
            btn.set_size_request(36, 36)
            btn.connect("clicked", self._on_icon_clicked, pid)
            self.icon_playlists_container.append(btn)

    def _populate_list(self, listbox: Gtk.ListBox):
        while True:
            child = listbox.get_first_child()
            if child is None:
                break
            listbox.remove(child)

        row_all = Gtk.ListBoxRow()
        row_all_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row_all_box.set_size_request(-1, 36)
        row_all_box.set_margin_top(6)
        row_all_box.set_margin_bottom(6)
        row_all_box.set_margin_start(8)
        row_all_box.set_margin_end(8)
        row_all_box.append(Gtk.Label(label="All Wallpapers", xalign=0))
        row_all.set_child(row_all_box)
        row_all._playlist_id = None
        listbox.append(row_all)

        for playlist in self.playlists.get_playlists():
            pid = playlist.get("id")
            name = playlist.get("name", "Unnamed")

            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            box.set_size_request(-1, 36)
            box.set_margin_top(6)
            box.set_margin_bottom(6)
            box.set_margin_start(8)
            box.set_margin_end(8)

            lbl = Gtk.Label(label=name)
            lbl.set_halign(Gtk.Align.START)
            lbl.set_hexpand(True)
            box.append(lbl)

            row.set_child(box)
            row._playlist_id = pid
            listbox.append(row)

        self._select_current(listbox)

    def _select_current(self, listbox: Gtk.ListBox):
        idx = 0
        while True:
            row = listbox.get_row_at_index(idx)
            if row is None:
                break
            if getattr(row, "_playlist_id", None) == self._selected_playlist_id:
                listbox.select_row(row)
                break
            idx += 1

    def select_playlist(self, playlist_id: Optional[str]):
        self._selected_playlist_id = playlist_id
        self._select_current(self.floating_list)
        self._select_current(self.locked_list)

    def _on_icon_clicked(self, btn, playlist_id: Optional[str]):
        self.select_playlist(playlist_id)
        self.on_playlist_selected(playlist_id)

        if self._state == "minimized":
            self.set_state("floating")

    def _on_playlist_selected(self, listbox, row):
        if row is None:
            return
        playlist_id = getattr(row, "_playlist_id", None)
        self._selected_playlist_id = playlist_id
        self.on_playlist_selected(playlist_id)

    def _on_icon_column_enter(self, controller, x, y):
        if self._state == "minimized":
            if self._hover_timer_id is not None:
                GLib.source_remove(self._hover_timer_id)
            self._hover_timer_id = GLib.timeout_add(300, self._on_hover_timeout)

    def _on_icon_column_motion(self, controller, x, y):
        if self._state == "minimized" and self._hover_timer_id is None:
            self._hover_timer_id = GLib.timeout_add(300, self._on_hover_timeout)

    def _on_icon_column_leave(self, controller):
        if self._hover_timer_id:
            GLib.source_remove(self._hover_timer_id)
            self._hover_timer_id = None
        if self._state == "floating":
            if self._close_timer_id is not None:
                GLib.source_remove(self._close_timer_id)
            self._close_timer_id = GLib.timeout_add(500, self._on_close_timeout)

    def _on_hover_timeout(self):
        self._hover_timer_id = None
        if self._state == "minimized":
            self.set_state("floating")
        return False

    def _on_floating_enter(self, controller, x, y):
        if self._close_timer_id:
            GLib.source_remove(self._close_timer_id)
            self._close_timer_id = None

    def _on_floating_leave(self, controller):
        if self._state == "floating":
            if self._close_timer_id is not None:
                GLib.source_remove(self._close_timer_id)
            self._close_timer_id = GLib.timeout_add(500, self._on_close_timeout)

    def _on_close_timeout(self):
        self._close_timer_id = None
        if self._state == "floating":
            self.set_state("minimized")
        return False

    def _on_pin_clicked(self, btn):
        self.set_state("locked")

    def _on_unpin_clicked(self, btn):
        self.set_state("minimized")

    def _on_rename_clicked(self, btn):
        if self._selected_playlist_id:
            self.on_rename_playlist(self._selected_playlist_id)

    def _on_delete_clicked(self, btn):
        if self._selected_playlist_id:
            self.on_delete_playlist(self._selected_playlist_id)
