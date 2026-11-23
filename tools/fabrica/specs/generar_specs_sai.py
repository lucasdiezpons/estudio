#!/usr/bin/env python3
"""TikToks de SAI (Unit 4 · Codecs). Genera specs/sai-*.json + lint.
Cada vídeo sigue GUIA §2: frase clave -> 3 ganchos -> borrador -> revisión -> reescritura -> cierre.
Los textos de aquí ya son la versión reescrita (la revisión está resumida en "_guion")."""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
EXAMEN = "Unit 4 Codecs"

PRON = {
    "ADPCM": "a de pe ce eme", "MP3": "eme pe tres", "MP2": "eme pe dos", "MPEG": "empeg", "JPEG": "jota peg",
    "MJPEG": "eme jota peg", "DCT": "de ce te", "GoP": "gop", "RTP": "erre te pe", "VAD": "uve a de",
    "PCM": "pe ce eme", "G.726": "ge setecientos veintiséis", "H.261": "hache doscientos sesenta y uno",
    "ITU-R": "i te u erre", "EoB": "e o be", "N": "ene", "M": "eme", "P": "pe", "B": "be", "I": "i",
    "A": "a", "C": "ce", "D": "de", "DC": "de ce", "GIF": "guif", "CPU": "ce pe u", "lookahead": "lukajed",
    "ms": "milisegundos", "CBR": "ce be erre", "RGB": "erre ge be", "UDP": "u de pe", "IP": "i pe",
    "Cb": "ce be", "Cr": "ce erre", "G.723.1": "ge setecientos veintitrés punto uno",
}

# ---------- helpers de visuales ----------
def alerta(icono, l1, l2, stamp=None):
    v = {"tipo": "alerta", "icono": icono, "linea1": l1, "linea2": l2}
    if stamp: v["stamp"] = stamp
    return v

def calculo(*lineas, **kw):
    out = []
    for l in lineas:
        out.append({"txt": l[0], "en": l[1]} if isinstance(l, tuple) else {"txt": l})
    return {"tipo": "calculo", "lineas": out, **kw}

def big(b, s, stamp=None):
    v = {"tipo": "big", "big": b, "small": s}
    if stamp: v["stamp"] = stamp
    return v

def img(archivo, en=None, pie=None):
    v = {"tipo": "imagen", "archivo": "img/" + archivo}
    if en: v["en"] = en
    if pie: v["pie"] = pie
    return v

def pregunta(p, ops, ok, en=None):
    v = {"tipo": "pregunta", "pregunta": p, "opciones": ops, "correcta": ok}
    if en: v["en"] = en
    return v

def vs(izq, der, ganador=None, en=None, stamp=None):
    v = {"tipo": "vs", "izq": izq, "der": der}
    if ganador: v["ganador"] = ganador
    if en: v["en"] = en
    if stamp: v["stamp"] = stamp
    return v

def filas(*rows, stamp=None):
    return {"tipo": "filas", "filas": [dict(zip(("icono", "izq", "der", "en"), r)) if len(r) == 4 else dict(zip(("icono", "izq", "der"), r)) for r in rows]}

def S(tag, sub, titulo, visual):
    return {"tag": tag, "sub": sub, "titulo": titulo, "visual": visual}

V = []  # lista de vídeos
def video(id, formato, titulo, texto, tema, etiqueta, frase, ganchos, elegido, segs):
    V.append({"id": id, "formato": formato, "titulo": titulo, "texto": texto, "tema": "SAI · " + tema,
              "examen": EXAMEN, "etiqueta": etiqueta, "pron": PRON,
              "_guion": {"frase_clave": frase, "ganchos": ganchos, "elegido": elegido},
              "segmentos": segs})

# =====================================================================  AUDIO
video("sai-adpcm-forward-backward", "vs", "Forward vs backward", "Quién calcula los coeficientes",
      "ADPCM y silencios", "adpcm",
      "En forward los coeficientes viajan con los datos (más bits); en backward los calculan los dos lados (nada extra): por eso casi todos son backward.",
      ["Misma voz, mismo ADPCM... y una versión sale 12,8 kbit/s más cara.", "¿Quién calcula los coeficientes, el que manda o el que recibe?", "Forward y backward parecen lo mismo. No lo son."], 1, [
    S("el reto", "Misma voz, mismo *ADPCM*... y una versión sale *doce coma ocho* kilobits por segundo más cara.", "¿QUIÉN *CALCULA*?",
      alerta("🧮", "ADPCM: ¿quién saca los coeficientes?", "+12,8 kbit/s")),
    S("forward", "En *forward* los calcula el que manda... y tiene que *enviárselos* al otro lado, junto con los datos.", "FORWARD *ENVÍA*",
      alerta("📤", "Viajan diferencias + coeficientes", "DOS COSAS")),
    S("backward", "En *backward* los dos ven las mismas diferencias, así que los calculan *solos*. No hay nada que contar.", "BACKWARD: *CERO*",
      alerta("🔁", "Emisor y receptor calculan lo mismo", "CERO EXTRA")),
    S("la cuenta", "Ocho coeficientes de treinta y dos bits, cada veinte milisegundos... son *doce coma ocho* kilobits de más.", "LA *CUENTA*",
      calculo(("8 coef. × 32 bits", "Ocho"), ("÷ 20 ms", "veinte"), ("= 12,8 kbit/s", "doce"))),
    S("el total", "Por eso casi todos usan *backward*: veinticuatro kilobits contra treinta y seis coma ocho.", "SE LLEVA *BACKWARD*",
      vs({"icono": "📤", "titulo": "Forward", "puntos": ["36,8 kbit/s", "manda coeficientes"]},
         {"icono": "🔁", "titulo": "Backward", "puntos": ["24 kbit/s", "calcula cada lado"]}, "der", "backward:")),
    S("para recordar", "Regla: si el otro lado lo puede *adivinar*... no se lo mandes.", "NO LO *MANDES*",
      alerta("🤫", "Si los dos lo pueden calcular", "NO SE ENVÍA")),
])

video("sai-adpcm-bitrate", "formula", "Bits por muestra", "Caudal de un ADPCM", "ADPCM y silencios", "adpcm",
      "Caudal = muestras por segundo × bits por muestra (ADPCM-32 a 8 kHz = 4 bits por muestra).",
      ["ADPCM de 32 kbit/s: ¿cuántos bits por muestra? Diez segundos.", "Una multiplicación y sabes el caudal de cualquier códec.", "Treinta y dos kilobits... ¿cuántos bits tiene cada muestra?"], 1, [
    S("el reto", "ADPCM de treinta y dos kilobits por segundo. ¿Cuántos bits ocupa *cada muestra*?", "¿BITS POR *MUESTRA*?",
      pregunta("ADPCM-32 a 8 kHz → bits por muestra", ["2 bits", "4 bits", "8 bits"], 1)),
    S("la fórmula", "Es una multiplicación: muestras por segundo, por bits por muestra, igual a *kilobits* por segundo.", "LA *FÓRMULA*",
      big("fs × bits", "muestras/s × bits/muestra = bit/s")),
    S("aplicar", "Ocho mil muestras por segundo... y treinta y dos mil entre ocho mil son *cuatro* bits.", "SON *4 BITS*",
      calculo(("32 000 ÷ 8 000", "Ocho"), ("= 4 bits/muestra", "cuatro"))),
    S("la familia", "Y en G.726 van de dos a cinco bits: *dieciséis*, veinticuatro, treinta y dos o cuarenta kilobits.", "DE 2 A *5 BITS*",
      calculo("2 bits → 16 kbit/s", "3 bits → 24 kbit/s", "4 bits → 32 kbit/s", "5 bits → 40 kbit/s")),
    S("el PCM", "El PCM del teléfono son ocho bits: sesenta y cuatro kilobits. El ADPCM de treinta y dos va a la *mitad*.", "LA *MITAD*",
      vs({"icono": "☎️", "titulo": "PCM", "puntos": ["8 bits/muestra", "64 kbit/s"]},
         {"icono": "🗜️", "titulo": "ADPCM-32", "puntos": ["4 bits/muestra", "32 kbit/s"]}, "der", "mitad.")),
    S("para recordar", "Acuérdate: bits por muestra, por ocho mil, y *listo*.", "× *8000* Y YA",
      big("× 8000", "bits/muestra × 8000 = bit/s (voz)")),
])

