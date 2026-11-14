// Spiral stairs: a ball bounces down a floating spiral staircase of pillars that
// descends into the void, each step smaller and lower than the last, curling
// inward forever. The fixed point sits below the steps, so each step drops a
// visible amount. The ball shrinks with the steps, so every bounce looks the same.
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

const STEPS = {
  marble: { label: 'Marble', mat: { roughness: 0.16, clearcoat: 0.9, clearcoatRoughness: 0.08, vein: true, veinScale: 9, mottle: 4, mottleAmt: 0.15, colorVar: 0.08 }, pals: [['#f2efe9', '#5b6066'], ['#1d1f22', '#d8d4cc'], ['#2f4a3e', '#e6efe8']], vein: true },
  wood: { label: 'Wooden', mat: { roughness: 0.5, clearcoat: 0.35, clearcoatRoughness: 0.3, vein: true, veinScale: 30, grain: 50, grainAmt: 0.25, mottle: 3, mottleAmt: 0.3, colorVar: 0.2 }, pals: [['#c8925a', '#6b4226'], ['#e0b47c', '#8c5a32'], ['#8a5a3b', '#4a2c1a']], vein: true },
  concrete: { label: 'Concrete', mat: { roughness: 0.85, grain: 160, grainAmt: 0.6, mottle: 3, mottleAmt: 0.45, colorVar: 0.22, bump: 0.01, roughVar: 0.15 }, pals: [['#b9b6b0'], ['#8d9095'], ['#c9bfb2']] },
  candy: { label: 'Rainbow', mat: { roughness: 0.18, clearcoat: 1, clearcoatRoughness: 0.05 }, grads: [['#ff4d6d', '#ffd23f'], ['#3a86ff', '#ff006e'], ['#06d6a0', '#118ab2'], ['#8338ec', '#ffbe0b'], ['#f72585', '#4cc9f0']] },
  pastel: { label: 'Pastel', mat: { roughness: 0.65, sheen: 0.5, sheenRoughness: 0.7 }, grads: [['#ffadad', '#9bf6ff'], ['#cdb4db', '#ffc8dd'], ['#bde0fe', '#ffd6a5'], ['#caffbf', '#ffc6ff']] },
};
const BALLS = {
  chrome: { label: 'Chrome', mat: { color: '#d9dce1', roughness: 0.05, metalness: 1 } },
  gold: { label: 'Gold', mat: { color: '#e8c36a', roughness: 0.12, metalness: 1 } },
  rubber: { label: 'Bouncy', mat: { roughness: 0.45, clearcoat: 0.6, clearcoatRoughness: 0.3 }, colors: ['#ff3b30', '#ff9500', '#34c759', '#007aff', '#af52de', '#ff2d55'] },
  pearl: { label: 'Pearl', mat: { color: '#f3eee7', roughness: 0.25, clearcoat: 0.9, sheen: 1, sheenRoughness: 0.3 } },
  glossy: { label: 'Glossy', mat: { roughness: 0.06, clearcoat: 1, clearcoatRoughness: 0.02 }, colors: ['#111214', '#f4f4f2', '#e63946', '#1d3557'] },
};
const BG = ['#ece8e1', '#e1e6ec', '#ebe4ea', '#e6ebe2', '#f1e6d6', '#22252b', '#1c1f2b'];

