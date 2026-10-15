// Nested shell: a hollow sphere cracks, its halves roll open into rocking bowls
// and slide away, revealing a smaller sphere inside, which does the same. Forever.
const SHELLS = {
  ceramic: { label: 'Ceramic', mat: { roughness: 0.22, clearcoat: 1, clearcoatRoughness: 0.08 } },
  pearl: { label: 'Pearl', mat: { roughness: 0.3, clearcoat: 0.7, sheen: 1, sheenRoughness: 0.35, sheenColor: '#ffffff' } },
  chrome: { label: 'Chrome', mat: { roughness: 0.08, metalness: 1 } },
  matte: { label: 'Soft Touch', mat: { roughness: 0.62, sheen: 0.6, sheenRoughness: 0.8, mottle: 3, mottleAmt: 0.15, colorVar: 0.06 } },
  candy: { label: 'Candy', mat: { roughness: 0.1, clearcoat: 1, clearcoatRoughness: 0.03, specularIntensity: 1 } },
};
const PALS = [
  ['#ff5d8f', '#ffd166', '#06d6a0', '#118ab2'],
  ['#f94144', '#f9c74f', '#90be6d', '#577590'],
  ['#c77dff', '#ff9e00', '#00bbf9', '#f15bb5'],
  ['#ef476f', '#2ec4b6'],
  ['#ffb5a7', '#a2d2ff', '#cdb4db', '#b9fbc0'],
];
const INSIDES = [
  { color: '#e8c36a', metalness: 1, roughness: 0.22, label: 'gold' },
  { color: '#f4f1ea', roughness: 0.55, label: 'white' },
  { color: '#c9ccd3', metalness: 1, roughness: 0.18, label: 'silver' },
];
const BG = ['#e8e4dd', '#dde3ea', '#e9e1e6', '#e2e7de', '#1d1f24'];

const clamp01 = (x) => Math.min(1, Math.max(0, x));
const ease = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };

