"""Specs de los TikToks del Tema 1 de CESA (acondicionamiento de energía). Uso: python3 generar_specs_t1.py"""
import json, os

def A(icono, l1, l2, stamp=None):
    v = {"tipo": "alerta", "icono": icono, "linea1": l1, "linea2": l2}
    if stamp: v["stamp"] = stamp
    return v

def F(*filas, stamp=None):
    v = {"tipo": "filas", "filas": [dict(zip(("icono", "izq", "der", "rojo", "en"), f)) for f in filas]}
    for f in v["filas"]:
        if f.get("rojo") is None: f.pop("rojo", None)
        if f.get("en") is None: f.pop("en", None)
    if stamp: v["stamp"] = stamp
    return v

def B(big, small, stamp=None):
    v = {"tipo": "big", "big": big, "small": small}
    if stamp: v["stamp"] = stamp
    return v

def S(tag, sub, titulo, visual, num=None):
    s = {"tag": tag, "sub": sub, "titulo": titulo, "visual": visual}
    if num: s["num"] = num
    return s

R = "en resumen"; RT = "EN *RESUMEN*"; C = "la curiosidad"

V = []

V.append({"id": "cesa-familias-y-rendimiento", "titulo": "Las 4 familias de un cargador",
 "texto": "Qué entra, qué sale y cuánto se pierde", "examen": "MQ", "tema": "CESA · Conversión de energía", "etiqueta": "conversión",
 "pron": {"AC": "alterna", "DC": "continua"},
 "segmentos": [
  S(C, "¿Sabías que convertir energía tiene solo *cuatro* familias... según lo que entra y lo que sale?", "4 *FAMILIAS*",
    A("🔌", "alterna o continua, a la entrada y a la salida", "4 FAMILIAS")),
  S("alterna y continua", "De alterna a continua... un *rectificador.* De continua a alterna... un *inversor.*", "AC *Y* DC",
    F(("🔁", "Alterna → continua", "RECTIFICADOR", None, "rectificador."), ("🔁", "Continua → alterna", "INVERSOR", True, "inversor.")), 1),
  S("las otras dos", "De continua a continua... un *regulador.* Y de alterna a alterna, cambiando la frecuencia... un *cicloconvertidor.*", "LAS *OTRAS* DOS",
    F(("⚙️", "Continua → continua", "REGULADOR", None, "regulador."), ("🔄", "Alterna → alterna", "CICLOCONVERTIDOR", True, "cicloconvertidor.")), 1),
  S("rendimiento", "Lo que importa es el *rendimiento:* la potencia que sale... entre la que entra. Lo que falta se convierte en *calor.*", "*RENDIMIENTO*",
    B("SALE / ENTRA", "lo que falta = calor"), 2),
  S("en cadena", "Y si pones dos en cadena... los rendimientos se *multiplican.* Noventa por ciento por ochenta... setenta y dos por *ciento.*", "SE *MULTIPLICAN*",
    B("0,9 · 0,8 = 0,72", "dos convertidores en cadena"), 2),
  S("el tamaño", "Por eso un cargador *pequeño* necesita mucho rendimiento: si casi no hay calor... no hace falta *radiador.*", "PEQUEÑO = *EFICIENTE*",
    A("🔥", "poco calor, sin radiador", "PEQUEÑO = RENDIMIENTO ALTO"), 3),
  S(R, "Así que ya sabes. Cuatro familias según lo que entra y sale... y los rendimientos en cadena se *multiplican.*", RT,
    F(("🔌", "Clasificar", "QUÉ ENTRA → QUÉ SALE", None, "sale..."), ("✖️", "En cadena", "SE MULTIPLICAN", True, "multiplican."))),
 ]})

