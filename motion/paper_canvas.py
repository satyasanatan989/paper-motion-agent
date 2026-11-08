"""
Procedural Tactile Paper & Parchment Engine.
Generates realistic paper texture, notebook spine creases, and scorched borders.
"""

def generate_parchment_css() -> str:
    """Returns CSS rules for the MeanwhileMayank papercraft aesthetic."""
    return """
/* PaperMotion AI - Tactile Papercraft Aesthetic */
:root {
  --bg-parchment: #EFE4D0;
  --bg-parchment-dark: #DECBB0;
  --text-dark: #201815;
  --text-gold: #C69214;
  --royal-crimson: #9B111E;
  --royal-saffron: #E65100;
  --royal-navy: #002244;
  --parchment-shadow: 0 12px 28px rgba(32, 24, 21, 0.28), 0 3px 8px rgba(32, 24, 21, 0.16);
  --paper-cutout: drop-shadow(0 10px 18px rgba(25, 18, 12, 0.32)) drop-shadow(0 2px 5px rgba(25, 18, 12, 0.18));
}

#stage-container {
  position: relative;
  width: 1080px;
  height: 1920px;
  transform-origin: center center;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.85);
  background: var(--bg-parchment);
  overflow: hidden;
}

/* Center Scroll Crease */
.scroll-spine {
  position: absolute;
  top: 0;
  left: 540px;
  width: 3px;
  height: 100%;
  background: linear-gradient(to right, rgba(0,0,0,0.22), rgba(255,255,255,0.18), rgba(0,0,0,0.22));
  box-shadow: -6px 0 16px rgba(0,0,0,0.12), 6px 0 16px rgba(0,0,0,0.12);
  z-index: 5;
  pointer-events: none;
}

/* Scorched Edge Vignette */
.scorched-border {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  box-shadow: inset 0 0 100px rgba(60, 35, 15, 0.45), inset 0 0 35px rgba(30, 15, 5, 0.65);
  pointer-events: none;
  z-index: 6;
}

.scene {
  position: absolute;
  top: 0;
  left: 0;
  width: 1080px;
  height: 1920px;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s ease-out;
  padding: 170px 80px 200px 90px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

body.render-mode .scene {
  transition: none !important;
}

.scene.active {
  opacity: 1;
  visibility: visible;
}
"""

def generate_parchment_canvas_js() -> str:
    """Returns Javascript code to paint organic fibers & grain onto HTML5 canvas."""
    return """
function renderParchmentTexture() {
  const canvas = document.getElementById('parchment-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  // Warm ochre & parchment radial gradient
  const grad = ctx.createRadialGradient(540, 960, 200, 540, 960, 1100);
  grad.addColorStop(0, '#FAF2E4');
  grad.addColorStop(0.65, '#EFE2CB');
  grad.addColorStop(1, '#D8C3A4');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 1080, 1920);

  // Subtle paper fibers & gold flakes
  const imgData = ctx.getImageData(0, 0, 1080, 1920);
  const data = imgData.data;
  for (let i = 0; i < data.length; i += 4) {
    const noise = (Math.random() - 0.5) * 16;
    data[i] = Math.min(255, Math.max(0, data[i] + noise));
    data[i + 1] = Math.min(255, Math.max(0, data[i + 1] + noise - 2));
    data[i + 2] = Math.min(255, Math.max(0, data[i + 2] + noise - 6));
  }
  ctx.putImageData(imgData, 0, 0);
}
"""
