"""
Batch-by-Batch Modular Production Engine for Food Code Episode 001.
Renders each scene independently with authentic MeanwhileMayank / Vox
Photographic Papercraft Collage assets and stitches them losslessly.
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
print("🎬 FOOD CODE 001 — AUTHENTIC PHOTOGRAPHIC PAPERCRAFT COLLAGE")
print("=================================================================\n")

# Asset URI helpers
def get_asset_uri(name: str) -> str:
    path = assets_dir / name
    if not path.exists():
        raise FileNotFoundError(f"Missing photographic asset: {path}")
    return path.resolve().as_uri()

CANVAS_URI = get_asset_uri("notebook_canvas.jpg")
FLIP_CLOCK_URI = get_asset_uri("flip_clock_card.png")
MACRO_NOODLES_URI = get_asset_uri("macro_noodles_sticker.png")
RAMEN_NOODLES_URI = get_asset_uri("ramen_noodles_cutout.png")
MOUTH_ENZYME_URI = get_asset_uri("mouth_enzyme_cutout.png")
STOMACH_URI = get_asset_uri("stomach_anatomy_cutout.png")
INTESTINE_URI = get_asset_uri("intestine_sugars_cutout.png")
BLOODSTREAM_URI = get_asset_uri("bloodstream_absorption_cutout.png")
NUTRITION_LABEL_URI = get_asset_uri("nutrition_label_cutout.png")
BALANCED_BOWL_URI = get_asset_uri("balanced_bowl_cutout.png")
HERO_CREST_URI = get_asset_uri("science_foodcode_crest.png")

# Base CSS with MeanwhileMayank / Vox aesthetic
BASE_CSS = f"""
:root {{
  --fc-black: #0E0C0A;
  --fc-surface: #181512;
  --fc-orange: #FF6B00;
  --fc-gold: #FFA94D;
  --fc-cream: #F5EBE1;
  --fc-muted: #A89F91;
  --fc-red: #8B3524;
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
  background: radial-gradient(circle, rgba(255, 107, 0, 0.12) 0%, transparent 70%);
  pointer-events: none; z-index: 50;
}}

/* MeanwhileMayank Huge Bold Typography */
.headline-box {{
  position: absolute; top: 220px; left: 80px; right: 80px;
  text-align: center; z-index: 800;
}}
.headline-sub {{
  font-family: 'Montserrat', sans-serif; font-size: 17px; font-weight: 800;
  letter-spacing: 5px; color: var(--fc-orange); margin-bottom: 8px; text-transform: uppercase;
}}
.headline-main {{
  font-family: 'Bebas Neue', sans-serif; font-size: 78px; line-height: 0.98;
  letter-spacing: 2px; color: var(--fc-cream); text-transform: uppercase;
  text-shadow: 0 6px 35px rgba(0, 0, 0, 0.95);
}}

/* Tactile Papercraft Stage */
.papercraft-stage {{
  position: absolute; top: 400px; left: 60px;
  width: 960px; height: 960px;
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
  z-index: 250;
}}

/* Floating Badges & Callout Labels */
.badge-row {{
  position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 16px; justify-content: center; width: 100%;
  z-index: 300;
}}
.paper-badge {{
  background: rgba(24, 20, 16, 0.94);
  border: 1.5px solid var(--fc-cream);
  padding: 8px 18px; border-radius: 8px;
  font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 800;
  letter-spacing: 1px; color: var(--fc-cream);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.75);
}}
.paper-badge.orange {{
  border-color: var(--fc-orange);
  color: var(--fc-orange);
  background: rgba(35, 18, 10, 0.95);
}}

