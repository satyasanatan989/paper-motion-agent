"""
Sample Assets Generator for 15-Second Studio Tier Explainer.
Generates:
1. Die-cut vinyl ice cream sticker with peeled corner and glossy sheen.
2. Fractal torn paper evidence card (using generate_torn_paper_edge).
3. Crimson rubber stamp seal.
"""

import math
import sys
import numpy as np
from pathlib import Path

# Add paper-motion-agent root to sys.path
agent_root = Path(__file__).resolve().parent.parent.parent
if str(agent_root) not in sys.path:
    sys.path.insert(0, str(agent_root))

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

from assets.photographic.generate_photocollage_assets import (
    paperize_cutout,
    generate_torn_paper_edge
)

def make_die_cut_ice_cream_sticker(out_path: Path) -> Path:
    """Creates a die-cut vinyl sticker with white border and peeled/folded corner."""
    w, h = 500, 600
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx = w // 2
    # 1. Waffle Cone
    cone_pts = [(cx - 90, 240), (cx + 90, 240), (cx, 520)]
    draw.polygon(cone_pts, fill=(210, 140, 60, 255))
    # Cone cross-hatch lines
    for y in range(260, 500, 30):
        t = (y - 240) / 280.0
        hw = int(90 * (1.0 - t))
        draw.line([(cx - hw, y), (cx + hw, y + 25)], fill=(160, 95, 30, 200), width=3)
        draw.line([(cx + hw, y), (cx - hw, y + 25)], fill=(160, 95, 30, 200), width=3)

    # 2. Ice cream scoops (stacked)
    # Chocolate / Bottom scoop
    draw.circle((cx, 240), 95, fill=(110, 60, 30, 255))
    # Vanilla / Middle scoop
    draw.circle((cx, 165), 85, fill=(250, 245, 230, 255))
    # Strawberry / Top scoop
    draw.circle((cx, 105), 75, fill=(235, 90, 110, 255))
    # Cherry on top
    draw.circle((cx, 45), 26, fill=(190, 20, 35, 255))
    draw.arc([cx, 15, cx + 35, 55], start=180, end=300, fill=(70, 130, 40, 255), width=4)

    # Drips on the cone
    draw.rounded_rectangle([cx - 50, 230, cx - 30, 280], radius=10, fill=(250, 245, 230, 255))
    draw.rounded_rectangle([cx + 25, 230, cx + 45, 295], radius=10, fill=(110, 60, 30, 255))

    # 3. Vinyl Die-Cut White Outline
    alpha = img.split()[3]
    dilated = alpha.filter(ImageFilter.MaxFilter(17)) # 8px vinyl border
    vinyl_stroke = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    die_cut = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    die_cut.paste(vinyl_stroke, (0, 0), dilated)
    die_cut.paste(img, (0, 0), img)

    # 4. Glossy Sheen Overlay (diagonal translucent highlight)
    gloss = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gloss)
    g_draw.polygon([(0, 0), (w, 0), (w, 180), (0, 320)], fill=(255, 255, 255, 40))
    gloss.putalpha(ImageChops.multiply(gloss.split()[3], dilated))
    die_cut = Image.alpha_composite(die_cut, gloss)

    # 5. Peeled / Dog-Eared Corner (Top Right)
    # Cut off corner from die_cut and draw folded back triangle
    corner_size = 55
    peel_mask = Image.new("L", (w, h), 255)
    pm_draw = ImageDraw.Draw(peel_mask)
    # Top-right corner cut: x > w - corner_size, y < corner_size
    pm_draw.polygon([(w - 120, 20), (w - 20, 20), (w - 20, 120)], fill=0)
    
    peeled_die_cut = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    peeled_die_cut.paste(die_cut, (0, 0), peel_mask)
    
    # Draw folded corner flap (adhesive gray underside with shadow)
    f_draw = ImageDraw.Draw(peeled_die_cut)
    flap_pts = [(w - 120, 20), (w - 20, 120), (w - 105, 105)]
    # Soft drop shadow under flap
    f_draw.polygon([(w - 118, 22), (w - 22, 118), (w - 100, 115)], fill=(0, 0, 0, 90))
    # Underside metallic/adhesive gray flap
    f_draw.polygon(flap_pts, fill=(225, 225, 225, 255), outline=(180, 180, 180, 255), width=2)

    # Apply paperize for realistic physical desk drop shadow
    final_sticker = paperize_cutout(peeled_die_cut, inner_border_px=0, shadow_blur=16, shadow_opacity=0.42)
    final_sticker.save(out_path, "PNG")
    print(f"Generated die-cut vinyl sticker: {out_path}")
    return out_path

from PIL import ImageChops

