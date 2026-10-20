"""Build the final Shorts from rendered segments: 1080x1920, labels, impact-synced SFX.
usage: python3 assemble.py --plan plan.json --segs SEGDIR --outdir videos/asmrvideo [--manifest fluid/runs/D.json]
SEGDIR/<video id>/<fluid>/{frames/*.png, meta.json}
Videos with a missing segment are skipped (and listed as failed in the manifest).
"""
import argparse, json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fluids import FLUIDS

ap = argparse.ArgumentParser()
ap.add_argument("--plan", required=True)
ap.add_argument("--segs", required=True)
ap.add_argument("--outdir", required=True)
ap.add_argument("--manifest")
ap.add_argument("--raw-base", default="https://raw.githubusercontent.com/FurkiFor/testvv/main")
ap.add_argument("--clean", action="store_true", help="also write a version without text")
A = ap.parse_args()
FONT = f"{HERE}/fonts/Poppins-Bold.ttf"
P = json.load(open(A.plan))
os.makedirs(A.outdir, exist_ok=True)


def sfx_info(name):
    a = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f"{HERE}/sfx/{name}.mp3", "-ac", "1", "-ar", "22050",
                        "-f", "f32le", "-"], capture_output=True, check=True).stdout
    sig = np.frombuffer(a, np.float32)
    env = np.sqrt(np.convolve(sig * sig, np.ones(441) / 441, "same"))
    return np.argmax(env > 0.3 * env.max()) / 22050, min(6.0, 0.32 / max(env.max(), 1e-4))


def pick_sfx(fl, used):
    for n in FLUIDS[fl]["sfx"]:
        if os.path.exists(f"{HERE}/sfx/{n}.mp3") and n not in used:
            return n
    return next(n for n in FLUIDS[fl]["sfx"] + ["water1"] if os.path.exists(f"{HERE}/sfx/{n}.mp3"))


def build(v, labeled, out):
    segs, used = [], set()
    t0 = 0.0
    for fl in v["fluids"]:
        d = f"{A.segs}/{v['id']}/{fl}"
        meta = json.load(open(f"{d}/meta.json"))
        nf = len([f for f in os.listdir(f"{d}/frames") if f.endswith(".png")])
        if nf < meta["frames"]:
            raise RuntimeError(f"{v['id']}/{fl}: only {nf}/{meta['frames']} frames")
        sname = pick_sfx(fl, used); used.add(sname)
        onset, gain = sfx_info(sname)
        t_imp = t0 + (meta["impact_frame"] - 1) / meta["fps"]
        segs.append(dict(fl=fl, pat=f"{d}/frames/%04d.png", fps=meta["fps"], sfx=sname,
                         delay=max(0, int((t_imp - onset) * 1000)), gain=gain))
        t0 += meta["frames"] / meta["fps"]
    total = t0
    cmd = ["ffmpeg", "-loglevel", "error", "-y"]
    for s in segs:
        cmd += ["-framerate", str(s["fps"]), "-i", s["pat"]]
    for s in segs:
        cmd += ["-i", f"{HERE}/sfx/{s['sfx']}.mp3"]
    fc = []
    for i, s in enumerate(segs):
        f = f"[{i}:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0.0,setsar=1"
        if labeled:
            lab = FLUIDS[s["fl"]]["label"]
            y = 250
            if v["mode"] == "object":
                f += (f",drawtext=fontfile={FONT}:text='Steel Ball into':fontsize=58:fontcolor=white:"
                      f"borderw=4:bordercolor=black@0.85:x=(w-text_w)/2:y=200")
                y = 300
            size = 118 if len(lab) <= 10 else 96
            f += (f",drawtext=fontfile={FONT}:text='{lab}':fontsize={size}:fontcolor=white:"
                  f"borderw=6:bordercolor=black@0.85:x=(w-text_w)/2:y={y}")
        fc.append(f + f"[v{i}]")
    fc.append("".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0[vout]")
    for j, s in enumerate(segs):
        fc.append(f"[{len(segs)+j}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={s['gain']:.3f},"
                  f"adelay={s['delay']}|{s['delay']}[a{j}]")
    fc.append("".join(f"[a{j}]" for j in range(len(segs))) +
              f"amix=inputs={len(segs)}:normalize=0,apad,atrim=0:{total:.3f},"
              f"afade=t=out:st={total-0.08:.3f}:d=0.08,alimiter=limit=0.9[aout]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow",
            "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    return segs


man = dict(date=P["date"], videos=[])
for v in P["videos"]:
    out = f"{A.outdir}/{v['id']}.mp4"
    rec = {k: v[k] for k in ("id", "slot", "mode", "container", "fluids", "title", "caption", "tags")}
    try:
        segs = build(v, True, out)
        if A.clean:
            build(v, False, f"{A.outdir}/{v['id']}-clean.mp4")
        rec.update(file=out, url=f"{A.raw_base}/{out}", sfx=[s["sfx"] for s in segs], status="ok")
        print("OK", out, flush=True)
    except Exception as e:
        rec.update(status="failed", error=str(e)[:300])
        print("FAILED", v["id"], e, flush=True)
    man["videos"].append(rec)
if A.manifest:
    os.makedirs(os.path.dirname(A.manifest), exist_ok=True)
    json.dump(man, open(A.manifest, "w"), indent=1, ensure_ascii=False)
print(json.dumps(man, indent=1, ensure_ascii=False))
