"""
Fullbleed Parallax Scene Template (MeanwhileMayank Ref 1 style).
Features:
- 3-Layer multiplane depth (sky/stars 0.92x, mid architecture 1.00x, fg terrace/charpai 1.06x).
- Ambient atmospheric particles / dust drift.
- Continuous camera push or drift.
"""

from typing import Dict, Any, List
from templates.scenes.base_template import render_top_left_headline, render_watermark, render_caption_chunk

def render_fullbleed_parallax(beat: Any, asset_map: Dict[str, str]) -> str:
    headline_html = render_top_left_headline(beat.headline_top, beat.headline_punch)
    watermark_html = render_watermark()
    caption_html = render_caption_chunk(beat.caption_chunk, beat.caption_highlight)

    # Resolve 3 layers from asset_map or procedural defaults
    bg_src = asset_map.get("bg", "assets/indian_rooftop_layer0_bg.png")
    mid_src = asset_map.get("mid", "assets/indian_rooftop_layer10_mid.png")
    fg_src = asset_map.get("fg", "assets/indian_rooftop_layer20_fg.png")

    # Additional hero assets in the scene
    extra_assets_html = []
    for a in beat.assets:
        aid = a.get("id", "")
        src = asset_map.get(aid, f"assets/{aid}.png")
        enter_cls = f"enter-{a.get('enter', 'pop')}"
        extra_assets_html.append(
            f'<img class="scene-asset {enter_cls}" id="asset-{aid}" src="{src}" style="position:absolute;z-index:15;" />'
        )

    return f"""
    <div class="template-fullbleed-parallax" data-beat="{beat.beat_id}">
      {watermark_html}
      {headline_html}

      <div class="parallax-world">
        <div class="parallax-layer layer-bg" style="background-image:url('{bg_src}');"></div>
        <div class="parallax-layer layer-mid" style="background-image:url('{mid_src}');"></div>
        {"".join(extra_assets_html)}
        <div class="parallax-layer layer-fg" style="background-image:url('{fg_src}');"></div>
      </div>

      {caption_html}
    </div>
    """
