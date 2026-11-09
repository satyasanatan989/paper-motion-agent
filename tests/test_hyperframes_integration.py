"""Comprehensive Unit Tests for HyperFrames Engine & Motion Graphics Integration.

Tests:
  1. HyperFramesPrimitives:
     - Vox Annotate SVG markup, hand-drawn marker styles, connector curve, and monospace pill.
     - Torn paper edge generation, deterministic closed-form seed reproducibility, roughness scaling.
     - CSS polygon clip-path generation for scene transitions.
     - Stop-motion cadence stepped-time driver and 2-frame edge boil hash law.
  2. Scene Composer Integration:
     - Injection of Vox annotation markup into the 2.5D visual stage.
     - HyperFrames CSS declarations.
     - Dynamic JS timeline and window.__timelines registry.
  3. HyperFrames Bridge:
     - Project export complying with the HyperFrames contract (index.html, compositions/, hyperframes.json).
  4. Storyboard Schema Validation:
     - Validation of annotation, paper_transition, and cadence properties.
"""

import json
from pathlib import Path
import pytest
import jsonschema

from storyboard.generator import (
    StoryboardPlan,
    ScenePlan,
    CameraSpec,
    TypographySpec,
    TransitionSpec,
    LayerSpec,
)
from visual_engine.scene_composer import DynamicSceneComposer
from visual_engine.hyperframes_primitives import HyperFramesPrimitives
from pipeline.hyperframes_bridge import HyperFramesBridge


# ---------------------------------------------------------
# Test Suite 1: HyperFramesPrimitives
# ---------------------------------------------------------

def test_vox_annotate_markup_styles():
    """Verify hand-drawn marker styles produce correct SVGs and paths."""
    for style in ["highlight", "circle", "underline", "scribble"]:
        markup = HyperFramesPrimitives.render_vox_annotate_markup(
            keyword="GLUTEN",
            note="INFLAMMATORY PROTEIN",
            style=style,
            accent="burnt_orange",
            widget_id=f"test-anno-{style}"
        )
        assert f'id="test-anno-{style}"' in markup
        assert f'data-style="{style}"' in markup
        assert "GLUTEN" in markup
        assert "INFLAMMATORY PROTEIN" in markup
        assert "va-mark" in markup
        assert "va-conn" in markup
        assert "va-note" in markup
        assert "#F46A38" in markup  # burnt_orange hex


def test_vox_annotate_no_note():
    """Verify empty note produces marker only without connector or note pill."""
    markup = HyperFramesPrimitives.render_vox_annotate_markup(
        keyword="ENDOSPERM",
        note="",
        style="circle",
        accent="warm_gold",
        widget_id="test-no-note"
    )
    assert "ENDOSPERM" in markup
    assert "va-mark" in markup
    assert "va-conn" not in markup
    assert "va-note" not in markup


def test_torn_paper_edge_determinism():
    """Verify closed-form LCG seed produces bit-identical edge points across runs."""
    pts1 = HyperFramesPrimitives.generate_torn_paper_edge(rows=50, roughness=50.0, seed=0x12345678)
    pts2 = HyperFramesPrimitives.generate_torn_paper_edge(rows=50, roughness=50.0, seed=0x12345678)

    assert len(pts1) == 51
    assert len(pts2) == 51
    for p1, p2 in zip(pts1, pts2):
        assert p1["y_pct"] == pytest.approx(p2["y_pct"])
        assert p1["offset_pct"] == pytest.approx(p2["offset_pct"])
        assert p1["rim_px"] == pytest.approx(p2["rim_px"])


def test_torn_polygon_css_directions():
    """Verify CSS polygon syntax and bounds for left-to-right and right-to-left."""
    pts = HyperFramesPrimitives.generate_torn_paper_edge(rows=30, roughness=60.0)

    css_ltr = HyperFramesPrimitives.generate_torn_polygon_css(pts, direction="left-to-right", progress=0.5)
    assert css_ltr.startswith("polygon(")
    assert css_ltr.endswith(")")
    assert "0% 0%" in css_ltr
    assert "0% 100%" in css_ltr

    css_rtl = HyperFramesPrimitives.generate_torn_polygon_css(pts, direction="right-to-left", progress=0.7)
    assert css_rtl.startswith("polygon(")
    assert css_rtl.endswith(")")
    assert "100% 0%" in css_rtl
    assert "100% 100%" in css_rtl


