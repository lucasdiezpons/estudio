#!/usr/bin/env python3
"""
Añade a videos/videos.json los vídeos nuevos de la carpeta videos/.

Uso (desde la carpeta del proyecto):
    python3 tools/actualizar.py              # solo añade los nuevos al json
    python3 tools/actualizar.py --comprimir  # además los comprime (necesita ffmpeg)

Nombre del archivo = título y tema automáticos:
    "OESC - Ley de Ohm.mp4"  ->  tema "OESC", título "Ley de Ohm"
    "ley-de-ohm.mp4"         ->  tema "Sin tema", título "Ley de ohm"
Luego puedes cambiar título, texto y tema a mano en videos/videos.json.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CARPETA = RAIZ / "videos"
JSON = CARPETA / "videos.json"
EXTS = {".mp4", ".mov", ".m4v", ".webm"}
COMPRIMIR = "--comprimir" in sys.argv
FFMPEG = shutil.which("ffmpeg")


def slug(s):
    s = s.lower()
    for a, b in zip("áéíóúüñ", "aeiouun"):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "video"


def comprimir(src: Path) -> Path:
    """Vertical 9:16, ~1-2 MB por cada 25 s. Devuelve el .mp4 final."""
    dst = src.with_name(slug(src.stem) + ".mp4")
    tmp = src.with_name(dst.stem + ".tmp.mp4")
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", str(src),
                    "-vf", "scale='min(720,iw)':-2", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "28", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(tmp)],
                   check=True)
    if src != dst:
        src.unlink()
    tmp.replace(dst)
    return dst


def poster(video: Path) -> str:
    jpg = video.with_suffix(".jpg")
    if not jpg.exists() and FFMPEG:
        subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", "1", "-i", str(video),
                        "-frames:v", "1", "-vf", "scale=288:-2", "-q:v", "5", str(jpg)])
    return jpg.name if jpg.exists() else ""


def main():
    datos = json.loads(JSON.read_text("utf-8")) if JSON.exists() else []
    conocidos = {d["archivo"] for d in datos}
    nuevos = 0
    for f in sorted(CARPETA.iterdir()):
        if f.suffix.lower() not in EXTS or f.name in conocidos or ".tmp." in f.name:
            continue
        nombre = f.stem
        if COMPRIMIR and FFMPEG:
            print("Comprimiendo", f.name, "...")
            f = comprimir(f)
            if f.name in conocidos:
                continue
        tema, titulo = ("Sin tema", nombre)
        if " - " in nombre:
            tema, titulo = [x.strip() for x in nombre.split(" - ", 1)]
        titulo = titulo.replace("-", " ").replace("_", " ").strip()
        datos.append({
            "id": slug(f.stem),
            "archivo": f.name,
            "poster": poster(f),
            "titulo": titulo[:1].upper() + titulo[1:],
            "texto": "",
            "tema": tema,
        })
        nuevos += 1
        print("  +", f.name, "->", tema, "/", titulo)
    # quita del json los vídeos que ya no existen
    antes = len(datos)
    datos = [d for d in datos if (CARPETA / d["archivo"]).exists()]
    JSON.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(f"Listo: {nuevos} nuevos, {antes - len(datos)} quitados, {len(datos)} en total.")
    if not FFMPEG:
        print("(Sin ffmpeg: no se han creado miniaturas ni comprimido nada)")


if __name__ == "__main__":
    main()
