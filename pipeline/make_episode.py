#!/usr/bin/env python3
"""History Group Chat — build one Short from an episode JSON.

usage: python3 make_episode.py episodes/<slug>.json
output: out/<slug>.mp4 (1080x1920, H.264/AAC, -14 LUFS) and out/<slug>_sheet.png (6 check frames)
"""
import json, os, sys, subprocess, shutil
import numpy as np, soundfile as sf

P = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(P, '.models')
FONTS = os.path.join(P, '.fonts')
FPS = 30
MAX_LEN = 59.0

ep_path = os.path.abspath(sys.argv[1])
ep = json.load(open(ep_path))
slug = ep['slug']
B = os.path.join(P, 'build', slug)
OUT = os.path.join(P, 'out')
os.makedirs(os.path.join(B, 'vo'), exist_ok=True); os.makedirs(OUT, exist_ok=True)
for side in ('you', 'them'):
    ep[side]['svg'] = open(os.path.join(P, 'portraits', ep[side]['portrait'])).read()
COLD = ep.get('hook', {}).get('mode') == 'none'      # no hook scene, no narrator: open straight on the chat
CUT = ep.get('ending') == 'cut'                       # no meme card: end right after the last message
ep['props'] = {}
for m in ep['chat']:
    if m.get('photo'):
        ep['props'][m['photo']] = open(os.path.join(P, 'props', m['photo'])).read()

# ---------- validation ----------
if not COLD:
    assert len(ep['hook']['lines']) in (2, 3, 4), 'hook.lines: 2-4 short lines'
    assert len(ep['notifications']) == 2, 'notifications: exactly 2'
assert ep.get('ending', 'block') in ('block', 'none', 'cut')
for m in ep['chat']:
    assert m['k'] in ('chip', 'in', 'out'), m
    if m['k'] != 'chip' and not m.get('big'):
        assert m.get('say'), f'missing say: {m}'

# ---------- voice lines ----------
nar = ep.get('narrator', {'voice': 'am_onyx', 'speed': 1.2})
LINES = ([] if COLD else [('hook', ep['hook'], nar, 0.0)]) + ([] if CUT else [('meme', ep['meme'], nar, -0.1)])
for i, m in enumerate(ep['chat']):
    if m.get('say'):
        LINES.append((f'c{i}', m, ep['you'] if m['k'] == 'out' else ep['them'], 0.0))

# `--lines`: write build/<slug>/lines.json (what ElevenLabs must speak) and stop.
if '--lines' in sys.argv:
    rows = [{'name': n, 'text': src.get('el_say', src['say']), 'voice_id': who.get('el_voice'),
             'file': os.path.join(B, 'vo_src', f'{n}.mp3')} for n, src, who, _ in LINES]
    os.makedirs(os.path.join(B, 'vo_src'), exist_ok=True)
    json.dump(rows, open(os.path.join(B, 'lines.json'), 'w'), indent=1)
    print(os.path.join(B, 'lines.json'))
    sys.exit(0)

# ElevenLabs mode: every line already has build/<slug>/vo_src/<name>.mp3|.wav
VO_SRC = os.path.join(B, 'vo_src')
def ext_file(n):
    for e in ('mp3', 'wav'):
        f = os.path.join(VO_SRC, f'{n}.{e}')
        if os.path.isfile(f) and os.path.getsize(f) > 1000: return f
EXT = all(ext_file(n) for n, *_ in LINES)
print('voice engine:', 'elevenlabs' if EXT else 'kokoro', flush=True)

def trim_save(name, a, sr):
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 240): idx[-1] + 1200]
    sf.write(os.path.join(B, 'vo', f'{name}.wav'), a, sr)
    return len(a) / sr

if EXT:
    def tts(name, who, delta, boost):
        tempo = max(0.6, min(1.9, (who.get('el_speed', 1.06) + delta * 0.5) * boost))
        tmp = os.path.join(B, 'vo', f'{name}.raw.wav')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', ext_file(name), '-af', f'atempo={tempo:.3f}',
                        '-ac', '1', '-ar', '24000', tmp], check=True)
        a, sr = sf.read(tmp); os.remove(tmp)
        return trim_save(name, a, sr)
else:
    from kokoro_onnx import Kokoro
    K = Kokoro(os.path.join(MODELS, 'kokoro-v1.0.onnx'), os.path.join(MODELS, 'voices-v1.0.bin'))
    def tts(name, who, delta, boost):
        src = dict((n, s) for n, s, *_ in LINES)[name]
        a, sr = K.create(src['say'], voice=who['voice'], speed=(who['speed'] + delta) * boost, lang='en-us')
        return trim_save(name, a, sr)

def make_voices(boost):
    return {n: tts(n, who, delta, boost) for n, src, who, delta in LINES}