export default function build({ THREE, rand, pick, range, makeMaterial }) {
  const stepKey = pick(Object.keys(STEPS));
  const S = STEPS[stepKey];
  const ballKey = pick(Object.keys(BALLS));
  const B = BALLS[ballKey];
  const bg = pick(BG);
  const dark = bg === '#22252b' || bg === '#1c1f2b';

  const perTurn = Math.floor(range(11, 15));
  const phi = (2 * Math.PI) / perTurn;
  const r = range(0.93, 0.945);
  const cycleSec = range(0.42, 0.5);
  const cycles = Math.round(10 / cycleSec / 6) * 6;
  const P = S.grads ? pick([cycles, cycles / 2]) : 6;

  // step colours: gradient around the cycle, or a stone/wood with veins
  let mats;
  if (S.grads) {
    const g = pick(S.grads);
    const ca = new THREE.Color(g[0]), cb = new THREE.Color(g[1]);
    mats = Array.from({ length: P }, (_, i) => {
      const t = 0.5 - 0.5 * Math.cos((2 * Math.PI * i) / P);
      return makeMaterial({ ...S.mat, color: '#' + ca.clone().lerp(cb, t).getHexString() });
    });
  } else {
    const pal = pick(S.pals);
    const base = new THREE.Color(pal[0]);
    mats = Array.from({ length: P }, (_, i) => makeMaterial({
      ...S.mat,
      color: '#' + base.clone().offsetHSL(0, 0, (i % 2 ? -1 : 1) * 0.025).getHexString(),
      ...(S.vein ? { veinColor: pal[1] } : {}),
    }));
  }
  const ballColor = B.colors ? pick(B.colors) : B.mat.color;
  const ballMat = makeMaterial({ ...B.mat, color: ballColor });

  // Step n sits at radius 1 (angle 0); step n+1 is M(step n).
  const L = range(1.6, 2.2); // depth of the fixed point below the step tops
  const top = 0; // step tops at y=0 in copy-0 space; the fixed point is at y=-L
  const colLen = 0.13; // thin floating slabs
  const p0 = new THREE.Vector3(1, 0, 0);
  const p1 = new THREE.Vector3(r * Math.cos(phi), 0, -r * Math.sin(phi));
  const chord = p1.distanceTo(p0);
  const depth = chord * 1.04, width = 0.36;
  const yaw = Math.atan2(p1.x - p0.x, p1.z - p0.z);
  const stepGeo = new RoundedBoxGeometry(width, colLen, depth, 2, 0.012);
  stepGeo.translate(0, -colLen / 2, 0);

  const b = 0.11; // ball radius
  const A = new THREE.Vector3(1, top + b, 0);
  // M about (0,-L,0): y -> -L + r (y + L)
  const Bp = new THREE.Vector3(r * Math.cos(phi), -L + r * (top + b + L), -r * Math.sin(phi));
  const hop = range(0.16, 0.24);
  const ballGeo = new THREE.SphereGeometry(b, 40, 28);
  const dir = Bp.clone().sub(A).setY(0).normalize();
  const spinAxis = new THREE.Vector3(0, 1, 0).cross(dir).normalize();
  const roll = (chord / b) * 0.9;

  function makeCopy(n) {
    const root = new THREE.Group();
    const step = new THREE.Mesh(stepGeo, mats[((n % P) + P) % P]);
    step.position.copy(p0);
    step.rotation.y = yaw;
    root.add(step);
    const ball = new THREE.Mesh(ballGeo, ballMat);
    root.add(ball);
    root.userData.update = (tau) => {
      if (tau < 0 || tau >= 1) { ball.visible = false; return; }
      ball.visible = true;
      const u = tau;
      ball.position.lerpVectors(A, Bp, u);
      ball.position.y += hop * 4 * u * (1 - u);
      // squash a little right after leaving and before landing
      const s = Math.pow(r, u);
      const sq = 1 - 0.12 * Math.max(0, 1 - u / 0.06) - 0.12 * Math.max(0, 1 - (1 - u) / 0.04);
      ball.scale.set(s / Math.sqrt(sq), s * sq, s / Math.sqrt(sq));
      ball.position.y -= b * s * (1 - sq);
      ball.quaternion.setFromAxisAngle(spinAxis, roll * u);
    };
    return root;
  }

  const seq = Array.from({ length: cycles }, () => range(0.9, 1.12));
  const word = S.label;
  const titles = [
    `The Staircase That Never Ends 🔁 #asmr #satisfying`,
    `${word} Stairs Into Infinity 🔁 #asmr`,
    `This Ball Will Never Reach The Bottom 🔁 #satisfying #asmr`,
    `Bouncing Down Forever 🔁 #asmr #satisfying`,
    `Endless ${word} Spiral Staircase 🔁 #satisfying`,
    `How Many Steps Are There? 🔁 #asmr`,
    `${B.label} Ball vs Infinite Stairs 🔁 #asmr #satisfying`,
    `The Bottom Step Doesn't Exist 🔁 #asmr`,
  ];
  const caps = [
    `Every step is smaller than the last. The ball keeps bouncing… forever. 🔁`,
    `Down and down and down. There is no last step. How long can you watch? 🔁`,
    `It spirals inward, step after step, and never lands. Can you find the loop? 🔁`,
  ];
  return {
    family: 'spiralstairs',
    M: { c: new THREE.Vector3(0, -L, 0), r, phi },
    nMin: -40, nMax: 150, minScale: 3e-3, maxScale: 5,
    cycles, cycleSec,
    bg, floor: false, fog: [5, 13], envIntensity: dark ? 0.45 : 0.6, keyIntensity: dark ? 2.8 : 2.3,
    camera: { pos: [1.1, 6.2, 3.0], target: [0.3, -0.9, -0.3], fov: 40 },
    cameraVar: { yaw: 0.3 },
    keyPos: [2.5, 8, 3.5], shadowSize: 3.5,
    makeCopy,
    events: [
      { tau: 0.0, type: 'clack', gain: 0.75, pan: 0, pitchSeq: seq, panOrbit: phi },
      { tau: 0.0, type: 'thud', gain: 0.22, pan: 0, pitch: 1.6 },
    ],
    bed: { type: 'room', gain: 0.05 },
    meta: {
      slug: `${stepKey}-stairs`,
      title: pick(titles),
      caption: `${pick(caps)}\n\n#asmr #satisfying #oddlysatisfying #infinitestairs #infiniteloop #shorts`,
      tags: ['asmr', 'satisfying', 'oddly satisfying', 'infinite stairs', 'spiral staircase', 'bouncing ball', 'infinite loop', 'never ending', 'satisfying video', 'relaxing', '3d animation', 'loop video', 'shorts'],
    },
  };
}
