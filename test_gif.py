import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

def on_activate(app):
    win = Gtk.ApplicationWindow(application=app)
    win.set_title("GIF Test")
    win.set_default_size(400, 400)
    
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    win.set_child(box)
    
    lbl = Gtk.Label(label="Testing GIF loading...")
    box.append(lbl)
    
    # 1. Create a dummy GIF if not exists
    gif_path = "/tmp/test.gif"
    try:
        from PIL import Image, ImageDraw
        images = []
        for i in range(10):
            img = Image.new('RGB', (100, 100), color=(i*20, 0, 0))
            d = ImageDraw.Draw(img)
            d.text((10,10), str(i), fill=(255,255,255))
            images.append(img)
        images[0].save(gif_path, save_all=True, append_images=images[1:], duration=200, loop=0)
        print(f"Created test GIF at {gif_path}")
    except ImportError:
        print("PIL not found, cannot create test GIF. Please provide a path.")
        lbl.set_label("PIL missing, cannot create test GIF")
        return

    # 2. Test Gtk.Picture.set_filename
    pic = Gtk.Picture()
    pic.set_size_request(200, 200)
    pic.set_filename(gif_path)
    box.append(pic)
    
    win.present()

app = Gtk.Application(application_id='com.example.giftest')
app.connect('activate', on_activate)
app.run(None)
