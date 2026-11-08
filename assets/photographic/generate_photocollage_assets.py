"""
Photographic Papercraft Collage Asset Generator for PaperMotion AI.
Generates the authentic MeanwhileMayank / Vox documentary aesthetic:
- 1080x1920 Dark Journal Canvas with Binder Punch Holes & Central Spine Crease
- Mechanical Vintage Split-Flap Flip Clock Card
- High-Resolution Photographic Food, Anatomy, and Infographic Paper Cutouts
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path

out_dir = Path(__file__).parent
out_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. Dark Journal Notebook Canvas (with Binder Holes & Spine Crease)
# -------------------------------------------------------------
def make_notebook_canvas():
    w, h = 1080, 1920
    # Base dark charcoal paper
    img = Image.new("RGB", (w, h), (18, 16, 14))
    draw = ImageDraw.Draw(img)
    
    # 1. Subtle Paper Grain & Star Speckle Texture
    np.random.seed(42)
    noise = np.random.randint(-12, 12, (h, w), dtype=np.int16)
    base_arr = np.array(img, dtype=np.int16)
    for c in range(3):
        base_arr[:, :, c] = np.clip(base_arr[:, :, c] + noise, 8, 32)
    img = Image.fromarray(base_arr.astype(np.uint8))
    draw = ImageDraw.Draw(img)
    
    # Subtle star dust speckles (like MeanwhileMayank space & night shots)
    for _ in range(180):
        sx = np.random.randint(40, w - 40)
        sy = np.random.randint(40, h - 40)
        brightness = np.random.randint(140, 220)
        r = np.random.choice([1, 1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(brightness, brightness, brightness, 180))
        
    # 2. Vertical Book Spine Crease (down the center at x=540)
    # Left shadow, central highlight, right shadow
    spine_x = 540
    for offset in range(-15, 16):
        x = spine_x + offset
        if offset == 0:
            col = (45, 42, 38) # Light crease ridge
        elif offset in (-1, 1):
            col = (10, 9, 8)   # Deep crease fold
        else:
            intensity = int(18 - (15 - abs(offset)) * 0.6)
            col = (intensity, intensity - 2, intensity - 4)
        draw.line([(x, 0), (x, h)], fill=col, width=1)
        
    # 3. Binder Punch Holes along the left margin (at x=38)
    hole_x = 38
    num_holes = 7
    hole_y_spacing = (h - 240) // (num_holes - 1)
    
    for i in range(num_holes):
        hy = 120 + i * hole_y_spacing
        hr = 14
        # Outer indent ring (pressed cardboard rim)
        draw.ellipse([hole_x - hr - 3, hy - hr - 3, hole_x + hr + 3, hy + hr + 3], outline=(40, 36, 32), width=2)
        # Inner dark hole
        draw.ellipse([hole_x - hr, hy - hr, hole_x + hr, hy + hr], fill=(8, 7, 6))
        # Inner shadow crescent
        draw.arc([hole_x - hr + 1, hy - hr + 1, hole_x + hr - 1, hy + hr - 1], start=180, end=360, fill=(3, 2, 2), width=3)
        
    canvas_path = out_dir / "notebook_canvas.jpg"
    img.save(canvas_path, "JPEG", quality=95)
    print(f"Created: {canvas_path.name}")

# -------------------------------------------------------------
# 2. Vintage Mechanical Split-Flap Flip Clock Card
# -------------------------------------------------------------
def make_flip_clock_card():
    cw, ch = 540, 270
    img = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Cream Cardboard Substrate
    card_margin = 15
    card_rect = [card_margin, card_margin, cw - card_margin, ch - card_margin]
    draw.rounded_rectangle(card_rect, radius=22, fill=(235, 224, 206, 255), outline=(195, 180, 160, 255), width=3)
    
    # Left Flip Tile Box (Minutes / Hours)
    t1_rect = [45, 40, 235, 195]
    draw.rounded_rectangle(t1_rect, radius=12, fill=(34, 30, 26, 255), outline=(20, 18, 15, 255), width=2)
    # Split seam across the middle
    draw.line([(45, 117), (235, 117)], fill=(12, 10, 8, 255), width=3)
    
    # Right Flip Tile Box (Seconds)
    t2_rect = [305, 40, 495, 195]
    draw.rounded_rectangle(t2_rect, radius=12, fill=(34, 30, 26, 255), outline=(20, 18, 15, 255), width=2)
    draw.line([(305, 117), (495, 117)], fill=(12, 10, 8, 255), width=3)
    
    # Central Colon Dots
    draw.circle((270, 95), radius=7, fill=(34, 30, 26, 255))
    draw.circle((270, 140), radius=7, fill=(34, 30, 26, 255))
    
    # Large Split Numbers (Cream on dark tile)
    # Left: "50"
    draw.text((140, 115), "50", fill=(245, 238, 225, 255), anchor="mm", font_size=96)
    # Right: "00"
    draw.text((400, 115), "00", fill=(245, 238, 225, 255), anchor="mm", font_size=96)
    
    # Bottom Sub-Labels (MIN & SEC / HOURS)
    draw.text((140, 225), "HOURS", fill=(90, 80, 70, 255), anchor="mm", font_size=20)
    draw.text((400, 225), "TRANSIT", fill=(90, 80, 70, 255), anchor="mm", font_size=20)
    
    # Add signature paper cutout shadow
    shadow = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([card_margin+4, card_margin+10, cw - card_margin+4, ch - card_margin+10], radius=22, fill=(0, 0, 0, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    
    final_card = Image.alpha_composite(shadow, img)
    card_path = out_dir / "flip_clock_card.png"
    final_card.save(card_path, "PNG")
    print(f"Created: {card_path.name}")

# -------------------------------------------------------------
# 3. High-Resolution Photographic Ramen Noodles Cutout
# -------------------------------------------------------------
def make_ramen_noodles_cutout():
    w, h = 750, 500
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Wavy overlapping golden-yellow noodle strands with paper drop shadow
    np.random.seed(101)
    
    # Draw ~40 overlapping organic wavy noodle curves
    for i in range(45):
        y_start = 120 + (i * 7) + np.random.randint(-15, 15)
        points = []
        for x in range(80, 670, 15):
            freq = 0.04
            wave = math.sin(x * freq + i * 0.5) * 22 + math.cos(x * 0.08) * 10
            y = y_start + wave
            points.append((x, y))
            
        # Shading: base deep gold, highlight warm yellow, glossy white reflections
        strand_width = np.random.randint(9, 14)
        # Deep shadow under strand
        draw.line(points, fill=(160, 105, 25, 230), width=strand_width + 4)
        # Core noodle
        draw.line(points, fill=(244, 208, 111, 255), width=strand_width)
        # Glossy oil highlight line
        hi_points = [(px, py - 2) for px, py in points]
        draw.line(hi_points, fill=(255, 245, 200, 200), width=max(2, strand_width // 3))
        
    # Add signature paper-cutout shadow filter
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    # Mask bounding contour
    s_draw.rounded_rectangle([70, 100, 680, 420], radius=40, fill=(0, 0, 0, 190))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    
    final_noodles = Image.alpha_composite(shadow, img)
    out_path = out_dir / "ramen_noodles_cutout.png"
    final_noodles.save(out_path, "PNG")
    print(f"Created: {out_path.name}")

# -------------------------------------------------------------
# 4. 3D Anatomical Stomach Cross-Section Cutout
# -------------------------------------------------------------
def make_stomach_anatomy_cutout():
    w, h = 650, 750
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer muscular wall (Deep burgundy with paper cutout rim)
    wall_poly = [
        (330, 40), (380, 40), (410, 130), (420, 200),
        (540, 240), (610, 360), (610, 520), (560, 660),
        (460, 720), (320, 720), (180, 660), (100, 520),
        (100, 360), (220, 250), (290, 190), (300, 120), (330, 40)
    ]
    
    # White papercut border
    draw.polygon(wall_poly, fill=(70, 20, 28, 255), outline=(245, 235, 220, 240), width=4)
    
    # Inner gastric lumen cavity (Dark velvet)
    lumen_poly = [
        (340, 90), (370, 90), (390, 180), (510, 260),
        (560, 370), (560, 500), (500, 630), (340, 670),
        (220, 620), (150, 500), (150, 370), (260, 270), (310, 180), (340, 90)
    ]
    draw.polygon(lumen_poly, fill=(28, 8, 12, 255), outline=(139, 53, 36, 255), width=3)
    
    # Rugal folds (corrugated muscle ridges)
    for y_offset in range(300, 580, 45):
        ridge_pts = [(180, y_offset), (260, y_offset + 30), (350, y_offset - 10), (450, y_offset + 25), (530, y_offset)]
        draw.line(ridge_pts, fill=(180, 60, 45, 200), width=8)
        
    # Bubbling Acid / Chyme Pool in fundus & antrum
    draw.ellipse([180, 520, 520, 660], fill=(242, 140, 40, 220), outline=(255, 107, 0, 255), width=3)
    # Acid bubbles
    draw.circle((260, 570), 12, fill=(255, 245, 220, 230))
    draw.circle((380, 550), 16, fill=(255, 245, 220, 230))
    draw.circle((440, 590), 14, fill=(255, 245, 220, 230))
    
    # Paper cutout drop shadow
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.polygon([(px+6, py+14) for px, py in wall_poly], fill=(0, 0, 0, 190))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    
    final_stomach = Image.alpha_composite(shadow, img)
    out_path = out_dir / "stomach_anatomy_cutout.png"
    final_stomach.save(out_path, "PNG")
    print(f"Created: {out_path.name}")

# -------------------------------------------------------------
# 5. Gourmet Balanced Ramen Bowl Cutout (Toppings & Egg)
# -------------------------------------------------------------
def make_balanced_bowl_cutout():
    w, h = 750, 750
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx, cy = 375, 420
    # Ceramic bowl rim
    draw.ellipse([cx - 320, cy - 240, cx + 320, cy + 240], fill=(24, 20, 18, 255), outline=(245, 235, 220, 240), width=4)
    draw.ellipse([cx - 290, cy - 210, cx + 290, cy + 210], fill=(120, 60, 22, 255), outline=(242, 140, 40, 255), width=3)
    
    # Noodle curls in broth
    for rad in range(60, 220, 40):
        draw.arc([cx - rad, cy - int(rad*0.7), cx + rad, cy + int(rad*0.7)], start=0, end=360, fill=(244, 208, 111, 230), width=7)
        
    # Half Soft-Boiled Egg (Hero Right)
    egg_cx, egg_cy = cx + 110, cy - 30
    draw.ellipse([egg_cx - 65, egg_cy - 85, egg_cx + 65, egg_cy + 85], fill=(250, 245, 238, 255), outline=(220, 210, 195, 255), width=3)
    # Liquid Golden Yolk
    draw.circle((egg_cx, egg_cy + 10), 40, fill=(242, 140, 40, 255))
    draw.circle((egg_cx - 10, egg_cy + 5), 12, fill=(255, 210, 80, 240)) # Specular gleam
    
    # Fresh Bok Choy Greens (Hero Left)
    for leaf_angle in [-40, -15, 10]:
        lx = cx - 140 + int(math.cos(math.radians(leaf_angle)) * 40)
        ly = cy - 40 + int(math.sin(math.radians(leaf_angle)) * 30)
        draw.ellipse([lx - 55, ly - 80, lx + 55, ly + 80], fill=(45, 106, 79, 255), outline=(82, 183, 136, 255), width=2)
        # White stem
        draw.line([(lx, ly + 70), (lx, ly - 30)], fill=(235, 245, 235, 255), width=8)
        
    # Sliced Carrot Ribbons
    draw.rounded_rectangle([cx - 30, cy + 80, cx + 45, cy + 105], radius=6, fill=(232, 93, 4, 255))
    draw.rounded_rectangle([cx + 20, cy + 110, cx + 90, cy + 130], radius=6, fill=(232, 93, 4, 255))
    
    # Paper cutout drop shadow
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 315, cy - 225, cx + 325, cy + 255], fill=(0, 0, 0, 210))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    
    final_bowl = Image.alpha_composite(shadow, img)
    out_path = out_dir / "balanced_bowl_cutout.png"
    final_bowl.save(out_path, "PNG")
    print(f"Created: {out_path.name}")

# -------------------------------------------------------------
# 6. Technical Nutrition Facts Label Cutout
# -------------------------------------------------------------
def make_nutrition_label_cutout():
    w, h = 500, 680
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Cardstock card
    draw.rounded_rectangle([20, 20, w - 20, h - 20], radius=16, fill=(22, 19, 16, 255), outline=(245, 235, 220, 240), width=3)
    
    # Header block
    draw.rounded_rectangle([20, 20, w - 20, 100], radius=16, fill=(245, 235, 220, 255))
    draw.text((w // 2, 60), "NUTRITION FACTS", fill=(17, 17, 17, 255), anchor="mm", font_size=38)
    
    # Rows
    y = 130
    draw.text((45, y), "Serving Size: 1 Packet", fill=(200, 190, 180, 255), font_size=18)
    y += 40
    draw.line([(40, y), (w - 40, y)], fill=(80, 75, 70, 255), width=2)
    y += 20
    draw.text((45, y), "Carbohydrates (Refined Starch)", fill=(245, 235, 220, 255), font_size=20)
    y += 45
    draw.line([(40, y), (w - 40, y)], fill=(80, 75, 70, 255), width=2)
    
    # SODIUM HIGHLIGHT CALLOUT (BURNT ORANGE STAMP)
    y += 20
    draw.rounded_rectangle([35, y, w - 35, y + 110], radius=10, fill=(45, 22, 10, 255), outline=(255, 107, 0, 255), width=3)
    draw.text((55, y + 35), "SODIUM (SALT)", fill=(255, 107, 0, 255), font_size=32)
    draw.text((55, y + 75), "HIGHLY VARIABLE BY BRAND", fill=(255, 169, 77, 255), font_size=16)
    # Exclamation badge
    draw.circle((w - 75, y + 55), 20, fill=(255, 107, 0, 255))
    draw.text((w - 75, y + 55), "!", fill=(17, 17, 17, 255), anchor="mm", font_size=26)
    
    y += 140
    draw.line([(40, y), (w - 40, y)], fill=(80, 75, 70, 255), width=2)
    y += 25
    draw.text((45, y), "Dietary Fiber: Minimal (<2g)", fill=(180, 170, 160, 255), font_size=18)
    y += 45
    draw.line([(40, y), (w - 40, y)], fill=(80, 75, 70, 255), width=2)
    y += 25
    draw.text((45, y), "Protein: Low (4-6g)", fill=(180, 170, 160, 255), font_size=18)
    
    # Advisory stamp
    y += 65
    draw.rounded_rectangle([45, y, w - 45, y + 80], radius=8, fill=(11, 9, 7, 255), outline=(242, 140, 40, 255), width=2)
    draw.text((w // 2, y + 28), "ALWAYS CHECK PACKET LABEL", fill=(245, 235, 220, 255), anchor="mm", font_size=15)
    draw.text((w // 2, y + 55), "Balance with fresh vegetables & protein", fill=(255, 169, 77, 255), anchor="mm", font_size=13)
    
    # Shadow
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([26, 32, w - 14, h - 8], radius=16, fill=(0, 0, 0, 190))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    
    final_card = Image.alpha_composite(shadow, img)
    out_path = out_dir / "nutrition_label_cutout.png"
    final_card.save(out_path, "PNG")
    print(f"Created: {out_path.name}")

if __name__ == "__main__":
    make_notebook_canvas()
    make_flip_clock_card()
    make_ramen_noodles_cutout()
    make_stomach_anatomy_cutout()
    make_balanced_bowl_cutout()
    make_nutrition_label_cutout()
    print("\nALL PHOTOGRAPHIC PAPERCRAFT COLLAGE ASSETS GENERATED!")
