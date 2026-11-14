// Funnel marbles: marbles roll down a spiral into a cone, shrinking as they near
// the centre. New ones keep rolling in from the edge. No floor; the cone is the
// world (self-similar about its apex).
const BALLS = {
  glossy: { label: 'Glossy', mat: { roughness: 0.08, clearcoat: 1, clearcoatRoughness: 0.03 } },
  chrome: { label: 'Chrome', mat: { roughness: 0.05, metalness: 1 } },
  pearl: { label: 'Pearl', mat: { roughness: 0.25, clearcoat: 0.8, sheen: 1, sheenRoughness: 0.3 } },
  gold: { label: 'Golden', mat: { roughness: 0.15, metalness: 1 }, fixed: ['#e8c36a', '#d9a441', '#f3d98b'] },
  copper: { label: 'Copper', mat: { roughness: 0.18, metalness: 1 }, fixed: ['#c8743f', '#b5603a', '#e09a6b'], plain: true },
  neon: { label: 'Neon', mat: { roughness: 0.25, clearcoat: 1, emissiveIntensity: 0.75 }, neon: true },
  stone: { label: 'Marble Stone', mat: { roughness: 0.2, clearcoat: 0.9, vein: true, veinScale: 40, veinColor: '#3a3f44', mottle: 12, mottleAmt: 0.15, colorVar: 0.08 }, fixed: ['#f4f1ea', '#2e3236', '#d8cfc4'], plain: true },
  wood: { label: 'Wooden', mat: { roughness: 0.55, grain: 60, grainAmt: 0.35, mottle: 10, mottleAmt: 0.3, colorVar: 0.22 }, fixed: ['#c8925a', '#8c5a32', '#e0b47c'] },
  candy: { label: 'Candy', mat: { roughness: 0.06, clearcoat: 1, clearcoatRoughness: 0.02 } },
};
const NEON = [['#ff2e88', '#00e5ff', '#39ff14'], ['#ffea00', '#ff00e6', '#00e5ff'], ['#7c4dff', '#ff3d00', '#00ffa3']];
const PALS = [
  ['#ff4d6d', '#ffd23f', '#3a86ff'], ['#06d6a0', '#ef476f', '#ffd166'], ['#8338ec', '#ff006e', '#fb5607'],
  ['#4cc9f0', '#f72585', '#b8f2e6'], ['#f4f1de', '#e07a5f', '#3d405b'],
  ['#ff9f1c', '#2ec4b6', '#e71d36'], ['#9b5de5', '#f15bb5', '#fee440'], ['#00bbf9', '#00f5d4', '#ffffff'],
  ['#264653', '#e9c46a', '#e76f51'], ['#cdb4db', '#ffc8dd', '#a2d2ff'],
];
const CONES = [
  ['#e9e4dc', '#d8d1c6'], ['#262a31', '#1b1e23'], ['#dfe7ee', '#c9d4de'], ['#2f3e46', '#354f52'], ['#efe1d1', '#e4cdb4'],
  ['#3d2c4f', '#2a1f38'], ['#e8dfee', '#d6c8e2'], ['#1f3b36', '#18302c'], ['#f2e3c9', '#e3caa0'], ['#5a2a2a', '#3f1d1d'],
];
const DARK_CONES = [['#14161a', '#1d2128'], ['#1a1530', '#120f22'], ['#0f1d1b', '#162a27']];

