// Frame-time benchmark: node bench.mjs <family> <seed> <w> <h> '<quality json>'
import { openScene } from './render.mjs';
const [family = 'cubecut', seed = '7', w = '720', h = '1280', qj = '{}'] = process.argv.slice(2);
const { frame, close } = await openScene({ family, seed: Number(seed), width: Number(w), height: Number(h), quality: JSON.parse(qj) });
await frame(0.01);
const N = 5;
const t0 = Date.now();
for (let i = 0; i < N; i++) await frame(0.1 + i * 0.13);
console.log(`${family} ${w}x${h} ${qj}: ${((Date.now() - t0) / N).toFixed(0)} ms/frame`);
await close();
