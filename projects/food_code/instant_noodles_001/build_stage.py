"""
Build Web Stage for Food Code Episode 001: Instant Noodles.
Generates index.html, style.css, and timeline.js into projects/food_code/instant_noodles_001/stage/
"""

import json
from pathlib import Path

out_dir = Path(__file__).parent
stage_dir = out_dir / "stage"
stage_dir.mkdir(parents=True, exist_ok=True)

with open(out_dir / "storyboard.json", encoding="utf-8") as f:
    sb = json.load(f)

scenes = sb["scenes"]
total_dur = sb["estimated_duration"]

# Calculate scene start and end times
curr_time = 0.0
scene_bounds = []
for sc in scenes:
    start_t = curr_time
    end_t = curr_time + sc["duration"]
    scene_bounds.append({
        "id": sc["scene_id"],
        "title": sc["title"],
        "start": round(start_t, 2),
        "end": round(end_t, 2),
        "duration": sc["duration"],
        "camera": sc["camera"]
    })
    curr_time = end_t

# --- 1. Generate index.html ---
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
  <title>Food Code 001 - What Happens When You Eat Instant Noodles?</title>
  <link rel="stylesheet" href="style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cinzel:wght@700;900&family=Montserrat:wght@400;600;800;900&family=JetBrains+Mono:wght@700;800&display=swap" rel="stylesheet">
</head>
<body>
  <div id="viewport">
    <!-- Global Brand Badge -->
    <div class="brand-badge">
      <div class="brand-dot"></div>
      <span class="brand-title">FOOD CODE</span>
      <span class="brand-code">EP 001</span>
    </div>

    <!-- Vignette & Cinematic Overlay -->
    <div class="cinematic-vignette"></div>
    <div class="ambient-glow"></div>

    <!-- Active Scene Stages -->
