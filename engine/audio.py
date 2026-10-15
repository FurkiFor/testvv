"""Synthesize a seamless ASMR soundtrack from a scene's event list.

Usage: python3 audio.py spec.json out.wav

The track is built on a circular buffer of exactly the video's length: every
event is placed at (cycle + tau) * cycleSec and wraps around the end, the beds
are shaped in the frequency domain of that same buffer, and the room reverb is
a circular convolution. The result loops with no click, like the picture.
"""
import json
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000


def bp(x, lo, hi, order=2):
    hi = min(hi, SR / 2 * 0.95)
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def t_axis(sec):
    return np.arange(int(sec * SR)) / SR


def shape_env(n, attack=0.15, release=0.3):
    e = np.ones(n)
    a = max(1, int(n * attack))
    r = max(1, int(n * release))
    e[:a] = np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    e[-r:] = np.cos(np.linspace(0, np.pi / 2, r)) ** 2
    return e


def granular(rng, sec, rate, lo, hi, hiss_lo, hiss_hi, hiss=0.25, grain_amp=1.0):
    n = int(sec * SR)
    x = np.zeros(n)
    k = rng.poisson(rate * sec)
    pos = rng.integers(0, max(1, n - 1), size=k)
    x[pos] += rng.uniform(-1, 1, size=k) * rng.uniform(0.2, 1.0, size=k) ** 2 * grain_amp
    g = bp(x, lo, hi, 2) * 6
    h = bp(rng.standard_normal(n), hiss_lo, hiss_hi, 2) * hiss
    return (g + h) * shape_env(n, 0.12, 0.3)


def resonator(t, freqs, decays, amps):
    return sum(a * np.exp(-t / d) * np.sin(2 * np.pi * f * t) for f, d, a in zip(freqs, decays, amps))


def click(rng, sec=0.003, lo=2000):
    n = int(sec * SR)
    return hp(rng.standard_normal(n), lo) * np.exp(-np.arange(n) / (n / 4))


def synth(kind, rng, dur, pitch):
    if kind == "sand":
        return granular(rng, dur, 1100, 1500, 7500, 300, 2400, 0.35)
    if kind == "soap":
        return granular(rng, dur, 260, 900, 4200, 600, 3200, 0.55, 0.6)
    if kind == "crisp":
        s = granular(rng, dur, 420, 2000, 9000, 1200, 5000, 0.2)
        s[: int(0.004 * SR)] += click(rng, 0.004) * 1.5
        return s
    if kind == "stone":
        return granular(rng, dur, 1600, 600, 4500, 400, 3000, 0.4, 0.8)
    if kind == "tick":
        t = t_axis(0.09)
        f = 2300 * pitch
        s = resonator(t, [f, f * 2.31, f * 3.93], [0.022, 0.012, 0.007], [1, 0.5, 0.3])
        c = click(rng, 0.002)
        s[: len(c)] += c * 0.8
        return s
    if kind == "thud":
        t = t_axis(0.25)
        f = 110 * pitch * np.exp(-t / 0.08) + 55
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07)
        s += lp(rng.standard_normal(len(t)), 500) * np.exp(-t / 0.03) * 0.6
        return s
    if kind == "slide":
        t = t_axis(dur)
        s = bp(rng.standard_normal(len(t)), 160, 1300, 2) * (1 + 0.25 * np.sin(2 * np.pi * 7 * t))
        return s * shape_env(len(t), 0.25, 0.45) * 1.4
    if kind == "crack":
        out = np.zeros(int(0.12 * SR))
        at = 0
        for i in range(int(rng.integers(4, 7))):
            t = t_axis(0.03)
            f = rng.uniform(3000, 5200) * pitch
            s = resonator(t, [f, f * 1.7], [0.006, 0.004], [1, 0.4]) * (0.85 ** i)
            j = min(len(out) - len(s), at)
            out[j:j + len(s)] += s
            at += int(rng.uniform(0.006, 0.016) * SR)
        return out
    if kind == "pop":
        t = t_axis(0.08)
        f = 180 + 720 * np.exp(-t / 0.012)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.02)
        return s + np.pad(click(rng, 0.002, 1000), (0, len(t) - int(0.002 * SR))) * 0.5
    if kind == "whoosh":
        n = int(dur * SR)
        x = rng.standard_normal(n)
        out = np.zeros(n)
        blocks = 24
        for b in range(blocks):
            a, z = b * n // blocks, (b + 1) * n // blocks
            fc = 350 * (8 ** (b / blocks))
            seg = bp(x[max(0, a - 512):z], fc * 0.6, fc * 1.6, 2)[-(z - a):]
            out[a:z] = seg
        return out * shape_env(n, 0.35, 0.5) * 1.2
    if kind == "chime":
        f = pitch if pitch > 20 else 660 * pitch
        t = t_axis(1.8)
        return resonator(t, [f, f * 2.0, f * 2.76, f * 5.4], [1.4, 0.8, 0.5, 0.2], [1, 0.35, 0.28, 0.1]) * 0.5
    if kind == "clack":
        t = t_axis(0.07)
        s = resonator(t, [1550 * pitch, 2950 * pitch, 420 * pitch], [0.016, 0.009, 0.012], [1, 0.6, 0.5])
        c = click(rng, 0.003, 1800)
        s[: len(c)] += c
        return s
    raise ValueError(f"unknown sound {kind}")


