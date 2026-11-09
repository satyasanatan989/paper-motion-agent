"""
Scene Template Library Registry.
Dispatches beat specifications to dedicated visual template renderers.
"""

from typing import Dict, Any, Callable
from templates.scenes.fullbleed_parallax import render_fullbleed_parallax
from templates.scenes.object_on_dark import render_object_on_dark
from templates.scenes.notebook_sticker import render_notebook_sticker
from templates.scenes.compare_pair import render_compare_pair
from templates.scenes.cutaway_diagram import render_cutaway_diagram
from templates.scenes.zoom_lens import render_zoom_lens
from templates.scenes.stamp_reveal import render_stamp_reveal
from templates.scenes.endcard import render_endcard

SCENE_TEMPLATES: Dict[str, Callable[[Any, Dict[str, str]], str]] = {
    "fullbleed_parallax": render_fullbleed_parallax,
    "object_on_dark": render_object_on_dark,
    "notebook_sticker": render_notebook_sticker,
    "compare_pair": render_compare_pair,
    "cutaway_diagram": render_cutaway_diagram,
    "zoom_lens": render_zoom_lens,
    "stamp_reveal": render_stamp_reveal,
    "endcard": render_endcard,
}

def render_scene_template(beat: Any, asset_map: Dict[str, str]) -> str:
    """Dispatches a beat to its matching scene template renderer."""
    renderer = SCENE_TEMPLATES.get(beat.template, render_notebook_sticker)
    return renderer(beat, asset_map)
