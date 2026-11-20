#!/usr/bin/env python3
"""Copia el vídeo de un spec al repo, actualiza videos.json, commit y push."""
import json, shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
spec = json.loads(Path(sys.argv[1]).read_text("utf-8"))
out = Path(__file__).parent / "out" / spec["id"]
vid = REPO / "videos"
for ext in ("mp4", "jpg"):
    shutil.copy(out / f"{spec['id']}.{ext}", vid / f"{spec['id']}.{ext}")
js = vid / "videos.json"
data = [d for d in json.loads(js.read_text("utf-8")) if d["id"] != spec["id"]]
data.append({"id": spec["id"], "archivo": spec["id"] + ".mp4", "poster": spec["id"] + ".jpg",
             "titulo": spec["titulo"], "texto": spec.get("texto", ""), "tema": spec["tema"], "examen": spec.get("examen", "")})
js.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")
g = lambda *a: subprocess.run(["git", "-C", str(REPO), *a], check=True)
g("add", "videos")
if "--no-push" in sys.argv:
    print("Copiado (sin commit)"); sys.exit()
g("-c", "user.name=lucasdiezpons", "-c", "user.email=lucasdiezpons@gmail.com", "commit", "-q", "-m",
  f"Añade vídeo: {spec['titulo']}\n\nCo-Authored-By: Claude <noreply@anthropic.com>")
g("-c", "push.negotiate=true", "push", "-q", "origin", "HEAD")
print("Publicado:", spec["id"], "· total vídeos:", len(data))
