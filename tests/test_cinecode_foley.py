import numpy as np
import pytest
from pathlib import Path
from voice.cinecode_foley import CineCodeFoleyEngine

def test_foley_transients_generation():
    engine = CineCodeFoleyEngine(sample_rate=44100)
    
    whoosh = engine.generate_card_whoosh(duration=0.35)
    assert isinstance(whoosh, np.ndarray)
    assert len(whoosh) == int(44100 * 0.35)
    assert np.max(np.abs(whoosh)) > 0.05

    tape = engine.generate_tape_snap(duration=0.18)
    assert isinstance(tape, np.ndarray)
    assert len(tape) == int(44100 * 0.18)
    assert np.max(np.abs(tape)) > 0.05

    pin = engine.generate_pushpin_thud(duration=0.22)
    assert isinstance(pin, np.ndarray)
    assert len(pin) == int(44100 * 0.22)
    assert np.max(np.abs(pin)) > 0.05

    stamp = engine.generate_rubber_stamp_slam(duration=0.45)
    assert isinstance(stamp, np.ndarray)
    assert len(stamp) == int(44100 * 0.45)
    assert np.max(np.abs(stamp)) > 0.05

    click = engine.generate_split_flap_click(duration=0.05)
    assert isinstance(click, np.ndarray)
    assert len(click) == int(44100 * 0.05)
    assert np.max(np.abs(click)) > 0.05

    pop = engine.generate_acid_bubble_pop(duration=0.12)
    assert isinstance(pop, np.ndarray)
    assert len(pop) == int(44100 * 0.12)
    assert np.max(np.abs(pop)) > 0.05

def test_food_code_foley_timeline():
    engine = CineCodeFoleyEngine(sample_rate=44100)
    total_dur = 57.46
    scene_starts = [0.0, 4.91, 11.52, 18.27, 24.64, 34.18, 43.93, 51.67]
    
    track = engine.build_food_code_foley_track(total_duration=total_dur, scene_starts=scene_starts)
    assert isinstance(track, np.ndarray)
    assert len(track) == int(44100 * total_dur)
    assert np.max(np.abs(track)) > 0.1
    # Check that track is not silent
    rms = np.sqrt(np.mean(track ** 2))
    assert rms > 0.005
