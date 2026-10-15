import json, os, sys, numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt
D = sys.argv[1]  # build dir holding timeline.json and vo/
SR = 44100
tl = json.load(open(f'{D}/timeline.json'))
N = int((tl['total'] + 0.5) * SR)
rng = np.random.default_rng(7)

def env(n, a=0.002, d=0.1):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def tone(f0, f1, dur, d=0.1, a=0.002):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, a, d)
def noise(dur): return rng.standard_normal(int(dur * SR))
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'highpass', fs=SR, output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f, 'lowpass', fs=SR, output='sos'), x)
def mx(a, b):
    n = max(len(a), len(b)); return np.pad(a, (0, n - len(a))) + np.pad(b, (0, n - len(b)))
def norm(x, g): return x / (np.max(np.abs(x)) + 1e-9) * g

S = {}
S['pop'] = norm(mx(tone(1100, 380, 0.09, 0.025), 0.3 * tone(2200, 760, 0.05, 0.01)), 0.45)
n = noise(0.32); sweep = np.linspace(0, 1, len(n))
S['swoosh'] = norm(bp(n, 900, 5000) * np.sin(np.pi * sweep) ** 2, 0.28)
S['ding'] = norm(tone(1318, 1318, 0.7, 0.18) + 0.5 * tone(1976, 1976, 0.7, 0.12), 0.32)
S['key'] = norm(hp(noise(0.012), 2500) * env(int(0.012 * SR), 0.0005, 0.004), 0.10)
S['tap'] = norm(hp(noise(0.03), 1500) * env(int(0.03 * SR), 0.0005, 0.008), 0.25)
b = tone(95, 42, 1.4, 0.5, 0.001)
b = np.tanh(b * 3.5) + 0.25 * lp(noise(1.4), 200) * env(int(1.4 * SR), 0.001, 0.08)
S['boom'] = norm(b, 0.95)
w = bp(noise(0.7), 300, 3000) * np.sin(np.pi * np.linspace(0, 1, int(0.7 * SR)))
S['whoosh'] = norm(w, 0.4) + np.pad(norm(np.tanh(tone(80, 40, 0.5, 0.2) * 2), 0.6), (int(0.2 * SR), 0))[:len(w)]
S['thud'] = norm(np.tanh(tone(120, 55, 0.35, 0.09) * 2.5) + 0.3 * lp(noise(0.35), 800) * env(int(0.35 * SR), 0.001, 0.03), 0.7)
# record scratch: buzzy saw with fast pitch wobble + noise
n = int(0.55 * SR); t = np.arange(n) / SR
f = 260 + 520 * np.abs(np.sin(2 * np.pi * 7 * t)) * np.exp(-t * 2)
saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
S['scratch'] = norm(bp(saw + 0.6 * noise(0.55), 400, 4000) * env(n, 0.003, 0.25), 0.6)
# ring (two 1s bursts of 440+480 tremolo)
n = int(1.0 * SR); t = np.arange(n) / SR
r = (np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 480 * t)) * (0.6 + 0.4 * np.sin(2 * np.pi * 20 * t))
r *= np.minimum(1, t / 0.02) * np.minimum(1, (1.0 - t) / 0.05)
S['ring'] = norm(np.concatenate([r, np.zeros(int(0.35 * SR)), r[:int(0.4 * SR)]]), 0.22)
S['decline'] = norm(np.concatenate([tone(f_, f_, 0.16, 0.2, 0.003) for f_ in (620, 480, 360)]), 0.35)
S['bonk'] = norm(mx(tone(340, 170, 0.35, 0.07, 0.0005), 0.5 * tone(920, 460, 0.2, 0.03, 0.0005)), 0.7)

sfx = np.zeros(N)
for name, at in tl['sfx']:
    s = S[name]; i = int(at * SR); j = min(N, i + len(s)); sfx[i:j] += s[:j - i]

vo = np.zeros(N); vmask = np.zeros(N)
for name, at in tl['vo']:
    a, sr = sf.read(f'{D}/vo/{name}.wav')
    if a.ndim > 1: a = a.mean(1)
    a = resample_poly(a, 147, 80)  # 24k -> 44.1k
    a = norm(a, 0.9)
    i = int(at * SR); j = min(N, i + len(a)); vo[i:j] += a[:j - i]; vmask[i:j] = 1

# sneaky pizzicato bed (Karplus-Strong), 112 bpm, ducked under voice
def pluck(freq, dur=0.35):
    n = int(dur * SR); p = int(SR / freq)
    buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for k in range(n):
        out[k] = buf[k % p]; buf[k % p] = 0.5 * (buf[k % p] + buf[(k + 1) % p]) * 0.996
    return out * env(n, 0.001, 0.18)
notes = [110, 0, 130.8, 110, 164.8, 0, 146.8, 130.8, 110, 0, 130.8, 110, 98, 0, 103.8, 110]
cache = {f: pluck(f) for f in set(notes) if f}
step = 60 / 112 / 2
music = np.zeros(N); k = 0; t0 = 0.0
while t0 < tl['total'] - 1.0:
    f_ = notes[k % len(notes)]
    if f_:
        s = cache[f_]; i = int(t0 * SR); j = min(N, i + len(s)); music[i:j] += s[:j - i]
        if k % 4 == 0:
            h = norm(hp(noise(0.04), 6000) * env(int(0.04 * SR), 0.0005, 0.01), 1); jj = min(N, i + len(h)); music[i:jj] += 0.3 * h[:jj - i]
    k += 1; t0 += step
music = norm(music, 1.0)
# ducking envelope (smoothed)
from scipy.ndimage import uniform_filter1d
duck = 1 - 0.65 * uniform_filter1d(vmask, int(0.15 * SR))
music *= 0.12 * duck
# silence music during the meme card hit for drama, bring back after
m0 = int(tl['end']['meme'] * SR); music[m0:m0 + int(1.0 * SR)] *= np.linspace(0, 1, int(1.0 * SR))[:len(music[m0:m0 + int(1.0 * SR)])]

mixd = vo * 0.95 + sfx * 0.6 + music
mixd = np.tanh(mixd * 1.1) / np.tanh(1.1)
mixd = norm(mixd, 0.93)
fade = int(0.4 * SR); mixd[-fade:] *= np.linspace(1, 0, fade)
sf.write(f'{D}/mix.wav', np.stack([mixd, mixd], 1), SR)
print('mix ok', round(N / SR, 2), 's')
