// Cube cut: a knife cuts the cube three times into 8. Seven pieces slide away and
// the back corner piece is the next cube, half size, in the next colour. Forever.
const MATS = {
  sand: {
    label: 'Kinetic Sand', word: 'sand',
    pals: [['#ff6fa8', '#39c6c0', '#8f6cf0', '#ffc94a'], ['#7ad1ff', '#ff8a5c', '#9be37a', '#f070d8'], ['#e85d75', '#f7b267', '#5ec2b7', '#6a7bd8']],
    mat: { roughness: 0.95, grain: 140, grainAmt: 0.9, mottle: 3, mottleAmt: 0.25, bump: 0.035, colorVar: 0.32, roughVar: 0.05, sheen: 0.4, sheenRoughness: 0.9 },
    cut: 'sand',
  },
  soap: {
    label: 'Soap', word: 'soap',
    pals: [['#ffd6e8', '#cdeffd'], ['#e7dcff', '#fff1c9'], ['#c9f2df', '#ffd9cc']],
    mat: { roughness: 0.32, clearcoat: 0.6, clearcoatRoughness: 0.25, mottle: 2.2, mottleAmt: 0.25, colorVar: 0.12, sheen: 0.5 },
    cut: 'soap',
  },
  clay: {
    label: 'Clay', word: 'clay',
    pals: [['#e07a5f', '#3d405b', '#81b29a', '#f2cc8f'], ['#d62828', '#f77f00', '#fcbf49', '#003049']],
    mat: { roughness: 0.75, grain: 45, grainAmt: 0.25, mottle: 2.5, mottleAmt: 0.3, bump: 0.01, colorVar: 0.18 },
    cut: 'soap',
  },
  chocolate: {
    label: 'Chocolate', word: 'chocolate',
    pals: [['#4a2717', '#f1e2c8'], ['#3b1f12', '#c98b5a']],
    mat: { roughness: 0.38, clearcoat: 0.35, clearcoatRoughness: 0.35, mottle: 3, mottleAmt: 0.18, colorVar: 0.15 },
    cut: 'crisp',
  },
  marble: {
    label: 'Marble', word: 'marble',
    pals: [['#f2f0ea', '#2c3a36'], ['#efe7dd', '#1f2833']],
    mat: { roughness: 0.18, clearcoat: 0.8, clearcoatRoughness: 0.1, vein: true, veinScale: 4.5, mottle: 2, mottleAmt: 0.2, colorVar: 0.1 },
    cut: 'stone',
  },
};

const BG = ['#e9e5df', '#dfe6ea', '#ebe3ea', '#e4e9e1', '#d9d6e4'];

const clamp01 = (x) => Math.min(1, Math.max(0, x));
const ease = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
const lerp = (a, b, t) => a + (b - a) * t;

