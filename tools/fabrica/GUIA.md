# 🎬 Fábrica de vídeos de estudio (estilo TikTok)

Pipeline: **guion JSON → voz (ElevenLabs Dan Dan o gratis edge-tts) con tiempos por palabra → render PIL + schemdraw/matplotlib + ffmpeg → app web (GitHub Pages)**.
App: repo `lucasdiezpons/estudio` → `https://lucasdiezpons.github.io/estudio/`.

> ⚠️ GitHub: SIEMPRE la cuenta personal **lucasdiezpons** (gmail). NUNCA la de la UPC.
> ⚠️ La API key de ElevenLabs NUNCA va al repo: `~/.elevenkey` o `ELEVENLABS_API_KEY`.

## 0. Preparar (cada chat nuevo)
1. Repo: añadir `lucasdiezpons/estudio` con permiso de push y clonar (`git clone --depth 1`).
2. `pip install pillow schemdraw matplotlib numpy --break-system-packages` (si falta) · `ffmpeg` debe existir.
3. Pedir a Lucas la API key → `printf '%s' 'sk_...' > ~/.elevenkey && chmod 600 ~/.elevenkey`.
4. Red: `api.elevenlabs.io` tiene que estar permitido en claude.ai → Settings → Capabilities (ya lo está).

## 1. Material → qué vídeos hacer
- **Fuente principal: los exámenes de otros años** (PC de Lucas: `Descargas/UPC/<ASIG>/2 Exámenes`, `0 Para estudiar`, PA de API…). Primero mira QUÉ preguntan y CÓMO; el vídeo responde a eso.
- Después apuntes/teoría para entender el porqué.
- 1 vídeo = 1 idea que hay que llevarse. Si una idea no cabe en 45 s, son dos vídeos.
- Lo dudoso se marca y se narra con prudencia ("normalmente…"), nunca inventado.

## 2. Guion — escribir con cariño (OBLIGATORIO, vídeo a vídeo)

### 2.1 Elige el formato según el tema (no todos iguales)
| Formato (`"formato"`) | Cuándo | Cómo arranca | Visual que pega |
|---|---|---|---|
| `trampa` | Lo que casi todos fallan | "Mucha gente pone X… y no." | `pregunta`, `calculo` |
| `resuelto` | Ejercicio con números | Enunciado en 1 frase y se resuelve paso a paso | `circuito` + `calculo` |
| `analogia` | Concepto abstracto | "Imagina una tubería / un cubo / un portero…" | `alerta`, `imagen` |
| `vs` | Dos cosas que se confunden | "X y Y parecen iguales. No lo son." | `vs`, `filas` |
| `porque` | Componentes, protecciones, protocolos | El problema primero, el invento después | `alerta`, `circuito` |
| `adivina` | Repaso de memoria | Pregunta → pausa ("…") → respuesta | `pregunta` |
| `formula` | Fórmula clave | Qué es cada letra y qué pasa si la cambias | `big`, `calculo`, `grafica` |
| `regla` | Datos sueltos | "Siempre… / Nunca…" + truco para acordarse | `filas`, `big` |

### 2.2 Pasos para escribirlo (no saltarse ninguno)
1. **La frase clave**: escribe en UNA frase qué tiene que saber Lucas al acabar. Si no sale en una frase, el vídeo no está claro.
2. **Formato**: elige uno de la tabla. Dos vídeos seguidos de la misma tanda NUNCA con el mismo formato, gancho ni cierre.
3. **3 ganchos**: escribe 3 primeras frases distintas y quédate con la que más dan ganas de seguir mirando. Prohibido abrir siempre con "¿Sabías que…?" (como mucho 1 de cada 5 vídeos).
4. **Borrador** entero.
5. **Revisión** — repasa frase a frase:
   - **¿Lo diría una persona?** Léelo en voz alta en tu cabeza: si suena a libro, a apuntes o a robot, reescríbelo como se lo contarías a un amigo en el bar. Nada de "cabe destacar", "es importante", "por lo tanto", "dicho dispositivo".
   - **¿Es fácil?** Palabras de la calle. Un tecnicismo solo si hace falta, y explicado en la misma frase. Si hay forma fácil de decirlo, esa.
   - **¿Sobra?** Si quitas la frase y se entiende igual, fuera.
   - **¿Es concreto?** Al menos un número, un ejemplo o una imagen mental.
   - **¿Hay un "¡ahh, claro!"?** El momento en que encaja. Si no lo hay, falta el porqué.
   - **¿Es correcto?** Comprobado contra apuntes o solución oficial. Nunca inventar datos.
   - **¿Sirve para el examen?** Responde a algo que preguntan (sin decir "examen").
6. **Reescribe** aplicando todo lo anterior. Es normal que cambie la mitad.
7. **Cierre**: una frase que se quede (regla "siempre/nunca", el truco, o la respuesta al gancho). Varía: no siempre "Así que ya sabes".