V.append({"id": "cesa-condensador-rectificador", "titulo": "El condensador que castiga a los diodos",
 "texto": "Menos rizado... a un precio", "examen": "MQ", "tema": "CESA · Rectificadores", "etiqueta": "rectificadores",
 "pron": {},
 "segmentos": [
  S(C, "¿Sabías que poner un condensador más *grande* en una fuente... hace sufrir más a los *diodos?*", "MÁS C, *MÁS PICO*",
    A("🔋", "más condensador en el filtro", "MÁS PICO EN LOS DIODOS")),
  S("el pico", "El condensador se carga hasta el *pico* de la onda... no hasta el valor eficaz. Por eso siempre aparece la raíz de *dos.*", "HASTA EL *PICO*",
    B("√2 · Vef", "230 V eficaces → unos 325 V de pico"), 1),
  S("el rizado", "Entre pico y pico, el condensador alimenta él solo a la carga... y se va *vaciando.* Eso es el *rizado.*", "EL *RIZADO*",
    A("📉", "entre picos, el condensador se descarga", "RIZADO"), 1),
  S("más condensador", "Con más condensador se vacía menos... y el diodo solo conduce un instante, en la *puntita* del pico.", "UN *INSTANTE*",
    F(("🔋", "Más condensador", "MENOS RIZADO", None, None), ("⏱️", "El diodo conduce", "UN INSTANTE", True, "puntita"))),
  S("el precio", "Pero tiene que reponer la misma carga... en mucho menos tiempo. Resultado: un pico de corriente [(intensidad)] *enorme.*", "PICO *ENORME*",
    A("⚡", "misma carga en menos tiempo", "PICO ENORME", "¡OJO!"), 2),
  S("media onda", "Y en media onda es peor: recarga una sola vez por ciclo... así que el rizado y el pico salen el *doble.*", "MEDIA *ONDA*",
    F(("1️⃣", "Media onda: se descarga", "UN PERIODO", True, None), ("2️⃣", "Onda completa: se descarga", "MEDIO PERIODO", None, None)), 3),
  S(R, "Así que ya sabes. Más condensador... menos rizado, pero más pico en los *diodos.*", RT,
    F(("📉", "Más condensador", "MENOS RIZADO", None, "rizado,"), ("⚡", "Pero", "MÁS PICO EN LOS DIODOS", True, "diodos."))),
 ]})

V.append({"id": "cesa-graetz-vs-toma-media", "titulo": "Puente de Graetz o toma media",
 "texto": "Dos rectificadores, dos trampas", "examen": "MQ", "tema": "CESA · Rectificadores", "etiqueta": "rectificadores",
 "pron": {"Graetz": "grets"},
 "segmentos": [
  S(C, "¿Sabías que hay dos formas de aprovechar las *dos* mitades de la onda... y cada una tiene su *trampa?*", "ONDA *COMPLETA*",
    A("🌊", "aprovechar los dos semiciclos", "DOS FORMAS")),
  S("Graetz", "El puente de *Graetz* usa cuatro diodos en rombo. En cada mitad de la onda... conducen *dos* a la vez.", "PUENTE DE *GRAETZ*",
    F(("🔷", "Puente de Graetz", "4 DIODOS", None, "rombo."), ("⚡", "Conducen a la vez", "DOS", True, "vez.")), 1),
  S("toma media", "La toma media usa un transformador partido en dos... y solo dos diodos. Aquí conduce *uno* cada vez.", "TOMA *MEDIA*",
    F(("🔌", "Toma media", "2 DIODOS", None, "diodos."), ("⚡", "Conduce cada vez", "UNO", True, "cada")), 1),
  S("trampa uno", "Primera trampa: cada diodo que conduce se come unos cero coma siete voltios. En Graetz pierdes el *doble.*", "TRAMPA *1*",
    F(("🔷", "Graetz", "PIERDE 2 × 0,7 V", True, "Graetz"), ("🔌", "Toma media", "PIERDE 0,7 V", None, "voltios.")), 2),
  S("trampa dos", "Segunda trampa, al revés: el diodo apagado de la toma media aguanta *dos* veces la tensión [(voltaje)] de salida. En Graetz... solo *una.*", "TRAMPA *2*",
    F(("🔌", "Toma media aguanta", "≈ 2 × Vo", True, "aguanta"), ("🔷", "Graetz aguanta", "≈ Vo", None, "una.")), 3),
  S(R, "Así que ya sabes. Graetz pierde más tensión [(voltaje)]... y la toma media hace sufrir más a sus *diodos.*", RT,
    F(("🔷", "Graetz", "−2 DIODOS DE TENSIÓN", None, "Graetz"), ("🔌", "Toma media", "DIODOS AGUANTAN 2×", True, "diodos."))),
 ]})