"""

# Scene-specific SVG vectors and HTML contents
def get_scene_visual_html(scene_id: str) -> str:
    if scene_id == "scene_001":
        # Boiling Pot & Instant Noodle Block
        return """
        <svg class="fc-visual scene1-noodles" viewBox="0 0 800 900" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="brothGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#FF6B00" stop-opacity="0.8"/>
              <stop offset="60%" stop-color="#8B3524" stop-opacity="0.6"/>
              <stop offset="100%" stop-color="#111111" stop-opacity="0.95"/>
            </radialGradient>
            <filter id="noodleGlow">
              <feGaussianBlur stdDeviation="6" result="blur"/>
              <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
          </defs>
          <!-- Boiling Pot Silhouette -->
          <ellipse cx="400" cy="550" rx="340" ry="240" fill="url(#brothGlow)" stroke="#F28C28" stroke-width="4"/>
          <ellipse cx="400" cy="520" rx="290" ry="190" fill="#22140A" stroke="#FF6B00" stroke-width="2"/>
          <!-- Boiling Bubbles -->
          <circle cx="320" cy="480" r="14" fill="#FFA94D" opacity="0.8" class="bubble-anim"/>
          <circle cx="460" cy="530" r="20" fill="#FFA94D" opacity="0.8" class="bubble-anim"/>
          <circle cx="380" cy="570" r="16" fill="#FFA94D" opacity="0.8" class="bubble-anim"/>
          <circle cx="490" cy="460" r="12" fill="#FFA94D" opacity="0.8" class="bubble-anim"/>
          <!-- Wavy Instant Ramen Block Descending -->
          <g id="noodle-block" class="noodle-falling" filter="url(#noodleGlow)">
            <rect x="230" y="240" width="340" height="230" rx="24" fill="#F4D06F" stroke="#E09F3E" stroke-width="5"/>
            <!-- Wavy Noodle Strands Texture -->
            <path d="M 250 270 Q 280 250, 310 270 T 370 270 T 430 270 T 490 270 T 550 270" fill="none" stroke="#D48B28" stroke-width="6"/>
            <path d="M 250 310 Q 280 290, 310 310 T 370 310 T 430 310 T 490 310 T 550 310" fill="none" stroke="#D48B28" stroke-width="6"/>
            <path d="M 250 350 Q 280 330, 310 350 T 370 350 T 430 350 T 490 350 T 550 350" fill="none" stroke="#D48B28" stroke-width="6"/>
            <path d="M 250 390 Q 280 370, 310 390 T 370 390 T 430 390 T 490 390 T 550 390" fill="none" stroke="#D48B28" stroke-width="6"/>
            <path d="M 250 430 Q 280 410, 310 430 T 370 430 T 430 430 T 490 430 T 550 430" fill="none" stroke="#D48B28" stroke-width="6"/>
          </g>
          <!-- Splash Flare -->
          <circle cx="400" cy="520" r="110" fill="none" stroke="#F28C28" stroke-width="4" stroke-dasharray="12 8" opacity="0.75" class="ripple-anim"/>
        </svg>
        """
    elif scene_id == "scene_002":
        # Oral Cavity, Mastication, Salivary Amylase Cleavage
        return """
        <svg class="fc-visual scene2-mouth" viewBox="0 0 800 850" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="oralGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#5C1D24"/>
              <stop offset="100%" stop-color="#111111"/>
            </linearGradient>
          </defs>
          <!-- Oral Cavity Anatomy Backdrop -->
          <path d="M 150 180 C 250 100, 550 100, 650 180 C 700 320, 700 580, 650 680 C 520 740, 280 740, 150 680 C 100 560, 100 320, 150 180 Z"
                fill="url(#oralGrad)" stroke="#8B3524" stroke-width="3"/>
          <!-- Food Bolus Mixing -->
          <g transform="translate(400, 420)" id="food-bolus">
            <circle cx="0" cy="0" r="95" fill="#E8C374" opacity="0.9" stroke="#F28C28" stroke-width="4"/>
            <!-- Saliva Fluid Droplets -->
            <ellipse cx="-45" cy="-25" rx="18" ry="12" fill="#FFFFFF" opacity="0.75"/>
            <ellipse cx="35" cy="40" rx="16" ry="10" fill="#FFFFFF" opacity="0.75"/>
          </g>
          <!-- Starch Chain & Amylase Cleavage Inset -->
          <g transform="translate(180, 580)" id="starch-inset">
            <rect width="440" height="150" rx="16" fill="#161310" stroke="#F28C28" stroke-width="2.5"/>
            <text x="220" y="32" font-family="'Montserrat', sans-serif" font-size="14" font-weight="800" fill="#F28C28" text-anchor="middle" letter-spacing="2">SALIVARY ALPHA-AMYLASE INSET</text>
            <!-- Glucose Units Connected in Amylose Polymer Chain -->
            <circle cx="90" cy="95" r="22" fill="#FFA94D" stroke="#FFFFFF" stroke-width="2"/>
            <line x1="112" y1="95" x2="158" y2="95" stroke="#F5F0E8" stroke-width="4"/>
            <circle cx="180" cy="95" r="22" fill="#FFA94D" stroke="#FFFFFF" stroke-width="2"/>
            <!-- Cleavage Scissors / Scissor Icon / Arrow -->
            <text x="225" y="85" font-family="'Cinzel', serif" font-size="28" fill="#FF3344" text-anchor="middle">✂</text>
            <line x1="245" y1="95" x2="285" y2="95" stroke="#F5F0E8" stroke-width="4" stroke-dasharray="4 4"/>
            <circle cx="310" cy="95" r="22" fill="#FFA94D" stroke="#FFFFFF" stroke-width="2"/>
            <line x1="332" y1="95" x2="378" y2="95" stroke="#F5F0E8" stroke-width="4"/>
            <circle cx="400" cy="95" r="22" fill="#FFA94D" stroke="#FFFFFF" stroke-width="2"/>
          </g>
        </svg>
        """
    elif scene_id == "scene_003":
        # Stomach Peristaltic Churn & Gastric Juices
        return """
        <svg class="fc-visual scene3-stomach" viewBox="0 0 800 850" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="stomachMuscles" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#4A151B"/>
              <stop offset="50%" stop-color="#2D0B0F"/>
              <stop offset="100%" stop-color="#140507"/>
            </linearGradient>
            <radialGradient id="chymeFluid" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#F28C28" stop-opacity="0.85"/>
              <stop offset="70%" stop-color="#8B3524" stop-opacity="0.7"/>
              <stop offset="100%" stop-color="#111111" stop-opacity="0.9"/>
            </radialGradient>
          </defs>
          <!-- Stomach Organ Outer Silhouette -->
          <g id="stomach-contour" class="peristalsis-churn">
            <path d="M 400 60 C 440 60, 480 140, 480 200 C 600 240, 700 360, 700 520 C 700 720, 540 800, 390 800 C 220 800, 120 680, 120 500 C 120 340, 260 250, 340 190 C 340 130, 340 60, 400 60 Z"
                  fill="url(#stomachMuscles)" stroke="#F28C28" stroke-width="3" stroke-opacity="0.6"/>
            <!-- Rugal Folds -->
            <path d="M 220 420 Q 280 500, 340 430 T 480 470" fill="none" stroke="#8B3524" stroke-width="6" opacity="0.65"/>
            <path d="M 200 520 Q 300 620, 400 540 T 560 580" fill="none" stroke="#8B3524" stroke-width="6" opacity="0.65"/>
            <!-- Active Chyme Mixing Pool -->
            <ellipse cx="400" cy="620" rx="200" ry="120" fill="url(#chymeFluid)"/>
            <circle cx="340" cy="590" r="14" fill="#FFFFEE" opacity="0.8" class="bubble-anim"/>
            <circle cx="450" cy="630" r="18" fill="#FFFFEE" opacity="0.8" class="bubble-anim"/>
          </g>
          <!-- Badge Tag -->
          <g transform="translate(140, 180)">
            <rect width="180" height="42" rx="6" fill="#161310" stroke="#F28C28" stroke-width="2"/>
            <text x="90" y="26" font-family="'Bebas Neue', sans-serif" font-size="20" fill="#F5F0E8" text-anchor="middle">GASTRIC PERISTALSIS</text>
          </g>
        </svg>
        """
    elif scene_id == "scene_004":
        # Small Intestine, Duodenal Amylase, Sugar Cleavage
        return """
        <svg class="fc-visual scene4-enzymes" viewBox="0 0 800 850" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="enzymeGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#F28C28" stop-opacity="0.9"/>
              <stop offset="100%" stop-color="#8B3524" stop-opacity="0.1"/>
            </radialGradient>
          </defs>
          <!-- Duodenal Lumen Backdrop -->
          <rect width="800" height="850" fill="#111111"/>
          <!-- Intestinal Villi Micro Carpet along Borders -->
          <g fill="#2D0F14" stroke="#8B3524" stroke-width="2">
            <path d="M 0 100 Q 40 80, 80 100 T 160 100 T 240 100 T 320 100 T 400 100 T 480 100 T 560 100 T 640 100 T 720 100 T 800 100 L 800 0 L 0 0 Z"/>
            <path d="M 0 750 Q 40 770, 80 750 T 160 750 T 240 750 T 320 750 T 400 750 T 480 750 T 560 750 T 640 750 T 720 750 T 800 750 L 800 850 L 0 850 Z"/>
          </g>
          <!-- Pancreatic Amylase Catalytic Machine -->
          <g transform="translate(400, 360)" id="pancreatic-enzyme">
            <circle cx="0" cy="0" r="110" fill="url(#enzymeGlow)" stroke="#F28C28" stroke-width="3"/>
            <text x="0" y="5" font-family="'Cinzel', serif" font-size="16" font-weight="900" fill="#F5F0E8" text-anchor="middle" letter-spacing="3">PANCREATIC AMYLASE</text>
            <text x="0" y="28" font-family="'Montserrat', sans-serif" font-size="11" font-weight="700" fill="#FFA94D" text-anchor="middle">ENZYME CATALYSIS</text>
          </g>
          <!-- Cleaved Sugar Units Radiating Outward -->
          <g transform="translate(180, 520)" class="sugar-unit">
            <polygon points="40,0 80,25 80,65 40,90 0,65 0,25" fill="#FFA94D" stroke="#FFFFFF" stroke-width="2"/>
            <text x="40" y="50" font-family="'Bebas Neue', sans-serif" font-size="18" fill="#111111" text-anchor="middle">GLUCOSE</text>
          </g>
          <g transform="translate(540, 520)" class="sugar-unit">
            <polygon points="40,0 80,25 80,65 40,90 0,65 0,25" fill="#FFA94D" stroke="#FFFFFF" stroke-width="2"/>
            <text x="40" y="50" font-family="'Bebas Neue', sans-serif" font-size="18" fill="#111111" text-anchor="middle">MALTOSE</text>
          </g>
          <g transform="translate(360, 590)" class="sugar-unit">
            <polygon points="40,0 80,25 80,65 40,90 0,65 0,25" fill="#FFA94D" stroke="#FFFFFF" stroke-width="2"/>
            <text x="40" y="50" font-family="'Bebas Neue', sans-serif" font-size="18" fill="#111111" text-anchor="middle">GLUCOSE</text>
          </g>
        </svg>
        """
    elif scene_id == "scene_005":
        # Nutrient Absorption into Bloodstream
        return """
        <svg class="fc-visual scene5-bloodstream" viewBox="0 0 800 850" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="capillaryGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#8B3524"/>
              <stop offset="50%" stop-color="#B83A2A"/>
              <stop offset="100%" stop-color="#4A141A"/>
            </linearGradient>
          </defs>
          <!-- Enterocyte Epithelial Border -->
          <g transform="translate(0, 140)">
            <rect width="800" height="110" fill="#36171B" stroke="#F28C28" stroke-width="2"/>
            <text x="400" y="65" font-family="'Montserrat', sans-serif" font-size="15" font-weight="800" fill="#F5F0E8" text-anchor="middle" letter-spacing="4">INTESTINAL EPITHELIAL BARRIER</text>
          </g>
          <!-- Capillary Blood Vessel Tube -->
          <g transform="translate(0, 340)">
            <rect width="800" height="380" fill="url(#capillaryGrad)" stroke="#FF6B00" stroke-width="3"/>
            <!-- Pulsing Red Blood Cells Flowing -->
            <g class="blood-flow-left">
              <ellipse cx="120" cy="120" rx="36" ry="24" fill="#E63946" stroke="#800E13" stroke-width="3"/>
              <ellipse cx="280" cy="220" rx="42" ry="28" fill="#E63946" stroke="#800E13" stroke-width="3"/>
              <ellipse cx="440" cy="140" rx="38" ry="26" fill="#E63946" stroke="#800E13" stroke-width="3"/>
              <ellipse cx="620" cy="240" rx="40" ry="26" fill="#E63946" stroke="#800E13" stroke-width="3"/>
              <ellipse cx="740" cy="130" rx="35" ry="24" fill="#E63946" stroke="#800E13" stroke-width="3"/>
            </g>
            <!-- Absorbed Glowing Glucose Molecules Entering -->
            <g class="glucose-transport">
              <circle cx="200" cy="60" r="16" fill="#FFA94D" stroke="#FFFFFF" stroke-width="2"/>
              <circle cx="360" cy="80" r="16" fill="#FFA94D" stroke="#FFFFFF" stroke-width="2"/>
              <circle cx="520" cy="50" r="16" fill="#FFA94D" stroke="#FFFFFF" stroke-width="2"/>
            </g>
          </g>
          <!-- Destination Tags -->
          <g transform="translate(400, 770)">
            <rect x="-170" y="0" width="340" height="42" rx="6" fill="#161310" stroke="#F28C28" stroke-width="2"/>
            <text x="0" y="27" font-family="'Bebas Neue', sans-serif" font-size="22" fill="#FFA94D" text-anchor="middle">CELLULAR ENERGY & GLYCOGEN</text>
          </g>
        </svg>
        """
    elif scene_id == "scene_006":
        # The Sodium Factor & Nutrition Label Infographic
        return """
        <svg class="fc-visual scene6-sodium" viewBox="0 0 800 850" xmlns="http://www.w3.org/2000/svg">
          <!-- Background Blueprint Grid -->
          <rect width="800" height="850" fill="#111111"/>
          <!-- Generic Technical Nutrition Facts Panel (Accurate, non-fabricated) -->
          <g transform="translate(180, 160)">
            <rect width="440" height="580" rx="14" fill="#161310" stroke="#F5F0E8" stroke-width="3"/>
            <!-- Header -->
            <rect width="440" height="70" rx="14" fill="#F5F0E8"/>
            <text x="220" y="46" font-family="'Bebas Neue', sans-serif" font-size="38" fill="#111111" text-anchor="middle" letter-spacing="2">NUTRITION FACTS</text>
            <!-- Label Rows -->
            <line x1="20" y1="120" x2="420" y2="120" stroke="#444" stroke-width="2"/>
            <text x="30" y="110" font-family="'Montserrat', sans-serif" font-size="16" font-weight="700" fill="#F5F0E8">Serving Size</text>
            <text x="410" y="110" font-family="'Montserrat', sans-serif" font-size="16" fill="#A89F91" text-anchor="end">1 Packet (Prepared)</text>

            <line x1="20" y1="180" x2="420" y2="180" stroke="#444" stroke-width="2"/>
            <text x="30" y="165" font-family="'Montserrat', sans-serif" font-size="18" font-weight="800" fill="#F5F0E8">Carbohydrates</text>
            <text x="410" y="165" font-family="'Montserrat', sans-serif" font-size="18" fill="#F5F0E8" text-anchor="end">Wheat Starch</text>

            <!-- SODIUM ROW - BURNT ORANGE EMPHASIS CALLOUT -->
            <rect x="15" y="210" width="410" height="85" rx="8" fill="#2E170A" stroke="#F28C28" stroke-width="3"/>
            <text x="30" y="250" font-family="'Bebas Neue', sans-serif" font-size="34" fill="#F28C28">SODIUM (SALT)</text>
            <text x="30" y="278" font-family="'Montserrat', sans-serif" font-size="12" font-weight="800" fill="#FFA94D">VARIES BY FLAVOUR & BRAND</text>
            <circle cx="390" cy="252" r="18" fill="#F28C28"/>
            <text x="390" y="259" font-family="'Bebas Neue', sans-serif" font-size="22" fill="#111111" text-anchor="middle">!</text>

            <line x1="20" y1="330" x2="420" y2="330" stroke="#444" stroke-width="2"/>
            <text x="30" y="320" font-family="'Montserrat', sans-serif" font-size="16" fill="#F5F0E8">Dietary Fiber</text>
            <text x="410" y="320" font-family="'Montserrat', sans-serif" font-size="16" fill="#F28C28" text-anchor="end">Minimal (Refined)</text>

            <line x1="20" y1="380" x2="420" y2="380" stroke="#444" stroke-width="2"/>
            <text x="30" y="370" font-family="'Montserrat', sans-serif" font-size="16" fill="#F5F0E8">Protein</text>
            <text x="410" y="370" font-family="'Montserrat', sans-serif" font-size="16" fill="#A89F91" text-anchor="end">Low (Endosperm)</text>

            <!-- Advice Card -->
            <rect x="25" y="440" width="390" height="100" rx="8" fill="#0B0907" stroke="#F28C28" stroke-width="1.5"/>
            <text x="220" y="475" font-family="'Montserrat', sans-serif" font-size="14" font-weight="800" fill="#F5F0E8" text-anchor="middle">ALWAYS CHECK PACKET LABEL</text>
            <text x="220" y="505" font-family="'Montserrat', sans-serif" font-size="12" fill="#FFA94D" text-anchor="middle">Do not ingest whole seasoning sachet if monitoring salt</text>
          </g>
        </svg>
        """
    elif scene_id == "scene_007":
        # A More Balanced Bowl (Toppings Entering)
        return """
        <svg class="fc-visual scene7-balanced" viewBox="0 0 800 850" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="bowlCeramic" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#3A322C"/>
              <stop offset="85%" stop-color="#1E1915"/>
              <stop offset="100%" stop-color="#0E0C0A"/>
            </radialGradient>
          </defs>
          <!-- Ceramic Ramen Bowl -->
          <ellipse cx="400" cy="560" rx="340" ry="240" fill="url(#bowlCeramic)" stroke="#F28C28" stroke-width="4"/>
          <!-- Steaming Golden Broth -->
          <ellipse cx="400" cy="530" rx="280" ry="180" fill="#7A3F16" stroke="#D48B28" stroke-width="2"/>
          <!-- Cooked Ramen Noodle Strands -->
          <g stroke="#F4D06F" stroke-width="5" fill="none">
            <path d="M 240 500 Q 300 460, 380 500 T 500 480"/>
            <path d="M 280 540 Q 360 510, 440 550 T 560 520"/>
            <path d="M 220 520 Q 320 580, 420 520 T 540 560"/>
          </g>
          <!-- Descending Balanced Toppings (Animation Class) -->
          <!-- 1. Protein: Half Soft-Boiled Egg -->
          <g transform="translate(480, 430)" class="topping-drop">
            <ellipse cx="50" cy="65" rx="50" ry="65" fill="#F5F0E8" stroke="#E0D6C8" stroke-width="2"/>
            <circle cx="50" cy="70" r="30" fill="#F28C28"/>
            <circle cx="45" cy="65" r="8" fill="#FFA94D"/>
          </g>
          <!-- 2. Fiber & Micronutrients: Fresh Bok Choy Greens -->
          <g transform="translate(220, 420)" class="topping-drop">
            <path d="M 30 100 C 10 50, 40 10, 80 0 C 100 40, 110 80, 80 120 Z" fill="#2D6A4F" stroke="#40916C" stroke-width="2"/>
            <path d="M 60 110 C 50 60, 80 20, 120 10 C 140 50, 140 90, 110 130 Z" fill="#40916C" stroke="#52B788" stroke-width="2"/>
          </g>
          <!-- 3. Sliced Carrot Strips -->
          <g transform="translate(360, 420)" class="topping-drop">
            <rect x="0" y="0" width="12" height="60" rx="3" fill="#E85D04" transform="rotate(25)"/>
            <rect x="25" y="10" width="12" height="55" rx="3" fill="#E85D04" transform="rotate(40)"/>
          </g>
          <!-- Balancing Formula Badge -->
          <g transform="translate(200, 240)">
            <rect width="400" height="46" rx="23" fill="#161310" stroke="#48BB78" stroke-width="2"/>
            <text x="200" y="29" font-family="'Montserrat', sans-serif" font-size="14" font-weight="800" fill="#F5F0E8" text-anchor="middle" letter-spacing="2">NOODLES + VEGETABLES + PROTEIN</text>
          </g>
        </svg>
        """
    else: # scene_008: Final Takeaway & Food Code Brand Ending
        return """
        <svg class="fc-visual scene8-verdict" viewBox="0 0 800 850" xmlns="http://www.w3.org/2000/svg">
          <!-- Hero Bowl Centerpiece -->
          <g transform="translate(400, 460)">
            <ellipse cx="0" cy="50" rx="280" ry="160" fill="#1C1713" stroke="#F28C28" stroke-width="4"/>
            <ellipse cx="0" cy="30" rx="230" ry="120" fill="#7A3F16"/>
            <!-- Soft Egg & Greens in hero position -->
            <ellipse cx="50" cy="20" rx="40" ry="50" fill="#F5F0E8"/>
            <circle cx="50" cy="25" r="22" fill="#F28C28"/>
            <path d="M -80 0 C -100 -30, -60 -50, -40 -30 Z" fill="#2D6A4F"/>
          </g>
          <!-- Food Code Official Brand Seal -->
          <g transform="translate(400, 240)" id="food-code-seal">
            <circle cx="0" cy="0" r="95" fill="#111111" stroke="#F28C28" stroke-width="4"/>
            <circle cx="0" cy="0" r="80" fill="none" stroke="#FFA94D" stroke-dasharray="6 4" stroke-width="2"/>
            <!-- Brand Monogram -->
            <text x="0" y="-10" font-family="'Cinzel', serif" font-size="28" font-weight="900" fill="#F5F0E8" text-anchor="middle" letter-spacing="4">FOOD</text>
            <text x="0" y="25" font-family="'Cinzel', serif" font-size="28" font-weight="900" fill="#F28C28" text-anchor="middle" letter-spacing="4">CODE</text>
            <circle cx="0" cy="45" r="6" fill="#F28C28"/>
          </g>
          <text x="400" y="740" font-family="'Cinzel', serif" font-size="18" font-weight="700" fill="#FFA94D" text-anchor="middle" letter-spacing="5">FOOD KO FEAR SE NAHI, SCIENCE SE SAMJHO</text>
        </svg>
        """

for i, sc in enumerate(scenes):
    s_id = sc["scene_id"]
    title = sc["title"]
    headline = sc["typography"]["headline_main"]
    sub = sc["typography"]["headline_sub"]
    visual_svg = get_scene_visual_html(s_id)
    
    html_content += f"""
    <!-- Scene {i+1}: {title} -->
    <div class="scene-container" id="{s_id}" data-scene-idx="{i}">
      <!-- Background Parallax Layer -->
      <div class="layer layer-bg" id="{s_id}_bg">
        <div class="dark-texture"></div>
      </div>

      <!-- Midground Action Layer -->
      <div class="layer layer-mid" id="{s_id}_mid">
        <div class="visual-stage" id="{s_id}_stage">
          {visual_svg}
        </div>
      </div>

      <!-- Foreground Particle Layer -->
      <div class="layer layer-fg" id="{s_id}_fg">
        <div class="particle-field" id="{s_id}_particles"></div>
      </div>

      <!-- Overlay Typographic Layer -->
      <div class="layer layer-overlay">
        <div class="headline-box">
          <div class="headline-sub">{sub}</div>
          <div class="headline-main">{headline}</div>
        </div>
        <div class="caption-box" id="{s_id}_caption">
          <div class="caption-text">{sc['narration']}</div>
        </div>
      </div>
    </div>
