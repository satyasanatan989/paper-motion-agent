"""
Food Code - Reusable Scientific Visual & Macro Cinematography Library.
Implements the official visual identity for FOOD CODE:
- Dark cinematic environments (#0C0A09, #171412)
- Burnt-orange highlights (#FF6B00, #E65100, #FF8C38)
- Warm-white typography (#F5EBE1, #FFF5EB)
- 3D/2.5D biological and food science vector graphics & procedural shaders.
"""

from dataclasses import dataclass
from typing import Dict, Any, List
import html

# Food Code Brand Color Palette
FOOD_CODE_THEME = {
    "bg_dark": "#0B0907",
    "bg_surface": "#161310",
    "bg_card": "rgba(28, 23, 19, 0.85)",
    "accent_burnt_orange": "#FF6B00",
    "accent_deep_orange": "#E65100",
    "accent_gold": "#FFA94D",
    "text_warm_white": "#F5EBE1",
    "text_muted": "#A89F91",
    "acid_green_yellow": "#CCFF00",
    "danger_crimson": "#FF3344",
    "vignette": "radial-gradient(circle at 50% 45%, rgba(255, 107, 0, 0.08) 0%, rgba(11, 9, 7, 0.96) 80%)"
}

class FoodScienceVisuals:
    """Reusable library of macro food science and biological anatomy SVGs."""

    @staticmethod
    def wheat_kernel_macro() -> str:
        """
        Macro wheat grain anatomical cross-section.
        Visualizes outer fibrous bran (brown), nutrient-dense germ (golden), and starchy endosperm core.
        """
        return """
        <svg class="food-code-asset macro-grain" viewBox="0 0 600 700" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="endospermGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
              <stop offset="70%" stop-color="#F5EBE1" stop-opacity="0.85"/>
              <stop offset="100%" stop-color="#D5C5B5" stop-opacity="0.7"/>
            </radialGradient>
            <linearGradient id="branShell" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#8C532B"/>
              <stop offset="50%" stop-color="#5E3013"/>
              <stop offset="100%" stop-color="#3D1D09"/>
            </linearGradient>
            <linearGradient id="germGold" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#FFA94D"/>
              <stop offset="100%" stop-color="#FF6B00"/>
            </linearGradient>
            <filter id="grainGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="8" result="blur"/>
              <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
          </defs>

          <!-- Outer Fibrous Bran Layer (Peeling outwards) -->
          <g class="bran-layer" style="transform-origin: 300px 350px;">
            <path d="M 300 60 C 440 60, 520 200, 510 400 C 500 560, 400 640, 300 650 C 200 640, 100 560, 90 400 C 80 200, 160 60, 300 60 Z"
                  fill="url(#branShell)" stroke="#FF6B00" stroke-width="2" stroke-opacity="0.6"/>
            <!-- Longitudinal Crease -->
            <path d="M 300 70 C 290 250, 290 450, 300 640" stroke="#261205" stroke-width="8" stroke-linecap="round"/>
          </g>

          <!-- Starchy Endosperm Core (Pure Amylose/Amylopectin) -->
          <g class="endosperm-core" filter="url(#grainGlow)">
            <ellipse cx="300" cy="330" rx="160" ry="210" fill="url(#endospermGlow)"/>
            <!-- Starch granules micro-dots -->
            <circle cx="260" cy="280" r="14" fill="#FFFFFF" opacity="0.8"/>
            <circle cx="330" cy="270" r="18" fill="#FFFFFF" opacity="0.8"/>
            <circle cx="280" cy="350" r="22" fill="#FFFFFF" opacity="0.8"/>
            <circle cx="340" cy="360" r="16" fill="#FFFFFF" opacity="0.8"/>
            <circle cx="300" cy="420" r="20" fill="#FFFFFF" opacity="0.8"/>
          </g>

          <!-- Embryonic Germ (Micro-nutrients & Vitamin E) -->
          <g class="germ-embryo" style="transform-origin: 300px 560px;">
            <path d="M 270 540 C 270 500, 330 500, 330 540 C 330 580, 300 600, 270 540 Z" fill="url(#germGold)"/>
            <text x="300" y="555" font-family="'Montserrat', sans-serif" font-size="11" font-weight="900" fill="#0B0907" text-anchor="middle">GERM</text>
          </g>

          <!-- Callout Badges -->
          <g class="label-bran">
            <line x1="120" y1="260" x2="50" y2="230" stroke="#FF6B00" stroke-width="2" stroke-dasharray="4 4"/>
            <rect x="10" y="210" width="75" height="26" rx="4" fill="#161310" stroke="#FF6B00" stroke-width="1.5"/>
            <text x="47" y="227" font-family="'Bebas Neue', sans-serif" font-size="14" fill="#F5EBE1" text-anchor="middle">BRAN 14%</text>
          </g>
          <g class="label-endosperm">
            <line x1="440" y1="330" x2="510" y2="310" stroke="#FF6B00" stroke-width="2" stroke-dasharray="4 4"/>
            <rect x="500" y="295" width="90" height="26" rx="4" fill="#161310" stroke="#FF6B00" stroke-width="1.5"/>
            <text x="545" y="312" font-family="'Bebas Neue', sans-serif" font-size="14" fill="#F5EBE1" text-anchor="middle">ENDOSPERM 83%</text>
          </g>
        </svg>
        """

    @staticmethod
    def gluten_matrix_macro() -> str:
        """
        Microscopic gluten-starch adhesive network.
        Illustrates hydrated glutenin & gliadin proteins forming an adhesive trap.
        """
        return """
        <svg class="food-code-asset macro-gluten" viewBox="0 0 700 700" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="starchPasteGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#FF6B00" stop-opacity="0.25"/>
              <stop offset="60%" stop-color="#161310" stop-opacity="0.85"/>
              <stop offset="100%" stop-color="#0B0907" stop-opacity="1.0"/>
            </radialGradient>
            <filter id="viscousBlur">
              <feGaussianBlur in="SourceGraphic" stdDeviation="5"/>
            </filter>
          </defs>

          <!-- Viscous Fluid Background -->
          <rect width="700" height="700" fill="url(#starchPasteGlow)"/>

          <!-- Intertwined Glutenin Fibers -->
          <g stroke="#D4A373" stroke-width="7" stroke-linecap="round" fill="none" opacity="0.85">
            <path d="M 80 140 Q 220 280, 360 200 T 620 320"/>
            <path d="M 120 480 Q 280 340, 440 460 T 640 400"/>
            <path d="M 220 80 Q 280 260, 240 480 T 380 620"/>
            <path d="M 460 100 Q 420 320, 520 490 T 480 640"/>
          </g>

          <!-- Cross-linking Gliadin Protein Knots -->
          <g fill="#FF6B00" stroke="#FFA94D" stroke-width="2">
            <circle cx="230" cy="250" r="16" class="pulse-node"/>
            <circle cx="360" cy="200" r="19" class="pulse-node"/>
            <circle cx="435" cy="330" r="22" class="pulse-node"/>
            <circle cx="275" cy="355" r="18" class="pulse-node"/>
            <circle cx="465" cy="480" r="17" class="pulse-node"/>
          </g>

          <!-- Trapped Starch Spheres (Adhered Granules) -->
          <g fill="#FFFFFF" opacity="0.9" stroke="#E65100" stroke-width="2">
            <circle cx="160" cy="380" r="26"/>
            <circle cx="340" cy="290" r="32"/>
            <circle cx="510" cy="240" r="28"/>
            <circle cx="390" cy="430" r="36"/>
            <circle cx="560" cy="460" r="24"/>
          </g>

          <text x="350" y="660" font-family="'Cinzel', serif" font-size="18" font-weight="700" fill="#FFA94D" letter-spacing="4" text-anchor="middle">VISCOUS GLUTEN-STARCH GEL</text>
        </svg>
        """

    @staticmethod
    def stomach_acid_reflux_macro() -> str:
        """
        3D Scientific Cross-Section: Gastric Mucosa, Boiling Acid Pool, and Reflux Surge.
        Demonstrates corrosive pH 1.5 acid overcoming Lower Esophageal Sphincter (LES).
        """
        return """
        <svg class="food-code-asset gastric-acid" viewBox="0 0 700 850" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="acidLumen" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#FF3344" stop-opacity="0.95"/>
              <stop offset="35%" stop-color="#FF6B00" stop-opacity="0.9"/>
              <stop offset="70%" stop-color="#CCFF00" stop-opacity="0.85"/>
              <stop offset="100%" stop-color="#88CC00" stop-opacity="0.9"/>
            </linearGradient>
            <linearGradient id="stomachWall" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#5C1D24"/>
              <stop offset="50%" stop-color="#3B1217"/>
              <stop offset="100%" stop-color="#1A080A"/>
            </linearGradient>
            <filter id="acidGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="12" result="blur"/>
              <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
          </defs>

          <!-- Stomach Muscular Organ Outer Silhouette -->
          <path d="M 350 40 
                   C 390 40, 420 120, 420 180 
                   C 520 220, 620 320, 620 480 
                   C 620 680, 480 780, 340 780 
                   C 180 780, 100 650, 100 480 
                   C 100 320, 240 240, 310 180 
                   C 310 120, 310 40, 350 40 Z"
                fill="url(#stomachWall)" stroke="#FF6B00" stroke-width="3" stroke-opacity="0.4"/>

          <!-- Corrosive Acid Liquid Pool (Animated Wave Level) -->
          <g filter="url(#acidGlow)">
            <path d="M 120 490 
                     Q 240 450, 360 490 
                     T 600 480 
                     L 590 660 
                     C 520 750, 400 760, 340 760 
                     C 220 760, 140 700, 130 640 Z"
                  fill="url(#acidLumen)"/>
            
            <!-- Rising Reflux Acid Plume into Esophagus -->
            <path d="M 330 460 C 330 320, 340 210, 345 70 C 355 70, 365 70, 375 70 C 380 210, 390 320, 390 460 Z"
                  fill="url(#acidLumen)" opacity="0.9"/>
          </g>

          <!-- Boiling HCl Bubbles -->
          <g fill="#FFFFEE" opacity="0.8">
            <circle cx="340" cy="530" r="12" class="bubble-float"/>
            <circle cx="420" cy="580" r="16" class="bubble-float"/>
            <circle cx="260" cy="560" r="10" class="bubble-float"/>
            <circle cx="480" cy="520" r="14" class="bubble-float"/>
            <circle cx="355" cy="260" r="8" class="bubble-float"/>
            <circle cx="365" cy="140" r="9" class="bubble-float"/>
          </g>

          <!-- Acid pH Warning Indicator -->
          <g transform="translate(180, 320)">
            <rect width="130" height="46" rx="6" fill="#161310" stroke="#FF3344" stroke-width="2"/>
            <text x="65" y="24" font-family="'Bebas Neue', sans-serif" font-size="20" fill="#FF3344" text-anchor="middle">ACIDITY: pH 1.5</text>
            <text x="65" y="38" font-family="'Montserrat', sans-serif" font-size="9" font-weight="700" fill="#F5EBE1" text-anchor="middle">SEVERE REFLUX</text>
          </g>

          <!-- Esophageal Valve Failure Tag -->
          <g transform="translate(410, 120)">
            <line x1="0" y1="20" x2="-45" y2="20" stroke="#FF6B00" stroke-width="2"/>
            <rect width="160" height="40" rx="4" fill="#0B0907" stroke="#FF6B00" stroke-width="1.5"/>
            <text x="80" y="25" font-family="'Bebas Neue', sans-serif" font-size="16" fill="#FF6B00" text-anchor="middle">LES SPHINCTER BREACH</text>
          </g>
        </svg>
        """

    @staticmethod
    def transit_clock_comparison() -> str:
        """
        Dual Antique/Scientific Mechanical Clocks:
        24 Hours (Whole Grain Peristalsis) vs 50+ Hours (Maida Gut Stagnation).
        """
        return """
        <svg class="food-code-asset transit-clock" viewBox="0 0 700 480" xmlns="http://www.w3.org/2000/svg">
          <!-- Whole Grain Clock (Left) -->
          <g transform="translate(80, 40)">
            <circle cx="110" cy="110" r="95" fill="#161310" stroke="#48BB78" stroke-width="4"/>
            <circle cx="110" cy="110" r="75" fill="none" stroke="#2D3748" stroke-dasharray="4 6"/>
            <!-- Clock Hands pointing to 24h cycle -->
            <line x1="110" y1="110" x2="110" y2="40" stroke="#48BB78" stroke-width="4" stroke-linecap="round"/>
            <line x1="110" y1="110" x2="155" y2="110" stroke="#48BB78" stroke-width="3" stroke-linecap="round"/>
            <circle cx="110" cy="110" r="6" fill="#48BB78"/>
            <!-- Badges -->
            <text x="110" y="250" font-family="'Bebas Neue', sans-serif" font-size="28" fill="#48BB78" text-anchor="middle">24 HOURS</text>
            <text x="110" y="275" font-family="'Montserrat', sans-serif" font-size="12" font-weight="700" fill="#F5EBE1" text-anchor="middle">WHOLE GRAIN FIBER</text>
            <text x="110" y="295" font-family="'Montserrat', sans-serif" font-size="11" fill="#A89F91" text-anchor="middle">Active Peristalsis</text>
          </g>

          <!-- Refined Starch Clock (Right) -->
          <g transform="translate(400, 40)">
            <circle cx="110" cy="110" r="95" fill="#161310" stroke="#FF6B00" stroke-width="4"/>
            <circle cx="110" cy="110" r="75" fill="none" stroke="#E65100" stroke-dasharray="4 6"/>
            <!-- Clock Hands indicating 50+ hours multi-rotation -->
            <line x1="110" y1="110" x2="160" y2="70" stroke="#FF6B00" stroke-width="4" stroke-linecap="round"/>
            <line x1="110" y1="110" x2="110" y2="165" stroke="#FF6B00" stroke-width="3" stroke-linecap="round"/>
            <circle cx="110" cy="110" r="6" fill="#FF6B00"/>
            <!-- Badges -->
            <text x="110" y="250" font-family="'Bebas Neue', sans-serif" font-size="28" fill="#FF6B00" text-anchor="middle">50+ HOURS</text>
            <text x="110" y="275" font-family="'Montserrat', sans-serif" font-size="12" font-weight="700" fill="#FF6B00" text-anchor="middle">REFINED MAIDA PASTE</text>
            <text x="110" y="295" font-family="'Montserrat', sans-serif" font-size="11" fill="#A89F91" text-anchor="middle">Intestinal Stagnation</text>
          </g>

          <!-- Central VS / Contrast Divider -->
          <line x1="350" y1="60" x2="350" y2="360" stroke="#FF6B00" stroke-width="2" stroke-opacity="0.3" stroke-dasharray="6 6"/>
          <circle cx="350" cy="200" r="24" fill="#0B0907" stroke="#FF6B00" stroke-width="2"/>
          <text x="350" y="206" font-family="'Cinzel', serif" font-size="16" font-weight="900" fill="#FFA94D" text-anchor="middle">VS</text>
        </svg>
        """

    @staticmethod
    def glucose_ring_molecule() -> str:
        """3D Scientific representation of cyclic D-Glucose molecule."""
        return """
        <svg class="food-code-asset molecule-glucose" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="carbonSphere" cx="35%" cy="35%" r="65%">
              <stop offset="0%" stop-color="#FFA94D"/>
              <stop offset="60%" stop-color="#FF6B00"/>
              <stop offset="100%" stop-color="#803500"/>
            </radialGradient>
            <radialGradient id="oxygenSphere" cx="35%" cy="35%" r="65%">
              <stop offset="0%" stop-color="#FF6B8B"/>
              <stop offset="60%" stop-color="#FF3344"/>
              <stop offset="100%" stop-color="#800010"/>
            </radialGradient>
          </defs>

          <!-- Hexagonal Ring Chemical Bonds -->
          <g stroke="#F5EBE1" stroke-width="5" stroke-linecap="round" opacity="0.8">
            <line x1="250" y1="100" x2="370" y2="170"/>
            <line x1="370" y1="170" x2="370" y2="310"/>
            <line x1="370" y1="310" x2="250" y2="380"/>
            <line x1="250" y1="380" x2="130" y2="310"/>
            <line x1="130" y1="310" x2="130" y2="170"/>
            <line x1="130" y1="170" x2="250" y2="100"/>
          </g>

          <!-- Ring Atoms (C1-C5 and Ring Oxygen) -->
          <circle cx="250" cy="100" r="22" fill="url(#oxygenSphere)"/>
          <circle cx="370" cy="170" r="24" fill="url(#carbonSphere)"/>
          <circle cx="370" cy="310" r="24" fill="url(#carbonSphere)"/>
          <circle cx="250" cy="380" r="24" fill="url(#carbonSphere)"/>
          <circle cx="130" cy="310" r="24" fill="url(#carbonSphere)"/>
          <circle cx="130" cy="170" r="24" fill="url(#carbonSphere)"/>

          <text x="250" y="440" font-family="'Cinzel', serif" font-size="16" font-weight="700" fill="#FFA94D" letter-spacing="3" text-anchor="middle">RAPID GLUCOSE SPIKE</text>
        </svg>
        """

    @staticmethod
    def get_food_code_css() -> str:
        """Global CSS rules matching the Food Code brand identity."""
        return f"""
        /* FOOD CODE — Official Cinematic Visual Theme */
        :root {{
          --fc-bg-dark: {FOOD_CODE_THEME['bg_dark']};
          --fc-bg-surface: {FOOD_CODE_THEME['bg_surface']};
          --fc-burnt-orange: {FOOD_CODE_THEME['accent_burnt_orange']};
          --fc-deep-orange: {FOOD_CODE_THEME['accent_deep_orange']};
          --fc-gold: {FOOD_CODE_THEME['accent_gold']};
          --fc-warm-white: {FOOD_CODE_THEME['text_warm_white']};
          --fc-muted: {FOOD_CODE_THEME['text_muted']};
        }}

        body {{
          background-color: var(--fc-bg-dark);
          color: var(--fc-warm-white);
          font-family: 'Montserrat', sans-serif;
        }}

        .brand-badge {{
          position: absolute;
          top: 70px;
          left: 50%;
          transform: translateX(-50%);
          display: flex;
          align-items: center;
          gap: 8px;
          background: rgba(22, 19, 16, 0.9);
          border: 1px solid var(--fc-burnt-orange);
          padding: 6px 18px;
          border-radius: 30px;
          box-shadow: 0 4px 20px rgba(255, 107, 0, 0.25);
          z-index: 100;
        }}
        .brand-badge .dot {{
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: var(--fc-burnt-orange);
          box-shadow: 0 0 10px var(--fc-burnt-orange);
        }}
        .brand-badge span {{
          font-family: 'Cinzel', serif;
          font-size: 14px;
          font-weight: 800;
          letter-spacing: 3px;
          color: var(--fc-warm-white);
        }}

        /* Headline & Typography Rules */
        .headline-main {{
          font-family: 'Bebas Neue', sans-serif;
          font-size: 54px;
          letter-spacing: 2px;
          color: var(--fc-warm-white);
          text-shadow: 0 4px 24px rgba(0, 0, 0, 0.9);
        }}
        .headline-sub {{
          font-family: 'Montserrat', sans-serif;
          font-size: 16px;
          font-weight: 800;
          letter-spacing: 4px;
          color: var(--fc-burnt-orange);
          margin-bottom: 8px;
        }}
        .highlight {{
          color: var(--fc-burnt-orange) !important;
          text-shadow: 0 0 14px rgba(255, 107, 0, 0.6);
        }}

        /* Macro Food Science Animations */
        .bubble-float {{
          animation: floatUp 2.8s infinite ease-in-out;
        }}
        @keyframes floatUp {{
          0% {{ transform: translateY(0); opacity: 0.2; }}
          50% {{ opacity: 0.9; }}
          100% {{ transform: translateY(-80px); opacity: 0; }}
        }}

        .pulse-node {{
          animation: nodePulse 1.8s infinite ease-in-out alternate;
        }}
        @keyframes nodePulse {{
          0% {{ transform: scale(1); opacity: 0.7; }}
          100% {{ transform: scale(1.2); opacity: 1; filter: drop-shadow(0 0 8px var(--fc-burnt-orange)); }}
        }}
        """
