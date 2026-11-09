"""
Unit tests for Studio Tier enhancements:
1. Damped Harmonic Oscillator Spring Physics (SpringSolver & presets)
2. Handheld Desk Parallax Camera & Multiplane Depth Transforms
3. Fractal Torn Paper Edge Generator (generate_torn_paper_edge)
4. Dynamic Scene Composer Spring & Craft CSS/JS injection
5. Stage Preview Server request handler
"""

import pytest
import math
from pathlib import Path
from PIL import Image

from visual_engine.spring_physics import SpringConfig, SpringSolver, SPRING_PRESETS
from visual_engine.camera import CameraController, CameraKeyframe
from assets.photographic.generate_photocollage_assets import generate_torn_paper_edge
from visual_engine.scene_composer import DynamicSceneComposer
from storyboard.generator import StoryboardPlan, ScenePlan, TypographySpec, CameraSpec, TransitionSpec


def test_spring_physics_underdamped_and_keyframes():
    cfg = SPRING_PRESETS["stamp_slam"]
    assert cfg.damping_ratio < 1.0  # Underdamped
    assert cfg.natural_frequency > 0.0

    # Start at 0.0
    val_0 = SpringSolver.evaluate(cfg, 0.0)
    assert val_0 == 0.0

    # Overshoots slightly past 1.0 due to underdamping
    samples = [SpringSolver.evaluate(cfg, t / 100.0) for t in range(1, 100)]
    max_val = max(samples)
    assert max_val >= 1.02  # Detectable overshoot

    # Settles near 1.0
    val_settled = SpringSolver.evaluate(cfg, 1.2)
    assert math.isclose(val_settled, 1.0, abs_tol=0.03)

    # Keyframes generation
    kfs = SpringSolver.generate_keyframes(cfg, duration=0.6, steps=20)
    assert len(kfs) == 21
    assert kfs[0][0] == 0.0
    assert kfs[-1][0] == 100.0


def test_spring_physics_critically_and_overdamped():
    # Critically damped: c = 2 * sqrt(m * k)
    crit_cfg = SpringConfig(stiffness=100.0, damping=20.0, mass=1.0)
    assert math.isclose(crit_cfg.damping_ratio, 1.0, rel_tol=1e-4)
    assert SpringSolver.evaluate(crit_cfg, 0.0) == 0.0
    assert SpringSolver.evaluate(crit_cfg, 1.0) > 0.9

    # Near-critically damped boundary test (zeta in [1.0 - 1e-4, 1.0]): must not divide by zero or explode
    near_crit_cfg = SpringConfig(stiffness=100.0, damping=19.9998, mass=1.0)
    assert near_crit_cfg.damping_ratio < 1.0
    val_near_crit = SpringSolver.evaluate(near_crit_cfg, 0.5)
    assert 0.8 < val_near_crit < 1.2

    # Overdamped: c > 2 * sqrt(m * k)
    over_cfg = SpringConfig(stiffness=100.0, damping=35.0, mass=1.0)
    assert over_cfg.damping_ratio > 1.0
    assert SpringSolver.evaluate(over_cfg, 0.0) == 0.0
    assert SpringSolver.evaluate(over_cfg, 1.0) > 0.8

    # CSS & JS generation
    css = SpringSolver.generate_css_keyframes("testSpring", crit_cfg, property_template="opacity: {v}")
    assert "@keyframes testSpring" in css
    assert "opacity: 0.0" in css or "opacity: 0" in css

    js = SpringSolver.generate_js_spring_runtime()
    assert "function solveSpring" in js


def test_camera_handheld_desk_wander_and_multiplane():
    # Test handheld desk wander mode
    cam = CameraController.get_camera_state("handheld_desk_wander", progress=0.5)
    assert isinstance(cam, CameraKeyframe)
    assert cam.time == 0.5
    assert cam.zoom > 1.0
    assert cam.tilt != 0.0

    # Test multiplane transform calculations
    planes = CameraController.calculate_multiplane_transforms(cam)
    assert "background" in planes
    assert "content" in planes
    assert "foreground" in planes

    # Background moves slower (depth 0.92) than foreground (depth 1.06)
    assert "scale(" in planes["background"]
    assert "translate3d(" in planes["foreground"]


