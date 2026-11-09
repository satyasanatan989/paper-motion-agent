"""
Batch-by-Batch Modular Production Engine for Food Code Episode 001.
Professional Documentary Video Editor Edition:
- Word-by-Word Kinetic Karaoke Subtitles (Alex Hormozi / Vox style)
- In-Camera Film Burn & Whip-Flash Transitions (0ms drift)
- 35mm Procedural Film Grain & Warm Corner Light Leaks
- Tactile Camera Impact Shakes on Stamp & Pushpin Hits
- 3D Split-Flap Clock Flips & Real-Time Sodium Odometer
- Bubbling Gastric Acid Pool & Scanning Laser
"""

import json
import re
import subprocess
import time
import sys
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure repo root is on sys.path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from pipeline.batch_stitcher import BatchStitcher
from quality_control.validator import QualityValidator
from tools.aesthetic_judge import AestheticJudge
from visual_engine.kinetic_elements import KineticElements
from voice.cinecode_foley import CineCodeFoleyEngine

proj_dir = Path(__file__).resolve().parent
output_dir = repo_root / "output" / "food_code"
batch_dir = output_dir / "batch"
batch_dir.mkdir(parents=True, exist_ok=True)
stages_dir = proj_dir / "batch_stages"
stages_dir.mkdir(parents=True, exist_ok=True)
assets_dir = repo_root / "assets" / "photographic"

with open(proj_dir / "storyboard.json", encoding="utf-8") as f:
    sb = json.load(f)

with open(proj_dir / "timings.json", encoding="utf-8") as f:
    timings = json.load(f)

scenes = sb["scenes"]
master_soundtrack = proj_dir / "soundtrack.mp3"
render_js = repo_root / "pipeline" / "render.js"

print("=================================================================")
print("🎬 FOOD CODE 001 — PROFESSIONAL DOCUMENTARY EDITING SUITE")
print("=================================================================\n")

# Asset URI helpers
def get_asset_uri(name: str) -> str:
    path = assets_dir / name
    if not path.exists():
        raise FileNotFoundError(f"Missing photographic asset: {path}")
    return path.resolve().as_uri()

CANVAS_URI = get_asset_uri("notebook_canvas.jpg")
MACRO_NOODLES_URI = get_asset_uri("macro_noodles_sticker.png")
RAMEN_NOODLES_URI = get_asset_uri("ramen_noodles_cutout.png")
MOUTH_ENZYME_URI = get_asset_uri("mouth_enzyme_cutout.png")
STOMACH_URI = get_asset_uri("photo_stomach_cutout.png")
INTESTINE_URI = get_asset_uri("photo_villi_cutout.png")
BLOODSTREAM_URI = get_asset_uri("photo_bloodstream_cutout.png")
NUTRITION_LABEL_URI = get_asset_uri("nutrition_label_cutout.png")
BALANCED_BOWL_URI = get_asset_uri("photo_bowl_cutout.png")
HERO_CREST_URI = get_asset_uri("science_foodcode_crest.png")
VORK_3D_CREST_URI = get_asset_uri("vork_3d_gold_crest.png")
VORK_3D_MOLECULE_URI = get_asset_uri("vork_3d_glucose_molecule.png")

# Tactile Props URIs
SCOTCH_TAPE_URI = get_asset_uri("scotch_tape_strip.png")
PUSHPIN_URI = get_asset_uri("pushpin_red.png")
RUBBER_STAMP_URI = get_asset_uri("rubber_stamp_warning.png")

# Kinetic Styles
KINETIC_CSS = KineticElements.get_kinetic_css()

