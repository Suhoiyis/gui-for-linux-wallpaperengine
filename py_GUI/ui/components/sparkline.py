import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib
import cairo

class Sparkline(Gtk.DrawingArea):
    def __init__(self, color=(0.2, 0.6, 1.0), height=60, title="", max_points=60):
        super().__init__()
        self.set_content_height(height)
        self.set_vexpand(False)
        self.set_hexpand(True)
        self.set_draw_func(self.on_draw)
        
        self.data = []
        self.max_val = 100.0
        self.color = color
        self.title = title
        self.unit = ""
        self.max_points = max_points
        
        # Margins
        self.margin_left = 35
        self.margin_right = 10
        self.margin_top = 15
        self.margin_bottom = 15

    def set_data(self, data, max_val=None, unit=""):
        self.data = list(data) # Copy data
        self.unit = unit
        if max_val is not None:
            self.max_val = max_val
        elif data:
            self.max_val = max(max(data) * 1.2, 1.0)
        self.queue_draw()

    def set_color(self, color):
        self.color = color
        self.queue_draw()

    def on_draw(self, area, ctx, width, height):
        # Calculate plotting area
        graph_width = width - self.margin_left - self.margin_right
        graph_height = height - self.margin_top - self.margin_bottom
        
        # Draw Background Grid
        ctx.set_line_width(1.0)
        ctx.set_source_rgba(1, 1, 1, 0.05)
        
        # Horizontal lines (0%, 25%, 50%, 75%, 100%)
        ctx.set_font_size(9)
        for i in [0, 0.25, 0.5, 0.75, 1.0]:
            y_rel = graph_height * (1 - i)
            y = self.margin_top + y_rel
            
            # Draw grid line
            ctx.move_to(self.margin_left, y)
            ctx.line_to(width - self.margin_right, y)
            
            # Draw label
            if self.max_val > 0:
                val = int(self.max_val * i)
                label = f"{val}{self.unit}"
                ctx.set_source_rgba(1, 1, 1, 0.4)
                extents = ctx.text_extents(label)
                # Align right vertically centered
                ctx.move_to(self.margin_left - extents.width - 5, y + extents.height/2 - 1)
                ctx.show_text(label)
                
            # Reset for line drawing
            ctx.set_source_rgba(1, 1, 1, 0.05)
        
        # Vertical lines (60s, 45s, 30s, 15s, 0s)
        for i in [0.25, 0.5, 0.75]:
            x = self.margin_left + graph_width * i
            ctx.move_to(x, self.margin_top)
            ctx.line_to(x, height - self.margin_bottom)
            
        ctx.stroke()

        # Labels (Title, Time)
        ctx.set_source_rgba(1, 1, 1, 0.5)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(10)
        
        # Title
        if self.title:
            ctx.move_to(self.margin_left, 10)
            ctx.show_text(self.title)
            
        # Time Labels
        ctx.set_font_size(9)
        ctx.move_to(self.margin_left, height - 2)
        ctx.show_text("60s")
        
        ctx.move_to(self.margin_left + graph_width * 0.5 - 10, height - 2)
        ctx.show_text("30s")
        
        ctx.move_to(width - self.margin_right - 20, height - 2)
        ctx.show_text("Now")

        if not self.data:
            return

        ctx.set_line_width(2.0)
        ctx.set_source_rgba(*self.color, 1.0)

        # Scale calculation
        # Always use max_points - 1 to calculate step, ensuring 60s scale
        step_x = graph_width / (self.max_points - 1)
        scale_y = graph_height / self.max_val if self.max_val > 0 else 1.0
        
        # Calculate start x (align right if fewer points)
        points_count = len(self.data)
        start_offset = (self.max_points - points_count) * step_x

        # Draw path
        # Clamp values to avoid drawing outside
        first_val = min(self.data[0], self.max_val)
        ctx.move_to(self.margin_left + start_offset, 
                   self.margin_top + graph_height - (first_val * scale_y))
        
        for i, val in enumerate(self.data[1:], 1):
            val = min(val, self.max_val)
            x = self.margin_left + start_offset + i * step_x
            y = self.margin_top + graph_height - (val * scale_y)
            ctx.line_to(x, y)
        
        ctx.stroke_preserve()

        # Fill under line
        ctx.line_to(self.margin_left + start_offset + (points_count - 1) * step_x, 
                   self.margin_top + graph_height)
        ctx.line_to(self.margin_left + start_offset, 
                   self.margin_top + graph_height)
        ctx.close_path()
        ctx.set_source_rgba(*self.color, 0.1)
        ctx.fill()
