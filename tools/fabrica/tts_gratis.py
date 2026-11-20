#!/usr/bin/env python3
"""Igual que tts.py pero con voz GRATIS (edge-tts, es-MX-DaliaNeural) y tiempos por palabra (WordBoundary).
Uso: python tts_gratis.py specs/X.json      (VOZ_FAKE=1 → audio en silencio, para probar sin internet)"""
import asyncio, json, os, re, subprocess, sys, unicodedata
from pathlib import Path

VOICE = os.environ.get("VOZ", "es-MX-DaliaNeural")
RATE = os.environ.get("VOZ_RATE", "+8%")
FAKE = os.environ.get("VOZ_FAKE") == "1"
PUNCT = "¿?¡!.,:;"


def tokens(seg_sub):
    out = []
    for raw in seg_sub.split():
        mute = raw.startswith("[") and raw.endswith("]")
        if mute:
            raw = raw[1:-1]
        rojo = "*" in raw
        disp = raw.replace("*", "")
        out.append([disp, None if mute else disp, rojo])
    return out


def spoken(word, pron):
    core = word.strip(PUNCT)
    if core in pron:
        i = word.find(core)
        return word[:i] + pron[core] + word[i + len(core):]
    return word


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c)[0] in "LN")
    return w


async def _edge(text, mp3):
    import edge_tts
    for intento in range(5):
        try:
            try:
                c = edge_tts.Communicate(text, VOICE, rate=RATE, boundary="WordBoundary")
            except TypeError:  # versiones antiguas: WordBoundary por defecto
                c = edge_tts.Communicate(text, VOICE, rate=RATE)
            bounds, audio = [], bytearray()
            async for ch in c.stream():
                if ch["type"] == "audio":
                    audio += ch["data"]
                elif ch["type"] == "WordBoundary":
                    t0 = ch["offset"] / 1e7
                    bounds.append({"t": ch["text"], "t0": t0, "t1": t0 + ch["duration"] / 1e7})
            if audio and bounds:
                Path(mp3).write_bytes(bytes(audio))
                return bounds
            print("   (voz vacía, reintento)")
        except Exception as e:
            print("   reintento voz:", e)
        await asyncio.sleep(2 + 3 * intento)
    sys.exit("No se pudo generar la voz (¿hay internet?)")


def _fake(text, mp3):
    bounds, t = [], 0.3
    for w in text.split():
        d = 0.07 * len(w) + 0.08
        bounds.append({"t": w, "t0": t, "t1": t + d})
        t += d + (0.35 if w[-1] in ".?!" else 0.05)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                    "-t", f"{t + 0.5:.2f}", "-c:a", "libmp3lame", str(mp3)], check=True)
    return bounds


def main(spec_path):
    spec = json.loads(Path(spec_path).read_text("utf-8"))
    pron = {k.replace("*", "").strip(PUNCT): v.rstrip(PUNCT) for k, v in spec.get("pron", {}).items()}
    outdir = Path(__file__).parent / "out" / spec["id"]
    outdir.mkdir(parents=True, exist_ok=True)

    segs, units = [], []  # units: (seg, tok, norm) por cada palabra hablada
    text_parts = []
    for si, s in enumerate(spec["segmentos"]):
        toks = tokens(s["sub"])
        for ti, t in enumerate(toks):
            if t[1] is None:
                continue
            w = spoken(t[1], pron)
            text_parts.append(w)
            for u in w.split():
                n = norm(u)
                if n:
                    units.append((si, ti, n))
        segs.append(toks)
    text = " ".join(text_parts)

    cache = outdir / "voz_gratis.json"
    mp3 = outdir / "voz.mp3"
    if cache.exists() and mp3.exists() and json.loads(cache.read_text("utf-8")).get("text") == text + VOICE + RATE and not FAKE:
        bounds = json.loads(cache.read_text("utf-8"))["b"]
        print("Voz en caché")
    else:
        bounds = _fake(text, mp3) if FAKE else asyncio.run(_edge(text, mp3))
        if not FAKE:
            cache.write_text(json.dumps({"text": text + VOICE + RATE, "b": bounds}, ensure_ascii=False), "utf-8")
        print(f"Voz generada ({VOICE}{' FAKE' if FAKE else ''}): {len(text)} caracteres")

    # alinear palabras del guion con las del sintetizador (greedy con ventana)
    bn = [norm(b["t"]) for b in bounds]
    j, times = 0, {}
    for k, (si, ti, n) in enumerate(units):
        hit = None
        for d in range(0, 6):
            if j + d < len(bn) and (bn[j + d] == n or (bn[j + d] and (bn[j + d].startswith(n) or n.startswith(bn[j + d])))):
                hit = j + d
                break
        if hit is not None:
            a, b = bounds[hit]["t0"], bounds[hit]["t1"]
            j = hit + 1
        else:
            prev = bounds[j - 1]["t1"] if j > 0 else 0.0
            a = b = prev
        r = times.setdefault((si, ti), [a, b])
        r[1] = max(r[1], b)

    res, last = [], 0.0
    for si, toks in enumerate(segs):
        row = []
        for ti, t in enumerate(toks):
            if (si, ti) in times:
                t0, t1 = times[(si, ti)]
                t0 = max(t0, last) if t0 < last - 0.01 else t0
                t1 = max(t1, t0)
                last = t1
            else:
                t0 = t1 = last
            row.append({"w": t[0], "rojo": t[2], "t0": t0, "t1": t1})
        res.append(row)
    (outdir / "tiempos.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), "utf-8")
    print("Duración voz:", round(bounds[-1]["t1"], 2), "s")


if __name__ == "__main__":
    main(sys.argv[1])
