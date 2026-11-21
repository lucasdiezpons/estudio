#!/usr/bin/env python3
"""Genera la voz (ElevenLabs) + tiempos por palabra para un spec. Cachea para no gastar créditos."""
import base64, json, re, sys, urllib.request
from pathlib import Path

VOICE = "9F4C8ztpNUmXkdDDbz3J"  # Dan Dan
MODEL = "eleven_v3"
import os
def _key():
    if os.environ.get("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"].strip()
    for p in (Path.home() / ".elevenkey", Path("/home/claude/.elevenkey")):
        if p.exists():
            return p.read_text().strip()
    sys.exit("Falta la API key: export ELEVENLABS_API_KEY=... o guárdala en ~/.elevenkey (NUNCA en el repo)")
KEY = _key()
PUNCT = "¿?¡!.,:;"


def tokens(seg_sub):
    """[(display, spoken_or_None, rojo)]"""
    out = []
    for raw in seg_sub.split():
        m = re.fullmatch(r"\[(.*)\]([.,:;!?…]*)", raw)  # [(intensidad)] o [(intensidad)]... → mudo
        mute = bool(m)
        if mute:
            raw = m.group(1) + m.group(2)
            if m.group(2) and out and out[-1][1]:
                out[-1][1] += m.group(2)  # la pausa se la queda la palabra hablada anterior
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


def main(spec_path):
    spec = json.loads(Path(spec_path).read_text("utf-8"))
    pron = {k.replace("*", "").strip(PUNCT): v.rstrip(PUNCT) for k, v in spec.get("pron", {}).items()}
    outdir = Path(__file__).parent / "out" / spec["id"]
    outdir.mkdir(parents=True, exist_ok=True)

    text, spans, segs = "", [], []
    for s in spec["segmentos"]:
        toks = tokens(s["sub"])
        for t in toks:
            if t[1] is None:
                spans.append(None)
                continue
            w = spoken(t[1], pron)
            if text:
                text += " "
            spans.append((len(text), len(text) + len(w)))
            text += w
        segs.append(toks)

    cache = outdir / "voz.json"
    if cache.exists() and json.loads(cache.read_text())["text"] == text and json.loads(cache.read_text()).get("v") == VOICE + MODEL:
        data = json.loads(cache.read_text())
        print("Voz en caché (0 créditos)")
    else:
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
            data=json.dumps({"text": text, "model_id": MODEL, "language_code": "es",
                             "voice_settings": {"stability": 1.0, "similarity_boost": 0.8}}).encode(),
            headers={"xi-api-key": KEY, "Content-Type": "application/json"})
        r = json.loads(urllib.request.urlopen(req, timeout=120).read())
        data = {"text": text, "v": VOICE + MODEL, "audio": r["audio_base64"], "al": r["alignment"]}
        cache.write_text(json.dumps(data))
        print(f"Voz generada: {len(text)} caracteres")
    (outdir / "voz.mp3").write_bytes(base64.b64decode(data["audio"]))
    st, en = data["al"]["character_start_times_seconds"], data["al"]["character_end_times_seconds"]

    # tiempos por token
    k, last = 0, 0.0
    res = []
    for toks in segs:
        row = []
        for t in toks:
            sp = spans[k]; k += 1
            if sp is None:
                row.append({"w": t[0], "rojo": t[2], "t0": last, "t1": last})
            else:
                a, b = sp
                t0, t1 = st[a], en[b - 1]
                last = t1
                row.append({"w": t[0], "rojo": t[2], "t0": t0, "t1": t1})
        res.append(row)
    (outdir / "tiempos.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print("Duración voz:", round(en[-1], 2), "s")


if __name__ == "__main__":
    main(sys.argv[1])
