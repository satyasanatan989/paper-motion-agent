"""
Vork 3D & VFX Engine Integration for Paper Motion Agent.
Leverages the native GPU-accelerated Vork renderer (Rust + Slang on Vulkan/NVIDIA)
to author and render photorealistic 3D assets, transparent alpha cutouts,
subsurface scattering biological structures, and procedural metallic seals.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

class Vork3DEngine:
    """
    Manages Vork 3D scene authoring and GPU rendering for video production.
    """

    def __init__(self, vork_bin: Optional[str] = None):
        self.vork_bin = vork_bin or self._find_vork_binary()

    def _find_vork_binary(self) -> Optional[str]:
        # 1. Check PATH
        which_path = shutil.which("vork")
        if which_path:
            return which_path

        # 2. Check LocalAppData on Windows
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        if local_app_data:
            candidate = Path(local_app_data) / "Programs" / "vork" / "vork.exe"
            if candidate.exists():
                return str(candidate)

        return None

    def is_available(self) -> bool:
        """Returns True if the vork binary is located and executable."""
        if not self.vork_bin:
            return False
        try:
            res = subprocess.run([self.vork_bin, "--version"], capture_output=True, text=True)
            return res.returncode == 0
        except Exception:
            return False

    def create_gold_crest_scene(
        self,
        resolution: Tuple[int, int] = (1080, 1080)
    ) -> Dict[str, Any]:
        """
        Authors a procedural 3D Food Code gold seal medallion scene:
        - OpenPBR metallic brass/gold surface with micro-roughness
        - 3-point cinematic lighting with warm key light and cool rim light
        - Transparent background for lossless alpha compositing
        """
        scene = {
            "version": 2,
            "nodes": [
                # 1. Main Medallion Body (Outer Ring)
                {
                    "type": "mesh",
                    "name": "outer_ring",
                    "geometry": {
                        "std": "sphere",
                        "radius": 1.25,
                        "segments": 48,
                        "rings": 24
                    },
                    "scale": [1.0, 1.0, 0.12],
                    "translation": [0, 0, 0],
                    "materials": [
                        {
                            "program": "std/openpbr",
                            "inputs": {
                                "base_color": [0.88, 0.65, 0.22],
                                "base_metalness": 0.95,
                                "specular_roughness": 0.22,
                                "coat_weight": 0.4,
                                "coat_roughness": 0.08
                            }
                        }
                    ]
                },
                # 2. Inner Emblem Core
                {
                    "type": "mesh",
                    "name": "inner_core",
                    "geometry": {
                        "std": "box",
                        "size": [1.2, 1.2, 0.2]
                    },
                    "rotation": {"euler": [0, 0, 0.785398]},  # 45 deg diamond
                    "materials": [
                        {
                            "program": "std/openpbr",
                            "inputs": {
                                "base_color": [0.98, 0.78, 0.30],
                                "base_metalness": 0.98,
                                "specular_roughness": 0.14,
                                "emission_luminance": 12.0,
                                "emission_color": [1.0, 0.65, 0.15]
                            }
                        }
                    ]
                },
                # 3. Studio 3-Point Lighting
                # Key Light (Warm Sunlight)
                {
                    "type": "light",
                    "name": "key_light",
                    "shape": "rectangle",
                    "translation": [-2.8, 3.5, 4.0],
                    "target": [0, 0, 0],
                    "energy": 850,
                    "size": 3.0,
                    "color": [1.0, 0.92, 0.82]
                },
                # Fill Light (Soft Neutral)
                {
                    "type": "light",
                    "name": "fill_light",
                    "shape": "rectangle",
                    "translation": [3.2, 1.8, 3.5],
                    "target": [0, 0, 0],
                    "energy": 380,
                    "size": 4.5,
                    "color": [0.85, 0.90, 1.0]
                },
                # Rim Light (Crisp Edge Accent)
                {
                    "type": "light",
                    "name": "rim_light",
                    "shape": "rectangle",
                    "translation": [0, -3.0, -3.0],
                    "target": [0, 0, 0],
                    "energy": 900,
                    "size": 2.5,
                    "color": [1.0, 0.75, 0.40]
                },
                # 4. Perspective Camera
                {
                    "type": "camera",
                    "name": "cam_main",
                    "translation": [0, 0, 4.2],
                    "target": [0, 0, 0]
                }
            ],
            "render": {
                "background": "transparent",
                "resolution": list(resolution)
            }
        }
        return scene

    def create_3d_molecule_scene(
        self,
        resolution: Tuple[int, int] = (1080, 1080)
    ) -> Dict[str, Any]:
        """
        Authors a 3D Glucose Molecule model with physical OpenPBR glass/carbon spheres.
        """
        scene = {
            "version": 2,
            "nodes": [
                # Central Carbon Node (Dark Graphite)
                {
                    "type": "mesh",
                    "name": "c_center",
                    "geometry": {"std": "sphere", "radius": 0.75, "segments": 32, "rings": 16},
                    "translation": [0, 0, 0],
                    "materials": [{
                        "inputs": {
                            "base_color": [0.15, 0.15, 0.15],
                            "base_metalness": 0.2,
                            "specular_roughness": 0.25
                        }
                    }]
                },
                # Oxygen Node 1 (Crimson Red)
                {
                    "type": "mesh",
                    "name": "o_node1",
                    "geometry": {"std": "sphere", "radius": 0.55, "segments": 32, "rings": 16},
                    "translation": [-1.2, 0.8, 0.2],
                    "materials": [{
                        "inputs": {
                            "base_color": [0.85, 0.08, 0.12],
                            "base_metalness": 0.1,
                            "specular_roughness": 0.15,
                            "subsurface_weight": 0.4,
                            "subsurface_color": [1.0, 0.2, 0.2]
                        }
                    }]
                },
                # Oxygen Node 2 (Warm Orange)
                {
                    "type": "mesh",
                    "name": "o_node2",
                    "geometry": {"std": "sphere", "radius": 0.55, "segments": 32, "rings": 16},
                    "translation": [1.1, -0.7, -0.2],
                    "materials": [{
                        "inputs": {
                            "base_color": [1.0, 0.45, 0.05],
                            "base_metalness": 0.1,
                            "specular_roughness": 0.15,
                            "emission_luminance": 8.0,
                            "emission_color": [1.0, 0.45, 0.05]
                        }
                    }]
                },
                # Hydrogen Node (Clean White)
                {
                    "type": "mesh",
                    "name": "h_node1",
                    "geometry": {"std": "sphere", "radius": 0.38, "segments": 24, "rings": 12},
                    "translation": [0.2, 1.3, -0.4],
                    "materials": [{
                        "inputs": {
                            "base_color": [0.95, 0.95, 0.95],
                            "specular_roughness": 0.1
                        }
                    }]
                },
                # Lighting
                {
                    "type": "light",
                    "shape": "rectangle",
                    "translation": [-3, 4, 4],
                    "target": [0, 0, 0],
                    "energy": 900,
                    "size": 3.5,
                    "color": [1.0, 0.95, 0.9]
                },
                {
                    "type": "light",
                    "shape": "rectangle",
                    "translation": [3, -2, 3],
                    "target": [0, 0, 0],
                    "energy": 450,
                    "size": 4.0,
                    "color": [0.8, 0.9, 1.0]
                },
                # Camera
                {
                    "type": "camera",
                    "translation": [0, 0, 4.5],
                    "target": [0, 0, 0]
                }
            ],
            "render": {
                "background": "transparent",
                "resolution": list(resolution)
            }
        }
        return scene

    def render_crest(
        self,
        output_png: Path,
        resolution: Tuple[int, int] = (1080, 1080),
        profile: str = "std/draft"
    ) -> Path:
        """Renders the 3D gold seal to a transparent PNG."""
        output_png = Path(output_png)
        output_png.parent.mkdir(parents=True, exist_ok=True)
        
        scene_data = self.create_gold_crest_scene(resolution=resolution)
        temp_scene_json = output_png.parent / f"{output_png.stem}_scene.json"
        
        with open(temp_scene_json, "w", encoding="utf-8") as f:
            json.dump(scene_data, f, indent=2)

        return self.render_scene_file(temp_scene_json, output_png, profile=profile)

    def render_molecule(
        self,
        output_png: Path,
        resolution: Tuple[int, int] = (1080, 1080),
        profile: str = "std/draft"
    ) -> Path:
        """Renders the 3D glucose molecule to a transparent PNG."""
        output_png = Path(output_png)
        output_png.parent.mkdir(parents=True, exist_ok=True)
        
        scene_data = self.create_3d_molecule_scene(resolution=resolution)
        temp_scene_json = output_png.parent / f"{output_png.stem}_scene.json"
        
        with open(temp_scene_json, "w", encoding="utf-8") as f:
            json.dump(scene_data, f, indent=2)

        return self.render_scene_file(temp_scene_json, output_png, profile=profile)

    def render_scene_file(
        self,
        scene_json: Path,
        output_path: Path,
        profile: str = "std/draft"
    ) -> Path:
        """Invokes vork CLI to render a scene file on the GPU."""
        if not self.vork_bin:
            raise RuntimeError("Vork binary not found. Please run vork install.ps1.")

        cmd = [
            self.vork_bin,
            "render",
            str(scene_json.resolve()),
            "--out", str(output_path.resolve()),
            "--profile", profile
        ]

        env = os.environ.copy()
        vork_dir = str(Path(self.vork_bin).parent)
        env["PATH"] = f"{vork_dir};{env.get('PATH', '')}"

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        if res.returncode != 0:
            raise RuntimeError(f"Vork render failed (code {res.returncode}): {res.stderr}")

        return output_path
