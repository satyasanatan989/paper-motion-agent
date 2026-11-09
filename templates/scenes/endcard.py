"""
Endcard Scene Template (Follow / Share / Save with Bell Icon).
Features:
- High-retention call to action card with channel seal.
- Golden ringing notification bell icon.
- Subtle particle glow and subscription prompt.
"""

from typing import Dict, Any
from templates.scenes.base_template import render_top_left_headline, render_watermark, render_caption_chunk

def render_endcard(beat: Any, asset_map: Dict[str, str]) -> str:
    headline_html = render_top_left_headline(beat.headline_top, beat.headline_punch)
    watermark_html = render_watermark()
    caption_html = render_caption_chunk(beat.caption_chunk, beat.caption_highlight)

    bell_src = asset_map.get("bell_icon", "assets/bell_icon.png")

    return f"""
    <div class="template-endcard" data-beat="{beat.beat_id}">
      {watermark_html}
      {headline_html}

      <div class="endcard-center-card enter-pop">
        <div class="endcard-bell-wrapper">
          <img class="bell-icon-img" src="{bell_src}" />
        </div>
        <div class="endcard-brand-title">THE FOOD CODE</div>
        <div class="endcard-sub-cta">SHARE WITH FRIENDS • FOLLOW FOR DAILY TRUTH</div>
      </div>

      {caption_html}
    </div>
    """
