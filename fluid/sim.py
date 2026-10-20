"""MLS-MPM liquid simulation (Taichi CPU) + splashsurf surface meshes.

usage: python sim.py --container bowl --fluid honey --mode ball|object --out DIR
                     [--frames 66] [--dx 0.02] [--hover 5]
mode ball   : the container is full of <fluid>; a sphere of the same fluid drops in.
mode object : the container is full of <fluid>; a solid steel ball drops in
              (1-DOF buoyancy/drag dynamics, two-way pushes the liquid).
Writes DIR/mesh_XXXX.npz (v,f), DIR/container.npz, DIR/meta.json
"""
import argparse, os, sys, time, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import containers
from fluids import FLUIDS, K_BULK, STEEL_RHO

ap = argparse.ArgumentParser()
ap.add_argument("--container", required=True)
ap.add_argument("--fluid", required=True)
ap.add_argument("--mode", default="ball", choices=["ball", "object"])
ap.add_argument("--out", required=True)
ap.add_argument("--frames", type=int, default=66)
ap.add_argument("--dx", type=float, default=0.02)
ap.add_argument("--hover", type=int, default=5)
A = ap.parse_args()

import taichi as ti

FPS, PREROLL = 30, 8
DX, NFR, HOVER, OBJ = A.dx, A.frames, A.hover, A.mode == "object"
FL = FLUIDS[A.fluid]
K = K_BULK
os.makedirs(A.out, exist_ok=True)
C = containers.get(A.container)

bx, by, bz, br = C["ball"]
if OBJ:
    br = C.get("obj_r", 0.15)
    bz = C["rim"] + br + 0.28
MARGIN_XY, TOP_PAD = 0.5, 0.15
lo = np.array([C["lo"][0] - MARGIN_XY, C["lo"][1] - MARGIN_XY, -3 * DX])
hi = np.array([C["hi"][0] + MARGIN_XY, C["hi"][1] + MARGIN_XY, bz + br + TOP_PAD])
n = np.ceil((hi - lo) / DX).astype(int) + 1
print("grid", n, "nodes", int(n.prod()), flush=True)

# solid SDF (container + floor) on grid nodes
xs = [lo[a] + np.arange(n[a]) * DX for a in range(3)]
X, Y, Z = np.meshgrid(*xs, indexing="ij")
phi = np.minimum(C["sdf"](X, Y, Z), Z).astype(np.float32)
g = np.stack(np.gradient(phi, DX), -1)
g /= (np.linalg.norm(g, axis=-1, keepdims=True) + 1e-9)
del X, Y, Z

# container render mesh (fine marching cubes from the same SDF)
from skimage.measure import marching_cubes
h = 0.006
clo = np.array(C["lo"]) - 0.12; chi = np.array(C["hi"]) + 0.12; clo[2] = -0.01
cx = [clo[a] + np.arange(int((chi[a] - clo[a]) / h) + 1) * h for a in range(3)]
CX, CY, CZ = np.meshgrid(*cx, indexing="ij")
cv, cf, _, _ = marching_cubes(C["sdf"](CX, CY, CZ).astype(np.float32), 0.0, spacing=(h, h, h))
np.savez(f"{A.out}/container.npz", v=(cv + clo).astype(np.float32), f=cf.astype(np.int32))
del CX, CY, CZ

# particles (lattice spacing dx/2, light jitter)
s = DX / 2
rng = np.random.default_rng(7)
pl = [np.arange(C["lo"][a] - 0.1, C["hi"][a] + 0.1, s) for a in range(3)]
PX, PY, PZ = np.meshgrid(*pl, indexing="ij")
m = C["fill"](PX, PY, PZ)
fillp = np.stack([PX[m], PY[m], PZ[m]], -1)
del PX, PY, PZ
if OBJ:
    ballp = np.zeros((0, 3))
else:
    b = np.arange(-br, br + s, s)
    BX, BY, BZ = np.meshgrid(b, b, b, indexing="ij")
    mb = BX ** 2 + BY ** 2 + BZ ** 2 < br ** 2
    ballp = np.stack([BX[mb] + bx, BY[mb] + by, BZ[mb] + bz], -1)
P = np.concatenate([fillp, ballp]).astype(np.float32)
P += (rng.random(P.shape, dtype=np.float32) - 0.5) * 0.3 * s
NF, NB = len(fillp), len(ballp)
N = NF + NB
SURF = float(fillp[:, 2].max())
print("particles fill", NF, "ball", NB, "surface", round(SURF, 3), flush=True)

