"""
Unit Tests for Beat Schema, BeatSpec, and Beat Validation Rules.
Validates:
1. schemas/beat_schema.json compliance
2. Pacing (1.5-3.5s per beat)
3. Headline line word limits (top <= 4, punch <= 3)
4. Widget presence tied strictly to numbers
5. Prevention of 3 consecutive identical templates
"""

import json
import pytest
from pathlib import Path
import jsonschema

from storyboard.generator import (
    BeatSpec,
    StoryboardPlan,
    StoryboardGenerator
)

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "beat_schema.json"

@pytest.fixture
def beat_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def test_beat_schema_validation(beat_schema):
    sample_beat = {
        "beat_id": "b01",
        "start": 0.0,
        "end": 2.5,
        "voice": "Sirf 8 minute tak... kisi ko pata hi nahi chalega.",
        "headline_top": "FOR 8 MINUTES",
        "headline_punch": "NOBODY KNOWS",
        "caption_chunk": "8 minute tak",
        "caption_highlight": "8",
        "scene_id": "gali_lookup",
        "scene_reuse": False,
        "template": "fullbleed_parallax",
        "assets": [
            {"id": "sun", "prompt": "golden sun glowing", "layer": "mid", "enter": "pop"}
        ],
        "widget": {"type": "flip_counter", "value": "8:19", "unit": "MIN SEC"},
        "stamp": None,
        "camera": "slow_push_in",
        "sfx": ["paper_flip", "tick"]
    }

    # Should validate cleanly against beat_schema.json
    jsonschema.validate(instance=sample_beat, schema=beat_schema)

def test_validate_beat_rules():
    gen = StoryboardGenerator()

    valid_beats = [
        BeatSpec(
            beat_id="b01",
            start=0.0,
            end=2.5,
            voice="Kya packaged nariyal pani sach me healthy hai?",
            headline_top="IS IT HEALTHY?",
            headline_punch="COCONUT WATER",
            caption_chunk="nariyal pani",
            caption_highlight="HEALTHY",
            scene_id="tapri_desk",
            template="notebook_sticker",
            assets=[{"id": "tetra_pack", "prompt": "coconut water pack", "layer": "mid", "enter": "pop"}],
            camera="slow_push_in",
            sfx=["paper_flip"]
        ),
        BeatSpec(
            beat_id="b02",
            start=2.5,
            end=5.2,
            voice="Reality check: 200 ml me 15 gram added sugar!",
            headline_top="SHOCKING REALITY",
            headline_punch="15G SUGAR",
            caption_chunk="15 gram sugar",
            caption_highlight="SUGAR",
            scene_id="tapri_desk",
            template="object_on_dark",
            widget={"type": "odometer", "value": "15", "unit": "G"},
            camera="fast_push_in",
            sfx=["odometer_tick"],
            scene_reuse=True
        )
    ]

    issues = gen.validate_beat_rules(valid_beats)
    assert len(issues) == 0, f"Expected 0 issues for valid beats, got: {issues}"

def test_validate_beat_rules_catches_violations():
    gen = StoryboardGenerator()

    invalid_beats = [
        # Violation 1: duration too long (4.5s > 3.5s)
        # Violation 2: headline_top > 4 words
        # Violation 3: headline_punch > 3 words
        # Violation 4: widget without numbers in voice
        BeatSpec(
            beat_id="b01",
            start=0.0,
            end=4.5,
            voice="Yeh packaged drink bilkul bhi fresh nahi hai dosto",
            headline_top="THIS IS A VERY LONG HEADLINE", # 6 words > 4
            headline_punch="TOTALLY FAKE JUICE DRINK",      # 4 words > 3
            caption_chunk="fake drink",
            caption_highlight="FAKE",
            scene_id="desk",
            template="notebook_sticker",
            widget={"type": "odometer", "value": "100", "unit": "%"} # No number in voice
        ),
        BeatSpec(
            beat_id="b02",
            start=4.5,
            end=7.0,
            voice="Clue number two",
            headline_top="CLUE TWO",
            headline_punch="LAB RESULTS",
            caption_chunk="lab test",
            caption_highlight="LAB",
            scene_id="desk",
            template="notebook_sticker"
        ),
        # Violation 5: 3 consecutive notebook_sticker without scene_reuse
        BeatSpec(
            beat_id="b03",
            start=7.0,
            end=9.2,
            voice="Verdict time now",
            headline_top="FINAL VERDICT",
            headline_punch="NOT HEALTHY",
            caption_chunk="not healthy",
            caption_highlight="HEALTHY",
            scene_id="other_desk",
            template="notebook_sticker",
            scene_reuse=False
        )
    ]

    issues = gen.validate_beat_rules(invalid_beats)
    assert any("outside ideal 1.5–3.5s window" in iss for iss in issues)
    assert any("headline_top" in iss and "exceeds 4 words" in iss for iss in issues)
    assert any("headline_punch" in iss and "exceeds 3 words" in iss for iss in issues)
    assert any("widget present but voice text contains no number" in iss for iss in issues)
    assert any("used 3 times consecutively" in iss for iss in issues)

def test_generate_storyboard_from_beats():
    gen = StoryboardGenerator()
    beats = [
        BeatSpec(
            beat_id="b01",
            start=0.0,
            end=2.4,
            voice="Look up at the sky right now.",
            headline_top="LOOK UP",
            headline_punch="THE SKY",
            caption_chunk="look up",
            caption_highlight="SKY",
            scene_id="gali_lookup",
            template="fullbleed_parallax",
            camera="slow_push_in"
        ),
        BeatSpec(
            beat_id="b02",
            start=2.4,
            end=5.0,
            voice="What if the Moon vanished in 1 second?",
            headline_top="WHAT IF",
            headline_punch="MOON VANISHED",
            caption_chunk="moon vanished",
            caption_highlight="VANISHED",
            scene_id="night_sky",
            template="object_on_dark",
            widget={"type": "flip_counter", "value": "1", "unit": "SEC"},
            camera="fast_push_in"
        )
    ]

    storyboard = gen.generate_storyboard_from_beats(
        topic="What if the Moon disappeared?",
        beats=beats,
        project_name="moon_disappeared",
        genre="what_if_space",
        fps=30
    )

    assert len(storyboard.beats) == 2
    assert len(storyboard.scenes) == 2
    assert storyboard.estimated_duration == 5.0
    assert storyboard.scenes[0].scene_id == "b01"
    assert storyboard.scenes[0].duration == 2.4
    assert storyboard.scenes[1].widget["value"] == "1"
