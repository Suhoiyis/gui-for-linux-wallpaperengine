import gi
from typing import Optional, Callable

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw


class EmptyState(Gtk.Box):
    """
    A reusable empty state component for displaying when no data is available.

    Features:
    - Icon display
    - Title and description
    - Optional action button
    - Consistent styling across the app
    """

    def __init__(
        self,
        icon_name: str,
        title: str,
        description: Optional[str] = None,
        action_label: Optional[str] = None,
        on_action: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12, **kwargs)

        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.set_margin_top(48)
        self.set_margin_bottom(48)
        self.set_margin_start(32)
        self.set_margin_end(32)

        # Icon
        self.icon = Gtk.Image.new_from_icon_name(icon_name)
        self.icon.set_pixel_size(64)
        self.icon.add_css_class("dim-label")
        self.append(self.icon)

        # Title
        self.title_label = Gtk.Label(label=title)
        self.title_label.add_css_class("title-2")
        self.title_label.set_wrap(True)
        self.title_label.set_max_width_chars(40)
        self.title_label.set_justify(Gtk.Justification.CENTER)
        self.append(self.title_label)

        # Description (optional)
        if description:
            self.desc_label = Gtk.Label(label=description)
            self.desc_label.add_css_class("body")
            self.desc_label.add_css_class("dim-label")
            self.desc_label.set_wrap(True)
            self.desc_label.set_max_width_chars(50)
            self.desc_label.set_justify(Gtk.Justification.CENTER)
            self.append(self.desc_label)

        # Action button (optional)
        if action_label and on_action:
            self.action_btn = Gtk.Button(label=action_label)
            self.action_btn.add_css_class("suggested-action")
            self.action_btn.set_margin_top(8)
            self.action_btn.connect("clicked", lambda btn: on_action())
            self.append(self.action_btn)

    def set_icon_name(self, icon_name: str):
        """Update the icon."""
        self.icon.set_from_icon_name(icon_name)

    def set_title(self, title: str):
        """Update the title."""
        self.title_label.set_label(title)

    def set_description(self, description: str):
        """Update or set the description."""
        if hasattr(self, "desc_label"):
            self.desc_label.set_label(description)
        else:
            self.desc_label = Gtk.Label(label=description)
            self.desc_label.add_css_class("body")
            self.desc_label.add_css_class("dim-label")
            self.desc_label.set_wrap(True)
            self.desc_label.set_max_width_chars(50)
            self.desc_label.set_justify(Gtk.Justification.CENTER)
            # Insert before action button if it exists
            if hasattr(self, "action_btn"):
                self.insert_child_after(self.desc_label, self.title_label)
            else:
                self.append(self.desc_label)


class LibraryEmptyState(EmptyState):
    """Empty state specifically for the library page."""

    def __init__(
        self,
        scenario: str = "default",
        on_clear_search: Optional[Callable] = None,
        **kwargs,
    ):
        """
        Args:
            scenario: One of "default", "search", "playlist", "favorites"
            on_clear_search: Callback for clear search action
        """
        configs = {
            "default": {
                "icon_name": "folder-open-symbolic",
                "title": "No Wallpapers Found",
                "description": "Your library is empty. Configure the workshop path to get started.",
                "action_label": "Open Settings",
            },
            "search": {
                "icon_name": "edit-find-symbolic",
                "title": "No Results Found",
                "description": "No wallpapers match your search criteria.",
                "action_label": "Clear Search",
            },
            "playlist": {
                "icon_name": "view-list-symbolic",
                "title": "Playlist is Empty",
                "description": "This playlist doesn't have any wallpapers yet.",
                "action_label": None,
            },
            "favorites": {
                "icon_name": "starred-symbolic",
                "title": "No Favorites Yet",
                "description": "Click the star icon on wallpapers to add them to favorites.",
                "action_label": None,
            },
        }

        config = configs.get(scenario, configs["default"])

        # Set up action callback based on scenario
        action_callback = None
        if config.get("action_label"):
            if scenario == "search" and on_clear_search:
                action_callback = on_clear_search
            elif scenario == "default":
                # Will be set by parent
                action_callback = lambda: None

        super().__init__(
            icon_name=config["icon_name"],
            title=config["title"],
            description=config["description"],
            action_label=config.get("action_label"),
            on_action=action_callback,
            **kwargs,
        )

        self.scenario = scenario
        self._on_settings_callback = None

    def set_settings_callback(self, callback: Callable):
        """Set the callback for opening settings (for default scenario)."""
        self._on_settings_callback = callback
        if self.scenario == "default" and hasattr(self, "action_btn"):
            # Reconnect the button
            for handler_id in self.action_btn.list_handlers():
                self.action_btn.disconnect(handler_id)
            self.action_btn.connect("clicked", lambda btn: callback())
