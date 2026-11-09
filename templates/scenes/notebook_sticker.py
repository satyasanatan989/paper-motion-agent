"""
Notebook Sticker Scene Template (The Food Code Refs 2 & 3).
Features:
- Aged notebook/journal cardstock with binder punch holes and subtle grid lines.
- 1-2 glossy 3D stickers with white vinyl die-cut border entering with spring pop.
- Translucent washi tape strips pinning top corners.
- Technical label / case file tag.
"""

from typing import Dict, Any
from templates.scenes.base_template import render_top_left_headline, render_watermark, render_caption_chunk

def render_notebook_sticker(beat: Any, asset_map: Dict[str, str]) -> str:
    headline_html = render_top_left_headline(beat.headline_top, beat.headline_punch)
    watermark_html = render_watermark()
    caption_html = render_caption_chunk(beat.caption_chunk, beat.caption_highlight)

    stickers_html = []
    for idx, a in enumerate(beat.assets):
        aid = a.get("id", "")
        src = asset_map.get(aid, f"assets/{aid}.png")
        enter_cls = f"enter-{a.get('enter', 'pop')}"
        tape_cls = "tape-tr" if idx % 2 == 0 else "tape-tl"
        stickers_html.append(f"""
        <div class="notebook-sticker-item {enter_cls}">
          <div class="craft-washi-tape {tape_cls}"></div>
          <img class="sticker-img" src="{src}" alt="{aid}" />
        </div>
        """)

    # Optional widget if numbers are spoken
    widget_html = ""
    if beat.widget:
        w_val = beat.widget.get("value", "")
        w_unit = beat.widget.get("unit", "")
        widget_html = f"""
        <div class="notebook-badge-callout enter-pop">
          <span class="badge-num">{w_val}</span>
          <span class="badge-unit">{w_unit}</span>
        </div>
        """

    return f"""
    <div class="template-notebook-sticker" data-beat="{beat.beat_id}">
      {watermark_html}
      {headline_html}

      <div class="notebook-page-surface">
        <div class="stickers-layout-row">
          {"".join(stickers_html)}
        </div>
        {widget_html}
      </div>

      {caption_html}
    </div>
    """
