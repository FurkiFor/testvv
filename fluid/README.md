# fluid/ — asmrvideo comparison Shorts (3D fluid simulation)

Format (since 2026-10-20): **one scene, four substances, side-by-side comparison** — the formula of
"Fluid Simulation with Bath" (Kawaken 3DCG, 2.6M views), but the container changes every video.

| mode | what happens | label on screen |
|---|---|---|
| `ball` | container full of X, a sphere of the same X drops in, 4 substances in a row | `Water` / `Honey` … |
| `object` | the same steel ball drops into 4 liquids (glass container so the sinking is visible); the last one is always mercury — the steel ball floats | `Steel Ball into` + `Mercury` |

Each segment is 66 frames (2.2 s, 5 hover frames → release); a video is 4 segments ≈ 8.8 s and loops.
Text on screen is ON (the comparison needs the names); `assemble.py --clean` also writes a text-free copy.

## Pipeline

```
plan.py --date D      -> plan.json (3 videos: 12:00 ball, 17:00 object, 21:00 ball; container/fluid sets rotate by date)
segment.sh C M F OUT  -> sim.py (Taichi MLS-MPM, CPU) -> OUT/sim/mesh_*.npz
                      -> render.py (Blender 5.2 bpy, Cycles CPU) -> OUT/frames/*.png
assemble.py           -> videos/asmrvideo/<id>.mp4 (1080x1920, labels, ElevenLabs SFX synced to impact)
                      -> fluid/runs/D.json (manifest: title, caption, tags, url, status)
```

* `containers.py` — every container is an SDF; the same function drives collisions and the visible mesh
  (marching cubes). Add a container = add one function. Walls must be ≥ 5 cm (≥ 2.5 cells at dx = 0.02),
  thinner walls leak.
* `fluids.py` — viscosity, wall friction, density (buoyancy of the steel ball), label and SFX per substance.
* `sfx/` — pre-generated ElevenLabs sound effects (one or two per substance). No API calls at run time.
* `fonts/Poppins-Bold.ttf` — label font (SIL Open Font License).

## Cost

CPU only. One segment on 2 cores ≈ 20 min sim + 35 min render (bowl, 605x1075, 24 spp). On a 4-core
GitHub runner ≈ 35–45 min at 720x1280. 3 videos = 12 segments → run them in parallel (one job each).

## Local run

```
bash fluid/setup.sh
python3 fluid/plan.py --date 2026-10-21 --out plan.json
bash fluid/segment.sh bowl ball honey /tmp/seg/<video id>/honey
python3 fluid/assemble.py --plan plan.json --segs /tmp/seg --outdir videos/asmrvideo --manifest fluid/runs/2026-10-21.json
```

The old `engine/` (cube/sphere/marble/domino loops) is retired; nothing here depends on it.
