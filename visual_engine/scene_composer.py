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
    from visual_engine.transitions import TransitionLibrary
    from visual_engine.typography import KineticTypography
    from visual_engine.hyperframes_primitives import HyperFramesPrimitives
except ImportError:
    from ..storyboard.generator import StoryboardPlan, ScenePlan
    from .camera import CameraController
    from .transitions import TransitionLibrary
    from .typography import KineticTypography
    from .hyperframes_primitives import HyperFramesPrimitives

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

        # 4. Copy word_timestamps.json if present in parent directory
        src_timestamps = output_dir.parent / "word_timestamps.json"
        if src_timestamps.exists():
            import shutil
            shutil.copy(src_timestamps, output_dir / "word_timestamps.json")

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
            if scene.keywords and not (getattr(scene, 'metric_title', None) or getattr(scene, 'metric_val', None)):
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
    
    <!-- Layer 0 (Background): Dynamic CSS gradient canvas -->
    <canvas id="parchment-canvas" class="parchment-canvas" width="{storyboard.resolution['width']}" height="{storyboard.resolution['height']}"></canvas>

    <!-- Layer 10 (Midground): Main Animated Content Layer -->
    <div class="content-layer">
      {"".join(scenes_html)}
    </div>

    <!-- Layer 99 (Foreground Rig): Fixed 2.5D Persistent Paper Rig -->
    <div class="global-paper-rig">
      <div class="binder-margin">
        <div class="binder-hole"></div>
        <div class="binder-hole"></div>
        <div class="binder-hole"></div>
        <div class="binder-hole"></div>
        <div class="binder-hole"></div>
        <div class="binder-hole"></div>
        <div class="binder-hole"></div>
      </div>
      <div class="paper-crease-shadow"></div>
      <div class="paper-grain-overlay"></div>
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
        """Constructs vector artwork and depth layers for a scene, including mechanical widgets."""
        vtype = scene.visual_type
        sid = scene.scene_id

        # 1. Specialized Ice Cream vs Frozen Dessert Visuals
        if "Ice Cream" in scene.title or "Frozen Dessert" in scene.title or "Dairy Law" in scene.title or "Palm Oil" in scene.title or "Profit" in scene.title or "Melting" in scene.title or "Deception" in scene.title or "Label" in scene.title:
            if "Deception" in scene.title or scene.chapter_num == 1:
                base_content = f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <polygon points="380,480 300,280 460,280" fill="#C68A4C" stroke="#7A4B1A" stroke-width="6"/>
            <path d="M 300,280 L 460,280" stroke="#7A4B1A" stroke-width="4" stroke-dasharray="8 6"/>
            <circle cx="350" cy="220" r="80" fill="#FFF8EE" stroke="#D1B894" stroke-width="5"/>
            <circle cx="420" cy="200" r="75" fill="#6A3B18" stroke="#3D1E08" stroke-width="5"/>
            <g class="hazard-ribbon" transform="translate(240, 90)">
              <rect x="0" y="0" width="280" height="48" rx="8" fill="#E53E3E" stroke="#9B111E" stroke-width="3"/>
              <text x="140" y="32" font-family="'Cinzel'" font-size="20" font-weight="900" fill="#FFF" text-anchor="middle">FAKE ICE CREAM?</text>
            </g>
          </svg>"""
            elif "Dairy Law" in scene.title or scene.chapter_num == 2:
                base_content = f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <rect x="260" y="100" width="240" height="360" rx="40" fill="#FFFDF8" stroke="#8C6D37" stroke-width="8"/>
            <rect x="330" y="50" width="100" height="60" rx="10" fill="#E2D3B8" stroke="#8C6D37" stroke-width="6"/>
            <rect x="268" y="240" width="224" height="212" rx="30" fill="#FEEBC8"/>
            <text x="380" y="290" font-family="'Cinzel'" font-size="28" font-weight="900" fill="#744210" text-anchor="middle">10% MILK FAT</text>
            <text x="380" y="330" font-family="'Montserrat'" font-size="16" font-weight="800" fill="#975A16" text-anchor="middle">LEGAL MANDATE</text>
            <circle cx="380" cy="390" r="34" fill="#38A169" stroke="#22543D" stroke-width="4"/>
            <text x="380" y="398" font-family="'JetBrains Mono'" font-size="15" font-weight="800" fill="#FFF" text-anchor="middle">FSSAI</text>
          </svg>"""
            elif "Palm Oil" in scene.title or scene.chapter_num == 3:
                base_content = f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <rect x="160" y="120" width="180" height="260" rx="16" fill="#DD6B20" stroke="#7B341E" stroke-width="6"/>
            <text x="250" y="240" font-family="'Impact'" font-size="32" fill="#FFF" text-anchor="middle">PALM OIL</text>
            <text x="250" y="275" font-family="'JetBrains Mono'" font-size="16" fill="#FFD8A8" text-anchor="middle">VANASPATI FAT</text>
            <path d="M 370 250 L 440 250 M 420 230 L 440 250 L 420 270" stroke="#E53E3E" stroke-width="8" stroke-linecap="round"/>
            <rect x="460" y="140" width="180" height="220" rx="12" fill="#EDF2F7" stroke="#4A5568" stroke-width="6"/>
            <text x="550" y="235" font-family="'Cinzel'" font-size="20" font-weight="900" fill="#2D3748" text-anchor="middle">FROZEN</text>
            <text x="550" y="265" font-family="'Cinzel'" font-size="20" font-weight="900" fill="#E53E3E" text-anchor="middle">DESSERT</text>
          </svg>"""
            elif "Profit" in scene.title or scene.chapter_num == 4:
                base_content = f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <path d="M 380 140 L 380 440 M 320 440 L 440 440" stroke="#8C6D37" stroke-width="10" stroke-linecap="round"/>
            <line x1="160" y1="210" x2="600" y2="290" stroke="#B7791F" stroke-width="12" stroke-linecap="round"/>
            <line x1="160" y1="210" x2="160" y2="310" stroke="#744210" stroke-width="4"/>
            <ellipse cx="160" cy="320" rx="80" ry="24" fill="#ECC94B" stroke="#744210" stroke-width="5"/>
            <text x="160" y="380" font-family="'Impact'" font-size="34" fill="#ECC94B" text-anchor="middle">Rs 450/KG</text>
            <text x="160" y="410" font-family="'Montserrat'" font-size="16" font-weight="800" fill="#FFFDF8" text-anchor="middle">PURE DAIRY FAT</text>
            <line x1="600" y1="290" x2="600" y2="390" stroke="#744210" stroke-width="4"/>
            <ellipse cx="600" cy="400" rx="80" ry="24" fill="#C53030" stroke="#742A2A" stroke-width="5"/>
            <text x="600" y="450" font-family="'Impact'" font-size="34" fill="#E53E3E" text-anchor="middle">Rs 90/KG</text>
            <text x="600" y="480" font-family="'Montserrat'" font-size="16" font-weight="800" fill="#FFFDF8" text-anchor="middle">CHEAP PALM OIL</text>
          </svg>"""
            elif "Melting" in scene.title or scene.chapter_num == 5:
                base_content = f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <g transform="translate(80, 100)">
              <ellipse cx="120" cy="260" rx="110" ry="40" fill="#E2E8F0" stroke="#718096" stroke-width="5"/>
              <path d="M 50 250 Q 120 220 190 250 Q 180 290 120 290 Q 60 290 50 250 Z" fill="#FFFDF5"/>
              <text x="120" y="340" font-family="'Cinzel'" font-size="20" font-weight="900" fill="#38A169" text-anchor="middle">REAL ICE CREAM</text>
              <text x="120" y="370" font-family="'Montserrat'" font-size="14" font-weight="700" fill="#A0AEC0" text-anchor="middle">Melts into liquid milk</text>
            </g>
            <g transform="translate(440, 100)">
              <ellipse cx="120" cy="260" rx="110" ry="40" fill="#E2E8F0" stroke="#718096" stroke-width="5"/>
              <path d="M 60 230 C 80 200 160 200 180 230 C 190 270 170 290 120 290 C 70 290 50 270 60 230 Z" fill="#ECC94B" opacity="0.85"/>
              <circle cx="95" cy="240" r="12" fill="#FAF089" stroke="#B7791F" stroke-width="2"/>
              <circle cx="135" cy="235" r="16" fill="#FAF089" stroke="#B7791F" stroke-width="2"/>
              <circle cx="150" cy="260" r="10" fill="#FAF089" stroke="#B7791F" stroke-width="2"/>
              <text x="120" y="340" font-family="'Cinzel'" font-size="20" font-weight="900" fill="#E53E3E" text-anchor="middle">FROZEN DESSERT</text>
              <text x="120" y="370" font-family="'Montserrat'" font-size="14" font-weight="700" fill="#E53E3E" text-anchor="middle">Oily curdled foam puddle</text>
            </g>
          </svg>"""
            else:
                base_content = f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <circle cx="380" cy="220" r="150" fill="#22543D" stroke="#1C4532" stroke-width="8"/>
            <circle cx="380" cy="220" r="125" fill="#276749" stroke="#9AE6B4" stroke-width="4" stroke-dasharray="8 6"/>
            <text x="380" y="195" font-family="'Cinzel'" font-size="32" font-weight="900" fill="#9AE6B4" text-anchor="middle">VERDICT</text>
            <text x="380" y="235" font-family="'Impact'" font-size="32" fill="#FFF" text-anchor="middle">READ THE LABEL</text>
            <text x="380" y="270" font-family="'Montserrat'" font-size="18" font-weight="800" fill="#ECC94B" text-anchor="middle">CHOOSE MILK FAT</text>
            <path d="M 280 340 L 320 440 L 380 400 L 440 440 L 480 340 Z" fill="#1C4532"/>
          </svg>"""

        # 2. Biological Macro / Health Explainer Stages
        elif vtype == "biological_macro" or "Gut" in scene.title or "Grain" in scene.title:
            if "Grain" in scene.title or "Wheat" in scene.title or scene.chapter_num == 2:
                base_content = f"""
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
          </svg>"""
            elif "Acid" in scene.title or scene.chapter_num == 4:
                base_content = f"""
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
          </svg>"""
            else: # Gut Glue Matrix
                base_content = f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <path d="M 220 120 C 140 220 160 380 240 440 C 340 500 500 480 560 380 C 620 280 580 180 480 120 Z" fill="#ECD8BE" stroke="#8C6848" stroke-width="8"/>
            <!-- Viscous Glue Paste -->
            <g id="{sid}-glue-paste" class="glue-matrix">
              <path d="M 260 240 Q 380 210 500 240 Q 520 340 480 380 Q 380 420 280 380 Z" fill="#D69E2E" stroke="#744210" stroke-width="6"/>
              <path d="M 320 280 Q 380 360 440 290" stroke="#FFF5F5" stroke-width="8" stroke-linecap="round" fill="none"/>
              <text x="380" y="340" font-family="'Cinzel'" font-size="28" font-weight="900" fill="#744210" text-anchor="middle">STICKY GLUE</text>
            </g>
          </svg>"""

        # 2. Cinematic 2.5D Food Hook (Chapter 1)
        elif scene.chapter_num == 1:
            base_content = f"""
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
          </svg>"""

        # 3. Dramatic Final Verdict
        elif vtype == "dramatic_verdict" or scene.chapter_num == len(scene.title):
            base_content = f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <!-- Wax Seal & Ribbon -->
            <circle cx="380" cy="240" r="160" fill="#8C1D24" stroke="#520D12" stroke-width="8"/>
            <circle cx="380" cy="240" r="135" fill="#A82830" stroke="#ECC94B" stroke-width="4" stroke-dasharray="8 6"/>
            <text x="380" y="225" font-family="'Cinzel'" font-size="34" font-weight="900" fill="#ECC94B" text-anchor="middle">VERDICT</text>
            <text x="380" y="265" font-family="'Montserrat'" font-size="20" font-weight="800" fill="#FFFDF8" text-anchor="middle">CONSCIOUS EATING</text>
            <path d="M 280 370 L 320 470 L 380 430 L 440 470 L 480 370 Z" fill="#520D12"/>
          </svg>"""

        # 4. Default Vector Infographic
        else:
            base_content = f"""
          <svg id="{sid}-visual" width="760" height="520" viewBox="0 0 760 520" style="filter: var(--paper-cutout);">
            <rect x="80" y="80" width="600" height="360" rx="16" fill="#F3E5CE" stroke="#8C6D37" stroke-width="6"/>
            <circle cx="380" cy="260" r="100" fill="#ECC94B" stroke="#744210" stroke-width="4"/>
            <text x="380" y="270" font-family="'Cinzel'" font-size="32" font-weight="900" fill="#2D241E" text-anchor="middle">{html.escape(scene.title.upper())}</text>
          </svg>"""

        # Unpack widget specs from scene.widget or direct attributes
        widget_data = getattr(scene, 'widget', None)
        w_type = "odometer"
        if isinstance(widget_data, dict):
            w_type = widget_data.get("type", "odometer")
            metric_title = getattr(scene, 'metric_title', None) or widget_data.get("metric_title")
            metric_val = getattr(scene, 'metric_val', None) or widget_data.get("metric_val")
        else:
            metric_title = getattr(scene, 'metric_title', None)
            metric_val = getattr(scene, 'metric_val', None)

        widget_markup = ""
        if metric_title or metric_val:
            m_title = metric_title or (scene.keywords[0].upper() if scene.keywords else "INDEX")
            m_val = str(metric_val or "100%")
            if w_type == "hanging_tag":
                widget_markup = self.render_hanging_tag_widget(m_title, m_val, widget_id=f"{sid}-tag")
            elif w_type == "meter_bar":
                widget_markup = self.render_meter_bar_widget(m_title, m_val, widget_id=f"{sid}-meter")
            else:
                widget_markup = self.render_odometer_widget(m_title, m_val, widget_id=f"{sid}-odometer")

        # HyperFrames Vox Annotation Rig
        anno_markup = ""
        anno_data = getattr(scene, 'annotation', None)
        if isinstance(anno_data, dict):
            kw = anno_data.get("keyword", (scene.keywords[0] if scene.keywords else "KEYWORD"))
            nt = anno_data.get("note", "CRITICAL FACTOR")
            st = anno_data.get("style", "highlight")
            ac = anno_data.get("accent", "burnt_orange")
            anno_markup = HyperFramesPrimitives.render_vox_annotate_markup(
                keyword=kw,
                note=nt,
                style=st,
                accent=ac,
                widget_id=f"{sid}-vox-anno"
            )

        combined = base_content
        if widget_markup:
            combined = f"{combined}\n{widget_markup}"
        if anno_markup:
            combined = f"{combined}\n{anno_markup}"
        return combined

    @staticmethod
    def render_hanging_tag_widget(metric_title: str, metric_val: str, widget_id: str = "hanging-tag-widget") -> str:
        """Reusable mechanical hanging tag widget."""
        return f"""
          <div class="hanging-tag-widget" id="{html.escape(widget_id)}">
            <span style="font-size: 15px; opacity: 0.75; display: block; font-family: 'JetBrains Mono', monospace;">{html.escape(metric_title.upper())}</span>
            <span>{html.escape(str(metric_val).upper())}</span>
          </div>"""

    @staticmethod
    def render_meter_bar_widget(metric_title: str, metric_val: str, widget_id: str = "meter-bar-widget") -> str:
        """Reusable mechanical meter bar widget."""
        return f"""
          <div class="meter-bar-widget" id="{html.escape(widget_id)}">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 800; color: #F4EFE6; margin-bottom: 6px;">{html.escape(metric_title.upper())}: {html.escape(str(metric_val))}</div>
            <div class="meter-bar-fill"></div>
          </div>"""

    @staticmethod
    def render_odometer_widget(metric_title: str, metric_val: str, widget_id: str = "odometer-widget") -> str:
        """Reusable mechanical odometer data widget populated with metric_title and metric_val."""
        val_str = str(metric_val).strip()
        digit_spans = "".join(f'<span class="odometer-digit">{html.escape(c)}</span>' for c in val_str)
        return f"""
          <div class="odometer-widget" id="{html.escape(widget_id)}">
            <div class="odometer-title">{html.escape(metric_title.upper())}</div>
            <div class="odometer-value-box">
              <div class="odometer-dial">
                {digit_spans}
              </div>
            </div>
          </div>"""

    def _generate_css(self, storyboard: StoryboardPlan) -> str:
        font_imports = KineticTypography.get_font_imports()
        transitions_css = TransitionLibrary.get_all_css()

        return f"""{font_imports}

:root {{
  --bg-parchment: #1A140E;
  --ink-primary: #FFFDF8;
  --ink-secondary: #E2D3B8;
  --cream-warm: #F4EFE6;
  --accent-burnt-orange: #FF6B00;
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

/* Layer 0 (Background): Dynamic CSS gradient canvas */
#parchment-canvas, .parchment-canvas {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  background: radial-gradient(circle at 50% 45%, #241D17 0%, #15110E 65%, #0B0907 100%);
}}

/* Layer 10 (Midground): Main Animated Content Layer */
.content-layer {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10;
}}

/* Layer 99 (Foreground Rig): Fixed 2.5D Persistent Paper Rig */
.global-paper-rig {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 99;
  pointer-events: none;
}}

.binder-margin {{
  position: absolute;
  top: 0;
  left: 36px;
  width: 44px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  pointer-events: none;
}}

.binder-hole {{
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #0E0B08;
  box-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.95), 0 1px 2px rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.05);
}}

.paper-crease-shadow {{
  position: absolute;
  top: 0;
  left: 62%;
  width: 16px;
  height: 100%;
  background: linear-gradient(to right, rgba(0,0,0,0.55), rgba(0,0,0,0.12) 40%, rgba(255,255,255,0.06) 60%, rgba(0,0,0,0.45));
  pointer-events: none;
  opacity: 0.85;
}}

.paper-grain-overlay {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  opacity: 0.12;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
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
  position: absolute;
  top: 125px;
  left: 110px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 19px;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #FFFDF8;
  background: rgba(18, 12, 8, 0.95);
  padding: 10px 24px;
  border-radius: 999px;
  box-shadow: var(--paper-cutout-sm);
  border: 2px solid var(--accent-gold);
  z-index: 15;
}}

/* 2-Tier Kinetic Typography System locked to top-left (x: 110px, y: 180px) */
.headline-wrap {{
  position: absolute;
  top: 180px;
  left: 110px;
  text-align: left;
  z-index: 15;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  pointer-events: none;
  max-width: 860px;
}}

.headline-sub {{
  font-family: 'Bebas Neue', 'Montserrat', sans-serif;
  font-size: 32px;
  font-weight: 400;
  letter-spacing: 0.14em;
  color: var(--cream-warm);
  text-transform: uppercase;
  margin-bottom: 4px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.85);
}}

.headline-main {{
  font-family: 'Impact', 'Montserrat', sans-serif;
  font-size: 64px;
  font-weight: 900;
  letter-spacing: 0.02em;
  color: var(--accent-burnt-orange);
  text-transform: uppercase;
  line-height: 1.05;
  text-shadow: 0 6px 28px rgba(0, 0, 0, 0.95), 0 2px 8px rgba(0, 0, 0, 0.9);
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

/* Mechanical Data Widgets: Odometer */
.odometer-widget {{
  position: absolute;
  bottom: 180px;
  right: 80px;
  background: #140E0A;
  border: 3px solid var(--accent-burnt-orange);
  border-radius: 12px;
  padding: 14px 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.85), inset 0 2px 6px rgba(0, 0, 0, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 20;
  filter: var(--paper-cutout-sm);
}}

.odometer-title {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.16em;
  color: var(--cream-warm);
  text-transform: uppercase;
  margin-bottom: 8px;
}}

.odometer-value-box {{
  background: #0B0806;
  border: 2px solid #5A4328;
  border-radius: 6px;
  padding: 8px 16px;
  display: flex;
  gap: 6px;
}}

.odometer-dial {{
  display: flex;
  gap: 6px;
}}

.odometer-digit {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 38px;
  font-weight: 900;
  color: var(--accent-burnt-orange);
  background: #1B130D;
  padding: 4px 10px;
  border-radius: 4px;
  border: 1px solid rgba(255, 107, 0, 0.35);
  text-shadow: 0 0 12px rgba(255, 107, 0, 0.45);
}}

/* Mechanical Data Widgets: Hanging Tag */
.hanging-tag-widget {{
  position: absolute;
  top: 140px;
  right: 80px;
  background: var(--cream-warm);
  color: #1A140E;
  padding: 12px 24px;
  border: 2px solid #8C6D37;
  border-radius: 4px 16px 16px 4px;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 26px;
  letter-spacing: 0.1em;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
  transform-origin: top center;
  z-index: 20;
}}

/* Mechanical Data Widgets: Meter Bar */
.meter-bar-widget {{
  position: absolute;
  bottom: 180px;
  left: 110px;
  width: 320px;
  background: #140E0A;
  border: 2px solid var(--accent-gold);
  border-radius: 8px;
  padding: 10px 16px;
  z-index: 20;
}}

.meter-bar-fill {{
  height: 14px;
  background: linear-gradient(90deg, var(--accent-gold), var(--accent-burnt-orange));
  border-radius: 4px;
  width: 75%;
  transition: width 1s ease-out;
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
  color: var(--accent-burnt-orange);
  background: rgba(255, 107, 0, 0.22);
  padding: 3px 8px;
  border-radius: 6px;
}}

{transitions_css}

{HyperFramesPrimitives.get_hyperframes_css_rules()}
"""

    def _generate_js(self, storyboard: StoryboardPlan) -> str:
        chapters_json = []
        cur_time = 0.0
        for scene in storyboard.scenes:
            scene_start = round(cur_time, 2)
            scene_end = round(cur_time + scene.duration, 2)
            cur_time = scene_end
            chapters_json.append({
                "id": scene.chapter_num,
                "start": scene_start,
                "end": scene_end,
                "sceneId": scene.scene_id,
                "caption": scene.narration,
                "keywords": scene.keywords,
                "annotation": getattr(scene, 'annotation', None),
                "paperTransition": getattr(scene, 'paper_transition', None),
                "cadence": getattr(scene, 'cadence', None),
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

  // Word-level audio synchronization for millisecond-accurate CSS transitions
  let wordTimestamps = [];
  fetch('word_timestamps.json')
    .then(r => r.json())
    .then(data => {{ if (Array.isArray(data)) wordTimestamps = data; }})
    .catch(() => {{
      fetch('../word_timestamps.json')
        .then(r => r.json())
        .then(data => {{ if (Array.isArray(data)) wordTimestamps = data; }})
        .catch(() => {{}});
    }});

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

    // Update Subtitles with Word-Level Synchronization
    if (captionBox) {{
      let captionHtml = highlightKeywords(currentChapter.caption, currentChapter.keywords);
      if (wordTimestamps && wordTimestamps.length > 0) {{
        const activeWord = wordTimestamps.find(w => t >= w.start && t <= w.end);
        if (activeWord && activeWord.word) {{
          const cleanWord = activeWord.word.replace(/[^a-zA-Z0-9\u0900-\u097F]/g, '');
          if (cleanWord.length > 1) {{
            const wordReg = new RegExp(`(\\\\b${{cleanWord}}\\\\b)`, 'i');
            captionHtml = captionHtml.replace(wordReg, '<span class="active-word" style="color:var(--accent-burnt-orange);text-shadow:0 0 16px var(--accent-burnt-orange);font-weight:900;">$1</span>');
          }}
        }}
      }}
      captionBox.innerHTML = captionHtml;
    }}

    // Interpolation progress within active chapter
    const dur = Math.max(0.1, currentChapter.end - currentChapter.start);
    const relT = t - currentChapter.start;
    const progress = Math.min(1.0, Math.max(0.0, relT / dur));

    const activeSceneEl = document.getElementById(currentChapter.sceneId);

    // HyperFrames Vox Annotation Trigger
    const activeAnno = activeSceneEl ? activeSceneEl.querySelector('.vox-annotate-container') : null;
    if (activeAnno) {{
      const drawAt = (currentChapter.annotation && currentChapter.annotation.draw_at != null) ? currentChapter.annotation.draw_at : 0.6;
      if (relT >= drawAt) {{
        if (!activeAnno.classList.contains('active')) activeAnno.classList.add('active');
      }} else {{
        activeAnno.classList.remove('active');
      }}
    }}

    // Dynamic Camera Application
    const cam = applyCameraMovement(
      currentChapter.camera.movement,
      progress,
      currentChapter.camera.zoomStart || 1.0,
      currentChapter.camera.zoomEnd || 1.07
    );

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

  // Register with HyperFrames deterministic timeline registry
  window.__timelines = window.__timelines || {{}};
  window.__timelines['main'] = {{
    seek: function (t) {{ window.setSeekTime(t); }},
    duration: function () {{ return window.getVideoDuration(); }}
  }};

}})();
"""
