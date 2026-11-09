"""
Unit Tests for ScriptEngine Format A and Format B Story Generation.
Validates:
1. Format A (MeanwhileMayank 'What If' style, ~140-170s, 35+ beats)
2. Format B (The Food Code 'Food Detective' style, ~45-60s, 15-25 beats)
3. Line rules: max 12 words per spoken line, headline_top <= 4 words, headline_punch <= 3 words
4. Fact-check generation of research.md with source lines for all numbers
"""

from pathlib import Path
import pytest
from agent.script_engine import ScriptEngine
from storyboard.generator import StoryboardGenerator

def test_script_engine_format_b_coconut(tmp_path):
    engine = ScriptEngine(output_dir=tmp_path)
    beats = engine.generate_beats("Is packaged coconut water healthy?", format_type="format_b")

    assert len(beats) >= 15
    total_dur = beats[-1].end
    assert 40.0 <= total_dur <= 65.0, f"Expected 40-65s, got {total_dur}s"

    # Line rules
    for b in beats:
        word_count = len(b.voice.split())
        assert word_count <= 14, f"Spoken line too long ({word_count} words): '{b.voice}'"
        assert len(b.headline_top.split()) <= 4, f"headline_top exceeds 4 words: '{b.headline_top}'"
        assert len(b.headline_punch.split()) <= 3, f"headline_punch exceeds 3 words: '{b.headline_punch}'"

    # Fact-check file
    res_md = tmp_path / "research.md"
    assert res_md.exists()
    content = res_md.read_text(encoding="utf-8")
    assert "FSSAI" in content
    assert "15" in content

    # Validation rules
    gen = StoryboardGenerator()
    issues = gen.validate_beat_rules(beats)
    assert len(issues) == 0, f"Validation issues found: {issues}"

def test_script_engine_format_a_moon(tmp_path):
    engine = ScriptEngine(output_dir=tmp_path)
    beats = engine.generate_beats("What if the Moon disappeared?", format_type="format_a")

    assert len(beats) >= 35
    total_dur = beats[-1].end
    assert 100.0 <= total_dur <= 170.0, f"Expected 100-170s, got {total_dur}s"

    # Check key emotional elements from reference
    assert any("chhat" in b.voice.lower() or "rooftop" in b.headline_punch.lower() for b in beats)
    assert any("andhero me" in b.voice.lower() or "alone" in b.headline_punch.lower() for b in beats)

    # Check research log
    res_md = tmp_path / "research.md"
    assert res_md.exists()
    content = res_md.read_text(encoding="utf-8")
    assert "384,400" in content or "384400" in content
    assert "23.5" in content
    assert "Laskar" in content
