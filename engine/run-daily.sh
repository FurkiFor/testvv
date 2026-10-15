#!/usr/bin/env bash
# Render the day's asmrvideo Shorts. Usage: bash engine/run-daily.sh --date YYYY-MM-DD --count 3
# Long job (~5 min per video): run it in the background and poll the log, e.g.
#   nohup bash engine/run-daily.sh --date 2026-10-16 --count 3 > /tmp/asmr-daily.log 2>&1 &
set -euo pipefail
cd "$(dirname "$0")"
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}"
[ -d node_modules/three ] || npm install --no-audit --no-fund
python3 -c "import numpy, scipy" 2>/dev/null || pip install --break-system-packages -q numpy scipy
node daily.mjs "$@"
