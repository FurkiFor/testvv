#!/bin/bash
# Installs the two Python environments (sim: Py3.11 + Taichi, render: Py3.13 + Blender bpy 5.2).
set -e
command -v uv >/dev/null || python3 -m pip install --user -q uv || pip install -q --break-system-packages uv
export PATH="$HOME/.local/bin:$PATH"
SIM=${FLUID_SIM_ENV:-$HOME/fluidenv-sim}; REN=${FLUID_RENDER_ENV:-$HOME/fluidenv-render}
[ -x $SIM/bin/python ] || { uv python install 3.11 >/dev/null; uv venv -q -p 3.11 $SIM; }
uv pip install -q -p $SIM taichi==1.7.4 pysplashsurf scikit-image numpy
[ -x $REN/bin/python ] || { uv python install 3.13 >/dev/null; uv venv -q -p 3.13 $REN; }
uv pip install -q -p $REN bpy==5.2.2 numpy
$SIM/bin/python -c "import taichi, pysplashsurf, skimage; print('sim env ok')"
$REN/bin/python -c "import bpy; print('render env ok', bpy.app.version_string)"