video("sai-vad-ruido", "resuelto", "VAD y ruido", "Callar cuando no hablas", "ADPCM y silencios", "vad",
      "Con VAD solo mandas cuando hablas (24 × 0,4 = 9,6 kbit/s) y el ruido de confort añade 0,24: total 9,84 kbit/s.",
      ["Hablas menos de la mitad del tiempo... ¿y pagas la llamada entera?", "Una llamada sin hablar no debería costar nada. ¿O sí?", "Solo hablas el cuarenta por ciento. Haz la cuenta."], 2, [
    S("el reto", "Solo hablas el *cuarenta* por ciento de la llamada. El resto es silencio... ¿y se manda igual?", "¿Y EL *SILENCIO*?",
      alerta("🤫", "ADPCM 24 kbit/s · hablas el 40 %", "¿SE MANDA TODO?")),
    S("sin VAD", "Sin detector se manda todo: ocho mil por tres bits... *veinticuatro* kilobits, hables o no.", "SIN VAD: *24 k*",
      calculo("8000 × 3 bits", "= 24 kbit/s")),
    S("con VAD", "Con el detector solo mandas cuando hablas: veinticuatro por cero coma cuatro son *nueve coma seis*.", "CON VAD: *9,6 k*",
      calculo("24 × 0,4", "= 9,6 kbit/s")),
    S("el problema", "Pero un silencio total suena raro, como si se cortara. Así que se manda un *ruidito* de fondo.", "RUIDO DE *CONFORT*",
      alerta("📞", "Silencio total = parece cortada", "RUIDO DE CONFORT")),
    S("la cuenta", "Un byte cada veinte milisegundos, solo el sesenta por ciento del tiempo: *cero coma veinticuatro* kilobits.", "SOLO *0,24 k*",
      calculo("0,6 × 8 bits ÷ 20 ms", "= 0,24 kbit/s")),
    S("el total", "Total: nueve coma ocho cuatro kilobits. Menos de la *mitad*. Si no hablas, casi no pagas.", "TOTAL *9,84 k*",
      calculo("9,6 + 0,24", "= 9,84 kbit/s")),
])

video("sai-retardo-voip", "trampa", "Retardo en VoIP", "G.723.1 llega tarde", "Voz sobre IP", "voip",
      "El retardo de G.723.1 no es 37,5 ms: sumando CPU, buffer y red son 120-170 ms y con el límite de 150 ms pierdes el 40 %.",
      ["Mucha gente dice que el retardo del códec es 37,5 ms. Y no.", "Ciento cinco milisegundos... y aún no has contado la red.", "¿Se oye bien una llamada que tarda 170?"], 0, [
    S("la trampa", "Mucha gente suma solo la trama y el *lookahead*: treinta y siete coma cinco milisegundos. Y no es todo.", "NO ES *37,5*",
      calculo("30 ms de trama", "+ 7,5 ms de lookahead", "= 37,5 ms ✗")),
    S("lo que falta", "Falta la CPU: diecisiete coma cinco para comprimir, cinco para *descomprimir*. Y cuarenta y cinco de buffer.", "FALTA *EL RESTO*",
      calculo("+ 17,5 ms comprimir", "+ 5 ms descomprimir", "+ 45 ms de buffer")),
    S("el fijo", "Todo eso son *ciento cinco* milisegundos fijos... y todavía no has contado la red.", "SON *105 ms*",
      big("105 ms", "fijos, sin contar la red")),
    S("con la red", "La red añade entre quince y sesenta y cinco. Total: entre *ciento veinte* y ciento setenta milisegundos.", "120 A *170 ms*",
      calculo("105 + (15 a 65)", "= 120 … 170 ms")),
    S("el límite", "Para hablar de tú a tú, el límite son *ciento cincuenta*. Lo que pase de ahí llega tarde: el cuarenta por ciento.", "PIERDES *40 %*",
      calculo("170 − 150 = 20 ms de más", "20 ÷ 50 ms de margen", "= 40 % tarde ✗")),
    S("arreglo", "Arreglo: un códec con trama más corta, o menos buffer... aunque con menos buffer el audio se *corta* más.", "CÓDEC MÁS *CORTO*",
      alerta("✂️", "Trama corta o menos buffer", "SUMA TODO")),
])

video("sai-eficiencia-rtp", "formula", "Voz vs cabeceras", "Eficiencia de una llamada IP", "Voz sobre IP", "voip",
      "Eficiencia = bytes de voz / (voz + 40 de cabeceras): con G.723.1 solo 37,5 %; más tramas por paquete suben la eficiencia pero también el retardo.",
      ["De cada paquete, más de la mitad no es voz.", "En una llamada IP, la voz ocupa menos que las cabeceras.", "¿Cuánto de tu llamada es voz y cuánto es sobre?"], 1, [
    S("el gancho", "En una llamada por IP, la voz ocupa *menos* que las cabeceras. Veinticuatro bytes de voz... contra cuarenta.", "VOZ < *CABECERAS*",
      vs({"icono": "🎙️", "titulo": "Voz", "puntos": ["24 bytes"]}, {"icono": "📦", "titulo": "Cabeceras", "puntos": ["40 bytes"]}, "der", "menos")),
    S("cabeceras", "Cabeceras: IP veinte, UDP ocho, RTP doce. Son *cuarenta* bytes en todos los paquetes.", "20 + 8 + *12*",
      calculo("IP 20 + UDP 8 + RTP 12", "= 40 bytes")),
    S("la voz", "Y la voz: seis coma tres kilobits durante treinta milisegundos son ciento ochenta y nueve bits... *veinticuatro* bytes.", "24 BYTES DE *VOZ*",
      calculo("6,3 kbit/s × 30 ms", "= 189 bits ≈ 24 bytes")),
    S("eficiencia", "Eficiencia: lo útil entre lo que mandas. Veinticuatro entre sesenta y cuatro: *treinta y siete coma cinco* por ciento.", "EFICIENCIA *37,5 %*",
      calculo("24 ÷ (24 + 40)", "= 37,5 %")),
    S("aún peor", "Con la versión de cinco coma tres son veinte bytes: aún peor, *treinta y tres* por ciento.", "AÚN *PEOR*",
      calculo("20 ÷ 60 = 33,3 %", "60 B × 8 ÷ 30 ms", "= 16 kbit/s en la red")),
    S("el peaje", "Mete dos tramas por paquete: sube la eficiencia, pero pagas *treinta* milisegundos más. Siempre hay peaje.", "TRAMAS *EXTRA*",
      alerta("⚖️", "2 tramas: 10,6 kbit/s", "+30 ms DE RETARDO")),
])

