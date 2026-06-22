import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

def create_visual_preview(output_path="preview_frame.png"):
    # 1. Setup Canvas (720p)
    width, height = 1280, 720
    # Background: Dark Noir Gradient
    base = Image.new("RGB", (width, height), (5, 5, 5))
    draw = ImageDraw.Draw(base)
    
    # Simulate Noir Lighting (Amber Highlight)
    for r in range(width, 0, -5):
        alpha = int(40 * (1 - r/width))
        draw.ellipse([width//2-r, height//2-r, width//2+r, height//2+r], 
                     outline=(255, 180, 50, alpha))

    # 2. Generate Procedural Mask (The Fragment)
    mask_w, mask_h = 850, 400
    mask_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    # Procedural edges for the "torn paper"
    m_left, m_top = (width - mask_w)//2, (height - mask_h)//2
    m_right, m_bottom = m_left + mask_w, m_top + mask_h
    
    # Draw base mask shape
    mask_shape = Image.new("L", (mask_w, mask_h), 0)
    mask_draw = ImageDraw.Draw(mask_shape)
    margin = 20
    mask_draw.rectangle([margin, margin, mask_w-margin, mask_h-margin], fill=255)
    
    # Add noise to edges
    mask_array = np.array(mask_shape)
    for _ in range(5):
        noise = np.random.randint(-12, 12, size=mask_array.shape).astype(np.int16)
        mask_array = np.clip(mask_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    mask_shape = Image.fromarray(mask_array).filter(ImageFilter.GaussianBlur(radius=1))
    
    # Paper Texture Color
    paper_color = (30, 30, 30, 230) # Dark grey semi-transparent paper
    paper_surface = Image.new("RGBA", (mask_w, mask_h), paper_color)
    
    # Composite paper onto mask layer
    mask_layer.paste(paper_surface, (m_left, m_top), mask_shape)
    base.paste(mask_layer, (0, 0), mask_layer)

    # 3. Add Typography
    # Using default fonts if specific ones aren't available, but aiming for style
    try:
        # Try to find a serif font on Linux
        font_bible = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", 35)
        font_macro = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 80)
    except:
        font_bible = ImageFont.load_default()
        font_macro = ImageFont.load_default()

    draw = ImageDraw.Draw(base)
    
    # Bible Text (Inside Mask)
    bible_text = "Thy word is a lamp unto my feet,\nand a light unto my path.\n- Psalm 119:105"
    draw.text((width//2, height//2 - 40), bible_text, fill=(220, 220, 220), font=font_bible, anchor="mm", align="center")
    
    # Macro Concept (Gold, Bottom)
    macro_text = "THE GUIDING LIGHT"
    draw.text((width//2, height - 100), macro_text, fill=(255, 215, 0), font=font_macro, anchor="mm")

    # Final Polish: Vignette
    vignette = Image.new("L", (width, height), 0)
    v_draw = ImageDraw.Draw(vignette)
    v_draw.ellipse([-100, -100, width+100, height+100], fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=150))
    base = Image.composite(base, Image.new("RGB", (width, height), (0,0,0)), vignette)

    base.save(output_path)
    print(f"Preview generated at: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_visual_preview()
