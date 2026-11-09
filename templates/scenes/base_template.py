"""
Base Scene Template Helpers for PaperMotion Studio Tier.
Enforces reference typography standards:
- Top-left 2-line headline: Cream line 1 (~64px) + Orange punch line 2 (~104px, pops in 0.35s later).
- Short 2-4 word caption chunk with 1 highlighted keyword (no full paragraphs).
- Persistent watermark: @FoodCode with verified badge.
- Zero chapter badges.
"""

import html
from typing import Optional, Dict, Any

def render_top_left_headline(headline_top: str, headline_punch: str) -> str:
    """Renders 2-line top-left punchy headline matching MeanwhileMayank & Food Code."""
    safe_top = html.escape(headline_top.upper())
    safe_punch = html.escape(headline_punch.upper())
    return f"""
    <div class="reference-headline-block">
      <div class="headline-top-line">{safe_top}</div>
      <div class="headline-punch-line">{safe_punch}</div>
    </div>
    """

def render_watermark(handle: str = "@FoodCode") -> str:
    """Renders persistent subtle watermark in top-right."""
    return f"""
    <div class="studio-watermark">
      <span class="watermark-icon">✦</span>
      <span class="watermark-handle">{html.escape(handle)}</span>
    </div>
    """

def render_caption_chunk(caption_chunk: str, highlight_word: Optional[str] = None) -> str:
    """Renders short 2-4 word caption box with highlighted keyword."""
    if not caption_chunk:
        return ""
    text = html.escape(caption_chunk)
    if highlight_word:
        hw_clean = html.escape(highlight_word)
        import re
        reg = re.compile(rf"(?<!\w)({re.escape(hw_clean)})(?!\w)", re.IGNORECASE)
        text = reg.sub(r'<span class="caption-highlight">\1</span>', text)

    return f"""
    <div class="studio-caption-box">
      <div class="studio-caption-text">{text}</div>
    </div>
    """