video("sai-enmascaramiento", "analogia", "Sonidos tapados", "Lo que el MP3 se ahorra", "Audio perceptual", "mp3",
      "Un tono fuerte tapa a los vecinos en frecuencia (y un poco en el tiempo); lo tapado no se codifica y el MP3 ahorra bits.",
      ["Intenta oír un susurro pegado a un taladro: el MP3 se aprovecha.", "El MP3 tira sonidos que existen pero tú no oyes.", "Hay sonidos que están... y tu oído no recibe."], 0, [
    S("el gancho", "Intenta oír un susurro pegado a un taladro. No puedes... y el *MP3* se aprovecha de eso.", "TAPAR *SONIDOS*",
      alerta("🔊", "Taladro + susurro", "NO SE OYE EL SUSURRO")),
    S("el nombre", "A eso se le llama enmascaramiento: un tono *fuerte* tapa a los que tiene cerca en frecuencia.", "TONO *FUERTE*",
      img("sai-enmascara.png", "tapa")),
    S("la gráfica", "En la gráfica, el tono de sesenta decibelios levanta una zona... y lo que queda debajo *no se oye*.", "LA ZONA *ROJA*",
      img("sai-enmascara.png", "oye.", "debajo de lo rojo: no se oye")),
    S("el tiempo", "Y también funciona en el *tiempo*: tras un sonido fuerte te quedas sordo unos milisegundos.", "TAMBIÉN EN *TIEMPO*",
      alerta("⏱️", "Tras un tono fuerte", "UNOS ms SIN OÍR")),
    S("los bits", "En el ejemplo de clase pasas de siete bits a *tres*: los cuatro de abajo quedaban bajo la máscara.", "MENOS *BITS*",
      calculo("PCM: 7 bits (42 dB)", "4 bits bajo la máscara: fuera", "Se quedan: 3 bits ✓")),
    S("para recordar", "Regla: lo que queda bajo la zona tapada, *se tira*. Por eso el MP3 comprime tanto sin que lo notes.", "SE *TIRA*",
      alerta("✂️", "Bajo la máscara", "NO SE CODIFICA")),
])

video("sai-mp3-trama", "resuelto", "Trama de MP3", "417,95 bytes", "Audio perceptual", "mp3",
      "Una trama MP3 son 1152 muestras = 26,12 ms; a 128 kbit/s mide 417,95 bytes: el 95 % miden 418 (con padding) y el resto 417.",
      ["Una trama de MP3 mide 417,95 bytes. ¿Y el decimal?", "¿Cuántos bytes tiene una trama de MP3? Hay truco.", "El MP3 tiene bytes con decimales. ¿Cómo se manda medio byte?"], 0, [
    S("el gancho", "Una trama de MP3 mide cuatrocientos diecisiete coma noventa y cinco bytes... ¿y el *decimal*?", "¿MEDIO *BYTE*?",
      big("417,95 B", "una trama MP3 a 128 kbit/s")),
    S("el tiempo", "Una trama son mil ciento cincuenta y dos muestras. A cuarenta y cuatro mil cien por segundo: *veintiséis coma doce* ms.", "26,12 *ms*",
      calculo("1152 ÷ 44 100", "= 26,12 ms")),
    S("los bytes", "Los bytes: ciento veintiocho kilobits en ese tiempo... *cuatrocientos diecisiete coma noventa y cinco*.", "LOS *BYTES*",
      calculo("128 kbit/s × 26,12 ms", "÷ 8 bits", "= 417,95 bytes")),
    S("el reparto", "Sin decimales: el noventa y cinco por ciento miden *cuatrocientos dieciocho* y el resto, diecisiete.", "418 O *417*",
      vs({"icono": "📏", "titulo": "418 bytes", "puntos": ["95 % de tramas", "con padding"]},
         {"icono": "📐", "titulo": "417 bytes", "puntos": ["5 % de tramas", "sin padding"]}, "izq", "dieciocho")),
    S("el padding", "El *padding* es un byte extra, y un bit de la cabecera avisa de cuándo lo hay.", "BIT DE *PADDING*",
      alerta("🧩", "En la cabecera (1 bit)", "1 = BYTE EXTRA")),
    S("para recordar", "Acuérdate: mil ciento cincuenta y dos muestras por trama en MP2 y MP3. *Siempre*. Lo demás sale de dividir.", "1152 *SIEMPRE*",
      big("1152", "muestras por trama · MP2 y MP3")),
])

video("sai-mp3-reloj-rtp", "adivina", "Reloj del MP3", "La excepción de RTP", "Audio perceptual", "mp3",
      "En RTP el audio MPEG usa reloj de 90 kHz (no su frecuencia de muestreo): 1 trama = 2351 ticks, 2 tramas = 4702.",
      ["¿Qué reloj usa el MP3 en RTP?", "El audio normal usa su frecuencia de muestreo. El MP3, no.", "Noventa mil: el número que más se olvida."], 0, [
    S("el reto", "En RTP el reloj suele ser la frecuencia de muestreo: ocho mil para voz. ¿Y en *MP3*? ¿Cuál será?", "¿QUÉ *RELOJ*?",
      pregunta("Reloj RTP del audio MPEG", ["44 100 Hz", "48 000 Hz", "90 000 Hz"], 2)),
    S("la excepción", "Pues ninguno de esos: el audio MPEG usa *noventa mil* hercios. Es la gran excepción.", "EXCEPCIÓN: *90 kHz*",
      big("90 kHz", "reloj RTP del audio MPEG", "SIEMPRE")),
    S("una trama", "Una trama dura veintiséis coma doce milisegundos. Por noventa mil... son *dos mil trescientos cincuenta y uno* ticks.", "TICKS POR *TRAMA*",
      calculo("0,02612 s × 90 000", "= 2351 ticks")),
    S("dos tramas", "Si el paquete lleva dos tramas, el timestamp salta *cuatro mil setecientos dos*. Luego nueve mil cuatrocientos cuatro.", "SALTA *4702*",
      calculo("2 × 2351", "= 4702 ticks", "0 → 4702 → 9404")),
    S("al revés", "Y al revés: un salto de veintiún mil ciento cincuenta y nueve ticks son *nueve tramas* en un paquete.", "SALTO = *TRAMAS*",
      calculo("21 159 ÷ 2351", "= 9 tramas")),
    S("para recordar", "Regla: audio normal, reloj igual al muestreo. Audio *MPEG*, noventa mil, siempre.", "MPEG = *90 000*",
      alerta("⏰", "Audio MPEG en RTP", "RELOJ 90 kHz")),
])

# =====================================================================  IMAGEN
video("sai-jpeg-simbolos", "regla", "Leer símbolos", "(ceros, tamaño)(valor)", "JPEG", "jpeg",
      "En un símbolo AC (r,s)(v): r son ceros que te saltas, s el tamaño y v el valor. El DC va solo y EoB cierra el bloque.",
      ["El primer número de (3,4) no es un coeficiente: son ceros.", "Los ceros no se escriben: se cuentan.", "Cuando JPEG escribe 3,4, está contando ceros."], 2, [
    S("el gancho", "En JPEG, un símbolo como tres coma cuatro, menos diez, no es tres, cuatro. Son *tres ceros* y luego menos diez.", "(3,4)(−10)",
      calculo("(3, 4)(−10)", "3 ceros, luego −10")),
    S("el tamaño", "El primer número son los *ceros* de delante. El segundo es el tamaño: cuántos bits hacen falta para ese valor.", "(CEROS, *TAMAÑO*)",
      calculo("(ceros, tamaño)(valor)", "−10 está entre 8 y 15", "→ tamaño 4")),
    S("el DC", "El primero de todos, el DC, va solo: ese seis es el tamaño del valor *cincuenta*.", "EL DC *VA SOLO*",
      alerta("🎯", "(6)(+50)", "DC: SIN CEROS")),
    S("el orden", "Los huecos se cuentan en *zig-zag*: uno a la derecha, luego en diagonal... hasta cubrir las sesenta y cuatro casillas.", "ORDEN *ZIG-ZAG*",
      img("sai-zigzag-orden.png", "zig-zag:")),
    S("el final", "Y cuando ya no queda nada, ponen *EoB*: fin de bloque. Todo lo que falta son ceros.", "EOB = *FIN*",
      alerta("🏁", "End of Block", "EL RESTO, CEROS")),
    S("para recordar", "Regla: en los AC la primera cifra *nunca* es un coeficiente. Siempre son ceros que te saltas.", "1.ª CIFRA = *CEROS*",
      alerta("🔑", "(r, s)(v): r = ceros", "SALTA r HUECOS")),
])