# Base CSS with Professional Editing Suite Features
BASE_CSS = f"""
:root {{
  --fc-black: #0E0C0A;
  --fc-surface: #181512;
  --fc-orange: #FF6B00;
  --fc-gold: #FFA94D;
  --fc-cream: #F5EBE1;
  --fc-muted: #A89F91;
  --fc-red: #D90429;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{
  width: 1080px; height: 1920px;
  background-color: var(--fc-black);
  color: var(--fc-cream);
  overflow: hidden;
  font-family: 'Montserrat', sans-serif;
}}
#viewport {{
  position: relative; width: 1080px; height: 1920px;
  background: #12100E url('{CANVAS_URI}') no-repeat center center / cover;
  perspective: 1200px; overflow: hidden;
}}

/* 35mm Procedural Film Grain Overlay */
.film-grain {{
  position: absolute; inset: 0;
  pointer-events: none; z-index: 950;
  opacity: 0.14;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}}

/* Warm Documentary Corner Light Leak */
.light-leak {{
  position: absolute; top: -140px; right: -140px; width: 750px; height: 750px;
  background: radial-gradient(circle, rgba(255, 120, 30, 0.35) 0%, rgba(255, 107, 0, 0.16) 50%, transparent 75%);
  pointer-events: none; z-index: 920;
  mix-blend-mode: screen;
}}

/* Film Burn Whip-Flash Transition Overlay */
.film-flash {{
  position: absolute; inset: 0;
  background: radial-gradient(circle, rgba(255, 160, 50, 0.95) 0%, rgba(255, 107, 0, 0.5) 60%, transparent 100%);
  pointer-events: none; z-index: 990; opacity: 0;
  mix-blend-mode: screen;
}}

/* Authentic Top Brand Badge */
.brand-badge {{
  position: absolute; top: 90px; left: 50%;
  transform: translateX(-50%);
  display: flex; align-items: center; gap: 14px;
  background: rgba(22, 19, 16, 0.94);
  border: 1.5px solid var(--fc-orange);
  padding: 10px 28px; border-radius: 40px;
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.85);
  z-index: 1000;
}}
.brand-dot {{
  width: 12px; height: 12px; border-radius: 50%;
  background: var(--fc-orange);
  box-shadow: 0 0 16px var(--fc-orange);
}}
.brand-title {{
  font-family: 'Cinzel', serif; font-size: 18px; font-weight: 900;
  letter-spacing: 4px; color: var(--fc-cream);
}}
.brand-code {{
  font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 800;
  color: var(--fc-orange); background: rgba(255, 107, 0, 0.18);
  padding: 3px 10px; border-radius: 6px;
}}

/* Subtle Vignette & Warm Glow */
.cinematic-vignette {{
  position: absolute; inset: 0;
  background: radial-gradient(circle at 50% 50%, transparent 55%, rgba(10, 8, 7, 0.85) 100%);
  pointer-events: none; z-index: 900;
}}
.ambient-glow {{
  position: absolute; top: 46%; left: 50%; transform: translate(-50%, -50%);
  width: 900px; height: 900px;
  background: radial-gradient(circle, rgba(255, 107, 0, 0.14) 0%, transparent 70%);
  pointer-events: none; z-index: 50;
}}

/* MeanwhileMayank Huge Bold Typography */
.headline-box {{
  position: absolute; top: 210px; left: 80px; right: 80px;
  text-align: center; z-index: 800;
}}
.headline-sub {{
  font-family: 'Montserrat', sans-serif; font-size: 17px; font-weight: 800;
  letter-spacing: 5px; color: var(--fc-orange); margin-bottom: 8px; text-transform: uppercase;
}}
.headline-main {{
  font-family: 'Bebas Neue', sans-serif; font-size: 80px; line-height: 0.96;
  letter-spacing: 2px; color: var(--fc-cream); text-transform: uppercase;
  text-shadow: 0 6px 35px rgba(0, 0, 0, 0.95);
}}

/* Tactile Papercraft Stage */
.papercraft-stage {{
  position: absolute; top: 380px; left: 60px;
  width: 960px; height: 980px;
  display: flex; align-items: center; justify-content: center;
  z-index: 200;
  transform-origin: center center;
}}
.hero-cutout {{
  max-width: 860px; max-height: 720px;
  filter: drop-shadow(0 25px 45px rgba(0, 0, 0, 0.9));
  transform-origin: center center;
}}
.secondary-cutout {{
  position: absolute;
  filter: drop-shadow(0 20px 35px rgba(0, 0, 0, 0.85));
  z-index: 240;
  transform-origin: center center;
}}

/* Tactile Props */
.prop-tape {{
  position: absolute;
  width: 220px;
  filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.4));
  z-index: 500;
  pointer-events: none;
  transform-origin: center center;
}}
.prop-pin {{
  position: absolute;
  width: 70px;
  filter: drop-shadow(0 10px 18px rgba(0, 0, 0, 0.7));
  z-index: 600;
  pointer-events: none;
  transform-origin: center center;
}}
.prop-stamp {{
  position: absolute;
  width: 280px;
  filter: drop-shadow(0 6px 15px rgba(0, 0, 0, 0.6));
  z-index: 550;
  pointer-events: none;
  transform-origin: center center;
}}

/* Floating Badges & Callout Labels */
.badge-row {{
  position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 16px; justify-content: center; width: 100%;
  z-index: 300;
}}
.paper-badge {{
  background: rgba(24, 20, 16, 0.95);
  border: 1.5px solid var(--fc-orange);
  padding: 8px 18px; border-radius: 8px;
  font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 800;
  letter-spacing: 1px; color: var(--fc-cream);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.75);
  transform-origin: center center;
}}
.paper-badge.orange {{
  border-color: var(--fc-orange);
  color: #FFFFFF;
  background: #FF6B00;
  box-shadow: 0 0 24px rgba(255, 107, 0, 0.75);
}}

/* Word-by-Word Kinetic Karaoke Subtitle Box */
.caption-box {{
  position: absolute; bottom: 210px; left: 80px; right: 80px;
  background: rgba(18, 15, 12, 0.96);
  border: 1.5px solid rgba(255, 107, 0, 0.5);
  padding: 24px 34px; border-radius: 20px;
  box-shadow: 0 16px 50px rgba(0, 0, 0, 0.92);
  backdrop-filter: blur(12px); z-index: 800;
  text-align: center;
}}
.caption-text {{
  font-family: 'Montserrat', sans-serif; font-size: 30px; line-height: 1.5;
  font-weight: 700; color: #FAF5E8;
}}
.k-word {{
  display: inline-block;
  margin: 0 4px;
  transition: transform 0.08s ease, color 0.08s ease;
}}
.k-word.active {{
  color: #FFFFFF !important;
  font-weight: 900 !important;
  transform: scale(1.18);
  background: #FF6B00;
  padding: 2px 10px;
  border-radius: 6px;
  box-shadow: 0 0 20px rgba(255, 107, 0, 0.85);
}}
.k-word.kw.active {{
  background: #E53E3E;
  box-shadow: 0 0 22px rgba(229, 62, 62, 0.9);
}}
.k-word.spoken {{
  color: #FAF5E8;
  opacity: 0.95;
}}
.k-word.upcoming {{
  color: #8C8276;
  opacity: 0.40;
}}

{KINETIC_CSS}
"""

