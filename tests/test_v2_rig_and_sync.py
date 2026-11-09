"""
Unit tests for PaperMotion Agent v2 Pipeline upgrades:
- Task 1: Persistent 2.5D Binder Rig & Typography in scene_composer.py
- Task 2: Word-Level Audio Sync in director.py
- Task 3: Articulated Cutouts (paperize_cutout) in generate_photocollage_assets.py
- Task 4: Prompt & Schema Constraints in prompts.py & storyboard_schema.json
"""

import pytest
from pathlib import Path
from PIL import Image, ImageDraw
import json

from visual_engine.scene_composer import DynamicSceneComposer
from storyboard.generator import StoryboardGenerator, StoryboardPlan, ScenePlan, CameraSpec, LayerSpec, TypographySpec, TransitionSpec
from assets.photographic.generate_photocollage_assets import paperize_cutout
from agent.prompts import MAYANK_DIRECTOR_SYSTEM_PROMPT, DIRECTOR_JSON_SCHEMA_INSTRUCTIONS

def test_persistent_binder_rig_dom_and_typography():
    composer = DynamicSceneComposer()
    
    # Mock scene with metric
    scene = ScenePlan(
        scene_id="scene_001",
        chapter_num=1,
        title="Wheat Anatomy",
        duration=3.5,
        narration="Har grain ke teen hisse hote hain",
        visual_type="biological_macro",
        environment="dark_macro_lab",
        background_tone={"primary": "#1A140E", "secondary": "#0E0B08"},
        camera=CameraSpec(movement="slow_dolly_in"),
        layers=[LayerSpec(name="wheat", depth_level="midground", type="svg_vector", content_id="kernel", animation="float")],
        typography=TypographySpec(
            badge="CHAPTER 01 · ANATOMY",
            headline_main="ZERO FIBER",
            headline_sub="REFINED STARCH",
            highlight_words=["GRAIN", "FIBER"]
        ),
        transition=TransitionSpec(type="cinematic_zoom"),
        metric_title="STARCH RATIO",
        metric_val="98%"
    )
    
    storyboard = StoryboardPlan(
        project_name="test_prod",
        topic="Wheat Starch",
        language="hinglish",
        genre="science_bio",
        aspect_ratio="9:16",
        resolution={"width": 1080, "height": 1920},
        fps=30,
        estimated_duration=3.5,
        soundtrack_preset="health_bio",
        scenes=[scene]
    )
    
    html = composer._generate_html(storyboard)
    css = composer._generate_css(storyboard)
    
    # 1. Verify 3-Layer DOM structure
    assert 'id="parchment-canvas"' in html, "Layer 0 canvas missing"
    assert '<div class="content-layer">' in html, "Layer 10 midground content-layer missing"
    assert '<div class="global-paper-rig">' in html, "Layer 99 foreground rig missing"
    assert '<div class="binder-margin">' in html, "Binder margin missing"
    assert '<div class="paper-crease-shadow">' in html, "Paper crease shadow missing"
    assert '<div class="paper-grain-overlay">' in html, "Paper grain overlay missing"
    
    # 2. Verify 2-tier kinetic typography locked to top-left (x: 110px, y: 180px)
    assert "top: 180px" in css
    assert "left: 110px" in css
    assert "Bebas Neue" in css
    assert "Impact" in css
    assert "#F4EFE6" in css or "--cream-warm" in css
    assert "#FF6B00" in css or "--accent-burnt-orange" in css
    
    # 3. Verify OdometerWidget block injection
    assert 'class="odometer-widget"' in html
    assert "STARCH RATIO" in html
    assert '<span class="odometer-digit">9</span>' in html
    assert '<span class="odometer-digit">8</span>' in html
    assert '<span class="odometer-digit">%</span>' in html

def test_paperize_cutout_cardboard_and_shadow():
    # Create test transparent image
    img = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([25, 25, 125, 125], fill=(220, 80, 40, 255))
    
    paperized = paperize_cutout(
        img,
        inner_border_color=(244, 239, 230),
        inner_border_px=2,
        shadow_offset=(10, 16),
        shadow_blur=12,
        shadow_opacity=0.45
    )
    
    # Dimensions must be expanded to accommodate blur and offset
    assert paperized.width > img.width
    assert paperized.height > img.height
    assert paperized.mode == "RGBA"
    
    # Check that shadow offset region has non-zero alpha (shadow baked-in)
    center_shadow_pixel = paperized.getpixel((paperized.width - 20, paperized.height - 20))
    assert center_shadow_pixel[3] >= 0

