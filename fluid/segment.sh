#!/bin/bash
# One comparison segment: simulate + render.  Output: OUT/meta.json, OUT/frames/0001.png ...
# usage: segment.sh <container> <ball|object> <fluid> <OUT> [frames=66] [pct=67] [samples=24]
set -eo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
CONT=$1; MODE=$2; FL=$3; OUT=$4; NF=${5:-66}; PCT=${6:-67}; SMP=${7:-24}
SIM=${FLUID_SIM_ENV:-$HOME/fluidenv-sim}; REN=${FLUID_RENDER_ENV:-$HOME/fluidenv-render}
mkdir -p "$OUT/frames"
if [ ! -f "$OUT/sim/meta.json" ]; then
  $SIM/bin/python "$HERE/sim.py" --container $CONT --mode $MODE --fluid $FL --out "$OUT/sim" --frames $NF 2>&1 \
    | grep --line-buffered -vE '^\[Taichi\]'
fi
DONE=$(ls "$OUT/frames" | wc -l)
if [ "$DONE" -lt "$NF" ]; then
  $REN/bin/python "$HERE/render.py" --src "$OUT/sim" --dst "$OUT/frames" --pct $PCT --samples $SMP --start $((DONE>0?DONE:1)) 2>&1 \
    | grep --line-buffered -E 'RFRAME|Error|Traceback|line [0-9]+' | grep -v CUEW
fi
cp "$OUT/sim/meta.json" "$OUT/meta.json"
[ "$(ls "$OUT/frames" | wc -l)" -ge "$NF" ] && echo "SEGMENT_OK $CONT $MODE $FL"
