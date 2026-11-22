#!/usr/bin/env python3
"""Voz gratis (edge-tts Dalia) + render + publicar para specs/gratis/<prefijo>*.json.
Uso (en el PC, con internet): python hacer_gratis.py api-g-   [--push]"""
import subprocess, sys, json
from pathlib import Path
H = Path(__file__).parent
pref = sys.argv[1] if len(sys.argv) > 1 else "api-g-"
vids = json.loads((H.parents[1] / "videos" / "videos.json").read_text("utf-8"))
hechos = {d["id"] for d in vids}
py = sys.executable
for f in sorted((H / "specs" / "gratis").glob(pref + "*.json")):
    sid = f.stem
    if sid in hechos and "--rehacer" not in sys.argv:
        print("ya publicado:", sid); continue
    print("==", sid)
    for cmd in (["tts_gratis.py"], ["render.py"], ["publicar.py", "--no-push"]):
        subprocess.run([py, cmd[0], str(f), *cmd[1:]], cwd=H, check=True)
if "--push" in sys.argv:
    g = lambda *a: subprocess.run(["git", "-C", str(H.parents[1]), *a], check=True)
    g("-c", "user.name=lucasdiezpons", "-c", "user.email=lucasdiezpons@gmail.com", "commit", "-q", "-m", f"TikToks voz gratis: {pref}*")
    g("pull", "--rebase"); g("-c", "push.negotiate=true", "push", "origin", "HEAD")
    print("Publicado")