export default function build({ THREE, rand, pick, range, makeMaterial }) {
  const key = pick(Object.keys(MATS));
  const M0 = MATS[key];
  const pal = pick(M0.pals);
  const P = pal.length;
  const cycles = 4; // P divides 4
  const cycleSec = range(2.5, 2.9);
  const bg = pick(BG);

  const mats = pal.map((c) => makeMaterial({ ...M0.mat, color: c }));
  const knifeMat = makeMaterial({ color: '#dfe3e8', metalness: 1, roughness: 0.16 });
  const handleMat = makeMaterial({ color: pick(['#2b2b2e', '#5a3a26', '#1f3d36']), roughness: 0.5, grain: 30, grainAmt: 0.2, colorVar: 0.1 });

  const H = 0.5;
  const qFlat = new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().makeBasis(
    new THREE.Vector3(0, 1, 0), new THREE.Vector3(0, 0, 1), new THREE.Vector3(1, 0, 0)));
  const pieceKeys = [];
  for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) for (let k = 0; k < 2; k++) if (i || j || k) pieceKeys.push([i, j, k]);

  function makeKnife() {
    const g = new THREE.Group();
    const blade = new THREE.Mesh(new THREE.BoxGeometry(0.008, 0.62, 1.45), knifeMat);
    blade.position.set(0, -0.24, 0);
    const handle = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.12, 0.6), handleMat);
    handle.position.set(0, -0.02, 1.0);
    g.add(blade, handle);
    return g;
  }

  function makeCopy(n) {
    const root = new THREE.Group();
    const mat = mats[((n % P) + P) % P];
    const pieces = pieceKeys.map(([i, j, k]) => {
      const cx = (i + 0.5) * H, cy = (j + 0.5) * H, cz = (k + 0.5) * H;
      const geo = new THREE.BoxGeometry(H, H, H, 1, 1, 1);
      geo.translate(cx, cy, cz);
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(-cx, -cy, -cz);
      const pivot = new THREE.Group();
      pivot.add(mesh);
      root.add(pivot);
      return { i, j, k, cx, cy, cz, pivot };
    });
    const knife = makeKnife();
    root.add(knife);

    root.userData.update = (tau) => {
      // knife
      const cuts = [
        { a: 0.0, b: 0.2, c: 0.26, axis: 'x' },
        { a: 0.26, b: 0.46, c: 0.52, axis: 'z' },
        { a: 0.52, b: 0.66, c: 0.74, axis: 'h' },
      ];
      knife.visible = false;
      for (const ct of cuts) {
        if (tau < ct.a || tau >= ct.c) continue;
        knife.visible = true;
        const down = tau < ct.b ? ease((tau - ct.a) / (ct.b - ct.a)) : 1 - ease((tau - ct.b) / (ct.c - ct.b));
        if (ct.axis === 'x') {
          knife.rotation.set(0, 0, 0);
          knife.position.set(0.5, lerp(3.4, 0.55, down), 0.62);
        } else if (ct.axis === 'z') {
          knife.rotation.set(0, Math.PI / 2, 0);
          knife.position.set(0.62, lerp(3.4, 0.55, down), 0.5);
        } else {
          // horizontal slice: drop in front, sweep through, pull back, lift out
          knife.quaternion.copy(qFlat);
          const u = (tau - ct.a) / (ct.c - ct.a);
          let yy = 0.5, zz = 1.75;
          if (u < 0.2) yy = lerp(3.4, 0.5, ease(u / 0.2));
          else if (u < 0.62) zz = lerp(1.75, 0.48, ease((u - 0.2) / 0.42));
          else if (u < 0.8) zz = lerp(0.48, 1.75, ease((u - 0.62) / 0.18));
          else yy = lerp(0.5, 3.4, ease((u - 0.8) / 0.2));
          knife.position.set(0.55, yy, zz);
        }
      }
      // pieces
      const gap = 0.006;
      const slideU = (tau - 0.74) / 0.42;
      const slide = slideU <= 0 ? 0 : slideU < 1 ? slideU * slideU : 1 + 2 * (slideU - 1);
      const D = 1.6 * slide;
      for (const p of pieces) {
        let x = p.cx, y = p.cy, z = p.cz, rx = 0, rz = 0;
        if (tau > 0.2 && p.i) x += gap * ease((tau - 0.2) / 0.05);
        if (tau > 0.46 && p.k) z += gap * ease((tau - 0.46) / 0.05);
        if (p.i && !p.k) x += D;
        else if (p.k && !p.i) z += D;
        else if (p.i && p.k) { x += D * 0.95; z += D * 0.35; }
        else if (p.j) {
          // top-back piece sits on the next cube: slides back and drops off.
          const u = clamp01((tau - 0.74) / 0.34);
          const d = 0.85 * ease(u) + 2.4 * Math.max(0, tau - 1.08);
          x -= d * 0.72; z -= d * 0.72;
          const fall = clamp01((d - 0.38) / 0.36);
          y -= 0.5 * fall * fall;
          rx = -0.45 * fall; rz = 0.45 * fall;
        }
        p.pivot.position.set(x, y, z);
        p.pivot.rotation.set(rx, 0, rz);
      }
    };
    return root;
  }

  const tags = ['asmr', 'satisfying', 'oddly satisfying', `${M0.word} cutting`, `${M0.label.toLowerCase()} asmr`, 'cube cutting', 'infinite loop', 'never ending', 'satisfying video', 'relaxing', '3d animation', 'loop video', 'shorts'];
  const titles = [
    `This ${M0.label} Cube Never Ends 🔁 #asmr #satisfying`,
    `Cutting ${M0.label}… Forever 🔁 #asmr #satisfying`,
    `The ${M0.label} Cube That Keeps Shrinking 🔁 #asmr`,
    `Every Cut Reveals Another Cube 🔁 #satisfying #asmr`,
  ];
  const caps = [
    `Cut it into eight. Keep the last piece. Cut it again… it never runs out. Watch till the end — there is no end. 🔁`,
    `Every time you think it's the last cube, there's another one inside. How long can you watch? 🔁`,
  ];

  return {
    family: 'cubecut',
    M: { c: new THREE.Vector3(0, 0, 0), r: 0.5, phi: 0 },
    nMin: -2, nMax: 12,
    cycles, cycleSec,
    bg, fog: [9, 22],
    camera: { pos: [4.55, 6.3, 5.6], target: [0.78, 0.45, 0.82], fov: 30 },
    keyPos: [3.5, 8, 2.5], shadowSize: 4.5,
    makeCopy,
    events: [
      { tau: 0.035, type: M0.cut, dur: 0.17, gain: 1.0, pan: 0.0 },
      { tau: 0.198, type: 'tick', gain: 0.45, pan: 0.0 },
      { tau: 0.295, type: M0.cut, dur: 0.17, gain: 1.0, pan: 0.15 },
      { tau: 0.458, type: 'tick', gain: 0.45, pan: 0.15 },
      { tau: 0.565, type: M0.cut, dur: 0.09, gain: 0.85, pan: -0.1 },
      { tau: 0.75, type: 'slide', dur: 0.55, gain: 0.55, pan: 0.0 },
      { tau: 0.98, type: 'thud', gain: 0.5, pan: -0.35 },
    ],
    bed: { type: 'room', gain: 0.06 },
    meta: {
      slug: `${key}-cube`,
      title: pick(titles),
      caption: `${pick(caps)}\n\n#asmr #satisfying #oddlysatisfying #${M0.word}cutting #infiniteloop #shorts`,
      tags,
    },
  };
}
