"""
Kinetic Elements & Motion Graphics Engine for Paper Motion Agent.
Provides rich interactive DOM elements and per-frame JavaScript animators for:
- 3D Split-Flap Mechanical Flip Clock with dynamic numeral flipping
- Rapid Metric Odometers (0 -> 1760mg, 0% -> 76% DV)
- Kinetic Reticles, Crosshairs & Scanning Lasers
- Animated Biological Flows (Bubbling Acid, Glucose Particles, RBC Stream)
- Spring Physics Entry & Slamming Stamp Impacts
"""

import math

class KineticElements:

    @staticmethod
    def split_flap_clock_html(clock_id: str = "flip-clock") -> str:
        """Renders a tactile mechanical split-flap clock with real 3D flappable tiles."""
        return f"""
        <div id="{clock_id}" class="kinetic-flip-clock">
          <div class="clock-housing">
            <div class="tile-group">
              <div class="flap-box"><span id="{clock_id}-h1" class="flap-digit">0</span><div class="flap-crease"></div></div>
              <div class="flap-box"><span id="{clock_id}-h2" class="flap-digit">0</span><div class="flap-crease"></div></div>
            </div>
            <div class="clock-colon">:</div>
            <div class="tile-group">
              <div class="flap-box"><span id="{clock_id}-m1" class="flap-digit">0</span><div class="flap-crease"></div></div>
              <div class="flap-box"><span id="{clock_id}-m2" class="flap-digit">0</span><div class="flap-crease"></div></div>
            </div>
            <div class="clock-label" id="{clock_id}-unit">HOURS</div>
          </div>
        </div>
        """

    @staticmethod
    def kinetic_odometer_html(counter_id: str = "sodium-odometer") -> str:
        """Renders an animated metric gauge with numerical odometer and radial bar."""
        return f"""
        <div id="{counter_id}" class="kinetic-odometer-card">
          <div class="odometer-header">
            <span class="odo-icon">⚠️</span>
            <span class="odo-title">SODIUM CONTENT ANALYSIS</span>
          </div>
          <div class="odometer-display">
            <span id="{counter_id}-val" class="odo-number">0</span>
            <span class="odo-unit">mg</span>
          </div>
          <div class="odometer-bar-track">
            <div id="{counter_id}-bar" class="odometer-bar-fill"></div>
          </div>
          <div class="odometer-footer">
            <span class="odo-alert">DAILY VALUE: <strong id="{counter_id}-pct">0%</strong></span>
            <span class="odo-status">CRITICAL</span>
          </div>
        </div>
        """

    @staticmethod
    def scanning_laser_html() -> str:
        """Renders a high-tech documentary scanning bar that sweeps over documents."""
        return """
        <div class="scanning-laser-line" id="doc-laser"></div>
        """

    @staticmethod
    def bubbling_acid_svg() -> str:
        """Renders animated rising bubbles for the stomach gastric acid pool."""
        bubbles = ""
        for i in range(12):
            cx = 40 + (i * 24) % 240
            r = 4 + (i % 4) * 2.5
            bubbles += f'<circle id="acid-bub-{i}" cx="{cx}" cy="120" r="{r}" fill="#FFE6A7" opacity="0.85"/>\n'
        return f"""
        <svg class="acid-bubble-emitter" viewBox="0 0 320 160">
          {bubbles}
        </svg>
        """

    @staticmethod
    def get_kinetic_css() -> str:
        """Returns CSS styles for all kinetic components."""
        return """
        /* 3D Mechanical Split-Flap Clock */
        .kinetic-flip-clock {
          position: absolute;
          background: #E8DEC8;
          border: 3px solid #C4B296;
          border-radius: 16px;
          padding: 12px 20px;
          box-shadow: 0 16px 35px rgba(0,0,0,0.85);
          z-index: 400;
        }
        .clock-housing {
          display: flex; align-items: center; gap: 8px;
        }
        .tile-group { display: flex; gap: 4px; }
        .flap-box {
          position: relative;
          width: 50px; height: 70px;
          background: #24201C;
          border-radius: 8px;
          display: flex; align-items: center; justify-content: center;
          overflow: hidden;
          box-shadow: inset 0 2px 6px rgba(0,0,0,0.8);
        }
        .flap-digit {
          font-family: 'Bebas Neue', sans-serif;
          font-size: 58px; color: #FAF5E8;
          line-height: 1;
        }
        .flap-crease {
          position: absolute; top: 34px; left: 0; right: 0;
          height: 2px; background: rgba(10,8,6,0.9);
          box-shadow: 0 1px 2px rgba(255,255,255,0.15);
        }
        .clock-colon {
          font-family: 'Bebas Neue', sans-serif;
          font-size: 48px; color: #8B3524;
          font-weight: 900; line-height: 1;
        }
        .clock-label {
          font-family: 'JetBrains Mono', monospace;
          font-size: 11px; font-weight: 800;
          color: #6E5C4E; letter-spacing: 2px;
          margin-left: 6px;
        }

        /* Kinetic Odometer Card */
        .kinetic-odometer-card {
          position: absolute;
          background: rgba(24, 20, 16, 0.96);
          border: 2px solid #FF6B00;
          border-radius: 18px;
          padding: 20px 26px;
          box-shadow: 0 18px 45px rgba(0,0,0,0.92);
          z-index: 450;
        }
        .odometer-header {
          display: flex; align-items: center; gap: 8px;
          font-family: 'Montserrat', sans-serif; font-size: 13px; font-weight: 800;
          color: #FF6B00; letter-spacing: 2px; margin-bottom: 8px;
        }
        .odometer-display {
          display: flex; align-items: baseline; gap: 6px; margin-bottom: 12px;
        }
        .odo-number {
          font-family: 'Bebas Neue', sans-serif; font-size: 72px;
          color: #FFFFFF; line-height: 0.9;
        }
        .odo-unit {
          font-family: 'JetBrains Mono', monospace; font-size: 24px;
          color: #FF6B00; font-weight: 800;
        }
        .odometer-bar-track {
          width: 100%; height: 12px; background: #33271E;
          border-radius: 6px; overflow: hidden; margin-bottom: 10px;
        }
        .odometer-bar-fill {
          height: 100%; width: 0%;
          background: linear-gradient(90deg, #FF6B00, #E53E3E);
          border-radius: 6px;
          box-shadow: 0 0 14px rgba(255, 107, 0, 0.7);
        }
        .odometer-footer {
          display: flex; justify-content: space-between; align-items: center;
          font-family: 'JetBrains Mono', monospace; font-size: 13px;
        }
        .odo-alert { color: #FAF5E8; font-weight: 700; }
        .odo-alert strong { color: #E53E3E; font-size: 16px; }
        .odo-status {
          background: #8B3524; color: #FFF; padding: 2px 8px; border-radius: 4px; font-weight: 800;
        }

        /* Scanning Laser */
        .scanning-laser-line {
          position: absolute; left: 0; right: 0; height: 3px;
          background: #FF6B00;
          box-shadow: 0 0 16px 4px rgba(255, 107, 0, 0.85);
          pointer-events: none; z-index: 550; opacity: 0;
        }

        /* Acid Bubbles */
        .acid-bubble-emitter {
          position: absolute; bottom: 180px; left: 320px;
          width: 320px; height: 160px; pointer-events: none; z-index: 350;
        }
        """

    @staticmethod
    def get_kinetic_js_helpers() -> str:
        """Returns JavaScript runtime math helpers for spring physics and continuous flow."""
        return """
        // Spring bounce easing
        function springBounce(p) {
          if (p <= 0) return 0;
          if (p >= 1) return 1;
          return 1.0 - Math.exp(-6 * p) * Math.cos(p * Math.PI * 3.5);
        }

        // Clamp helper
        function clamp(val, min, max) {
          return Math.max(min, Math.min(max, val));
        }

        // Smoothstep
        function smoothstep(min, max, value) {
          var x = Math.max(0, Math.min(1, (value - min) / (max - min)));
          return x * x * (3 - 2 * x);
        }
        """
