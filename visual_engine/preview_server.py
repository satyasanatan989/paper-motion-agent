"""
Interactive Local Stage Previewer & Scrubbing HUD Server.
Zero-dependency Python HTTP server that serves PaperMotion web stages with
a live timeline scrubbing interface, frame stepper, and word-level audio sync inspector.
"""

import http.server
import socketserver
import threading
import sys
import urllib.parse
from pathlib import Path
from typing import Optional


PREVIEW_HUD_SCRIPT = """
<!-- PaperMotion Live Timeline Scrubber HUD -->
<div id="papermotion-preview-hud" style="
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: rgba(18, 14, 10, 0.96);
  border-top: 2px solid #ECC94B;
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 16px;
  z-index: 999999;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #FFFDF8;
  box-shadow: 0 -8px 24px rgba(0,0,0,0.8);
">
  <button id="pm-play-btn" style="
    background: #FF6B00;
    border: none;
    color: white;
    padding: 8px 16px;
    font-weight: 800;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
  ">PLAY</button>

  <button id="pm-step-back" style="background:#2C2218;border:1px solid #5A4328;color:#FFF;padding:6px 10px;border-radius:4px;cursor:pointer;">-1F</button>
  <button id="pm-step-fwd" style="background:#2C2218;border:1px solid #5A4328;color:#FFF;padding:6px 10px;border-radius:4px;cursor:pointer;">+1F</button>

  <input type="range" id="pm-scrubber" min="0" max="100" step="0.01" value="0" style="
    flex: 1;
    accent-color: #FF6B00;
    cursor: pointer;
  ">

  <div id="pm-timecode" style="font-family: monospace; font-size: 14px; color: #ECC94B; min-width: 130px;">
    00:00.00 / 00:00.00
  </div>

  <select id="pm-speed" style="background:#2C2218;border:1px solid #5A4328;color:#FFF;padding:6px 8px;border-radius:4px;cursor:pointer;">
    <option value="0.25">0.25x</option>
    <option value="0.5">0.5x</option>
    <option value="1.0" selected>1.0x</option>
    <option value="2.0">2.0x</option>
  </select>

  <select id="pm-scenes" style="background:#2C2218;border:1px solid #5A4328;color:#FFF;padding:6px 8px;border-radius:4px;cursor:pointer;">
    <option value="">Jump to Scene...</option>
  </select>
</div>

<script>
(function() {
  const playBtn = document.getElementById('pm-play-btn');
  const scrubber = document.getElementById('pm-scrubber');
  const timecode = document.getElementById('pm-timecode');
  const speedSel = document.getElementById('pm-speed');
  const scenesSel = document.getElementById('pm-scenes');
  const stepBackBtn = document.getElementById('pm-step-back');
  const stepFwdBtn = document.getElementById('pm-step-fwd');

  let isPlaying = false;
  let curT = 0.0;
  let maxT = 10.0;
  let lastRafTime = 0;
  let speed = 1.0;

  function fmtTime(s) {
    const mins = Math.floor(s / 60);
    const secs = (s % 60).toFixed(2);
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(5, '0')}`;
  }

  function updateDisplay() {
    scrubber.value = curT;
    timecode.textContent = `${fmtTime(curT)} / ${fmtTime(maxT)}`;
    if (window.setSeekTime) window.setSeekTime(curT);
  }

  // Populate scenes from window.__timelines or chapters
  setTimeout(() => {
    if (window.getVideoDuration) {
      maxT = window.getVideoDuration();
      scrubber.max = maxT;
    }
    const sceneEls = document.querySelectorAll('.scene');
    sceneEls.forEach((sc, i) => {
      const opt = document.createElement('option');
      opt.value = i;
      opt.textContent = `Scene ${i + 1}: ${sc.id}`;
      scenesSel.appendChild(opt);
    });
    updateDisplay();
  }, 300);

  function loop(now) {
    if (!isPlaying) return;
    if (!lastRafTime) lastRafTime = now;
    const dt = (now - lastRafTime) / 1000.0;
    lastRafTime = now;

    curT += dt * speed;
    if (curT >= maxT) {
      curT = maxT;
      isPlaying = false;
      playBtn.textContent = 'PLAY';
    }
    updateDisplay();
    requestAnimationFrame(loop);
  }

  playBtn.addEventListener('click', () => {
    isPlaying = !isPlaying;
    playBtn.textContent = isPlaying ? 'PAUSE' : 'PLAY';
    if (isPlaying) {
      if (curT >= maxT) curT = 0.0;
      lastRafTime = 0;
      requestAnimationFrame(loop);
    }
  });

  scrubber.addEventListener('input', (e) => {
    curT = parseFloat(e.target.value);
    updateDisplay();
  });

  speedSel.addEventListener('change', (e) => {
    speed = parseFloat(e.target.value);
  });

  scenesSel.addEventListener('change', (e) => {
    const idx = parseInt(e.target.value, 10);
    if (!isNaN(idx)) {
      const scenes = document.querySelectorAll('.scene');
      if (scenes[idx]) {
        // Seek to approximately the start of this chapter
        curT = (idx / scenes.length) * maxT;
        updateDisplay();
      }
    }
  });

  stepBackBtn.addEventListener('click', () => {
    isPlaying = false;
    playBtn.textContent = 'PLAY';
    curT = Math.max(0.0, curT - (1.0 / 30.0));
    updateDisplay();
  });

  stepFwdBtn.addEventListener('click', () => {
    isPlaying = false;
    playBtn.textContent = 'PLAY';
    curT = Math.min(maxT, curT + (1.0 / 30.0));
    updateDisplay();
  });

  // Spacebar toggle
  window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
      e.preventDefault();
      playBtn.click();
    } else if (e.code === 'ArrowLeft') {
      e.preventDefault();
      stepBackBtn.click();
    } else if (e.code === 'ArrowRight') {
      e.preventDefault();
      stepFwdBtn.click();
    }
  });
})();
</script>
"""


class StagePreviewRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler injecting the live timeline scrubbing HUD into index.html."""

    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def end_headers(self):
        # Prevent caching so edits are instantly visible
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        clean_path = urllib.parse.urlsplit(self.path).path
        if clean_path in ("/", "/index.html"):
            index_path = Path(self.directory) / "index.html"
            if index_path.exists():
                content = index_path.read_text(encoding="utf-8")
                # Inject scrubber HUD before </body>
                if "</body>" in content:
                    content = content.replace("</body>", f"{PREVIEW_HUD_SCRIPT}\n</body>")
                else:
                    content += PREVIEW_HUD_SCRIPT

                encoded = content.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
                return

        return super().do_GET()


class ThreadedStageServer(socketserver.ThreadingTCPServer):
    """Multi-threaded TCP server enabling non-blocking asset streaming and address reuse."""
    allow_reuse_address = True
    daemon_threads = True


def run_preview_server(stage_dir: Path, port: int = 8080, host: str = "127.0.0.1") -> None:
    """Runs a local multi-threaded preview server for the specified stage directory."""
    stage_path = Path(stage_dir).resolve()
    if not stage_path.exists():
        raise FileNotFoundError(f"Stage directory not found: {stage_path}")

    handler = lambda *args, **kwargs: StagePreviewRequestHandler(*args, directory=str(stage_path), **kwargs)
    with ThreadedStageServer((host, port), handler) as httpd:
        print(f"🎬 PaperMotion Stage Previewer running at http://{host}:{port}")
        print(f"   Serving: {stage_path}")
        print(f"   Controls: Space=Play/Pause, Left/Right=Step Frame")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()
            print("\nShutting down preview server.")


if __name__ == "__main__":
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist/stage")
    target_port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    run_preview_server(target_dir, target_port)
