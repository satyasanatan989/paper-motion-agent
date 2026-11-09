"""
Object on Dark Paper Scene Template (MeanwhileMayank Ref 1 Earth/Moon & Space Objects).
Features:
- Dark charcoal parchment canvas (#120F0D) with concentric orbit lines & technical compass markers.
- Central hero object entering with spring pop and subtle slow axial rotation.
- Synchronized mechanical flip counter or odometer widget when numbers are spoken.
"""

from typing import Dict, Any
from templates.scenes.base_template import render_top_left_headline, render_watermark, render_caption_chunk

def render_object_on_dark(beat: Any, asset_map: Dict[str, str]) -> str:
    headline_html = render_top_left_headline(beat.headline_top, beat.headline_punch)
    watermark_html = render_watermark()
    caption_html = render_caption_chunk(beat.caption_chunk, beat.caption_highlight)

    hero_asset_html = ""
    if beat.assets:
        primary = beat.assets[0]
        aid = primary.get("id", "")
        src = asset_map.get(aid, f"assets/{aid}.png")
        hero_asset_html = f"""
        <div class="hero-orbit-wrapper">
          <div class="orbit-concentric-ring ring-1"></div>
          <div class="orbit-concentric-ring ring-2"></div>
          <div class="orbit-concentric-ring ring-3"></div>
          <img class="hero-object enter-pop" id="hero-{aid}" src="{src}" />
        </div>
        """

    # Mechanical widget (flip counter / odometer)
    widget_html = ""
    if beat.widget:
        w_type = beat.widget.get("type", "flip_counter")
        w_val = beat.widget.get("value", "")
        w_unit = beat.widget.get("unit", "")
        if w_type == "flip_counter" or w_type == "odometer":
            digits = "".join(f'<span class="flip-digit-tile">{c}</span>' for c in str(w_val))
            widget_html = f"""
            <div class="object-widget-box enter-pop">
              <div class="flip-digit-row">{digits}</div>
              <div class="flip-unit-label">{w_unit}</div>
            </div>
            """

    return f"""
    <div class="template-object-on-dark" data-beat="{beat.beat_id}">
      {watermark_html}
      {headline_html}

      <div class="dark-stage-center">
        {hero_asset_html}
        {widget_html}
      </div>

      {caption_html}
    </div>
    """
