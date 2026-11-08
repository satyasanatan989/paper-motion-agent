"""
Dynamic Scene Composer for PaperMotion AI.
Transforms a structured StoryboardPlan into a complete, executable, interactive 1080x1920 (9:16)
web stage containing HTML5 Canvas, SVG vector layers, CSS 3D styling, and millisecond-accurate timeline driver.
"""

from pathlib import Path
from typing import Dict, Any, List
import json
import html

try:
    from storyboard.generator import StoryboardPlan, ScenePlan
    from visual_engine.camera import CameraController
    from visual_engine.motion_presets import MotionEasing, ParticleField
    from visual_engine.transitions import TransitionLibrary
    from visual_engine.typography import KineticTypography
except ImportError:
    from ..storyboard.generator import StoryboardPlan, ScenePlan
    from .camera import CameraController
    from .motion_presets import MotionEasing, ParticleField
    from .transitions import TransitionLibrary
    from .typography import KineticTypography

class DynamicSceneComposer:
    """Assembles full HTML/CSS/JS web stages tailored dynamically to any storyboard."""

    def compose_stage(self, storyboard: StoryboardPlan, output_dir: Path) -> Path:
        """
        Generates index.html, style.css, and timeline.js into output_dir.
        Returns the path to index.html.
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 1. Generate HTML
        html_content = self._generate_html(storyboard)
        html_file = output_dir / "index.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        # 2. Generate CSS
        css_content = self._generate_css(storyboard)
        css_file = output_dir / "style.css"
        with open(css_file, "w", encoding="utf-8") as f:
            f.write(css_content)

        # 3. Generate Timeline JS
        js_content = self._generate_js(storyboard)
        js_file = output_dir / "timeline.js"
        with open(js_file, "w", encoding="utf-8") as f:
            f.write(js_content)

        return html_file

    def _generate_html(self, storyboard: StoryboardPlan) -> str:
        scenes_html = []
        for idx, scene in enumerate(storyboard.scenes):
            is_active = " active" if idx == 0 else ""
            visual_stage_content = self._build_visual_stage_html(scene)

            badge_html = KineticTypography.render_chapter_badge(scene.typography.badge)
            headline_html = KineticTypography.render_headline(
                scene.typography.headline_sub,
                scene.typography.headline_main
            )

            # Metric Box
            metric_html = ""
            if scene.keywords:
                metric_title = scene.title
                metric_val = scene.keywords[0].upper() if scene.keywords else "VERIFIED"
                metric_sub = scene.typography.headline_sub
                metric_html = KineticTypography.render_metric_card(
                    metric_title, metric_val, metric_sub,
                    style_mode="flip_counter" if scene.visual_type == "infographic_data" else "standard"
                )

            scene_markup = f"""
      <!-- SCENE {scene.chapter_num:02d}: {html.escape(scene.title)} -->
      <section id="{scene.scene_id}" class="scene{is_active}" data-visual-type="{scene.visual_type}">
        {badge_html}
        {headline_html}

        <div class="visual-stage">
          {visual_stage_content}
          {metric_html}
        </div>
      </section>
            """
            scenes_html.append(scene_markup)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(storyboard.topic)} - PaperMotion Cinematic Explainer</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <div id="stage-container">
    
    <!-- Procedural Aged Parchment Canvas -->
    <canvas id="parchment-canvas" class="parchment-canvas" width="{storyboard.resolution['width']}" height="{storyboard.resolution['height']}"></canvas>

    <!-- Center Scroll Spine & Scorched Edge Vignette -->
    <div class="scroll-spine"></div>
    <div class="scorched-border"></div>

    <!-- Main Animated Content Layer -->
    <div class="content-layer">
      {"".join(scenes_html)}
    </div>

    <!-- Synchronized Subtitle Caption Streamer -->
    <div class="caption-streamer">
      <div id="caption-box" class="caption-text">
        {html.escape(storyboard.scenes[0].narration)}
      </div>
    </div>

  </div>

  <script src="timeline.js"></script>
</body>
</html>
"""

    def _build_visual_stage_html(self, scene: ScenePlan) -> str:
        """Constructs vector artwork and depth layers for a scene."""
        vtype = scene.visual_type
        sid = scene.scene_id

        # 1. Biological Macro / Health Explainer Stages
        if vtype == "biological_macro" or "Gut" in scene.title or "Grain" in scene.title:
            if "Grain" in scene.title or "Wheat" in scene.title or scene.chapter_num == 2:
                return f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <!-- Wheat Stem & Husk -->
            <path d="M 380 500 Q 380 320 380 180" stroke="#8C6D37" stroke-width="12" fill="none" stroke-linecap="round"/>
            <g id="{sid}-bran" class="layer-bran" transform="translate(140, 40)">
              <ellipse cx="240" cy="220" rx="140" ry="200" fill="#B8860B" stroke="#684E07" stroke-width="6"/>
              <ellipse cx="240" cy="220" rx="120" ry="180" fill="#D4AF37" stroke="#8C6D37" stroke-width="4" stroke-dasharray="8 6"/>
              <text x="240" y="140" font-family="'Cinzel'" font-size="28" font-weight="900" fill="#422E04" text-anchor="middle">FIBROUS BRAN</text>
            </g>
            <g id="{sid}-germ" class="layer-germ" transform="translate(140, 40)">
              <path d="M 240 330 C 200 330 200 390 240 410 C 280 390 280 330 240 330 Z" fill="#48BB78" stroke="#22543D" stroke-width="5"/>
              <text x="240" y="375" font-family="'Montserrat'" font-size="20" font-weight="800" fill="#1C4532" text-anchor="middle">GERM</text>
            </g>
            <g id="{sid}-endosperm" class="layer-core" transform="translate(140, 40)">
              <ellipse cx="240" cy="220" rx="90" ry="140" fill="#FFFDF5" stroke="#A88B58" stroke-width="4"/>
              <text x="240" y="215" font-family="'Montserrat'" font-size="22" font-weight="800" fill="#744210" text-anchor="middle">ENDOSPERM</text>
              <text x="240" y="245" font-family="'JetBrains Mono'" font-size="16" font-weight="700" fill="#C53030" text-anchor="middle">100% STARCH</text>
            </g>
          </svg>
                """
            elif "Acid" in scene.title or scene.chapter_num == 4:
                return f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <!-- Stomach Outline -->
            <path d="M 260 80 Q 200 180 200 320 Q 200 460 380 470 Q 560 460 560 340 Q 560 220 460 160 Q 430 80 430 40 L 350 40 Q 350 80 340 100 Z" fill="#E2C9B3" stroke="#8C4E34" stroke-width="8"/>
            <path d="M 360 40 L 360 140" stroke="#E53E3E" stroke-width="12" stroke-linecap="round" opacity="0.8"/>
            <!-- Acid Pool -->
            <g id="{sid}-acid-pool" class="acid-pool-wave">
              <path d="M 210 360 Q 380 330 550 360 L 550 460 Q 380 470 210 460 Z" fill="#E53E3E" stroke="#9B111E" stroke-width="4"/>
              <ellipse cx="280" cy="380" rx="16" ry="8" fill="#FEB2B2"/>
              <ellipse cx="440" cy="370" rx="22" ry="10" fill="#FEB2B2"/>
            </g>
            <circle cx="360" cy="260" r="16" fill="#FF8C00" filter="drop-shadow(0 0 12px #E53E3E)"/>
            <circle cx="390" cy="200" r="10" fill="#FF8C00" filter="drop-shadow(0 0 8px #E53E3E)"/>
          </svg>
                """
            else: # Gut Glue Matrix
                return f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <path d="M 220 120 C 140 220 160 380 240 440 C 340 500 500 480 560 380 C 620 280 580 180 480 120 Z" fill="#ECD8BE" stroke="#8C6848" stroke-width="8"/>
            <!-- Viscous Glue Paste -->
            <g id="{sid}-glue-paste" class="glue-matrix">
              <path d="M 260 240 Q 380 210 500 240 Q 520 340 480 380 Q 380 420 280 380 Z" fill="#D69E2E" stroke="#744210" stroke-width="6"/>
              <path d="M 320 280 Q 380 360 440 290" stroke="#FFF5F5" stroke-width="8" stroke-linecap="round" fill="none"/>
              <text x="380" y="340" font-family="'Cinzel'" font-size="28" font-weight="900" fill="#744210" text-anchor="middle">STICKY GLUE</text>
            </g>
          </svg>
                """

        # 2. Cinematic 2.5D Food Hook (Chapter 1)
        elif scene.chapter_num == 1:
            return f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <rect x="130" y="220" width="500" height="260" rx="20" fill="#E8D8BA" stroke="#A88B58" stroke-width="4" stroke-dasharray="12 8"/>
            <!-- Samosa -->
            <g id="{sid}-samosa" class="floating-samosa" transform="translate(180, 160)">
              <polygon points="120,40 240,240 0,240" fill="#D9822B" stroke="#8C4308" stroke-width="6"/>
              <path d="M 0,240 Q 120,270 240,240" fill="#C47020" stroke="#8C4308" stroke-width="6"/>
              <circle cx="80" cy="180" r="10" fill="#EFA44E" opacity="0.8"/>
              <circle cx="140" cy="140" r="14" fill="#EFA44E" opacity="0.8"/>
            </g>
            <!-- Flame Flare -->
            <g id="{sid}-flame" class="flare-pulse" transform="translate(340, 20)">
              <path d="M 40 180 C 10 130 10 70 40 10 C 70 70 70 130 40 180 Z" fill="#E53E3E" filter="drop-shadow(0 0 16px #DD6B20)"/>
              <path d="M 40 160 C 25 120 25 80 40 30 C 55 80 55 120 40 160 Z" fill="#F6E05E"/>
            </g>
          </svg>
            """

        # 3. Dramatic Final Verdict
        elif vtype == "dramatic_verdict" or scene.chapter_num == len(scene.title):
            return f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <!-- Wax Seal & Ribbon -->
            <circle cx="380" cy="240" r="160" fill="#8C1D24" stroke="#520D12" stroke-width="8"/>
            <circle cx="380" cy="240" r="135" fill="#A82830" stroke="#ECC94B" stroke-width="4" stroke-dasharray="8 6"/>
            <text x="380" y="225" font-family="'Cinzel'" font-size="34" font-weight="900" fill="#ECC94B" text-anchor="middle">VERDICT</text>
            <text x="380" y="265" font-family="'Montserrat'" font-size="20" font-weight="800" fill="#FFFDF8" text-anchor="middle">CONSCIOUS EATING</text>
            <path d="M 280 370 L 320 470 L 380 430 L 440 470 L 480 370 Z" fill="#520D12"/>
          </svg>
            """

        # 4. Default Vector Infographic
        else:
            return f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <rect x="80" y="80" width="600" height="360" rx="16" fill="#F3E5CE" stroke="#8C6D37" stroke-width="6"/>
            <circle cx="380" cy="260" r="100" fill="#ECC94B" stroke="#744210" stroke-width="4"/>
            <text x="380" y="270" font-family="'Cinzel'" font-size="32" font-weight="900" fill="#2D241E" text-anchor="middle">{html.escape(scene.title.upper())}</text>
          </svg>
            """

    def _generate_css(self, storyboard: StoryboardPlan) -> str:
        font_imports = KineticTypography.get_font_imports()
        transitions_css = TransitionLibrary.get_all_css()

        return f"""{font_imports}

:root {{
  --bg-parchment: #1A140E;
  --ink-primary: #FFFDF8;
  --ink-secondary: #E2D3B8;
  --accent-gold: #ECC94B;
  --accent-crimson: #8C1D24;
  --accent-acid: #E53E3E;
  --paper-cutout: drop-shadow(0 14px 24px rgba(0, 0, 0, 0.65)) drop-shadow(0 3px 6px rgba(0, 0, 0, 0.45));
  --paper-cutout-sm: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.5));
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  user-select: none;
}}

html, body {{
  width: 100%;
  height: 100%;
  background-color: #0E0B08;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  font-family: 'Montserrat', sans-serif;
  color: var(--ink-primary);
}}

#stage-container {{
  position: relative;
  width: {storyboard.resolution['width']}px;
  height: {storyboard.resolution['height']}px;
  background-color: var(--bg-parchment);
  overflow: hidden;
  box-shadow: 0 0 100px rgba(0, 0, 0, 0.95);
}}

/* Background Canvas */
.parchment-canvas {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}}

/* Book Spine Crease */
.scroll-spine {{
  position: absolute;
  top: 0;
  left: {storyboard.resolution['width'] // 2 - 3}px;
  width: 6px;
  height: 100%;
  background: linear-gradient(to right, rgba(0,0,0,0.5), rgba(0,0,0,0.1) 40%, rgba(255,255,255,0.08) 60%, rgba(0,0,0,0.6));
  z-index: 5;
  pointer-events: none;
  opacity: 0.85;
}}

/* Scorched Edge Vignette */
.scorched-border {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  box-shadow: inset 0 0 140px 60px rgba(10, 5, 2, 0.92), inset 0 0 50px 20px rgba(0, 0, 0, 0.98);
  z-index: 6;
  pointer-events: none;
}}

.content-layer {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10;
}}

.scene {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  padding: 130px 80px 140px 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  opacity: 0;
  transform: scale(0.96) translateY(24px);
  transition: opacity 0.45s cubic-bezier(0.16, 1, 0.3, 1), transform 0.45s cubic-bezier(0.16, 1, 0.3, 1);
  pointer-events: none;
}}

.scene.active {{
  opacity: 1;
  transform: scale(1) translateY(0);
  pointer-events: auto;
}}

.chapter-badge {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 21px;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #FFFDF8;
  background: rgba(18, 12, 8, 0.95);
  padding: 14px 34px;
  border-radius: 999px;
  box-shadow: var(--paper-cutout-sm);
  border: 2px solid var(--accent-gold);
  margin-bottom: 28px;
}}

.headline-wrap {{
  text-align: center;
  margin-bottom: 30px;
}}

.headline-sub {{
  font-family: 'Cinzel', serif;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 0.22em;
  color: var(--accent-gold);
  margin-bottom: 8px;
}}

.headline-main {{
  font-family: 'Montserrat', sans-serif;
  font-size: 48px;
  font-weight: 900;
  letter-spacing: 0.04em;
  color: #FFFDF8;
  text-shadow: 0 4px 14px rgba(0, 0, 0, 0.7);
}}

.visual-stage {{
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}}

/* Metric Box */
.metric-box {{
  margin-top: 35px;
  background: rgba(22, 16, 10, 0.92);
  border: 2px solid var(--accent-gold);
  border-radius: 18px;
  padding: 20px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  filter: var(--paper-cutout);
}}

.metric-title {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: var(--accent-gold);
  margin-bottom: 10px;
}}

.flip-row {{
  display: flex;
  gap: 10px;
}}

.flip-tile {{
  background: #100B07;
  color: #FFFDF8;
  font-family: 'JetBrains Mono', monospace;
  font-size: 46px;
  font-weight: 800;
  width: 60px;
  height: 74px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: 2px solid #5A4328;
}}

.metric-sub {{
  font-family: 'Montserrat', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--ink-secondary);
  letter-spacing: 0.08em;
  margin-top: 12px;
}}

/* Subtitles Streamer */
.caption-streamer {{
  position: absolute;
  bottom: 75px;
  left: 60px;
  right: 60px;
  background: rgba(14, 9, 6, 0.94);
  border: 2px solid var(--accent-gold);
  border-radius: 18px;
  padding: 24px 34px;
  text-align: center;
  filter: var(--paper-cutout);
  z-index: 25;
}}

.caption-text {{
  font-family: 'Montserrat', sans-serif;
  font-size: 29px;
  font-weight: 700;
  line-height: 1.45;
  color: #FFFDF8;
}}

.caption-text span.highlight {{
  color: var(--accent-gold);
  background: rgba(236, 201, 75, 0.22);
  padding: 3px 8px;
  border-radius: 6px;
}}

{transitions_css}
"""

    def _generate_js(self, storyboard: StoryboardPlan) -> str:
        chapters_json = []
        for scene in storyboard.scenes:
            chapters_json.append({
                "id": scene.chapter_num,
                "start": round(scene.duration * (scene.chapter_num - 1), 2), # Updated dynamically at runtime
                "end": round(scene.duration * scene.chapter_num, 2),
                "sceneId": scene.scene_id,
                "caption": scene.narration,
                "keywords": scene.keywords,
                "camera": {
                    "movement": scene.camera.movement,
                    "zoomStart": scene.camera.zoom_start,
                    "zoomEnd": scene.camera.zoom_end
                }
            })

        chapters_str = json.dumps(chapters_json, indent=4, ensure_ascii=False)
        cam_runtime = CameraController.generate_js_camera_runtime()

        return f"""/**
 * PaperMotion Dynamic Timeline Driver & Frame-Accurate CDP Controller.
 * Drives 2.5D camera dolly/zoom, multi-plane parallax, continuous kinetic motion,
 * and word-level synchronized subtitles.
 */

(function () {{
  // 1. Procedural Dark Parchment Canvas Generator
  function initParchment() {{
    const canvas = document.getElementById('parchment-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    const grad = ctx.createRadialGradient(w / 2, h / 2, 200, w / 2, h / 2, 1100);
    grad.addColorStop(0, '#2D221A');
    grad.addColorStop(0.5, '#221913');
    grad.addColorStop(0.85, '#19120D');
    grad.addColorStop(1, '#0F0B08');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    // Procedural organic speckles
    const rng = (function (seed) {{
      return function () {{
        seed = (seed * 9301 + 49297) % 233280;
        return seed / 233280;
      }};
    }})(42);

    ctx.fillStyle = 'rgba(255, 230, 190, 0.035)';
    for (let i = 0; i < 20000; i++) {{
      const x = rng() * w;
      const y = rng() * h;
      const r = rng() * 1.8;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }}
  }}

  initParchment();

  // 2. Chapter Timeline Configuration
  let chapters = {chapters_str};

  // Sync with live timestamps.json if present
  fetch('../output/timestamps.json')
    .then(r => r.json())
    .then(data => {{
      if (data && data.chapters) {{
        data.chapters.forEach((ch, idx) => {{
          if (chapters[idx]) {{
            chapters[idx].start = ch.start;
            chapters[idx].end = ch.end;
            chapters[idx].caption = ch.text;
          }}
        }});
      }}
    }})
    .catch(() => {{}});

  // 3. Camera System Runtime
  {cam_runtime}

  // 4. Kinetic Subtitle Highlighter
  const captionBox = document.getElementById('caption-box');
  const scenes = document.querySelectorAll('.scene');

  function highlightKeywords(text, keywords) {{
    let res = text;
    if (!keywords || !keywords.length) return res;
    keywords.forEach(kw => {{
      if (!kw || kw.length < 2) return;
      const reg = new RegExp(`(${{kw}})`, 'gi');
      res = res.replace(reg, '<span class="highlight">$1</span>');
    }});
    return res;
  }}

  // 5. Millisecond-Accurate Frame Seek Driver
  window.setSeekTime = function (t) {{
    let currentChapter = chapters[0];
    for (let i = 0; i < chapters.length; i++) {{
      if (t >= chapters[i].start && t <= chapters[i].end) {{
        currentChapter = chapters[i];
        break;
      }}
      if (t > chapters[chapters.length - 1].end) {{
        currentChapter = chapters[chapters.length - 1];
      }}
    }}

    // Switch Scene Active State
    scenes.forEach(s => {{
      if (s.id === currentChapter.sceneId) {{
        if (!s.classList.contains('active')) s.classList.add('active');
      }} else {{
        s.classList.remove('active');
      }}
    }});

    // Update Subtitles
    if (captionBox) {{
      captionBox.innerHTML = highlightKeywords(currentChapter.caption, currentChapter.keywords);
    }}

    // Interpolation progress within active chapter
    const dur = Math.max(0.1, currentChapter.end - currentChapter.start);
    const relT = t - currentChapter.start;
    const progress = Math.min(1.0, Math.max(0.0, relT / dur));

    // Dynamic Camera Application
    const cam = applyCameraMovement(
      currentChapter.camera.movement,
      progress,
      currentChapter.camera.zoomStart || 1.0,
      currentChapter.camera.zoomEnd || 1.07
    );

    const activeSceneEl = document.getElementById(currentChapter.sceneId);
    if (activeSceneEl) {{
      const vStage = activeSceneEl.querySelector('.visual-stage');
      if (vStage) {{
        vStage.style.transform = `translate3d(${{cam.cx}}px, ${{cam.cy}}px, ${{cam.cz}}px) scale(${{cam.zoom}})`;
      }}
    }}

    // Continuous Kinetic Micro-Animations (Zero Static Holds)
    const sid = currentChapter.sceneId;

    // Samosa & Flame
    const flame = document.getElementById(`${{sid}}-flame`);
    if (flame) {{
      const flameScale = 1.0 + 0.15 * Math.sin(t * 7.5) + 0.05 * Math.cos(t * 14.0);
      const flameY = -12 * Math.sin(t * 4.5);
      flame.style.transform = `translate(340px, ${{20 + flameY}}px) scale(${{flameScale}})`;
    }}

    const samosa = document.getElementById(`${{sid}}-samosa`);
    if (samosa) {{
      const hoverY = 4.0 * Math.sin(t * 3.5);
      const hoverRot = 1.2 * Math.cos(t * 2.8);
      samosa.style.transform = `translate(180px, ${{160 + hoverY}}px) rotate(${{hoverRot}}deg)`;
    }}

    // Wheat Kernel Peeling
    const bran = document.getElementById(`${{sid}}-bran`);
    const germ = document.getElementById(`${{sid}}-germ`);
    if (bran && germ) {{
      const peelX = progress * 45 + 2.5 * Math.sin(t * 4.0);
      bran.style.transform = `translate(${{140 - peelX}}px, 40px) scale(${{1.0 - progress * 0.08}})`;
      germ.style.transform = `translate(${{140 + peelX}}px, 40px) scale(${{1.0 - progress * 0.08}})`;
    }}

    // Glue Paste Stretch
    const glue = document.getElementById(`${{sid}}-glue-paste`);
    if (glue) {{
      const stretch = 1.0 + 0.12 * Math.sin(t * 4.5);
      const squish = 1.0 + 0.06 * Math.cos(t * 3.8);
      glue.style.transform = `scale(${{squish}}, ${{stretch}})`;
    }}

    // Acid Pool Wave Surge
    const acid = document.getElementById(`${{sid}}-acid-pool`);
    if (acid) {{
      const acidRise = Math.min(65, progress * 75);
      const acidWave = 4.5 * Math.sin(t * 5.5) + 2.0 * Math.cos(t * 11.0);
      acid.style.transform = `translateY(${{-(acidRise + acidWave)}}px)`;
    }}

    // Flip Counter
    const flipTiles = activeSceneEl ? activeSceneEl.querySelectorAll('.flip-tile') : [];
    if (flipTiles.length >= 2) {{
      const countHours = Math.min(54, Math.floor(24 + progress * 30));
      const strH = String(countHours).padStart(2, '0');
      flipTiles[0].textContent = strH[0];
      flipTiles[1].textContent = strH[1];
    }}
  }};

  window.getVideoDuration = function () {{
    return chapters[chapters.length - 1].end;
  }};

}})();
"""