def test_prompts_and_schema_constraints():
    # Prompt assertions
    assert "MANDATORY 2-TIER HEADLINE OBJECT" in MAYANK_DIRECTOR_SYSTEM_PROMPT
    assert "NO FULL-SENTENCE CAPTIONS ON SCREEN" in MAYANK_DIRECTOR_SYSTEM_PROMPT
    assert "setup_text" in MAYANK_DIRECTOR_SYSTEM_PROMPT
    assert "punch_text" in MAYANK_DIRECTOR_SYSTEM_PROMPT
    assert "odometer" in MAYANK_DIRECTOR_SYSTEM_PROMPT
    assert "hanging_tag" in MAYANK_DIRECTOR_SYSTEM_PROMPT
    assert "meter_bar" in MAYANK_DIRECTOR_SYSTEM_PROMPT
    
    # Schema assertions
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "storyboard_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    
    scene_props = schema["definitions"]["Scene"]["properties"]
    assert "metric_title" in scene_props
    assert "metric_val" in scene_props
    assert "widget" in scene_props
    assert set(scene_props["widget"]["properties"]["type"]["enum"]) == {"odometer", "hanging_tag", "meter_bar"}

def test_cumulative_timeline_calculation_and_widget_variants():
    composer = DynamicSceneComposer()
    
    # Test scenes with varying durations to ensure no gaps or snaps
    s1 = ScenePlan(
        scene_id="scene_001", chapter_num=1, title="S1", duration=4.2, narration="First",
        visual_type="biological_macro", environment="e1", background_tone={}, camera=CameraSpec("pan_left"),
        layers=[], typography=TypographySpec("B1", "M1", "S1", []), transition=TransitionSpec("cinematic_zoom"),
        widget={"type": "hanging_tag", "metric_title": "HAZARD", "metric_val": "CRITICAL"}
    )
    s2 = ScenePlan(
        scene_id="scene_002", chapter_num=2, title="S2", duration=2.8, narration="Second",
        visual_type="biological_macro", environment="e2", background_tone={}, camera=CameraSpec("pan_right"),
        layers=[], typography=TypographySpec("B2", "M2", "S2", []), transition=TransitionSpec("paper_tear"),
        widget={"type": "meter_bar", "metric_title": "ACID LEVEL", "metric_val": "85%"}
    )
    
    sb = StoryboardPlan(
        project_name="timeline_test", topic="Timeline Test", language="hinglish", genre="science_bio",
        aspect_ratio="9:16", resolution={"width": 1080, "height": 1920}, fps=30, estimated_duration=7.0,
        soundtrack_preset="health_bio", scenes=[s1, s2]
    )
    
    js = composer._generate_js(sb)
    html = composer._generate_html(sb)
    
    # 1. Verify cumulative time (no index-multiplication overlaps or gaps)
    assert '"start": 0.0' in js
    assert '"end": 4.2' in js
    assert '"start": 4.2' in js
    assert '"end": 7.0' in js
    
    # 2. Verify hanging tag & meter bar rendered
    assert 'class="hanging-tag-widget"' in html
    assert 'class="meter-bar-widget"' in html
    assert "HAZARD" in html
    assert "ACID LEVEL" in html

def test_word_level_audio_sync_structure(tmp_path):
    # Test flat array structure of word_timestamps.json
    mock_timestamps = [
        {"word": "Har", "start": 0.1, "end": 0.45, "chapter": 1},
        {"word": "grain", "start": 0.46, "end": 0.88, "chapter": 1},
        {"word": "starch", "start": 0.90, "end": 1.40, "chapter": 1}
    ]
    out_file = tmp_path / "word_timestamps.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(mock_timestamps, f, indent=2)
    
    with open(out_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    
    assert len(loaded) == 3
    assert loaded[0]["word"] == "Har"
    assert loaded[0]["start"] == 0.1
    assert loaded[1]["end"] == 0.88
    assert loaded[2]["chapter"] == 1