video("sai-jpeg-que-imagen", "resuelto", "¿Qué imagen es?", "Fila o columna", "JPEG", "jpeg",
      "Pon cada coeficiente en su casilla del zig-zag: todos en la columna de la izquierda = solo frecuencias verticales; en la fila de arriba = horizontales.",
      ["Te dan símbolos de JPEG y piden la imagen: solo mira dónde caen los ceros.", "Los ceros delatan la imagen.", "Cincuenta, veinte, menos diez, siete: ¿qué imagen es?"], 0, [
    S("el enunciado", "Te dan estos símbolos y piden la imagen. Mira solo dónde caen los *ceros*.", "¿QUÉ *IMAGEN*?",
      calculo("(6)(+50) (1,5)(+20)", "(0,4)(−10) (5,3)(+7) EoB")),
    S("casilla dos", "Un cero antes del veinte: el cero ocupa la casilla uno y el veinte la *dos*.", "EL 20: *CASILLA 2*",
      img("sai-zigzag-orden.png", "dos.")),
    S("casilla nueve", "El menos diez, sin ceros, es la casilla tres. Cinco ceros después, y el siete cae en la *nueve*.", "EL 7: *CASILLA 9*",
      img("sai-zigzag-orden.png", "nueve.")),
    S("conclusión", "Casillas dos, tres, nueve... todas están en la *columna* de la izquierda.", "TODO EN *COLUMNA*",
      img("sai-zz-columna.png", "columna")),
    S("la imagen", "Una columna son frecuencias *verticales*: la imagen solo cambia de arriba a abajo.", "SOLO *VERTICAL*",
      alerta("↕️", "Columna de la izquierda", "FRECUENCIAS VERTICALES")),
    S("para recordar", "Y si fuera la fila de arriba, serían horizontales. Regla: *fila* igual horizontal, *columna* igual vertical.", "FILA O *COLUMNA*",
      img("sai-zz-fila.png", "fila", "fila = horizontal · columna = vertical")),
])

video("sai-jpeg-mascara", "porque", "Dividir y redondear", "Aquí pierde JPEG", "JPEG", "jpeg",
      "JPEG pierde calidad al dividir cada coeficiente por la tabla y redondear: lo pequeño se vuelve cero.",
      ["La parte donde JPEG te roba calidad es una simple división.", "La DCT no pierde nada: la pérdida es una división.", "¿Dónde se pierde la calidad? En una cuenta de primaria."], 0, [
    S("el gancho", "Aquí es donde JPEG te roba calidad... y es solo una *división*.", "UNA *DIVISIÓN*",
      alerta("➗", "Cada coeficiente ÷ tabla", "Y SE REDONDEA")),
    S("ejemplo uno", "Coeficiente dieciocho coma dos, la tabla dice once. Dieciocho entre once, uno coma seis: redondeas a *dos*.", "18,2 ÷ 11 = *2*",
      calculo("18,2 ÷ 11 = 1,65", "redondeo → 2")),
    S("ejemplo dos", "Menos doce entre diez, menos uno coma dos... *menos uno*.", "−12 ÷ 10 = *−1*",
      calculo("−12 ÷ 10 = −1,2", "redondeo → −1")),
    S("lo pequeño", "Pero cinco coma tres entre dieciséis: cero coma treinta y tres. Redondeas y se vuelve *cero*.", "SE VUELVE *CERO*",
      calculo("5,3 ÷ 16 = 0,33", "redondeo → 0 ✗")),
    S("las altas", "Y la tabla tiene números *grandes* hacia las altas frecuencias, así que ahí desaparece casi todo.", "ALTAS: *PIERDEN*",
      alerta("📉", "Tabla más grande abajo a la derecha", "ALTAS → CEROS")),
    S("para recordar", "Regla: dividir y redondear. Lo pequeño se va a *cero*, y los ceros salen casi gratis.", "DIVIDE Y *REDONDEA*",
      alerta("🎯", "Cuantizar = dividir + redondear", "CEROS GRATIS")),
])

video("sai-jpeg-trampa-dct", "trampa", "La DCT no pierde", "Dónde se pierde la calidad", "JPEG", "jpeg",
      "La DCT es reversible y no pierde nada; la pérdida está en la máscara y da dos efectos: borrosidad y bloques de 8×8.",
      ["Mucha gente dice que la DCT comprime la imagen. Y no.", "¿Dónde pierde JPEG la calidad? No donde crees.", "La DCT se puede deshacer entera. ¿De dónde sale el borrón?"], 0, [
    S("la trampa", "Mucha gente dice que la *DCT* comprime la imagen. Y no: la DCT por sí sola no pierde *nada*.", "LA DCT *NO PIERDE*",
      pregunta("¿Dónde pierde JPEG la calidad?", ["En la DCT", "Al dividir por la tabla", "En el Huffman"], 1, "nada.")),
    S("reversible", "Se puede deshacer entera: con la DCT inversa recuperas el bloque *idéntico*. Es solo un cambio de idioma.", "SE PUEDE *DESHACER*",
      alerta("🔄", "DCT inversa → mismo bloque", "REVERSIBLE")),
    S("la pérdida", "La pérdida está en la máscara, al redondear. Y de ahí salen *dos* efectos.", "DOS *EFECTOS*",
      alerta("🔍", "Pérdida = máscara", "DOS EFECTOS")),
    S("efecto uno", "Uno: *borrosidad*. Al tirar las frecuencias altas, los bordes finos se suavizan.", "EFECTO 1: *BORROSO*",
      alerta("🌫️", "Se pierden frecuencias altas", "IMAGEN BLANDA")),
    S("efecto dos", "Dos: *bloques*. Cada trozo de ocho por ocho va por su cuenta, y entre vecinos se nota el salto.", "EFECTO 2: *BLOQUES*",
      alerta("🧱", "Cada bloque 8×8 va por libre", "CUADRÍCULA VISIBLE")),
    S("la medida", "Por eso un defecto de dieciséis por dieciséis píxeles son *cuatro bloques*: dos por dos. Siempre múltiplos de ocho.", "MÚLTIPLOS DE *8*",
      calculo("16 ÷ 8 = 2", "2 × 2 = 4 bloques")),
])

video("sai-jpeg-bits-pixel", "formula", "Bits por píxel", "Cuánta calidad es esto", "JPEG", "jpeg",
      "Bits por píxel = bits del archivo / píxeles: 0,15 reconocible, 0,25 útil, 0,75 excelente, 1,5 indistinguible; factor = 8 / bpp.",
      ["Treinta y un bits para sesenta y cuatro píxeles: ¿buena o mala calidad?", "Un número resume la calidad de un JPEG.", "Medio bit por píxel: ¿se ve bien?"], 0, [
    S("el reto", "Un bloque de sesenta y cuatro píxeles se queda en treinta y un bits. ¿Calidad *buena* o mala?", "¿BUENA O *MALA*?",
      alerta("🧮", "Bloque 8×8 → 31 bits", "¿QUÉ CALIDAD?")),
    S("la medida", "Se mide en bits por píxel: los bits que ocupa entre los píxeles que *representa*.", "BITS POR *PÍXEL*",
      big("b/p", "bits del archivo ÷ píxeles")),
    S("la cuenta", "Treinta y uno entre sesenta y cuatro son casi *medio* bit por píxel.", "0,5 *BIT/PÍXEL*",
      calculo("31 ÷ 64", "≈ 0,5 bits/píxel")),
    S("la escala", "Cero coma quince: se reconoce. Cero coma veinticinco: útil. Cero coma setenta y cinco: *excelente*.", "¿Y ESO *QUÉ ES*?",
      filas(("👀", "0,15 bits/píxel", "Reconocible", "reconoce."), ("👍", "0,25 bits/píxel", "Útil", "útil."), ("⭐", "0,75 bits/píxel", "Excelente", "excelente."))),
    S("compresión", "Así que medio bit está entre útil y excelente. Y de ocho bits a medio, comprimes *dieciséis* veces.", "COMPRIMES *×16*",
      calculo("8 bits ÷ 0,5", "= ×16")),
    S("para recordar", "Uno coma cinco bits por píxel ya no se distingue del original. Más que eso, *tiras* bits.", "1,5 = *IGUAL*",
      big("1,5", "bits/píxel: indistinguible del original")),
])

