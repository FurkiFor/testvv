// Domino spiral: dominoes on a logarithmic spiral topple inward, each one smaller
// than the last. The camera follows the wave, so it never reaches the centre.
const STYLES = {
  gloss: { label: 'Glossy', mat: { roughness: 0.2, clearcoat: 1, clearcoatRoughness: 0.06 } },
  wood: { label: 'Wooden', mat: { roughness: 0.55, grain: 9, grainAmt: 0.35, mottle: 1.5, mottleAmt: 0.3, colorVar: 0.22, bump: 0.002 }, wood: true },
  matte: { label: 'Pastel', mat: { roughness: 0.7, sheen: 0.4 } },
  metal: { label: 'Metal', mat: { roughness: 0.22, metalness: 1 } },
};
const GRADS = [
  ['#ff4d6d', '#ffd23f'], ['#3a86ff', '#ff006e'], ['#06d6a0', '#118ab2'], ['#8338ec', '#ffbe0b'],
  ['#f72585', '#4cc9f0'], ['#e76f51', '#2a9d8f'], ['#ffadad', '#9bf6ff'],
];
const WOODS = [['#c8925a', '#8c5a32'], ['#e0b47c', '#a8703e']];
const BG = ['#ece8e1', '#e1e6ec', '#ebe4ea', '#22252b', '#e6ebe2'];

const clamp01 = (x) => Math.min(1, Math.max(0, x));
const ease = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };

export default function build({ THREE, rand, pick, range, makeMaterial }) {
  const styleKey = pick(Object.keys(STYLES));
  const S = STYLES[styleKey];
  const grad = S.wood ? pick(WOODS) : pick(GRADS);
  const bg = pick(BG);
  const dark = bg === '#22252b';
  const perTurn = Math.floor(range(14, 19));
  const phi = (2 * Math.PI) / perTurn;
  const r = range(0.95, 0.962);
  const cycleSec = range(0.21, 0.26);
  const cycles = Math.round(10 / cycleSec / 6) * 6; // multiple of 6, ~10 s
  const P = pick([cycles, cycles / 2, cycles / 3]);

  const ca = new THREE.Color(grad[0]), cb = new THREE.Color(grad[1]);
  const mats = Array.from({ length: P }, (_, i) => {
    const t = 0.5 - 0.5 * Math.cos((2 * Math.PI * i) / P);
    return makeMaterial({ ...S.mat, color: '#' + ca.clone().lerp(cb, t).getHexString() });
  });

  const h = 0.5, w = 0.24, t = 0.066;
  const p0 = new THREE.Vector3(1, 0, 0);
  const p1 = new THREE.Vector3(r * Math.cos(phi), 0, -r * Math.sin(phi));
  const d = p1.clone().sub(p0);
  const yaw = Math.atan2(d.x, d.z);
  const gap = d.length() - t;
  const thC = Math.asin(Math.min(0.98, gap / h));
  const thR = 1.25;
  const geo = new THREE.BoxGeometry(w, h, t);
  geo.translate(0, h / 2, -t / 2); // pivot at front-bottom edge

  function makeCopy(n) {
    const root = new THREE.Group();
    const yawG = new THREE.Group();
    yawG.position.copy(p0).addScaledVector(d.clone().normalize(), t / 2);
    yawG.rotation.y = yaw;
    const mesh = new THREE.Mesh(geo, mats[((n % P) + P) % P]);
    yawG.add(mesh);
    root.add(yawG);
    root.userData.update = (tau) => {
      let th = 0;
      if (tau > 0) th = tau < 1 ? thC * tau * tau : thC + (thR - thC) * ease((tau - 1) / 1.2);
      mesh.rotation.x = th;
    };
    return root;
  }

  const seq = Array.from({ length: cycles }, () => range(0.88, 1.14));
  const titles = [
    `Dominoes That Never Stop Falling 🔁 #asmr #satisfying`,
    `The Infinite Domino Spiral 🔁 #satisfying #asmr`,
    `This Domino Spiral Has No End 🔁 #asmr`,
    `${S.label} Dominoes Falling Forever 🔁 #satisfying`,
  ];
  const caps = [
    `Every domino is smaller than the last. The centre never comes. How long can you watch? 🔁`,
    `They keep falling. Smaller and smaller… forever. Watch till the end — there is no end. 🔁`,
  ];
  return {
    family: 'dominospiral',
    M: { c: new THREE.Vector3(0, 0, 0), r, phi },
    nMin: -40, nMax: 135, minScale: 3e-3,
    cycles, cycleSec,
    bg, fog: [9, 20], envIntensity: dark ? 0.45 : 0.6, keyIntensity: dark ? 2.8 : 2.3,
    camera: { pos: [0.2, 7.9, 5.0], target: [0.05, 0, 0.1], fov: 36 },
    keyPos: [2.5, 8, 3.5], shadowSize: 4,
    makeCopy,
    events: [
      { tau: 1.0, type: 'clack', gain: 0.8, pan: 0, pitchSeq: seq, panOrbit: phi },
      { tau: 1.85, type: 'tick', gain: 0.18, pan: 0, pitch: 0.8, pitchSeq: seq },
    ],
    bed: { type: 'room', gain: 0.05 },
    meta: {
      slug: `${styleKey}-domino`,
      title: pick(titles),
      caption: `${pick(caps)}\n\n#asmr #satisfying #oddlysatisfying #dominoes #infiniteloop #shorts`,
      tags: ['asmr', 'satisfying', 'oddly satisfying', 'dominoes', 'domino spiral', 'domino effect', 'infinite loop', 'never ending', 'satisfying video', 'relaxing', '3d animation', 'loop video', 'shorts'],
    },
  };
}
