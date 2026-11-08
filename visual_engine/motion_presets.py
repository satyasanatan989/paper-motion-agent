"""
Motion Presets and Procedural Particle Engine.
Encodes cinematic easing curves, spring dynamics, and particle simulations.
"""

import math
from typing import List, Dict, Any

class MotionEasing:
    """Mathematical easing and spring dynamics functions."""

    @staticmethod
    def ease_out_cubic(x: float) -> float:
        return 1.0 - math.pow(1.0 - max(0.0, min(1.0, x)), 3)

    @staticmethod
    def ease_in_out_quad(x: float) -> float:
        x = max(0.0, min(1.0, x))
        return 2.0 * x * x if x < 0.5 else 1.0 - math.pow(-2.0 * x + 2.0, 2) / 2.0

    @staticmethod
    def spring_overshoot(x: float, tension: float = 1.7) -> float:
        """Classic elastic overshoot for rubber stamp / metric card impacts."""
        x = max(0.0, min(1.0, x)) - 1.0
        return x * x * ((tension + 1.0) * x + tension) + 1.0

    @staticmethod
    def breathing_oscillation(t: float, frequency: float = 2.5, amplitude: float = 0.05) -> float:
        return 1.0 + amplitude * math.sin(t * frequency)

class ParticleField:
    """Procedural generator for high-retention cinematic particle effects."""

    @staticmethod
    def generate_particles_svg(
        field_type: str = "steam",
        count: int = 12,
        width: int = 760,
        height: int = 500
    ) -> str:
        """
        Generates SVG elements for organic particle emitters.
        field_type: 'steam', 'acid_bubbles', 'sparks', 'fiber_dust'
        """
        svg_elements = []
        import random
        rng = random.Random(42)

        for i in range(count):
            cx = rng.randint(60, width - 60)
            cy = rng.randint(80, height - 80)
            r = rng.randint(4, 14) if field_type != "sparks" else rng.randint(2, 6)

            if field_type == "steam":
                fill = "rgba(240, 230, 215, 0.45)"
                filter_style = "filter: blur(4px);"
            elif field_type == "acid_bubbles":
                fill = "rgba(255, 90, 80, 0.75)"
                filter_style = "filter: drop-shadow(0 0 8px rgba(255, 60, 50, 0.6));"
            elif field_type == "sparks":
                fill = "#FFD700"
                filter_style = "filter: drop-shadow(0 0 10px #FF8C00);"
            else:
                fill = "rgba(180, 150, 110, 0.35)"
                filter_style = ""

            svg_elements.append(
                f'<circle id="pt-{i}" class="particle-node" data-speed="{rng.uniform(0.8, 2.2):.2f}" '
                f'cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" style="{filter_style}" />'
            )

        return f'<g class="particle-field particle-{field_type}">{"".join(svg_elements)}</g>'
