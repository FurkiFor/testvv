#!/usr/bin/env python3
"""Yok Artık! — kodla animasyonlu Shorts motoru (temalı).

Kullanım: python3 engine.py script.json voice.mp3 out.mp4 [--theme pop|gazete|neon|uzay]
          python3 engine.py --preview script.json out.png [--theme ...]   (sesiz kare önizleme)
script.json: {"id":..., "theme":"pop", "scenes":[{"say":..., "cap":..., "type":..., ...}]}
"""
import io, json, math, os, re, subprocess, sys, functools, random, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cairosvg

W, H, FPS = 1080, 1920, 30
ROOT = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(ROOT, "assets", "tw", "package")
F_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
F_BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"

INK = (14, 12, 20)
WHITE = (255, 255, 255)

# ---------------------------------------------------------------- temalar
THEMES = {
    "uzay": dict(bg="space", text=WHITE, stroke=INK, acc=(255, 210, 63), acc2=(255, 72, 88), good=(60, 230, 140),
                 num=(255, 210, 63), num_stroke=INK, pill_bg=WHITE, pill_fg=INK, brand_bg=(255, 210, 63),
                 brand_fg=INK, line=(255, 255, 255), glow=(255, 210, 63), glow_s=120,
                 cap_text=WHITE, cap_stroke=INK, cap_hl_bg=(255, 210, 63), cap_hl_fg=INK,
                 stamp_bg=(255, 72, 88), stamp_fg=WHITE, flash=(255, 255, 255)),
    "pop": dict(bg="pop", text=INK, stroke=WHITE, acc=(232, 33, 58), acc2=(232, 33, 58), good=(0, 150, 90),
                num=(232, 33, 58), num_stroke=WHITE, pill_bg=INK, pill_fg=(255, 214, 10), brand_bg=INK,
                brand_fg=(255, 214, 10), line=INK, glow=INK, glow_s=70,
                cap_text=WHITE, cap_stroke=INK, cap_hl_bg=(232, 33, 58), cap_hl_fg=WHITE,
                stamp_bg=(232, 33, 58), stamp_fg=WHITE, flash=(255, 255, 255)),
    "gazete": dict(bg="paper", text=INK, stroke=(243, 238, 227), acc=(206, 28, 36), acc2=(206, 28, 36),
                   good=(20, 120, 70), num=INK, num_stroke=(243, 238, 227), pill_bg=(206, 28, 36),
                   pill_fg=WHITE, brand_bg=INK, brand_fg=(243, 238, 227), line=INK, glow=INK, glow_s=45,
                   cap_text=INK, cap_stroke=(243, 238, 227), cap_hl_bg=INK, cap_hl_fg=(243, 238, 227),
                   stamp_bg=(206, 28, 36), stamp_fg=WHITE, flash=(255, 255, 255)),
    "neon": dict(bg="neon", text=WHITE, stroke=(40, 0, 60), acc=(45, 244, 255), acc2=(255, 46, 170),
                 good=(120, 255, 120), num=(45, 244, 255), num_stroke=(10, 0, 30), pill_bg=(255, 46, 170),
                 pill_fg=WHITE, brand_bg=(45, 244, 255), brand_fg=(10, 0, 30), line=(45, 244, 255),
                 glow=(255, 46, 170), glow_s=170, cap_text=WHITE, cap_stroke=(40, 0, 60),
                 cap_hl_bg=(255, 46, 170), cap_hl_fg=WHITE, stamp_bg=(255, 46, 170), stamp_fg=WHITE,
                 flash=(255, 46, 170)),
}
T = dict(THEMES["pop"])

def set_theme(name):
    T.clear(); T.update(THEMES.get(name, THEMES["pop"])); T["name"] = name
    for f in (_cached_text_key, caption_img, _stamp, pill):
        f.cache_clear()

def col(name):
    return {"yellow": T["acc"], "acc": T["acc"], "red": T["acc2"], "green": T["good"]}.get(name, T["acc"])

# ---------------------------------------------------------------- yardımcılar

def tr_upper(s):
    return s.replace("i", "İ").replace("ı", "I").upper()

@functools.lru_cache(maxsize=64)
def font(path, size):
    return ImageFont.truetype(path, size)

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def ease_out_cubic(t):
    t = clamp(t); return 1 - (1 - t) ** 3

def ease_out_back(t, s=1.9):
    t = clamp(t) - 1; return t * t * ((s + 1) * t + s) + 1

def ease_in_out(t):
    t = clamp(t); return t * t * (3 - 2 * t)

_ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]