def build_scene_visual_html(s_id: str) -> str:
    """Builds MeanwhileMayank photographic papercraft collage with kinetic elements."""
    if s_id == "scene_001":
        clock_html = KineticElements.split_flap_clock_html("clock-01")
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img id="hero-card" class="hero-cutout" src="{MACRO_NOODLES_URI}" alt="Ramen Noodles Macro">
          <img id="pin-elem" class="prop-pin" src="{PUSHPIN_URI}" style="top: 130px; left: 470px;" alt="Pushpin">
          
          <div id="clock-container" style="position: absolute; top: 30px; right: 20px; transform: rotate(5deg);">
            {clock_html}
          </div>
          <img id="tape-elem" class="prop-tape" src="{SCOTCH_TAPE_URI}" style="top: 15px; right: 90px; transform: rotate(-3deg);" alt="Scotch Tape">
          
          <img id="stamp-elem" class="prop-stamp" src="{RUBBER_STAMP_URI}" style="bottom: 120px; left: 40px; transform: rotate(-8deg);" alt="Evidence Stamp">
          
          <div class="badge-row">
            <span id="badge-1" class="paper-badge orange">DEEP FRIED & DEHYDRATED</span>
            <span id="badge-2" class="paper-badge">REFINED WHEAT (MAIDA)</span>
          </div>
        </div>
        """
    elif s_id == "scene_002":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img id="sec-card" class="secondary-cutout" src="{RAMEN_NOODLES_URI}" style="top: 30px; left: 20px; width: 380px; transform: rotate(-5deg); opacity: 0.9;" alt="Noodle Strands">
          <img id="pin-elem" class="prop-pin" src="{PUSHPIN_URI}" style="top: 15px; left: 190px;" alt="Pushpin">
          
          <img id="hero-card" class="hero-cutout" src="{MOUTH_ENZYME_URI}" style="margin-top: 120px;" alt="Salivary Amylase">
          <img id="tape-elem" class="prop-tape" src="{SCOTCH_TAPE_URI}" style="top: 230px; right: 120px; transform: rotate(12deg);" alt="Tape">
          <img id="stamp-elem" class="prop-stamp" src="{RUBBER_STAMP_URI}" style="bottom: 110px; right: 40px; transform: rotate(-5deg);" alt="Evidence Stamp">
          
          <div class="badge-row">
            <span id="badge-1" class="paper-badge orange">SALIVARY AMYLASE (PTYALIN)</span>
            <span id="badge-2" class="paper-badge">STARCH → DISACCHARIDES</span>
          </div>
        </div>
        """
    elif s_id == "scene_003":
        clock_html = KineticElements.split_flap_clock_html("clock-03")
        acid_bubbles = KineticElements.bubbling_acid_svg()
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img id="hero-card" class="hero-cutout" src="{STOMACH_URI}" alt="Stomach Anatomy">
          {acid_bubbles}
          <img id="pin-elem" class="prop-pin" src="{PUSHPIN_URI}" style="top: 120px; left: 490px;" alt="Pushpin">
          
          <div id="clock-container" style="position: absolute; top: 30px; left: 20px; transform: rotate(-6deg);">
            {clock_html}
          </div>
          <img id="tape-elem" class="prop-tape" src="{SCOTCH_TAPE_URI}" style="top: 15px; left: 80px; transform: rotate(-2deg);" alt="Tape">
          
          <img id="stamp-elem" class="prop-stamp" src="{RUBBER_STAMP_URI}" style="bottom: 110px; right: 40px; transform: rotate(6deg);" alt="Warning Stamp">
          
          <div class="badge-row">
            <span id="badge-1" class="paper-badge orange">HYDROCHLORIC ACID (pH 1.5 - 2.0)</span>
            <span id="badge-2" class="paper-badge">GASTRIC PERISTALSIS</span>
          </div>
        </div>
        """
    elif s_id == "scene_004":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img id="sec-card" class="secondary-cutout" src="{MACRO_NOODLES_URI}" style="top: 20px; right: 30px; width: 280px; transform: rotate(6deg); opacity: 0.85;" alt="Noodles">
          <img id="tape-elem" class="prop-tape" src="{SCOTCH_TAPE_URI}" style="top: 10px; right: 80px; transform: rotate(-4deg);" alt="Tape">
          
          <img id="hero-card" class="hero-cutout" src="{INTESTINE_URI}" style="margin-top: 20px;" alt="Intestinal Brush Border">
          <img id="mol-elem" class="secondary-cutout" src="{VORK_3D_MOLECULE_URI}" style="top: 220px; right: 30px; width: 330px;" alt="3D Glucose Molecule">
          
          <img id="pin-elem" class="prop-pin" src="{PUSHPIN_URI}" style="top: 140px; left: 320px;" alt="Pushpin">
          <img id="stamp-elem" class="prop-stamp" src="{RUBBER_STAMP_URI}" style="bottom: 110px; left: 40px; transform: rotate(7deg);" alt="Warning Stamp">
          
          <div class="badge-row">
            <span id="badge-1" class="paper-badge orange">PANCREATIC ENZYMES</span>
            <span id="badge-2" class="paper-badge">RAPID GLUCOSE SPIKE</span>
          </div>
        </div>
        """
    elif s_id == "scene_005":
        clock_html = KineticElements.split_flap_clock_html("clock-05")
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <div id="clock-container" style="position: absolute; top: 20px; left: 30px; transform: rotate(-5deg);">
            {clock_html}
          </div>
          <img id="tape-elem" class="prop-tape" src="{SCOTCH_TAPE_URI}" style="top: 10px; left: 90px; transform: rotate(3deg);" alt="Tape">
          
          <img id="hero-card" class="hero-cutout" src="{BLOODSTREAM_URI}" style="margin-top: 20px;" alt="Bloodstream Absorption">
          <img id="mol-elem" class="secondary-cutout" src="{VORK_3D_MOLECULE_URI}" style="top: 240px; left: 40px; width: 310px;" alt="3D Glucose Molecule">
          
          <img id="pin-elem" class="prop-pin" src="{PUSHPIN_URI}" style="top: 150px; right: 340px;" alt="Pushpin">
          <img id="stamp-elem" class="prop-stamp" src="{RUBBER_STAMP_URI}" style="bottom: 110px; right: 40px; transform: rotate(-6deg);" alt="Warning Stamp">
          
          <div class="badge-row">
            <span id="badge-1" class="paper-badge orange">GLYCEMIC SURGE</span>
            <span id="badge-2" class="paper-badge">INSULIN RESPONSE • CELLULAR ENERGY</span>
          </div>
        </div>
        """
    elif s_id == "scene_006":
        laser_html = KineticElements.scanning_laser_html()
        odometer_html = KineticElements.kinetic_odometer_html("odo-sodium")
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <div id="nutrition-wrap" style="position: relative;">
            <img id="hero-card" class="hero-cutout" src="{NUTRITION_LABEL_URI}" alt="Nutrition Label">
            {laser_html}
          </div>
          <img id="tape-elem-1" class="prop-tape" src="{SCOTCH_TAPE_URI}" style="top: 140px; left: 240px; transform: rotate(-18deg);" alt="Tape Left">
          <img id="tape-elem-2" class="prop-tape" src="{SCOTCH_TAPE_URI}" style="top: 140px; right: 240px; transform: rotate(18deg);" alt="Tape Right">
          
          <div id="odometer-container" style="position: absolute; bottom: 80px; left: 50%; transform: translateX(-50%); width: 440px;">
            {odometer_html}
          </div>
          
          <img id="stamp-elem" class="prop-stamp" src="{RUBBER_STAMP_URI}" style="top: 420px; right: 80px; transform: rotate(10deg);" alt="Stamp Warning">
          <img id="pin-elem" class="prop-pin" src="{PUSHPIN_URI}" style="top: 120px; left: 450px;" alt="Pushpin">
          
          <div class="badge-row" style="bottom: 10px;">
            <span id="badge-1" class="paper-badge orange">SODIUM: ~1760mg (76% DV)</span>
            <span id="badge-2" class="paper-badge">SEASONING OIL SACHET</span>
          </div>
        </div>
        """
    elif s_id == "scene_007":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img id="sec-card" class="secondary-cutout" src="{NUTRITION_LABEL_URI}" style="top: 20px; left: 20px; width: 280px; transform: rotate(-8deg); opacity: 0.85;" alt="Nutrition Label">
          <img id="tape-elem" class="prop-tape" src="{SCOTCH_TAPE_URI}" style="top: 10px; left: 80px; transform: rotate(4deg);" alt="Tape">
          
          <img id="hero-card" class="hero-cutout" src="{BALANCED_BOWL_URI}" style="margin-top: 10px; max-width: 650px; max-height: 650px;" alt="Balanced Bowl">
          <img id="pin-elem" class="prop-pin" src="{PUSHPIN_URI}" style="top: 140px; right: 380px;" alt="Pushpin">
          <img id="stamp-elem" class="prop-stamp" src="{RUBBER_STAMP_URI}" style="bottom: 110px; left: 40px; transform: rotate(6deg);" alt="Warning Stamp">
          
          <div class="badge-row">
            <span id="badge-1" class="paper-badge orange">+ PROTEIN (BOILED EGG)</span>
            <span id="badge-2" class="paper-badge">+ FIBER (BOK CHOY & GREENS)</span>
          </div>
        </div>
        """
    elif s_id == "scene_008":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img id="hero-card" class="hero-cutout" src="{VORK_3D_CREST_URI}" style="max-width: 680px; max-height: 680px; filter: drop-shadow(0 25px 60px rgba(0, 0, 0, 0.98));" alt="Food Code 3D Gold Seal">
          <img id="pin-elem" class="prop-pin" src="{PUSHPIN_URI}" style="top: 140px; left: 450px;" alt="Pushpin">
          <img id="tape-elem" class="prop-tape" src="{SCOTCH_TAPE_URI}" style="top: 160px; right: 210px; transform: rotate(15deg);" alt="Tape">
          
          <img id="sec-card" class="secondary-cutout" src="{BALANCED_BOWL_URI}" style="bottom: 40px; right: 30px; width: 320px; transform: rotate(6deg);" alt="Bowl Accent">
          <img id="stamp-elem" class="prop-stamp" src="{RUBBER_STAMP_URI}" style="bottom: 120px; left: 40px; transform: rotate(-6deg);" alt="Stamp">
          
          <div class="badge-row">
            <span id="badge-1" class="paper-badge orange">SCIENCE > FEAR</span>
            <span id="badge-2" class="paper-badge">EVIDENCE-BASED NUTRITION</span>
          </div>
        </div>
        """
    return "<div></div>"

