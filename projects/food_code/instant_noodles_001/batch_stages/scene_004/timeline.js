
    
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
        
    
    let currentTime = 0.0;
    const TOTAL_DURATION = 6.37;
    const WORD_COUNT = 12;
    
    window.setSeekTime = function(t) {
      currentTime = Math.max(0.0, Math.min(TOTAL_DURATION, t));
      const p = currentTime / TOTAL_DURATION;
      // Smooth cubic ease out for camera
      const easeP = 1.0 - Math.pow(1.0 - p, 3);
      const zoom = 1.0 + (1.12 - 1.0) * easeP;
      
      let panX = 0, panY = 0;
      let rot = 0;
      if ('pan_left' === 'pan_right') {
        panX = -45 * easeP;
      } else if ('pan_left' === 'pan_left') {
        panX = 45 * easeP;
      } else if ('pan_left' === 'tilt_down') {
        panY = -35 * easeP;
      } else if ('pan_left' === 'fast_push_in') {
        panY = -20 * easeP;
        rot = Math.sin(p * Math.PI) * 1.2;
      } else if ('pan_left' === 'subtle_orbit') {
        panX = 18 * Math.sin(p * Math.PI);
        panY = 10 * Math.cos(p * Math.PI) - 10;
        rot = 0.8 * Math.sin(p * Math.PI);
      }
      
      // Camera Impact Shake (Triggered by Stamp Slam at t = 0.85s - 1.05s)
      let impactShake = 0;
      if (currentTime >= 0.85 && currentTime <= 1.05) {
        const shakeP = (currentTime - 0.85) / 0.20;
        impactShake = Math.sin(shakeP * Math.PI * 8) * (1.0 - shakeP) * 5.0;
      }
      
      // Stop-Motion Frame Jitter Engine (Quantized to 12 FPS)
      const frameNum = Math.floor(currentTime * 30);
      const jitterCycle = Math.floor(frameNum / 2.5);
      const hash = Math.sin(jitterCycle * 12.9898 + 78.233) * 43758.5453;
      const jitterRot = ((hash - Math.floor(hash)) - 0.5) * 1.2;
      const jitterX = (((hash * 10) - Math.floor(hash * 10)) - 0.5) * 2.6;
      const jitterY = (((hash * 100) - Math.floor(hash * 100)) - 0.5) * 2.6;
      
      const st = document.getElementById('stage-asset');
      if (st) {
        const finalX = (panX + jitterX).toFixed(2);
        const finalY = (panY + jitterY + impactShake).toFixed(2);
        const finalRot = (rot + jitterRot).toFixed(2);
        st.style.transform = `translate3d(${finalX}px, ${finalY}px, 0px) scale(${zoom.toFixed(4)}) rotate(${finalRot}deg)`;
      }
      
      // Film Flash Transition on Scene Exit (Final 0.22s)
      const flash = document.getElementById('film-flash');
      if (flash) {
        if (currentTime >= TOTAL_DURATION - 0.22) {
          const flashP = (currentTime - (TOTAL_DURATION - 0.22)) / 0.22;
          flash.style.opacity = (Math.sin(flashP * Math.PI) * 0.70).toFixed(2);
        } else {
          flash.style.opacity = '0';
        }
      }
      
      // 1. Spring Entry on Hero Cutout
      const hero = document.getElementById('hero-card');
      if (hero) {
        const entryP = clamp(currentTime / 0.42, 0, 1);
        const spring = springBounce(entryP);
        const dropY = (1.0 - spring) * -90;
        const entryScale = 0.88 + 0.12 * spring;
        hero.style.transform = `translateY(${dropY.toFixed(2)}px) scale(${entryScale.toFixed(4)})`;
      }
      
      // 2. Pushpin Slam
      const pin = document.getElementById('pin-elem');
      if (pin) {
        const pinP = clamp((currentTime - 0.35) / 0.22, 0, 1);
        const pScale = springBounce(pinP);
        pin.style.transform = `scale(${pScale.toFixed(3)})`;
        pin.style.opacity = pinP > 0 ? '1' : '0';
      }
      
      // 3. Scotch Tape Slap
      const tape = document.getElementById('tape-elem');
      if (tape) {
        const tapeP = clamp((currentTime - 0.25) / 0.22, 0, 1);
        const tScale = springBounce(tapeP);
        tape.style.transform = `scale(${tScale.toFixed(3)})`;
        tape.style.opacity = tapeP > 0 ? '1' : '0';
      }
      
      // 4. Rubber Stamp Slam Impact
      const stamp = document.getElementById('stamp-elem');
      if (stamp) {
        const stampP = clamp((currentTime - 0.85) / 0.22, 0, 1);
        if (stampP <= 0) {
          stamp.style.opacity = '0';
        } else {
          const sScale = 2.2 - 1.2 * springBounce(stampP);
          stamp.style.opacity = '0.94';
          stamp.style.transform = `scale(${sScale.toFixed(3)}) rotate(-6deg)`;
        }
      }
      
      // 5. Secondary Cutout Follow-Through Physics (CineCode / Vox Style)
      const sec = document.getElementById('sec-card');
      if (sec) {
        const secP = clamp((currentTime - 0.12) / 0.38, 0, 1);
        const secSpring = springBounce(secP);
        const secDropY = (1.0 - secSpring) * -45;
        const secScale = 0.88 + 0.12 * secSpring;
        sec.style.transform = `translateY(${secDropY.toFixed(2)}px) scale(${secScale.toFixed(4)})`;
        sec.style.opacity = secP > 0 ? '0.92' : '0';
      }

      // 6. Sequential Tactile Badge Landings
      const b1 = document.getElementById('badge-1');
      const b2 = document.getElementById('badge-2');
      if (b1) {
        const p1 = clamp((currentTime - 0.30) / 0.28, 0, 1);
        b1.style.transform = `scale(${springBounce(p1).toFixed(3)})`;
        b1.style.opacity = p1 > 0 ? '1' : '0';
      }
      if (b2) {
        const p2 = clamp((currentTime - 0.52) / 0.28, 0, 1);
        b2.style.transform = `scale(${springBounce(p2).toFixed(3)})`;
        b2.style.opacity = p2 > 0 ? '1' : '0';
      }

      // 7. Mechanical Flip Clock Pop-in
      const clockBox = document.getElementById('clock-container');
      if (clockBox) {
        const cP = clamp(currentTime / 0.30, 0, 1);
        clockBox.style.transform = `scale(${springBounce(cP).toFixed(3)})`;
      }

      // 8. 3D Vork Molecule Floating Animation
      const mol = document.getElementById('mol-elem');
      if (mol) {
        const molP = clamp((currentTime - 0.20) / 0.40, 0, 1);
        const mSpring = springBounce(molP);
        const mFloat = Math.sin(currentTime * 3.5) * 12.0;
        const mRot = Math.cos(currentTime * 2.0) * 6.0;
        mol.style.transform = `scale(${mSpring.toFixed(3)}) translateY(${mFloat.toFixed(2)}px) rotate(${mRot.toFixed(2)}deg)`;
        mol.style.opacity = molP > 0 ? '0.96' : '0';
      }

      // 9. Scene-Specific Kinetic Motions
      if ('scene_004' === 'scene_001') {
        const sec = Math.floor(currentTime * 12);
        const m2 = document.getElementById('clock-01-m2');
        const m1 = document.getElementById('clock-01-m1');
        if (m2) m2.innerText = (sec % 10);
        if (m1) m1.innerText = Math.floor((sec / 10) % 6);
      }
      else if ('scene_004' === 'scene_003') {
        for (let b = 0; b < 12; b++) {
          const bub = document.getElementById('acid-bub-' + b);
          if (bub) {
            const cycle = (currentTime * 45 + b * 18) % 100;
            bub.setAttribute('cy', (140 - cycle).toFixed(1));
            bub.setAttribute('opacity', (1.0 - cycle / 100).toFixed(2));
          }
        }
        const hr = Math.floor((currentTime / TOTAL_DURATION) * 2.0);
        const h2 = document.getElementById('clock-03-h2');
        if (h2) h2.innerText = hr;
      }
      else if ('scene_004' === 'scene_006') {
        const laser = document.getElementById('doc-laser');
        if (laser) {
          const laserP = clamp((currentTime - 0.4) / 1.8, 0, 1);
          laser.style.top = (laserP * 560).toFixed(1) + 'px';
          laser.style.opacity = (currentTime >= 0.4 && currentTime <= 2.4) ? '1' : '0';
        }
        const odoVal = document.getElementById('odo-sodium-val');
        const odoPct = document.getElementById('odo-sodium-pct');
        const odoBar = document.getElementById('odo-sodium-bar');
        if (odoVal && odoPct && odoBar) {
          const odoP = clamp((currentTime - 0.5) / 2.2, 0, 1);
          const easedOdo = springBounce(odoP);
          const currentMg = Math.floor(easedOdo * 1760);
          const currentPercent = Math.floor(easedOdo * 76);
          odoVal.innerText = currentMg.toLocaleString();
          odoPct.innerText = currentPercent + '%';
          odoBar.style.width = currentPercent + '%';
        }
      }
      else if ('scene_004' === 'scene_007') {
        const b1 = document.getElementById('badge-1');
        const b2 = document.getElementById('badge-2');
        if (b1) {
          const p1 = clamp((currentTime - 0.6) / 0.3, 0, 1);
          b1.style.transform = `scale(${springBounce(p1).toFixed(3)})`;
        }
        if (b2) {
          const p2 = clamp((currentTime - 1.4) / 0.3, 0, 1);
          b2.style.transform = `scale(${springBounce(p2).toFixed(3)})`;
        }
      }
      
      // 6. Word-by-Word Kinetic Karaoke Subtitle Engine
      const activeWordIdx = Math.floor((currentTime / TOTAL_DURATION) * WORD_COUNT);
      for (let w = 0; w < WORD_COUNT; w++) {
        const wElem = document.getElementById(`w-3-` + w);
        if (wElem) {
          if (w === activeWordIdx) {
            wElem.className = wElem.className.replace(/\s*(active|spoken|upcoming)/g, '') + ' active';
          } else if (w < activeWordIdx) {
            wElem.className = wElem.className.replace(/\s*(active|spoken|upcoming)/g, '') + ' spoken';
          } else {
            wElem.className = wElem.className.replace(/\s*(active|spoken|upcoming)/g, '') + ' upcoming';
          }
        }
      }
    };
    window.getCurrentTime = () => currentTime;
    window.getTotalDuration = () => TOTAL_DURATION;
    document.addEventListener('DOMContentLoaded', () => window.setSeekTime(0.0));
    