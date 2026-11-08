/**
 * PaperMotion AI - CDP Headless Memory Pipe Video Renderer
 * Streams raw frame buffers from Chrome DevTools Protocol directly into FFmpeg stdin.
 */

const { spawn } = require('child_process');
const http = require('http');
const path = require('path');
const fs = require('fs');

function parseArgs() {
  const args = process.argv.slice(2);
  const params = {
    html: path.resolve(__dirname, '..', 'templates', 'mayank_notebook', 'index.html'),
    audio: null,
    output: path.resolve(__dirname, '..', 'output', 'papermotion_render.mp4'),
    fps: 30,
    duration: 22.31,
    port: 9225,
    width: 1080,
    height: 1920
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--html' && args[i + 1]) params.html = path.resolve(args[++i]);
    else if (args[i] === '--audio' && args[i + 1]) params.audio = path.resolve(args[++i]);
    else if (args[i] === '--output' && args[i + 1]) params.output = path.resolve(args[++i]);
    else if (args[i] === '--fps' && args[i + 1]) params.fps = parseInt(args[++i], 10);
    else if (args[i] === '--duration' && args[i + 1]) params.duration = parseFloat(args[++i]);
    else if (args[i] === '--port' && args[i + 1]) params.port = parseInt(args[++i], 10);
  }
  return params;
}

const params = parseArgs();
const CHROME_PATH = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const tempProfile = path.join(process.env.TEMP || '/tmp', `chrome_papermotion_${Date.now()}`);
const htmlUrl = `file:///${params.html.replace(/\\/g, '/')}?render=1`;

console.log('==================================================');
console.log('   PaperMotion AI - Autonomous CDP Video Engine   ');
console.log('==================================================');
console.log(`Canvas Resolution: ${params.width}x${params.height} (9:16 Vertical)`);
console.log(`Framerate        : ${params.fps} FPS`);
console.log(`Duration         : ${params.duration}s (${Math.floor(params.duration * params.fps)} frames)`);
console.log(`HTML Source      : ${params.html}`);
console.log(`Audio Track      : ${params.audio || 'Muted'}`);
console.log(`Output Video     : ${params.output}`);
console.log('==================================================\n');

async function main() {
  // 1. Launch Chrome Headless
  console.log('[1/4] Launching Headless Chrome Instance...');
  const chromeProc = spawn(CHROME_PATH, [
    `--remote-debugging-port=${params.port}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    `--user-data-dir=${tempProfile}`,
    `--window-size=${params.width},${params.height}`,
    htmlUrl
  ], { stdio: 'ignore' });

  await new Promise(r => setTimeout(r, 2000));

  // 2. Discover WebSocket Debugger Target
  console.log('[2/4] Connecting over Chrome DevTools Protocol (CDP)...');
  let targets = null;
  for (let retry = 0; retry < 5; retry++) {
    try {
      targets = await new Promise((resolve, reject) => {
        http.get(`http://127.0.0.1:${params.port}/json`, res => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => resolve(JSON.parse(data)));
        }).on('error', reject);
      });
      break;
    } catch (e) {
      await new Promise(r => setTimeout(r, 500));
    }
  }

  if (!targets) throw new Error('Could not connect to Chrome debugging endpoint.');
  const pageTarget = targets.find(t => t.type === 'page');
  if (!pageTarget) throw new Error('No page target found.');

  // Check if ws package is available locally or in parent ECC
  let WebSocket;
  try {
    WebSocket = require('ws');
  } catch (e) {
    try {
      WebSocket = require(path.join(__dirname, '..', '..', 'ECC', 'node_modules', 'ws'));
    } catch (e2) {
      throw new Error("Package 'ws' not found. Run 'pnpm install' or 'npm install ws'");
    }
  }

  const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    ws.on('open', resolve);
    ws.on('error', reject);
  });

  let idCounter = 1;
  const pendingRequests = new Map();
  ws.on('message', raw => {
    const msg = JSON.parse(raw);
    if (msg.id && pendingRequests.has(msg.id)) {
      const { resolve, reject } = pendingRequests.get(msg.id);
      pendingRequests.delete(msg.id);
      if (msg.error) reject(msg.error);
      else resolve(msg.result);
    }
  });

  function sendCommand(method, cmdParams = {}) {
    return new Promise((resolve, reject) => {
      const id = idCounter++;
      pendingRequests.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params: cmdParams }));
    });
  }

  await sendCommand('Page.enable');
  await sendCommand('Emulation.setDeviceMetricsOverride', {
    width: params.width,
    height: params.height,
    deviceScaleFactor: 1,
    mobile: false
  });

  // 3. Spawn FFmpeg Pipeline
  console.log('[3/4] Streaming memory frames into FFmpeg encoder...');
  const outDir = path.dirname(params.output);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const ffmpegArgs = [
    '-y',
    '-f', 'image2pipe',
    '-vcodec', 'mjpeg',
    '-r', String(params.fps),
    '-i', 'pipe:0'
  ];

  if (params.audio && fs.existsSync(params.audio)) {
    ffmpegArgs.push('-i', params.audio);
    ffmpegArgs.push('-c:a', 'aac', '-b:a', '192k', '-shortest');
  }

  ffmpegArgs.push(
    '-c:v', 'libx264',
    '-preset', 'fast',
    '-crf', '18',
    '-pix_fmt', 'yuv420p',
    params.output
  );

  const ffmpegProc = spawn('ffmpeg', ffmpegArgs);
  ffmpegProc.stderr.on('data', () => {}); // Keep buffer drained

  const totalFrames = Math.floor(params.duration * params.fps);
  const startTime = Date.now();

  for (let i = 0; i < totalFrames; i++) {
    const t = i / params.fps;
    await sendCommand('Runtime.evaluate', {
      expression: `window.setSeekTime ? window.setSeekTime(${t.toFixed(4)}) : null`
    });

    const res = await sendCommand('Page.captureScreenshot', {
      format: 'jpeg',
      quality: 90
    });

    const buffer = Buffer.from(res.data, 'base64');
    ffmpegProc.stdin.write(buffer);

    if (i % 30 === 0 || i === totalFrames - 1) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      const fpsReal = (i / Math.max(0.1, parseFloat(elapsed))).toFixed(1);
      const pct = Math.floor((i / totalFrames) * 100);
      process.stdout.write(`\r[Rendering] Frame ${i + 1}/${totalFrames} (${pct}%) in ${elapsed}s [${fpsReal} FPS]`);
    }
  }

  ffmpegProc.stdin.end();
  await new Promise(resolve => ffmpegProc.on('close', resolve));
  ws.close();
  chromeProc.kill();

  console.log('\n\n[4/4] Video Render Successfully Completed!');
  console.log(`Saved Deliverable: ${params.output}`);
}

main().catch(err => {
  console.error('\nRender Pipeline Error:', err);
  process.exit(1);
});