video("sai-paleta-pierde", "adivina", "¿Paleta con pérdidas?", "Depende de los colores", "Paleta", "paleta",
      "Una paleta es un diccionario de colores dentro del archivo: sin pérdidas si caben todos los colores, con pérdidas si no.",
      ["¿La paleta pierde calidad? Depende de una sola cosa.", "GIF no pierde... salvo cuando sí.", "Un diccionario de colores: ¿con o sin pérdidas?"], 0, [
    S("el reto", "¿Una paleta comprime con pérdidas o *sin* pérdidas? Depende de una sola cosa.", "¿PIERDE *CALIDAD*?",
      pregunta("Paleta (GIF): ¿con o sin pérdidas?", ["Siempre sin pérdidas", "Siempre con pérdidas", "Depende de los colores"], 2)),
    S("qué es", "Una paleta es un diccionario de colores: cada píxel guarda solo un *número* que apunta al color.", "UN *DICCIONARIO*",
      alerta("📖", "Píxel → índice → color RGB", "GIF: 256 ENTRADAS")),
    S("el ahorro", "GIF tiene doscientas cincuenta y seis entradas de veinticuatro bits. Cada píxel pasa de veinticuatro a *ocho* bits.", "24 → *8 BITS*",
      calculo("24 bits/píxel", "256 entradas → 8 bits", "factor 3")),
    S("caben", "Si la imagen tiene como mucho esos colores, cabe todo: *sin pérdidas*.", "CABEN: *SIN PÉRDIDA*",
      alerta("✅", "Colores ≤ entradas", "SIN PÉRDIDAS")),
    S("no caben", "Si hay más colores que entradas, se quedan los más frecuentes y el resto se aproxima: *con pérdidas*.", "NO CABEN: *PIERDES*",
      alerta("✂️", "Más colores que entradas", "CON PÉRDIDAS")),
    S("para recordar", "Y la paleta va *siempre* dentro del archivo: sin diccionario, no se puede decodificar.", "VA *DENTRO*",
      alerta("📦", "El decodificador la necesita", "SIEMPRE EN EL ARCHIVO")),
])

video("sai-paleta-calculo", "resuelto", "Calcular la paleta", "Entradas y bits", "Paleta", "paleta",
      "Las entradas necesarias son una potencia de dos que supere los colores distintos; su exponente son los bits por píxel y el factor es 24 / bits.",
      ["Una foto de 800×600 con 86 192 colores distintos: ¿cabe en paleta?", "¿Cuántos bits necesita una paleta? Un exponente.", "Ochenta y seis mil colores: ¿cuántos bits?"], 0, [
    S("el enunciado", "Imagen de ochocientos por seiscientos, con ochenta y seis mil ciento noventa y dos colores *distintos*. ¿Paleta?", "¿SE *PUEDE*?",
      alerta("🖼️", "800×600 · 24 bits/píxel", "86 192 COLORES")),
    S("el máximo", "Primero: ¿cuántos colores puede haber como máximo? Uno por píxel: *cuatrocientos ochenta mil*.", "MÁXIMO *480 000*",
      calculo("800 × 600", "= 480 000 píxeles", "≤ 480 000 colores")),
    S("compensa", "Y hay solo ochenta y seis mil: muchísimos menos que dieciséis millones. Así que *sí* compensa una paleta.", "SÍ *COMPENSA*",
      alerta("✅", "86 192 ≪ 16,7 millones", "PALETA POSIBLE")),
    S("16 bits", "Para no perder nada hacen falta entradas para todos. Con dieciséis bits son sesenta y cinco mil... se queda *corto*.", "16 BITS *NO LLEGA*",
      calculo("16 bits → 65 536", "< 86 192 ✗")),
    S("17 bits", "Con diecisiete bits, ciento treinta y un mil setenta y dos entradas: *ahora sí* caben.", "17 BITS *SÍ*",
      calculo("17 bits → 131 072", "≥ 86 192 ✓")),
    S("el factor", "Pasas de veinticuatro a diecisiete bits por píxel: comprimes *uno coma cuatro* veces.", "FACTOR *1,4*",
      big("×1,4", "24 ÷ 17 bits/píxel · sin pérdidas")),
    S("para recordar", "Regla: busca la potencia de dos que supere tus colores. Su *exponente* son tus bits.", "EXPONENTE = *BITS*",
      alerta("🔑", "2^bits ≥ colores", "BITS = EXPONENTE")),
])

video("sai-jpeg-progresivo", "analogia", "JPEG progresivo", "Primero borroso, luego nítido", "JPEG", "jpeg",
      "JPEG progresivo manda primero las frecuencias bajas de todos los bloques y luego los detalles: la foto sale borrosa y se afina.",
      ["Hay fotos que llegan borrosas y se afinan solas: no es un truco web.", "¿Por qué algunas fotos se afinan al cargar? Se mandan al revés.", "Primero el boceto, luego los detalles."], 0, [
    S("el gancho", "Hay fotos que llegan borrosas y se van afinando solas. No es un truco de la web: es *JPEG progresivo*.", "BORROSO → *NÍTIDO*",
      img("sai-progresivo.png", "afinando")),
    S("analogía", "Imagina un dibujo: primero haces el boceto de toda la hoja, y luego vas *puliendo*. No acabas la esquina antes.", "PRIMERO *BOCETO*",
      alerta("✏️", "Boceto de toda la imagen", "LUEGO DETALLES")),
    S("la diferencia", "En el JPEG normal mandas bloque a bloque, cada uno *completo*. En el progresivo mandas todos los bloques, poco a poco.", "NORMAL O *PROGRESIVO*",
      vs({"icono": "🧱", "titulo": "Normal", "puntos": ["bloque a bloque", "completo"]},
         {"icono": "🌫️", "titulo": "Progresivo", "puntos": ["todos los bloques", "por capas"]}, "der")),
    S("el cómo", "Primer barrido: solo las frecuencias *bajas* de todos los bloques. Luego otro con las siguientes, y otro...", "BAJAS *PRIMERO*",
      img("sai-zigzag-orden.png", "bajas", "barrido 1: los primeros coeficientes")),
    S("forma y detalle", "Las bajas dan la forma general; las altas, los *detalles*. Con las primeras ya reconoces la foto.", "FORMA, LUEGO *DETALLE*",
      alerta("👁️", "Bajas = forma · Altas = detalle", "YA SE RECONOCE")),
    S("para recordar", "Por eso va bien en enlaces lentos: ves la foto *antes* de que termine de bajar.", "ENLACE *LENTO*",
      alerta("🐢", "Vista previa sin esperar", "VES ANTES DE TERMINAR")),
])