"""

html_content += """
  </div>
  <script src="timeline.js"></script>
</body>
</html>
"""

with open(stage_dir / "index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Stage index.html written successfully!")

# --- 2. Generate style.css ---
css_content = """
/* FOOD CODE Episode 001 - Cinematic Visual Stylesheet */
:root {
  --fc-black: #111111;
  --fc-surface: #1A1714;
  --fc-orange: #F28C28;
  --fc-gold: #FFA94D;
  --fc-white: #F5F0E8;
  --fc-red: #8B3524;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 1080px;
  height: 1920px;
  background-color: var(--fc-black);
  color: var(--fc-white);
  overflow: hidden;
  font-family: 'Montserrat', sans-serif;
  user-select: none;
}

#viewport {
  position: relative;
  width: 1080px;
  height: 1920px;
  background-color: var(--fc-black);
  perspective: 1200px;
  overflow: hidden;
}

/* Global Brand Badge */
.brand-badge {
  position: absolute;
  top: 90px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(22, 19, 16, 0.92);
  border: 1.5px solid var(--fc-orange);
  padding: 10px 24px;
  border-radius: 40px;
  box-shadow: 0 4px 30px rgba(242, 140, 40, 0.3);
  z-index: 1000;
}
.brand-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--fc-orange);
  box-shadow: 0 0 12px var(--fc-orange);
}
.brand-title {
  font-family: 'Cinzel', serif;
  font-size: 16px;
  font-weight: 900;
  letter-spacing: 4px;
  color: var(--fc-white);
}
.brand-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  color: var(--fc-orange);
  background: rgba(242, 140, 40, 0.15);
  padding: 2px 8px;
  border-radius: 4px;
}

