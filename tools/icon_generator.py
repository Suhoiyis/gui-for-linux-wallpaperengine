import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

def create_glassy_icon(input_path, output_path, size=None, radius_ratio=0.22):
    """
    Generates an iOS-style glassy rounded icon from a source image.
    
    Args:
        input_path: Path to source image
        output_path: Path to save generated icon
        size: Target size (width, height). If None, uses input image size.
        radius_ratio: Corner radius as a fraction of size (0.22 is roughly iOS style)
    """
    
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        return

    # 1. Load and Resize Source
    print(f"Loading {input_path}...")
    try:
        src = Image.open(input_path).convert("RGBA")
    except Exception as e:
        print(f"Failed to open image: {e}")
        return

    # Use original size if not specified
    if size is None:
        size = src.size
    else:
        src = src.resize(size, Image.Resampling.LANCZOS)
    
    print(f"Processing at size: {size}")
    
    # Create base canvas
    width, height = size
    icon = Image.new("RGBA", size, (0, 0, 0, 0))
    
    # 2. Create Rounded Rect Mask (Squircle-ish)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    radius = int(min(size) * radius_ratio)
    draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=255)
    
    # Apply mask to source
    src_rounded = Image.new("RGBA", size, (0, 0, 0, 0))
    src_rounded.paste(src, mask=mask)
    
    # 3. Add "Glassy" Effects
    
    # Effect A: Top Highlight (The "Gloss")
    # A soft white gradient from top-left to center
    gloss = Image.new("RGBA", size, (0, 0, 0, 0))
    gloss_draw = ImageDraw.Draw(gloss)
    
    # Draw a white shape at the top
    # Linear gradient simulation using alpha composite
    for y in range(height // 2):
        alpha = int(200 * (1 - (y / (height // 2)))**2) # Quadratic falloff
        gloss_draw.line([(0, y), (width, y)], fill=(255, 255, 255, max(0, alpha)))
    
    # Mask gloss to rounded shape but shrink slightly to look like internal reflection
    gloss_mask = mask.resize((int(width*0.96), int(height*0.96)), Image.Resampling.LANCZOS)
    gloss_layer = Image.new("RGBA", size, (0,0,0,0))
    # Center the smaller gloss mask
    offset = (int(width*0.02), int(height*0.02))
    gloss_layer.paste((255,255,255,0), (0,0,size[0],size[1])) # Blank
    
    # Actually, simpler approach for gloss:
    # Just an elliptical white highlight at top
    highlight = Image.new("RGBA", size, (0,0,0,0))
    h_draw = ImageDraw.Draw(highlight)
    # White ellipse at top, slightly transparent
    h_draw.ellipse([(-width*0.2, -height*0.1), (width*1.2, height*0.5)], fill=(255,255,255, 40))
    # Mask it to the icon shape
    src_rounded = Image.alpha_composite(src_rounded, Image.composite(highlight, Image.new("RGBA", size, (0,0,0,0)), mask))

    # Effect B: Inner Stroke/Bevel (Subtle edge light)
    # Create a stroke by differencing two masks
    stroke_mask = Image.new("L", size, 0)
    s_draw = ImageDraw.Draw(stroke_mask)
    s_draw.rounded_rectangle([(0,0), (width, height)], radius=radius, outline=255, width=2)
    
    stroke_layer = Image.new("RGBA", size, (255, 255, 255, 50)) # Subtle white stroke
    src_rounded.paste(stroke_layer, mask=stroke_mask)

    # Effect C: Subtle Shadow/Gradient at bottom (Depth)
    shadow = Image.new("RGBA", size, (0,0,0,0))
    sh_draw = ImageDraw.Draw(shadow)
    for y in range(height//2, height):
        alpha = int(100 * ((y - height//2) / (height//2)))
        sh_draw.line([(0, y), (width, y)], fill=(0, 0, 0, max(0, alpha)))
    
    # Composite shadow
    src_rounded = Image.alpha_composite(src_rounded, Image.composite(shadow, Image.new("RGBA", size, (0,0,0,0)), mask))

    # 4. Optional: Drop Shadow (External)
    # To add a drop shadow, we need a larger canvas.
    # Let's keep the image size strictly the icon for Linux app consistency,
    # usually Linux icons don't bake in large drop shadows as the dock handles that.
    # But we can add a very slight one if the user wants "3D" feel.
    # For now, let's stick to the icon itself to avoid scaling issues in docks.

    # Save Glassy Version
    print(f"Saving glassy icon to {output_path}...")
    src_rounded.save(output_path, "PNG")
    
    # Generate Simple Rounded Version (No Effects)
    simple_rounded = Image.new("RGBA", size, (0, 0, 0, 0))
    simple_rounded.paste(src, mask=mask)
    
    simple_output = output_path.replace("_glass.png", "_rounded.png")
    if simple_output == output_path:
        simple_output = output_path.replace(".png", "_rounded.png")
        
    print(f"Saving simple rounded icon to {simple_output}...")
    simple_rounded.save(simple_output, "PNG")
    
    print("Done! Generated both icons.")

if __name__ == "__main__":
    # Process main icon
    input_file = "pic/GUI.png"
    output_file = "pic/GUI_glass.png"
    
    # Check if PIL is installed
    try:
        import PIL
    except ImportError:
        print("Error: Pillow is not installed. Please run: pip install Pillow")
        exit(1)

    if os.path.exists(input_file):
        create_glassy_icon(input_file, output_file)
        
    # Process tray icon
    tray_input = "pic/gui_tray.png"
    if os.path.exists(tray_input):
        create_glassy_icon(tray_input, "pic/gui_tray_glass.png")