def test_stop_motion_cadence_js():
    """Verify stop-motion cadence law generates valid JS driver."""
    js = HyperFramesPrimitives.get_stop_motion_cadence_js(target_fps=12, boil=True)
    assert "CADENCE_FPS = 12" in js
    assert "Math.floor(t * CADENCE_FPS) / CADENCE_FPS" in js
    assert "boilActive = true" in js
    assert "window.__quantizeTime" in js
    assert "window.__applyCadenceStep" in js


# ---------------------------------------------------------
# Test Suite 2: DynamicSceneComposer Integration
# ---------------------------------------------------------

@pytest.fixture
def sample_hyperframes_storyboard():
    """Builds a storyboard containing HyperFrames annotations and transitions."""
    scene = ScenePlan(
        scene_id="scene_001",
        chapter_num=1,
        title="The Gluten Trap",
        duration=4.5,
        narration="Refined flour forms an elastic gluten matrix inside your gut.",
        visual_type="biological_macro",
        environment="Microscopic Gut Wall",
        background_tone={"primary": "#1A140E", "secondary": "#281D14", "vignette": True},
        camera=CameraSpec(movement="slow_dolly_in", depth_parallax=True),
        layers=[
            LayerSpec("gut_wall", "midground", "svg_vector", "gut_svg", "breathe", 0.5)
        ],
        typography=TypographySpec(
            badge="HAZARD 01",
            headline_main="GLUTEN MATRIX",
            headline_sub="THE INVISIBLE GLUE",
            highlight_words=["Gluten"]
        ),
        transition=TransitionSpec(type="paper_tear", duration=0.45),
        keywords=["Gluten", "Matrix"],
        annotation={
            "keyword": "Gluten",
            "note": "INTESTINAL INFLAMMATION",
            "style": "circle",
            "accent": "burnt_orange",
            "draw_at": 0.8
        },
        paper_transition={
            "type": "torn_paper_rip",
            "direction": "left-to-right",
            "roughness": 60,
            "tone": "cream"
        },
        cadence={
            "fps": 12,
            "boil": True
        }
    )

    scene2 = ScenePlan(
        scene_id="scene_002",
        chapter_num=2,
        title="Fiber Stripped Out",
        duration=3.5,
        narration="During refining, bran and germ layers are completely separated.",
        visual_type="vector_papercraft",
        environment="Industrial Roller Mill",
        background_tone={"primary": "#201812", "secondary": "#2A1F18", "vignette": True},
        camera=CameraSpec(movement="fast_push_in", depth_parallax=True),
        layers=[
            LayerSpec("wheat_peel", "midground", "svg_vector", "peel_svg", "split", 0.5)
        ],
        typography=TypographySpec(
            badge="HAZARD 02",
            headline_main="ZERO FIBER",
            headline_sub="ANATOMICAL LOSS",
            highlight_words=["Fiber"]
        ),
        transition=TransitionSpec(type="paper_tear", duration=0.45),
        keywords=["Fiber", "Bran"],
        annotation={
            "keyword": "Fiber",
            "note": "NUTRIENT DEFICIT",
            "style": "highlight",
            "accent": "warm_gold",
            "draw_at": 0.6
        }
    )

    scene3 = ScenePlan(
        scene_id="scene_003",
        chapter_num=3,
        title="The Final Verdict",
        duration=4.0,
        narration="Whole grains protect cellular vitality. Choose whole over refined.",
        visual_type="dramatic_verdict",
        environment="Court of Biological Truth",
        background_tone={"primary": "#1A140E", "secondary": "#281D14", "vignette": True},
        camera=CameraSpec(movement="smooth_pull_back", depth_parallax=True),
        layers=[
            LayerSpec("gold_seal", "midground", "svg_vector", "seal_svg", "stamp", 0.6)
        ],
        typography=TypographySpec(
            badge="VERDICT",
            headline_main="CHOOSE WHOLE",
            headline_sub="GOLDEN TRUTH",
            highlight_words=["Whole"]
        ),
        transition=TransitionSpec(type="cinematic_zoom", duration=0.5),
        keywords=["Whole", "Truth"]
    )

    return StoryboardPlan(
        project_name="hyperframes_explainer",
        topic="Refined Wheat Health Impact",
        language="hinglish",
        genre="science_bio",
        aspect_ratio="9:16",
        resolution={"width": 1080, "height": 1920},
        fps=30,
        estimated_duration=12.0,
        soundtrack_preset="health_bio",
        scenes=[scene, scene2, scene3]
    )