V.append({"id": "cesa-regulador-lineal", "titulo": "El regulador lineal es un grifo",
 "texto": "Salida limpia, pero quema lo que sobra", "examen": "MQ", "tema": "CESA · Reguladores lineales", "etiqueta": "reguladores",
 "pron": {"dropout": "drop aut", "LDO": "ele de o", "LDOs": "ele de os"},
 "segmentos": [
  S(C, "¿Sabías que un regulador lineal funciona como un *grifo?* Deja pasar la corriente [(intensidad)]... y se come lo que sobra.", "UN *GRIFO*",
    A("🚰", "un transistor que se abre más o menos", "UN GRIFO")),
  S("el calor", "Todo lo que sobra entre entrada y salida... se convierte en *calor.* Por eso su rendimiento es la salida entre la *entrada.*", "QUEMA LO QUE *SOBRA*",
    B("Vo / Vin", "rendimiento de un lineal"), 1),
  S("la ventaja", "Su gran ventaja: no conmuta... así que da una salida *limpia,* sin rizado. Pero solo sabe *bajar* la tensión [(voltaje)].", "SALIDA *LIMPIA*",
    F(("✨", "Salida", "SIN RIZADO", None, "limpia,"), ("⬇️", "Solo puede", "REDUCIR", True, "bajar")), 2),
  S("dropout", "Eso sí, necesita un colchón mínimo entre entrada y salida: el *dropout.* Si la entrada baja de ahí... deja de regular.", "EL *DROPOUT*",
    A("🛏️", "diferencia mínima entre entrada y salida", "DROPOUT"), 3),
  S("LDO", "Los LDO son lineales con un colchón *pequeñito:* siguen regulando con la entrada casi pegada a la *salida.*", "LOS *LDO*",
    A("🤏", "low dropout: lineal serie", "LDO"), 3),
  S("su consumo", "Y ojo: el regulador gasta su propia corriente [(intensidad)]... que se va a masa. Por eso entra *más* de lo que sale.", "ENTRA *MÁS*",
    B("Iin = Io + Ignd", "el regulador también consume"), 4),
  S(R, "Así que ya sabes. Salida limpia, pero quema lo que *sobra*... y siempre necesita su *dropout.*", RT,
    F(("🚰", "Lineal", "QUEMA LO QUE SOBRA", None, "sobra..."), ("🛏️", "Siempre necesita", "SU DROPOUT", True, "dropout."))),
 ]})

V.append({"id": "cesa-shunt-y-regulacion", "titulo": "El regulador que se traga lo que sobra",
 "texto": "Shunt, línea y carga", "examen": "MQ", "tema": "CESA · Reguladores lineales", "etiqueta": "reguladores",
 "pron": {"shunt": "shant"},
 "segmentos": [
  S(C, "¿Sabías que hay reguladores que, en vez de cortar... se *tragan* la corriente [(intensidad)] que sobra?", "SE LA *TRAGA*",
    A("🍽️", "en paralelo con la carga", "REGULADOR SHUNT")),
  S("cómo va", "Va en *paralelo* con la carga, con una resistencia en serie. Por la resistencia entra todo... y luego se *reparte.*", "EN *PARALELO*",
    F(("🔗", "Resistencia", "EN SERIE", None, "serie."), ("🔀", "Shunt", "EN PARALELO", True, "reparte.")), 1),
  S("la regla", "Por esa resistencia tiene que entrar siempre más de lo que pide la carga en su peor *momento.* Lo que sobra... se lo traga el *shunt.*", "LA *REGLA*",
    A("📏", "corriente de la resistencia > máxima de la carga", "SIEMPRE MÁS QUE LA MÁXIMA"), 1),
  S("sus límites", "Por eso la resistencia tiene un *máximo,* para que siempre llegue... y un *mínimo,* para que el shunt no se *queme.*", "MÁXIMO Y *MÍNIMO*",
    F(("⬆️", "Resistencia máxima", "QUE SIEMPRE LLEGUE", None, "máximo,"), ("🔥", "Resistencia mínima", "QUE NO SE QUEME", True, "mínimo,")), 2),
  S("calidad", "Y para saber si un regulador es bueno se miran dos cosas: la regulación de *línea,* y la de *carga.*", "LÍNEA Y *CARGA*",
    A("🔍", "cuánto se mueve la salida", "DOS REGULACIONES"), 3),
  S("la diferencia", "La de línea: cuánto se mueve la salida si cambia la *entrada.* La de carga: si cambia la corriente [(intensidad)] que *consume.*", "NO LAS *CONFUNDAS*",
    F(("🔌", "Línea", "CAMBIA LA ENTRADA", None, "entrada."), ("💡", "Carga", "CAMBIA LO QUE CONSUME", True, "consume.")), 3),
  S(R, "Así que ya sabes. El shunt se traga lo que sobra... y línea es la *entrada,* carga es lo que *consume.*", RT,
    F(("🍽️", "Shunt", "SE TRAGA LO QUE SOBRA", None, "sobra..."), ("🔌", "Línea / carga", "ENTRADA / CONSUMO", True, "consume."))),
 ]})

