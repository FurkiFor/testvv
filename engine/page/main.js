// Seamless infinite-loop renderer.
//
// Every scene is an infinite chain of copies: copy n+1 = M(copy n), where M is a
// similarity transform (uniform scale r and rotation phi about the vertical axis
// through the fixed point c). Copy n is drawn with transform M^(n-T) and local time
// tau = T - n. Because M^(n-T) at T+1 equals M^((n-1)-T), frame(T+1) == frame(T)
// exactly, so any whole number of cycles loops with no seam. Lights, floor and
// camera stay fixed, and any per-copy variation must repeat with a period that
// divides the video's cycle count.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { makeMaterial } from './materials.js';

export function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

let renderer, scene, camera, plan, copies = [];

function applySim(obj, M, e) {
  const s = Math.pow(M.r, e);
  const a = M.phi * e;
  const ca = Math.cos(a), sa = Math.sin(a);
  const c = M.c;
  const rcx = c.x * ca + c.z * sa;
  const rcz = -c.x * sa + c.z * ca;
  obj.position.set(c.x - s * rcx, c.y - s * c.y, c.z - s * rcz);
  obj.rotation.set(0, a, 0);
  obj.scale.setScalar(s);
  return s;
}

window.setup = async (cfg) => {
  const { family, seed, width, height } = cfg;
  const rand = mulberry32(seed);
  const pick = (arr) => arr[Math.floor(rand() * arr.length) % arr.length];
  const range = (a, b) => a + (b - a) * rand();

  const q = cfg.quality ?? {};
  renderer = new THREE.WebGLRenderer({ antialias: q.antialias ?? true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(width, height);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.shadowMap.enabled = q.shadows !== false;
  renderer.shadowMap.type = q.softShadows === false ? THREE.PCFShadowMap : THREE.PCFSoftShadowMap;
  document.body.appendChild(renderer.domElement);

  scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  const mod = await import(`./scenes/${family}.js`);
  const ctx = { THREE, rand, pick, range, makeMaterial, seed };
  plan = mod.default(ctx);

  // Backdrop, fog and floor (static, so loop-safe).
  const bg = new THREE.Color(plan.bg);
  scene.background = bg;
  if (plan.fog) scene.fog = new THREE.Fog(bg, plan.fog[0], plan.fog[1]);
  scene.environmentIntensity = plan.envIntensity ?? 0.55;
  if (plan.floor !== false) {
    const floor = new THREE.Mesh(
      new THREE.PlaneGeometry(400, 400),
      new THREE.MeshStandardMaterial({ color: plan.floorColor ?? plan.bg, roughness: 0.92, metalness: 0 })
    );
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);
  }

  // Lights: soft key with shadows, cool fill, warm rim.
  const key = new THREE.DirectionalLight(0xffffff, plan.keyIntensity ?? 2.4);
  const kp = plan.keyPos ?? [4, 9, 5];
  const tgt = plan.camera.target;
  key.position.set(tgt[0] + kp[0], tgt[1] + kp[1], tgt[2] + kp[2]);
  key.target.position.set(tgt[0], tgt[1], tgt[2]);
  key.castShadow = true;
  key.shadow.mapSize.set(q.shadowMap ?? 2048, q.shadowMap ?? 2048);
  const ss = plan.shadowSize ?? 4;
  Object.assign(key.shadow.camera, { left: -ss, right: ss, top: ss, bottom: -ss, near: 0.5, far: 40 });
  key.shadow.bias = -0.0004;
  key.shadow.normalBias = 0.02;
  key.shadow.radius = 4;
  scene.add(key, key.target);
  const fill = new THREE.HemisphereLight(0xdfe9ff, 0x2a2420, plan.fillIntensity ?? 0.5);
  scene.add(fill);
  const rim = new THREE.DirectionalLight(0xffe2c8, plan.rimIntensity ?? 0.9);
  rim.position.set(tgt[0] - 6, tgt[1] + 4, tgt[2] - 7);
  scene.add(rim);

  const cam = plan.camera;
  camera = new THREE.PerspectiveCamera(cam.fov ?? 32, width / height, 0.01, 200);
  camera.position.set(...cam.pos);
  camera.lookAt(...cam.target);

  copies = [];
  for (let n = plan.nMin; n <= plan.nMax; n++) {
    const g = plan.makeCopy(n);
    g.traverse((o) => { if (o.isMesh) { o.castShadow = o.userData.noShadow ? false : true; o.receiveShadow = true; } });
    scene.add(g);
    copies.push({ n, g });
  }
  if (plan.makeStatic) scene.add(plan.makeStatic());

  return {
    cycles: plan.cycles,
    cycleSec: plan.cycleSec,
    events: plan.events,
    bed: plan.bed,
    meta: plan.meta,
  };
};

window.renderOnly = (T) => { window.renderFrame(T, -1); };

window.renderFrame = (T, quality = 0.92) => {
  const minS = plan.minScale ?? 2e-3;
  const maxS = plan.maxScale ?? 60;
  for (const { n, g } of copies) {
    const s = applySim(g, plan.M, n - T);
    const vis = s > minS && s < maxS;
    g.visible = vis;
    if (vis && g.userData.update) g.userData.update(T - n);
  }
  if (plan.onFrame) plan.onFrame(T);
  renderer.render(scene, camera);
  if (quality < 0) { renderer.getContext().finish(); return ''; }
  return renderer.domElement.toDataURL('image/jpeg', quality);
};

window.engineReady = true;
