"""
Kinetic Typography & Word Highlight Timing Engine for PaperMotion AI.
Formats high-impact retro fonts: Cinzel, Rozha One, Bebas Neue, JetBrains Mono.
"""

from typing import List, Dict

class TypographyEngine:
    """Manages chapter titles, imperial banners, and word-level highlighting."""

    @staticmethod
    def get_font_imports() -> str:
        return "@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cinzel:wght@700;900&family=JetBrains+Mono:wght@700&family=Marcellus&family=Rozha+One&family=Yatra+One&display=swap');"

    @staticmethod
    def chapter_badge(chapter_num: int, title: str, icon: str = "⚔️") -> str:
        return f'<div class="chapter-badge">{icon} CHAPTER {chapter_num:02d} · {title.upper()}</div>'

    @staticmethod
    def headline(subtext: str, maintext: str, is_gold: bool = False) -> str:
        gold_cls = " headline-gold" if is_gold else ""
        return f"""
        <div class="headline-wrap">
          <div class="headline-sub">{subtext.upper()}</div>
          <div class="headline-main{gold_cls}">{maintext.upper()}</div>
        </div>
        """
