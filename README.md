# 📱 Estudio — TikTok de repaso

> ⚠️ **GitHub: NUNCA con la cuenta de la universidad (UPC).** Usa tu cuenta personal.

## Añadir vídeos
1. Mete los `.mp4` en `videos/` → nombre `TEMA - Título.mp4` (ej. `OESC - Ley de Ohm.mp4`)
2. Ejecuta: `python3 tools/actualizar.py --comprimir`
3. (Opcional) Retoca títulos, texto o tema en `videos/videos.json`
4. Sube los cambios a GitHub

## Publicar en GitHub Pages (una sola vez)
1. Crea un repo nuevo en tu cuenta **personal** (privado si quieres; Pages en privado solo va con GitHub Pro)
2. Sube **todo** el contenido de esta carpeta
3. Settings → Pages → Branch `main` / `root` → Save
4. En 1–2 min: `https://TU-USUARIO.github.io/NOMBRE-REPO/`

## En el iPhone
Safari → abre el link → Compartir → **Añadir a pantalla de inicio**

## Cómo funciona
| | |
|---|---|
| Orden | Primero lo no visto (mezclado) + ~15 % de vistos al azar por en medio |
| Visto | Al ver el 60 % del vídeo (se guarda en el móvil) |
| Filtro tema | Botón "Para ti ▾"; se quita al cerrar la app |
| Lista | 📚 abajo: todos los títulos por tema, con buscador |
| Controles | Tocar = pausa · 🔇/🔊 arriba a la derecha |

## Probar en el ordenador
`python3 -m http.server 8000` → abre `http://localhost:8000`

## Límite
GitHub Pages ≈ 1 GB → con vídeos comprimidos (~1–2 MB) caben unos 500+. Si se llena → pasar al servidor de casa.
