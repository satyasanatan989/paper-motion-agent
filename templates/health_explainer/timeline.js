/**
 * Timeline Controller & Procedural Parchment Generator
 * Supports real-time playback and headless frame-by-frame CDP rendering via window.setSeekTime(t)
 */

(function () {
  // --- 1. Procedural Aged Parchment Generator ---
  function initParchment() {
    const canvas = document.getElementById('parchment-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    // Base parchment tone
    const grad = ctx.createRadialGradient(w / 2, h / 2, 200, w / 2, h / 2, 1000);
    grad.addColorStop(0, '#FAF2E4');
    grad.addColorStop(0.5, '#F3E5CE');
    grad.addColorStop(0.85, '#E2D1B3');
    grad.addColorStop(1, '#CBB896');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    // Procedural organic speckles & fibers
    const rng = (function (seed) {
      return function () {
        seed = (seed * 9301 + 49297) % 233280;
        return seed / 233280;
      };
    })(42);

    ctx.fillStyle = 'rgba(100, 70, 40, 0.04)';
    for (let i = 0; i < 15000; i++) {
      const x = rng() * w;
      const y = rng() * h;
      const r = rng() * 1.8;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }

    // Aged tea-stain blotches
    for (let i = 0; i < 20; i++) {
      const bx = rng() * w;
      const by = rng() * h;
      const br = 80 + rng() * 220;
      const bGrad = ctx.createRadialGradient(bx, by, 0, bx, by, br);
      bGrad.addColorStop(0, 'rgba(120, 85, 45, 0.06)');
      bGrad.addColorStop(0.6, 'rgba(120, 85, 45, 0.02)');
      bGrad.addColorStop(1, 'rgba(120, 85, 45, 0)');
      ctx.fillStyle = bGrad;
      ctx.beginPath();
      ctx.arc(bx, by, br, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  initParchment();

  // --- 2. Chapter Timeline Configuration ---
  // Verified chapter boundaries synchronized with 62.60s Hinglish narration
  let chapters = [
    {
      id: 1,
      start: 0.0,
      end: 9.43,
      sceneId: 'scene-1',
      caption: 'पिज़्ज़ा, समोसा या भटूरे खाते ही मज़ा तो बहुत आता है, लेकिन कुछ घंटों बाद सीने में जलन और heavy acidity क्यों होती है?',
      keywords: ['पिज़्ज़ा', 'समोसा', 'भटूरे', 'सीने में जलन', 'heavy acidity', 'Pizza', 'samosa']
    },
    {
      id: 2,
      start: 9.88,
      end: 20.39,
      sceneId: 'scene-2',
      caption: 'Whole wheat grain में तीन parts होते हैं: bran, germ और endosperm. लेकिन मैदा बनाते वक्त सारा fiber strip कर दिया जाता है।',
      keywords: ['Whole wheat grain', 'bran', 'germ', 'endosperm', 'fiber strip', 'मैदा']
    },
    {
      id: 3,
      start: 20.84,
      end: 30.30,
      sceneId: 'scene-3',
      caption: 'पेट में जाते ही यह refined starch पानी के साथ मिलकर एक sticky glue बनाता है, जो stomach lining पर बुरी तरह चिपक जाता है।',
      keywords: ['refined starch', 'sticky glue', 'stomach lining', 'चिपक जाता है', 'glue']
    },
    {
      id: 4,
      start: 30.75,
      end: 41.21,
      sceneId: 'scene-4',
      caption: 'इस glue को तोड़ने के लिए पेट को extreme Hydrochloric Acid release करना पड़ता है, जो ऊपर आकर severe acidity और heartburn बनाता है।',
      keywords: ['Hydrochloric Acid', 'severe acidity', 'heartburn', 'acid reflux', 'HCl']
    },
    {
      id: 5,
      start: 41.66,
      end: 51.17,
      sceneId: 'scene-5',
      caption: 'Normal fiber twenty-four hours में digest हो जाता है, लेकिन मैदा fifty hours से भी ज़्यादा समय तक intestines में अटका रहता है।',
      keywords: ['Normal fiber', 'twenty-four hours', 'fifty hours', 'intestines', 'digest']
    },
    {
      id: 6,
      start: 51.62,
      end: 62.60,
      sceneId: 'scene-6',
      caption: 'तो अगली बार भटूरे खाने से पहले सोचना, यह स्वाद सिर्फ दस सेकंड जीभ का है, लेकिन अंदर यह आपके पेट का सबसे बड़ा दुश्मन है।',
      keywords: ['दस सेकंड', 'पेट का सबसे बड़ा दुश्मन', 'भटूरे', 'दुश्मन', 'स्वाद']
    }
  ];

  // Attempt to load live timestamps.json if served
  fetch('../output/timestamps.json')
    .then(r => r.json())
    .then(data => {
      if (data && data.chapters) {
        data.chapters.forEach((ch, idx) => {
          if (chapters[idx]) {
            chapters[idx].start = ch.start;
            chapters[idx].end = ch.end;
            chapters[idx].caption = ch.text;
          }
        });
        console.log("✔ Timestamps synchronized with IndicF5 narration:", chapters);
      }
    })
    .catch(() => {});

  // --- 3. Animation Driver & Frame-Accurate Seek Function ---
  const captionBox = document.getElementById('caption-box');
  const scenes = document.querySelectorAll('.scene');

  function highlightKeywords(text, keywords) {
    let res = text;
    keywords.forEach(kw => {
      const reg = new RegExp(`(${kw})`, 'gi');
      res = res.replace(reg, '<span class="highlight">$1</span>');
    });
    return res;
  }

  window.setSeekTime = function (t) {
    // 1. Identify active chapter
    let currentChapter = chapters[0];
    for (let i = 0; i < chapters.length; i++) {
      if (t >= chapters[i].start && t <= chapters[i].end) {
        currentChapter = chapters[i];
        break;
      }
      if (t > chapters[chapters.length - 1].end) {
        currentChapter = chapters[chapters.length - 1];
      }
    }

    // 2. Switch Active Scene
    scenes.forEach(s => {
      if (s.id === currentChapter.sceneId) {
        if (!s.classList.contains('active')) s.classList.add('active');
      } else {
        s.classList.remove('active');
      }
    });

    // 3. Update Subtitles with Highlights
    if (captionBox) {
      captionBox.innerHTML = highlightKeywords(currentChapter.caption, currentChapter.keywords);
    }

    // 4. Scene-Specific Motion Graphics Interpolation
    const relT = t - currentChapter.start;
    const progress = Math.min(1.0, Math.max(0.0, relT / (currentChapter.end - currentChapter.start)));

    // Scene 1: Heartburn Flame Pulse & Samosa Sizzle
    const flame = document.getElementById('s1-flame');
    if (flame) {
      const flameScale = 1.0 + 0.12 * Math.sin(t * 8.0);
      const flameY = -10 * Math.sin(t * 4.0);
      flame.style.transform = `translate(340px, ${20 + flameY}px) scale(${flameScale})`;
    }

    // Scene 2: Wheat Peeling & Stripping
    const bran = document.getElementById('s2-bran');
    const germ = document.getElementById('s2-germ');
    if (bran && germ) {
      const peelX = progress * 40;
      bran.style.transform = `translate(${140 - peelX}px, 40px) scale(${1.0 - progress * 0.08})`;
      germ.style.transform = `translate(${140 + peelX}px, 40px) scale(${1.0 - progress * 0.08})`;
    }

    // Scene 3: Gut Glue Adhesion Wave
    const gluePaste = document.getElementById('s3-glue-paste');
    if (gluePaste) {
      const stretch = 1.0 + 0.08 * Math.sin(t * 5.0);
      gluePaste.style.transform = `scaleY(${stretch})`;
    }

    // Scene 4: Acid Level Rising & Bubbles
    const acidPool = document.getElementById('s4-acid-pool');
    if (acidPool) {
      const acidRise = Math.min(60, progress * 70);
      acidPool.style.transform = `translateY(${-acidRise}px)`;
    }

    // Scene 5: Mechanical Flip Counter
    const f1 = document.getElementById('s5-f1');
    const f2 = document.getElementById('s5-f2');
    if (f1 && f2) {
      const countHours = Math.floor(24 + progress * 30);
      const strH = String(countHours).padStart(2, '0');
      f1.textContent = strH[0];
      f2.textContent = strH[1];
    }
  };

  // Expose total duration
  window.getVideoDuration = function () {
    return chapters[chapters.length - 1].end;
  };

})();