def make_torn_evidence_card(out_path: Path) -> Path:
    """Creates a cardstock evidence report with fractal torn edges and official stamps."""
    w, h = 540, 380
    base_card = generate_torn_paper_edge(
        width=w,
        height=h,
        edge_sides=("bottom", "right"),
        paper_color=(246, 242, 234),
        pulp_color=(255, 255, 255),
        tear_depth=16,
        seed=108
    )

    pad = 16 + 16
    draw = ImageDraw.Draw(base_card)
    
    # Header Banner
    draw.rounded_rectangle([pad + 30, pad + 25, pad + w - 30, pad + 85], radius=6, fill=(35, 28, 24, 255))
    draw.text((pad + 45, pad + 38), "MINISTRY OF HEALTH & FOOD SAFETY", fill=(217, 119, 6, 255), font_size=18)
    draw.text((pad + 45, pad + 60), "STATUTORY MANDATE : DAIRY STANDARD ACT", fill=(250, 245, 235, 255), font_size=13)

    # Evidence Rows
    y = pad + 110
    draw.text((pad + 35, y), "PRODUCT CLASSIFICATION REPORT", fill=(20, 20, 20, 255), font_size=20)
    y += 35
    draw.line([(pad + 35, y), (pad + w - 45, y)], fill=(180, 170, 160, 255), width=2)
    
    y += 18
    draw.text((pad + 35, y), "• Dairy Milk Fat Content:", fill=(60, 50, 45, 255), font_size=17)
    draw.text((pad + 280, y), "MINIMUM 10.0%", fill=(194, 65, 12, 255), font_size=18)

    y += 32
    draw.text((pad + 35, y), "• Vegetable Oil Replacement:", fill=(60, 50, 45, 255), font_size=17)
    draw.text((pad + 280, y), "STRICTLY PROHIBITED", fill=(185, 28, 28, 255), font_size=18)

    y += 32
    draw.text((pad + 35, y), "• Legal Classification:", fill=(60, 50, 45, 255), font_size=17)
    draw.text((pad + 280, y), "FROZEN DESSERT ONLY", fill=(30, 30, 30, 255), font_size=17)

    y += 38
    # Warning callout bar
    draw.rounded_rectangle([pad + 35, y, pad + w - 45, y + 45], radius=6, fill=(254, 242, 242, 255), outline=(220, 38, 38, 255), width=2)
    draw.text((pad + 50, y + 12), "VIOLATION: Non-dairy fat labeled as ice cream carries penal fine", fill=(185, 28, 28, 255), font_size=13)

    base_card.save(out_path, "PNG")
    print(f"Generated torn evidence card: {out_path}")
    return out_path

def make_rubber_stamp_seal(out_path: Path) -> Path:
    """Creates a crimson rubber stamp seal with distressed borders."""
    w, h = 340, 340
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = w // 2, h // 2

    # Double distressed circles
    crimson = (194, 65, 12, 235) # Burnt orange / crimson
    draw.circle((cx, cy), 145, outline=crimson, width=7)
    draw.circle((cx, cy), 130, outline=crimson, width=3)
    draw.circle((cx, cy), 122, outline=crimson, width=1)

    # Center Text
    draw.text((cx, cy - 35), "10% DAIRY FAT", fill=crimson, anchor="mm", font_size=28)
    draw.text((cx, cy + 5), "MANDATE", fill=crimson, anchor="mm", font_size=32)
    draw.text((cx, cy + 42), "VERIFIED LEGAL", fill=crimson, anchor="mm", font_size=16)

    # Stars
    draw.text((cx - 85, cy + 5), "★", fill=crimson, anchor="mm", font_size=24)
    draw.text((cx + 85, cy + 5), "★", fill=crimson, anchor="mm", font_size=24)

    # Grunge distress effect (noise erosion)
    rng = np.random.default_rng(99)
    noise = (rng.uniform(0, 1, (h, w)) > 0.88).astype(np.uint8) * 180
    noise_img = Image.fromarray(noise, mode="L")
    alpha = img.split()[3]
    eroded_alpha = ImageChops.subtract(alpha, noise_img)
    img.putalpha(eroded_alpha)

    # Slight angle rotation for realism
    rotated = img.rotate(-14, resample=Image.BICUBIC, expand=True)
    rotated.save(out_path, "PNG")
    print(f"Generated rubber stamp seal: {out_path}")
    return out_path

if __name__ == "__main__":
    out_dir = Path(__file__).parent / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    make_die_cut_ice_cream_sticker(out_dir / "ice_cream_sticker.png")
    make_torn_evidence_card(out_dir / "torn_evidence_card.png")
    make_rubber_stamp_seal(out_dir / "rubber_stamp_seal.png")
