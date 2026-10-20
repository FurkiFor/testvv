"""Daily plan: 3 comparison Shorts, chosen deterministically from the Dubai date.
usage: python3 plan.py --date YYYY-MM-DD [--out plan.json]
Slots: 12:00 ball mode, 17:00 object mode (steel ball), 21:00 ball mode (other container/set).
"""
import argparse, json, datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluids import FLUIDS

BALL_CONTAINERS = ["bowl", "bathtub", "bucket", "pot", "aquarium"]
OBJ_CONTAINERS = ["tumbler", "aquarium"]
BALL_SETS = [
    ["water", "blood", "honey", "copper"],
    ["water", "milk", "chocolate", "lava"],
    ["water", "oil", "slime", "mercury"],
    ["milk", "honey", "chocolate", "copper"],
    ["water", "slime", "lava", "mercury"],
    ["oil", "blood", "honey", "lava"],
]
OBJ_SETS = [  # mercury last: the steel ball floats -> payoff
    ["water", "oil", "honey", "mercury"],
    ["water", "milk", "chocolate", "mercury"],
    ["water", "slime", "lava", "mercury"],
    ["water", "honey", "copper", "mercury"],
]
CONT_NAME = dict(bowl="Giant Bowl", bathtub="Bathtub", bucket="Bucket", pot="Cooking Pot", aquarium="Glass Tank",
                 tumbler="Giant Glass")
BASE_TAGS = ["fluid simulation", "fluid simulation satisfying", "blender fluid simulation", "water simulation blender",
             "fluid simulation blender", "blender simulation", "liquid simulation", "satisfying", "satisfying video",
             "asmr", "physics simulation", "3d animation", "blender", "shorts"]


def title_for(v):
    names = [FLUIDS[f]["label"] for f in v["fluids"]]
    if v["mode"] == "object":
        return f"Steel Ball vs {', '.join(names[:-1])} & {names[-1]} 😳 #shorts"
    return f"{' vs '.join(names)} in a {CONT_NAME[v['container']]} 🫧 #shorts"


def caption_for(v):
    names = [FLUIDS[f]["label"] for f in v["fluids"]]
    if v["mode"] == "object":
        head = (f"What happens when the same steel ball drops into {', '.join(names[:-1])} and {names[-1]}? "
                f"Watch the last one 👀")
    else:
        head = f"Same drop, four liquids: {', '.join(names)}. Which one is the most satisfying?"
    return (head + "\n\n3D fluid simulation rendered in Blender (Cycles). Sound on 🔊\n\n"
            "#fluidsimulation #satisfying #asmr #blender #physics #shorts")


def plan(date):
    d = datetime.date.fromisoformat(date)
    k = d.toordinal()
    v1c = BALL_CONTAINERS[(k + 1) % len(BALL_CONTAINERS)]
    v3c = BALL_CONTAINERS[(k + 3) % len(BALL_CONTAINERS)]
    vids = [
        dict(slot="12:00", mode="ball", container=v1c, fluids=BALL_SETS[k % len(BALL_SETS)]),
        dict(slot="17:00", mode="object", container=OBJ_CONTAINERS[k % len(OBJ_CONTAINERS)],
             fluids=OBJ_SETS[k % len(OBJ_SETS)]),
        dict(slot="21:00", mode="ball", container=v3c, fluids=BALL_SETS[(k + 3) % len(BALL_SETS)]),
    ]
    for i, v in enumerate(vids, 1):
        v["id"] = f"{date}-{i}-{v['mode']}-{v['container']}"
        v["title"] = title_for(v)
        v["caption"] = caption_for(v)
        v["tags"] = BASE_TAGS + [FLUIDS[f]["label"].lower() for f in v["fluids"]] + [CONT_NAME[v["container"]].lower()]
    return dict(date=date, videos=vids)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--out", default="plan.json")
    a = ap.parse_args()
    p = plan(a.date)
    json.dump(p, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(json.dumps(p, indent=1, ensure_ascii=False))