def generate_scene_stage(scene: dict, scene_idx: int) -> Path:
    s_id = scene["scene_id"]
    dur = scene["duration"]
    stage_path = stages_dir / s_id
    stage_path.mkdir(parents=True, exist_ok=True)
    
    # Save style.css
    with open(stage_path / "style.css", "w", encoding="utf-8") as f:
        f.write(BASE_CSS)
        
    visual_html = build_scene_visual_html(s_id)
    
    # Build word-by-word karaoke subtitle HTML
    words = scene["narration"].split()
    word_spans = []
    for w_idx, w in enumerate(words):
        is_kw = any(re.search(r'\b' + re.escape(kw) + r'\b', w, re.I) for kw in scene["keywords"])
        kw_class = " kw" if is_kw else ""
        word_spans.append(f'<span class="k-word{kw_class}" id="w-{scene_idx}-{w_idx}">{w}</span>')
    karaoke_html = " ".join(word_spans)
    
    # Build timeline.js with spring physics, 12 FPS jitter, camera impact shakes, and karaoke subtitle sync
    cam = scene["camera"]
    z_start = cam.get("zoom_start", 1.0)
    z_end = cam.get("zoom_end", 1.10)
    movement = cam.get("movement", "slow_dolly_in")
    
    helpers_js = KineticElements.get_kinetic_js_helpers()
    
    js_content = f"""
    {helpers_js}
    
    let currentTime = 0.0;
    const TOTAL_DURATION = {dur};
    const WORD_COUNT = {len(words)};
    
    window.setSeekTime = function(t) {{
      currentTime = Math.max(0.0, Math.min(TOTAL_DURATION, t));
      const p = currentTime / TOTAL_DURATION;
      // Smooth cubic ease out for camera
      const easeP = 1.0 - Math.pow(1.0 - p, 3);
      const zoom = {z_start} + ({z_end} - {z_start}) * easeP;
      
      let panX = 0, panY = 0;
      let rot = 0;
      if ('{movement}' === 'pan_right') {{
        panX = -45 * easeP;
      }} else if ('{movement}' === 'pan_left') {{
        panX = 45 * easeP;
      }} else if ('{movement}' === 'tilt_down') {{
        panY = -35 * easeP;
      }} else if ('{movement}' === 'fast_push_in') {{
        panY = -20 * easeP;
        rot = Math.sin(p * Math.PI) * 1.2;
      }} else if ('{movement}' === 'subtle_orbit') {{
        panX = 18 * Math.sin(p * Math.PI);
        panY = 10 * Math.cos(p * Math.PI) - 10;
        rot = 0.8 * Math.sin(p * Math.PI);
      }}
      
      // Camera Impact Shake (Triggered by Stamp Slam at t = 0.85s - 1.05s)
      let impactShake = 0;
      if (currentTime >= 0.85 && currentTime <= 1.05) {{
        const shakeP = (currentTime - 0.85) / 0.20;
        impactShake = Math.sin(shakeP * Math.PI * 8) * (1.0 - shakeP) * 5.0;
      }}
      
      // Stop-Motion Frame Jitter Engine (Quantized to 12 FPS)
      const frameNum = Math.floor(currentTime * 30);
      const jitterCycle = Math.floor(frameNum / 2.5);
      const hash = Math.sin(jitterCycle * 12.9898 + 78.233) * 43758.5453;
      const jitterRot = ((hash - Math.floor(hash)) - 0.5) * 1.2;
      const jitterX = (((hash * 10) - Math.floor(hash * 10)) - 0.5) * 2.6;
      const jitterY = (((hash * 100) - Math.floor(hash * 100)) - 0.5) * 2.6;
      
      const st = document.getElementById('stage-asset');
      if (st) {{
        const finalX = (panX + jitterX).toFixed(2);
        const finalY = (panY + jitterY + impactShake).toFixed(2);
        const finalRot = (rot + jitterRot).toFixed(2);
        st.style.transform = `translate3d(${{finalX}}px, ${{finalY}}px, 0px) scale(${{zoom.toFixed(4)}}) rotate(${{finalRot}}deg)`;
      }}
      
      // Film Flash Transition on Scene Exit (Final 0.22s)
      const flash = document.getElementById('film-flash');
      if (flash) {{
        if (currentTime >= TOTAL_DURATION - 0.22) {{
          const flashP = (currentTime - (TOTAL_DURATION - 0.22)) / 0.22;
          flash.style.opacity = (Math.sin(flashP * Math.PI) * 0.70).toFixed(2);
        }} else {{
          flash.style.opacity = '0';
        }}
      }}
      
      // 1. Spring Entry on Hero Cutout
      const hero = document.getElementById('hero-card');
      if (hero) {{
        const entryP = clamp(currentTime / 0.42, 0, 1);
        const spring = springBounce(entryP);
        const dropY = (1.0 - spring) * -90;
        const entryScale = 0.88 + 0.12 * spring;
        hero.style.transform = `translateY(${{dropY.toFixed(2)}}px) scale(${{entryScale.toFixed(4)}})`;
      }}
      
      // 2. Pushpin Slam
      const pin = document.getElementById('pin-elem');
      if (pin) {{
        const pinP = clamp((currentTime - 0.35) / 0.22, 0, 1);
        const pScale = springBounce(pinP);
        pin.style.transform = `scale(${{pScale.toFixed(3)}})`;
        pin.style.opacity = pinP > 0 ? '1' : '0';
      }}
      
      // 3. Scotch Tape Slap
      const tape = document.getElementById('tape-elem');
      if (tape) {{
        const tapeP = clamp((currentTime - 0.25) / 0.22, 0, 1);
        const tScale = springBounce(tapeP);
        tape.style.transform = `scale(${{tScale.toFixed(3)}})`;
        tape.style.opacity = tapeP > 0 ? '1' : '0';
      }}
      
      // 4. Rubber Stamp Slam Impact
      const stamp = document.getElementById('stamp-elem');
      if (stamp) {{
        const stampP = clamp((currentTime - 0.85) / 0.22, 0, 1);
        if (stampP <= 0) {{
          stamp.style.opacity = '0';
        }} else {{
          const sScale = 2.2 - 1.2 * springBounce(stampP);
          stamp.style.opacity = '0.94';
          stamp.style.transform = `scale(${{sScale.toFixed(3)}}) rotate(-6deg)`;
        }}
      }}
      
      // 5. Secondary Cutout Follow-Through Physics (CineCode / Vox Style)
      const sec = document.getElementById('sec-card');
      if (sec) {{
        const secP = clamp((currentTime - 0.12) / 0.38, 0, 1);
        const secSpring = springBounce(secP);
        const secDropY = (1.0 - secSpring) * -45;
        const secScale = 0.88 + 0.12 * secSpring;
        sec.style.transform = `translateY(${{secDropY.toFixed(2)}}px) scale(${{secScale.toFixed(4)}})`;
        sec.style.opacity = secP > 0 ? '0.92' : '0';
      }}

      // 6. Sequential Tactile Badge Landings
      const b1 = document.getElementById('badge-1');
      const b2 = document.getElementById('badge-2');
      if (b1) {{
        const p1 = clamp((currentTime - 0.30) / 0.28, 0, 1);
        b1.style.transform = `scale(${{springBounce(p1).toFixed(3)}})`;
        b1.style.opacity = p1 > 0 ? '1' : '0';
      }}
      if (b2) {{
        const p2 = clamp((currentTime - 0.52) / 0.28, 0, 1);
        b2.style.transform = `scale(${{springBounce(p2).toFixed(3)}})`;
        b2.style.opacity = p2 > 0 ? '1' : '0';
      }}

      // 7. Mechanical Flip Clock Pop-in
      const clockBox = document.getElementById('clock-container');
      if (clockBox) {{
        const cP = clamp(currentTime / 0.30, 0, 1);
        clockBox.style.transform = `scale(${{springBounce(cP).toFixed(3)}})`;
      }}

      // 8. 3D Vork Molecule Floating Animation
      const mol = document.getElementById('mol-elem');
      if (mol) {{
        const molP = clamp((currentTime - 0.20) / 0.40, 0, 1);
        const mSpring = springBounce(molP);
        const mFloat = Math.sin(currentTime * 3.5) * 12.0;
        const mRot = Math.cos(currentTime * 2.0) * 6.0;
        mol.style.transform = `scale(${{mSpring.toFixed(3)}}) translateY(${{mFloat.toFixed(2)}}px) rotate(${{mRot.toFixed(2)}}deg)`;
        mol.style.opacity = molP > 0 ? '0.96' : '0';
      }}

      // 9. Scene-Specific Kinetic Motions
      if ('{s_id}' === 'scene_001') {{
        const sec = Math.floor(currentTime * 12);
        const m2 = document.getElementById('clock-01-m2');
        const m1 = document.getElementById('clock-01-m1');
        if (m2) m2.innerText = (sec % 10);
        if (m1) m1.innerText = Math.floor((sec / 10) % 6);
      }}
      else if ('{s_id}' === 'scene_003') {{
        for (let b = 0; b < 12; b++) {{
          const bub = document.getElementById('acid-bub-' + b);
          if (bub) {{
            const cycle = (currentTime * 45 + b * 18) % 100;
            bub.setAttribute('cy', (140 - cycle).toFixed(1));
            bub.setAttribute('opacity', (1.0 - cycle / 100).toFixed(2));
          }}
        }}
        const hr = Math.floor((currentTime / TOTAL_DURATION) * 2.0);
        const h2 = document.getElementById('clock-03-h2');
        if (h2) h2.innerText = hr;
      }}
      else if ('{s_id}' === 'scene_006') {{
        const laser = document.getElementById('doc-laser');
        if (laser) {{
          const laserP = clamp((currentTime - 0.4) / 1.8, 0, 1);
          laser.style.top = (laserP * 560).toFixed(1) + 'px';
          laser.style.opacity = (currentTime >= 0.4 && currentTime <= 2.4) ? '1' : '0';
        }}
        const odoVal = document.getElementById('odo-sodium-val');
        const odoPct = document.getElementById('odo-sodium-pct');
        const odoBar = document.getElementById('odo-sodium-bar');
        if (odoVal && odoPct && odoBar) {{
          const odoP = clamp((currentTime - 0.5) / 2.2, 0, 1);
          const easedOdo = springBounce(odoP);
          const currentMg = Math.floor(easedOdo * 1760);
          const currentPercent = Math.floor(easedOdo * 76);
          odoVal.innerText = currentMg.toLocaleString();
          odoPct.innerText = currentPercent + '%';
          odoBar.style.width = currentPercent + '%';
        }}
      }}
      else if ('{s_id}' === 'scene_007') {{
        const b1 = document.getElementById('badge-1');
        const b2 = document.getElementById('badge-2');
        if (b1) {{
          const p1 = clamp((currentTime - 0.6) / 0.3, 0, 1);
          b1.style.transform = `scale(${{springBounce(p1).toFixed(3)}})`;
        }}
        if (b2) {{
          const p2 = clamp((currentTime - 1.4) / 0.3, 0, 1);
          b2.style.transform = `scale(${{springBounce(p2).toFixed(3)}})`;
        }}
      }}
      
      // 6. Word-by-Word Kinetic Karaoke Subtitle Engine
      const activeWordIdx = Math.floor((currentTime / TOTAL_DURATION) * WORD_COUNT);
      for (let w = 0; w < WORD_COUNT; w++) {{
        const wElem = document.getElementById(`w-{scene_idx}-` + w);
        if (wElem) {{
          if (w === activeWordIdx) {{
            wElem.className = wElem.className.replace(/\\s*(active|spoken|upcoming)/g, '') + ' active';
          }} else if (w < activeWordIdx) {{
            wElem.className = wElem.className.replace(/\\s*(active|spoken|upcoming)/g, '') + ' spoken';
          }} else {{
            wElem.className = wElem.className.replace(/\\s*(active|spoken|upcoming)/g, '') + ' upcoming';
          }}
        }}
      }}
    }};
    window.getCurrentTime = () => currentTime;
    window.getTotalDuration = () => TOTAL_DURATION;
    document.addEventListener('DOMContentLoaded', () => window.setSeekTime(0.0));
    """
    with open(stage_path / "timeline.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="style.css">
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cinzel:wght@700;900&family=Montserrat:wght@400;600;700;800;900&family=JetBrains+Mono:wght@700;800&display=swap" rel="stylesheet">
</head>
<body>
  <div id="viewport">
    <div class="film-grain"></div>
    <div class="light-leak"></div>
    <div class="film-flash" id="film-flash"></div>
    
    <div class="brand-badge">
      <div class="brand-dot"></div>
      <span class="brand-title">FOOD CODE</span>
      <span class="brand-code">EP 001 • SCENE {scene_idx+1:02d}</span>
    </div>
    <div class="cinematic-vignette"></div>
    <div class="ambient-glow"></div>
    
    <div class="headline-box">
      <div class="headline-sub">{scene['typography']['headline_sub']}</div>
      <div class="headline-main">{scene['typography']['headline_main']}</div>
    </div>
    
    <div class="papercraft-stage" id="stage-asset">
      {visual_html}
    </div>
    
    <div class="caption-box">
      <div class="caption-text">{karaoke_html}</div>
    </div>
  </div>
  <script src="timeline.js"></script>
</body>
</html>"""
    
    html_file = stage_path / "index.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
    return html_file

# Step 1: Render each scene in batches
rendered_scenes = []
print(f"📦 Total Scenes to Render in Batch: {len(scenes)}")

for i, sc in enumerate(scenes):
    s_id = sc["scene_id"]
    dur = sc["duration"]
    scene_mp4 = batch_dir / f"{s_id}.mp4"
    print(f"\n🎬 [Batch {i+1}/8] Preparing {s_id} ({sc['title']}) — Duration: {dur}s...")
    
    html_path = generate_scene_stage(sc, i)
    
    force_render = "--force" in sys.argv
    if not force_render and scene_mp4.exists() and scene_mp4.stat().st_size > 500000:
        print(f"       -> [CACHED] {s_id}.mp4 already rendered ({scene_mp4.stat().st_size / 1024 / 1024:.2f} MB). Skipping CDP render.")
        rendered_scenes.append(scene_mp4)
        continue
        
    cmd = [
        "node",
        str(render_js),
        "--html", str(html_path.resolve()),
        "--output", str(scene_mp4.resolve()),
        "--duration", str(dur),
        "--fps", "30"
    ]
    
    print(f"       -> Launching CDP memory render for {s_id}...")
    start_t = time.time()
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"       -> [ERROR] Render failed for {s_id}: {res.stderr}")
        raise RuntimeError(f"Scene {s_id} render failed")
        
    el = time.time() - start_t
    print(f"       -> [SUCCESS] Rendered {s_id}.mp4 in {el:.1f}s ({scene_mp4.stat().st_size / 1024 / 1024:.2f} MB)")
    rendered_scenes.append(scene_mp4)

# Step 2: Synthesize Synchronized CineCode Foley & Master Soundtrack
print("\n🎧 [CineCode Foley Suite] Synthesizing synchronized tactile sound effects & BGM...")
foley_engine = CineCodeFoleyEngine(sample_rate=44100)
narration_wav = proj_dir / "narration.wav"
foley_master_mp3 = proj_dir / "soundtrack_foley_master.mp3"

scene_starts = [0.0]
for sc_item in scenes[:-1]:
    scene_starts.append(scene_starts[-1] + sc_item["duration"])

master_soundtrack = foley_engine.mix_production_soundtrack(
    voiceover_wav=narration_wav,
    output_path=foley_master_mp3,
    total_duration=57.46,
    scene_starts=scene_starts,
    bgm_volume=0.18,
    foley_volume=0.35,
    ducking_ratio=0.32
)
print(f"       -> [SUCCESS] Synthesized CineCode master audio with Foley: {master_soundtrack}")

# Step 3: Losslessly stitch scenes with master audio
print("\n🔗 [Stitching] Assembling all 8 scenes losslessly with master soundtrack...")
master_stitched_mp4 = output_dir / "instant_noodles_batch_master.mp4"
stitcher = BatchStitcher()

final_video = stitcher.stitch_scenes(
    scene_files=rendered_scenes,
    output_mp4=master_stitched_mp4,
    master_audio=master_soundtrack,
    transition="direct_cut"
)
print(f"       -> [SUCCESS] Master stitched video produced: {final_video}")

# Step 4: Run Quality Control
print("\n🔍 [Quality Control] Validating stitched master video...")
qc = QualityValidator()
qc_report = qc.inspect_video(final_video, expected_duration=57.46)
qc_path = output_dir / "quality_report_batch.json"
qc_report.save_json(qc_path)
print(f"       -> QC Status: {qc_report.status}")
print(f"       -> Resolution: {qc_report.resolution}")
print(f"       -> Framerate: {qc_report.framerate} FPS")
print(f"       -> Duration: {qc_report.duration:.2f}s")
print(f"       -> Loudness: {qc_report.integrated_lufs} LUFS (Peak: {qc_report.true_peak_db} dBTP)")
print(f"       -> Black Frames: {qc_report.black_frame_count}")

# Step 5: Run Aesthetic Judge Self-Evaluation
print("\n🎨 [Aesthetic Judge] Running visual critic & scoring against viral documentary standard...")
judge = AestheticJudge()
aesthetic_report = judge.judge_video(final_video, scene_count=8)
aesthetic_path = output_dir / "aesthetic_report.json"
with open(aesthetic_path, "w", encoding="utf-8") as f:
    json.dump(aesthetic_report, f, indent=2)
print(f"       -> Average Aesthetic Score: {aesthetic_report['average_aesthetic_score']}/100")
print(f"       -> Viral Ready: {aesthetic_report['viral_ready']}")
for sc_res in aesthetic_report["scenes"]:
    print(f"          Scene {sc_res['scene_index']:02d}: {sc_res['composite_score']} pts ({sc_res['status']})")

# Step 6: CineCode Hard QC Validation
cinecode_qc = repo_root.parent / "cinecode" / "scripts" / "qc.py"
if not cinecode_qc.exists():
    cinecode_qc = repo_root / "cinecode" / "scripts" / "qc.py"
if cinecode_qc.exists():
    print("\n⚡ [CineCode QC Suite] Testing Hook & Loudness against CineCode rules...")
    try:
        hook_cmd = ["python", str(cinecode_qc), "hook", str(final_video)]
        hook_res = subprocess.run(hook_cmd, capture_output=True, text=True)
        print(f"       -> Hook Check:\n{hook_res.stdout.strip()}")
        loud_cmd = ["python", str(cinecode_qc), "loud", str(final_video)]
        loud_res = subprocess.run(loud_cmd, capture_output=True, text=True)
        print(f"       -> Loudness Check:\n{loud_res.stdout.strip()}")
    except Exception as e:
        print(f"       -> CineCode QC notice: {e}")

print("\n=================================================================")
print("✅ PROFESSIONAL DOCUMENTARY EDITING SUITE PRODUCTION COMPLETE!")
print(f"   Deliverable: {final_video}")
print("=================================================================\n")
