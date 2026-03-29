import gi
from gi.repository import Gtk, GLib


class SkeletonBlock(Gtk.Box):
    """A skeleton placeholder block with pulse animation."""

    def __init__(self, width: int = 170, height: int = 170, **kwargs):
        super().__init__(**kwargs)
        self._width = width
        self._height = height
        self._pulse_id = None
        self._pulse_direction = 1
        self._current_opacity = 0.55

        self.set_size_request(width, height)
        self.add_css_class("skeleton-block")
        self.set_opacity(self._current_opacity)

        self._start_pulse()

    def _start_pulse(self):
        """Start the pulse animation using GLib timeout."""
        self._pulse_id = GLib.timeout_add(100, self._on_pulse_tick)

    def _on_pulse_tick(self) -> bool:
        """Update opacity for pulse effect."""
        if not self.get_parent():
            return False

        self._current_opacity += 0.05 * self._pulse_direction

        if self._current_opacity >= 0.9:
            self._current_opacity = 0.9
            self._pulse_direction = -1
        elif self._current_opacity <= 0.55:
            self._current_opacity = 0.55
            self._pulse_direction = 1

        self.set_opacity(self._current_opacity)
        return True

    def stop_pulse(self):
        """Stop the pulse animation."""
        if self._pulse_id:
            GLib.source_remove(self._pulse_id)
            self._pulse_id = None

    def do_unroot(self):
        """Clean up when widget is removed from hierarchy."""
        self.stop_pulse()
        super().do_unroot()


class SkeletonCard(Gtk.Box):
    """A skeleton card matching wallpaper card dimensions."""

    def __init__(self, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8, **kwargs)

        # Image placeholder
        self.image_skeleton = SkeletonBlock(170, 170)
        self.image_skeleton.add_css_class("card")
        self.append(self.image_skeleton)

        # Text placeholder
        self.text_skeleton = SkeletonBlock(120, 20)
        self.text_skeleton.set_halign(Gtk.Align.CENTER)
        self.append(self.text_skeleton)


class SkeletonGrid(Gtk.Box):
    """A grid of skeleton cards for loading state."""

    def __init__(self, count: int = 12, **kwargs):
        super().__init__(**kwargs)
        self._skeletons = []

        # Create flowbox-like layout
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.set_homogeneous(True)
        self.flowbox.set_max_children_per_line(4)
        self.flowbox.set_min_children_per_line(2)
        self.flowbox.set_column_spacing(16)
        self.flowbox.set_row_spacing(16)
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_halign(Gtk.Align.CENTER)

        for _ in range(count):
            skeleton = SkeletonCard()
            skeleton.set_margin_top(8)
            skeleton.set_margin_bottom(8)
            skeleton.set_margin_start(8)
            skeleton.set_margin_end(8)
            self.flowbox.append(skeleton)
            self._skeletons.append(skeleton)

        self.append(self.flowbox)

    def stop_all(self):
        """Stop all pulse animations."""
        for skeleton in self._skeletons:
            skeleton.image_skeleton.stop_pulse()
            skeleton.text_skeleton.stop_pulse()


class SkeletonView(Gtk.Box):
    """Full skeleton view for library loading state."""

    def __init__(self, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16, **kwargs)
        self.set_margin_top(16)
        self.set_margin_bottom(16)
        self.set_margin_start(16)
        self.set_margin_end(16)

        # Header placeholder
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        header.set_margin_bottom(16)

        search_skeleton = SkeletonBlock(300, 36)
        header.append(search_skeleton)

        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        header.append(spacer)

        actions_skeleton = SkeletonBlock(200, 36)
        header.append(actions_skeleton)

        self.append(header)

        self.grid = SkeletonGrid(count=8)
        self.grid.set_valign(Gtk.Align.START)
        self.append(self.grid)

    def stop_animations(self):
        """Stop all animations before hiding."""
        self.grid.stop_all()