# ---------- timeline ----------
def build_timeline(dur):
    tl = {"hook": {}, "msgs": [], "vo": [], "sfx": [], "end": {}}
    if COLD:
        tl["hook"] = {"end": 0.0}
        t = 0.35
    else:
        tl["sfx"] += [("whoosh", 0.0), ("ding", 0.8), ("ding", 1.3), ("ding", 1.8), ("pop", 2.2), ("pop", 2.4), ("thud", 2.8)]
        tl["vo"].append(("hook", 0.15))
        hook_end = max(0.15 + dur["hook"] + 0.35, 4.0)
        tl["hook"] = {"end": hook_end}
        t = hook_end + 0.15
    for i, m in enumerate(ep["chat"]):
        t += m.get("pause", 0)
        e = {"i": i, "k": m["k"], "text": m["text"], "time": m.get("time", ""), "quote": m.get("quote", ""), "big": m.get("big", False), "photo": m.get("photo", "")}
        vd = dur.get(f"c{i}", 0)
        if m["k"] == "chip":
            e["at"] = t; t += 0.45
        elif m["k"] == "out":
            type_len = max(vd * 0.92, 0.45)
            e["typeStart"] = t; e["typeEnd"] = t + type_len
            if vd: tl["vo"].append((f"c{i}", t + 0.05))
            e["at"] = t + max(type_len, vd) + 0.12
            tl["sfx"].append(("swoosh", e["at"]))
            n = len(m["text"])
            for c in range(n):
                if m["text"][c] != ' ':
                    tl["sfx"].append(("key", t + type_len * c / max(n, 1)))
            t = e["at"] + 0.2
        else:
            typing = m.get("typing", 0.4)
            e["dotsStart"] = t; e["at"] = t + typing
            tl["sfx"].append(("pop", e["at"]))
            if vd: tl["vo"].append((f"c{i}", e["at"] + 0.08))
            t = e["at"] + 0.08 + vd + 0.16 + (0.9 if m.get("photo") else 0)
        if m.get("sfx"):
            tl["sfx"].append((m["sfx"], e["at"] + (0.05 if m["sfx"] == "boom" else 0.0)))
        if m.get("big"):
            t += 0.6
        tl["msgs"].append(e)
    E = t
    if CUT:
        big = 1e9
        end = {k: big for k in ("tapHeader", "profile", "tapVideo", "call", "ringing", "declined", "profile2", "blocked", "meme")}
        end["total"] = E + ep.get("hold", 1.6)
        tl["end"] = end; tl["total"] = end["total"]
        return tl
    if ep.get("ending", "block") == "block":
        end = {"tapHeader": E + 0.05, "profile": E + 0.35, "tapVideo": E + 0.95, "call": E + 1.2,
               "ringing": E + 1.75, "declined": E + 2.75, "profile2": E + 3.3, "blocked": E + 3.6}
        tl["sfx"] += [("tap", end["tapHeader"]), ("tap", end["tapVideo"]), ("ring", end["call"] + 0.1),
                      ("decline", end["declined"]), ("bonk", end["blocked"]), ("boom", end["blocked"] + 0.08)]
        meme = end["blocked"] + 1.2
    else:
        big = 1e9
        end = {k: big for k in ("tapHeader", "profile", "tapVideo", "call", "ringing", "declined", "profile2", "blocked")}
        meme = E + 0.4
    end["meme"] = meme
    tl["sfx"].append(("boom", meme))
    tl["vo"].append(("meme", meme + 0.35))
    end["total"] = meme + 0.35 + dur["meme"] + 1.1
    tl["end"] = end; tl["total"] = end["total"]
    return tl

boost = 1.0
for attempt in range(4):
    dur = make_voices(boost)
    tl = build_timeline(dur)
    print(f'attempt {attempt}: speed x{boost:.2f} -> {tl["total"]:.1f}s', flush=True)
    if tl['total'] <= MAX_LEN: break
    boost *= min(1.12, (tl['total'] / MAX_LEN) ** 0.9 + 0.02)
if tl['total'] > MAX_LEN + 6:
    sys.exit(f'TOO LONG ({tl["total"]:.1f}s): cut chat lines and rerun')
json.dump(tl, open(os.path.join(B, 'timeline.json'), 'w'), indent=1)

# ---------- render frames ----------
html = open(os.path.join(P, 'template.html')).read()
html = html.replace('__FONTS__', 'file://' + FONTS).replace('__TIMELINE__', json.dumps(tl)).replace('__EPISODE__', json.dumps(ep))
page = os.path.join(B, 'page.html'); open(page, 'w').write(html)
from playwright.sync_api import sync_playwright
silent = os.path.join(B, 'silent.mp4')
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + page); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(1500)
    if errs: sys.exit('page error: ' + errs[0])
    st = pg.locator('#stage'); n = int(tl['total'] * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
    for i in range(n):
        pg.evaluate(f'render({i / FPS})')
        ff.stdin.write(st.screenshot(type='jpeg', quality=93))
        if i % 450 == 0: print('frame', i, '/', n, flush=True)
    ff.stdin.close(); ff.wait(); br.close()

# ---------- audio + mux ----------
subprocess.run([sys.executable, os.path.join(P, 'mix_audio.py'), B], check=True)
mp4 = os.path.join(OUT, f'{slug}.mp4')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', os.path.join(B, 'mix.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                '-af', 'loudnorm=I=-14:TP=-1:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-shortest', '-movflags', '+faststart', mp4], check=True)

# ---------- check sheet ----------
T = tl['total']; E = tl['end']
times = [1.5 if COLD else 2.6, tl['hook']['end'] + 4, T * 0.45, (tl['msgs'][-1]['at'] + 0.3), min(E['declined'], T - 3) if E['declined'] < 1e8 else T - 4, T - 1.5]
frames = []
for k, t in enumerate(times):
    f = os.path.join(B, f'sheet{k}.png'); frames.append(f)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', mp4, '-frames:v', '1', '-vf', 'scale=300:-1', f], check=True)
args = []
for f in frames: args += ['-i', f]
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *args, '-filter_complex', f'hstack={len(frames)}', os.path.join(OUT, f'{slug}_sheet.png')], check=True)
size = os.path.getsize(mp4) / 1e6
print(json.dumps({'mp4': mp4, 'sheet': os.path.join(OUT, f'{slug}_sheet.png'), 'seconds': round(T, 1), 'MB': round(size, 1)}))