export default function build({ THREE, rand, pick, range, makeMaterial }) {
  const shellKey = pick(Object.keys(SHELLS));
  const S = SHELLS[shellKey];
  const pal = pick(PALS);
  const P = pal.length;
  const inside = pick(INSIDES);
  const bg = pick(BG);
  const dark = bg === '#1d1f24';
  const r = range(0.56, 0.64);
  const cycles = 4;
  const cycleSec = range(2.0, 2.4);
  const thick = 0.016;

  const shellMats = pal.map((c) => makeMaterial({ ...S.mat, color: shellKey === 'chrome' ? mixHex(c, '#ffffff', 0.25) : c }));
  const innerMat = makeMaterial({ ...inside, side: THREE.BackSide });
  const rimMats = shellMats.map((m) => { const k = m.clone(); k.side = THREE.DoubleSide; k.onBeforeCompile = m.onBeforeCompile; return k; });

  function mixHex(a, b, t) { return '#' + new THREE.Color(a).lerp(new THREE.Color(b), t).getHexString(); }

  function half(sign, idx) {
    const pivot = new THREE.Group();
    const phiStart = sign > 0 ? Math.PI / 2 : -Math.PI / 2;
    const outer = new THREE.SphereGeometry(1, 72, 48, phiStart, Math.PI);
    const inner = new THREE.SphereGeometry(1 - thick, 72, 48, phiStart, Math.PI);
    const rim = new THREE.RingGeometry(1 - thick, 1, 72, 1);
    rim.rotateY(Math.PI / 2);
    const mo = new THREE.Mesh(outer, shellMats[idx]);
    const mi = new THREE.Mesh(inner, innerMat);
    const mr = new THREE.Mesh(rim, rimMats[idx]);
    const body = new THREE.Group();
    body.add(mo, mi, mr);
    pivot.add(body);
    pivot.position.set(0, 1, 0); // sphere centre
    return pivot;
  }

  function makeCopy(n) {
    const root = new THREE.Group();
    const idx = ((n % P) + P) % P;
    const halves = [half(1, idx), half(-1, idx)];
    root.add(...halves);
    root.userData.update = (tau) => {
      // resting inside the parent's shell until the parent opens
      const lift = tau < -0.75 ? thick / r : tau < -0.6 ? (thick / r) * (1 - ease((tau + 0.75) / 0.15)) : 0;
      halves.forEach((h, i) => {
        const s = i === 0 ? 1 : -1;
        let th = 0, x = 0;
        if (tau > 0.02) {
          const gapU = clamp01((tau - 0.02) / 0.1);
          x += s * 0.004 * gapU;
          // tiny shiver while cracking
          const shiver = tau < 0.14 ? Math.sin(tau * 260) * 0.012 * (1 - Math.abs(tau - 0.08) / 0.06) : 0;
          th = Math.max(0, shiver);
        }
        if (tau > 0.14) {
          const u = (tau - 0.14) / 0.38;
          if (u < 1) th = (Math.PI / 2) * u * u;
          else {
            const v = u - 1;
            th = Math.PI / 2 + 0.36 * Math.exp(-3.2 * v) * Math.sin(8.5 * v);
          }
        }
        x += s * th; // roll without slipping (radius 1)
        if (tau > 0.95) {
          const w = (tau - 0.95) / 0.45;
          x += s * (w < 1 ? 1.4 * w * w : 1.4 + 2.8 * (w - 1));
        }
        h.position.set(x, 1 + lift, 0);
        h.rotation.set(0, 0, -s * th);
      });
    };
    return root;
  }

  const notes = [523.25, 587.33, 659.25, 783.99, 880.0, 1046.5];
  const startNote = Math.floor(rand() * 2);
  const seq = Array.from({ length: cycles }, (_, k) => notes[startNote + (k % 4)]);

  const shapeWord = 'Sphere';
  const titles = [
    `Every ${shapeWord} Hides Another One 🔁 #asmr #satisfying`,
    `The ${S.label} Sphere That Never Ends 🔁 #asmr`,
    `How Deep Does This Sphere Go? 🔁 #satisfying #asmr`,
    `Open It… There's Always One More 🔁 #asmr #satisfying`,
  ];
  const caps = [
    `Crack it open… there's always one more inside. How deep does it go? Keep watching. 🔁`,
    `Every shell opens to a smaller one. It never stops. Can you find where it loops? 🔁`,
  ];
  return {
    family: 'nestshell',
    M: { c: new THREE.Vector3(0, 0, 0), r, phi: range(-0.32, 0.32) },
    nMin: -3, nMax: 10,
    cycles, cycleSec,
    bg, fog: [10, 26], envIntensity: dark ? 0.4 : 0.55,
    keyIntensity: dark ? 2.8 : 2.4,
    camera: { pos: [0.3, 2.7, 6.9], target: [0, 1.15, 0], fov: 30 },
    keyPos: [3, 8, 5], shadowSize: 4,
    makeCopy,
    events: [
      { tau: 0.025, type: 'crack', gain: 0.9, pan: 0 },
      { tau: 0.12, type: 'pop', gain: 0.6, pan: 0 },
      { tau: 0.16, type: 'whoosh', dur: 0.3, gain: 0.5, pan: 0, stereoSpread: true },
      { tau: 0.2, type: 'chime', gain: 0.45, pan: 0, pitchSeq: seq },
      { tau: 0.52, type: 'tick', gain: 0.55, pan: -0.5, pitch: 1.0 },
      { tau: 0.525, type: 'tick', gain: 0.5, pan: 0.5, pitch: 1.12 },
      { tau: 0.63, type: 'tick', gain: 0.22, pan: -0.5, pitch: 1.05 },
      { tau: 0.64, type: 'tick', gain: 0.2, pan: 0.5, pitch: 1.18 },
      { tau: 0.96, type: 'slide', dur: 0.45, gain: 0.35, pan: 0 },
    ],
    bed: { type: 'room', gain: 0.05 },
    meta: {
      slug: `${shellKey}-sphere`,
      title: pick(titles),
      caption: `${pick(caps)}\n\n#asmr #satisfying #oddlysatisfying #infiniteloop #matryoshka #shorts`,
      tags: ['asmr', 'satisfying', 'oddly satisfying', 'nested spheres', 'matryoshka', 'infinite loop', 'never ending', 'sphere opening', `${S.label.toLowerCase()} sphere`, 'satisfying video', 'relaxing', '3d animation', 'shorts'],
    },
  };
}
