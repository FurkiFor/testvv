// Make the day's videos: distinct scene families, fresh random variations.
//   node daily.mjs [--date 2026-10-16] [--count 3] [--outdir ../videos/asmrvideo]
// Writes engine/runs/<date>.json with file names, public URLs, titles, captions
// and tags for scheduling. Re-running skips videos that already exist.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openScene, renderVideo } from './render.mjs';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const FAMILIES = ['cubecut', 'nestshell', 'dominospiral', 'funnelmarbles'];
const RAW = 'https://raw.githubusercontent.com/FurkiFor/testvv/main/videos/asmrvideo/';

const args = Object.fromEntries(process.argv.slice(2).join(' ').split('--').filter(Boolean)
  .map((s) => { const [k, ...v] = s.trim().split(' '); return [k, v.join(' ')]; }));
const dubaiToday = new Date(Date.now() + 4 * 3600e3).toISOString().slice(0, 10);
const date = args.date || dubaiToday;
const count = Number(args.count || 3);
const outdir = path.resolve(ROOT, args.outdir || '../videos/asmrvideo');
const runsDir = path.join(ROOT, 'runs');
fs.mkdirSync(outdir, { recursive: true });
fs.mkdirSync(runsDir, { recursive: true });

function fnv(str) { let h = 2166136261; for (const c of str) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; }

// titles used in the last two weeks, to avoid repeats
const recent = new Set();
for (const f of fs.readdirSync(runsDir).filter((f) => f.endsWith('.json')).sort().slice(-14)) {
  try { for (const v of JSON.parse(fs.readFileSync(path.join(runsDir, f))).videos) recent.add(v.title); } catch {}
}

const dayIndex = Math.round((Date.parse(date) - Date.parse('2026-01-01')) / 864e5);
const manifestPath = path.join(runsDir, `${date}.json`);
const manifest = fs.existsSync(manifestPath) ? JSON.parse(fs.readFileSync(manifestPath)) : { date, videos: [] };

for (let i = 0; i < count; i++) {
  const family = FAMILIES[(dayIndex + i) % FAMILIES.length];
  if (manifest.videos[i] && fs.existsSync(path.join(outdir, manifest.videos[i].file))) {
    console.log(`skip ${manifest.videos[i].file} (exists)`);
    continue;
  }
  let seed = fnv(`${date}#${i}`), meta;
  for (let attempt = 0; attempt < 6; attempt++) {
    const s = await openScene({ family, seed, width: 64, height: 114 });
    meta = s.info.meta;
    await s.close();
    if (!recent.has(meta.title)) break;
    seed = (seed + 7919) >>> 0;
  }
  recent.add(meta.title);
  const file = `${date}-${i + 1}-${meta.slug}.mp4`;
  console.log(`[${i + 1}/${count}] ${family} seed=${seed} -> ${file}`);
  const res = await renderVideo({ family, seed, out: path.join(outdir, file) });
  manifest.videos[i] = {
    file, url: RAW + file, family, seed,
    title: meta.title, caption: meta.caption, tags: meta.tags,
    duration: Number(res.duration.toFixed(2)),
    sizeMB: Number((fs.statSync(path.join(outdir, file)).size / 1048576).toFixed(2)),
  };
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
}
console.log(`DONE ${manifestPath}`);
