import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf

class AnimatedPreview(Gtk.Picture):
    def __init__(self, size_request=(200, 200)):
        super().__init__()
        self.set_content_fit(Gtk.ContentFit.COVER)
        self.set_size_request(*size_request)
        
        # Force fill behavior
        self.set_halign(Gtk.Align.FILL)
        self.set_valign(Gtk.Align.FILL)
        self.set_hexpand(False)
        self.set_vexpand(False)
        self.set_can_shrink(True)
        
        self.anim = None
        self.anim_iter = None
        self.anim_timer = None
        self.current_path = None

    def set_image_from_path(self, path: str, wp_manager):
        """
        Smartly sets the image. If it's a GIF, starts animation.
        If it's static, sets a static texture.
        """
        if self.current_path == path:
            return

        self.stop_animation()
        self.current_path = path
        
        if not path:
            self.set_paintable(None)
            return

        loaded_anim = False
        if path.lower().endswith('.gif'):
            try:
                self._start_animation(path)
                loaded_anim = True
            except Exception:
                loaded_anim = False
        
        if not loaded_anim:
            # Fallback to static texture
            texture = wp_manager.get_texture(path, self.get_width() or 200)
            self.set_paintable(texture)

    def _start_animation(self, path):
        self.anim = GdkPixbuf.PixbufAnimation.new_from_file(path)
        self.anim_iter = self.anim.get_iter(None)
        
        pixbuf = self.anim_iter.get_pixbuf()
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.set_paintable(texture)
        
        if not self.anim.is_static_image():
            self.anim_timer = GLib.timeout_add(
                self.anim_iter.get_delay_time(),
                self._on_animation_frame
            )

    def _on_animation_frame(self):
        if not hasattr(self, 'anim_iter') or not self.anim_iter:
            return False
        
        try:
            self.anim_iter.advance(None)
        except:
            return False
        
        pixbuf = self.anim_iter.get_pixbuf()
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.set_paintable(texture)
        
        delay = self.anim_iter.get_delay_time()
        if delay <= 0:
            delay = 100
        
        self.anim_timer = GLib.timeout_add(delay, self._on_animation_frame)
        return False

    def stop_animation(self):
        if hasattr(self, 'anim_timer') and self.anim_timer:
            GLib.source_remove(self.anim_timer)
            self.anim_timer = None
        self.anim = None
        self.anim_iter = None
        self.current_path = None
