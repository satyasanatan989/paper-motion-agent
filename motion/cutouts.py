"""
Vector Paper-Cutout SVG Assets with Tactile Drop Shadows.
Includes historical warriors, clashing blades, blooming lotus, chakras, and tech nodes.
"""

import math

class CutoutLibrary:
    """Library of procedural papercraft SVG cutouts for high-retention explainers."""

    @staticmethod
    def sword_clash(id_prefix: str = "s2") -> str:
        """Returns SVG snippet for two clashing swords with impact spark particles."""
        return f"""
        <svg width="800" height="460" viewBox="0 0 800 460" style="filter: var(--paper-cutout); margin-top: 10px;">
          <!-- Sword Left -->
          <g id="{id_prefix}-sword-l" transform="translate(400, 230) rotate(-45)">
            <rect x="-14" y="-180" width="28" height="260" rx="4" fill="#E2E8F0" stroke="#2D3748" stroke-width="4"/>
            <path d="M -14 -180 L 0 -220 L 14 -180 Z" fill="#E2E8F0" stroke="#2D3748" stroke-width="4"/>
            <line x1="0" y1="-180" x2="0" y2="70" stroke="#CBD5E0" stroke-width="3"/>
            <rect x="-40" y="70" width="80" height="16" rx="6" fill="#D4AF37" stroke="#744210" stroke-width="3"/>
            <rect x="-10" y="86" width="20" height="50" rx="4" fill="#9B111E"/>
          </g>

          <!-- Sword Right -->
          <g id="{id_prefix}-sword-r" transform="translate(400, 230) rotate(45)">
            <rect x="-14" y="-180" width="28" height="260" rx="4" fill="#E2E8F0" stroke="#2D3748" stroke-width="4"/>
            <path d="M -14 -180 L 0 -220 L 14 -180 Z" fill="#E2E8F0" stroke="#2D3748" stroke-width="4"/>
            <line x1="0" y1="-180" x2="0" y2="70" stroke="#CBD5E0" stroke-width="3"/>
            <rect x="-40" y="70" width="80" height="16" rx="6" fill="#D4AF37" stroke="#744210" stroke-width="3"/>
            <rect x="-10" y="86" width="20" height="50" rx="4" fill="#9B111E"/>
          </g>

          <!-- Sparks -->
          <g id="{id_prefix}-sparks">
            <circle cx="400" cy="230" r="14" fill="#FFD700" filter="drop-shadow(0 0 16px #FF8C00)"/>
            <line x1="400" y1="230" x2="350" y2="180" stroke="#FFD700" stroke-width="4"/>
            <line x1="400" y1="230" x2="450" y2="170" stroke="#FF8C00" stroke-width="4"/>
            <line x1="400" y1="230" x2="420" y2="290" stroke="#FFD700" stroke-width="4"/>
          </g>
        </svg>
        """

    @staticmethod
    def ashoka_chakra(cx: int = 310, cy: int = 310, r: int = 270, id_str: str = "s5-chakra") -> str:
        """Mathematically generates the 24-spoke Ashoka Chakra (15 deg intervals)."""
        spokes = []
        for i in range(24):
            angle_rad = math.radians(i * 15)
            x2 = cx + r * math.cos(angle_rad)
            y2 = cy + r * math.sin(angle_rad)
            spokes.append(f'<line x1="{cx}" y1="{cy}" x2="{int(x2)}" y2="{int(y2)}"/>')

        spokes_svg = "\n".join(spokes)
        return f"""
        <svg id="{id_str}" width="{cx*2}" height="{cy*2}" viewBox="0 0 {cx*2} {cy*2}" style="filter: var(--paper-cutout); transform-origin: center center;">
          <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#002244" stroke-width="20"/>
          <circle cx="{cx}" cy="{cy}" r="50" fill="#002244"/>
          <circle cx="{cx}" cy="{cy}" r="24" fill="#FFFDF7"/>
          <g stroke="#002244" stroke-width="8" stroke-linecap="round">
            {spokes_svg}
          </g>
        </svg>
        """

    @staticmethod
    def blooming_lotus(id_str: str = "s3-lotus") -> str:
        """Papercraft blooming golden lotus flower."""
        return f"""
        <g id="{id_str}" transform="translate(390, 430)">
          <ellipse cx="0" cy="-60" rx="28" ry="46" fill="#D4AF37" stroke="#B7791F" stroke-width="3"/>
          <path d="M 0 -20 C -60 -40 -90 -90 -60 -130 C -40 -80 0 -50 0 -20 Z" fill="#F6E05E" stroke="#D69E2E" stroke-width="3"/>
          <path d="M 0 -20 C 60 -40 90 -90 60 -130 C 40 -80 0 -50 0 -20 Z" fill="#F6E05E" stroke="#D69E2E" stroke-width="3"/>
          <path d="M 0 -10 C -90 -20 -130 -60 -100 -100 C -70 -50 0 -30 0 -10 Z" fill="#ECC94B" stroke="#D69E2E" stroke-width="3"/>
          <path d="M 0 -10 C 90 -20 130 -60 100 -100 C 70 -50 0 -30 0 -10 Z" fill="#ECC94B" stroke="#D69E2E" stroke-width="3"/>
        </g>
        """