### 2.3 Reglas de forma (se mantienen)
- NUNCA decir examen, test, preguntas, control, estudiar, "x/8". Sí "mucha gente pone…", "te lo vas a encontrar así…".
- Frases cortas y habladas, pausas con `...`. 4–7 segmentos, 30–55 s.
- En pantalla, `corriente` → `[(intensidad)]` y `tensión` → `[(voltaje)]` (los `[...]` se ven pero no se dicen).
- `*palabra*` = rojo y cursiva en subtítulo y título.
- Siglas, números y símbolos → `pron` (claves sin puntuación). Grados con `°`.
- Títulos de pantalla: 2–3 palabras, que se entiendan sin audio.

```json
{
  "id": "asig-tema-corto",            // = nombre del archivo
  "formato": "trampa",                // de la tabla 2.1
  "titulo": "Título que sale en la app",
  "texto": "Subtítulo corto en la app",
  "tema": "CESA · Protecciones",
  "examen": "Control 2",
  "etiqueta": "protecciones",
  "pron": {"TT": "te te"},
  "segmentos": [
    {"tag": "el reto", "sub": "Frase hablada con *clave*...", "titulo": "TT *VS* TN", "num": 1,
     "visual": {"tipo": "alerta", "icono": "🔌", "linea1": "texto", "linea2": "CAJA GRANDE", "stamp": "SELLO"}}
  ]
}
```

### 2.4 Visuales
| tipo | campos | Para |
|---|---|---|
| `alerta` | `icono`, `linea1`, `linea2`, `stamp?` | idea suelta |
| `filas` | `filas: [{icono, izq, der, rojo?, en?}]`, `stamp?` | 2–3 datos |
| `big` | `big`, `small`, `stamp?` | número o fórmula |
| `diagrama` | `destino: "tierra"/"neutro"` | TT/TN |
| `circuito` | `nombre` (lm317, divisor, zener, puente, buck, boost), `valores: {R1: "240 Ω"…}`, `rojo: [...]`, `pasos: [{en, rojo: [...]}]`, `pie?` | circuito que se va pintando en rojo según lo que se dice |
| `imagen` | `archivo` (PNG en `specs/img/`), `en?`, `pie?` | cualquier dibujo propio (schemdraw / matplotlib / foto de diapositiva recortada) |
| `grafica` | `curvas: [{f: "expr en x", rojo?, label?, discontinua?}]`, `x: [a,b]`, `y?`, `xlabel`, `ylabel`, `puntos: [{x,y,txt}]`, `en?`, `pie?` | curva que se dibuja sola |
| `calculo` | `lineas: [{txt, en?, rojo?}]` (la última sale en rojo grande; `✓`/`✗` al final se ven bien) | cuenta paso a paso |
| `vs` | `izq/der: {icono, titulo, puntos: [..]}`, `ganador?: "izq"/"der"`, `en?`, `stamp?` | X contra Y |
| `pregunta` | `pregunta`, `opciones: [..]`, `correcta` (índice), `en` (palabra en la que se revela) | gancho tipo test / adivina |

- `en` = palabra EXACTA del subtítulo (con su puntuación y asteriscos) en la que aparece/cambia algo.
- Circuito nuevo: añade una función en `circuitos.py` (mira `lm317`) y pruébalo con `python3 circuitos.py nombre R1,R2`.
- Ejemplo completo con casi todo: `specs/ejemplos/demo-lm317-trampa.json`.
- Efectos de sonido suaves (whoosh al cambiar de bloque, pop en sellos, ding al revelar) y barra de progreso: automáticos. Quitar efectos: `"sfx": false` en el spec o `SFX=0`.
- Requisitos extra: `pip install schemdraw matplotlib numpy --break-system-packages`.

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
## Filtro de la app (Asignatura › Examen › Tema)
- Asignatura = lo que va antes de " · " en `tema`; examen = campo `examen` del spec (se copia a videos.json); tema = lo de después de " · ".
- CESA: `examen` = "Control 2" (Normativa, Fotovoltaica, Dimensionado FV, Baterías, Protecciones) o "MQ" (Tema 1).
- Lucas activa/desactiva cada nivel con interruptores; se guarda en el móvil (localStorage "apagados"; por defecto MQ apagado).
- Varias etiquetas: `"examen": ["MQ", "Control 2"]` (mismo tema) o `"rutas": ["CESA/MQ/Conmutados", "CESA/Control 2/Baterías"]` (temas distintos). Sale si CUALQUIER ruta está encendida.
- Spec nuevo: pon SIEMPRE `examen`. Asignatura nueva: `tema` = "ASIG · Tema".

## Voz gratis (edge-tts)
- `tts_gratis.py` = igual que `tts.py` pero con `es-MX-DaliaNeural` (edge-tts, WordBoundary). `VOZ_FAKE=1` → silencio para probar sin internet.
- El entorno cloud NO llega a `speech.platform.bing.com`: la voz se genera en el PC de Lucas.
- Paquete en el PC: `CESA\3 Vídeos (montaje)\TikToks Control 2 (voz gratis)\HACER_TIKTOKS.bat` (genera los 37 de `specs/gratis/` y, si dice "s", los sube con git).
