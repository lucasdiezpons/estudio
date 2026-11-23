#!/usr/bin/env python3
"""Renderiza un vídeo vertical estilo TikTok a partir de spec + tiempos de voz."""
import json, math, os, subprocess, sys
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).parent
GREEN = (30, 150, 70)

W, H, FPS = 720, 1280, 30
BG = (239, 235, 228)
INK = (20, 20, 20)
RED = (222, 41, 41)
GRAY = (150, 146, 140)
FAINT = (200, 196, 189)
CARD = (255, 255, 255)

_FD = Path(__file__).parent / "fonts"
F = {
    "anton": str(_FD / "Anton-Regular.ttf"),
    "inter": str(_FD / "Inter-SemiBold.otf"),
    "interb": str(_FD / "Inter-Bold.otf"),
    "ital": str(_FD / "CrimsonText-SemiBoldItalic.ttf"),
    "mono": str(_FD / "DejaVuSansMono.ttf"),
    "emoji": str(_FD / "NotoColorEmoji.ttf"),
}


@lru_cache(None)
def font(name, size):
    return ImageFont.truetype(F[name], size)


@lru_cache(None)
def emoji(ch, size):
    f = ImageFont.truetype(F["emoji"], 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    bb = im.getbbox()
    if not bb:
        im = Image.new("RGBA", (40, 40), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((4, 4, 36, 36), fill=RED)
    else:
        im = im.crop(bb)
    r = size / max(im.size)
    return im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)


# ---------- easing ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_back(x):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def paste_anim(base, layer, xy, t, t0, dur=0.28, s0=0.86, slam=False):
    """Pega layer (RGBA) con pop-in. xy = centro."""
    p = clamp((t - t0) / dur)
    if p <= 0:
        return
    if slam:
        s = 1.7 - 0.7 * (1 - (1 - p) ** 3)
    else:
        s = s0 + (1 - s0) * ease_back(p)
    a = clamp(p * 1.6)
    lw, lh = max(1, int(layer.width * s)), max(1, int(layer.height * s))
    L = layer.resize((lw, lh), Image.BILINEAR) if (lw, lh) != layer.size else layer
    if a < 1:
        L = L.copy()
        L.putalpha(L.getchannel("A").point(lambda v: int(v * a)))
    base.alpha_composite(L, (int(xy[0] - lw / 2), int(xy[1] - lh / 2)))


# ---------- piezas ----------
def fondo():
    im = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(im)
    for y in range(0, H, 22):
        for x in range(0, W, 22):
            d.point((x, y), fill=(225, 220, 212, 255))
    return im


def rich_title(text, maxw, size=86):
    """'TT *VS* TN' -> imagen con palabras rojas."""
    parts = []
    for chunk in text.split("*"):
        parts.append(chunk)
    while True:
        f = font("anton", size)
        widths = [f.getlength(p) for p in parts]
        if sum(widths) <= maxw or size < 40:
            break
        size -= 4
    asc, desc = f.getmetrics()
    im = Image.new("RGBA", (int(sum(widths)) + 4, asc + desc + 6), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 0
    for i, p in enumerate(parts):
        d.text((x, 0), p, font=f, fill=RED if i % 2 else INK)
        x += widths[i]
    return im


def num_box(n):
    im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 63, 63), 10, fill=INK)
    f = font("anton", 44)
    d.text((32, 30), str(n), font=f, fill=(255, 255, 255), anchor="mm")
    return im


def stamp(text):
    f = font("anton", 54)
    tw = int(f.getlength(text))
    im = Image.new("RGBA", (tw + 50, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, tw + 44, 90), 10, outline=RED, width=6, fill=(255, 255, 255, 230))
    d.text(((tw + 48) / 2, 47), text, font=f, fill=RED, anchor="mm")
    return im.rotate(-8, expand=True, resample=Image.BICUBIC)


def card(w, h):
    sh = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((20, 26, w + 20, h + 26), 22, fill=(0, 0, 0, 40))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    ImageDraw.Draw(sh).rounded_rectangle((20, 20, w + 20, h + 20), 22, fill=CARD + (255,))
    return sh


def fit(name, size, txt, maxw):
    while font(name, size).getlength(txt) > maxw and size > 14:
        size -= 2
    return font(name, size)