V.append({"id": "cesa-lm317", "titulo": "El truco del LM317",
 "texto": "Siempre 1,25 voltios", "examen": "MQ", "tema": "CESA · Reguladores lineales", "etiqueta": "reguladores",
 "pron": {"LM317": "ele eme tres uno siete"},
 "segmentos": [
  S(C, "¿Sabías que el LM317 tiene una manía? Entre dos de sus patas... *siempre* mantiene uno coma veinticinco voltios.", "SIEMPRE *1,25 V*",
    A("🎯", "entre la salida y el pin de ajuste", "SIEMPRE 1,25 V")),
  S("la de arriba", "Esos voltios caen justo en la resistencia de *arriba*... así que por ella pasa una corriente [(intensidad)] *fija.*", "CORRIENTE *FIJA*",
    F(("📌", "Resistencia de arriba", "1,25 V", None, "arriba..."), ("➡️", "Por ella pasa", "CORRIENTE FIJA", True, "fija.")), 1),
  S("la de abajo", "Por el pin de ajuste casi no entra nada... así que esa misma corriente baja también por la resistencia de *abajo.*", "LA *MISMA*",
    A("⬇️", "por el pin de ajuste casi no entra nada", "MISMA CORRIENTE ABAJO"), 1),
  S("la fórmula", "Sumas lo que cae en las dos... y sale la fórmula: uno coma veinticinco, por uno más R dos entre R *uno.*", "LA *FÓRMULA*",
    B("1,25·(1 + R2/R1)", "tensión de salida del LM317"), 2),
  S("el detalle", "Ojo con un detalle: ese mismo factor *multiplica* los defectos del chip. Si vale dieciséis... el error sale dieciséis veces más *grande.*", "LO *AMPLIFICA*",
    A("🔍", "el factor (1 + R2/R1) también multiplica", "LA REGULACIÓN ×16", "¡OJO!"), 3),
  S(R, "Así que ya sabes. Uno coma veinticinco en la de arriba... y la misma corriente baja por la de *abajo.*", RT,
    F(("📌", "Arriba", "SIEMPRE 1,25 V", None, "arriba..."), ("⬇️", "Abajo", "LA MISMA CORRIENTE", True, "abajo."))),
 ]})

V.append({"id": "cesa-calor-regulador", "titulo": "La ley de Ohm del calor",
 "texto": "Cuánto aguanta un chip antes de quemarse", "examen": "MQ", "tema": "CESA · Térmica", "etiqueta": "calor",
 "pron": {},
 "segmentos": [
  S(C, "¿Sabías que el calor de un chip se calcula igual que la ley de *Ohm?*", "LEY DE OHM *DEL CALOR*",
    A("🔥", "calor, temperatura y resistencia térmica", "LA LEY DE OHM DEL CALOR")),
  S("las piezas", "La potencia hace de corriente [(intensidad)]... la temperatura, de tensión [(voltaje)]... y la resistencia *térmica,* de resistencia.", "LAS *PIEZAS*",
    F(("⚡", "Potencia", "HACE DE CORRIENTE", None, None), ("🌡️", "Temperatura", "HACE DE TENSIÓN", None, None), ("🧱", "Resistencia térmica", "HACE DE RESISTENCIA", True, "térmica,")), 1),
  S("la fórmula", "Así que la temperatura del chip es la del ambiente... más la resistencia térmica por la *potencia.*", "LA *FÓRMULA*",
    B("Tj = Ta + Rth · P", "temperatura de la unión"), 1),
  S("con radiador", "Sin radiador, el calor va directo al *aire.* Con radiador hace tres saltos... y la pasta térmica facilita el del *medio.*", "CON *RADIADOR*",
    F(("🌬️", "Sin radiador", "DIRECTO AL AIRE", None, "aire."), ("🧊", "Con radiador", "3 SALTOS EN SERIE", True, "medio.")), 2),
  S("el peor día", "Y para ver cuánto aguanta, piensa en el peor día: el más *caluroso.* Con cincuenta grados aguanta menos... que con *cero.*", "EL *PEOR* DÍA",
    A("🌡️", "temperatura ambiente máxima", "PEOR CASO"), 3),
  S("cuándo se calienta", "Y el chip se calienta más con mucha entrada, mucha corriente [(intensidad)]... y la salida lo más *baja* posible.", "MÁS *CALIENTE*",
    B("(Vin − Vo) · I", "entrada alta, corriente alta, salida baja"), 3),
  S(R, "Así que ya sabes. Ambiente más resistencia por potencia... y siempre el día más *caluroso.*", RT,
    F(("🔥", "Temperatura del chip", "Ta + Rth · P", None, "potencia..."), ("🌡️", "Peor caso", "AMBIENTE MÁXIMO", True, "caluroso."))),
 ]})

