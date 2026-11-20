# 🎬 Fábrica de vídeos de estudio (estilo TikTok)

Pipeline: **guion JSON → voz ElevenLabs (con tiempos por palabra) → render PIL + ffmpeg → app web (GitHub Pages)**.
App: repo `lucasdiezpons/estudio` → `https://lucasdiezpons.github.io/estudio/`.

> ⚠️ GitHub: SIEMPRE la cuenta personal **lucasdiezpons** (gmail). NUNCA la de la UPC.
> ⚠️ La API key de ElevenLabs NUNCA va al repo: `~/.elevenkey` o `ELEVENLABS_API_KEY`.

## 0. Preparar (cada chat nuevo)
1. Repo: añadir `lucasdiezpons/estudio` con permiso de push y clonar (`git clone --depth 1`).
2. `pip install pillow --break-system-packages` (si falta) · `ffmpeg` debe existir.
3. Pedir a Lucas la API key → `printf '%s' 'sk_...' > ~/.elevenkey && chmod 600 ~/.elevenkey`.
4. Red: `api.elevenlabs.io` tiene que estar permitido en claude.ai → Settings → Capabilities (ya lo está).

## 1. Material → agrupar
- Entrada: banco de preguntas tipo test (enunciado, opciones, correcta, por qué).
- Agrupar en **el mínimo de vídeos**: 1 vídeo = 1 idea que responde varias preguntas (3–8).
- Marcar las dudosas y narrarlas con prudencia.

## 2. Guion (spec JSON) — reglas de estilo
- **Curiosidad**: empieza con "¿Sabías que…?". NUNCA mencionar examen, test, preguntas, control, estudiar, "x/8".
- Frases cortas, tono hablado, pausas con `...`, preguntas retóricas.
- 5–8 segmentos, 35–60 s. Último segmento: "Así que ya sabes. …" (tag `en resumen`, título `EN *RESUMEN*`).
- En pantalla, `corriente` → añadir `[(intensidad)]` y `tensión` → `[(voltaje)]` (los `[...]` se ven pero no se dicen).
- `*palabra*` = rojo y cursiva en el subtítulo y en el título.
- Siglas, números y símbolos → `pron` (ej. `"TT": "te te"`, `"55°": "cincuenta y cinco grados"`, `"CC/CV": "corriente constante y tensión constante"`). Las claves van sin puntuación.
- Grados: usar `°` (no `º`).

```json
{
  "id": "asig-tema-corto",            // = nombre del archivo
  "titulo": "Título que sale en la app",
  "texto": "Subtítulo corto en la app",
  "tema": "CESA · Protecciones",      // etiqueta: "ASIGNATURA · Subtema"
  "etiqueta": "protecciones",         // texto pequeño arriba del vídeo
  "pron": {"TT": "te te"},
  "segmentos": [
    {"tag": "la curiosidad", "sub": "¿Sabías que ... *clave* ...?", "titulo": "TT *VS* TN", "num": 1,
     "visual": {"tipo": "alerta", "icono": "🔌", "linea1": "texto", "linea2": "CAJA GRANDE", "stamp": "SELLO"}}
  ]
}
```
Visuales disponibles:
| tipo | campos |
|---|---|
| `alerta` | `icono` (emoji), `linea1`, `linea2` (caja), `stamp` opcional |
| `filas` | `filas: [{icono, izq, der, rojo?, en?}]` (2–3 filas; `en` = palabra EXACTA del subtítulo, con su puntuación, en la que aparece la fila), `stamp` opcional |
| `big` | `big` (número/símbolo corto), `small` |
| `diagrama` | `destino: "tierra" | "neutro"` |

Ejemplos completos: `specs/v11-tt-tn.json` y `specs/generar_specs.py` (13 vídeos de CESA).

## 3. Producir (todo en tanda, sin esperas entre vídeos)
```bash
cd tools/fabrica
python3 tts.py specs/X.json        # voz Dan Dan · eleven_v3 · stability 1.0 (cachea: repetir no gasta)
python3 render.py specs/X.json     # → out/X/X.mp4 + X.jpg (720x1280, ~20 s de render)
```
- Revisar con **una sola hoja de capturas** por tanda (ffmpeg `tile`), no vídeo a vídeo.
- Problemas típicos: subtítulo de 4+ líneas (acortar frase), filas que no salen (`en` mal escrito), emoji que no existe.

## 4. Publicar
```bash
python3 publicar.py specs/X.json --no-push   # copia a videos/ y actualiza videos.json (repetir por vídeo)
git add -A && git commit -m "Añade vídeos de ..." && git -c push.negotiate=true push origin HEAD   # un solo commit
```
`python3 publicar.py specs/X.json` (sin flag) = copia + commit + push de un vídeo.

## Voz
- **Dan Dan** `9F4C8ztpNUmXkdDDbz3J`, modelo `eleven_v3`, `stability: 1.0` (a Lucas le gusta esta; v2 sonaba robótica).
- ≈1 crédito por carácter; un vídeo ≈ 450–850 créditos.
- Plan Creator (promo estudiante): cancelar antes del 19 dic 2026 (recordatorio en su calendario el 17 dic).

## No hacer
- No programar un aviso por vídeo (gasta mucho Claude): hacer la asignatura entera de golpe.
- No generar muchas muestras de voz: ya está elegida.
- No subir la API key ni archivos `out/` al repo.

## Ganchos (opcional)
- `tools/fabrica/guiones/` = `hooks.json` (21 fórmulas de gancho) + `hookscore.py` (puntúa ganchos) del plugin MIT Jakeschincariol/youtube-agent-skill.
- Uso: escribir 5 ganchos por TikTok → `python3 tools/fabrica/guiones/hookscore.py --hook "frase"` → quedarse con el mejor.
- Ojo: está pensado para YouTube en inglés; la puntuación en español es orientativa.
## Grupos en la app
- `app.js` → `GRUPOS` (Control 2 / Tema 1) y `OCULTOS_EN_PARA_TI` (ahora oculta el Tema 1 en "Para ti"; vaciarlo tras el Control 2). Temas nuevos: añadirlos a su grupo.

## Voz gratis (edge-tts)
- `tts_gratis.py` = igual que `tts.py` pero con `es-MX-DaliaNeural` (edge-tts, WordBoundary). `VOZ_FAKE=1` → silencio para probar sin internet.
- El entorno cloud NO llega a `speech.platform.bing.com`: la voz se genera en el PC de Lucas.
- Paquete en el PC: `CESA\3 Vídeos (montaje)\TikToks Control 2 (voz gratis)\HACER_TIKTOKS.bat` (genera los 37 de `specs/gratis/` y, si dice "s", los sube con git).
