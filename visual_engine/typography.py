"""
Professional Kinetic Typography Engine.
Supports word-level keyword highlighting, high-contrast badges, split-flap counters,
and safe-area margins compliant with vertical video standards (9:16).
"""

from typing import List, Dict, Optional
import html

class KineticTypography:
    """Formats and highlights kinetic text elements for high retention."""

    @staticmethod
    def get_font_imports() -> str:
        return (
            "@import url('https://fonts.googleapis.com/css2?"
            "family=Cinzel:wght@600;700;900&"
            "family=Montserrat:wght@400;600;800;900&"
            "family=Rozha+One&"
            "family=Bebas+Neue&"
            "family=JetBrains+Mono:wght@500;700;800&"
            "family=Yatra+One&"
            "display=swap');"
        )

    @staticmethod
    def render_headline(subtext: str, maintext: str, accent_color: str = "#ECC94B") -> str:
        return f"""
        <div class="headline-wrap">
          <div class="headline-sub">{html.escape(subtext.upper())}</div>
          <div class="headline-main">{html.escape(maintext.upper())}</div>
        </div>
        """

    @staticmethod
    def render_chapter_badge(badge_text: str) -> str:
        return f'<div class="chapter-badge">{html.escape(badge_text)}</div>'

    @staticmethod
    def render_metric_card(title: str, val: str, subtext: str, style_mode: str = "flip_counter") -> str:
        """
        Renders antique mechanical split-flap tiles or modern data badges.
        """
        if style_mode == "flip_counter":
            # Extract digits or characters
            chars = list(val.replace(" ", ""))
            tiles = "".join(f'<div class="flip-tile">{html.escape(c)}</div>' for c in chars[:5])
            return f"""
            <div class="metric-box">
              <div class="metric-title">{html.escape(title.upper())}</div>
              <div class="flip-row">
                {tiles}
              </div>
              <div class="metric-sub">{html.escape(subtext.upper())}</div>
            </div>
            """
        else:
            return f"""
            <div class="metric-box">
              <div class="metric-title">{html.escape(title.upper())}</div>
              <div class="metric-value">{html.escape(val)}</div>
              <div class="metric-sub">{html.escape(subtext.upper())}</div>
            </div>
            """

    @staticmethod
    def highlight_keywords_in_html(text: str, keywords: List[str]) -> str:
        """Surrounds keywords with glowing accent spans."""
        res = text
        for kw in keywords:
            if not kw or len(kw.strip()) < 2:
                continue
            clean_kw = kw.strip()
            # Case insensitive replace preserving original case
            import re
            pattern = re.compile(f"({re.escape(clean_kw)})", re.IGNORECASE)
            res = pattern.sub(r'<span class="highlight">\1</span>', res)
        return res

    @staticmethod
    def create_chapter_badge(chapter_num: int, title: str) -> str:
        return f'<div class="chapter-badge">CHAPTER {chapter_num:02d} • {html.escape(title.upper())}</div>'

    @staticmethod
    def create_split_flap_counter(val: str, label: str) -> str:
        return KineticTypography.render_metric_card(title=label, val=val, subtext="MEASURED METRIC", style_mode="flip_counter")

