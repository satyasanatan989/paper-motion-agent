"""
Stamp Reveal Scene Template (The Food Code Verdict Slam).
Features:
- Heavy cardstock lab report document with fractal torn edges.
- Giant crimson or cobalt distressed rubber stamp slamming in with stamp_slam spring physics.
- Foley acoustic thud synchronization.
"""

from typing import Dict, Any
from templates.scenes.base_template import render_top_left_headline, render_watermark, render_caption_chunk

def render_stamp_reveal(beat: Any, asset_map: Dict[str, str]) -> str:
    headline_html = render_top_left_headline(beat.headline_top, beat.headline_punch)
    watermark_html = render_watermark()
    caption_html = render_caption_chunk(beat.caption_chunk, beat.caption_highlight)

    # Document base
    doc_src = asset_map.get("lab_sheet", asset_map.get("torn_card", "assets/torn_evidence_card.png"))
    doc_html = f"""
    <div class="evidence-doc-wrapper enter-pop">
      <img class="evidence-doc-img" src="{html.escape(doc_src)}" />
    </div>
    """

    # Rubber Stamp
    stamp_text = "VERIFIED"
    stamp_sub = "FOOD CODE LAB"
    stamp_color = "#DC2626"
    if beat.stamp:
        stamp_text = beat.stamp.get("text", stamp_text)
        stamp_sub = beat.stamp.get("sub", stamp_sub)
        stamp_color = beat.stamp.get("color", stamp_color)

    safe_sub = html.escape(stamp_sub)
    safe_text = html.escape(stamp_text)
    safe_color = html.escape(stamp_color)

    stamp_html = f"""
    <div class="craft-rubber-stamp enter-slam" style="border-color:{safe_color};color:{safe_color};animation:springStampSlam 0.60s forwards;">
      <div class="stamp-header-text">{safe_sub}</div>
      <div class="stamp-main-text">{safe_text}</div>
      <div class="stamp-star-row">★ ★ ★</div>
    </div>
    """

    return f"""
    <div class="template-stamp-reveal" data-beat="{beat.beat_id}">
      {watermark_html}
      {headline_html}

      <div class="stamp-stage-center">
        {doc_html}
        {stamp_html}
      </div>

      {caption_html}
    </div>
    """