V.append({"id": "cesa-conmutados", "titulo": "El truco de los conmutados",
 "texto": "Encender y apagar muy rápido", "examen": "MQ", "tema": "CESA · Conmutados", "etiqueta": "conmutados",
 "pron": {"D": "de", "Buck": "bak", "Boost": "bust"},
 "segmentos": [
  S(C, "¿Sabías que los cargadores modernos encienden y apagan un transistor... cientos de miles de veces por *segundo?*", "*CONMUTAR*",
    A("⚡", "el transistor trabaja como interruptor", "ON / OFF MUY RÁPIDO")),
  S("las piezas", "La energía la guarda una *bobina*... y un condensador la suaviza. Así casi no se pierde nada en *calor.*", "BOBINA Y *CONDENSADOR*",
    F(("🌀", "Bobina", "GUARDA ENERGÍA", True, "bobina..."), ("🔋", "Condensador", "SUAVIZA LA SALIDA", None, "suaviza.")), 1),
  S("la clave", "El truco está en *D:* la fracción de tiempo que el transistor está encendido. Cambiando D... cambias la *salida.*", "EL TRUCO: *D*",
    A("⏱️", "ciclo de trabajo", "D = TIEMPO ON / PERIODO"), 1),
  S("bajar o subir", "El Buck *baja:* la salida es D por la entrada. El Boost *sube:* la entrada entre uno menos *D.*", "BUCK Y *BOOST*",
    F(("⬇️", "Buck", "Vo = D · Vin", None, "baja:"), ("⬆️", "Boost", "Vo = Vin / (1 − D)", True, "sube:")), 2),
  S("quién decide", "¿Y quién decide D? Un control que mide la salida, la compara con la *referencia*... y corrige el *error.*", "EL *CONTROL*",
    A("🎛️", "error → PID → D → PWM", "LAZO DE CONTROL"), 3),
  S("la trampa", "Una trampa: si la corriente [(intensidad)] de la bobina llega a *cero,* el diodo se apaga y aparece un tercer estado. Es el modo *discontinuo.*", "MODO *DISCONTINUO*",
    F(("✅", "Continuo", "NUNCA LLEGA A CERO", None, "cero,"), ("⚠️", "Discontinuo", "TERCER ESTADO", True, "discontinuo.")), 4),
  S(R, "Así que ya sabes. La bobina guarda, D decide la salida... y si la corriente toca *cero,* aparece el *discontinuo.*", RT,
    F(("⏱️", "La salida la decide", "D", None, "salida..."), ("⚠️", "Si toca cero", "DISCONTINUO", True, "discontinuo."))),
 ]})

