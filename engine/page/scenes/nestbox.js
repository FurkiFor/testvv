// Nested boxes: the lid pops off, the four walls fall open flat, and there's a
// smaller box inside, which does the same. The fallen walls slide away. Forever.
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

const BOXES = {
  kraft: { label: 'Cardboard', mat: { roughness: 0.9, grain: 220, grainAmt: 0.5, mottle: 4, mottleAmt: 0.3, colorVar: 0.14, bump: 0.004 }, pals: [['#c49a6c', '#b88d5f'], ['#d2b48c', '#c4a27a']], tape: true },
  wood: { label: 'Wooden', mat: { roughness: 0.48, clearcoat: 0.4, clearcoatRoughness: 0.3, vein: true, veinScale: 26, grain: 40, grainAmt: 0.25, mottle: 3, mottleAmt: 0.3, colorVar: 0.2 }, pals: [['#c8925a', '#a8703e'], ['#8a5a3b', '#6b4226'], ['#e0b47c', '#c8925a']], vein: '#5a3620' },
  gift: { label: 'Gift', mat: { roughness: 0.35, clearcoat: 0.7, clearcoatRoughness: 0.2 }, pals: [['#e63946', '#1d3557', '#2a9d8f', '#f4a261'], ['#ff5d8f', '#ffd166', '#06d6a0', '#118ab2'], ['#9b5de5', '#f15bb5', '#fee440', '#00bbf9']], ribbon: true },
  velvet: { label: 'Velvet', mat: { roughness: 0.92, sheen: 1, sheenRoughness: 0.45, mottle: 6, mottleAmt: 0.12, colorVar: 0.08 }, pals: [['#7b1e3a', '#1f3a5f'], ['#2d6a4f', '#5a189a'], ['#9d0208', '#14213d']] },
  lacquer: { label: 'Lacquered', mat: { roughness: 0.12, clearcoat: 1, clearcoatRoughness: 0.03 }, pals: [['#111214', '#b5121b'], ['#0b3d2e', '#e8c36a'], ['#f4f1ea', '#1d3557'], ['#ffb5a7', '#a2d2ff', '#cdb4db', '#b9fbc0']] },
};
const LININGS = ['#f4f1ea', '#e8c36a', '#1d1f24', '#f2d7d9', '#dfe7ee'];
const BG = ['#e9e5df', '#dfe6ea', '#ebe3ea', '#e4e9e1', '#f0e3d3', '#2a2c31'];

const clamp01 = (x) => Math.min(1, Math.max(0, x));
const ease = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };

export default function build({ THREE, rand, pick, range, makeMaterial }) {
  const key = pick(Object.keys(BOXES));
  const K = BOXES[key];
  const pal = pick(K.pals);
  const P = pal.length; // 1, 2 or 4 — divides cycles
  const lining = pick(LININGS);
  const bg = pick(BG);
  const dark = bg === '#2a2c31';
  const r = range(0.6, 0.65);
  const cycles = 4;
  const cycleSec = range(1.8, 2.1);

  const W = 1, H = range(0.62, 0.78), th = 0.035;
  const outer = pal.map((c) => makeMaterial({ ...K.mat, color: c, ...(K.vein ? { veinColor: K.vein } : {}) }));
  const inner = makeMaterial({ color: lining, roughness: 0.7, sheen: 0.5, sheenRoughness: 0.6 });
  const tapeMat = makeMaterial({ color: '#c9a978', roughness: 0.35, clearcoat: 0.6 });
  const ribbonMat = makeMaterial({ color: pick(['#f4f1ea', '#e8c36a', '#c1121f', '#111214']), roughness: 0.3, sheen: 1, sheenRoughness: 0.3, clearcoat: 0.4 });

  // a wall: outer face in the box material, inner face in the lining
  // walls 0 and 2 span the full width; 1 and 3 fit between them
  const wallGeos = [W, W - 2 * th].map((ww) => { const g = new RoundedBoxGeometry(ww, H, th, 2, 0.008); g.translate(0, H / 2, -th / 2); return g; });
  const lineGeo = new THREE.PlaneGeometry(W - 2 * th - 0.004, H - 0.01);
  lineGeo.translate(0, H / 2, 0);
  const lidGeo = new RoundedBoxGeometry(W + 0.05, 0.06, W + 0.05, 2, 0.012);
  const lidRimGeo = new RoundedBoxGeometry(W + 0.05, 0.12, W + 0.05, 2, 0.012);

  function makeCopy(n) {
    const root = new THREE.Group();
    const mat = outer[((n % P) + P) % P];
    // four walls, each hinged at its outer bottom edge
    const walls = [0, 1, 2, 3].map((k) => {
      const yawG = new THREE.Group();
      yawG.rotation.y = (k * Math.PI) / 2;
      const hinge = new THREE.Group();
      hinge.position.set(0, 0, W / 2);
      const w = new THREE.Mesh(wallGeos[k % 2], mat);
      const ln = new THREE.Mesh(lineGeo, inner);
      ln.rotation.y = Math.PI; // faces into the box
      ln.position.z = -th - 0.0015;
      ln.userData.noShadow = true;
      w.add(ln);
      if (K.tape && (k === 0 || k === 2)) {
        const tape = new THREE.Mesh(new THREE.BoxGeometry(0.16, H * 0.55, 0.004), tapeMat);
        tape.position.set(0, H - H * 0.275, 0.002);
        tape.userData.noShadow = true;
        w.add(tape);
      }
      if (K.ribbon) {
        const rb = new THREE.Mesh(new THREE.BoxGeometry(0.1, H, 0.006), ribbonMat);
        rb.position.set(0, H / 2, 0.003);
        rb.userData.noShadow = true;
        w.add(rb);
      }
      hinge.add(w);
      yawG.add(hinge);
      root.add(yawG);
      return { hinge, k };
    });
    // lid with a skirt
    const lid = new THREE.Group();
    const lt = new THREE.Mesh(lidGeo, mat);
    lt.position.y = 0.03;
    const skirt = new THREE.Mesh(lidRimGeo, mat);
    skirt.position.y = -0.03;
    lid.add(skirt, lt);
    if (K.ribbon) {
      const a = new THREE.Mesh(new THREE.BoxGeometry(W + 0.07, 0.1, 0.1), ribbonMat);
      const b2 = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.1, W + 0.07), ribbonMat);
      a.position.y = b2.position.y = 0.02;
      const bow1 = new THREE.Mesh(new THREE.TorusGeometry(0.09, 0.025, 10, 24), ribbonMat);
      bow1.position.set(-0.08, 0.1, 0); bow1.rotation.set(0, 0, 0.5);
      const bow2 = bow1.clone(); bow2.position.x = 0.08; bow2.rotation.z = -0.5;
      lid.add(a, b2, bow1, bow2);
    }
    if (K.tape) {
      const tp = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.004, W + 0.06), tapeMat);
      tp.position.y = 0.062;
      lid.add(tp);
    }
    root.add(lid);

    root.userData.update = (tau) => {
      // lid: pops up, tilts, and flies off up and to the side
      let ly = H + 0.0, lx = 0, rz = 0, rx = 0;
      if (tau > 0) {
        const u = clamp01(tau / 0.22);
        ly += 0.35 * ease(u) + 6 * Math.max(0, tau - 0.18) ** 2 * 3;
        lx = -2.2 * Math.max(0, tau - 0.12) ** 1.5;
        rz = 1.4 * ease((tau - 0.05) / 0.4);
        rx = -0.5 * ease((tau - 0.1) / 0.5);
      }
      lid.position.set(lx, ly + 0.06, 0);
      lid.rotation.set(rx, 0, rz);
      lid.visible = tau < 1.2;
      // walls: fall outward with gravity, small bounce, then slide away
      for (const { hinge, k } of walls) {
        const t0 = 0.2 + 0.035 * k;
        let th2 = 0;
        if (tau > t0) {
          const u = (tau - t0) / 0.3;
          if (u < 1) th2 = (Math.PI / 2) * u * u;
          else {
            const v = u - 1;
            th2 = Math.PI / 2 - 0.1 * Math.exp(-6 * v) * Math.abs(Math.sin(9 * v));
          }
        }
        hinge.rotation.x = th2;
        const su = (tau - 0.62) / 0.5;
        const slide = su <= 0 ? 0 : su < 1 ? 0.9 * su * su : 0.9 + 1.8 * (su - 1);
        hinge.position.set(0, 0, W / 2 + slide);
      }
    };
    return root;
  }

  const notes = [523.25, 587.33, 659.25, 783.99, 880.0];
  const startNote = Math.floor(rand() * 2);
  const seq = Array.from({ length: cycles }, (_, k) => notes[startNote + (k % 4)]);
  const titles = [
    `There's Always Another Box Inside 🔁 #asmr #satisfying`,
    `Opening ${K.label} Boxes Forever 🔁 #asmr`,
    `The Box That Never Runs Out 🔁 #satisfying #asmr`,
    `How Many Boxes Are In Here? 🔁 #asmr`,
    `${K.label} Box Inside A Box Inside A… 🔁 #satisfying`,
    `Unboxing That Never Ends 🔁 #asmr #satisfying`,
    `The Last ${K.label} Box Never Comes 🔁 #asmr`,
  ];
  const caps = [
    `Open the box… there's a smaller one inside. Open that one… It never ends. 🔁`,
    `Lid off, walls down, one more box. Forever. Can you find where it loops? 🔁`,
  ];
  return {
    family: 'nestbox',
    M: { c: new THREE.Vector3(0, 0, 0), r, phi: range(-0.3, 0.3) },
    nMin: -3, nMax: 9,
    cycles, cycleSec,
    bg, fog: [10, 26], envIntensity: dark ? 0.4 : 0.55, keyIntensity: dark ? 2.8 : 2.4,
    camera: { pos: [0.4, 3.3, 4.6], target: [0, 0.32, 0], fov: 31 },
    keyPos: [3, 8, 5], shadowSize: 4,
    makeCopy,
    events: [
      { tau: 0.02, type: 'pop', gain: 0.7, pan: 0 },
      { tau: 0.08, type: 'whoosh', dur: 0.3, gain: 0.35, pan: -0.3, stereoSpread: true },
      { tau: 0.2, type: 'chime', gain: 0.3, pan: 0, pitchSeq: seq },
      { tau: 0.5, type: 'thud', gain: 0.6, pan: 0.0, pitch: 1.2 },
      { tau: 0.535, type: 'thud', gain: 0.55, pan: 0.6, pitch: 1.3 },
      { tau: 0.57, type: 'thud', gain: 0.5, pan: 0.0, pitch: 1.15 },
      { tau: 0.605, type: 'thud', gain: 0.55, pan: -0.6, pitch: 1.25 },
      { tau: 0.64, type: 'slide', dur: 0.5, gain: 0.35, pan: 0 },
    ],
    bed: { type: 'room', gain: 0.05 },
    meta: {
      slug: `${key}-box`,
      title: pick(titles),
      caption: `${pick(caps)}\n\n#asmr #satisfying #oddlysatisfying #unboxing #infiniteloop #shorts`,
      tags: ['asmr', 'satisfying', 'oddly satisfying', 'box in a box', 'unboxing', 'nested boxes', 'infinite loop', 'never ending', 'satisfying video', 'relaxing', '3d animation', 'loop video', 'shorts'],
    },
  };
}
