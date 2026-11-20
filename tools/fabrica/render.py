#!/usr/bin/env python3
"""Renderiza un vídeo vertical estilo TikTok a partir de spec + tiempos de voz."""
import json, math, subprocess, sys
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(out / "voz.mp3"),
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
        ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    # miniatura
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2.5", "-i", str(out / f"{spec['id']}.mp4"),
                    "-frames:v", "1", "-vf", "scale=288:-2", "-q:v", "5", str(out / f"{spec['id']}.jpg")])
    print("OK", out / f"{spec['id']}.mp4", round(total, 1), "s")


if __name__ == "__main__":
    main(sys.argv[1])