def test_scene_composer_renders_vox_annotation(tmp_path, sample_hyperframes_storyboard):
    """Verify scene composer injects Vox annotate markup, CSS, and JS timeline."""
    composer = DynamicSceneComposer()
    html_path = composer.compose_stage(sample_hyperframes_storyboard, tmp_path)

    assert html_path.exists()
    content = html_path.read_text(encoding="utf-8")

    # 1. HTML stage verification
    assert "vox-annotate-container" in content
    assert "scene_001-vox-anno" in content
    assert "Gluten" in content
    assert "INTESTINAL INFLAMMATION" in content
    assert "va-mark" in content
    assert "va-conn" in content

    # 2. CSS verification
    css_path = tmp_path / "style.css"
    assert css_path.exists()
    css_content = css_path.read_text(encoding="utf-8")
    assert ".vox-annotate-container" in css_content
    assert ".va-mark-path" in css_content
    assert ".va-conn-path" in css_content
    assert ".va-note" in css_content

    # 3. JS verification
    js_path = tmp_path / "timeline.js"
    assert js_path.exists()
    js_content = js_path.read_text(encoding="utf-8")
    assert "window.__timelines" in js_content
    assert "vox-annotate-container" in js_content
    assert "activeAnno.classList.add('active')" in js_content


# ---------------------------------------------------------
# Test Suite 3: HyperFramesBridge Project Export
# ---------------------------------------------------------

def test_hyperframes_bridge_export(tmp_path, sample_hyperframes_storyboard):
    """Verify HyperFrames bridge exports valid project structure conforming to HyperFrames contract."""
    bridge = HyperFramesBridge(output_root=tmp_path)
    export_dir = bridge.export_project(sample_hyperframes_storyboard)

    assert export_dir.exists()
    assert (export_dir / "index.html").exists()
    assert (export_dir / "compositions").exists()
    assert (export_dir / "compositions" / "scene_001.html").exists()
    assert (export_dir / "hyperframes.json").exists()

    # Verify root index.html contract
    root_html = (export_dir / "index.html").read_text(encoding="utf-8")
    assert 'data-composition-id="root"' in root_html
    assert 'data-composition-id="scene_001"' in root_html
    assert 'data-composition-src="compositions/scene_001.html"' in root_html
    assert 'data-composition-variables=' in root_html

    # Verify scene sub-composition template contract
    scene_html = (export_dir / "compositions" / "scene_001.html").read_text(encoding="utf-8")
    assert "<template>" in scene_html
    assert '</template>' in scene_html
    assert 'id="root"' in scene_html
    assert 'data-composition-id="scene_001"' in scene_html
    assert 'window.__timelines["scene_001"] = tl' in scene_html
    assert "vox-annotate-container" in scene_html


# ---------------------------------------------------------
# Test Suite 4: Schema Validation
# ---------------------------------------------------------

def test_schema_validates_hyperframes_fields(sample_hyperframes_storyboard):
    """Verify storyboard_schema.json validates annotation, paper_transition, and cadence."""
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "storyboard_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # Validate instance
    data = sample_hyperframes_storyboard.to_dict()
    jsonschema.validate(instance=data, schema=schema)
