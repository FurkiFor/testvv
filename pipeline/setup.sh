#!/usr/bin/env bash
# One-time setup for a fresh session: TTS model, Python deps, fonts.
set -euo pipefail
P="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$P/.models" "$P/.fonts"
cd "$P/.models"
[ -s kokoro-v1.0.onnx ] || curl -sSL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s voices-v1.0.bin ] || curl -sSL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
pip install -q --break-system-packages kokoro-onnx soundfile scipy playwright 2>&1 | grep -v WARNING || true
python3 -c "from playwright.sync_api import sync_playwright as s; b=s().start().chromium.launch(); b.close()" 2>/dev/null || python3 -m playwright install chromium
cd "$P/.fonts"
for pkg in @fontsource/anton @fontsource/manrope; do
  name=$(echo "$pkg" | sed 's|@fontsource/|fontsource-|')
  if ! ls -d ${name}-* >/dev/null 2>&1; then
    tgz=$(npm pack "$pkg" --silent | tail -1); mkdir -p tmp && tar xzf "$tgz" -C tmp && mv tmp/package "${tgz%.tgz}" && rm -rf tmp "$tgz"
  fi
done
# template expects these stable names
[ -e fontsource-anton-5.3.0 ] || ln -s "$(ls -d fontsource-anton-* | head -1)" fontsource-anton-5.3.0
[ -e fontsource-manrope-5.3.0 ] || ln -s "$(ls -d fontsource-manrope-* | head -1)" fontsource-manrope-5.3.0
fc-list : family | grep -i "color emoji" >/dev/null || echo "WARNING: no system Noto Color Emoji font — emoji will not render"
echo "setup ok"
