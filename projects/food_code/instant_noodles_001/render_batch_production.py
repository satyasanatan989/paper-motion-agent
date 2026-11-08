"""
Batch-by-Batch Modular Production Engine for Food Code Episode 001.
Renders each scene independently with high-density visual assets and stitches them losslessly.
"""

import json
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

with open(proj_dir / "storyboard.json", encoding="utf-8") as f:
    sb = json.load(f)

with open(proj_dir / "timings.json", encoding="utf-8") as f:
    timings = json.load(f)

scenes = sb["scenes"]
master_soundtrack = proj_dir / "soundtrack.mp3"
render_js = repo_root / "pipeline" / "render.js"

print("=================================================================")
print("🎬 FOOD CODE 001 — BATCH-BY-BATCH MODULAR CINEMATIC PRODUCTION")
print("=================================================================\n")

# Base CSS for all batch stages
BASE_CSS = """
:root {
  --fc-black: #0B0907;
  --fc-surface: #161310;
  --fc-orange: #FF6B00;
  --fc-gold: #FFA94D;
  --fc-white: #F5EBE1;
  --fc-muted: #A89F91;
  --fc-red: #8B3524;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  width: 1080px; height: 1920px;
  background-color: var(--fc-black);
  color: var(--fc-white);
  overflow: hidden;
  font-family: 'Montserrat', sans-serif;
}
#viewport {
  position: relative; width: 1080px; height: 1920px;
  background: radial-gradient(circle at 50% 45%, #181410 0%, #0B0907 80%);
  perspective: 1200px; overflow: hidden;
}
.brand-badge {
  position: absolute; top: 90px; left: 50%;
  transform: translateX(-50%);
  display: flex; align-items: center; gap: 12px;
  background: rgba(22, 19, 16, 0.94);
  border: 1.5px solid var(--fc-orange);
  padding: 10px 24px; border-radius: 40px;
  box-shadow: 0 4px 30px rgba(255, 107, 0, 0.3);
  z-index: 1000;
}
.brand-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--fc-orange); box-shadow: 0 0 14px var(--fc-orange); }
.brand-title { font-family: 'Cinzel', serif; font-size: 16px; font-weight: 900; letter-spacing: 4px; color: var(--fc-white); }
.brand-code { font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; color: var(--fc-orange); background: rgba(255, 107, 0, 0.15); padding: 2px 8px; border-radius: 4px; }
.cinematic-vignette {
  position: absolute; inset: 0;
  background: radial-gradient(circle at 50% 50%, transparent 45%, rgba(11, 9, 7, 0.96) 95%);
  pointer-events: none; z-index: 900;
}
.ambient-glow {
  position: absolute; top: 38%; left: 50%; transform: translate(-50%, -50%);
  width: 950px; height: 950px;
  background: radial-gradient(circle, rgba(255, 107, 0, 0.12) 0%, transparent 70%);
  pointer-events: none; z-index: 50;
}
.headline-box {
  position: absolute; top: 230px; left: 80px; right: 80px; text-align: center; z-index: 800;
}
.headline-sub {
  font-family: 'Montserrat', sans-serif; font-size: 16px; font-weight: 800;
  letter-spacing: 4px; color: var(--fc-orange); margin-bottom: 10px; text-transform: uppercase;
}
.headline-main {
  font-family: 'Bebas Neue', sans-serif; font-size: 60px; line-height: 1.05;
  letter-spacing: 2px; color: var(--fc-white); text-transform: uppercase;
  text-shadow: 0 4px 30px rgba(0, 0, 0, 0.95);
}
.caption-box {
  position: absolute; bottom: 250px; left: 80px; right: 80px;
  background: rgba(22, 19, 16, 0.92);
  border: 1.5px solid rgba(255, 107, 0, 0.4);
  padding: 24px 32px; border-radius: 20px;
  box-shadow: 0 10px 45px rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px); z-index: 800;
}
.caption-text {
  font-family: 'Montserrat', sans-serif; font-size: 30px; line-height: 1.45;
  font-weight: 600; color: var(--fc-white); text-align: center;
}
.caption-text .highlight {
  color: var(--fc-orange); font-weight: 800; text-shadow: 0 0 16px rgba(255, 107, 0, 0.6);
}
.visual-stage {
  position: absolute; top: 380px; left: 50%; transform: translateX(-50%);
  width: 920px; height: 980px;
  display: flex; align-items: center; justify-content: center; z-index: 200;
}
.fc-svg { width: 100%; height: 100%; }
"""

def generate_scene_stage(scene: dict, scene_idx: int) -> Path:
    s_id = scene["scene_id"]
    dur = scene["duration"]
    stage_path = stages_dir / s_id
    stage_path.mkdir(parents=True, exist_ok=True)
    
    # Save style.css
    with open(stage_path / "style.css", "w", encoding="utf-8") as f:
        f.write(BASE_CSS)
        
    # Read the visual SVG from the previous build_stage
    from projects.food_code.instant_noodles_001.build_stage import get_scene_visual_html
    visual_svg = get_scene_visual_html(s_id)
    
    # Build timeline.js for this individual scene
    cam = scene["camera"]
    z_start = cam.get("zoom_start", 1.0)
    z_end = cam.get("zoom_end", 1.08)
    movement = cam.get("movement", "slow_dolly_in")
    
    js_content = f"""
    let currentTime = 0.0;
    const TOTAL_DURATION = {dur};
    window.setSeekTime = function(t) {{
      currentTime = Math.max(0.0, Math.min(TOTAL_DURATION, t));
      const p = currentTime / TOTAL_DURATION;
      const easeP = 1.0 - Math.pow(1.0 - p, 3);
      const zoom = {z_start} + ({z_end} - {z_start}) * easeP;
      
      let panX = 0, panY = 0;
      if ('{movement}' === 'pan_right') panX = -50 * easeP;
      else if ('{movement}' === 'pan_left') panX = 50 * easeP;
      else if ('{movement}' === 'tilt_down') panY = -40 * easeP;
      else if ('{movement}' === 'fast_push_in') panY = -25 * easeP;
      else if ('{movement}' === 'subtle_orbit') {{
        panX = 20 * Math.sin(p * Math.PI);
        panY = 12 * Math.cos(p * Math.PI) - 12;
      }}
      
      const st = document.getElementById('stage-asset');
      if (st) {{
        st.style.transform = `translate3d(${{panX}}px, ${{panY}}px, 0px) scale(${{zoom.toFixed(4)}})`;
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
        import re
        highlighted_text = re.sub(f"({re.escape(kw)})", r'<span class="highlight">\1</span>', highlighted_text, flags=re.IGNORECASE)
        
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="style.css">
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cinzel:wght@700;900&family=Montserrat:wght@400;600;800;900&family=JetBrains+Mono:wght@700;800&display=swap" rel="stylesheet">
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
    
    <div class="visual-stage" id="stage-asset">
      {visual_svg}
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