def tr_num_words(n):
    n = int(n)
    if n == 0: return "sıfır"
    out = []
    for val, name in ((10**9, "milyar"), (10**6, "milyon"), (1000, "bin")):
        if n >= val:
            q, n = divmod(n, val)
            out.append(("" if (q == 1 and name == "bin") else tr_num_words(q)) + name)
    if n >= 100:
        q, n = divmod(n, 100)
        out.append(("" if q == 1 else _ONES[q]) + "yüz")
    out.append(_TENS[n // 10] + _ONES[n % 10])
    return "".join(out)

def spoken_weight(tok):
    core = re.sub(r"[^\w'%]", "", tok)
    digits = re.sub(r"[.,%']|[^\d]+$", "", core)
    if digits.isdigit():
        return len(tr_num_words(digits)) + 2 + (6 if "%" in core else 0)
    if core.upper() in ("MÖ", "MS"):
        return 10
    return max(2, len(core)) + 1.2

# ---------------------------------------------------------------- ikonlar

def _custom_icon(name, size):
    s = size; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if name == "pyramid":
        d.polygon([(s*0.5, s*0.08), (s*0.02, s*0.9), (s*0.5, s*0.9)], fill=(244, 196, 98))
        d.polygon([(s*0.5, s*0.08), (s*0.5, s*0.9), (s*0.98, s*0.9)], fill=(196, 140, 58))
        for k in range(1, 6):
            y = s*0.08 + (s*0.82)*k/6; half = (y - s*0.08) / 0.82 * 0.48
            d.line([(s*0.5-half, y), (s*0.5+half, y)], fill=(150, 104, 40), width=max(2, s//90))
        d.rectangle([0, s*0.9, s, s*0.96], fill=(230, 180, 90))
    elif name in ("venus", "mars", "planet"):
        base = {"venus": (236, 170, 80), "mars": (214, 92, 52), "planet": (120, 160, 230)}[name]
        m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).ellipse([s*0.04, s*0.04, s*0.96, s*0.96], fill=255)
        body = Image.new("RGBA", (s, s), base + (255,)); bd = ImageDraw.Draw(body)
        for k in range(7):  # bulut bantları
            y = s * (0.12 + k * 0.12); c2 = tuple(min(255, v + (22 if k % 2 else -18)) for v in base)
            bd.ellipse([-s*0.3, y, s*1.3, y + s*0.13], fill=c2 + (255,))
        shade = Image.new("L", (s, s), 0); ImageDraw.Draw(shade).ellipse([s*0.3, s*0.25, s*1.35, s*1.3], fill=110)
        shade = shade.filter(ImageFilter.GaussianBlur(s * 0.08))
        body = Image.composite(Image.new("RGBA", (s, s), (40, 20, 10, 255)), body, shade)
        hi = Image.new("L", (s, s), 0); ImageDraw.Draw(hi).ellipse([s*0.18, s*0.14, s*0.42, s*0.34], fill=90)
        body = Image.composite(Image.new("RGBA", (s, s), (255, 255, 255, 255)), body, hi.filter(ImageFilter.GaussianBlur(s*0.05)))
        im.paste(body, (0, 0), m)
    return im

@functools.lru_cache(maxsize=128)
def icon(code, size):
    path = os.path.join(ICON_DIR, f"{code}.svg")
    if not os.path.exists(path):
        return _custom_icon(code, size)
    png = cairosvg.svg2png(url=path, output_width=size, output_height=size)
    return Image.open(io.BytesIO(png)).convert("RGBA")

def glow(im, radius=28, color=None, strength=None):
    color = color or T["glow"]; strength = strength if strength is not None else T["glow_s"]
    p = radius * 2
    a = Image.new("L", (im.width + 2 * p, im.height + 2 * p), 0)
    a.paste(im.split()[-1], (p, p))
    a = a.filter(ImageFilter.GaussianBlur(radius))
    g = Image.new("RGBA", a.size, color + (0,))
    g.putalpha(a.point(lambda v: min(255, v * strength // 255)))
    return g

def shadow_or_glow(c, im, x, y, s, a, radius=30):
    """Koyu temalarda parıltı, açık temalarda yumuşak gölge."""
    if T["bg"] in ("pop", "paper"):
        paste(c, glow(im, 18, INK, T["glow_s"]), x + 10, y + 16, s, a)
    else:
        paste(c, glow(im, radius), x, y, s, a * 0.8)

# ---------------------------------------------------------------- metin

def wrap(text, fnt, max_w, draw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def text_block(text, size, color, stroke_col, max_w=920, path=F_BLACK, stroke=10,
               highlight=None, line_gap=1.08):
    fnt = font(path, size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    lines = wrap(text, fnt, max_w, tmp)
    lh = int(size * line_gap)
    widths = [tmp.textlength(l, font=fnt) for l in lines]
    w = int(max(widths) + stroke * 2 + 20); h = int(lh * len(lines) + stroke * 2 + size * 0.3)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, line in enumerate(lines):
        x = (w - widths[i]) / 2; y = stroke + i * lh
        for word in line.split(" "):
            key = re.sub(r"[^\wÇĞİÖŞÜçğıöşü']", "", word)
            c = (highlight or {}).get(key, color)
            d.text((x, y), word, font=fnt, fill=c, stroke_width=stroke, stroke_fill=stroke_col)
            x += tmp.textlength(word + " ", font=fnt)
    return im

@functools.lru_cache(maxsize=64)
def pill(text, size, bg, fg, pad=(34, 16), path=F_BLACK):
    fnt = font(path, size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = tmp.textlength(text, font=fnt); bb = fnt.getbbox(text)
    w, h = int(tw + pad[0] * 2), int(bb[3] - bb[1] + pad[1] * 2)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=bg)
    d.text((pad[0], pad[1] - bb[1]), text, font=fnt, fill=fg)
    return im

@functools.lru_cache(maxsize=256)
def _cached_text_key(text, size, hl_items, max_w, path, stroke, color, stroke_col):
    return text_block(tr_upper(text), size, color, stroke_col, max_w=max_w, path=path, stroke=stroke,
                      highlight={tr_upper(k): v for k, v in hl_items} if hl_items else None)

def ctext(text, size, hl=None, max_w=940, path=F_BLACK, stroke=10, color=None):
    items = tuple(sorted((k, col(v)) for k, v in (hl or {}).items()))
    return _cached_text_key(text, size, items, max_w, path, stroke, color or T["text"], T["stroke"])

# ---------------------------------------------------------------- kompozisyon

def paste(canvas, im, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if alpha <= 0.01 or scale <= 0.01: return
    if abs(scale - 1) > 0.005:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = im.split()[-1].point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def pop(t, delay=0.0, dur=0.38):
    p = (t - delay) / dur
    if p <= 0: return 0.0, 0.0
    return 0.55 + 0.45 * ease_out_back(p), ease_out_cubic(p * 1.6)

# ---------------------------------------------------------------- arka planlar

VIS_Y = 820

class SpaceBG:
    def __init__(self, seed=7):
        rnd = random.Random(seed)
        self.base_a = np.array([20, 10, 46], np.float32); self.base_b = np.array([6, 22, 58], np.float32)
        self.blobs = [(rnd.random(), rnd.random(), rnd.uniform(0.25, 0.4), rnd.uniform(0.2, 0.5),
                       np.array(c, np.float32)) for c in [(120, 40, 200), (20, 120, 220), (230, 60, 120)]]
        self.stars = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.5, 4), rnd.uniform(0, 6.28),
                       rnd.uniform(8, 30)) for _ in range(70)]
        sw, sh = 108, 192
        yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
        self.xx, self.yy = xx / sw, yy / sh
        vy, vx = np.mgrid[0:H:4, 0:W:4].astype(np.float32)
        d = np.sqrt(((vx - W / 2) / (W * 0.75)) ** 2 + ((vy - H / 2) / (H * 0.7)) ** 2)
        self.vignette = Image.fromarray((np.clip(1 - d * 0.55, 0.35, 1) * 255).astype(np.uint8)).resize((W, H))

    def frame(self, t):
        g = self.yy[..., None]
        img = self.base_a * (1 - g) + self.base_b * g
        for i, (bx, by, r, sp, c) in enumerate(self.blobs):
            cx = bx + 0.18 * math.sin(t * sp + i * 2.1); cy = by + 0.12 * math.cos(t * sp * 0.8 + i)
            dist = ((self.xx - cx) ** 2 + ((self.yy - cy) * 1.78) ** 2) / (r * r)
            img = img + c[None, None, :] * (np.exp(-dist)[..., None] * 0.55)
        bg = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").resize((W, H), Image.BILINEAR)
        bg = Image.composite(bg, Image.new("RGB", (W, H)), self.vignette).convert("RGBA")
        d = ImageDraw.Draw(bg)
        for (x, y, r, ph, sp) in self.stars:
            yy = (y - t * sp) % H; a = int(90 + 80 * math.sin(t * 2 + ph))
            d.ellipse([x - r, yy - r, x + r, yy + r], fill=(255, 255, 255, a))
        return bg

class PopBG:
    """Çizgi roman sarısı: dönen güneş ışınları + kayan halftone noktalar."""
    def __init__(self, seed=7):
        self.base = (255, 214, 10); self.ray = (255, 196, 0)
        dots = Image.new("RGBA", (W + 60, H + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(dots)
        for yy in range(0, H + 60, 30):
            for xx in range(0, W + 60, 30):
                off = 15 if (yy // 30) % 2 else 0
                r = 2 + 7 * (yy / (H + 60)) ** 1.6
                d.ellipse([xx + off - r, yy - r, xx + off + r, yy + r], fill=(230, 150, 0, 110))
        self.dots = dots
        vy, vx = np.mgrid[0:H:4, 0:W:4].astype(np.float32)
        dd = np.sqrt(((vx - W / 2) / W) ** 2 + ((vy - VIS_Y) / H) ** 2)
        v = np.clip(dd * 160 - 30, 0, 90).astype(np.uint8)
        self.vig = Image.fromarray(v).resize((W, H))
        self.vig_layer = Image.new("RGBA", (W, H), (200, 90, 0, 0)); self.vig_layer.putalpha(self.vig)

    def frame(self, t):
        bg = Image.new("RGBA", (W, H), self.base + (255,)); d = ImageDraw.Draw(bg)
        cx, cy, R, n = W / 2, VIS_Y, 2600, 18
        rot = t * 0.12
        for k in range(n):
            a0 = rot + k * 2 * math.pi / n; a1 = a0 + math.pi / n
            d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)),
                       (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=self.ray + (255,))
        o = int(t * 18) % 30
        bg.alpha_composite(self.dots.crop((o, o, o + W, o + H)))
        bg.alpha_composite(self.vig_layer)
        return bg

class PaperBG:
    """Eski gazete kâğıdı: doku + sütun çizgileri + soluk manşet yazıları."""
    def __init__(self, seed=7):
        rnd = np.random.default_rng(seed)
        base = np.array([243, 238, 227], np.float32)
        n = rnd.normal(0, 7, (H // 2, W // 2, 1)).astype(np.float32)
        img = np.clip(base + n, 0, 255).astype(np.uint8)
        paper = Image.fromarray(img, "RGB").resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.6))
        paper = paper.convert("RGBA")
        over = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(over)
        fnt = font(F_BLACK, 60); small = font(F_BOLD, 22)
        rr = random.Random(seed)
        words = ["İNANILMAZ", "ŞOK GERÇEK", "BİLİM", "TARİH", "DOĞA", "GİZEM", "REKOR", "KEŞİF"]
        y = 40
        while y < H:
            d.line([(40, y), (W - 40, y)], fill=(60, 50, 40, 40), width=3)
            d.text((50, y + 12), rr.choice(words) + " · " + rr.choice(words), font=fnt, fill=(60, 50, 40, 22))
            for col_x in (50, 400, 750):
                for k in range(6):
                    d.rectangle([col_x, y + 95 + k * 30, col_x + rr.randint(200, 290), y + 108 + k * 30],
                                fill=(60, 50, 40, 16))
            y += 330
        paper.alpha_composite(over)
        vy, vx = np.mgrid[0:H:4, 0:W:4].astype(np.float32)
        dd = np.sqrt(((vx - W / 2) / W) ** 2 + ((vy - H / 2) / H) ** 2)
        v = Image.fromarray(np.clip(dd * 200 - 40, 0, 110).astype(np.uint8)).resize((W, H))
        burn = Image.new("RGBA", (W, H), (120, 80, 30, 0)); burn.putalpha(v)
        paper.alpha_composite(burn)
        self.paper = paper

    def frame(self, t):
        return self.paper.copy()

class NeonBG:
    """Synthwave: koyu gökyüzü, batan güneş, kayan perspektif ızgara."""
    def __init__(self, seed=7):
        sky = np.zeros((H, 1, 3), np.float32)
        ys = np.linspace(0, 1, H)[:, None]
        top, mid = np.array([8, 4, 24], np.float32), np.array([60, 10, 80], np.float32)
        sky[:, 0, :] = top * (1 - ys) + mid * ys
        self.sky = Image.fromarray(np.clip(sky, 0, 255).astype(np.uint8)).resize((W, H)).convert("RGBA")
        sun = Image.new("RGBA", (700, 700)); d = ImageDraw.Draw(sun)
        for r in range(350, 0, -2):
            k = r / 350
            d.ellipse([350 - r, 350 - r, 350 + r, 350 + r],
                      fill=(int(255), int(60 + 140 * (1 - k)), int(170 * k), 255))
        for i, y in enumerate(range(380, 700, 34)):
            d.rectangle([0, y, 700, y + 6 + i * 2], fill=(0, 0, 0, 0))
        self.sun = sun; self.sun_glow = glow(sun, 60, (255, 46, 170), 160)
        self.horizon = 1180
        rnd = random.Random(seed)
        self.stars = [(rnd.uniform(0, W), rnd.uniform(0, self.horizon - 100), rnd.uniform(1, 3)) for _ in range(60)]

    def frame(self, t):
        bg = self.sky.copy(); d = ImageDraw.Draw(bg)
        for x, y, r in self.stars:
            a = int(120 + 100 * math.sin(t * 3 + x))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))
        hz = self.horizon
        bg.alpha_composite(self.sun_glow, (W // 2 - self.sun_glow.width // 2, hz - 470 - (self.sun_glow.height - 700) // 2))
        bg.alpha_composite(self.sun, (W // 2 - 350, hz - 470))
        d.rectangle([0, hz, W, H], fill=(10, 0, 24, 255))
        gc = (255, 46, 170, 255)
        for i in range(-14, 15):
            d.line([(W / 2 + i * 40, hz), (W / 2 + i * 260, H)], fill=gc, width=3)
        ph = (t * 0.9) % 1.0
        for k in range(14):
            z = (k + ph) / 14; y = hz + (H - hz) * z ** 2.2
            d.line([(0, y), (W, y)], fill=gc, width=2 + int(4 * z))
        d.line([(0, hz), (W, hz)], fill=(45, 244, 255, 255), width=4)
        return bg

BACKGROUNDS = {"space": SpaceBG, "pop": PopBG, "paper": PaperBG, "neon": NeonBG}

# ---------------------------------------------------------------- sahne tipleri

def scene_hook(c, sc, t, dur):
    icons = sc.get("icons", []); n = len(icons)
    for i, code in enumerate(icons):
        s, a = pop(t, 0.05 + i * 0.12)
        gap = 330 if n <= 2 else 310
        x = W / 2 + (i - (n - 1) / 2) * gap; y = VIS_Y - 170 + 14 * math.sin(t * 3 + i)
        if n == 3 and i == 1: y -= 70  # ortadaki (özne) biraz yukarıda
        im = icon(code, 300 if n <= 2 else 250)
        shadow_or_glow(c, im, x, y, s, a)
        paste(c, im, x, y, s, a, rot=6 * math.sin(t * 2 + i))
    if sc.get("text"):
        s, a = pop(t, 0.25)
        paste(c, ctext(sc["text"], 92, sc.get("hl")), W / 2, VIS_Y + 150, s, a)

def scene_statement(c, sc, t, dur):
    if sc.get("icon"):
        s, a = pop(t, 0.0)
        im = icon(sc["icon"], 360); y = VIS_Y - 150 + 12 * math.sin(t * 3)
        shadow_or_glow(c, im, W / 2, y, s, a, 34)
        paste(c, im, W / 2, y, s, a)
    if sc.get("text"):
        s, a = pop(t, 0.18)
        paste(c, ctext(sc["text"], 100, sc.get("hl")), W / 2, VIS_Y + 170, s, a)

def scene_number(c, sc, t, dur):
    if sc.get("icon"):
        s, a = pop(t, 0.0)
        im = icon(sc["icon"], 250); y = VIS_Y - 300 + 10 * math.sin(t * 3)
        shadow_or_glow(c, im, W / 2, y, s, a)
        paste(c, im, W / 2, y, s, a)
    val = float(sc["value"]); dec = int(sc.get("decimals", 0))
    p = ease_out_cubic(t / min(1.2, dur * 0.6))
    if sc.get("year"):  # Türkçede yıllar binlik ayraçsız yazılır: MÖ 2560
        num = str(int(round(val * p)))
    else:
        num = f"{val * p:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    txt = sc.get("prefix", "") + num + sc.get("suffix", "")
    fnt = font(F_BLACK, int(sc.get("size", 210)))
    tw = ImageDraw.Draw(c).textlength(txt, font=fnt)
    layer = Image.new("RGBA", (int(tw + 60), int(fnt.size * 1.35)), (0, 0, 0, 0))
    fill = T["good"] if sc.get("color") == "green" else T["num"]
    ImageDraw.Draw(layer).text((30, 10), txt, font=fnt, fill=fill, stroke_width=12, stroke_fill=T["num_stroke"])
    s, a = pop(t, 0.05)
    punch = 1 + 0.06 * max(0, 1 - abs(t - 1.2) * 5) if p >= 0.999 else 1
    shadow_or_glow(c, layer, W / 2, VIS_Y, s * punch, a, 26)
    paste(c, layer, W / 2, VIS_Y, s * punch, a)
    if sc.get("label"):
        sl, al = pop(t, 0.3)
        paste(c, pill(tr_upper(sc["label"]), 54, T["pill_bg"], T["pill_fg"]), W / 2, VIS_Y + 190, sl, al)

def scene_timeline(c, sc, t, dur):
    pts = sc["points"]; vals = [p["at"] for p in pts]; lo, hi = min(vals), max(vals)
    x0, x1, y = 150, W - 150, VIS_Y + 40
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([x0 - 10, y - 7, x0 - 10 + (x1 - x0 + 20) * ease_in_out(t / 0.6), y + 7], 7,
                        fill=T["line"] + (230,))
    for i, p in enumerate(pts):
        s, a = pop(t, p.get("delay", 0.15 + i * 0.15)); x = X(p["at"])
        im = icon(p["icon"], 150); iy = y - 150 + 8 * math.sin(t * 3 + i)
        shadow_or_glow(c, im, x, iy, s, a, 18)
        paste(c, im, x, iy, s, a)
        dot = Image.new("RGBA", (44, 44))
        ImageDraw.Draw(dot).ellipse([2, 2, 41, 41], fill=T["acc"], outline=T["stroke"], width=5)
        paste(c, dot, x, y, s, a)
        paste(c, ctext(p["label"], 40, None, max_w=300, path=F_BOLD, stroke=6), x, y + 70, s, a)
        yt = ctext(p["year"], 46, None, max_w=230, stroke=7, color=T["acc"])
        paste(c, yt, x, y + 105 + yt.height / 2, s, a)
    for j, sp in enumerate(sc.get("spans", [])):
        delay = sp.get("delay", 0.6 + j * 0.4); p = ease_out_cubic((t - delay) / 0.45)
        if p <= 0: continue
        xa, xb = X(sp["from"]), X(sp["to"]); cc = col(sp.get("color", "acc"))
        side = -1 if sp.get("side", "below") == "above" else 1
        yy = y + side * (250 if side > 0 else 300); xm = (xa + xb) / 2; hw = (xb - xa) / 2 * p
        d.line([(xm - hw, yy), (xm + hw, yy)], fill=cc + (255,), width=10)
        for xe in (xm - hw, xm + hw):
            d.line([(xe, yy - 26), (xe, yy + 26)], fill=cc + (255,), width=10)
        s, a = pop(t, delay + 0.2)
        paste(c, pill(sp["text"], 58, cc, WHITE), xm, yy + side * 80, s, a)

@functools.lru_cache(maxsize=4)
def _stamp():
    fnt = font(F_BLACK, 150); txt = "YOK ARTIK!"
    tw = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textlength(txt, font=fnt)
    w, h = int(tw + 110), 250
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, w - 6, h - 6], 40, fill=T["stamp_bg"], outline=WHITE, width=10)
    d.text((55, 38), txt, font=fnt, fill=T["stamp_fg"], stroke_width=6, stroke_fill=INK)
    return im

def scene_outro(c, sc, t, dur):
    s, a = pop(t, 0.0)
    im = icon(sc.get("icon", "1f92f"), 330); y = VIS_Y - 210 + 10 * math.sin(t * 4)
    shadow_or_glow(c, im, W / 2, y, s, a, 34)
    paste(c, im, W / 2, y, s, a)
    p = (t - 0.25) / 0.3
    if p > 0:
        paste(c, _stamp(), W / 2, VIS_Y + 80, 2.2 - 1.2 * ease_out_cubic(p), clamp(p * 2), rot=-6)
    if sc.get("text"):
        s2, a2 = pop(t, 0.7)
        paste(c, ctext(sc["text"], 64, sc.get("hl"), path=F_BOLD, stroke=8), W / 2, VIS_Y + 300, s2, a2)

SCENES = {"hook": scene_hook, "statement": scene_statement, "number": scene_number,
          "timeline": scene_timeline, "outro": scene_outro}

# ---------------------------------------------------------------- altyazı

def cap_tokens(scene):
    """Altyazı kelimeleri + grup kırılımları. cap içinde ' / ' ile elle öbek verilebilir."""
    toks, brks, br = [], [], True
    for t in CLEAN(scene.get("cap", scene["say"])).split():
        if t == "/":
            br = True; continue
        toks.append(t); brks.append(br); br = False
    return toks, brks

def build_caption_groups(words, max_chars=16, max_words=3):
    if any(w.get("brk") for w in words[1:]):
        groups, cur = [], []
        for w in words:
            if cur and (w.get("brk") or re.search(r"[.!?]$", cur[-1]["w"])):
                groups.append(cur); cur = []
            cur.append(w)
        if cur: groups.append(cur)
        return groups
    groups, cur = [], []
    particle = re.compile(r"^(Mİ|MI|MU|MÜ|DE|DA|Kİ)[,.?!]*$")
    for w in words:
        txt = " ".join(x["w"] for x in cur + [w])
        hard = bool(cur) and re.search(r"[.!?]$", cur[-1]["w"])
        soft = bool(cur) and (len(txt) > max_chars or len(cur) >= max_words)
        # MÖ/MS sayıdan, soru eki (mi, mı...) önceki kelimeden ayrılmaz
        keep = bool(cur) and (cur[-1]["w"] in ("MÖ", "MS") or particle.match(w["w"]))
        if hard or (soft and not keep):
            groups.append(cur); cur = []
        elif cur and re.search(r",$", cur[-1]["w"]) and len(cur) >= 2:
            groups.append(cur); cur = []
        cur.append(w)
    if cur: groups.append(cur)
    return groups

@functools.lru_cache(maxsize=512)
def caption_img(group_txt, active):
    fnt = font(F_BLACK, 86); words = group_txt.split("\u0001")
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    sp = tmp.textlength(" ", font=fnt); ws = [tmp.textlength(w, font=fnt) for w in words]
    total = sum(ws) + sp * (len(words) - 1)
    if total > 980:
        fnt = font(F_BLACK, int(86 * 980 / total)); ws = [tmp.textlength(w, font=fnt) for w in words]
        sp = tmp.textlength(" ", font=fnt); total = sum(ws) + sp * (len(words) - 1)
    im = Image.new("RGBA", (int(total + 60), 150)); d = ImageDraw.Draw(im); x = 30
    for i, w in enumerate(words):
        if i == active:
            d.rounded_rectangle([x - 14, 14, x + ws[i] + 14, 132], 22, fill=T["cap_hl_bg"])
            d.text((x, 22), w, font=fnt, fill=T["cap_hl_fg"])
        else:
            d.text((x, 22), w, font=fnt, fill=T["cap_text"], stroke_width=9, stroke_fill=T["cap_stroke"])
        x += ws[i] + sp
    return im

# ---------------------------------------------------------------- hizalama

def detect_silences(audio):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", audio, "-af", "silencedetect=noise=-38dB:d=0.16",
                        "-f", "null", "-"], capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    h, m, s = re.findall(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)[0]
    dur = int(h) * 3600 + int(m) * 60 + float(s)
    return list(zip(starts, ends + [dur] * (len(starts) - len(ends)))), dur

CLEAN = lambda x: re.sub(r"\[[^\]]*\]", "", x)

def align(scenes, audio):
    sil, dur = detect_silences(audio)
    speech_start = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
    speech_end = sil[-1][0] if sil and sil[-1][1] >= dur - 0.05 else dur
    weights = [sum(spoken_weight(w) for w in CLEAN(s["say"]).split()) for s in scenes]
    total = sum(weights); span = speech_end - speech_start
    inner = [s for s in sil if s[0] > speech_start + 0.2 and s[1] < speech_end - 0.2]
    bounds = [speech_start]; acc = 0; used = set()
    for wgt in weights[:-1]:
        acc += wgt; exp = speech_start + span * acc / total; best = None
        for i, (a, b) in enumerate(inner):
            if i in used or (a + b) / 2 <= bounds[-1] + 0.3: continue
            dist = abs((a + b) / 2 - exp) - min(0.25, (b - a)) * 0.6
            if best is None or dist < best[0]: best = (dist, i)
        if best and best[0] < 1.6:
            used.add(best[1]); a, b = inner[best[1]]; bounds.append(round((a + b) / 2, 3))
        else:
            bounds.append(exp)
    bounds.append(speech_end)
    words = []
    for k, s in enumerate(scenes):
        t0, t1 = bounds[k], bounds[k + 1]
        segs = [x for x in sil if t0 < x[0] < t1 and x[1] >= t1 - 0.05]
        t1s = segs[0][0] if segs else t1
        pre = [x for x in sil if x[0] <= t0 + 0.02 and x[1] > t0]
        t0s = min(pre[0][1], t1s - 0.3) if pre else t0
        toks, brks = cap_tokens(s)
        wts = [spoken_weight(w) for w in toks]; tw = sum(wts); a = t0s
        for tok, wt, br in zip(toks, wts, brks):
            b = a + (t1s - t0s) * wt / tw
            words.append({"w": tr_upper(tok), "s": a, "e": b, "scene": k, "brk": br}); a = b
    return bounds, words, dur

def align_from_words(scenes, words_path, dur):
    """ElevenLabs Scribe kelime zamanlarıyla kesin hizalama."""
    raw = json.load(open(words_path, encoding="utf-8"))
    raw = raw.get("words", raw) if isinstance(raw, dict) else raw
    sw = [w for w in raw if w.get("type", "word") == "word" and not w["text"].startswith("[")]
    counts = [len(CLEAN(s["say"]).split()) for s in scenes]
    if sum(counts) != len(sw):
        print(f"uyarı: kelime sayısı tutmadı ({sum(counts)} vs {len(sw)}), sessizlik hizalamasına dönülüyor",
              file=sys.stderr)
        return None
    groups, i = [], 0
    for n in counts:
        groups.append(sw[i:i + n]); i += n
    bounds = [0.0]
    for k in range(1, len(groups)):
        bounds.append(round((groups[k - 1][-1]["end"] + groups[k][0]["start"]) / 2, 3))
    bounds.append(min(dur, groups[-1][-1]["end"] + 0.05))
    words = []
    for k, (s, g) in enumerate(zip(scenes, groups)):
        toks, brks = cap_tokens(s)
        if len(toks) == len(g):
            for tok, w, br in zip(toks, g, brks):
                words.append({"w": tr_upper(tok), "s": w["start"], "e": w["end"], "scene": k, "brk": br})
        else:
            t0, t1 = g[0]["start"], g[-1]["end"]
            wts = [spoken_weight(x) for x in toks]; tw = sum(wts); a = t0
            for tok, wt, br in zip(toks, wts, brks):
                b = a + (t1 - t0) * wt / tw
                words.append({"w": tr_upper(tok), "s": a, "e": b, "scene": k, "brk": br}); a = b
    return bounds, words, dur

# ---------------------------------------------------------------- ses efektleri

def make_sfx(bounds, dur, path, sr=44100):
    n = int((dur + 1.5) * sr); out = np.zeros(n, np.float32); rng = np.random.default_rng(3)
    for t in bounds[:-1]:
        L = int(0.35 * sr); noise = rng.standard_normal(L).astype(np.float32)
        alpha = np.linspace(0.02, 0.35, L).astype(np.float32); y = np.zeros(L, np.float32); acc = 0.0
        for i in range(L): acc += alpha[i] * (noise[i] - acc); y[i] = acc
        env = np.sin(np.linspace(0, np.pi, L)) ** 2
        st = max(0, int((t - 0.12) * sr)); out[st:st + L] += (y * env)[: n - st] * 0.35
    t = bounds[-2] + 0.25; L = int(0.25 * sr); tt = np.arange(L) / sr
    thump = np.sin(2 * np.pi * 70 * tt) * np.exp(-tt * 18) + 0.3 * rng.standard_normal(L) * np.exp(-tt * 60)
    st = int(t * sr); out[st:st + L] += thump[: n - st].astype(np.float32) * 0.6
    pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(pcm.tobytes())

# ---------------------------------------------------------------- render

def draw_frame(bg, brand, scenes, bounds, groups, total, t):
    k = min(max(0, sum(1 for b in bounds[1:-1] if t >= b)), len(scenes) - 1)
    st = bounds[k]; en = bounds[k + 1] if k + 1 < len(bounds) else total; lt = t - st
    canvas = bg.frame(t)
    # ilk sahne: hook ilk karede tam görünür olsun (sessizde de okunabilsin)
    SCENES[scenes[k].get("type", "statement")](canvas, scenes[k], lt + (0.7 if k == 0 else 0), en - st)
    paste(canvas, brand, W / 2, 175, 1 + 0.04 * math.sin(t * 4))
    ImageDraw.Draw(canvas).rectangle([0, 0, W * (t / total), 12], fill=T["acc"])
    for gi, g in enumerate(groups):
        end = groups[gi + 1][0]["s"] - 0.05 if gi + 1 < len(groups) else g[-1]["e"] + 0.4
        if g[0]["s"] - 0.05 <= t < end:
            act = max([i for i, w in enumerate(g) if t >= w["s"] - 0.03] or [0])
            s = 0.85 + 0.15 * ease_out_back((t - g[0]["s"] + 0.05) / 0.18)
            paste(canvas, caption_img("\u0001".join(w["w"] for w in g), act), W / 2, 1460, s)
            break
    if lt < 0.08 and k > 0:
        canvas.alpha_composite(Image.new("RGBA", (W, H), T["flash"] + (int(70 * (1 - lt / 0.08)),)))
    return canvas

def setup(sc, theme=None):
    set_theme(theme or sc.get("theme", "pop"))
    bg = BACKGROUNDS[T["bg"]](seed=sum(map(ord, sc.get("id", "x"))) % 1000)
    brand = pill("YOK ARTIK!", 46, T["brand_bg"], T["brand_fg"])
    return bg, brand

def render(script_path, audio, out, theme=None, words_path=None):
    sc = json.load(open(script_path, encoding="utf-8")); scenes = sc["scenes"]
    bg, brand = setup(sc, theme)
    trimmed = os.path.splitext(os.path.abspath(out))[0] + "_vo.wav"
    res = None
    if words_path:
        # kelime zamanları orijinal sese göre: baştan kırpma yapma
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", audio, "-ar", "44100", trimmed], check=True)
        res = align_from_words(scenes, words_path, detect_silences(trimmed)[1])
    if res is None:
        # baştaki sessizliği kırp: ses ilk ~0,05 sn'de başlasın
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", audio, "-af",
                        "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.05,"
                        "areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.15,"
                        "areverse", "-ar", "44100", trimmed], check=True)
        res = align(scenes, trimmed)
    audio = trimmed
    bounds, words, adur = res
    total = adur + 0.6; nframes = int(total * FPS)
    groups = build_caption_groups(words)
    sfx = os.path.join(os.path.dirname(os.path.abspath(out)), "_sfx.wav"); make_sfx(bounds, total, sfx)
    json.dump({"bounds": bounds, "words": words, "theme": T["name"]}, open(out + ".timing.json", "w"),
              ensure_ascii=False, indent=1)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", audio, "-i", sfx,
           "-filter_complex", "[1:a]volume=1.0[v];[2:a]volume=0.55[s];[v][s]amix=inputs=2:duration=first:"
                              "normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart",
           "-t", f"{total:.2f}", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(nframes):
        ff.stdin.write(draw_frame(bg, brand, scenes, bounds, groups, total, f / FPS).convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    return ff.returncode

def preview(script_path, out_png, theme=None, scene_ids=(0, 2, 5, 6)):
    """Ses olmadan her sahneden birer kare (animasyon oturmuş halde) yan yana."""
    sc = json.load(open(script_path, encoding="utf-8")); scenes = sc["scenes"]
    bg, brand = setup(sc, theme)
    bounds = [i * 4.0 for i in range(len(scenes) + 1)]
    words = []
    for k, s in enumerate(scenes):
        toks, brks = cap_tokens(s)
        for j, (tok, br) in enumerate(zip(toks, brks)):
            a = bounds[k] + 3.5 * j / len(toks)
            words.append({"w": tr_upper(tok), "s": a, "e": a + 3.5 / len(toks), "scene": k, "brk": br})
    groups = build_caption_groups(words); total = bounds[-1]
    frames = [draw_frame(bg, brand, scenes, bounds, groups, total, bounds[k] + 3.2).convert("RGB")
              .resize((360, 640)) for k in scene_ids if k < len(scenes)]
    sheet = Image.new("RGB", (360 * len(frames) + 10 * (len(frames) - 1), 640), (255, 255, 255))
    for i, f in enumerate(frames): sheet.paste(f, (i * 370, 0))
    sheet.save(out_png)

if __name__ == "__main__":
    args = sys.argv[1:]; theme = None; words = None
    if "--theme" in args:
        i = args.index("--theme"); theme = args[i + 1]; del args[i:i + 2]
    if "--words" in args:
        i = args.index("--words"); words = args[i + 1]; del args[i:i + 2]
    if args[0] == "--preview":
        preview(args[1], args[2], theme)
    else:
        sys.exit(render(args[0], args[1], args[2], theme, words))
