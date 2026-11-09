"""
Zoom Lens Scene Template (Magnifier circle revealing microscopic / cellular detail).
Features:
- Brass/gold circular magnifying loupe element (#lens-zoom).
- High-detail micro element inside lens with animated focus ripple.
"""

from typing import Dict, Any
from templates.scenes.base_template import render_top_left_headline, render_watermark, render_caption_chunk

def render_zoom_lens(beat: Any, asset_map: Dict[str, str]) -> str:
    headline_html = render_top_left_headline(beat.headline_top, beat.headline_punch)
    watermark_html = render_watermark()
    caption_html = render_caption_chunk(beat.caption_chunk, beat.caption_highlight)

    lens_asset_html = ""
    if beat.assets:
        primary = beat.assets[0]
        aid = primary.get("id", "")
        src = asset_map.get(aid, f"assets/{aid}.png")
        lens_asset_html = f"""
        <div class="zoom-loupe-frame enter-pop">
          <div class="loupe-glass-circle">
            <img class="loupe-micro-img" src="{src}" />
          </div>
          <div class="loupe-handle-stem"></div>
        </div>
        """

    return f"""
    <div class="template-zoom-lens" data-beat="{beat.beat_id}">
      {watermark_html}
      {headline_html}

      <div class="zoom-lens-center">
        {lens_asset_html}
      </div>

      {caption_html}
    </div>
    """