/* Bottom Editorial Caption Box */
.caption-box {{
  position: absolute; bottom: 230px; left: 80px; right: 80px;
  background: rgba(20, 17, 14, 0.94);
  border: 1.5px solid rgba(255, 107, 0, 0.45);
  padding: 24px 34px; border-radius: 20px;
  box-shadow: 0 14px 50px rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(12px); z-index: 800;
}}
.caption-text {{
  font-family: 'Montserrat', sans-serif; font-size: 28px; line-height: 1.45;
  font-weight: 700; color: var(--fc-cream); text-align: center;
}}
.caption-text .highlight {{
  color: var(--fc-orange); font-weight: 900;
  text-shadow: 0 0 18px rgba(255, 107, 0, 0.65);
}}
"""

def build_scene_visual_html(s_id: str) -> str:
    """Builds MeanwhileMayank photographic papercraft collage DOM elements for each scene."""
    if s_id == "scene_001":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img class="hero-cutout" src="{MACRO_NOODLES_URI}" alt="Ramen Noodles Macro">
          <img class="secondary-cutout" src="{FLIP_CLOCK_URI}" style="top: 20px; right: 20px; width: 320px; transform: rotate(4deg);" alt="Split Flap Clock">
          <div class="badge-row">
            <span class="paper-badge orange">DEEP FRIED & DEHYDRATED</span>
            <span class="paper-badge">REFINED WHEAT (MAIDA)</span>
          </div>
        </div>
        """
    elif s_id == "scene_002":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img class="hero-cutout" src="{MOUTH_ENZYME_URI}" alt="Salivary Amylase">
          <img class="secondary-cutout" src="{RAMEN_NOODLES_URI}" style="bottom: 80px; left: 10px; width: 280px; transform: rotate(-6deg); opacity: 0.85;" alt="Noodle Strands">
          <div class="badge-row">
            <span class="paper-badge orange">SALIVARY AMYLASE (PTYALIN)</span>
            <span class="paper-badge">pH 6.8 OPTIMAL</span>
          </div>
        </div>
        """
    elif s_id == "scene_003":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img class="hero-cutout" src="{STOMACH_URI}" alt="Stomach Anatomy">
          <img class="secondary-cutout" src="{FLIP_CLOCK_URI}" style="top: 30px; left: 30px; width: 300px; transform: rotate(-5deg);" alt="Split Flap Clock">
          <div class="badge-row">
            <span class="paper-badge orange">HYDROCHLORIC ACID (pH 1.5 - 2.0)</span>
            <span class="paper-badge">GASTRIC PERISTALSIS</span>
          </div>
        </div>
        """
    elif s_id == "scene_004":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img class="hero-cutout" src="{INTESTINE_URI}" alt="Intestinal Brush Border">
          <div class="badge-row">
            <span class="paper-badge orange">PANCREATIC ENZYMES</span>
            <span class="paper-badge">MALTOSE → GLUCOSE</span>
          </div>
        </div>
        """
    elif s_id == "scene_005":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img class="hero-cutout" src="{BLOODSTREAM_URI}" alt="Bloodstream Absorption">
          <div class="badge-row">
            <span class="paper-badge orange">GLYCEMIC SURGE</span>
            <span class="paper-badge">INSULIN RESPONSE • CELLULAR ENERGY</span>
          </div>
        </div>
        """
    elif s_id == "scene_006":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img class="hero-cutout" src="{NUTRITION_LABEL_URI}" alt="Nutrition Label">
          <div class="badge-row">
            <span class="paper-badge orange">SODIUM: ~1760mg (76% DV)</span>
            <span class="paper-badge">SEASONING OIL SACHET</span>
          </div>
        </div>
        """
    elif s_id == "scene_007":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img class="hero-cutout" src="{BALANCED_BOWL_URI}" alt="Balanced Bowl">
          <div class="badge-row">
            <span class="paper-badge orange">+ PROTEIN (BOILED EGG)</span>
            <span class="paper-badge">+ FIBER (BOK CHOY & GREENS)</span>
          </div>
        </div>
        """
    elif s_id == "scene_008":
        return f"""
        <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
          <img class="hero-cutout" src="{HERO_CREST_URI}" alt="Food Code Crest">
          <img class="secondary-cutout" src="{BALANCED_BOWL_URI}" style="bottom: 20px; right: 20px; width: 280px; transform: rotate(5deg); opacity: 0.85;" alt="Balanced Bowl Accent">
          <div class="badge-row">
            <span class="paper-badge orange">SCIENCE > FEAR</span>
            <span class="paper-badge">EVIDENCE-BASED NUTRITION</span>
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
    
    # Build timeline.js with cinematic ease and parallax drift
    cam = scene["camera"]
    z_start = cam.get("zoom_start", 1.0)
    z_end = cam.get("zoom_end", 1.10)
    movement = cam.get("movement", "slow_dolly_in")
    
    js_content = f"""
    let currentTime = 0.0;
    const TOTAL_DURATION = {dur};
    window.setSeekTime = function(t) {{
      currentTime = Math.max(0.0, Math.min(TOTAL_DURATION, t));
      const p = currentTime / TOTAL_DURATION;
      // Smooth cubic ease out
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
      
      const st = document.getElementById('stage-asset');
      if (st) {{
        st.style.transform = `translate3d(${{panX.toFixed(2)}}px, ${{panY.toFixed(2)}}px, 0px) scale(${{zoom.toFixed(4)}}) rotate(${{rot.toFixed(2)}}deg)`;
      }}
    }};
    window.getCurrentTime = () => currentTime;
    window.getTotalDuration = () => TOTAL_DURATION;
    document.addEventListener('DOMContentLoaded', () => window.setSeekTime(0.0));
    """
    with open(stage_path / "timeline.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    # Build index.html
    highlighted_text = scene["narration"]
    for kw in scene["keywords"]:
        highlighted_text = re.sub(f"({re.escape(kw)})", r'<span class="highlight">\1</span>', highlighted_text, flags=re.IGNORECASE)
        
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="style.css">
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cinzel:wght@700;900&family=Montserrat:wght@400;600;700;800;900&family=JetBrains+Mono:wght@700;800&display=swap" rel="stylesheet">
</head>
<body>
  <div id="viewport">
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
      <div class="caption-text">{highlighted_text}</div>
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

# Step 2: Losslessly stitch scenes with master audio
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

# Step 3: Run Quality Control
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

print("\n=================================================================")
print("✅ BATCH-BY-BATCH PRODUCTION & LOSSLESS STITCHING COMPLETE!")
print(f"   Deliverable: {final_video}")
print("=================================================================\n")
