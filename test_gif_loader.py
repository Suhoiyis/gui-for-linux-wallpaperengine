import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GdkPixbuf, GLib

def on_activate(app):
    win = Gtk.ApplicationWindow(application=app)
    win.set_title("GIF Loader Test")
    win.set_default_size(400, 400)
    
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    win.set_child(box)
    
    lbl = Gtk.Label(label="Testing GIF loading...")
    box.append(lbl)
    
    gif_path = "/tmp/test.gif"
    
    # 1. Try Loading via PixbufAnimation
    try:
        anim = GdkPixbuf.PixbufAnimation.new_from_file(gif_path)
        info = f"PixbufAnimation: Loaded! Size={anim.get_width()}x{anim.get_height()}, Static={anim.is_static_image()}"
        print(info)
        lbl.set_label(info)
    except Exception as e:
        print(f"PixbufAnimation Failed: {e}")
        lbl.set_label(f"Loader Failed: {e}")
        win.present()
        return

    # 2. Try Gtk.Picture (what we use in app)
    try:
        pic = Gtk.Picture()
        pic.set_size_request(200, 200)
        # pic.set_filename(gif_path) # We know this failed
        
        # If set_filename fails, we might need a workaround.
        # But let's see if we can set it from a resource or something?
        # Or maybe set_file(Gio.File) works better?
        
        from gi.repository import Gio
        gfile = Gio.File.new_for_path(gif_path)
        pic.set_file(gfile)
        
        box.append(pic)
    except Exception as e:
        print(f"Picture setup failed: {e}")

    win.present()

app = Gtk.Application(application_id='com.example.giftest2')
app.connect('activate', on_activate)
app.run(None)
