"""
Compare Pair Scene Template (Side-by-side / Dual Comparison).
Features:
- Two objects juxtaposed with hanging tags (e.g. Fresh Coconut Rs 60 vs Packaged Drink Rs 50, or Mars -63°C vs Earth -73°C).
- Swinging price / temperature tags with hanging_swing spring physics.
"""

from typing import Dict, Any
from templates.scenes.base_template import render_top_left_headline, render_watermark, render_caption_chunk

def render_compare_pair(beat: Any, asset_map: Dict[str, str]) -> str:
    headline_html = render_top_left_headline(beat.headline_top, beat.headline_punch)
    watermark_html = render_watermark()
    caption_html = render_caption_chunk(beat.caption_chunk, beat.caption_highlight)

    # Assets layout
    cards_html = []
    for idx, a in enumerate(beat.assets[:2]):
        aid = a.get("id", "")
        src = asset_map.get(aid, f"assets/{aid}.png")
        enter_cls = f"enter-{a.get('enter', 'pop')}"
        cards_html.append(f"""
        <div class="compare-card {html.escape(enter_cls)}">
          <img class="compare-item-img" src="{html.escape(src)}" />
        </div>
        """)

    # Widget hanging tag
    widget_html = ""
    if beat.widget:
        w_val = html.escape(str(beat.widget.get("value", "")))
        w_unit = html.escape(str(beat.widget.get("unit", "")))
        widget_html = f"""
        <div class="hanging-tag-widget enter-pop" style="animation: springTagSwing 0.85s forwards;">
          <div class="hanging-tag-string"></div>
          <div class="hanging-tag-hole"></div>
          <div class="hanging-tag-value">{w_val} {w_unit}</div>
        </div>
        """

    return f"""
    <div class="template-compare-pair" data-beat="{beat.beat_id}">
      {watermark_html}
      {headline_html}

      <div class="compare-stage-row">
        {"".join(cards_html)}
        {widget_html}
      </div>

      {caption_html}
    </div>
    """