def text_img(txt, fnt, fill, pad=4):
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bb = tmp.multiline_textbbox((0, 0), txt, font=fnt, align="center")
    im = Image.new("RGBA", (int(bb[2]) + pad * 2, int(bb[3]) + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).multiline_text((pad, pad), txt, font=fnt, fill=fill, align="center")
    return im


# ---------- subtítulo palabra a palabra ----------
def layout_sub(words, maxw=650, big=42, small=32):
    lines, cur, x = [], [], 0
    for w in words:
        f = font("ital", big) if w["rojo"] else font("inter", small)
        ww = f.getlength(w["w"] + " ")
        if x + ww > maxw and cur:
            lines.append(cur); cur, x = [], 0
        cur.append((w, x, f)); x += ww
    if cur:
        lines.append(cur)
    if len(lines) > 3 and small > 26:
        return layout_sub(words, maxw, big - 3, small - 3)
    return lines


def draw_sub(base, lines, t, y0=154):
    d = ImageDraw.Draw(base)
    y = y0
    for line in lines:
        for w, x, f in line:
            col = (RED if w["rojo"] else INK) if t >= w["t0"] - 0.02 else FAINT
            d.text((40 + x, y + 40), w["w"], font=f, fill=col, anchor="ls")
        y += 46


# ---------- visuales ----------
CX, CY0, CW, CH = W // 2, 478, 650, 545   # tarjeta: centro x, y arriba, ancho, alto


def word_time(words, key, default):
    for w in words:
        if w["w"] == key:
            return w["t0"]
    return default


def visual(base, v, t, s0, s1, words):
    dur = s1 - s0
    tipo = v["tipo"]
    if tipo in NUEVOS:
        return visual_nuevo(base, v, t, s0, s1, words)
    if tipo == "big":
        paste_anim(base, card(CW, CH), (CX, CY0 + CH / 2), t, s0 + 0.1)
        paste_anim(base, text_img(v["big"], fit("anton", 240, v["big"], 560), INK), (CX, CY0 + 225), t, s0 + 0.3)
        paste_anim(base, text_img(v["small"], fit("interb", 36, v["small"], 580), GRAY), (CX, CY0 + 455), t, s0 + 0.5)
        if v.get("stamp"):
            paste_anim(base, stamp(v["stamp"]), (CX + 170, CY0 + 130), t, s0 + dur * 0.55, slam=True)

    elif tipo == "diagrama":
        paste_anim(base, card(CW, CH), (CX, CY0 + CH / 2), t, s0 + 0.05)
        if t < s0 + 0.2:
            return
        d = ImageDraw.Draw(base)
        # equipo
        bx, by = CX, CY0 + 120
        eq = Image.new("RGBA", (320, 150), (0, 0, 0, 0))
        ed = ImageDraw.Draw(eq)
        ed.rounded_rectangle((0, 0, 319, 149), 18, fill=(245, 243, 239), outline=INK, width=4)
        ed.text((160, 55), "EQUIPO", font=font("anton", 52), fill=INK, anchor="mm")
        ed.text((160, 115), "carcasa metálica", font=font("inter", 26), fill=GRAY, anchor="mm")
        paste_anim(base, eq, (bx, by), t, s0 + 0.2)
        # cable que crece
        p = clamp((t - (s0 + 0.6)) / 0.9)
        if p > 0:
            ytop, ybot = by + 76, CY0 + 392
            ycur = ytop + (ybot - ytop) * p
            for yy in range(int(ytop), int(ycur), 24):
                col = (40, 160, 70) if (yy // 24) % 2 == 0 else (235, 200, 30)
                d.line((bx, yy, bx, min(yy + 24, ycur)), fill=col, width=12)
            lbl = text_img("cable de\nprotección", font("interb", 28), GRAY)
            paste_anim(base, lbl, (bx + 130, (ytop + ybot) / 2), t, s0 + 0.9)
        tend = s0 + 1.5
        if v["destino"] == "tierra":
            g = Image.new("RGBA", (260, 150), (0, 0, 0, 0))
            gd = ImageDraw.Draw(g)
            for i, ww in enumerate((190, 125, 60)):
                gd.line((130 - ww / 2, 10 + i * 26, 130 + ww / 2, 10 + i * 26), fill=INK, width=10)
            gd.text((130, 120), "TIERRA", font=font("anton", 46), fill=RED, anchor="mm")
            paste_anim(base, g, (bx, CY0 + 462), t, tend)
        else:
            n = Image.new("RGBA", (440, 120), (0, 0, 0, 0))
            nd = ImageDraw.Draw(n)
            nd.rounded_rectangle((0, 20, 439, 60), 8, fill=(40, 90, 200))
            nd.text((220, 40), "N", font=font("anton", 30), fill=(255, 255, 255), anchor="mm")
            nd.text((220, 100), "NEUTRO", font=font("anton", 46), fill=RED, anchor="mm")
            paste_anim(base, n, (bx, CY0 + 455), t, tend)

    elif tipo == "alerta":
        paste_anim(base, card(CW, CH), (CX, CY0 + CH / 2), t, s0 + 0.05)
        paste_anim(base, emoji(v["icono"], 200), (CX, CY0 + 150), t, s0 + 0.25)
        paste_anim(base, text_img(v["linea1"], fit("interb", 31, v["linea1"], 590), INK), (CX, CY0 + 310), t, s0 + 0.5)
        m = Image.new("RGBA", (480, 130), (0, 0, 0, 0))
        md = ImageDraw.Draw(m)
        md.rounded_rectangle((0, 0, 479, 129), 18, fill=(245, 243, 239), outline=INK, width=4)
        md.text((240, 65), v["linea2"].upper(), font=fit("anton", 54, v["linea2"].upper(), 440), fill=INK, anchor="mm")
        paste_anim(base, m, (CX, CY0 + 408), t, s0 + dur * 0.4)
        if v.get("stamp"):
            paste_anim(base, stamp(v["stamp"]), (CX + 120, CY0 + 492), t, s0 + dur * 0.62, slam=True)

    elif tipo == "filas":
        filas = v["filas"]
        paste_anim(base, card(CW, CH), (CX, CY0 + CH / 2), t, s0 + 0.05)
        n = len(filas)
        rh = 215 if n <= 2 else 178
        bh = rh - 20
        ytop = CY0 + CH / 2 - rh * (len(filas) - 1) / 2 - (40 if v.get("stamp") else 0)
        prev = s0
        for i, r in enumerate(filas):
            ta = word_time(words, r.get("en"), None) if r.get("en") else None
            if ta is None:
                ta = max(s0 + 0.3 + i * dur / (len(filas) + 1), prev + 0.6)
            prev = ta
            row = Image.new("RGBA", (600, bh), (0, 0, 0, 0))
            rd = ImageDraw.Draw(row)
            rd.rounded_rectangle((0, 0, 599, bh - 1), 20, fill=(248, 246, 242), outline=(225, 220, 212), width=3)
            ic = emoji(r["icono"], 84 if n <= 2 else 70)
            row.alpha_composite(ic, (24, int(bh / 2 - ic.height / 2)))
            rd.text((128, bh * 0.32), r["izq"], font=fit("inter", 30, r["izq"], 455), fill=GRAY, anchor="lm")
            fz = 66 if n <= 2 else 56
            while font("anton", fz).getlength(r["der"]) > 450 and fz > 26:
                fz -= 2
            rd.text((128, bh * 0.66), r["der"], font=font("anton", fz), fill=RED if r.get("rojo") else INK, anchor="lm")
            paste_anim(base, row, (CX, ytop + i * rh), t, ta - 0.05)
        if v.get("stamp"):
            paste_anim(base, stamp(v["stamp"]), (CX + 170, CY0 + CH - 60), t, s0 + dur * 0.8, slam=True)


# ---------- visuales nuevos (circuito, imagen, grafica, calculo, vs, pregunta) ----------
@lru_cache(None)
def _img_fit(path, maxw, maxh):
    im = Image.open(path).convert("RGBA")
    bb = im.getbbox()
    if bb:
        im = im.crop(bb)
    r = min(maxw / im.width, maxh / im.height)
    return im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)


def _when(words, en, default):
    return word_time(words, en, default) if en else default


def _pie(base, txt, t, t0):
    if txt:
        paste_anim(base, text_img(txt, fit("interb", 30, txt, 590), GRAY), (CX, CY0 + CH - 40), t, t0)


@lru_cache(None)
def _grafica_png(key):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    v = json.loads(key)
    x0, x1 = v.get("x", [0, 10])
    x = np.linspace(x0, x1, 400)
    fig, ax = plt.subplots(figsize=(6.0, 4.6), dpi=110)
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    for c in v.get("curvas", []):
        y = eval(c["f"], {"np": np, "x": x, "pi": np.pi, "sin": np.sin, "cos": np.cos, "exp": np.exp,
                          "sqrt": np.sqrt, "abs": np.abs, "clip": np.clip, "log": np.log})
        ax.plot(x, y * np.ones_like(x), lw=4, color="#de2929" if c.get("rojo") else "#141414",
                ls="--" if c.get("discontinua") else "-", label=c.get("label"))
    for p in v.get("puntos", []):
        ax.plot([p["x"]], [p["y"]], "o", ms=12, color="#de2929")
        if p.get("txt"):
            ax.annotate(p["txt"], (p["x"], p["y"]), textcoords="offset points", xytext=(10, 10),
                        fontsize=17, color="#de2929", weight="bold")
    if v.get("y"):
        ax.set_ylim(*v["y"])
    ax.set_xlabel(v.get("xlabel", ""), fontsize=17); ax.set_ylabel(v.get("ylabel", ""), fontsize=17)
    ax.tick_params(labelsize=13)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(alpha=0.25)
    if any(c.get("label") for c in v.get("curvas", [])):
        ax.legend(fontsize=15, frameon=False)
    fig.tight_layout()
    p = HERE / "out" / "_graf" / (str(abs(hash(key))) + ".png")
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(p, transparent=True); plt.close(fig)
    return str(p)


def _txt_marca(txt, f, col):
    """Texto + ✓/✗ final (Anton/Inter no tienen esos símbolos: se dibujan con DejaVu)."""
    txt = txt.rstrip()
    if not txt or txt[-1] not in "✓✗✔✘":
        return text_img(txt, f, col)
    m = txt[-1]
    a = text_img(txt[:-1].rstrip(), f, col)
    b = text_img("✓" if m in "✓✔" else "✗", font("mono", int(f.size * 0.9)), GREEN if m in "✓✔" else RED)
    im = Image.new("RGBA", (a.width + 18 + b.width, max(a.height, b.height)), (0, 0, 0, 0))
    im.alpha_composite(a, (0, (im.height - a.height) // 2))
    im.alpha_composite(b, (a.width + 18, (im.height - b.height) // 2))
    return im


def visual_nuevo(base, v, t, s0, s1, words):
    dur = s1 - s0
    tipo = v["tipo"]
    paste_anim(base, card(CW, CH), (CX, CY0 + CH / 2), t, s0 + 0.05)
    maxh = CH - (110 if v.get("pie") else 50)

    if tipo == "circuito":
        import circuitos
        rojo, tr = list(v.get("rojo", [])), s0 + 0.25
        for p in v.get("pasos", []):
            tp = _when(words, p.get("en"), None)
            if tp is not None and t >= tp - 0.05:
                rojo = p.get("rojo", rojo)
        img = _img_fit(str(circuitos.png(v["nombre"], rojo, v.get("valores"))), CW - 50, maxh)
        paste_anim(base, img, (CX, CY0 + 25 + maxh / 2), t, tr, s0=0.95)
        _pie(base, v.get("pie"), t, s0 + 0.6)

    elif tipo == "imagen":
        p = Path(v["archivo"])
        if not p.is_absolute():
            p = HERE / "specs" / p
        img = _img_fit(str(p), CW - 50, maxh)
        paste_anim(base, img, (CX, CY0 + 25 + maxh / 2), t, _when(words, v.get("en"), s0 + 0.25), s0=0.95)
        _pie(base, v.get("pie"), t, s0 + 0.6)

    elif tipo == "grafica":
        img = _img_fit(_grafica_png(json.dumps({k: v[k] for k in v if k not in ("pie", "en")}, sort_keys=True)),
                       CW - 40, maxh)
        t0 = _when(words, v.get("en"), s0 + 0.3)
        p = clamp((t - t0) / 1.4)
        if p > 0:
            # eje y fijo + la curva "se dibuja" de izquierda a derecha
            wv = max(1, int(img.width * (0.12 + 0.88 * p)))
            base.alpha_composite(img.crop((0, 0, wv, img.height)),
                                 (int(CX - img.width / 2), int(CY0 + 25 + maxh / 2 - img.height / 2)))
        _pie(base, v.get("pie"), t, t0 + 1.2)

    elif tipo == "calculo":
        lineas = v["lineas"]
        n = len(lineas)
        lh = min(120, (CH - 80) / max(n, 1))
        y = CY0 + CH / 2 - lh * (n - 1) / 2
        prev = s0
        for i, ln in enumerate(lineas):
            ta = _when(words, ln.get("en"), None)
            if ta is None:
                ta = max(s0 + 0.3 + i * dur / (n + 1), prev + 0.5)
            prev = ta
            last = ln.get("rojo") or i == n - 1 and v.get("resaltar_final", True)
            f = fit("anton" if last else "interb", 64 if last else 40, ln["txt"], 580)
            paste_anim(base, _txt_marca(ln["txt"], f, RED if last else INK), (CX, y + i * lh), t, ta - 0.05)

    elif tipo == "vs":
        ganador = v.get("ganador")
        tg = _when(words, v.get("en"), s0 + dur * 0.7)
        for k, lado in enumerate(("izq", "der")):
            col = v[lado]
            cx = CX - 160 + 320 * k
            ta = s0 + 0.25 + 0.35 * k
            if col.get("icono"):
                paste_anim(base, emoji(col["icono"], 110), (cx, CY0 + 100), t, ta)
            paste_anim(base, text_img(col["titulo"], fit("anton", 52, col["titulo"], 280), INK), (cx, CY0 + 205), t, ta)
            for j, pt in enumerate(col.get("puntos", [])):
                paste_anim(base, text_img(pt, fit("inter", 28, pt, 280), GRAY), (cx, CY0 + 275 + j * 48), t, ta + 0.2 + 0.15 * j)
            if ganador == lado and t >= tg:
                d = ImageDraw.Draw(base)
                d.rounded_rectangle((cx - 150, CY0 + 30, cx + 150, CY0 + CH - 30), 20, outline=RED, width=6)
        ImageDraw.Draw(base).line((CX, CY0 + 60, CX, CY0 + CH - 60), fill=FAINT, width=3) if t > s0 + 0.2 else None
        if v.get("stamp"):
            paste_anim(base, stamp(v["stamp"]), (CX, CY0 + CH - 70), t, tg, slam=True)

    elif tipo == "pregunta":
        ops = v["opciones"]
        tr = _when(words, v.get("en"), s0 + dur * 0.75)
        paste_anim(base, text_img(v["pregunta"], fit("interb", 34, v["pregunta"], 590), INK), (CX, CY0 + 70), t, s0 + 0.2)
        rh = min(110, (CH - 170) / len(ops))
        for i, op in enumerate(ops):
            ok = i == v["correcta"]
            revel = t >= tr
            row = Image.new("RGBA", (590, int(rh - 16)), (0, 0, 0, 0))
            rd = ImageDraw.Draw(row)
            fill = (225, 245, 230) if (revel and ok) else (248, 246, 242)
            outl = GREEN if (revel and ok) else (225, 220, 212)
            rd.rounded_rectangle((0, 0, 589, row.height - 1), 16, fill=fill, outline=outl, width=4 if revel and ok else 3)
            colt = GREEN if (revel and ok) else (FAINT if revel else INK)
            rd.text((24, row.height / 2), "ABCD"[i] + ")  " + op, font=fit("interb", 32, op, 470), fill=colt, anchor="lm")
            if revel:
                rd.text((560, row.height / 2), "✓" if ok else "✗", font=font("mono", 40), fill=GREEN if ok else RED, anchor="mm")
            paste_anim(base, row, (CX, CY0 + 170 + i * rh), t, s0 + 0.4 + 0.25 * i)


NUEVOS = {"circuito", "imagen", "grafica", "calculo", "vs", "pregunta"}


# ---------- sonido: efectos suaves generados (sin descargar nada) ----------
SR = 44100


def _sfx(kind):
    import numpy as np
    if kind == "whoosh":
        n = int(SR * 0.35); t = np.arange(n) / SR
        noise = np.random.default_rng(1).normal(0, 1, n)
        k = np.convolve(noise, np.ones(30) / 30, mode="same")       # ruido suave
        env = np.sin(np.pi * t / t[-1]) ** 2
        return 0.10 * k * env / (abs(k).max() + 1e-9)
    if kind == "pop":
        n = int(SR * 0.12); t = np.arange(n) / SR
        f = 900 - 500 * t / t[-1]
        return 0.16 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40)
    if kind == "ding":
        n = int(SR * 0.6); t = np.arange(n) / SR
        return 0.14 * (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1976 * t)) * np.exp(-t * 6)
    raise ValueError(kind)


def mezclar_audio(voz_mp3, eventos, total, destino):
    """Voz + efectos -> wav. eventos = [(t, 'whoosh'|'pop'|'ding')]."""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(voz_mp3), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    voz = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    n = max(len(voz), int((total + 0.5) * SR))
    mix = np.zeros(n, dtype=np.float32); mix[:len(voz)] += voz
    for t0, kind in eventos:
        x = _sfx(kind); i = int(t0 * SR)
        if 0 <= i < n:
            m = min(len(x), n - i); mix[i:i + m] += x[:m]
    mix = np.clip(mix, -1, 1)
    import wave
    with wave.open(str(destino), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    return destino


def eventos_sfx(segs, starts, ends, tiempos):
    ev = [(starts[i], "whoosh") for i in range(1, len(segs))]
    for i, s in enumerate(segs):
        v = s.get("visual", {}); s0, s1 = starts[i], ends[i]
        if v.get("stamp"):
            ev.append((s0 + (s1 - s0) * 0.6, "pop"))
        if v.get("tipo") == "pregunta":
            ev.append((word_time(tiempos[i], v.get("en"), s0 + (s1 - s0) * 0.75) if v.get("en") else s0 + (s1 - s0) * 0.75, "ding"))
        if v.get("tipo") == "calculo":
            ln = v["lineas"][-1]
            ev.append((word_time(tiempos[i], ln.get("en"), s1 - 0.8) if ln.get("en") else s1 - 0.8, "ding"))
    return ev


def barra(fr, t, total):
    d = ImageDraw.Draw(fr)
    d.rectangle((0, H - 10, W, H), fill=FAINT)
    d.rectangle((0, H - 10, int(W * clamp(t / total)), H), fill=RED)


# ---------- main ----------
def main(spec_path):
    spec = json.loads(Path(spec_path).read_text("utf-8"))
    out = Path(__file__).parent / "out" / spec["id"]
    tiempos = json.loads((out / "tiempos.json").read_text("utf-8"))
    segs = spec["segmentos"]
    starts = [max(0.0, row[0]["t0"] - 0.15) for row in tiempos]
    starts[0] = 0.0
    total = tiempos[-1][-1]["t1"] + 1.6
    ends = starts[1:] + [total]

    bg = fondo()
    pre = []
    for s, row in zip(segs, tiempos):
        pre.append({
            "lines": layout_sub(row),
            "title": rich_title(s["titulo"], 560 if s.get("num") else 640),
            "num": num_box(s["num"]) if s.get("num") else None,
            "tag": "// " + s["tag"],
        })

    nframes = int(total * FPS)
    audio = out / "voz.mp3"
    if spec.get("sfx", True) and os.environ.get("SFX", "1") != "0":
        audio = mezclar_audio(out / "voz.mp3", eventos_sfx(segs, starts, ends, tiempos), total, out / "mezcla.wav")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(audio),
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p",
                           "-af", "apad", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart",
                           str(out / f"{spec['id']}.mp4")], stdin=subprocess.PIPE)
    for k in range(nframes):
        t = k / FPS
        i = max(j for j in range(len(segs)) if starts[j] <= t)
        s0, s1, P = starts[i], ends[i], pre[i]
        fr = bg.copy()
        d = ImageDraw.Draw(fr)
        d.text((40, 118), P["tag"] + "   ·   " + spec["etiqueta"], font=font("mono", 18), fill=GRAY)
        draw_sub(fr, P["lines"], t)
        tl = P["title"]
        ty = 390
        paste_anim(fr, tl, (40 + tl.width / 2, ty), t, s0 + 0.05)
        if P["num"]:
            paste_anim(fr, P["num"], (W - 40 - 32, ty), t, s0 + 0.15)
        visual(fr, segs[i]["visual"], t, s0, s1, tiempos[i])
        barra(fr, t, total)
        ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    # miniatura
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2.5", "-i", str(out / f"{spec['id']}.mp4"),
                    "-frames:v", "1", "-vf", "scale=288:-2", "-q:v", "5", str(out / f"{spec['id']}.jpg")])
    print("OK", out / f"{spec['id']}.mp4", round(total, 1), "s")


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    main(sys.argv[1])
