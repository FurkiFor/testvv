// Render one seamless loop video (or still previews) with headless Chromium.
//   node render.mjs --family cubecut --seed 42 --out out/test.mp4 [--fps 30]
//   node render.mjs --family cubecut --seed 42 --preview out/prev --at 0,0.5,1
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
process.env.PLAYWRIGHT_BROWSERS_PATH ??= fs.existsSync('/opt/pw-browsers') ? '/opt/pw-browsers' : undefined;
const { chromium } = await import('playwright');

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json' };

function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const u = decodeURIComponent(new URL(req.url, 'http://x').pathname);
      const file = u.startsWith('/node_modules/') ? path.join(ROOT, u) : path.join(ROOT, 'page', u === '/' ? 'index.html' : u);
      if (!file.startsWith(ROOT) || !fs.existsSync(file)) { res.writeHead(404); return res.end(); }
      res.writeHead(200, { 'content-type': TYPES[path.extname(file)] ?? 'application/octet-stream' });
      fs.createReadStream(file).pipe(res);
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}

function run(cmd, args, opts = {}) {
  return new Promise((resolve, reject) => {
    const p = spawn(cmd, args, { stdio: ['ignore', 'inherit', 'inherit'], ...opts });
    p.on('exit', (c) => (c === 0 ? resolve() : reject(new Error(`${cmd} exited ${c}`))));
  });
}

export async function openScene({ family, seed, width = 1080, height = 1920, quality }) {
  const srv = await serve();
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width, height } });
  page.on('pageerror', (e) => console.error('[page]', e.message));
  page.on('console', (m) => { if (m.type() === 'error') console.error('[console]', m.text()); });
  await page.goto(`http://127.0.0.1:${srv.address().port}/index.html`);
  await page.waitForFunction(() => window.engineReady === true);
  const info = await page.evaluate((c) => window.setup(c), { family, seed, width, height, quality });
  const close = async () => { await browser.close(); srv.close(); };
  const frame = async (T, q = 0.92) => {
    const url = await page.evaluate(([t, qq]) => window.renderFrame(t, qq), [T, q]);
    return Buffer.from(url.slice(url.indexOf(',') + 1), 'base64');
  };
  const renderOnly = (T) => page.evaluate((t) => window.renderOnly(t), T);
  return { info, frame, renderOnly, close };
}

// Frames render at 720x1280 (software WebGL is fill-bound) and are upscaled to
// 1080x1920 with Lanczos + light sharpening for a full-HD Shorts upload.
export async function renderVideo({ family, seed, out, fps = 30, width = 720, height = 1280, outW = 1080, outH = 1920, log = console.log }) {
  const t0 = Date.now();
  const { info, frame, close } = await openScene({ family, seed, width, height });
  const total = info.cycles * info.cycleSec;
  const frames = Math.round(total * fps);
  const dur = frames / fps;
  const tmpDir = fs.mkdtempSync(path.join(path.dirname(out), '.tmp-'));
  const silent = path.join(tmpDir, 'v.mp4');
  const wav = path.join(tmpDir, 'a.wav');

  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(fps), '-i', '-',
    '-vf', `scale=${outW}:${outH}:flags=lanczos,unsharp=5:5:0.6:5:5:0`,
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-maxrate', '10M', '-bufsize', '20M', '-pix_fmt', 'yuv420p', '-r', String(fps), silent],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const ffDone = new Promise((res, rej) => ff.on('exit', (c) => (c === 0 ? res() : rej(new Error('ffmpeg encode failed')))));
  for (let i = 0; i < frames; i++) {
    const T = (i / frames) * info.cycles;
    const buf = await frame(T, 0.93);
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 60 === 0) log(`  ${family} frame ${i}/${frames} (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
  }
  ff.stdin.end();
  await ffDone;
  await close();

  // Audio: synthesized from the scene's event list, circular so it loops too.
  const spec = { duration: dur, cycles: info.cycles, cycleSec: dur / info.cycles, events: info.events, bed: info.bed, seed };
  const specFile = path.join(tmpDir, 'audio.json');
  fs.writeFileSync(specFile, JSON.stringify(spec));
  await run('python3', ['-I', path.join(ROOT, 'audio.py'), specFile, wav]);
  await run('ffmpeg', ['-y', '-v', 'error', '-i', silent, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', '-movflags', '+faststart', out]);
  fs.rmSync(tmpDir, { recursive: true, force: true });
  log(`  ${family} done: ${out} (${dur.toFixed(2)}s, ${frames} frames, ${((Date.now() - t0) / 1000).toFixed(0)}s)`);
  return { ...info, duration: dur, frames };
}

// CLI
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const a = Object.fromEntries(process.argv.slice(2).join(' ').split('--').filter(Boolean).map((s) => { const [k, ...v] = s.trim().split(' '); return [k, v.join(' ')]; }));
  const family = a.family, seed = Number(a.seed ?? 1);
  if (a.preview) {
    fs.mkdirSync(a.preview, { recursive: true });
    const { info, frame, close } = await openScene({ family, seed });
    console.log(JSON.stringify(info.meta), 'cycles', info.cycles, 'cycleSec', info.cycleSec.toFixed(2));
    for (const t of (a.at ?? '0,0.25,0.5,0.75,1').split(',').map(Number)) {
      fs.writeFileSync(path.join(a.preview, `${family}-${seed}-${t}.jpg`), await frame(t, 0.9));
    }
    await close();
  } else {
    fs.mkdirSync(path.dirname(a.out), { recursive: true });
    await renderVideo({ family, seed, out: a.out, fps: Number(a.fps ?? 30) });
  }
}
