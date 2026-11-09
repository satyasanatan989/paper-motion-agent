"""
Cutaway Diagram Scene Template.
Features:
- Cross-section diagram with technical arrows, indicator leader lines, and thermal/meter gauges.
- Used for heat processing (140°C), axial tilt (23.5°), and planetary structure.
"""

from typing import Dict, Any
from templates.scenes.base_template import render_top_left_headline, render_watermark, render_caption_chunk

def render_cutaway_diagram(beat: Any, asset_map: Dict[str, str]) -> str:
    headline_html = render_top_left_headline(beat.headline_top, beat.headline_punch)
    watermark_html = render_watermark()
    caption_html = render_caption_chunk(beat.caption_chunk, beat.caption_highlight)

    diagram_asset_html = ""
    if beat.assets:
        primary = beat.assets[0]
        aid = primary.get("id", "")
        src = asset_map.get(aid, f"assets/{aid}.png")
        diagram_asset_html = f"""
        <div class="diagram-asset-container enter-pop">
          <img class="diagram-img" src="{src}" />
          <svg class="diagram-vector-overlay" width="600" height="400" viewBox="0 0 600 400">
            <line x1="120" y1="200" x2="480" y2="200" stroke="#F28C28" stroke-width="4" stroke-dasharray="8 6"/>
            <circle cx="120" cy="200" r="8" fill="#F28C28"/>
            <circle cx="480" cy="200" r="8" fill="#F28C28"/>
          </svg>
        </div>
        """

    meter_html = ""
    if beat.widget:
        w_val = beat.widget.get("value", "")
        w_unit = beat.widget.get("unit", "")
        meter_html = f"""
        <div class="meter-bar-widget enter-pop">
          <div class="meter-bar-title">{w_val} {w_unit}</div>
          <div class="meter-bar-track">
            <div class="meter-bar-fill" style="width: 80%;"></div>
          </div>
        </div>
        """

    return f"""
    <div class="template-cutaway-diagram" data-beat="{beat.beat_id}">
      {watermark_html}
      {headline_html}

      <div class="cutaway-stage-center">
        {diagram_asset_html}
        {meter_html}
      </div>

      {caption_html}
    </div>
    """
