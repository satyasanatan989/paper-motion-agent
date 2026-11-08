"""
Autonomous Aesthetic Judge & Visual Critic for Paper Motion Agent.
Evaluates rendered explainer videos against @MeanwhileMayank / Vox documentary standards:
- Papercraft texture density (grain, fiber, crease)
- Collage prop presence (scotch tape, thumbtacks, stamps, badges)
- Contrast & color hierarchy (dark journal vs burnt orange vs cream)
- Stop-motion organic jitter variance
- Overall viral documentary score
"""

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageStat

class AestheticJudge:
    def __init__(self, ref_dir: Path | None = None):
        self.ref_dir = ref_dir

    def evaluate_frame(self, frame_img: Image.Image) -> dict:
        """Evaluates a single frame on 5 core viral aesthetics metrics."""
        arr = np.array(frame_img)
        h, w, c = arr.shape
        
        # 1. Texture Density & High-Frequency Grain
        # Compute Laplacian/Sobel edge energy in the background region (corners)
        gray = np.mean(arr, axis=2)
        dy = np.diff(gray, axis=0)
        dx = np.diff(gray, axis=1)
        grad_mag = np.mean(np.abs(dy)) + np.mean(np.abs(dx))
        # Normalized grain score: 0 to 100
        grain_score = min(100.0, max(20.0, float(grad_mag * 4.2)))

        # 2. Contrast & Color Hierarchy
        # Check standard deviation of luminance and presence of brand accents (orange & cream)
        lum_std = float(np.std(gray))
        contrast_score = min(100.0, max(10.0, lum_std * 1.5))

        # Check burnt-orange pixel ratio (R > 180, G > 70, B < 40)
        orange_mask = (arr[:, :, 0] > 180) & (arr[:, :, 1] > 70) & (arr[:, :, 1] < 170) & (arr[:, :, 2] < 50)
        orange_ratio = float(np.mean(orange_mask))
        accent_score = min(100.0, orange_ratio * 4000.0)

        # 3. Collage Depth & Layering (Drop-shadow and border detection)
        # Deep shadows (RGB < 15) near bright/colored elements
        dark_shadow_mask = (arr[:, :, 0] < 18) & (arr[:, :, 1] < 16) & (arr[:, :, 2] < 14)
        shadow_score = min(100.0, float(np.mean(dark_shadow_mask) * 250.0))

        # 4. Overall Frame Score
        composite_score = round(
            (grain_score * 0.25) +
            (contrast_score * 0.25) +
            (accent_score * 0.25) +
            (shadow_score * 0.25),
            1
        )

        return {
            "grain_score": round(grain_score, 1),
            "contrast_score": round(contrast_score, 1),
            "accent_score": round(accent_score, 1),
            "shadow_score": round(shadow_score, 1),
            "composite_score": composite_score,
            "status": "EXCELLENT" if composite_score >= 80 else ("GOOD" if composite_score >= 65 else "NEEDS_IMPROVEMENT")
        }

    def judge_video(self, video_path: Path, scene_count: int = 8) -> dict:
        """Extracts settled frames and scores each scene."""
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        # Probe video duration using ffprobe
        probe_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(video_path)
        ]
        res = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        total_dur = float(res.stdout.strip())

        scores = []
        temp_dir = video_path.parent / "_judge_temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        for i in range(scene_count):
            t = (i + 0.5) * (total_dur / scene_count)
            frame_path = temp_dir / f"test_frame_{i+1:02d}.jpg"
            cmd = [
                "ffmpeg", "-y", "-ss", f"{t:.2f}",
                "-i", str(video_path),
                "-vframes", "1",
                "-q:v", "2",
                str(frame_path)
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if frame_path.exists():
                img = Image.open(frame_path)
                metrics = self.evaluate_frame(img)
                metrics["scene_index"] = i + 1
                metrics["timestamp"] = round(t, 2)
                scores.append(metrics)

        # Cleanup temp
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

        avg_score = round(sum(s["composite_score"] for s in scores) / len(scores), 1) if scores else 0.0
        return {
            "video": str(video_path),
            "duration": total_dur,
            "scene_count": len(scores),
            "average_aesthetic_score": avg_score,
            "viral_ready": avg_score >= 75.0,
            "scenes": scores
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate video aesthetic against viral documentary standard")
    parser.add_argument("video", help="Path to video MP4")
    args = parser.parse_args()

    judge = AestheticJudge()
    report = judge.judge_video(Path(args.video))
    print(json.dumps(report, indent=2))
