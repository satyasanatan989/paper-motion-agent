# FOOD CODE — Cinematic Visual Style Guide & Director Manual

```
  ███████╗ ██████╗  ██████╗ ██████╗      ██████╗ ██████╗ ██████╗ ███████╗
  ██╔════╝██╔═══██╗██╔═══██╗██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔════╝
  █████╗  ██║   ██║██║   ██║██║  ██║    ██║     ██║   ██║██║  ██║█████╗  
  ██╔══╝  ██║   ██║██║   ██║██║  ██║    ██║     ██║   ██║██║  ██║██╔══╝  
  ██║     ╚██████╔╝╚██████╔╝██████╔╝    ╚██████╗╚██████╔╝██████╔╝███████╗
  ╚═╝      ╚═════╝  ╚═════╝ ╚═════╝      ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
```

> **Official Visual Identity, Cinematography Language & Motion Design System**  
> *Brand*: **FOOD CODE**  
> *Format*: Vertical 9:16 ($1080 \times 1920$), 30 FPS  
> *Target Aesthetic*: High-End Documentary (Kurzgesagt $\times$ Vox $\times$ Chef's Table)

---

## 1. Brand Identity & Atmosphere

Food Code transforms complex nutritional physiology, biochemistry, and food industrial processing into visually stunning, cinematic vertical documentaries. 

### Core Visual Pillars:
1. **Dark Cinematic Environments**: Deep void obsidian, charred iron, and dark espresso backdrops (`#0B0907`, `#161310`) that make illuminated food assets leap forward.
2. **Signature Burnt-Orange Glow**: High-retention kinetic accenting (`#FF6B00`, `#E65100`, `#FFA94D`) applied strategically to critical mechanisms, hazard indicators, and chemical bonds.
3. **Warm-White Typography**: Elegant, high-contrast, paper-pressed typographic hierarchy (`#F5EBE1`) ensuring readability on mobile screens without harsh pure-white glare.
4. **Macro Food Cinematography**: Extreme close-up perspectives revealing biological textures—wheat husk fibers, gluten elasticity, boiling gastric acid, lipid micelles, and glucose lattices.
5. **Multi-Plane 2.5D Parallax**: Continuous physical camera depth separating foreground smoke/acid particles, midground anatomical organs, and background scorched vignettes.

---

## 2. Color System & Light Architecture

```
[ Primary Background: #0B0907 ] ─── [ Surface Canvas: #161310 ]
             │                                     │
             ▼                                     ▼
[ Burnt Orange Glow: #FF6B00 ] ─── [ Deep Amber: #E65100 ]
             │                                     │
             ▼                                     ▼
[ Warm White Type: #F5EBE1 ]   ─── [ Muted Earth: #A89F91 ]
```

### Color Palette Matrix:
| Role | Hex Code | Swatch Name | Strategic Usage Rule |
| :--- | :--- | :--- | :--- |
| **Primary Base** | `#0B0907` | Deep Obsidian | Canvas foundation. Replaces flat gray/black with warm charcoal tone. |
| **Surface Elev** | `#161310` | Dark Espresso | Card backgrounds, organ walls, and metric tile containers. |
| **Primary Accent**| `#FF6B00`| **Burnt Orange** | **Core Brand Color.** Highlighted keywords, chemical bonds, acid reflux plumes. |
| **Deep Contrast**| `#E65100` | Scorched Amber | Borders, inactive indicators, drop shadows, and gluten fiber cross-links. |
| **Warm Highlight**| `#FFA94D`| Radiant Gold | Active counter numbers, enzyme active sites, and gold-leaf verdict stamps. |
| **Primary Text** | `#F5EBE1` | Warm Alabaster | Headlines, voiceover subtitle captions, and chapter titles. |
| **Secondary Text**| `#A89F91`| Muted Stone | Metric sub-labels, source citations, and timeline unit markers. |
| **Hazard Alert** | `#FF3344` | Acid Crimson | Gastric ulceration, cellular damage, toxic breakdown markers. |
| **Bio/Vitality** | `#48BB78` | Chlorophyll Green| Whole fiber nutrients, active peristalsis, and healthy gut microbiome. |

> [!IMPORTANT]
> **The 10% Orange Rule**: Never bathe the entire frame in orange. Orange is the visual laser. If more than 15% of the total screen pixels are bright orange simultaneously, contrast collapses and the viewer tunes out.

---

## 3. Typographic Hierarchy & Vertical 9:16 Geometry

All typography must respect social mobile safe areas (120px top header clearance for platform chrome, 240px bottom clearance for engagement icons and caption bars).

```
┌───────────────────────── 1080 px ─────────────────────────┐
│                                                           │ 0 px
│   [ SAFE MARGIN TOP: 120px - Story / Reel Chrome Area ]   │
│                                                           │
│   ┌───────────────────────────────────────────────────┐   │
│   │  ● FOOD CODE • BRAND BADGE (Top Center)           │   │ 140 px
│   └───────────────────────────────────────────────────┘   │
│                                                           │
│   ┌───────────────────────────────────────────────────┐   │
│   │  CHAPTER 03 • CORE MECHANISM                      │   │ 280 px
│   │  THE GUT GLUE MATRIX                              │   │ (Headline)
│   └───────────────────────────────────────────────────┘   │
│                                                           │
│                                                           │
│          [ SCIENTIFIC 3D / 2.5D MACRO STAGE ]             │
│                                                           │
│                                                           │
│   ┌───────────────────────────────────────────────────┐   │
│   │  "In the stomach, water and maida react to form   │   │ 1420 px
│   │   a <span class="highlight">dense adhesive paste</span>" │   │ (Subtitles)
│   └───────────────────────────────────────────────────┘   │
│                                                           │
│   [ SAFE MARGIN BOTTOM: 240px - Social UI & Thumb Area ]  │
│                                                           │ 1920 px
└───────────────────────────────────────────────────────────┘
```

### Font Pairings:
1. **Headlines (`.headline-main`)**:
   - Font: `Bebas Neue` / `Cinzel` (Condensed Uppercase).
   - Size: $54\text{px} - 68\text{px}$, Tracking $+2\text{px}$, Line-height $1.1$.
   - Drop shadow: `0 4px 24px rgba(0, 0, 0, 0.9)`.
2. **Chapter Badges (`.headline-sub`)**:
   - Font: `Montserrat` (Weight: 800 ExtraBold).
   - Size: $15\text{px} - 18\text{px}$, Tracking $+4\text{px}$, Color: `var(--fc-burnt-orange)`.
3. **Narration Subtitles (`.subtitle-text`)**:
   - Font: `Montserrat` / `Rozha One` (Latin + Devanagari Hindi code-switching).
   - Size: $34\text{px} - 40\text{px}$, Line-height $1.35$.
   - Highlighting: Dynamic burnt-orange glow (`text-shadow: 0 0 14px rgba(255, 107, 0, 0.6)`).
4. **Data Counters (`.flip-tile`)**:
   - Font: `JetBrains Mono` / `Cinzel` in mechanical split-flap tiles.

---

## 4. The 10 Creative Rules of Food Code

### Rule 1: Never Repeat Scene Layouts in Consecutive Scenes
- **Violation**: Chapter 1 displays a center card with text below. Chapter 2 displays another center card with text below.
- **Enforcement**: Alternating compositional geometry:
  - *Scene 1*: Extreme macro focal center with radial outward lighting.
  - *Scene 2*: Split-screen longitudinal cross-section (Left vs Right).
  - *Scene 3*: Vertical scroll tracking camera following liquid downward.
  - *Scene 4*: Close-up organ cutaway with animated fluid overlay.
  - *Scene 5*: Dual mechanical split-flap comparison counters.
  - *Scene 6*: Gold-embossed verdict seal with weighted balance scale.

### Rule 2: Never Use Static Slides as a Substitute for Animation
- Every frame must have continuous micro-motion: breathing organ oscillation, floating steam particles, rising acid bubbles, or subtle camera drift ($z\text{-zoom} \ge 1.05\times$).

### Rule 3: Every Scene Must Contain at Least One Meaningful Visual Event
- A visual event is not just text appearing. Examples:
  - A wheat kernel mechanically peeling outward into bran, germ, and starch.
  - A pool of gastric acid boiling and breaching the lower esophageal valve.
  - A split-flap counter rapidly spinning from $0$ to $50\text{ hours}$.

### Rule 4: Use Depth, Perspective & Camera Movement Wherever Appropriate
- Always separate visual elements into 3 distinct parallax depth planes ($0.1\times$ background drift, $0.5\times$ midground motion, $1.4\times$ foreground particles).

### Rule 5: Use Macro Cinematography to Communicate Ingredient Textures
- When talking about flour, show the microscopic jagged starch granules; when talking about oil, show the amber refractive lipid spheres with specular highlights.

### Rule 6: Use 3D Scientific Visualizations for Biological Processes
- Render organ cross-sections (stomach rugae, pyloric sphincter, villi micro-fingers) rather than generic cartoon clipart.

### Rule 7: Use Typography to Emphasize Important Concepts, Not Fill Space
- Subtitles must be concise and word-synchronized. Never display walls of paragraphs.

### Rule 8: Strategic Use of Burnt Orange
- Reserve burnt-orange accents for the single most important concept per second (the keyword, the chemical bond, the rising acid).

### Rule 9: Narratively Motivated Transitions
- Transitions must match the physics of the narration: downward camera tilt when food is swallowed; paper tear when grain is stripped; heat wipe when temperature rises.

### Rule 10: Scientific Accuracy Over Cheap Spectacle
- Ground all anatomical structures, chemical equations, and transit time statistics in peer-reviewed physiological facts.

---

## 5. Camera Grammar & Mathematical Easing

All camera moves must follow smooth non-linear acceleration curves (`ease-out-cubic` or `ease-in-out-quad`). Linear camera movement is strictly forbidden.

```
Camera Move             Zoom Range        Pan / Tilt Target           Narrative Emotion
─────────────────────────────────────────────────────────────────────────────────────────────
Slow Cinematic Push-In  1.00x → 1.08x     Center Focus (0, -15px)     Intrigue, focus, gravity
Fast Impact Zoom        1.00x → 1.16x     Hazard Focal Point          Shock, crisis, biological hazard
Macro Tracking          1.12x → 1.25x     Following fluid / particle  Scientific inspection
Smooth Pull-Back        1.10x → 1.00x     Wide scale reveal           Context, whole-body impact
Controlled Whip Tilt    1.00x → 1.06x     Y: +45px (Esophagus → Gut)  Swallowing / downward transit
Subtle Orbit            1.00x → 1.04x     Polar angular oscillation   Verdict, reflection, conclusion
```

---

## 6. Food Science Reusable Asset Library

Available in [`visual_engine/food_science_library.py`](file:///C:/Users/prabh/Documents/antigravity/lucid-shannon/paper-motion-agent/visual_engine/food_science_library.py):

```python
from visual_engine.food_science_library import FoodScienceVisuals

# 1. Wheat Kernel Macro Cross-Section
kernel_svg = FoodScienceVisuals.wheat_kernel_macro()

# 2. Viscous Glutenin/Gliadin Starch Matrix
gluten_svg = FoodScienceVisuals.gluten_matrix_macro()

# 3. 3D Gastric Mucosa & Acid Reflux Plume
stomach_svg = FoodScienceVisuals.stomach_acid_reflux_macro()

# 4. Dual Split-Flap Gut Transit Comparison Clock
clock_svg = FoodScienceVisuals.transit_clock_comparison()

# 5. Cyclic Glucose Ring Molecule
glucose_svg = FoodScienceVisuals.glucose_ring_molecule()
```

---

## 7. Quality Control Checklist

Before approving any Food Code documentary video, verify:

- [ ] **Color Check**: Dark obsidian base with strategic burnt-orange accents (under 15% frame occupancy).
- [ ] **No Static Hold**: Continuous micro-motion on all layers (breathing oscillation or particle drift).
- [ ] **No PowerPoint Aesthetic**: Multi-plane depth with distinct camera parallax.
- [ ] **9:16 Safe Areas**: All text and critical graphics remain inside the $120\text{px}$ top and $240\text{px}$ bottom margins.
- [ ] **Loudness**: Integrated loudness conforms to $-14\text{ LUFS} \pm 1.5\text{ LUFS}$ with zero peak clipping.
- [ ] **Scientific Grounding**: Correct anatomical names, biochemical terminology, and timeframes.
