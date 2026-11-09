import pytest
from pathlib import Path
from visual_engine.vork_engine import Vork3DEngine

def test_vork_engine_detection():
    engine = Vork3DEngine()
    assert engine.is_available() is True

def test_vork_scene_creation(tmp_path):
    engine = Vork3DEngine()
    scene_file = tmp_path / "test_scene.json"
    scene_data = engine.create_gold_crest_scene()
    
    assert "version" in scene_data
    assert scene_data["version"] == 2
    assert "nodes" in scene_data
    assert any(n.get("type") == "camera" for n in scene_data["nodes"])
    assert any(n.get("type") == "light" for n in scene_data["nodes"])
    assert scene_data["render"]["background"] == "transparent"

def test_vork_render_asset(tmp_path):
    engine = Vork3DEngine()
    out_png = tmp_path / "crest_3d.png"
    result = engine.render_crest(out_png, resolution=(512, 512), profile="std/draft")
    
    assert out_png.exists()
    assert out_png.stat().st_size > 10000
