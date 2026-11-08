
/**
 * Food Code Episode 001 - Millisecond Accurate CDP Timeline Driver
 */

const SCENE_BOUNDS = [
  {
    "id": "scene_001",
    "title": "The Hook",
    "start": 0.0,
    "end": 4.91,
    "duration": 4.91,
    "camera": {
      "movement": "fast_push_in",
      "depth_parallax": true,
      "zoom_start": 1.0,
      "zoom_end": 1.15,
      "easing": "cubic_bezier"
    }
  },
  {
    "id": "scene_002",
    "title": "The Mouth & Starch",
    "start": 4.91,
    "end": 11.52,
    "duration": 6.61,
    "camera": {
      "movement": "pan_right",
      "depth_parallax": true,
      "zoom_start": 1.0,
      "zoom_end": 1.08,
      "easing": "cubic_bezier"
    }
  },
  {
    "id": "scene_003",
    "title": "The Stomach",
    "start": 11.52,
    "end": 18.27,
    "duration": 6.75,
    "camera": {
      "movement": "tilt_down",
      "depth_parallax": true,
      "zoom_start": 1.0,
      "zoom_end": 1.1,
      "easing": "cubic_bezier"
    }
  },
  {
    "id": "scene_004",
    "title": "Small Intestine",
    "start": 18.27,
    "end": 24.64,
    "duration": 6.37,
    "camera": {
      "movement": "pan_left",
      "depth_parallax": true,
      "zoom_start": 1.0,
      "zoom_end": 1.12,
      "easing": "cubic_bezier"
    }
  },
  {
    "id": "scene_005",
    "title": "Nutrient Absorption",
    "start": 24.64,
    "end": 34.18,
    "duration": 9.54,
    "camera": {
      "movement": "fast_push_in",
      "depth_parallax": true,
      "zoom_start": 1.0,
      "zoom_end": 1.14,
      "easing": "cubic_bezier"
    }
  },
  {
    "id": "scene_006",
    "title": "The Sodium Factor",
    "start": 34.18,
    "end": 43.93,
    "duration": 9.75,
    "camera": {
      "movement": "smooth_pull_back",
      "depth_parallax": true,
      "zoom_start": 1.18,
      "zoom_end": 1.0,
      "easing": "cubic_bezier"
    }
  },
  {
    "id": "scene_007",
    "title": "A More Balanced Bowl",
    "start": 43.93,
    "end": 51.67,
    "duration": 7.74,
    "camera": {
      "movement": "subtle_orbit",
      "depth_parallax": true,
      "zoom_start": 1.0,
      "zoom_end": 1.06,
      "easing": "cubic_bezier"
    }
  },
  {
    "id": "scene_008",
    "title": "Final Takeaway",
    "start": 51.67,
    "end": 57.71,
    "duration": 6.04,
    "camera": {
      "movement": "smooth_pull_back",
      "depth_parallax": true,
      "zoom_start": 1.06,
      "zoom_end": 1.0,
      "easing": "cubic_bezier"
    }
  }
];
const TOTAL_DURATION = 57.46;

let currentTime = 0.0;
let isPlaying = false;
let audioElem = null;

function initPlayer() {
  window.setSeekTime = setSeekTime;
  window.getCurrentTime = () => currentTime;
  window.getTotalDuration = () => TOTAL_DURATION;

  // Render initial frame
  setSeekTime(0.0);
}

function setSeekTime(timeInSeconds) {
  currentTime = Math.max(0.0, Math.min(TOTAL_DURATION, timeInSeconds));

  // Determine active scene
  let activeScene = SCENE_BOUNDS[0];
  for (let sc of SCENE_BOUNDS) {
    if (currentTime >= sc.start && currentTime <= sc.end) {
      activeScene = sc;
      break;
    }
  }

  // Update DOM active scene visibility
  SCENE_BOUNDS.forEach(sc => {
    const el = document.getElementById(sc.id);
    if (!el) return;
    if (sc.id === activeScene.id) {
      el.classList.add('active');
    } else {
      el.classList.remove('active');
    }
  });

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
  if (cam.movement === 'pan_right') {
    panX = -45 * easeProgress;
  } else if (cam.movement === 'pan_left') {
    panX = 45 * easeProgress;
  } else if (cam.movement === 'tilt_down') {
    panY = -35 * easeProgress;
  } else if (cam.movement === 'fast_push_in') {
    panY = -20 * easeProgress;
  } else if (cam.movement === 'subtle_orbit') {
    panX = 18 * Math.sin(progress * Math.PI);
    panY = 10 * Math.cos(progress * Math.PI) - 10;
  }

  // Apply parallax to active scene layers
  const midLayer = document.getElementById(activeScene.id + '_mid');
  if (midLayer) {
    midLayer.style.transform = `translate3d(${panX}px, ${panY}px, 0px) scale(${currentZoom.toFixed(4)})`;
  }

  const bgLayer = document.getElementById(activeScene.id + '_bg');
  if (bgLayer) {
    bgLayer.style.transform = `translate3d(${(panX * 0.2).toFixed(2)}px, ${(panY * 0.2).toFixed(2)}px, -200px) scale(${(1.0 + (currentZoom - 1.0) * 0.2).toFixed(4)})`;
  }

  const fgLayer = document.getElementById(activeScene.id + '_fg');
  if (fgLayer) {
    fgLayer.style.transform = `translate3d(${(panX * 1.4).toFixed(2)}px, ${(panY * 1.4).toFixed(2)}px, 150px) scale(${(1.0 + (currentZoom - 1.0) * 1.4).toFixed(4)})`;
  }
}

document.addEventListener('DOMContentLoaded', initPlayer);
