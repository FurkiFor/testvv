// Make the day's videos: distinct scene families, fresh random variations.
//   node daily.mjs [--date 2026-10-16] [--count 3] [--outdir ../videos/asmrvideo] [--dry]
// Writes engine/runs/<date>.json with file names, public URLs, titles, captions
// and tags for scheduling. Re-running skips videos that already exist.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openScene, renderVideo } from './render.mjs';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const FAMILIES = ['cubecut', 'nestshell', 'dominospiral', 'funnelmarbles', 'nestbox', 'spiralstairs'];
// Slot plan (12:00, 17:00, 21:00 Dubai), from channel data 2026-10-19: dominoes and
// marbles get far more views than spheres and cubes, so they run every day. The
// first slot rotates through the other four (Furkan, 2026-11-14).
const ROTATION = ['cubecut', 'spiralstairs', 'nestshell', 'nestbox'];
function familyFor(dayIndex, i) {
  const plan = [ROTATION[((dayIndex % 4) + 4) % 4], 'funnelmarbles', 'dominospiral'];
  return i < plan.length ? plan[i] : FAMILIES[(dayIndex + i) % FAMILIES.length];
}
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

// titles used in the last two weeks, and styles (material slug) used in the last
// STYLE_DAYS days, to avoid repeats
const STYLE_DAYS = 6;
const recent = new Set();
const recentStyles = new Set();
const runFiles = fs.readdirSync(runsDir).filter((f) => f.endsWith('.json') && f < `${date}.json`).sort();
runFiles.slice(-14).forEach((f, idx, arr) => {
  try {
    for (const v of JSON.parse(fs.readFileSync(path.join(runsDir, f))).videos) {
      recent.add(v.title);
      if (idx >= arr.length - STYLE_DAYS) recentStyles.add(v.file.replace(/^\d{4}-\d{2}-\d{2}-\d+-/, '').replace(/\.mp4$/, ''));
    }
  } catch {}
});

const dayIndex = Math.round((Date.parse(date) - Date.parse('2026-01-01')) / 864e5);
const manifestPath = path.join(runsDir, `${date}.json`);
const manifest = fs.existsSync(manifestPath) ? JSON.parse(fs.readFileSync(manifestPath)) : { date, videos: [] };

const todayMats = new Set(); // material word (slug prefix) already used in another slot today
for (let i = 0; i < count; i++) {
  const family = familyFor(dayIndex, i);
  if (manifest.videos[i] && fs.existsSync(path.join(outdir, manifest.videos[i].file))) {
    console.log(`skip ${manifest.videos[i].file} (exists)`);
    todayMats.add(manifest.videos[i].file.replace(/^\d{4}-\d{2}-\d{2}-\d+-/, '').split('-')[0]);
    continue;
  }
  // Prefer a seed whose style and title are both fresh; fall back to a fresh title.
  const base = fnv(`${date}#${i}`);
  let seed = base, meta, fallback = null;
  for (let attempt = 0; attempt < 16; attempt++) {
    const cand = (base + attempt * 7919) >>> 0;
    const s = await openScene({ family, seed: cand, width: 64, height: 114 });
    const m = s.info.meta;
    await s.close();
    if (recent.has(m.title)) continue;
    if (!fallback) fallback = { seed: cand, meta: m };
    if (!recentStyles.has(m.slug) && !todayMats.has(m.slug.split('-')[0])) { seed = cand; meta = m; break; }
  }
  if (!meta) ({ seed, meta } = fallback ?? { seed: base, meta: (await (async () => { const s = await openScene({ family, seed: base, width: 64, height: 114 }); const m = s.info.meta; await s.close(); return m; })()) });
  recentStyles.add(meta.slug);
  todayMats.add(meta.slug.split('-')[0]);
  recent.add(meta.title);
  const file = `${date}-${i + 1}-${meta.slug}.mp4`;
  console.log(`[${i + 1}/${count}] ${family} seed=${seed} -> ${file}`);
  if ('dry' in args) continue; // --dry: show the day's picks without rendering
  const res = await renderVideo({ family, seed, out: path.join(outdir, file) });
  manifest.videos[i] = {
    file, url: RAW + file, family, seed,
    title: meta.title, caption: meta.caption, tags: meta.tags,
    duration: Number(res.duration.toFixed(2)),
    sizeMB: Number((fs.statSync(path.join(outdir, file)).size / 1048576).toFixed(2)),
  };
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
}
if (!('dry' in args)) console.log(`DONE ${manifestPath}`);
