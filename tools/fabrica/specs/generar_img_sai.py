#!/usr/bin/env python3
"""Dibujos propios para los TikToks de SAI (Unit 4 Codecs) -> specs/img/sai-*.png
Estilo: tinta oscura, rojo para lo importante, fondo transparente."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).parent / "img"
OUT.mkdir(exist_ok=True)
INK, RED, GRAY, GREEN, BLUE = "#141414", "#de2929", "#96928c", "#1e9646", "#2b6fd6"
LIGHT = "#f8f6f2"
plt.rcParams.update({"font.size": 15, "font.weight": "bold", "axes.edgecolor": INK})


def save(fig, name):
    fig.savefig(OUT / name, dpi=170, transparent=True, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def zigzag(n=8):
    out = []
    for s in range(2 * n - 1):
        rs = [r for r in range(n) if 0 <= s - r < n]
        if s % 2 == 0:
            rs = rs[::-1]
        out += [(r, s - r) for r in rs]
    return out  # (fila, col) en orden zig-zag


ZZ = zigzag()


def grid(ax, n=8):
    for r in range(n):
        for c in range(n):
            ax.add_patch(Rectangle((c, n - 1 - r), 1, 1, fc=LIGHT, ec=GRAY, lw=1))
    ax.set_xlim(-0.1, n + 0.1); ax.set_ylim(-0.1, n + 0.1); ax.set_aspect("equal"); ax.axis("off")


def cell(ax, r, c, txt, color=RED, n=8, fs=17):
    ax.add_patch(Rectangle((c, n - 1 - r), 1, 1, fc="#fde4e4", ec=color, lw=2.5))
    ax.text(c + .5, n - 1 - r + .5, txt, ha="center", va="center", color=color, fontsize=fs)


# ---- 1) orden zig-zag
fig, ax = plt.subplots(figsize=(6, 6))
grid(ax)
for k, (r, c) in enumerate(ZZ):
    if k <= 10:
        cell(ax, r, c, str(k), RED, fs=15)
    else:
        ax.text(c + .5, 7 - r + .5, str(k), ha="center", va="center", color=GRAY, fontsize=9)
pts = [(c + .5, 7 - r + .5) for r, c in ZZ[:11]]
ax.plot(*zip(*pts), color=RED, lw=1.6, alpha=.55)
ax.text(4, 8.55, "se lee en zig-zag →", ha="center", color=INK, fontsize=17)
save(fig, "sai-zigzag-orden.png")


# ---- 2) fila / columna
def fila_col(name, vals, fila=True, cap=""):
    fig, ax = plt.subplots(figsize=(6, 6))
    grid(ax)
    for i, v in enumerate(vals):
        cell(ax, 0 if fila else i, i if fila else 0, v)
    ax.text(4, 8.55, cap, ha="center", color=INK, fontsize=17)
    save(fig, name)


fila_col("sai-zz-fila.png", ["50", "20", "-10", "7"], True, "todo en la fila de arriba")
fila_col("sai-zz-columna.png", ["50", "20", "-10", "7"], False, "todo en la columna de la izquierda")

# ---- 3) GoP con N y M
COL = {"I": RED, "P": BLUE, "B": GREEN}


def cajas(ax, seq, y, x0=0, w=1.0, fs=15, labels=None):
    for i, t in enumerate(seq):
        ax.add_patch(Rectangle((x0 + i * w, y), w * .92, .9, fc=COL[t[0]], ec=INK, lw=1.5))
        ax.text(x0 + i * w + w * .46, y + .45, labels[i] if labels else t, color="white", ha="center", va="center", fontsize=fs)


fig, ax = plt.subplots(figsize=(6.4, 3.6))
seq = list("IBBPBBPBBI")
cajas(ax, seq, 1.6, w=1.0, fs=17)
# N: de I a antes de la siguiente I
ax.annotate("", xy=(0, 1.2), xytext=(9.92, 1.2), arrowprops=dict(arrowstyle="<->", color=RED, lw=2.4))
ax.text(4.9, .5, "N = 9  (de una I a la siguiente)", ha="center", color=RED, fontsize=17)
# M: I -> P
ax.annotate("", xy=(0.46, 2.85), xytext=(3.46, 2.85), arrowprops=dict(arrowstyle="<->", color=INK, lw=2.4))
ax.text(1.96, 3.15, "M = 3", ha="center", color=INK, fontsize=17)
ax.set_xlim(-.2, 10.3); ax.set_ylim(0, 3.7); ax.axis("off")
save(fig, "sai-gop-nm.png")

# ---- 4) reordenado M=4
fig, ax = plt.subplots(figsize=(6.4, 4.4))
cap = ["I0", "B1", "B2", "B3", "P4", "B5", "B6", "B7", "I8"]
cod = ["I0", "P4", "B1", "B2", "B3", "I8", "B5", "B6", "B7"]
ax.text(-.1, 6.15, "Así sale de la cámara", fontsize=15, color=GRAY, va="bottom")
cajas(ax, cap, 5.15, w=1.0, fs=14, labels=cap)
ax.text(-.1, 3.65, "Así se codifica y se manda", fontsize=15, color=RED, va="bottom")
cajas(ax, cod, 2.65, w=1.0, fs=14, labels=cod)
ax.text(-.1, 1.15, "Así se reproduce", fontsize=15, color=GRAY, va="bottom")
cajas(ax, cap, .15, w=1.0, fs=14, labels=cap)
ax.set_xlim(-.2, 9.4); ax.set_ylim(0, 7.0); ax.axis("off")
save(fig, "sai-reorden.png")

# ---- 5) perfiles bytes/imagen
rng = np.random.default_rng(7)
fig, axs = plt.subplots(2, 2, figsize=(6.4, 4.6))
perf = {}
perf["A"] = [30] * 24
perf["B"] = list(np.clip(22 + rng.normal(0, 5, 24), 8, 38))
perf["C"] = [(40 if i % 8 == 0 else 16 if i % 4 == 0 else 8) for i in range(24)]
perf["D"] = [40] + [4 + abs(rng.normal(0, 1.2)) for _ in range(10)] + [14] + [4 + abs(rng.normal(0, 1.2)) for _ in range(12)]
for ax, (k, v) in zip(axs.flat, perf.items()):
    ax.bar(range(len(v)), v, color=RED if k == "C" else INK, width=.75)
    ax.set_title(k, color=RED, fontsize=19, loc="left", pad=2)
    ax.set_ylim(0, 46); ax.set_xticks([]); ax.set_yticks([])
    for s in ("top", "right"): ax.spines[s].set_visible(False)
plt.tight_layout()
save(fig, "sai-perfiles.png")

# ---- 6) cambio de escena
fig, ax = plt.subplots(figsize=(6.4, 3.8))
tipos = []
for i in range(44):
    j = i if i < 22 else i - 22
    if i < 22:
        tipos.append("I" if i % 14 == 0 else ("P" if i % 2 == 0 else "B"))
    else:
        tipos.append("I" if j % 14 == 0 else ("P" if j % 2 == 0 else "B"))
tam = {"I": 40, "P": 17, "B": 8}
ax.bar(range(44), [tam[t] for t in tipos], color=[COL[t] for t in tipos], width=.78)
ax.annotate("cambio de escena:\nuna P pasa a I", xy=(22, 41), xytext=(25, 46), color=RED, fontsize=16,
            arrowprops=dict(arrowstyle="->", color=RED, lw=2.4))
ax.set_ylim(0, 58); ax.set_xticks([]); ax.set_yticks([])
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.set_ylabel("bytes / imagen", fontsize=14)
save(fig, "sai-escena.png")

# ---- 7) JPEG progresivo: 3 barridos
n = 64
yy, xx = np.mgrid[0:n, 0:n]
img = 80 + 120 * ((xx - 32) ** 2 + (yy - 30) ** 2 < 17 ** 2) + 40 * (xx / n)
img[8:14, 6:58] = 30
img[44:60, 40:56] = 250
img = img.astype(float) - 128


def dctm(N=8):
    M = np.zeros((N, N))
    for k in range(N):
        for i in range(N):
            M[k, i] = np.cos((2 * i + 1) * k * np.pi / 16)
    M *= np.sqrt(2 / N); M[0] /= np.sqrt(2)
    return M


M = dctm()


def recon(maxfreq):
    out = np.zeros_like(img)
    for by in range(0, n, 8):
        for bx in range(0, n, 8):
            B = img[by:by + 8, bx:bx + 8]
            C = M @ B @ M.T
            mask = np.add.outer(np.arange(8), np.arange(8)) <= maxfreq
            out[by:by + 8, bx:bx + 8] = M.T @ (C * mask) @ M
    return np.clip(out + 128, 0, 255)


fig, axs = plt.subplots(1, 3, figsize=(7.4, 3.0))
for ax, (mf, tit) in zip(axs, [(0, "1.º barrido"), (2, "2.º barrido"), (14, "al final")]):
    ax.imshow(recon(mf), cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    ax.set_title(tit, fontsize=15, color=RED if mf == 14 else INK)
    ax.axis("off")
plt.tight_layout()
save(fig, "sai-progresivo.png")

# ---- 8) enmascaramiento
f = np.logspace(np.log10(.2), np.log10(12), 400)
umbral = 3.64 * f ** -.8 - 6.5 * np.exp(-.6 * (f - 3.3) ** 2) + 1e-3 * f ** 4
f0, L0 = 1.0, 60
mask = np.where(f < f0, L0 - 8 - 55 * (np.log2(f0 / f)), L0 - 8 - 22 * np.log2(f / f0))
mask = np.maximum(mask, umbral)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.plot(f, umbral, color=GRAY, lw=2.4, label="lo mínimo que se oye (en silencio)")
ax.fill_between(f, umbral, mask, color=RED, alpha=.18)
ax.plot(f, mask, color=RED, lw=2.8)
ax.vlines(f0, -10, L0, color=INK, lw=7)
ax.text(f0, L0 + 3, "tono fuerte\n60 dB", ha="center", color=INK, fontsize=15)
ax.vlines(1.3, -10, 36, color=GRAY, lw=7)
ax.text(1.75, 38, "este NO se oye", color=RED, fontsize=16)
ax.set_xscale("log"); ax.set_ylim(-10, 84); ax.set_xlim(.2, 12)
ax.set_xticks([.2, 1, 5, 10]); ax.set_xticklabels(["0,2", "1", "5", "10 kHz"])
ax.set_yticks([]); ax.set_ylabel("nivel (dB)", fontsize=14)
for s in ("top", "right"): ax.spines[s].set_visible(False)
save(fig, "sai-enmascara.png")
print("imágenes OK:", sorted(p.name for p in OUT.glob("sai-*.png")))