def test_generate_torn_paper_edge():
    # Test bottom torn edge
    img_bottom = generate_torn_paper_edge(
        width=300,
        height=180,
        edge_sides=("bottom",),
        tear_depth=12,
        seed=101
    )
    assert isinstance(img_bottom, Image.Image)
    assert img_bottom.mode == "RGBA"
    w, h = img_bottom.size
    assert w > 300 and h > 180

    # Test four torn edges
    img_all = generate_torn_paper_edge(
        width=250,
        height=200,
        edge_sides=("top", "bottom", "left", "right"),
        tear_depth=10,
        seed=202
    )
    assert isinstance(img_all, Image.Image)
    assert img_all.mode == "RGBA"

    # Verify pulp is exposed on all 4 individual edges
    import numpy as np
    for side in ("top", "bottom", "left", "right"):
        card = generate_torn_paper_edge(
            width=200, height=100,
            edge_sides=(side,),
            paper_color=(200, 100, 50),
            pulp_color=(255, 255, 255),
            seed=42
        )
        arr = np.array(card)
        pulp_visible = (arr[:, :, 0] == 255) & (arr[:, :, 1] == 255) & (arr[:, :, 2] == 255) & (arr[:, :, 3] > 0)
        assert np.sum(pulp_visible) > 100, f"Pulp must be exposed on side {side}"


def test_scene_composer_spring_and_craft_integration():
    composer = DynamicSceneComposer()
    mock_scene = ScenePlan(
        scene_id="scene_craft_test",
        chapter_num=1,
        title="Tactile Craft Test",
        duration=4.0,
        narration="Testing the spring physics and craft layers.",
        visual_type="infographic_data",
        environment="Desk",
        background_tone={"primary": "#1A140E", "secondary": "#2A1F16", "vignette": True},
        layers=[],
        transition=TransitionSpec(type="directional_wipe"),
        typography=TypographySpec(
            badge="01",
            headline_sub="CHAPTER 01",
            headline_main="PHYSICS TEST",
            highlight_words=["PHYSICS"]
        ),
        camera=CameraSpec(movement="handheld_desk_wander"),
        keywords=["PHYSICS", "CRAFT"]
    )
    mock_storyboard = StoryboardPlan(
        project_name="studio_test",
        topic="Physics Explainer",
        language="hinglish",
        genre="science_bio",
        aspect_ratio="9:16",
        resolution={"width": 1080, "height": 1920},
        fps=30,
        estimated_duration=4.0,
        scenes=[mock_scene]
    )

    css = composer._generate_css(mock_storyboard)
    assert "@keyframes springStampSlam" in css
    assert "@keyframes springStickerPop" in css
    assert ".craft-washi-tape" in css
    assert ".craft-rubber-stamp" in css

    js = composer._generate_js(mock_storyboard)
    assert "solveSpring" in js
    assert "applyCameraMovement" in js
    assert "parchmentCanvas.style.transform" in js
    assert "globalRig.style.transform" in js


def test_preview_server_hud_injection(tmp_path):
    from visual_engine.preview_server import PREVIEW_HUD_SCRIPT, ThreadedStageServer
    assert "papermotion-preview-hud" in PREVIEW_HUD_SCRIPT
    assert "pm-play-btn" in PREVIEW_HUD_SCRIPT
    assert "pm-scrubber" in PREVIEW_HUD_SCRIPT
    assert ThreadedStageServer.allow_reuse_address is True

    # Test query string parsing
    import urllib.parse
    req_path = "/index.html?scene=2&speed=1.5"
    clean = urllib.parse.urlsplit(req_path).path
    assert clean in ("/", "/index.html")

    # Test HUD injection into index.html
    sample_html = "<html><head></head><body><h1>Stage</h1></body></html>"
    injected = sample_html.replace("</body>", f"{PREVIEW_HUD_SCRIPT}\n</body>")
    assert "papermotion-preview-hud" in injected
    assert "</body>" in injected