video("sai-mjpeg-bloques", "resuelto", "Caudal de MJPEG", "Cuenta bloques de 8×8", "JPEG", "mjpeg",
      "Caudal = (bloques Y × bits Y + bloques C × bits C) × imágenes por segundo; 640×480 4:2:0 a 25 im/s con 38 y 26 bits da 6,12 Mbit/s.",
      ["¿Cuánto caudal genera una cámara MJPEG? Cuenta bloques de ocho por ocho.", "Seis megabits sin saber nada de vídeo: solo contar bloques.", "Una cámara, una multiplicación."], 0, [
    S("el enunciado", "Cámara *MJPEG*: seiscientos cuarenta por cuatrocientos ochenta, veinticinco imágenes por segundo. ¿Cuántos megabits?", "¿CUÁNTO *CAUDAL*?",
      alerta("📹", "640×480 · 25 im/s · 4:2:0", "¿Mbit/s?")),
    S("luminancia", "Bloques de ocho por ocho: seiscientos cuarenta por cuatrocientos ochenta entre sesenta y cuatro, *cuatro mil ochocientos*.", "BLOQUES *Y*",
      calculo("640 × 480 ÷ 64", "= 4800 bloques Y")),
    S("color", "El color va a un cuarto: *mil doscientos* de Cb y mil doscientos de Cr.", "COLOR: *2400*",
      calculo("4800 ÷ 4 = 1200 Cb", "1200 Cr", "= 2400 bloques C")),
    S("los bits", "Cuatro mil ochocientos por treinta y ocho, más dos mil cuatrocientos por veintiséis: *244 800* bits.", "BITS POR *IMAGEN*",
      calculo("4800 × 38 = 182 400", "2400 × 26 = 62 400", "= 244 800 bits")),
    S("el caudal", "Por veinticinco imágenes por segundo: *seis coma doce* megabits por segundo.", "6,12 *Mbit/s*",
      calculo("244 800 × 25", "= 6,12 Mbit/s")),
    S("para recordar", "Siempre igual: cuenta bloques, multiplica por bits, y por las imágenes de cada *segundo*.", "BLOQUES × *BITS*",
      big("B × b × fps", "bloques × bits/bloque × imágenes/s")),
])

# =====================================================================  VÍDEO
video("sai-mpeg-ipb", "analogia", "I, P y B", "Un álbum de fotos", "MPEG GoP", "mpeg",
      "I = foto completa (un JPEG), P = parche respecto al pasado, B = usa pasado y futuro y es la más barata.",
      ["Un vídeo MPEG es un álbum donde solo algunas hojas son fotos de verdad.", "Tres tipos de imagen: la foto, el parche y el comodín.", "¿Por qué una imagen pesa cinco veces menos que otra?"], 0, [
    S("el gancho", "Un vídeo MPEG es como un álbum donde solo *algunas* hojas son fotos de verdad.", "ÁLBUM *MPEG*",
      alerta("📔", "Tres tipos de imagen", "I · P · B")),
    S("la I", "La *I* es la foto entera: un JPEG de toda la vida. Se entiende ella sola.", "I = *FOTO*",
      alerta("📷", "Un JPEG por sí sola", "NO DEPENDE DE NADIE")),
    S("la P", "La *P* dice: es como la anterior, pero esto se movió así. Solo guarda la *diferencia*.", "P = *PARCHE*",
      alerta("🩹", "Mira hacia atrás", "GUARDA LA DIFERENCIA")),
    S("la B", "La *B* mira a las dos: la anterior y la que *viene*. Por eso es la más barata.", "B = *AMBAS*",
      alerta("🔀", "Pasado y futuro", "LA MÁS BARATA")),
    S("los tamaños", "En un ejemplo: la I pesa cuarenta mil bytes, la P dieciséis mil, y la B *ocho mil*.", "¿Y CUÁNTO *PESAN*?",
      filas(("📷", "Imagen I", "40 000 B", "cuarenta"), ("🩹", "Imagen P", "16 000 B", "dieciséis"), ("🔀", "Imagen B", "8 000 B", "ocho"))),
    S("para recordar", "Cuanto más mira a otras, *menos pesa*. La I, que no mira a nadie, es la más cara.", "MIRA = *AHORRA*",
      alerta("💡", "I > P > B (en peso)", "MIRAR AHORRA BITS")),
])

video("sai-mpeg-n-m", "regla", "N y M", "Dos distancias", "MPEG GoP", "mpeg",
      "N = distancia entre I y la siguiente I (longitud del GoP); M = distancia entre referencias (I o P); entre ellas hay M−1 B.",
      ["N y M se confunden siempre. Truco: una se cuenta entre I, otra entre referencias.", "Dos letras que todo el mundo mezcla.", "I B B P B B P B B: ¿cuánto valen N y M?"], 0, [
    S("el gancho", "N y M se confunden siempre. Truco: mira la secuencia I B B P B B P B B, y cuenta.", "N Y *M*",
      img("sai-gop-nm.png")),
    S("N", "*N* es la distancia entre una I y la siguiente. Aquí, nueve imágenes: N igual a nueve.", "N = *9*",
      img("sai-gop-nm.png", None, "de I a I")),
    S("GoP", "Esas nueve forman un *GoP*: el grupo de imágenes que cuelga de una I.", "GOP = *N*",
      alerta("🧩", "Grupo de imágenes", "LONGITUD = N")),
    S("M", "*M* es la distancia entre referencias: de la I a la P. Aquí tres: M igual a tres.", "M = *3*",
      img("sai-gop-nm.png", None, "de referencia a referencia")),
    S("las B", "Y entre dos referencias siempre hay M menos uno B. Con M igual a tres, *dos B*.", "B = *M − 1*",
      calculo("M = 3", "B seguidas = M − 1", "= 2")),
    S("para recordar", "Regla: N entre I, M entre referencias, y las B son M menos uno. Sin B, *M vale uno*.", "SIN B, *M = 1*",
      alerta("🔑", "I P P P P...", "M = 1")),
])

video("sai-mpeg-n-error", "resuelto", "Sacar N y M", "Con el caudal y un error", "MPEG GoP", "mpeg",
      "N sale del peor caso de error (se arregla en la siguiente I) y M de la media de bytes por imagen.",
      ["Te dan caudal, tamaños y cuánto dura un error: con eso sacas N y M.", "N y M sin ver la secuencia.", "Un error dura ocho imágenes: ¿cuánto vale N?"], 0, [
    S("el enunciado", "Un vídeo a veinticinco imágenes por segundo y dos coma seis megabits. Un error dura como mucho *ocho* imágenes.", "¿N Y *M*?",
      alerta("🧮", "25 im/s · 2,6 Mbit/s", "ERROR: 8 IMÁGENES")),
    S("N", "Un error se arrastra hasta la siguiente I. Si dura ocho, la I llega cada ocho: *N igual a ocho*.", "N = *8*",
      alerta("🩹", "El error muere en la próxima I", "N = 8")),
    S("la media", "Para M miramos el tamaño medio: dos coma seis megabits entre veinticinco: *trece mil bytes* por imagen.", "MEDIA *13 000 B*",
      calculo("2 600 000 ÷ 25 = 104 000 bits", "÷ 8 = 13 000 bytes")),
    S("la cuenta", "En ocho imágenes hay una I, unas cuantas P y el resto B. Hechas las cuentas: doce mil más mil por cada *P*.", "12 000 + *1000 P*",
      calculo("(40 000 + P·16 000", "+ (7−P)·8 000) ÷ 8", "= 12 000 + 1000·P")),
    S("la P", "Igualas a trece mil, y sale una sola P: *P igual a uno*.", "P = *1*",
      calculo("13 000 = 12 000 + 1000·P", "P = 1")),
    S("el resultado", "Una I, una P y seis B en ocho: I B B B P B B B. Entre referencias hay cuatro: *M igual a cuatro*.", "N=8 · *M=4*",
      big("N=8 M=4", "I B B B P B B B")),
])