ti.init(arch=ti.cpu, default_fp=ti.f32, cpu_max_num_threads=os.cpu_count())
inv_dx = 1.0 / DX
p_vol = s ** 3
p_mass = p_vol
OR = float(br) if OBJ else -1.0
x = ti.Vector.field(3, float, N)
v = ti.Vector.field(3, float, N)
Cm = ti.Matrix.field(3, 3, float, N)
J = ti.field(float, N)
st = ti.field(int, N)  # 0 held, 1 active, 2 gone
gv = ti.Vector.field(3, float, tuple(n))
gm = ti.field(float, tuple(n))
ph = ti.field(float, tuple(n))
nr = ti.Vector.field(3, float, tuple(n))
oc = ti.Vector.field(3, float, ())
ov = ti.Vector.field(3, float, ())
LO = ti.Vector(list(lo.astype(np.float32)))
HIc = ti.Vector(list((hi - 3 * DX).astype(np.float32)))
LOc = ti.Vector([lo[0] + 3 * DX, lo[1] + 3 * DX, -1.0])
NG = ti.Vector(list(n))
x.from_numpy(P)
v.fill(0); Cm.fill(0)
Jn = np.ones(N, np.float32)
Jn[:NF] = 1.0 - 9.81 * np.clip(SURF - P[:NF, 2], 0, None) / K      # hydrostatic start
J.from_numpy(Jn)
stn = np.ones(N, np.int32); stn[NF:] = 0
st.from_numpy(stn)
ph.from_numpy(phi); nr.from_numpy(g.astype(np.float32))
oc[None] = [bx, by, bz]; ov[None] = [0.0, 0.0, 0.0]
del phi, g


@ti.kernel
def substep(dt: float, K: float, mu: float, fric: float):
    for I in ti.grouped(gm):
        gv[I] = ti.Vector.zero(float, 3)
        gm[I] = 0.0
    for p in x:
        if st[p] == 1:
            Xp = (x[p] - LO) * inv_dx
            base = int(Xp - 0.5)
            fx = Xp - base
            w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1) ** 2, 0.5 * (fx - 0.5) ** 2]
            sig = K * (J[p] - 1.0) * ti.Matrix.identity(float, 3) + mu * (Cm[p] + Cm[p].transpose())
            affine = -dt * p_vol * 4 * inv_dx * inv_dx * sig + p_mass * Cm[p]
            for i, j, k in ti.static(ti.ndrange(3, 3, 3)):
                off = ti.Vector([i, j, k])
                dpos = (off - fx) * DX
                wt = w[i][0] * w[j][1] * w[k][2]
                gv[base + off] += wt * (p_mass * v[p] + affine @ dpos)
                gm[base + off] += wt * p_mass
    for I in ti.grouped(gm):
        if gm[I] > 0:
            vv = gv[I] / gm[I]
            vv.z -= dt * 9.81
            if ph[I] < 0.0:
                nn = nr[I]
                vn = vv.dot(nn)
                if vn < 0:
                    vt = vv - vn * nn
                    tl = vt.norm()
                    vv = vt * ti.max(0.0, 1.0 - fric * (-vn) / (tl + 1e-6))
            if OR > 0:
                rel = LO + I * DX - oc[None]
                dd = rel.norm()
                if dd < OR + 0.5 * DX:
                    on = rel / (dd + 1e-6)
                    vn2 = (vv - ov[None]).dot(on)
                    if vn2 < 0:
                        vv -= vn2 * on
            gv[I] = vv
    for p in x:
        if st[p] == 1:
            Xp = (x[p] - LO) * inv_dx
            base = int(Xp - 0.5)
            fx = Xp - base
            w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1) ** 2, 0.5 * (fx - 0.5) ** 2]
            nv = ti.Vector.zero(float, 3)
            nC = ti.Matrix.zero(float, 3, 3)
            for i, j, k in ti.static(ti.ndrange(3, 3, 3)):
                off = ti.Vector([i, j, k])
                dpos = (off - fx) * DX
                wt = w[i][0] * w[j][1] * w[k][2]
                gg = gv[base + off]
                nv += wt * gg
                nC += 4 * inv_dx * inv_dx * wt * gg.outer_product(dpos)
            v[p] = nv
            Cm[p] = nC
            x[p] += dt * nv
            J[p] = ti.min(ti.max(J[p] * (1 + dt * nC.trace()), 0.6), 1.0)
            gi = ti.min(ti.max(int((x[p] - LO) * inv_dx + 0.5), 0), NG - 1)
            d = ph[gi]
            if d < 0.0:
                nn = nr[gi]
                x[p] -= d * nn
                vn = v[p].dot(nn)
                if vn < 0:
                    v[p] -= vn * nn
            if OR > 0:
                rp = x[p] - oc[None]
                dp = rp.norm()
                if dp < OR:
                    on = rp / (dp + 1e-6)
                    x[p] = oc[None] + on * OR
                    vn3 = (v[p] - ov[None]).dot(on)
                    if vn3 < 0:
                        v[p] -= vn3 * on
            if x[p].x < LOc.x or x[p].y < LOc.y or x[p].x > HIc.x or x[p].y > HIc.y or x[p].z > HIc.z:
                st[p] = 2


