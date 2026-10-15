// Frame-time benchmark: node bench.mjs <family> <seed> <w> <h> '<quality json>'
import { openScene } from './render.mjs';
const [family = 'cubecut', seed = '7', w = '1080', h = '1920', qj = '{}'] = process.argv.slice(2);
const { frame, renderOnly, close } = await openScene({ family, seed: Number(seed), width: Number(w), height: Number(h), quality: JSON.parse(qj) });
await frame(0.01);
const N = 5;
let t0 = Date.now();
for (let i = 0; i < N; i++) await renderOnly(0.1 + i * 0.13);
const r = (Date.now() - t0) / N;
t0 = Date.now();
for (let i = 0; i < N; i++) await frame(0.1 + i * 0.13);
console.log(`${family} ${w}x${h} ${qj}: render ${r.toFixed(0)} ms, render+encode ${((Date.now() - t0) / N).toFixed(0)} ms`);
await close();