video("sai-mpeg-reordenar", "porque", "Reordenar imágenes", "El futuro primero", "MPEG GoP", "mpeg",
      "La B necesita una imagen futura, así que se codifica y manda la P antes que las B; el receptor reordena y eso mete retardo.",
      ["¿Cómo codificas una imagen que depende de otra que aún no ha pasado?", "MPEG no se manda en el orden en que lo ves.", "Una imagen no sale hasta que llegue su futuro."], 0, [
    S("el problema", "¿Cómo codificas una imagen que depende de otra que *todavía no ha pasado*?", "EL *FUTURO*",
      alerta("⏳", "B mira a una P que viene después", "¿CÓMO?")),
    S("esperas", "Muy fácil: esperas. La cámara da I cero, B uno, B dos, B tres, y P *cuatro*.", "ESPERAS *A LA P*",
      img("sai-reorden.png", "cuatro.")),
    S("la P antes", "Entonces se codifica la P cuatro *antes* que las B, porque las B la necesitan.", "P *ANTES* QUE B",
      img("sai-reorden.png", "antes")),
    S("se manda", "Se manda así: I cero, P cuatro, B uno, B dos, B tres... y el *receptor* las recoloca.", "SE *RECOLOCA*",
      img("sai-reorden.png", "receptor")),
    S("el coste", "Y ojo: B uno no se puede ver hasta que llegue P cuatro. Ahí se pierde *tiempo*.", "ESPERAR = *RETARDO*",
      alerta("⏱️", "B espera a su P", "RETARDO")),
    S("para recordar", "Regla: sin B no hay que reordenar; con B, *esperas*. Es el precio de comprimir más.", "B = *ESPERA*",
      alerta("💸", "B comprime más", "PERO CUESTA RETARDO")),
])

video("sai-mpeg-retardo", "formula", "Retardo de reordenar", "M por el tiempo de una imagen", "MPEG retardo", "mpeg",
      "Retardo de reordenación = (M−1) imágenes en el codificador + 1 en el decodificador = M imágenes × tiempo por imagen.",
      ["¿Cuánto retardo mete reordenar? Una resta, una suma y una multiplicación.", "Cuatro imágenes de espera: ¿cuántos milisegundos?", "Reordenar cuesta M imágenes."], 0, [
    S("el reto", "¿Cuánto retardo mete reordenar? Con M cuatro y veinticinco por segundo: una *resta*, una suma y una multiplicación.", "¿CUÁNTO *RETARDO*?",
      alerta("⏱️", "M = 4 · 25 im/s", "¿CUÁNTOS ms?")),
    S("codificador", "En el codificador esperas M menos uno: *tres* imágenes, hasta que llega la P.", "CODIFICADOR: *M − 1*",
      calculo("4 − 1", "= 3 imágenes")),
    S("decodificador", "En el decodificador esperas *una*: la P tiene que llegar antes de enseñar las B.", "DECODIFICADOR: *1*",
      alerta("1️⃣", "Decodificador: +1 imagen", "ESPERA A LA P")),
    S("el total", "Total: tres más una, *cuatro* imágenes. Siempre te sale M.", "TOTAL = *M*",
      calculo("3 + 1", "= 4 imágenes")),
    S("en tiempo", "A veinticinco por segundo, una imagen dura cuarenta milisegundos. Cuatro por cuarenta: *ciento sesenta*.", "160 *ms*",
      calculo("1 imagen = 1 ÷ 25 = 40 ms", "4 × 40", "= 160 ms")),
    S("para recordar", "Regla: retardo igual a M por el tiempo de una imagen. Y ojo con las imágenes por segundo: *cambian* el tiempo.", "M × *T IMAGEN*",
      big("M × T", "T = 1 / imágenes por segundo")),
])

video("sai-mpeg-videoconferencia", "adivina", "¿Sirve para videollamada?", "El límite de 150 ms", "MPEG retardo", "mpeg",
      "Una videoconferencia pide menos de 150 ms en un sentido; solo reordenar con M=4 ya son 160 ms, así que N y M de TV no sirven: sin B no se reordena.",
      ["¿Sirve ese MPEG para videoconferencia? Mira un solo número.", "Ciento sesenta contra ciento cincuenta.", "La tele puede esperar. Una videollamada, no."], 0, [
    S("el reto", "Con N ocho y M cuatro, ¿sirve para una videoconferencia? Mira *un solo número*.", "¿SIRVE?",
      pregunta("N = 8, M = 4 a 25 im/s → videoconferencia", ["Sí, va justo", "Sí, con buena red", "No, pasa de 150 ms"], 2, "número.")),
    S("el límite", "Hablar de tú a tú pide como mucho ciento cincuenta milisegundos en un sentido. Son *trescientos* ida y vuelta.", "LÍMITE *150 ms*",
      big("150 ms", "un sentido (300 ms ida y vuelta)")),
    S("reordenar", "Y solo reordenar ya son *ciento sesenta*. Te pasas... sin haber mandado nada por la red.", "REORDENAR: *160 ms*",
      calculo("Reordenar: 160 ms", "Límite: 150 ms", "160 > 150 ✗")),
    S("lo demás", "Y aún faltan la CPU, empaquetar, la red, el buffer y descomprimir. Todo eso *se suma*.", "Y *LO DEMÁS*",
      alerta("➕", "CPU · paquetes · red · buffer", "TODO SE SUMA")),
    S("la solución", "La solución es sin B: solo I y P. Sin B no hay que reordenar: *cero* retardo por ahí.", "SIN B, *SIN ESPERA*",
      alerta("✂️", "I P P P P...", "REORDENAR = 0")),
    S("para recordar", "Regla: la televisión puede esperar, la videoconferencia *no*. M pequeño, o sin B.", "VIDEOCONF: *M=1*",
      alerta("🔑", "TV: puede esperar", "VIDEOCONF: NO")),
])

video("sai-mpeg-bitrate", "resuelto", "Caudal de MPEG", "Cuántas I, P y B hay", "MPEG retardo", "mpeg",
      "En un GoP con N=15 y M=3 hay 1 I, 4 P y 10 B; media ponderada de tamaños × imágenes por segundo = 1,4 Mbit/s.",
      ["¿Cuántos megabits genera un MPEG? Cuenta las I, P y B de un GoP.", "Una media ponderada y listo.", "Quince imágenes: ¿cuántas son I, P y B?"], 0, [
    S("el reto", "Tienes N igual a quince, M igual a tres. ¿Cuántas I, P y B hay en cada grupo? Eso decide *el caudal*.", "CUENTA *I P B*",
      alerta("🧮", "N = 15 · M = 3", "¿CUÁNTAS DE CADA?")),
    S("las P", "Una I por grupo. Y de P: quince entre tres, menos uno... *cuatro*.", "P = N/M − *1*",
      calculo("15 ÷ 3 − 1", "= 4 P")),
    S("las B", "Las B son las que sobran: quince menos una, menos cuatro... *diez*.", "B = *10*",
      calculo("15 − 1 − 4", "= 10 B")),
    S("la media", "Ahora la media: I catorce mil cuatrocientos, P siete mil seiscientos, B cuatro mil trescientos, cada una con su *peso*.", "MEDIA *PONDERADA*",
      calculo("14 442 · 1/15", "+ 7 595 · 4/15", "+ 4 311 · 10/15")),
    S("el resultado", "Salen cinco mil ochocientos sesenta y dos bytes por imagen: a veintinueve coma noventa y siete, *uno coma cuatro* megabits.", "1,4 *Mbit/s*",
      calculo("5 862 B × 8 = 46 897 bits", "× 29,97 im/s", "≈ 1,405 Mbit/s")),
    S("para recordar", "Siempre igual: media ponderada de tamaños, por ocho bits, por imágenes por segundo. Y ojo con los *bytes*.", "BYTES × 8 × *FPS*",
      big("× 8 × fps", "bytes/imagen → bit/s")),
])

