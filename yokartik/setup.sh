#!/usr/bin/env bash
# Yok Artık motoru için bağımlılıklar (idempotent)
set -e
cd "$(dirname "$0")"
if [ ! -d assets/tw/package ]; then
  mkdir -p assets/tw
  (cd assets && npm pack @twemoji/svg --silent >/dev/null && tar -xzf twemoji-svg-*.tgz -C tw && rm -f twemoji-svg-*.tgz)
fi
python3 -c "import cairosvg, PIL, numpy" 2>/dev/null || pip install -q --break-system-packages cairosvg pillow numpy
command -v ffmpeg >/dev/null || { echo "ffmpeg yok"; exit 1; }
ls /usr/share/fonts/opentype/inter/InterDisplay-Black.otf >/dev/null
echo "setup ok"
