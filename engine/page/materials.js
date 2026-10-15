// Physically based materials with optional procedural surface detail.
// Detail is computed from the geometry's object-space position, so pieces cut
// from one block keep a continuous grain across the cut, and every copy in the
// chain looks the same at the same relative size (loop-safe).
import * as THREE from 'three';

const NOISE = /* glsl */`
varying vec3 vObjPos;
uniform float uGrain, uGrainAmt, uMottle, uMottleAmt, uBump, uVein, uVeinScale;
uniform vec3 uVeinColor;
float h31(vec3 p){ p = fract(p*0.3183099 + 0.1); p *= 17.0; return fract(p.x*p.y*p.z*(p.x+p.y+p.z)); }
float vnoise(vec3 x){
  vec3 i = floor(x); vec3 f = fract(x); f = f*f*(3.0-2.0*f);
  return mix(mix(mix(h31(i),h31(i+vec3(1,0,0)),f.x), mix(h31(i+vec3(0,1,0)),h31(i+vec3(1,1,0)),f.x),f.y),
             mix(mix(h31(i+vec3(0,0,1)),h31(i+vec3(1,0,1)),f.x), mix(h31(i+vec3(0,1,1)),h31(i+vec3(1,1,1)),f.x),f.y), f.z);
}
float fbm(vec3 p){ float a=0.5, s=0.0; for(int i=0;i<4;i++){ s += a*vnoise(p); p = p*2.03 + 17.1; a *= 0.5; } return s; }
float detailHeight(vec3 p){
  float g = vnoise(p*uGrain) * 0.65 + vnoise(p*uGrain*2.3 + 5.0) * 0.35;
  return g * uGrainAmt + fbm(p*uMottle) * uMottleAmt;
}
`;

export function makeMaterial(o = {}) {
  const m = new THREE.MeshPhysicalMaterial({
    color: new THREE.Color(o.color ?? '#cccccc'),
    roughness: o.roughness ?? 0.6,
    metalness: o.metalness ?? 0,
    clearcoat: o.clearcoat ?? 0,
    clearcoatRoughness: o.clearcoatRoughness ?? 0.2,
    sheen: o.sheen ?? 0,
    sheenRoughness: o.sheenRoughness ?? 0.6,
    sheenColor: new THREE.Color(o.sheenColor ?? '#ffffff'),
    specularIntensity: o.specularIntensity ?? 1,
    ior: o.ior ?? 1.5,
    side: o.side ?? THREE.FrontSide,
    envMapIntensity: o.envMapIntensity ?? 1,
  });
  if (o.emissive) { m.emissive = new THREE.Color(o.emissive); m.emissiveIntensity = o.emissiveIntensity ?? 1; }
  const detail = o.grain || o.mottleAmt || o.vein;
  if (!detail) return m;

  const u = {
    uGrain: { value: o.grain ?? 0 },
    uGrainAmt: { value: o.grainAmt ?? 0 },
    uMottle: { value: o.mottle ?? 2 },
    uMottleAmt: { value: o.mottleAmt ?? 0 },
    uBump: { value: o.bump ?? 0 },
    uVein: { value: o.vein ? 1 : 0 },
    uVeinScale: { value: o.veinScale ?? 3 },
    uVeinColor: { value: new THREE.Color(o.veinColor ?? '#555555') },
  };
  const colorAmt = (o.colorVar ?? 0.35).toFixed(3);
  const roughVar = (o.roughVar ?? 0.15).toFixed(3);
  m.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, u);
    sh.vertexShader = 'varying vec3 vObjPos;\n' + sh.vertexShader.replace(
      '#include <begin_vertex>', '#include <begin_vertex>\n vObjPos = position;');
    sh.fragmentShader = NOISE + sh.fragmentShader
      .replace('#include <color_fragment>', `#include <color_fragment>
        float dh = detailHeight(vObjPos);
        diffuseColor.rgb *= 1.0 + (dh - 0.5*(uGrainAmt+uMottleAmt)) * ${colorAmt} * 2.0;
        if (uVein > 0.5) {
          float v = abs(sin(vObjPos.x*uVeinScale + vObjPos.y*uVeinScale*0.6 + fbm(vObjPos*1.7)*7.0));
          float vein = pow(1.0 - v, 9.0);
          diffuseColor.rgb = mix(diffuseColor.rgb, uVeinColor, clamp(vein*0.85, 0.0, 1.0));
        }`)
      .replace('#include <roughnessmap_fragment>', `#include <roughnessmap_fragment>
        roughnessFactor = clamp(roughnessFactor + (dh - 0.5*(uGrainAmt+uMottleAmt)) * ${roughVar}, 0.02, 1.0);`)
      .replace('#include <normal_fragment_maps>', `#include <normal_fragment_maps>
        if (uBump > 0.0) {
          vec3 sx = dFdx(-vViewPosition); vec3 sy = dFdy(-vViewPosition);
          float hx = dFdx(dh); float hy = dFdy(dh);
          vec3 r1 = cross(sy, normal); vec3 r2 = cross(normal, sx);
          float det = dot(sx, r1) * faceDirection;
          vec3 grad = sign(det) * (hx * r1 + hy * r2);
          normal = normalize(abs(det) * normal - grad * uBump);
        }`);
  };
  m.customProgramCacheKey = () => `detail-${colorAmt}-${roughVar}`;
  return m;
}