video("sai-mpeg-macrobloques", "vs", "Saltado vs no codificado", "Macrobloques de MPEG", "Macrobloques", "mpeg",
      "Saltado (skipped) = no se manda nada; no codificado (not coded) = solo vector, sin JPEG de diferencia. La I solo tiene intra; la B puede tenerlos todos.",
      ["Skipped y Not coded parecen lo mismo. No lo son.", "Seis tipos de macrobloque y dos se confunden.", "¿Qué manda un macrobloque que no manda nada?"], 0, [
    S("el gancho", "El *saltado* y el *no codificado* parecen lo mismo. Los dos casi no llevan nada... pero no es igual.", "¿SON *IGUALES*?",
      alerta("🤔", "Skipped y Not coded", "¿LO MISMO?")),
    S("saltado", "El *saltado* no manda nada: ni vector ni diferencia. Es casi igual que antes, y se copia.", "SKIPPED = *NADA*",
      alerta("⏭️", "Casi no cambió", "NO SE MANDA NADA")),
    S("no codificado", "El *no codificado* sí manda vector de movimiento, pero ninguna diferencia: se movió, y no cambió.", "NOT CODED = *VECTOR*",
      alerta("🧭", "Se movió sin cambiar", "VECTOR, SIN JPEG")),
    S("el resumen", "Saltado, nada. No codificado, vector. Los demás llevan vector *más* diferencia.", "NADA O *VECTOR*",
      vs({"icono": "⏭️", "titulo": "Skipped", "puntos": ["nada"]}, {"icono": "🧭", "titulo": "Not coded", "puntos": ["vector", "sin JPEG"]})),
    S("dónde", "En la I todos son *intra*. En la P: intra, forward, saltados y no codificados. En la B, todos.", "¿DÓNDE *APARECEN*?",
      filas(("📷", "Imagen I", "Intra", "intra."), ("🩹", "Imagen P", "Intra · Fwd · Skip · NC", "P:"), ("🔀", "Imagen B", "Todos", "todos."))),
    S("para recordar", "Regla: la I solo *intra*; la B puede tener todos. Y los que no mandan diferencia, casi gratis.", "I = *INTRA*",
      alerta("🔑", "I → solo Intra", "B → TODOS")),
])

video("sai-perfiles-bytes", "adivina", "Adivina el códec", "Solo con las barras", "Macrobloques", "mpeg",
      "Por la gráfica de bytes/imagen: plana = ITU-R 601 (CBR), variable sin patrón = MJPEG, tres niveles periódicos = MPEG, imagen enorme y luego pequeñas = H.261.",
      ["Adivina el códec mirando solo las barras.", "Cuatro gráficas, cuatro códecs.", "Una gráfica de barras te dice qué códec es."], 0, [
    S("el reto", "Te enseñan solo barras de bytes por imagen... y adivinas el códec. Cuatro *gráficas*, cuatro códecs.", "ADIVINA *EL CÓDEC*",
      img("sai-perfiles.png")),
    S("A", "*A*, todas iguales: ITU-R seiscientos uno. Es el único de *caudal constante*.", "A = *ITU-R 601*",
      img("sai-perfiles.png", None, "A: todas iguales")),
    S("B", "*B*, tamaños parecidos pero que bailan. Eso es MJPEG: cada imagen es un JPEG por su *cuenta*.", "B = *MJPEG*",
      img("sai-perfiles.png", None, "B: parecidas, pero variables")),
    S("C", "*C*, tres alturas que se repiten, perfectamente periódicas: I, P y B. Es *MPEG*.", "C = *MPEG*",
      img("sai-perfiles.png", None, "C: tres niveles periódicos")),
    S("D", "*D*, una primera imagen enorme y luego pequeñas, con algún refresco. Eso es *H.261*.", "D = *H.261*",
      img("sai-perfiles.png", None, "D: una grande y luego chicas")),
    S("para recordar", "Truco: plana, ITU; variable sin patrón, MJPEG; periódica, MPEG; una gigante y *chicas*, H.261.", "4 *PERFILES*",
      calculo("plana → ITU-R 601", "variable → MJPEG", "con patrón → MPEG", "1 gigante → H.261")),
])

video("sai-cambio-escena", "porque", "Pico extraño", "Cambio de escena", "Macrobloques", "mpeg",
      "Un pico fuera de sitio es un cambio de escena: la predicción ya no sirve y el codificador convierte una P en I y reinicia el GoP (en H.261, casi todo pasa a Intra).",
      ["Un pico gigante en mitad de la secuencia: no es un error.", "Un corte de plano rompe el GoP.", "¿Por qué hay una I donde tocaba una P?"], 0, [
    S("el gancho", "Ves un pico gigante *en mitad* de la secuencia, donde tocaba una P. ¿Error? No.", "PICO *EXTRAÑO*",
      img("sai-escena.png")),
    S("el corte", "Es un cambio de escena. La imagen nueva no se parece *nada* a la anterior.", "CORTE DE *PLANO*",
      alerta("🎬", "Otra escena, otros colores", "NADA QUE COPIAR")),
    S("por qué", "Predecir desde la anterior no sirve de nada: el parche saldría *más grande* que la foto.", "PREDECIR *NO SIRVE*",
      alerta("🩹", "Diferencia ≈ imagen entera", "MEJOR UNA FOTO")),
    S("la solución", "Así que el codificador convierte esa P en una *I* y reinicia el grupo de imágenes.", "P → *I*",
      img("sai-escena.png", None, "el GoP se reinicia")),
    S("H.261", "En H.261 pasa parecido: casi todos los macrobloques se vuelven *intra*, y los vectores salen raros.", "H.261: *INTRA*",
      alerta("🌀", "Casi todo pasa a Intra", "VECTORES RAROS")),
    S("para recordar", "Regla: un pico fuera de sitio es un cambio de escena. Y el grupo *vuelve a empezar*.", "PICO = *CORTE*",
      alerta("🔑", "Pico donde no toca", "= CAMBIO DE ESCENA")),
])

# ===================================================================== LINT + ESCRITURA
PROHIBIDAS = re.compile(r"\b(examen|test|preguntas?|control|estudiar|estudio)\b", re.I)

def toks(sub):
    out = []
    for raw in sub.split():
        m = re.fullmatch(r"\[(.*)\]([.,:;!?…]*)", raw)
        if m:
            continue
        out.append(raw.replace("*", ""))
    return out

def lint():
    errores, formatos = [], [v["formato"] for v in V]
    for a, b in zip(formatos, formatos[1:]):
        if a == b:
            errores.append(f"formato repetido seguido: {a}")
    ids = set()
    for v in V:
        if v["id"] in ids: errores.append("id repetido " + v["id"])
        ids.add(v["id"])
        if not (4 <= len(v["segmentos"]) <= 7): errores.append(f"{v['id']}: nº segmentos {len(v['segmentos'])}")
        for s in v["segmentos"]:
            t = toks(s["sub"])
            n = len(" ".join(t))
            if n > 125: errores.append(f"{v['id']}/{s['tag']}: sub largo ({n}) → {s['sub']}")
            if PROHIBIDAS.search(s["sub"]) or PROHIBIDAS.search(s["titulo"]):
                errores.append(f"{v['id']}/{s['tag']}: palabra prohibida")
            vis = s["visual"]
            ens = []
            if vis.get("en"): ens.append(vis["en"])
            for l in vis.get("lineas", []) + vis.get("filas", []):
                if l.get("en"): ens.append(l["en"])
            for e in ens:
                if e not in t: errores.append(f"{v['id']}/{s['tag']}: en '{e}' no está en {t}")
            if len(re.sub(r"[*]", "", s["titulo"])) > 22: errores.append(f"{v['id']}/{s['tag']}: título largo '{s['titulo']}'")
    return errores


if __name__ == "__main__":
    errs = lint()
    for e in errs: print("LINT:", e)
    if "--solo-lint" in sys.argv: sys.exit(1 if errs else 0)
    for v in V:
        (HERE / f"{v['id']}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), "utf-8")
    chars = sum(len(" ".join(toks(s["sub"]))) for v in V for s in v["segmentos"])
    print(len(V), "specs escritos · caracteres aprox:", chars)
