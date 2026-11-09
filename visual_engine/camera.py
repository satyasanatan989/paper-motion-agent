"""
2.5D Camera Controller and Depth Parallax Engine.
Simulates physical cinema cameras (dolly, pan, tilt, zoom, and multi-plane depth parallax).
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import math

@dataclass(frozen=True)
class CameraKeyframe:
    time: float
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    zoom: float = 1.0
    tilt: float = 0.0  # degrees
    pan: float = 0.0   # degrees

class CameraController:
    """Calculates cinematic 2.5D camera coordinates and layer parallax offsets."""

    @staticmethod
    def get_camera_state(
        movement: str,
        progress: float,
        zoom_start: float = 1.0,
        zoom_end: float = 1.07
    ) -> CameraKeyframe:
        """
        Computes camera position and zoom at normalized progress (0.0 to 1.0).
        Uses smooth cubic easing to avoid robotic linear motion.
        """
        # Smooth cubic ease out: 1 - (1 - p)^3
        p = max(0.0, min(1.0, progress))
        ease_p = 1.0 - math.pow(1.0 - p, 3)

        if movement == "slow_dolly_in":
            zoom = zoom_start + (zoom_end - zoom_start) * ease_p
            return CameraKeyframe(time=p, x=0.0, y=-15.0 * ease_p, z=30.0 * ease_p, zoom=zoom)

        elif movement == "fast_push_in":
            zoom = zoom_start + (zoom_end * 1.08 - zoom_start) * (p * p)
            return CameraKeyframe(time=p, x=0.0, y=-25.0 * p, z=50.0 * p, zoom=zoom)

        elif movement == "smooth_pull_back":
            zoom = zoom_end - (zoom_end - zoom_start) * ease_p
            return CameraKeyframe(time=p, x=0.0, y=10.0 * ease_p, z=-20.0 * ease_p, zoom=zoom)

        elif movement == "pan_right":
            x_shift = -40.0 * ease_p
            zoom = zoom_start + (zoom_end - zoom_start) * 0.5 * ease_p
            return CameraKeyframe(time=p, x=x_shift, y=0.0, z=0.0, zoom=zoom, pan=1.5 * ease_p)

        elif movement == "pan_left":
            x_shift = 40.0 * ease_p
            zoom = zoom_start + (zoom_end - zoom_start) * 0.5 * ease_p
            return CameraKeyframe(time=p, x=x_shift, y=0.0, z=0.0, zoom=zoom, pan=-1.5 * ease_p)

        elif movement == "tilt_up":
            y_shift = 45.0 * ease_p
            zoom = zoom_start + (zoom_end - zoom_start) * ease_p
            return CameraKeyframe(time=p, x=0.0, y=y_shift, z=15.0 * ease_p, zoom=zoom, tilt=-2.0 * ease_p)

        elif movement == "tilt_down":
            y_shift = -45.0 * ease_p
            zoom = zoom_start + (zoom_end - zoom_start) * ease_p
            return CameraKeyframe(time=p, x=0.0, y=y_shift, z=15.0 * ease_p, zoom=zoom, tilt=2.0 * ease_p)

        elif movement == "subtle_orbit":
            angle = p * math.pi * 0.5
            x_shift = 20.0 * math.sin(angle)
            y_shift = 10.0 * math.cos(angle) - 10.0
            zoom = zoom_start + 0.04 * math.sin(angle)
            return CameraKeyframe(time=p, x=x_shift, y=y_shift, z=0.0, zoom=zoom, tilt=1.0 * math.sin(angle))

        elif movement == "handheld_desk_wander":
            # Organic handheld micro-wander (Vox / MeanwhileMayank desk camera style)
            x_shift = 14.0 * math.sin(p * math.pi * 2.0 * 0.4) + 4.0 * math.cos(p * math.pi * 4.0 * 0.3)
            y_shift = 9.0 * math.cos(p * math.pi * 2.0 * 0.35) - 4.0 * math.sin(p * math.pi * 3.0 * 0.5)
            tilt_w = 0.75 * math.sin(p * math.pi * 2.0 * 0.5)
            zoom = zoom_start + 0.025 * (1.0 - math.cos(p * math.pi))
            return CameraKeyframe(time=p, x=x_shift, y=y_shift, z=10.0 * p, zoom=zoom, tilt=tilt_w)

        else: # static_focus
            return CameraKeyframe(time=p, x=0.0, y=0.0, z=0.0, zoom=zoom_start)

    @staticmethod
    def calculate_layer_transform(
        cam: CameraKeyframe,
        depth_factor: float
    ) -> str:
        """
        Generates CSS transform string for a specific depth plane.
        Foreground moves faster (higher parallax), background moves slower.
        """
        px = cam.x * depth_factor
        py = cam.y * depth_factor
        pz = cam.z * depth_factor
        scale = 1.0 + (cam.zoom - 1.0) * depth_factor

        return f"translate3d({px:.2f}px, {py:.2f}px, {pz:.2f}px) scale({scale:.4f})"

    @classmethod
    def calculate_multiplane_transforms(cls, cam: CameraKeyframe) -> Dict[str, str]:
        """Calculates optical parallax CSS transforms for all 3 spatial planes."""
        return {
            "background": cls.calculate_layer_transform(cam, depth_factor=0.92),
            "content": cls.calculate_layer_transform(cam, depth_factor=1.00),
            "foreground": cls.calculate_layer_transform(cam, depth_factor=1.06),
        }

    @staticmethod
    def generate_js_camera_runtime() -> str:
        """Returns the client-side JavaScript camera evaluator injected into timeline.js."""
        return """
        function applyCameraMovement(movement, progress, zoomStart, zoomEnd) {
          const p = Math.max(0.0, Math.min(1.0, progress));
          const easeP = 1.0 - Math.pow(1.0 - p, 3);
          let cx = 0, cy = 0, cz = 0, zoom = zoomStart, tilt = 0, pan = 0;
          
          if (movement === 'slow_dolly_in') {
            zoom = zoomStart + (zoomEnd - zoomStart) * easeP;
            cy = -15 * easeP; cz = 30 * easeP;
          } else if (movement === 'fast_push_in') {
            zoom = zoomStart + (zoomEnd * 1.08 - zoomStart) * (p * p);
            cy = -25 * p; cz = 50 * p;
          } else if (movement === 'smooth_pull_back') {
            zoom = zoomEnd - (zoomEnd - zoomStart) * easeP;
            cy = 10 * easeP;
            cz = -20 * easeP;
          } else if (movement === 'pan_right') {
            cx = -40 * easeP;
            zoom = zoomStart + (zoomEnd - zoomStart) * 0.5 * easeP;
            pan = 1.5 * easeP;
          } else if (movement === 'pan_left') {
            cx = 40 * easeP;
            zoom = zoomStart + (zoomEnd - zoomStart) * 0.5 * easeP;
            pan = -1.5 * easeP;
          } else if (movement === 'tilt_up') {
            cy = 45 * easeP;
            cz = 15 * easeP;
            zoom = zoomStart + (zoomEnd - zoomStart) * easeP;
            tilt = -2.0 * easeP;
          } else if (movement === 'tilt_down') {
            cy = -45 * easeP;
            cz = 15 * easeP;
            zoom = zoomStart + (zoomEnd - zoomStart) * easeP;
            tilt = 2.0 * easeP;
          } else if (movement === 'subtle_orbit') {
            const angle = p * Math.PI * 0.5;
            cx = 20 * Math.sin(angle);
            cy = 10 * Math.cos(angle) - 10;
            zoom = zoomStart + 0.04 * Math.sin(angle);
            tilt = 1.0 * Math.sin(angle);
          } else if (movement === 'handheld_desk_wander') {
            cx = 14 * Math.sin(p * Math.PI * 2 * 0.4) + 4 * Math.cos(p * Math.PI * 4 * 0.3);
            cy = 9 * Math.cos(p * Math.PI * 2 * 0.35) - 4 * Math.sin(p * Math.PI * 3 * 0.5);
            tilt = 0.75 * Math.sin(p * Math.PI * 2 * 0.5);
            zoom = zoomStart + 0.025 * (1.0 - Math.cos(p * Math.PI));
            cz = 10 * p;
          }
          return { cx, cy, cz, zoom, tilt, pan };
        }
        """