V.append({"id": "cesa-flyback-forward", "titulo": "Flyback y Forward",
 "texto": "El transformador que también es bobina", "examen": "MQ", "tema": "CESA · Conmutados", "etiqueta": "conmutados",
 "pron": {"Flyback": "flái bak", "Forward": "fórguard", "Buck": "bak"},
 "segmentos": [
  S(C, "¿Sabías que el cargador de tu portátil lleva un transformador... que también hace de *bobina?*", "EL *FLYBACK*",
    A("💻", "transformador que guarda energía", "FLYBACK")),
  S("Forward", "El *Forward* es un Buck con un transformador delante. Tiene dos piezas magnéticas: el trafo... y la *bobina.*", "EL *FORWARD*",
    F(("🔌", "Forward", "TRAFO + BOBINA", None, "Forward"), ("🔢", "Piezas magnéticas", "DOS", True, "bobina.")), 1),
  S("Flyback", "El *Flyback* solo tiene una: un transformador que guarda la energía... como una bobina partida en *dos.*", "EL *FLYBACK*",
    F(("🔌", "Flyback", "SOLO EL TRAFO", None, "Flyback"), ("🔢", "Piezas magnéticas", "UNA", True, "dos.")), 1),
  S("encendido", "Mientras el transistor está encendido, el Flyback *guarda* energía... y el diodo de salida está *apagado.*", "ON: *GUARDA*",
    A("📥", "transistor encendido, diodo apagado", "GUARDA ENERGÍA"), 2),
  S("apagado", "Cuando lo apagas, el diodo se *enciende*... y toda esa energía pasa a la *salida.*", "OFF: *ENTREGA*",
    A("📤", "transistor apagado, diodo encendido", "ENTREGA ENERGÍA"), 2),
  S("en común", "Y los dos tienen algo en común: el transformador separa la entrada de la salida. Es el aislamiento *galvánico.*", "*AISLAMIENTO*",
    A("🛡️", "sin conexión eléctrica directa", "AISLAMIENTO GALVÁNICO"), 3),
  S(R, "Así que ya sabes. Forward, trafo más bobina... Flyback, solo el trafo, que *guarda* y luego *entrega.*", RT,
    F(("🔌", "Forward", "TRAFO + BOBINA", None, "bobina..."), ("🔌", "Flyback", "GUARDA Y ENTREGA", True, "entrega."))),
 ]})

V.append({"id": "cesa-mosfet-diodo", "titulo": "El diodo escondido del MOSFET",
 "texto": "Canal N, canal P y su diodo", "examen": "MQ", "tema": "CESA · Conmutados", "etiqueta": "transistores",
 "pron": {"MOSFET": "mos fet", "N": "ene", "P": "pe"},
 "segmentos": [
  S(C, "¿Sabías que todos los MOSFET llevan un *diodo* escondido dentro?", "UN DIODO *ESCONDIDO*",
    A("🕵️", "entre drenador y fuente", "DIODO PARÁSITO")),
  S("el umbral", "El de canal N se enciende con la puerta por *encima* de la fuente: umbral positivo. El de canal P... al *revés.*", "EL *UMBRAL*",
    F(("➕", "Canal N", "UMBRAL > 0", None, "encima"), ("➖", "Canal P", "UMBRAL < 0", True, "revés.")), 1),
  S("canal N", "En el de canal N, el diodo tiene el ánodo en la fuente... así que conduce cuando la tensión [(voltaje)] drenador fuente es *negativa.*", "EL DIODO *DEL N*",
    A("🔽", "ánodo en la fuente", "CONDUCE SI VDS < 0"), 2),
  S("canal P", "En el de canal P, todo al revés: el ánodo en el drenador... y conduce con esa tensión [(voltaje)] *positiva.*", "EL DIODO *DEL P*",
    A("🔼", "ánodo en el drenador", "CONDUCE SI VDS > 0"), 2),
  S("cómo se pone", "Por eso se coloca para que, apagado, el diodo quede en *inverso*... si no, el interruptor nunca se apagaría del *todo.*", "EN *INVERSO*",
    A("⚠️", "con el transistor apagado", "DIODO EN INVERSO", "¡OJO!"), 3),
  S("el truco", "Y un truco: si el interruptor va arriba, pegado a la entrada... mejor uno de canal *P.* Se enciende poniendo la puerta a *cero.*", "ARRIBA, *CANAL P*",
    F(("⬆️", "Interruptor arriba", "CANAL P", True, "P."), ("⬇️", "Interruptor abajo", "CANAL N", None, None)), 4),
  S(R, "Así que ya sabes. Todo MOSFET lleva su diodo... y hay que ponerlo para que, apagado, *bloquee.*", RT,
    F(("🕵️", "Todo MOSFET", "LLEVA UN DIODO", None, "diodo..."), ("⚠️", "Apagado", "QUE BLOQUEE", True, "bloquee."))),
 ]})

