"""
Damped Harmonic Oscillator Spring Physics Engine for Tactile Papercraft.
Simulates physical spring mechanics (stiffness, damping, mass, and velocity)
for editorial cutouts, dropped stamps, hanging price tags, and kinetic typography.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class SpringConfig:
    """Parameters defining a physical spring system."""
    stiffness: float  # k: spring tension / responsiveness
    damping: float    # c: resistance / friction to oscillations
    mass: float = 1.0 # m: physical object weight
    initial_velocity: float = 0.0

    @property
    def damping_ratio(self) -> float:
        """Zeta (ζ): < 1.0 is underdamped (oscillates), = 1.0 is critically damped, > 1.0 is overdamped."""
        denom = 2.0 * math.sqrt(self.mass * self.stiffness)
        return self.damping / denom if denom > 0 else 1.0

    @property
    def natural_frequency(self) -> float:
        """Omega 0 (ω₀): undamped angular frequency in rad/s."""
        return math.sqrt(self.stiffness / self.mass)


# Tactile editorial motion presets
SPRING_PRESETS: Dict[str, SpringConfig] = {
    # Hard cardboard slam with crisp subtle rebound (rubber stamps, evidence cards)
    "stamp_slam": SpringConfig(stiffness=280.0, damping=22.0, mass=1.0),
    # Snappy sticker drop with light tactile wobble (vinyl stickers, washi tape)
    "sticker_pop": SpringConfig(stiffness=220.0, damping=15.0, mass=1.0),
    # Dangled hanging tag swinging and gently settling (price tags, hazard ribbon)
    "hanging_swing": SpringConfig(stiffness=110.0, damping=7.5, mass=1.0),
    # Rapid mechanical register click (odometer dials, metric counters)
    "odometer_tick": SpringConfig(stiffness=380.0, damping=28.0, mass=1.0),
    # Punchy headline type entrance with high-energy landing
    "headline_punch": SpringConfig(stiffness=260.0, damping=19.0, mass=1.0),
    # Smooth paper slip sliding in across parchment
    "paper_glide": SpringConfig(stiffness=95.0, damping=18.0, mass=1.0),
}


class SpringSolver:
    """Calculates displacement values over time using closed-form analytical solutions."""

    @staticmethod
    def evaluate(config: SpringConfig, t: float) -> float:
        """
        Evaluates normalized spring progress from 0.0 (start) to 1.0 (settled).
        Returns the instantaneous position at time t (seconds).
        """
        if t <= 0.0:
            return 0.0

        zeta = config.damping_ratio
        w0 = config.natural_frequency

        if math.isclose(zeta, 1.0, abs_tol=1e-4):
            # Critically damped: Reaches equilibrium fastest without oscillation
            decay = math.exp(-w0 * t)
            c1 = 1.0
            c2 = w0 - config.initial_velocity
            return 1.0 - decay * (c1 + c2 * t)
        elif zeta < 1.0:
            # Underdamped: Oscillates around target before settling
            wd = w0 * math.sqrt(max(1e-9, 1.0 - zeta * zeta))
            decay = math.exp(-zeta * w0 * t)
            # Boundary conditions: x(0) = 0, x'(0) = initial_velocity
            c1 = 1.0
            c2 = (zeta * w0 - config.initial_velocity) / wd
            val = 1.0 - decay * (c1 * math.cos(wd * t) + c2 * math.sin(wd * t))
            return val
        else:
            # Overdamped: Sluggish return without oscillation
            s1 = -w0 * (zeta - math.sqrt(max(1e-9, zeta * zeta - 1.0)))
            s2 = -w0 * (zeta + math.sqrt(max(1e-9, zeta * zeta - 1.0)))
            denom = s2 - s1
            c1 = (s2 + config.initial_velocity) / denom if abs(denom) > 1e-9 else 1.0
            c2 = 1.0 - c1
            return 1.0 - (c1 * math.exp(s1 * t) + c2 * math.exp(s2 * t))

    @classmethod
    def generate_keyframes(
        cls,
        config: SpringConfig,
        duration: float = 0.65,
        steps: int = 30
    ) -> List[Tuple[float, float]]:
        """Generates (percentage, value) keyframe pairs for CSS @keyframes."""
        keyframes = []
        for i in range(steps + 1):
            pct = (i / steps) * 100.0
            t = (i / steps) * duration
            val = cls.evaluate(config, t)
            keyframes.append((round(pct, 2), round(val, 4)))
        return keyframes

    @classmethod
    def generate_css_keyframes(
        cls,
        name: str,
        config: SpringConfig,
        property_template: str = "transform: scale({v})",
        duration: float = 0.65,
        steps: int = 25
    ) -> str:
        """
        Generates a complete CSS @keyframes block with exact physical spring values.
        property_template can use {v} for progress (0.0 to 1.0+) or {inv_v} for (1.0 - v).
        """
        frames = cls.generate_keyframes(config, duration=duration, steps=steps)
        lines = [f"@keyframes {name} {{"]
        for pct, val in frames:
            inv_val = round(1.0 - val, 4)
            prop = property_template.format(v=val, inv_v=inv_val)
            lines.append(f"  {pct:.1f}% {{ {prop}; }}")
        lines.append("}")
        return "\n".join(lines)

    @classmethod
    def generate_js_spring_runtime(cls) -> str:
        """Returns the client-side JavaScript spring evaluator injected into timeline.js."""
        return """
  // Analytical Damped Harmonic Oscillator Spring Physics Solver (bang-motion / Framer Motion pattern)
  function solveSpring(stiffness, damping, mass, t) {
    if (t <= 0.0) return 0.0;
    const m = Math.max(0.01, mass || 1.0);
    const k = Math.max(0.1, stiffness || 200.0);
    const c = Math.max(0.01, damping || 15.0);
    const w0 = Math.sqrt(k / m);
    const zeta = c / (2.0 * Math.sqrt(m * k));
    
    if (Math.abs(zeta - 1.0) < 0.005) {
      const decay = Math.exp(-w0 * t);
      return 1.0 - decay * (1.0 + w0 * t);
    } else if (zeta < 1.0) {
      const wd = w0 * Math.sqrt(Math.max(1e-7, 1.0 - zeta * zeta));
      const decay = Math.exp(-zeta * w0 * t);
      return 1.0 - decay * (Math.cos(wd * t) + (zeta * w0 / wd) * Math.sin(wd * t));
    } else {
      const s1 = -w0 * (zeta - Math.sqrt(Math.max(1e-7, zeta * zeta - 1.0)));
      const s2 = -w0 * (zeta + Math.sqrt(Math.max(1e-7, zeta * zeta - 1.0)));
      const c1 = s2 / (s2 - s1);
      return 1.0 - (c1 * Math.exp(s1 * t) + (1.0 - c1) * Math.exp(s2 * t));
    }
  }
  window.solveSpring = solveSpring;
"""
