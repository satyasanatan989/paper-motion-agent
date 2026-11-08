"""
Motion graphics, SVG paper-cutout generators, and tactile canvas rendering for PaperMotion AI.
"""

from .paper_canvas import generate_parchment_css, generate_parchment_canvas_js
from .cutouts import CutoutLibrary
from .flip_counter import generate_flip_counter_html

__all__ = [
    "generate_parchment_css",
    "generate_parchment_canvas_js",
    "CutoutLibrary",
    "generate_flip_counter_html",
]