V.append({"id": "cesa-bombas-de-carga", "titulo": "Convertidores sin bobinas",
 "texto": "Las bombas de carga", "examen": "MQ", "tema": "CESA · Bombas de carga", "etiqueta": "bombas de carga",
 "pron": {},
 "segmentos": [
  S(C, "¿Sabías que se puede subir una tensión [(voltaje)] usando solo *condensadores*... sin ninguna bobina?", "SOLO *CONDENSADORES*",
    A("🫙", "condensadores + interruptores", "BOMBA DE CARGA")),
  S("el truco", "Primero cargas un condensador a la tensión de entrada... y luego lo *apilas* encima de ella. Resultado: el *doble.*", "EL *DOBLE*",
    B("2 · Vin", "un condensador apilado sobre la entrada"), 1),
  S("en un chip", "Los interruptores son transistores... y como no hay bobinas, todo cabe dentro de un *chip.*", "CABE EN UN *CHIP*",
    F(("🔘", "Interruptores", "TRANSISTORES", None, "transistores..."), ("🧩", "Sin bobinas", "INTEGRABLE", True, "chip.")), 2),
  S("versátil", "Puede subir, bajar o invertir la tensión [(voltaje)]... según cómo conecte los *condensadores.*", "*VERSÁTIL*",
    A("🔀", "es un convertidor conmutado", "SUBE, BAJA O INVIERTE"), 2),
  S("la pérdida", "Y un detalle curioso: al conectar dos condensadores a distinta tensión, siempre se pierde energía... y no depende de la *resistencia.*", "LA *PÉRDIDA*",
    F(("📦", "Depende de", "CAPACIDADES Y TENSIONES", None, "energía..."), ("🚫", "No depende de", "LA RESISTENCIA", True, "resistencia.")), 3),
  S(R, "Así que ya sabes. Solo condensadores e interruptores... y por eso caben en un *chip.*", RT,
    F(("🫙", "Bomba de carga", "SIN BOBINAS", None, "interruptores..."), ("🧩", "Por eso", "CABE EN UN CHIP", True, "chip."))),
 ]})

V.append({"id": "cesa-inversores", "titulo": "De continua a alterna",
 "texto": "Onda cuadrada, bipolar y unipolar", "examen": "MQ", "tema": "CESA · Inversores", "etiqueta": "inversores",
 "pron": {},
 "segmentos": [
  S(C, "¿Sabías que para sacar un enchufe de casa de una batería... hay que *trocear* la continua?", "*TROCEAR*",
    A("🔋", "de continua a alterna", "INVERSOR")),
  S("onda cuadrada", "Lo más simple es la onda *cuadrada:* los transistores cambian una vez por semiciclo... pero sale muy *distorsionada.*", "ONDA *CUADRADA*",
    F(("🐢", "Onda cuadrada", "CONMUTA LENTO", None, "cuadrada:"), ("〰️", "Salida", "MUCHA DISTORSIÓN", True, "distorsionada.")), 1),
  S("bipolar", "Para una senoide limpia se conmuta muy rápido. Con control *bipolar,* la entrada del filtro salta de un extremo al *otro.*", "*BIPOLAR*",
    B("+Vin → −Vin", "salta de un extremo al otro"), 2),
  S("unipolar", "Con control *unipolar,* solo va a un lado y a cero. Saltos más pequeños... y un filtro más *pequeño.*", "*UNIPOLAR*",
    F(("↕️", "Bipolar", "FILTRO GRANDE", None, "unipolar,"), ("↗️", "Unipolar", "FILTRO PEQUEÑO", True, "pequeño.")), 2),
  S("el puente", "En el puente, los transistores se encienden por *diagonales*... nunca los dos del mismo lado: sería un *cortocircuito.*", "POR *DIAGONALES*",
    A("✖️", "nunca los dos del mismo lado", "POR DIAGONALES", "¡OJO!"), 3),
  S(R, "Así que ya sabes. Cuadrada, lenta y sucia... y unipolar, con el filtro más *pequeño.*", RT,
    F(("🐢", "Onda cuadrada", "LENTA Y DISTORSIONADA", None, "sucia..."), ("↗️", "Unipolar", "FILTRO PEQUEÑO", True, "pequeño."))),
 ]})

if __name__ == "__main__":
    d = os.path.dirname(os.path.abspath(__file__))
    for v in V:
        with open(os.path.join(d, v["id"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=False, indent=1)
    print(len(V), "specs;", sum(len(s["sub"]) for v in V for s in v["segmentos"]), "caracteres de guion")