@ti.kernel
def release(vz: float):
    for p in x:
        if st[p] == 0:
            st[p] = 1
            v[p] = ti.Vector([0.0, 0.0, vz])


# steel ball: vertical dynamics with buoyancy, added mass, linear + quadratic drag
zc = np.linspace(0, C["rim"] + 1.0, 4000)
sd_col = C["sdf"](np.full_like(zc, bx), np.full_like(zc, by), zc)
ok = np.where((sd_col >= br) & (zc < SURF))[0]
ZREST = float(zc[ok[0]]) if len(ok) else 0.0
VOL = 4 / 3 * math.pi * br ** 3
M = STEEL_RHO * VOL
obj = dict(z=bz, v=0.0, held=True)


def obj_step(dt):
    if obj["held"]:
        return
    z, vz = obj["z"], obj["v"]
    hh = min(max(SURF - (z - br), 0.0), 2 * br)
    vsub = math.pi * hh * hh * (3 * br - hh) / 3
    frac = vsub / VOL
    rf = FL["rho"]
    F = -M * 9.81 + rf * vsub * 9.81 - FL["lin"] * M * vz * frac \
        - 0.25 * rf * math.pi * br * br * abs(vz) * vz * frac
    vz += dt * F / (M + 0.5 * rf * vsub)
    z += dt * vz
    if z < ZREST:
        z, vz = ZREST, (-0.15 * vz if vz < -0.3 else 0.0)
    obj["z"], obj["v"] = z, vz


c = math.sqrt(K)
dt_max = min(0.6 * DX / (c + 4.0), 0.4 * DX * DX / (FL["mu"] * 4 + 1e-9))
NSUB = max(1, math.ceil((1 / FPS) / dt_max))
DT = (1 / FPS) / NSUB
print("substeps/frame", NSUB, flush=True)


def step_frame():
    for _ in range(NSUB):
        if OBJ:
            obj_step(DT)
            oc[None] = [bx, by, obj["z"]]
            ov[None] = [0.0, 0.0, obj["v"]]
        substep(DT, K, FL["mu"], FL["fric"])


import pysplashsurf


def recon(fr):
    pts = x.to_numpy()[st.to_numpy() != 2].astype(np.float64)
    res = pysplashsurf.reconstruction_pipeline(
        pts, particle_radius=s * 0.62, rest_density=1000.0, smoothing_length=2.3, cube_size=0.65,
        iso_surface_threshold=0.6, mesh_smoothing_iters=35, mesh_smoothing_weights=True,
        normals_smoothing_iters=15, compute_normals=True, mesh_cleanup=True, decimate_barnacles=True)
    mesh = res[0] if isinstance(res, tuple) else res
    mm = mesh.mesh if hasattr(mesh, "mesh") else mesh
    vv = np.asarray(mm.vertices, np.float32)
    ff = np.asarray(mm.triangles if hasattr(mm, "triangles") else mm.cells, np.int32)
    np.savez(f"{A.out}/mesh_{fr:04d}.npz", v=vv, f=ff)
    return len(vv)


t0 = time.time()
for _ in range(PREROLL):
    step_frame()
ZS = []
for fr in range(1, NFR + 1):
    t = time.time()
    if fr == HOVER + 1:
        if OBJ:
            obj["held"], obj["v"] = False, -1.0
        else:
            release(FL["v0"])
    if fr > 1:
        step_frame()
    ZS.append(obj["z"])
    nv = recon(fr)
    print(f"FRAME {fr} {time.time()-t:.1f}s verts {nv}", flush=True)

impact = HOVER + 1 + ((-abs(FL["v0"]) + math.sqrt(FL["v0"] ** 2 + 2 * 9.81 * max(0.0, (bz - br) - SURF))) / 9.81) * FPS
if OBJ:
    impact = next((j + 1 for j, z in enumerate(ZS) if z - br <= SURF), HOVER + 1)
json.dump(dict(container=A.container, fluid=A.fluid, mode=A.mode, frames=NFR, hover=HOVER, fps=FPS,
               surface=SURF, impact_frame=float(impact), obj=dict(x=bx, y=by, r=br, z=ZS) if OBJ else None),
          open(f"{A.out}/meta.json", "w"))
print("DONE", round(time.time() - t0), flush=True)