export default function build({ THREE, rand, pick, range, makeMaterial }) {
  const ballKey = pick(Object.keys(BALLS));
  const B = BALLS[ballKey];
  const pal = B.fixed ?? (B.neon ? pick(NEON) : pick(PALS));
  const cone = B.neon ? pick(DARK_CONES) : pick(CONES);
  const dark = new THREE.Color(cone[0]).getHSL({}).l < 0.4;
  const perTurn = Math.floor(range(9, 13));
  const phi = (2 * Math.PI) / perTurn;
  const step = range(0.945, 0.958);
  const R = 1 / step; // > 1: marbles move inward and shrink over time
  const cycleSec = range(0.3, 0.36);
  const cycles = Math.round(10 / cycleSec / 3) * 3;
  const P = 3;
  const slope = range(0.32, 0.45);
  const m = 0.115;
  const bands = Math.floor(range(1, 3));

  const mats = pal.map((c) => makeMaterial({ ...B.mat, color: c, ...(B.neon ? { color: '#' + new THREE.Color(c).multiplyScalar(0.12).getHexString(), emissive: c } : {}) }));
  const nrm = new THREE.Vector3(-slope, 1, 0).normalize();
  const center = new THREE.Vector3(1, slope, 0).addScaledVector(nrm, m);
  const geo = new THREE.SphereGeometry(m, 32, 20);
  // a painted stripe so the rolling reads
  const stripeGeo = new THREE.TorusGeometry(m * 0.975, m * 0.055, 6, 40);
  const stripeMat = makeMaterial({ color: '#ffffff', roughness: 0.3, clearcoat: 1 });

  function makeCopy(n) {
    const root = new THREE.Group();
    const ball = new THREE.Group();
    ball.position.copy(center);
    const body = new THREE.Mesh(geo, mats[((n % P) + P) % P]);
    ball.add(body);
    if (ballKey !== 'chrome' && ballKey !== 'gold' && !B.plain) {
      const st = new THREE.Mesh(stripeGeo, stripeMat);
      st.userData.noShadow = true;
      ball.add(st);
    }
    root.add(ball);
    const chord = Math.sqrt(1 + step * step - 2 * step * Math.cos(phi));
    const spin = (chord / m) * 1.0;
    root.userData.update = (tau) => {
      ball.rotation.set(0, 0, 0);
      ball.rotateX(-spin * tau);
      ball.rotateZ(0.4);
    };
    return root;
  }

  function makeStatic() {
    // Lathe cone y = slope * rho, log-spaced profile, log-periodic colour bands.
    const pts = [];
    for (let i = 0; i <= 260; i++) {
      const rho = Math.exp(Math.log(0.0008) + (Math.log(30) - Math.log(0.0008)) * (i / 260));
      pts.push(new THREE.Vector2(rho, slope * rho));
    }
    const g = new THREE.LatheGeometry(pts, 160);
    const colors = [];
    const c0 = new THREE.Color(cone[0]), c1 = new THREE.Color(cone[1]);
    const pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) {
      // spiral track bands: invariant under (scale R, rotate phi) because they
      // depend only on k - theta/phi, which that transform leaves unchanged
      const rho = Math.hypot(pos.getX(i), pos.getZ(i));
      const k = Math.log(rho) / Math.log(R);
      const th = Math.atan2(-pos.getZ(i), pos.getX(i));
      const t = Math.pow(0.5 + 0.5 * Math.cos((2 * Math.PI * bands * (k - th / phi)) / perTurn), 3);
      const c = c0.clone().lerp(c1, t);
      colors.push(c.r, c.g, c.b);
    }
    g.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    const mat = makeMaterial({ color: '#ffffff', roughness: 0.42, clearcoat: 0.4, clearcoatRoughness: 0.3, side: THREE.DoubleSide });
    mat.vertexColors = true;
    const mesh = new THREE.Mesh(g, mat);
    mesh.receiveShadow = true;
    return mesh;
  }

  const seq = Array.from({ length: cycles }, () => range(0.85, 1.2));
  const titles = [
    `Marbles Falling Into Infinity 🔁 #asmr #satisfying`,
    `This Funnel Never Fills Up 🔁 #satisfying #asmr`,
    `${B.label} Marbles Spiraling Forever 🔁 #asmr`,
    `Where Do The Marbles Go? 🔁 #satisfying #asmr`,
    `The Marble Funnel With No Bottom 🔁 #asmr`,
    `${B.label} Marbles That Never Stop Rolling 🔁 #satisfying`,
    `Marbles Shrinking Forever 🔁 #asmr #satisfying`,
    `Can You Spot Where This Loops? 🔁 #asmr #marbles`,
    `This Marble Run Never Ends 🔁 #satisfying #asmr`,
    `${B.label} Marble Spiral Into Infinity 🔁 #asmr`,
    `The Funnel That Swallows Marbles Forever 🔁 #asmr`,
    `Endless ${B.label} Marble Spiral 🔁 #satisfying`,
  ];
  const caps = [
    `They roll in, spiral down, shrink… and never reach the bottom. Keep watching. 🔁`,
    `The funnel never fills. The marbles never stop. Can you find where it loops? 🔁`,
    `Round and round, smaller and smaller. There is no bottom. 🔁`,
  ];
  return {
    family: 'funnelmarbles',
    M: { c: new THREE.Vector3(0, 0, 0), r: R, phi },
    nMin: -95, nMax: 40, minScale: 0.012, maxScale: 30,
    cycles, cycleSec,
    bg: dark ? '#14161a' : cone[0], floor: false, fog: [12, 30],
    envIntensity: dark ? 0.5 : 0.6, keyIntensity: 2.4,
    camera: { pos: [0.1, 5.3, 3.7], target: [0, 0.15, 0], fov: 34 },
    keyPos: [2, 9, 3], shadowSize: 2.6,
    makeCopy, makeStatic,
    events: [
      { tau: 0.0, type: 'tick', gain: 0.32, pan: 0, pitch: 1.6, pitchSeq: seq },
    ],
    bed: { type: 'roll', gain: 0.22, rate: 1 / cycleSec },
    meta: {
      slug: `${ballKey}-marbles`,
      title: pick(titles),
      caption: `${pick(caps)}\n\n#asmr #satisfying #oddlysatisfying #marbles #infiniteloop #shorts`,
      tags: ['asmr', 'satisfying', 'oddly satisfying', 'marbles', 'marble run', 'gravity well', 'funnel', 'infinite loop', 'never ending', 'satisfying video', 'relaxing', '3d animation', 'shorts'],
    },
  };
}