def circular_noise(rng, n, lo, hi, tilt=0.0):
    spec = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    g = ((f >= lo) & (f <= hi)).astype(float)
    if tilt:
        g *= 1 / np.maximum(f, lo) ** tilt
    return np.fft.irfft(spec * g, n)


def main(spec_path, out_path):
    spec = json.load(open(spec_path))
    rng = np.random.default_rng(int(spec.get("seed", 1)) & 0xFFFFFFFF)
    D = spec["duration"]
    N = int(round(D * SR))
    cycles, cs = spec["cycles"], spec["cycleSec"]
    buf = np.zeros((2, N))

    def place(sig, start, pan, spread=False):
        idx = (start + np.arange(len(sig))) % N
        if spread:
            p = np.linspace(-0.7, 0.7, len(sig))
        else:
            p = np.full(len(sig), pan)
        L = np.cos((p + 1) * np.pi / 4)
        R = np.sin((p + 1) * np.pi / 4)
        np.add.at(buf[0], idx, sig * L)
        np.add.at(buf[1], idx, sig * R)

    for k in range(cycles):
        for ev in spec["events"]:
            seq = ev.get("pitchSeq")
            pitch = ev.get("pitch", 1.0) * (seq[k % len(seq)] if seq and ev["type"] != "chime" else 1.0)
            if ev["type"] == "chime" and seq:
                pitch = seq[k % len(seq)]
            dur = ev.get("dur", 0.2) * cs
            sig = synth(ev["type"], rng, dur, pitch) * ev.get("gain", 1.0)
            start = int(round(((k + ev["tau"]) * cs) * SR)) % N
            place(sig, start, ev.get("pan", 0.0), ev.get("stereoSpread", False))

    bed = spec.get("bed") or {}
    if bed.get("type") == "room":
        b = circular_noise(rng, N, 40, 6000, tilt=0.5)
        b /= np.abs(b).max() + 1e-9
        buf += b * bed.get("gain", 0.05) * 0.5
    elif bed.get("type") == "roll":
        t = np.arange(N) / SR
        rate = bed.get("rate", 3.0)
        cyc = round(rate * D) / D  # whole number of wobbles per loop
        rum = circular_noise(rng, N, 70, 650, tilt=0.6)
        rum /= np.abs(rum).max() + 1e-9
        grit = circular_noise(rng, N, 1800, 7000)
        grit /= np.abs(grit).max() + 1e-9
        am = 1 + 0.35 * np.sin(2 * np.pi * cyc * t)
        g = bed.get("gain", 0.2)
        buf[0] += (rum * am + grit * 0.18) * g
        buf[1] += (np.roll(rum, N // 3) * am + np.roll(grit, N // 5) * 0.18) * g

    # small room, circular convolution keeps the loop seamless
    ir_n = int(0.4 * SR)
    ti = np.arange(ir_n) / SR
    wet = np.zeros_like(buf)
    for ch in range(2):
        ir = lp(rng.standard_normal(ir_n), 5000) * np.exp(-ti / 0.075)
        ir /= np.sqrt((ir ** 2).sum())
        irp = np.zeros(N)
        irp[:ir_n] = ir
        wet[ch] = np.fft.irfft(np.fft.rfft(buf[ch]) * np.fft.rfft(irp), N)
    mix = buf + wet * 0.22
    spec_m = np.fft.rfft(mix, axis=1)
    spec_m[:, np.fft.rfftfreq(N, 1 / SR) < 30] = 0  # circular high-pass, no seam
    mix = np.fft.irfft(spec_m, N, axis=1)
    rms = np.sqrt((mix ** 2).mean()) + 1e-9
    mix *= 10 ** (-19.5 / 20) / rms
    mix = np.tanh(mix * 1.2) / np.tanh(1.2)
    mix *= 0.8 / max(0.8, np.abs(mix).max())  # headroom for AAC overshoot
    wavfile.write(out_path, SR, (mix.T * 32767).astype(np.int16))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
