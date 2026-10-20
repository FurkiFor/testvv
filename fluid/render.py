"""Cycles render of one simulated segment (run with the bpy module, Python 3.13).
usage: python render.py --src SIMDIR --dst FRAMEDIR [--pct 67] [--samples 24] [--start 1]
"""
import argparse, os, sys, time, json
import numpy as np
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import containers

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--dst", required=True)
ap.add_argument("--pct", type=int, default=67)
ap.add_argument("--samples", type=int, default=24)
ap.add_argument("--start", type=int, default=1)
A = ap.parse_args()
META = json.load(open(f"{A.src}/meta.json"))
C = containers.get(META["container"])
FLUID, NF = META["fluid"], META["frames"]
os.makedirs(A.dst, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


def link(o):
    scene.collection.objects.link(o)
    return o


def mesh_data(name, v, f):
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(v)); me.vertices.foreach_set("co", v.ravel())
    me.loops.add(f.size); me.loops.foreach_set("vertex_index", f.ravel())
    me.polygons.add(len(f)); me.polygons.foreach_set("loop_start", np.arange(0, f.size, 3, dtype=np.int32))
    me.update(calc_edges=True)
    me.shade_smooth()
    return me


def mat(name, vol=None, emit=None, **kw):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    for k, val in kw.items():
        b.inputs[k].default_value = val
    if vol:
        va = nt.nodes.new("ShaderNodeVolumeAbsorption")
        va.inputs["Color"].default_value = vol[0]
        va.inputs["Density"].default_value = vol[1]
        nt.links.new(va.outputs[0], nt.nodes["Material Output"].inputs["Volume"])
    if emit:   # lava: glowing cracks between dark crust (noise driven)
        tc = nt.nodes.new("ShaderNodeTexCoord")
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 9.0
        nz.inputs["Detail"].default_value = 6.0
        nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
        cr = nt.nodes.new("ShaderNodeValToRGB")
        cr.color_ramp.elements[0].position = 0.42; cr.color_ramp.elements[0].color = (1, 1, 1, 1)
        cr.color_ramp.elements[1].position = 0.58; cr.color_ramp.elements[1].color = (0, 0, 0, 1)
        nt.links.new(nz.outputs["Fac"], cr.inputs["Fac"])
        mu = nt.nodes.new("ShaderNodeMath"); mu.operation = "MULTIPLY"; mu.inputs[1].default_value = emit[1]
        nt.links.new(cr.outputs["Color"], mu.inputs[0])
        b.inputs["Emission Color"].default_value = emit[0]
        nt.links.new(mu.outputs[0], b.inputs["Emission Strength"])
    return m


CONT_MATS = {
    "ceramic": dict(**{"Base Color": (0.93, 0.93, 0.91, 1), "Roughness": 0.14, "Coat Weight": 0.7, "Coat Roughness": 0.03}),
    "glass": dict(**{"Base Color": (0.97, 0.99, 1.0, 1), "Transmission Weight": 1.0, "Roughness": 0.0, "IOR": 1.5}),
    "plastic": dict(**{"Base Color": (0.55, 0.78, 0.95, 1), "Roughness": 0.32}),
    "steel": dict(**{"Base Color": (0.86, 0.86, 0.87, 1), "Metallic": 1.0, "Roughness": 0.22, "Anisotropic": 0.4}),
}
T = "Transmission Weight"
LIQ = {
    "water": (dict(**{"Base Color": (0.85, 0.97, 1.0, 1), T: 1.0, "Roughness": 0.0, "IOR": 1.33}), ((0.55, 0.88, 0.96, 1), 1.0), None),
    "blood": (dict(**{"Base Color": (0.17, 0.004, 0.007, 1), "Roughness": 0.06, "Specular IOR Level": 0.8,
                      "Coat Weight": 0.6, "Coat Roughness": 0.02}), None, None),
    "honey": (dict(**{"Base Color": (1.0, 0.78, 0.32, 1), T: 1.0, "Roughness": 0.02, "IOR": 1.49}), ((1.0, 0.62, 0.12, 1), 1.1), None),
    "copper": (dict(**{"Base Color": (0.97, 0.56, 0.34, 1), "Metallic": 1.0, "Roughness": 0.13}), None, None),
    "oil": (dict(**{"Base Color": (1.0, 0.92, 0.55, 1), T: 1.0, "Roughness": 0.0, "IOR": 1.47}), ((1.0, 0.86, 0.35, 1), 0.7), None),
    "mercury": (dict(**{"Base Color": (0.86, 0.87, 0.89, 1), "Metallic": 1.0, "Roughness": 0.04}), None, None),
    "milk": (dict(**{"Base Color": (0.96, 0.95, 0.92, 1), "Roughness": 0.15, "Subsurface Weight": 1.0,
                     "Subsurface Radius": (0.6, 0.5, 0.35), "Subsurface Scale": 0.05}), None, None),
    "slime": (dict(**{"Base Color": (0.35, 1.0, 0.35, 1), T: 0.85, "Roughness": 0.05, "IOR": 1.4}), ((0.35, 1.0, 0.3, 1), 1.5), None),
    "chocolate": (dict(**{"Base Color": (0.11, 0.045, 0.02, 1), "Roughness": 0.18, "Coat Weight": 0.5,
                          "Coat Roughness": 0.08}), None, None),
    "lava": (dict(**{"Base Color": (0.06, 0.03, 0.025, 1), "Roughness": 0.55}), None, ((1.0, 0.30, 0.04, 1), 4.0)),
}