/* Cinematic Atmospheric Overlays */
.cinematic-vignette {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, transparent 40%, rgba(17, 17, 17, 0.95) 95%);
  pointer-events: none;
  z-index: 900;
}

.ambient-glow {
  position: absolute;
  top: 35%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 900px;
  height: 900px;
  background: radial-gradient(circle, rgba(242, 140, 40, 0.08) 0%, transparent 70%);
  pointer-events: none;
  z-index: 50;
}

/* Scene Container */
.scene-container {
  position: absolute;
  inset: 0;
  display: none;
  transform-style: preserve-3d;
}

.scene-container.active {
  display: block;
}

/* 2.5D Parallax Layers */
.layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.layer-bg {
  z-index: 10;
  transform: translateZ(-200px);
}

.layer-mid {
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: translateZ(0);
}

.layer-fg {
  z-index: 100;
  transform: translateZ(150px);
}

.layer-overlay {
  z-index: 800;
  pointer-events: auto;
}

/* Visual Stage Assets */
.visual-stage {
  width: 900px;
  height: 950px;
  margin-top: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fc-visual {
  width: 100%;
  height: 100%;
}

/* Typographic Hierarchy */
.headline-box {
  position: absolute;
  top: 240px;
  left: 80px;
  right: 80px;
  text-align: center;
}

.headline-sub {
  font-family: 'Montserrat', sans-serif;
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 4px;
  color: var(--fc-orange);
  margin-bottom: 10px;
  text-transform: uppercase;
}

.headline-main {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 58px;
  line-height: 1.05;
  letter-spacing: 2px;
  color: var(--fc-white);
  text-transform: uppercase;
  text-shadow: 0 4px 28px rgba(0, 0, 0, 0.95);
}

/* Subtitle Caption Box */
.caption-box {
  position: absolute;
  bottom: 260px;
  left: 90px;
  right: 90px;
  background: rgba(22, 19, 16, 0.88);
  border: 1px solid rgba(242, 140, 40, 0.35);
  padding: 24px 32px;
  border-radius: 18px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
}

.caption-text {
  font-family: 'Montserrat', sans-serif;
  font-size: 30px;
  line-height: 1.45;
  font-weight: 600;
  color: var(--fc-white);
  text-align: center;
}

.caption-text .highlight {
  color: var(--fc-orange);
  font-weight: 800;
  text-shadow: 0 0 16px rgba(242, 140, 40, 0.6);
}

/* Keyframe Animations */
.bubble-anim {
  animation: floatBubble 2.5s infinite ease-in-out;
}
@keyframes floatBubble {
  0% { transform: translateY(0); opacity: 0.3; }
  50% { opacity: 0.9; }
  100% { transform: translateY(-70px); opacity: 0; }
}

.ripple-anim {
  animation: pulseRipple 2.2s infinite ease-out;
}
@keyframes pulseRipple {
  0% { transform: scale(0.9); opacity: 0.8; }
  100% { transform: scale(1.3); opacity: 0; }
}

.blood-flow-left {
  animation: flowBlood 4s infinite linear;
}
@keyframes flowBlood {
  0% { transform: translateX(0); }
  100% { transform: translateX(-180px); }
}

.glucose-transport {
  animation: dropGlucose 2s infinite ease-in-out;
}
@keyframes dropGlucose {
  0% { transform: translateY(0); opacity: 0.4; }
  100% { transform: translateY(120px); opacity: 1; }
}
"""

with open(stage_dir / "style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

print("Stage style.css written successfully!")

# --- 3. Generate timeline.js ---
# Encodes frame-accurate setSeekTime(t) for Chrome CDP
js_content = f"""
/**
 * Food Code Episode 001 - Millisecond Accurate CDP Timeline Driver
 */

const SCENE_BOUNDS = {json.dumps(scene_bounds, indent=2)};
const TOTAL_DURATION = {total_dur};

let currentTime = 0.0;
let isPlaying = false;
let audioElem = null;

function initPlayer() {{
  window.setSeekTime = setSeekTime;
  window.getCurrentTime = () => currentTime;
  window.getTotalDuration = () => TOTAL_DURATION;

  // Render initial frame
  setSeekTime(0.0);
}}

function setSeekTime(timeInSeconds) {{
  currentTime = Math.max(0.0, Math.min(TOTAL_DURATION, timeInSeconds));

  // Determine active scene
  let activeScene = SCENE_BOUNDS[0];
  for (let sc of SCENE_BOUNDS) {{
    if (currentTime >= sc.start && currentTime <= sc.end) {{
      activeScene = sc;
      break;
    }}
  }}

  // Update DOM active scene visibility
  SCENE_BOUNDS.forEach(sc => {{
    const el = document.getElementById(sc.id);
    if (!el) return;
    if (sc.id === activeScene.id) {{
      el.classList.add('active');
    }} else {{
      el.classList.remove('active');
    }}
  }});

  // Compute scene relative progress
  const sceneDur = activeScene.end - activeScene.start;
  const progress = Math.max(0.0, Math.min(1.0, (currentTime - activeScene.start) / Math.max(0.1, sceneDur)));

  // Cubic Easing Out
  const easeProgress = 1.0 - Math.pow(1.0 - progress, 3);

  // Apply 2.5D Camera Transformation
  const cam = activeScene.camera;
  const zStart = cam.zoom_start || 1.0;
  const zEnd = cam.zoom_end || 1.08;
  const currentZoom = zStart + (zEnd - zStart) * easeProgress;

  let panX = 0, panY = 0;
  if (cam.movement === 'pan_right') {{
    panX = -45 * easeProgress;
  }} else if (cam.movement === 'pan_left') {{
    panX = 45 * easeProgress;
  }} else if (cam.movement === 'tilt_down') {{
    panY = -35 * easeProgress;
  }} else if (cam.movement === 'fast_push_in') {{
    panY = -20 * easeProgress;
  }} else if (cam.movement === 'subtle_orbit') {{
    panX = 18 * Math.sin(progress * Math.PI);
    panY = 10 * Math.cos(progress * Math.PI) - 10;
  }}

  // Apply parallax to active scene layers
  const midLayer = document.getElementById(activeScene.id + '_mid');
  if (midLayer) {{
    midLayer.style.transform = `translate3d(${{panX}}px, ${{panY}}px, 0px) scale(${{currentZoom.toFixed(4)}})`;
  }}

  const bgLayer = document.getElementById(activeScene.id + '_bg');
  if (bgLayer) {{
    bgLayer.style.transform = `translate3d(${{(panX * 0.2).toFixed(2)}}px, ${{(panY * 0.2).toFixed(2)}}px, -200px) scale(${{(1.0 + (currentZoom - 1.0) * 0.2).toFixed(4)}})`;
  }}

  const fgLayer = document.getElementById(activeScene.id + '_fg');
  if (fgLayer) {{
    fgLayer.style.transform = `translate3d(${{(panX * 1.4).toFixed(2)}}px, ${{(panY * 1.4).toFixed(2)}}px, 150px) scale(${{(1.0 + (currentZoom - 1.0) * 1.4).toFixed(4)}})`;
  }}
}}

document.addEventListener('DOMContentLoaded', initPlayer);
"""

with open(stage_dir / "timeline.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("Stage timeline.js written successfully!")
print("ALL STAGE ASSETS GENERATED FOR INSTANT NOODLES 001!")

