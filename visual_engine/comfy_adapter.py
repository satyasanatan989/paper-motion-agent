"""
ComfyUI Local Adapter for PaperMotion AI.
Enables local diffusion-powered asset and macro texture generation for Food Science reels.
Communicates via ComfyUI's local REST API (http://127.0.0.1:8188).
Runs in low-VRAM mode (optimized for 4GB RTX 2050 laptops).
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
import urllib.request
import urllib.error
import json
import time

class ComfyUIAdapter:
    """Client for local ComfyUI instances generating photorealistic food science assets."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8188):
        self.base_url = f"http://{host}:{port}"
        self.assets_dir = Path(__file__).parent.parent / "assets" / "comfy_generated"
        self.assets_dir.mkdir(parents=True, exist_ok=True)

    def is_available(self) -> bool:
        """Checks if local ComfyUI server is actively responding."""
        try:
            req = urllib.request.Request(f"{self.base_url}/system_stats", headers={"User-Agent": "PaperMotion-AI"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                return resp.status == 200
        except Exception:
            return False

    def get_hardware_info(self) -> Optional[Dict[str, Any]]:
        """Retrieves active device and VRAM status from ComfyUI."""
        try:
            req = urllib.request.Request(f"{self.base_url}/system_stats", headers={"User-Agent": "PaperMotion-AI"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            return None

    def build_sd15_food_prompt(
        self,
        positive_prompt: str,
        negative_prompt: str = "cartoon, text, low quality, blurry, deformed, watermark, oversaturated",
        width: int = 768,
        height: int = 768,
        seed: int = 42
    ) -> Dict[str, Any]:
        """
        Constructs standard ComfyUI API payload for lightweight SD 1.5 / Turbo models.
        Fits within 3.5GB VRAM using --medvram.
        """
        prompt_workflow = {
            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": 20,
                    "cfg": 7.0,
                    "sampler_name": "euler_ancestral",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "4": {
                "inputs": {
                    "ckpt_name": "v1-5-pruned-emaonly.safetensors"
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "text": f"cinematic macro food photography, {positive_prompt}, 8k, dark studio lighting, highly detailed texture, professional documentary style",
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": negative_prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "8": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode"
            },
            "9": {
                "inputs": {
                    "filename_prefix": "FoodCode_Asset",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            }
        }
        return {"prompt": prompt_workflow}

    def queue_generation(self, prompt_data: Dict[str, Any]) -> Optional[str]:
        """Submits generation job to ComfyUI REST queue."""
        try:
            data = json.dumps(prompt_data).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url}/prompt",
                data=data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res.get("prompt_id")
        except Exception as e:
            print(f"[ComfyUI Adapter Error] Queue failed: {e}")
            return None