cz = np.load(f"{A.src}/container.npz")
cont = link(bpy.data.objects.new("Container", mesh_data("Container", cz["v"], cz["f"])))
cont.data.materials.append(mat("ContMat", **CONT_MATS[C["material"]]))
fl = mesh_data("Floor", np.array([[-30, -30, -0.002], [30, -30, -0.002], [30, 30, -0.002], [-30, 30, -0.002]], np.float32),
               np.array([[0, 1, 2], [0, 2, 3]], np.int32))
floor = link(bpy.data.objects.new("Floor", fl))
floor.data.materials.append(mat("Floor", **{"Base Color": (0.30, 0.30, 0.31, 1), "Roughness": 0.6}))
lm, lvol, lemit = LIQ[FLUID]
liq_mat = mat(f"Liquid_{FLUID}", vol=lvol, emit=lemit, **lm)
liq = link(bpy.data.objects.new("Liquid", bpy.data.meshes.new("empty")))

ball = None
if META.get("obj"):
    import bmesh
    O = META["obj"]
    bmm = bmesh.new(); bmesh.ops.create_uvsphere(bmm, u_segments=64, v_segments=32, radius=O["r"])
    bme = bpy.data.meshes.new("Ball"); bmm.to_mesh(bme); bmm.free(); bme.shade_smooth()
    ball = link(bpy.data.objects.new("Ball", bme))
    ball.data.materials.append(mat("Steel", **{"Base Color": (0.9, 0.9, 0.92, 1), "Metallic": 1.0, "Roughness": 0.06}))
    btop = O["z"][0] + O["r"]
else:
    bx, by, bz, br = C["ball"]
    btop = bz + br

hx = max(abs(C["lo"][0]), C["hi"][0]); hy = max(abs(C["lo"][1]), C["hi"][1]); top = C["hi"][2]
target = link(bpy.data.objects.new("Target", None))
target.location = (0.0, 0.0, top * 0.5 + 0.12)
cam = link(bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")))
cam.data.lens = 35
W = max(hx, hy) * 1.15 + 0.35
dist = max(W / (10.125 / 35), (btop + 0.1) / (18 / 35) * 1.05)
cam.location = target.location + Vector((0.52, -0.66, 0.62)).normalized() * dist
tc = cam.constraints.new("TRACK_TO"); tc.target = target; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
scene.camera = cam


def area(name, loc, size, energy, color=(1, 1, 1)):
    l = bpy.data.lights.new(name, "AREA"); l.size = size; l.energy = energy; l.color = color
    o = link(bpy.data.objects.new(name, l)); o.location = loc
    c = o.constraints.new("TRACK_TO"); c.target = target; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"


area("Key", (-2.4, -2.0, 4.4), 3.0, 1000)
area("Fill", (3.4, -1.2, 2.2), 3.5, 260, (0.95, 0.97, 1.0))
area("Rim", (0.6, 3.2, 3.2), 2.5, 420)
world = bpy.data.worlds.new("W"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.57, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.35

r = scene.render
r.engine = "CYCLES"
r.resolution_x, r.resolution_y = 1080, 1920
r.resolution_percentage = A.pct
r.use_persistent_data = True
cy = scene.cycles
cy.device = "CPU"
cy.samples = A.samples
cy.use_adaptive_sampling = True
cy.adaptive_threshold = 0.04
cy.use_denoising = True
cy.denoiser = "OPENIMAGEDENOISE"
cy.max_bounces = 8; cy.diffuse_bounces = 2; cy.glossy_bounces = 4
cy.transmission_bounces = 8; cy.volume_bounces = 0; cy.transparent_max_bounces = 4
cy.caustics_reflective = False; cy.caustics_refractive = False
cy.blur_glossy = 1.0
scene.view_settings.view_transform = "AgX"
try:
    scene.view_settings.look = "AgX - Medium High Contrast"
except Exception:
    pass
r.image_settings.file_format = "PNG"
r.image_settings.color_mode = "RGB"

for fr in range(A.start, NF + 1):
    t = time.time()
    npz = np.load(f"{A.src}/mesh_{fr:04d}.npz")
    old = liq.data
    liq.data = mesh_data(f"L{fr}", npz["v"], npz["f"])
    liq.data.materials.append(liq_mat)
    bpy.data.meshes.remove(old)
    if ball:
        ball.location = (META["obj"]["x"], META["obj"]["y"], META["obj"]["z"][fr - 1])
    r.filepath = f"{A.dst}/{fr:04d}.png"
    bpy.ops.render.render(write_still=True)
    print(f"RFRAME {fr} {time.time()-t:.1f}s", flush=True)
