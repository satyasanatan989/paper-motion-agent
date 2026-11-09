"""HyperFrames Motion Primitives & Visual Components for PaperMotion.

Provides production-ready, deterministic visual components ported and adapted
from the HyperFrames motion graphics engine (HeyGen):
  1. Vox Annotate: Hand-drawn SVG marker strokes (highlight, circle, underline, scribble)
     with animated connector line leading to a monospace callout pill.
  2. Torn Paper Rip: Procedural jagged paper tear with fibrous deckle edges, paper core rim,
     and realistic cast shadow.
  3. Stop-Motion Cadence Law: Stepped-time quantization driver (8-15 fps) with 2-frame edge boil
     for authentic papercraft tactile animation.
  4. Number Wheel Tumbler: Kinetic rolling digit odometer reels.
  5. Paper Collage Scraps: Deckled paper scraps that lift and disperse on seeded arcs.
"""

from __future__ import annotations

import html
import math
from typing import Any, Dict, List


class HyperFramesPrimitives:
    """Motion graphic primitives adapted from the HyperFrames registry."""

    # Accent color palette matching documentary and papercraft aesthetics
    ACCENT_PALETTE: Dict[str, str] = {
        "burnt_orange": "#F46A38",
        "warm_gold": "#ECC94B",
        "paper_cream": "#F4EFE6",
        "ink_black": "#1A140E",
        "toxic_green": "#71F5A7",
        "cyan_accent": "#61A8FF",
        "violet_deep": "#C5A3FF",
        "crimson_alert": "#E53E3E",
    }

    # Hand-drawn marker stroke definitions authored in 100x40 or 100x12 viewBoxes
    MARKER_STYLES: Dict[str, Dict[str, Any]] = {
        "highlight": {
            "viewBox": "0 0 100 40",
            "d": "M 3 24 C 22 20.5, 47 25.5, 68 22.5 C 79 21, 90 23, 97 21.5",
            "strokeWidth": 26,
            "opacity": 0.55,
            "box_css": "left: -4%; top: 12%; width: 108%; height: 76%;",
        },
        "circle": {
            "viewBox": "0 0 100 40",
            "d": "M 22 7 C 58 1, 95 8, 97 20 C 99 31, 74 38, 44 37 C 16 36, 2 29, 3 19 C 4 10, 22 4, 52 4.5",
            "strokeWidth": 3.2,
            "opacity": 0.95,
            "box_css": "left: -12%; top: -24%; width: 124%; height: 148%;",
        },
        "underline": {
            "viewBox": "0 0 100 12",
            "d": "M 2 7 C 20 4.5, 46 8.5, 66 6 C 80 4.5, 92 7.5, 98 5.5",
            "strokeWidth": 4.5,
            "opacity": 0.95,
            "box_css": "left: -2%; bottom: -12%; width: 104%; height: 22%;",
        },
        "scribble": {
            "viewBox": "0 0 100 40",
            "d": "M 6 13 C 34 9.5, 66 11, 94 9 C 60 15, 26 16, 7 20 C 36 18, 68 21, 93 18 C 62 25, 28 27, 8 29",
            "strokeWidth": 5.0,
            "opacity": 0.70,
            "box_css": "left: -3%; top: 10%; width: 106%; height: 80%;",
        },
    }

    # Connector curve for Vox annotations (anchored from marker up-right to label)
    CONNECTOR_PATH = "M 10 94 C 52 82, 96 52, 148 32 C 176 21, 200 16, 218 14"

    @classmethod
    def render_vox_annotate_markup(
        cls,
        keyword: str,
        note: str,
        style: str = "highlight",
        accent: str = "burnt_orange",
        widget_id: str = "vox-annotate-001"
    ) -> str:
        """Renders the HTML markup for a Vox documentary callout."""
        style_key = style if style in cls.MARKER_STYLES else "highlight"
        marker_def = cls.MARKER_STYLES[style_key]
        accent_color = cls.ACCENT_PALETTE.get(accent, cls.ACCENT_PALETTE["burnt_orange"])

        escaped_keyword = html.escape(keyword)
        escaped_note = html.escape(note)
        escaped_id = html.escape(widget_id)

        connector_html = ""
        if note.strip():
            connector_html = f"""
        <div class="va-anno" aria-hidden="true">
          <svg class="va-conn" viewBox="0 0 240 100" preserveAspectRatio="none">
            <path class="va-conn-path" d="{cls.CONNECTOR_PATH}" fill="none" stroke="{accent_color}" stroke-width="2.8" stroke-linecap="round"/>
          </svg>
          <div class="va-note" style="border-left: 3px solid {accent_color}; color: {accent_color};">
            <span class="va-note-badge">NOTE</span>
            <span class="va-note-text">{escaped_note}</span>
          </div>
        </div>"""

        return f"""
      <div id="{escaped_id}" class="vox-annotate-container" data-style="{style_key}">
        <span class="va-em">
          <svg class="va-mark" viewBox="{marker_def['viewBox']}" preserveAspectRatio="none" aria-hidden="true" style="{marker_def['box_css']}">
            <path class="va-mark-path" d="{marker_def['d']}" fill="none" stroke="{accent_color}" stroke-width="{marker_def['strokeWidth']}" stroke-linecap="round" stroke-linejoin="round" opacity="{marker_def['opacity']}"/>
          </svg>
          <span class="va-em-text">{escaped_keyword}</span>
          {connector_html}
        </span>
      </div>"""

    @classmethod
    def generate_torn_paper_edge(
        cls,
        rows: int = 120,
        roughness: float = 55.0,
        seed: int = 0x7A9E11CF
    ) -> List[Dict[str, float]]:
        """Generates closed-form deterministic fibrous paper tear vertices."""
        roughness_norm = max(0.0, min(1.0, (roughness - 20.0) / 70.0))
        wander_px = 20.0 + roughness_norm * 35.0
        fibre_px = 2.0 + roughness_norm * 3.0
        diagonal_pct = 1.0 + roughness_norm * 3.0
        rim_min = 6.0
        rim_max = 14.0

        state = seed & 0xFFFFFFFF

        def rand() -> float:
            nonlocal state
            state = ((state * 1664525) + 1013904223) & 0xFFFFFFFF
            return state / 4294967296.0

        def value_noise(knots: int):
            k = [rand() * 2.0 - 1.0 for _ in range(knots + 1)]

            def sample(v: float) -> float:
                f = v * knots
                i = min(knots - 1, int(math.floor(f)))
                u = f - i
                u = u * u * (3.0 - 2.0 * u)
                return k[i] + (k[i + 1] - k[i]) * u

            return sample

        wander = value_noise(6)
        core_width = value_noise(12)

        edge_points: List[Dict[str, float]] = []
        for r in range(rows + 1):
            v = r / float(rows)
            rim_val = rim_min + (rim_max - rim_min) * (core_width(v) * 0.5 + 0.5)
            rim_val = max(rim_min, min(rim_max, rim_val + (rand() * 2.0 - 1.0) * fibre_px))
            offset_val = (v - 0.5) * diagonal_pct + (wander(v) * wander_px + (rand() * 2.0 - 1.0) * fibre_px) * 0.05
            edge_points.append({
                "y_pct": v * 100.0,
                "offset_pct": offset_val,
                "rim_px": rim_val
            })

        return edge_points

    @classmethod
    def generate_torn_polygon_css(
        cls,
        edge_points: List[Dict[str, float]],
        direction: str = "left-to-right",
        progress: float = 0.5
    ) -> str:
        """Builds a CSS polygon clip-path string for the torn tear line at given progress (0.0 to 1.0)."""
        pts: List[str] = []
        base_x = progress * 100.0

        if direction == "left-to-right":
            pts.append("0% 0%")
            for pt in edge_points:
                x = min(100.0, max(0.0, base_x + pt["offset_pct"]))
                pts.append(f"{x:.2f}% {pt['y_pct']:.2f}%")
            pts.append("0% 100%")
        else:
            pts.append("100% 0%")
            for pt in edge_points:
                x = min(100.0, max(0.0, (1.0 - progress) * 100.0 - pt["offset_pct"]))
                pts.append(f"{x:.2f}% {pt['y_pct']:.2f}%")
            pts.append("100% 100%")

        return f"polygon({', '.join(pts)})"

    @classmethod
    def get_stop_motion_cadence_js(cls, target_fps: int = 12, boil: bool = True) -> str:
        """Returns deterministic timeline quantization and edge-boil script."""
        boil_code = """
      if (boilActive) {
        var boilFrame = Math.floor(step / 2);
        var hash1 = ((Math.sin(boilFrame * 127.1 + 31.7) * 43758.5453) % 1);
        var hash2 = ((Math.sin(boilFrame * 269.5 + 18.3) * 43758.5453) % 1);
        var jx = (hash1 - 0.5) * 2.5;
        var jy = (hash2 - 0.5) * 2.5;
        var rot = (hash1 - 0.5) * 0.8;
        document.querySelectorAll('.cadence-boil').forEach(function(el) {
          el.style.transform = 'translate(' + jx.toFixed(2) + 'px, ' + jy.toFixed(2) + 'px) rotate(' + rot.toFixed(2) + 'deg)';
        });
      }
        """ if boil else ""

        return f"""
    // HyperFrames Stop-Motion Cadence Law ({target_fps} FPS stepped-time driver)
    var CADENCE_FPS = {target_fps};
    var boilActive = {'true' if boil else 'false'};
    function quantizeTime(t) {{
      return Math.floor(t * CADENCE_FPS) / CADENCE_FPS;
    }}
    function applyCadenceStep(t) {{
      var ts = quantizeTime(t);
      var step = Math.floor(t * CADENCE_FPS);
      {boil_code}
      return ts;
    }}
    window.__quantizeTime = quantizeTime;
    window.__applyCadenceStep = applyCadenceStep;
    """

    @classmethod
    def get_hyperframes_css_rules(cls) -> str:
        """Returns CSS stylesheet declarations for HyperFrames motion primitives."""
        return """
/* --- HyperFrames Motion Primitives Rig --- */
.vox-annotate-container {
  display: inline-block;
  position: relative;
  margin: 12px 0;
  vertical-align: middle;
}

.va-em {
  position: relative;
  display: inline-block;
  white-space: nowrap;
}

.va-em-text {
  position: relative;
  z-index: 2;
  font-family: 'Impact', 'Bebas Neue', sans-serif;
  font-size: 42px;
  letter-spacing: 0.04em;
  color: #F4EFE6;
  text-shadow: 2px 4px 10px rgba(0, 0, 0, 0.85);
}

.va-mark {
  position: absolute;
  z-index: 1;
  pointer-events: none;
  overflow: visible;
}

.va-mark-path {
  stroke-dasharray: 600;
  stroke-dashoffset: 600;
  transition: stroke-dashoffset 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}

.va-anno {
  position: absolute;
  left: 65%;
  bottom: calc(100% + 14px);
  width: 220px;
  height: 90px;
  z-index: 10;
  pointer-events: none;
}

.va-conn {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.va-conn-path {
  stroke-dasharray: 300;
  stroke-dashoffset: 300;
  transition: stroke-dashoffset 0.45s cubic-bezier(0.16, 1, 0.3, 1);
}

.va-note {
  position: absolute;
  top: -8px;
  right: -10px;
  background: rgba(26, 20, 14, 0.94);
  padding: 6px 12px;
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6), inset 0 0 8px rgba(0,0,0,0.4);
  font-family: 'JetBrains Mono', 'SF Mono', Consolas, monospace;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  white-space: nowrap;
  opacity: 0;
  transform: translateY(6px) scale(0.92);
  transition: opacity 0.35s ease-out, transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.va-note-badge {
  display: inline-block;
  font-size: 10px;
  padding: 1px 4px;
  margin-right: 6px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
  vertical-align: middle;
}

/* Activated state trigger */
.vox-annotate-container.active .va-mark-path {
  stroke-dashoffset: 0;
}
.vox-annotate-container.active .va-conn-path {
  stroke-dashoffset: 0;
}
.vox-annotate-container.active .va-note {
  opacity: 1;
  transform: translateY(0) scale(1.0);
}

/* Torn paper rip seam */
.torn-paper-rip-overlay {
  position: absolute;
  inset: 0;
  z-index: 85;
  pointer-events: none;
  overflow: hidden;
}

.tpr-sheet {
  position: absolute;
  inset: 0;
  background: #F4EFE6;
  filter: drop-shadow(-8px 12px 20px rgba(0, 0, 0, 0.7));
}

.tpr-sheet-rim {
  position: absolute;
  inset: 0;
  border-right: 4px solid #DFD7C7;
}

/* Cadence edge boil class */
.cadence-boil {
  transform-origin: center center;
  will-change: transform;
}
"""
