"""TikToks del control de laboratorio de CESA (prácticas 1-3). Voz Dan Dan.
Aperturas y cierres VARIADOS (no siempre "¿Sabías que...?" / "Así que ya sabes").
Uso: python3 generar_specs_lab.py → specs/lab/*.json"""
import json, os

def A(icono, l1, l2, stamp=None):
    v = {"tipo": "alerta", "icono": icono, "linea1": l1, "linea2": l2}
    if stamp: v["stamp"] = stamp
    return v

def F(*filas, stamp=None):
    v = {"tipo": "filas", "filas": []}
    for f in filas:
        d = dict(zip(("icono", "izq", "der", "rojo", "en"), f))
        if not d.get("rojo"): d.pop("rojo", None)
        if not d.get("en"): d.pop("en", None)
        v["filas"].append(d)
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

P1, P2, P3 = "P1 Dimmer", "P2 Fuente de alimentación", "P3 Baterías"
COM = {"AO": "a o", "LED": "led", "LEDs": "leds", "BJT": "be jota te", "NPN": "ene pe ene", "PNP": "pe ene pe",
       "PWM": "pe uve doble eme", "MOSFET": "mos fet", "NMOS": "ene mos", "PMOS": "pe mos", "LM317": "ele eme tres uno siete",
       "TL431": "te ele cuatro tres uno", "LP2951": "ele pe dos nueve cinco uno", "LDO": "ele de o", "TIP122": "tip ciento veintidós",
       "OCP": "o ce pe", "Vref": "uve ref", "Vo": "uve o", "Vcc": "uve ce ce", "VTH": "uve te hache", "VTL": "uve te ele",
       "Rs": "erre ese", "RC": "erre ce", "Buck": "bak", "D": "de", "MCC": "eme ce ce", "PT1000": "pe te mil",
       "DFR0205": "de efe erre cero dos cero cinco", "CC/CV": "ce ce, ce uve", "dropout": "drop aut", "pull-up": "pul ap",
       "push-pull": "push pul", "Zener": "séner", "HiZ": "hai zeta"}
V = []

def vid(id, practica, titulo, texto, etiqueta, segs, pron=None):
    p = dict(COM); p.update(pron or {})
    V.append({"id": "cesa-lab-" + id, "titulo": titulo, "texto": texto, "tema": "CESA · " + practica,
              "examen": "Control lab", "etiqueta": etiqueta, "pron": p, "segmentos": segs})

# =========================== P1 · DIMMER ===========================
vid("led-resistencia", P1, "Por qué un LED necesita su resistencia", "Una curva que se dispara", "LED", [
  S("el problema", "Conecta un LED directamente a una fuente... y en segundos puede estar *muerto.*", "UN LED *SOLO*", A("💡", "LED directo a la fuente", "PELIGRO")),
  S("la curva", "Su corriente [(intensidad)] crece de forma *exponencial* con la tensión [(voltaje)]. Un pelín más de tensión... y la corriente se *dispara.*", "CURVA *EXPONENCIAL*",
    A("📈", "un poco más de tensión", "MUCHA MÁS CORRIENTE"), 1),
  S("el calor", "Y con el calor, su tensión umbral *baja.* A la misma tensión... todavía más *corriente.*", "LA DERIVA *TÉRMICA*",
    A("🌡️", "se calienta → baja su umbral", "MÁS CORRIENTE"), 2),
  S("la solución", "Por eso se le pone una resistencia en *serie:* si la corriente sube, la resistencia se come la tensión que *sobra.*", "RESISTENCIA EN *SERIE*",
    A("🛡️", "Rs en serie", "FRENA LA CORRIENTE"), 3),
  S("cuanto más", "Y cuanto *mayor* es esa resistencia... *menos* varía la corriente con la temperatura.", "MÁS Rs, *MÁS ESTABLE*",
    F(("⬆️", "Más resistencia", "MENOS DERIVA", True, "mayor"), ("⬇️", "Menos resistencia", "MÁS DERIVA", None, None)), 3),
  S("la clave", "La clave: un LED se controla por *corriente,* nunca por tensión.", "LA *CLAVE*",
    B("CONTROLA LA CORRIENTE", "nunca la tensión de un LED")),
])

vid("bjt-tres-zonas", P1, "Las tres caras de un transistor", "Corte, activa y saturación", "transistores", [
  S("tres modos", "Un transistor bipolar puede ser tres cosas distintas: un *interruptor abierto,* un *grifo,* o un interruptor *cerrado.*", "TRES *CARAS*",
    F(("🚪", "Corte", "ABIERTO", None, "abierto,"), ("🚰", "Activa directa", "GRIFO", True, "grifo,"), ("🔌", "Saturación", "CERRADO", None, "cerrado."))),
  S("corte", "En *corte,* no entra corriente [(intensidad)] por la base... y entre colector y emisor no pasa *nada.*", "*CORTE*",
    A("🚪", "Ib = 0 → Ic = 0", "CIRCUITO ABIERTO"), 1),
  S("activa", "En activa *directa,* la corriente de colector es beta veces la de base. Es una fuente de corriente controlada.", "ACTIVA *DIRECTA*",
    B("Ic = beta · Ib", "y Vce > Vce sat"), 2),
  S("saturación", "En *saturación,* el transistor ya no puede más: entre colector y emisor queda una tensión [(voltaje)] *mínima.*", "*SATURACIÓN*",
    A("🔌", "Ic < beta · Ib", "Vce = Vce SAT"), 3),
  S("cómo saberlo", "Truco para saber dónde está: supón activa, calcula la tensión colector emisor... y si sale menor que la de saturación, estaba *saturado.*", "EL *TRUCO*",
    A("🔍", "supón activa y calcula Vce", "SI Vce < Vce SAT → SATURADO"), 4),
  S("quédate con esto", "Corte: nada. Activa: beta por la base. Saturación: tensión *mínima.*", "QUÉDATE CON *ESTO*",
    F(("🚪", "Corte", "Ic = 0", None, "nada."), ("🚰", "Activa", "Ic = beta · Ib", None, "base."), ("🔌", "Saturación", "Vce = Vce SAT", True, "mínima."))),
], pron={"Ic": "i ce", "Ib": "i be", "Vce": "uve ce e"})

vid("npn-o-pnp", P1, "NPN o PNP: dónde va cada uno", "Arriba o abajo de la carga", "transistores", [
  S("mismo dibujo", "El NPN y el PNP son el mismo dibujo... con los *signos* cambiados.", "EL MISMO *DIBUJO*", A("🔄", "mismas zonas, mismas fórmulas", "SIGNOS AL REVÉS")),
  S("el NPN", "El NPN quiere el emisor *abajo,* pegado a masa. Para encenderlo... *subes* la base.", "EL *NPN*",
    F(("⬇️", "Emisor", "A MASA", None, "abajo,"), ("⬆️", "Para encender", "SUBE LA BASE", True, "subes")), 1),
  S("el PNP", "El PNP quiere el emisor *arriba,* pegado a la alimentación. Para encenderlo... *bajas* la base.", "EL *PNP*",
    F(("⬆️", "Emisor", "A LA ALIMENTACIÓN", None, "arriba,"), ("⬇️", "Para encender", "BAJA LA BASE", True, "bajas")), 2),
  S("la carga", "Por eso el NPN va *debajo* de la carga... y el PNP, *encima.*", "¿DÓNDE *VA?*",
    F(("⬇️", "NPN", "DEBAJO DE LA CARGA", None, "debajo"), ("⬆️", "PNP", "ENCIMA DE LA CARGA", True, "encima.")), 3),
  S("la flecha", "Y la flecha del emisor lo dice: en el PNP *apunta* hacia la base. En el NPN, sale hacia *fuera.*", "LA *FLECHA*",
    A("➡️", "PNP: aPunta a la base", "NPN: No apunta"), 4),
  S("la regla", "Emisor abajo, NPN. Emisor arriba, *PNP.*", "LA *REGLA*", B("NPN ABAJO · PNP ARRIBA", "el emisor manda")),
])

vid("darlington", P1, "Dos transistores que parecen uno", "El Darlington del dimmer", "transistores", [
  S("dentro", "El TIP122 parece un transistor normal... pero dentro lleva *dos.*", "DOS EN *UNO*", A("🪆", "TIP122", "DARLINGTON")),
  S("cómo", "El primero amplifica la corriente [(intensidad)] de base... y se la pasa como base al *segundo.*", "EN *CADENA*",
    A("🔗", "la salida del 1 es la base del 2", "AMPLIFICA DOS VECES"), 1),
  S("la ganancia", "Así que las ganancias se *multiplican.* Mil por tres... *tres mil.*", "SE *MULTIPLICAN*",
    B("beta = beta1 · beta2", "por eso supera 1000"), 2),
  S("el precio", "El precio: hay *dos* uniones base emisor en serie. Su tensión [(voltaje)] de base es de un voltio, no cero coma *siete.*", "EL *PRECIO*",
    F(("⚡", "Vbe", "≈ 1 V", True, "siete."), ("🔌", "Vce de saturación", "MÁS ALTA", None, None)), 3),
  S("lo bueno", "Lo bueno: con una corriente de base diminuta, del potenciómetro... mueves la corriente enorme del *LED.*", "LO *BUENO*",
    A("🎛️", "microamperios en la base", "CIENTOS DE mA EN EL LED"), 4),
  S("en una frase", "Darlington: dos transistores, ganancias *multiplicadas*... y un voltio de base.", "EN UNA *FRASE*", B("beta1 · beta2", "y Vbe ≈ 1 V")),
], pron={"Vbe": "uve be e"})

vid("avalancha-termica", P1, "El transistor que se calienta solo", "Avalancha térmica", "transistores", [
  S("en el lab", "Pones el dimmer a media luz... esperas un rato... y el LED se va *encendiendo* solo.", "SE ENCIENDE *SOLO*", A("💡", "potenciómetro quieto", "LA CORRIENTE SUBE")),
  S("por qué", "La culpa es de *beta:* la ganancia del transistor sube con la *temperatura.*", "LA CULPA: *BETA*",
    A("🌡️", "más temperatura", "MÁS GANANCIA"), 1),
  S("el círculo", "Más ganancia, más corriente [(intensidad)]... más calor... y más ganancia otra vez. Un círculo *vicioso.*", "CÍRCULO *VICIOSO*",
    F(("⬆️", "Más ganancia", "MÁS CORRIENTE", None, None), ("🔥", "Más corriente", "MÁS CALOR", True, "vicioso.")), 2),
  S("final", "Hasta que el transistor acaba *saturado,* con la corriente al máximo.", "ACABA *SATURADO*", A("🔚", "final del círculo", "SATURACIÓN"), 2),
  S("la solución", "La solución: *realimentar.* Un amplificador operacional mide la corriente y corrige la base él solo.", "*REALIMENTAR*",
    A("🎛️", "el AO mide y corrige", "CORRIENTE ESTABLE"), 3),
  S("para recordar", "Sin realimentar, depende de beta y se *dispara.* Con el AO... queda *fija.*", "PARA *RECORDAR*",
    F(("🔥", "Sin AO", "INESTABLE", None, "dispara."), ("✅", "Con AO", "ESTABLE", True, "fija."))),
])

vid("cortocircuito-virtual", P1, "El truco del amplificador operacional", "Cortocircuito virtual", "AO", [
  S("la idea", "Un amplificador operacional con realimentación *negativa* hace todo lo posible para que sus dos entradas valgan *igual.*", "EL *TRUCO*",
    A("⚖️", "realimentación negativa", "V+ = V−")),
  S("el dimmer", "En el dimmer, la entrada más va al potenciómetro... y la menos, a la resistencia por donde pasa el *LED.*", "EN EL *DIMMER*",
    F(("🎛️", "Entrada +", "POTENCIÓMETRO", None, "potenciómetro..."), ("💡", "Entrada −", "RESISTENCIA DEL LED", True, "LED.")), 1),
  S("resultado", "Así que esa resistencia tiene la tensión [(voltaje)] del potenciómetro... y la corriente sale de una *división.*", "UNA *DIVISIÓN*",
    B("I LED = V pot / R", "ni beta ni Vbe"), 2),
  S("lo mejor", "Lo mejor: ya no depende ni de beta ni de la tensión base emisor. Aunque el transistor se caliente... la corriente no se *mueve.*", "NO SE *MUEVE*",
    A("🧊", "da igual la temperatura", "CORRIENTE FIJA"), 3),
  S("el límite", "Pero ojo: solo vale si el AO *no* está saturado. Si su salida toca el techo... se acabó el *truco.*", "EL *LÍMITE*",
    A("⚠️", "AO saturado", "NO HAY CORTOCIRCUITO VIRTUAL", "¡OJO!"), 4),
  S("resumen", "Realimentación negativa y AO sin saturar: entradas *iguales.*", "*RESUMEN*", B("V+ = V−", "solo en zona lineal")),
])

vid("lineal-o-conmutacion", P1, "Por qué el transistor quema en lineal", "Y no en conmutación", "conmutación", [
  S("dato", "En el dimmer lineal, el transistor se pone tan caliente que *quema* al tocarlo. Y el LED ni se *inmuta.*", "*QUEMA*",
    A("🔥", "dimmer lineal", "TRANSISTOR HIRVIENDO")),
  S("por qué", "En activa directa, el transistor tiene tensión [(voltaje)] *y* corriente [(intensidad)] a la vez. Su potencia es el *producto.*", "TENSIÓN *Y* CORRIENTE",
    B("P = Vce · Ic", "en activa directa"), 1),
  S("interruptor", "Un interruptor ideal no tiene ese problema. Cerrado, tensión *cero.* Abierto, corriente *cero.*", "UN *INTERRUPTOR*",
    F(("🔌", "Cerrado", "V = 0 → P = 0", None, "cero."), ("🚪", "Abierto", "I = 0 → P = 0", True, "cero.")), 2),
  S("conmutación", "Por eso se pasa a *conmutar:* encender y apagar muy rápido. El transistor casi no se *calienta.*", "*CONMUTAR*",
    A("⚡", "ON / OFF muy rápido", "CASI NO SE CALIENTA"), 3),
  S("MOSFET", "Y se usa un *MOSFET* en vez de un bipolar: en conducción tiene menos caída de *tensión.*", "MEJOR *MOSFET*",
    A("🔋", "en conducción", "MENOS CAÍDA QUE UN BIPOLAR"), 4),
  S("la clave", "Lineal: tensión por corriente, mucho *calor.* Conmutación: casi *nada.*", "LA *CLAVE*",
    F(("🔥", "Lineal", "MUCHO CALOR", None, "calor."), ("❄️", "Conmutación", "CASI NADA", True, "nada."))),
], pron={"Vce": "uve ce e", "Ic": "i ce"})

vid("multimetro", P1, "Cómo medir sin romper el multímetro", "Corriente en serie, tensión en paralelo", "instrumentos", [
  S("error típico", "El error más típico del lab: medir corriente [(intensidad)] con las puntas puestas como para *tensión.*", "ERROR *TÍPICO*",
    A("💥", "puntas en paralelo en modo amperios", "FUSIBLE FUNDIDO", "¡OJO!")),
  S("tensión", "La tensión [(voltaje)] se mide en *paralelo:* tocas los dos puntos, sin abrir el circuito. Borne de voltios y común.", "TENSIÓN: *PARALELO*",
    A("🔀", "bornes V y COM", "EN PARALELO"), 1),
  S("corriente", "La corriente se mide en *serie:* hay que *abrir* el circuito y meter el multímetro en medio, para que pase por él.", "CORRIENTE: *SERIE*",
    A("🔗", "bornes A y COM", "EN SERIE"), 2),
  S("por qué", "En modo corriente, el multímetro es casi un *cable.* Si lo pones en paralelo... haces un *cortocircuito.*", "CASI UN *CABLE*",
    F(("🔀", "Voltímetro", "RESISTENCIA ENORME", None, None), ("🔗", "Amperímetro", "RESISTENCIA CASI CERO", True, "cable.")), 3),
  S("ejemplos", "Corriente de base: abres la base y lo metes en *serie.* Tensión colector emisor: tocas colector y *emisor.*", "EN EL *DIMMER*",
    F(("🔗", "Ib", "EN SERIE CON LA BASE", None, "serie."), ("🔀", "Vce", "ENTRE C Y E", True, "emisor.")), 4),
  S("no lo olvides", "Tensión, en *paralelo.* Corriente, en *serie.*", "NO LO *OLVIDES*",
    F(("🔀", "Tensión", "PARALELO", None, "paralelo."), ("🔗", "Corriente", "SERIE", True, "serie."))),
], pron={"Ib": "i be", "Vce": "uve ce e"})

vid("fuente-ocp", P1, "El botón OCP de la fuente", "Limitar o cortar", "instrumentos", [
  S("pregunta", "La fuente del lab tiene un límite de corriente [(intensidad)]. Pero ¿qué hace *exactamente* cuando lo pasas?", "¿QUÉ *HACE?*",
    A("🔋", "límite de corriente", "DEPENDE DEL OCP")),
  S("OCP apagado", "Con el OCP *apagado,* la fuente *limita:* baja la tensión [(voltaje)] lo justo para no pasar del límite. Sigue dando corriente.", "OCP *APAGADO*",
    A("📉", "baja la tensión", "LIMITA LA CORRIENTE"), 1),
  S("OCP encendido", "Con el OCP *encendido,* la fuente *corta:* en cuanto pasas el límite... apaga la salida del todo.", "OCP *ENCENDIDO*",
    A("✂️", "pasa el límite", "APAGA LA SALIDA"), 2),
  S("en el dimmer", "En el dimmer se usa siete voltios con límite de cero coma ocho amperios... y OCP *apagado,* para que *limite.*", "EN EL *DIMMER*",
    B("7 V · 0,8 A", "OCP apagado → limita"), 3),
  S("para recordar", "OCP apagado: *limita.* OCP encendido: *corta.*", "PARA *RECORDAR*",
    F(("📉", "OCP OFF", "LIMITA", None, "limita."), ("✂️", "OCP ON", "CORTA", True, "corta."))),
])

vid("mosfet-interruptor", P1, "El MOSFET como interruptor", "Dónde poner drenador y fuente", "MOSFET", [
  S("dato", "Un MOSFET como interruptor deja pasar corriente [(intensidad)] en los *dos* sentidos... pero solo bloquea en *uno.*", "BLOQUEA EN *UNO*",
    A("↕️", "corriente en los dos sentidos", "BLOQUEA EN UNO")),
  S("por qué", "La culpa es su diodo parásito: aunque lo apagues... si lo pones al revés, la corriente pasa por el *diodo.*", "EL DIODO *PARÁSITO*",
    A("🕵️", "entre drenador y fuente", "NO SE PUEDE APAGAR"), 1),
  S("el NMOS", "Con un NMOS debajo del LED: la fuente a *masa,* el drenador hacia el *LED.* Así el diodo queda en inverso.", "EL *NMOS*",
    F(("⬇️", "Fuente", "A MASA", True, "masa,"), ("💡", "Drenador", "HACIA EL LED", None, "LED.")), 2),
  S("encender", "Y para encenderlo, la tensión [(voltaje)] puerta fuente tiene que pasar su umbral, que en un NMOS es *positivo.*", "EL *UMBRAL*",
    B("Vgs > VTH > 0", "NMOS encendido"), 3),
  S("al revés", "Si cambias drenador y fuente, el diodo conduce siempre... y el LED se queda encendido *pase lo que pase.*", "AL *REVÉS*",
    A("⚠️", "drenador y fuente cambiados", "LED SIEMPRE ENCENDIDO", "¡OJO!"), 4),
  S("la regla", "Pon el MOSFET para que, apagado, su diodo *bloquee.*", "LA *REGLA*", B("DIODO EN INVERSO", "cuando está apagado")),
], pron={"Vgs": "uve ge ese"})

vid("comparador-histeresis", P1, "Un comparador con dos umbrales", "Histéresis", "AO", [
  S("pregunta", "¿Y si un amplificador operacional se realimenta al *revés,* con realimentación positiva?", "AL *REVÉS*",
    A("🔁", "realimentación positiva", "COMPARADOR")),
  S("saturación", "Entonces nunca está en zona lineal: siempre está *saturado,* arriba o abajo. Y aquí *no* vale el cortocircuito virtual.", "SIEMPRE *SATURADO*",
    F(("⬆️", "Saturación +", "SALIDA ARRIBA", None, "arriba"), ("⬇️", "Saturación −", "SALIDA ABAJO", True, "abajo.")), 1),
  S("dos umbrales", "Y como la salida vuelve a la entrada más, cada estado tiene su propio umbral: uno *alto* y otro *bajo.*", "DOS *UMBRALES*",
    F(("⬆️", "Umbral alto", "VTH", None, "alto"), ("⬇️", "Umbral bajo", "VTL", True, "bajo.")), 2),
  S("histéresis", "Eso es la *histéresis:* para cambiar de estado hay que pasar el otro umbral. Así el ruido no lo hace *temblar.*", "*HISTÉRESIS*",
    A("🛡️", "entre los dos umbrales", "NO CAMBIA POR RUIDO"), 3),
  S("cómo verlo", "En el osciloscopio, en modo *XY,* sale un rectángulo: el ciclo de histéresis.", "MODO *XY*",
    A("📺", "entrada en X, salida en Y", "UN RECTÁNGULO"), 4),
  S("idea clave", "Realimentación *positiva:* saturado, sin cortocircuito virtual... y dos *umbrales.*", "IDEA *CLAVE*",
    F(("🔁", "Realimentación +", "SATURADO", None, "virtual..."), ("↕️", "Umbrales", "DOS", True, "umbrales."))),
], pron={"XY": "equis i griega"})

vid("astable-rc", P1, "El oscilador hecho con un condensador", "Astable RC", "AO", [
  S("idea", "Junta un comparador con histéresis y un condensador... y tienes un *oscilador* que no para nunca.", "UN *OSCILADOR*",
    A("🔄", "comparador + RC", "ASTABLE")),
  S("carga", "Con la salida arriba, el condensador se *carga*... hasta tocar el umbral alto. Entonces la salida *salta* abajo.", "SE *CARGA*",
    A("⬆️", "hasta el umbral alto", "LA SALIDA BAJA"), 1),
  S("descarga", "Con la salida abajo, se *descarga*... hasta el umbral bajo. Y vuelta a *empezar.*", "SE *DESCARGA*",
    A("⬇️", "hasta el umbral bajo", "LA SALIDA SUBE"), 1),
  S("el tiempo", "Cada tramo dura erre por ce... por el logaritmo de cuánto le falta al principio, entre cuánto le falta al *final.*", "EL *TIEMPO*",
    B("t = RC · ln((Vsat − Vini)/(Vsat − Vfin))", "carga o descarga hacia Vsat"), 2),
  S("las ondas", "Resultado: una onda *cuadrada* en la salida... y casi un *triángulo* en el condensador.", "LAS *ONDAS*",
    F(("⬜", "Salida del AO", "CUADRADA", None, "cuadrada"), ("🔺", "Condensador", "CASI TRIANGULAR", True, "triángulo")), 3),
  S("quédate con", "Carga hasta el alto, descarga hasta el *bajo*... y el tiempo sale con un *logaritmo.*", "QUÉDATE *CON ESTO*",
    B("RC · ln(...)", "cada tramo del astable")),
], pron={"t": "te", "RC": "erre ce"})

vid("pwm-dimmer", P1, "Cómo un LED parece estar a medias", "Modulación PWM", "PWM", [
  S("truco", "El LED del dimmer en realidad *nunca* está a media luz: se enciende y se apaga *mil* veces por segundo.", "NUNCA A *MEDIAS*",
    A("💡", "on / off muy rápido", "TU OJO VE LA MEDIA")),
  S("cómo", "Un comparador mira la onda *triangular* del oscilador... y la compara con la tensión [(voltaje)] del *potenciómetro.*", "TRIÁNGULO VS *POTENCIÓMETRO*",
    F(("🔺", "Triangular", "OSCILADOR", None, "triangular"), ("🎛️", "Referencia", "POTENCIÓMETRO", True, "potenciómetro.")), 1),
  S("la salida", "Mientras el triángulo está por debajo... salida *alta.* Si está por encima... salida *baja.* Una cuadrada de ancho *ajustable.*", "ANCHO *AJUSTABLE*",
    A("⬜", "misma frecuencia", "CICLO DE TRABAJO VARIABLE"), 2),
  S("la media", "La corriente [(intensidad)] media del LED es el ciclo de trabajo... por la corriente cuando está *encendido.*", "LA *MEDIA*",
    B("I media = D · (Vcc − VLED)/Rs", "D = ciclo de trabajo"), 3),
  S("las ondas", "Al dibujarlas, todo va *sincronizado:* cuando la puerta está alta, el LED conduce. Cuando está baja... *cero.*", "*SINCRONIZADAS*",
    A("📊", "Vg alta → LED encendido", "MISMA BASE DE TIEMPOS"), 4),
  S("en una frase", "PWM: misma frecuencia, ancho *variable*... y el ojo ve la *media.*", "EN UNA *FRASE*",
    F(("⬜", "PWM", "ANCHO VARIABLE", None, "variable..."), ("👁️", "El ojo", "VE LA MEDIA", True, "media."))),
], pron={"VLED": "uve led", "Vg": "uve ge"})

vid("sondas-generador", P1, "Dos trampas del osciloscopio y el generador", "Sondas 10:1 y salida HiZ", "instrumentos", [
  S("trampa uno", "Primera trampa: la sonda en *diez a uno.* Si no la calibras... las ondas cuadradas salen con *picos* o redondeadas.", "TRAMPA *1*",
    A("📺", "sonda 10:1 sin calibrar", "ONDA DEFORMADA")),
  S("por qué", "En diez a uno, la sonda lleva un divisor con un condensador *ajustable.* Hay que ajustarlo hasta ver una cuadrada *perfecta.*", "CALIBRAR",
    A("🪛", "tornillo de la sonda", "CUADRADA PERFECTA"), 1),
  S("uno a uno", "En uno a uno no hace falta: la sonda es casi un *cable,* no hay divisor que *compensar.*", "EN 1:1, *NO*",
    F(("🔟", "10:1", "HAY QUE CALIBRAR", True, None), ("1️⃣", "1:1", "NO HACE FALTA", None, "compensar.")), 2),
  S("trampa dos", "Segunda trampa: el *generador.* Por defecto cree que hay una carga de cincuenta ohmios... y si no la hay, sale el *doble.*", "TRAMPA *2*",
    A("🎛️", "generador en modo 50 Ω", "SALE EL DOBLE", "¡OJO!"), 3),
  S("la solución", "Si lo conectas a un circuito de alta impedancia, como la puerta de un MOSFET, ponlo en *HiZ.* Así sale lo que *marca.*", "PONLO EN *HiZ*",
    A("✅", "carga de alta impedancia", "MODO HiZ"), 4),
  S("recuerda", "Sonda diez a uno, *calibrada.* Generador con circuito, en *HiZ.*", "*RECUERDA*",
    F(("📺", "Sonda 10:1", "CALIBRAR", None, "calibrada."), ("🎛️", "Generador", "HiZ", True, "HiZ."))),
], pron={"10:1": "diez a uno", "1:1": "uno a uno"})

# =========================== P2 · FUENTE ===========================
vid("fuente-cuatro-bloques", P2, "Una fuente de alimentación por dentro", "Cuatro bloques", "fuente lineal", [
  S("de la red", "Del enchufe salen trescientos diez voltios de pico... y tu móvil quiere cinco en *continua.* ¿Cómo se pasa de uno a otro?", "DE 310 A *5 V*",
    A("🔌", "red: senoidal de 310 V de pico", "CARGA: 5 V CONTINUA")),
  S("1 y 2", "Primero un *transformador,* que baja la tensión [(voltaje)]. Luego un *rectificador,* que le da la vuelta a la parte negativa.", "BLOQUES *1 Y 2*",
    F(("🔁", "Transformador", "BAJA LA TENSIÓN", None, "transformador,"), ("〰️", "Rectificador", "SOLO POSITIVA", True, "rectificador,")), 1),
  S("3 y 4", "Después un *filtro* con un condensador, que suaviza el rizado. Y al final el *regulador,* que la deja *fija.*", "BLOQUES *3 Y 4*",
    F(("🔋", "Filtro", "MENOS RIZADO", None, "filtro"), ("🎯", "Regulador", "TENSIÓN FIJA", True, "regulador,")), 2),
  S("regulador", "El regulador mantiene la salida fija aunque cambie la red... o aunque la carga pida *más.*", "EL *REGULADOR*",
    F(("🔌", "Cambia la red", "REGULACIÓN DE LÍNEA", None, None), ("💡", "Cambia la carga", "REGULACIÓN DE CARGA", True, "más.")), 3),
  S("lineal o conmutada", "Si el regulador es lineal: *poco* rizado, pero rendimiento bajo. Si es conmutado... al *revés.*", "LINEAL O *CONMUTADA*",
    F(("✨", "Lineal", "POCO RIZADO", None, "poco"), ("⚡", "Conmutada", "MÁS RENDIMIENTO", True, "revés.")), 4),
  S("de memoria", "Transformador, rectificador, filtro y *regulador.* Y si quieres, un *limitador.*", "DE *MEMORIA*",
    B("TRAFO → RECT → FILTRO → REG", "+ limitador de corriente")),
])

vid("transitorio-arranque", P2, "El primer segundo de una fuente", "El transitorio de arranque", "rectificador", [
  S("el momento", "El momento más duro para los diodos de una fuente no es funcionando... es al *encenderla.*", "AL *ENCENDER*",
    A("⚡", "primer semiciclo", "PEOR MOMENTO")),
  S("por qué", "Al principio el condensador está *vacío.* Para llenarlo de golpe... los diodos dejan pasar un pico de corriente [(intensidad)] *enorme.*", "CONDENSADOR *VACÍO*",
    A("🔋", "se carga de cero", "PICO ENORME"), 1),
  S("luego", "Después ya solo repone lo que pierde entre pico y pico: picos mucho más *pequeños.*", "RÉGIMEN *ESTACIONARIO*",
    F(("🚀", "Arranque", "PICO ENORME", True, None), ("🔁", "Estacionario", "PICOS PEQUEÑOS", None, "pequeños.")), 2),
  S("el diodo", "Por suerte, solo pasa *una* vez. El datasheet lo llama corriente de pico no *repetitiva:* el diodo aguanta más en ese caso.", "SOLO *UNA VEZ*",
    A("📄", "Peak Forward Surge Current", "IFSM"), 3),
  S("cómo verlo", "Para verlo en el osciloscopio: disparo en modo *normal* y captura *única.* Si no, se te escapa.", "CÓMO *VERLO*",
    F(("🎯", "Disparo", "MODO NORMAL", None, "normal"), ("📸", "Captura", "ÚNICA", True, "única.")), 4),
  S("para llevarte", "Al encender, condensador vacío... y el pico más *grande* de todos.", "PARA *LLEVARTE*",
    B("ARRANQUE = PICO MÁXIMO", "una sola vez → IFSM")),
], pron={"IFSM": "i efe ese eme"})

vid("diodo-zener", P2, "El diodo que trabaja al revés", "Zener como referencia", "referencia", [
  S("al revés", "Un diodo normal no quiere trabajar en inverso. El *Zener,* en cambio, está hecho *para* eso.", "AL *REVÉS*",
    A("🔻", "diodo Zener", "TRABAJA EN RUPTURA")),
  S("la ruptura", "En inverso, al llegar a su tensión [(voltaje)] Zener... la corriente [(intensidad)] se dispara, pero la tensión casi *no* cambia.", "LA *RUPTURA*",
    A("📏", "pasa mucha o poca corriente", "TENSIÓN CASI FIJA"), 1),
  S("referencia", "Por eso sirve de *referencia:* con una resistencia en serie, su tensión casi no depende de la alimentación.", "UNA *REFERENCIA*",
    A("🎯", "Zener + resistencia en serie", "TENSIÓN DE REFERENCIA"), 2),
  S("el defecto", "Su defecto: la *temperatura.* Su tensión se mueve decenas de milivoltios por grado.", "EL *DEFECTO*",
    A("🌡️", "decenas de mV por grado", "DERIVA TÉRMICA", "¡OJO!"), 3),
  S("la mejora", "Por eso existen Zener *compensados,* y reguladores *shunt* como el TL431, que ya lo traen todo dentro.", "LA *MEJORA*",
    F(("🧊", "Zener compensado", "MENOS DERIVA", None, "compensados,"), ("🧩", "TL431", "SHUNT INTEGRADO", True, "dentro.")), 4),
  S("idea", "El Zener trabaja en *ruptura*... y ahí la tensión casi no se *mueve.*", "LA *IDEA*", B("RUPTURA = TENSIÓN FIJA", "por eso es referencia")),
])

vid("tl431", P2, "El TL431, una referencia de 2,5 voltios", "Y sus dos límites de corriente", "referencia", [
  S("presentación", "El TL431 es como un Zener *ajustable:* siempre compara con dos coma cinco voltios.", "SIEMPRE *2,5 V*",
    A("🎯", "referencia interna", "2,5 V")),
  S("ajustar", "Con un divisor de dos resistencias eliges la salida: dos coma cinco por uno más la de arriba entre la de *abajo.*", "LA *SALIDA*",
    B("Vo = 2,5 · (1 + Rarriba/Rabajo)", "para 3 V: Rarriba/Rabajo = 0,2"), 1),
  S("mínimo", "Pero necesita una corriente [(intensidad)] *mínima,* unos cero coma cuatro miliamperios. Por debajo... deja de *regular.*", "UN *MÍNIMO*",
    A("⬇️", "menos de 0,4 mA", "NO REGULA"), 2),
  S("máximo", "Y tiene un *máximo,* ciento cincuenta miliamperios. Por encima... se *calienta* demasiado.", "UN *MÁXIMO*",
    A("🔥", "más de 150 mA", "SE CALIENTA"), 2),
  S("el límite", "Por eso solo no puede alimentar una carga que varíe *más* que esa diferencia. Para eso hace falta un *transistor.*", "SU *LÍMITE*",
    A("🔌", "cargas que varían mucho", "AÑADIR UN TRANSISTOR"), 3),
  S("la resistencia", "La resistencia de entrada se elige con el *peor* caso: que llegue el mínimo con poca entrada... y no pase del máximo con mucha.", "EL *PEOR* CASO",
    F(("⬇️", "Entrada mínima, carga máxima", "≥ 0,4 mA", None, None), ("⬆️", "Entrada máxima, carga mínima", "≤ 150 mA", True, "mucha.")), 4),
  S("no olvides", "TL431: dos coma cinco voltios... y siempre entre su *mínimo* y su *máximo.*", "NO *OLVIDES*",
    B("2,5 V · 0,4–150 mA", "TL431")),
], pron={"Vo": "uve o"})

vid("nmos-o-pmos-regulador", P2, "NMOS o PMOS para regular", "Dropout y control", "regulador discreto", [
  S("dilema", "Para el transistor de una fuente lineal hay dos opciones... y cada una gana en *una* cosa.", "EL *DILEMA*",
    A("⚖️", "transistor de paso", "NMOS O PMOS")),
  S("NMOS", "Con un NMOS, la salida sigue a la puerta: la salida es la puerta *menos* su tensión [(voltaje)] puerta fuente. Muy fácil de *controlar.*", "EL *NMOS*",
    B("Vo = Vg − Vgs", "seguidor: fácil de controlar"), 1),
  S("su problema", "Pero la puerta tiene que estar *por encima* de la salida, unos voltios. Y eso dispara el dropout.", "SU *PROBLEMA*",
    A("📏", "puerta por encima de la salida", "DROPOUT GRANDE"), 2),
  S("PMOS", "Con un PMOS, la fuente va a la *entrada.* Para encenderlo bajas la puerta... y la salida puede quedar casi pegada a la *entrada.*", "EL *PMOS*",
    A("🤏", "fuente en la entrada", "DROPOUT PEQUEÑO"), 3),
  S("conclusión", "Por eso los LDO usan *PMOS.* Y si no te importa el dropout... el NMOS es más *estable.*", "*CONCLUSIÓN*",
    F(("🤏", "LDO", "PMOS", True, "PMOS."), ("🎛️", "Fácil de controlar", "NMOS", None, "estable.")), 4),
  S("la regla", "NMOS, fácil de *controlar.* PMOS, poco *dropout.*", "LA *REGLA*",
    F(("🎛️", "NMOS", "CONTROL FÁCIL", None, "controlar."), ("🤏", "PMOS", "LDO", True, "dropout."))),
], pron={"Vg": "uve ge", "Vgs": "uve ge ese"})

vid("dropout-discreto", P2, "Por qué tu fuente necesita tanto margen", "El dropout del regulador discreto", "regulador discreto", [
  S("pregunta", "¿Por qué la fuente del lab necesita *varios* voltios más en la entrada que en la salida?", "TANTO *MARGEN*",
    A("📏", "entrada − salida", "DROPOUT")),
  S("qué es", "El *dropout* es la diferencia mínima entre entrada y salida para que el regulador siga *regulando.*", "EL *DROPOUT*",
    A("🛏️", "diferencia mínima", "PARA SEGUIR REGULANDO"), 1),
  S("primer culpable", "Primer culpable: el AO. Su salida no llega arriba del todo: se queda *uno coma cinco* voltios por debajo de su alimentación.", "CULPABLE *1*",
    B("Vcc − 1,5 V", "máximo a la salida del LM324"), 2),
  S("segundo", "Segundo culpable: el NMOS necesita que la puerta esté unos *cuatro* voltios por encima de la *salida.*", "CULPABLE *2*",
    B("Vgs ≈ 4 V", "para dar la corriente de la carga"), 2),
  S("la suma", "Súmalos: uno coma cinco más cuatro... cinco coma cinco voltios de *dropout.*", "LA *SUMA*",
    B("1,5 + 4 = 5,5 V", "dropout del regulador discreto"), 3),
  S("clave", "Dropout: lo que pierde el AO... más lo que necesita la *puerta.*", "LA *CLAVE*",
    F(("🎛️", "AO", "− 1,5 V", None, "AO..."), ("🔌", "Puerta", "+ Vgs", True, "puerta."))),
], pron={"LM324": "ele eme tres dos cuatro", "Vgs": "uve ge ese"})

vid("condensadores-utiles", P2, "Condensadores que parecen inútiles", "Pero sin ellos oscila", "regulador discreto", [
  S("paradoja", "En continua, un condensador es un circuito *abierto.* Entonces, ¿para qué ponerlo a la salida de un regulador?", "¿PARA *QUÉ?*",
    A("🤔", "en continua es un abierto", "¿INÚTIL?")),
  S("cambios", "Porque la carga cambia de golpe... y el condensador da la corriente [(intensidad)] mientras el lazo *reacciona.*", "LOS *CAMBIOS*",
    A("⚡", "cambio brusco de carga", "EL CONDENSADOR RESPONDE"), 1),
  S("estabilidad", "Y lo más importante: estabiliza el *lazo* de control. Sin él, el regulador puede ponerse a *oscilar.*", "*ESTABILIDAD*",
    A("〰️", "sin condensador", "PUEDE OSCILAR", "¡OJO!"), 2),
  S("en el lab", "En la práctica de baterías se ve: quitas el condensador del LDO... y la salida se pone a *bailar.*", "EN EL *LAB*",
    F(("✅", "Con condensador", "SALIDA FIJA", None, None), ("〰️", "Sin condensador", "OSCILA", True, "bailar.")), 3),
  S("ruido", "Además filtran ruido y picos rápidos que el regulador es demasiado *lento* para corregir.", "EL *RUIDO*",
    A("🔇", "picos rápidos", "LOS FILTRA"), 4),
  S("resumen", "No están por la continua: están por los *cambios*... y para que el lazo no *oscile.*", "*RESUMEN*",
    F(("⚡", "Cambios bruscos", "LOS CUBRE", None, "cambios..."), ("🎛️", "Lazo de control", "NO OSCILA", True, "oscile."))),
])

vid("limitador-corriente", P2, "El transistor que protege tu fuente", "Limitador de corriente", "protección", [
  S("situación", "Si alguien cortocircuita la salida de tu fuente... sin protección, algo se *quema.*", "UN *CORTOCIRCUITO*",
    A("💥", "salida en cortocircuito", "SIN LIMITADOR SE QUEMA")),
  S("el sensor", "El truco: una resistencia pequeña en serie con la carga. Su tensión [(voltaje)] va entre base y emisor de un *transistor.*", "EL *SENSOR*",
    A("📏", "Rs en serie con la carga", "V = Rs · I"), 1),
  S("normal", "Con poca corriente, esa tensión no llega a cero coma siete: el transistor está en *corte* y no hace *nada.*", "TODO *NORMAL*",
    A("😴", "menos de 0,7 V", "TRANSISTOR EN CORTE"), 2),
  S("se pasa", "Si la corriente sube, el transistor *conduce,* le roba tensión a la puerta del MOSFET... y la salida *baja.*", "SE *PASA*",
    A("🛑", "más de 0,7 V", "BAJA LA PUERTA"), 3),
  S("el límite", "Así que la corriente máxima es cero coma siete entre esa *resistencia.*", "EL *LÍMITE*",
    B("I máx = 0,7 / Rs", "límite del limitador"), 3),
  S("el AO", "Y ojo: cuando limita, el AO intenta compensar y acaba *saturado.* Ahí ya no vale el cortocircuito *virtual.*", "EL AO *SATURA*",
    A("⚠️", "cuando limita", "AO SATURADO", "¡OJO!"), 4),
  S("la fórmula", "Corriente máxima: cero coma siete entre la resistencia de *sensado.*", "LA *FÓRMULA*", B("0,7 V / Rs", "y el AO saturado al limitar")),
])

vid("tres-reguladores-autonomia", P3, "Tres reguladores, tres autonomías", "LM317, LP2951 y Buck", "reguladores", [
  S("carrera", "Misma batería, misma carga, tres reguladores distintos. ¿Cuál aguanta *más?*", "LA *CARRERA*",
    F(("1️⃣", "LM317", "LINEAL", None, None), ("2️⃣", "LP2951", "LDO", None, None), ("3️⃣", "DFR0205", "BUCK", True, None))),
  S("LM317", "El *LM317* pierde por dos lados: quema lo que sobra... y necesita un dropout *grande,* así que deja de regular pronto.", "ÚLTIMO: *LM317*",
    A("🥉", "rendimiento bajo + dropout grande", "MENOS AUTONOMÍA"), 1),
  S("LDO", "El *LP2951* también quema lo que sobra... pero su dropout es *pequeñito:* aprovecha la batería casi hasta el final.", "SEGUNDO: *LDO*",
    A("🥈", "dropout pequeño", "APROVECHA MÁS LA BATERÍA"), 2),
  S("Buck", "El *Buck* gana: es conmutado, no quema lo que sobra. Su rendimiento es *alto,* y pide menos corriente [(intensidad)] a la batería.", "GANADOR: *BUCK*",
    A("🥇", "conmutado", "MÁS RENDIMIENTO"), 3),
  S("el precio", "Eso sí, el Buck tiene más *rizado* en la salida. Los lineales dan una salida más *limpia.*", "EL *PRECIO*",
    F(("〰️", "Buck", "MÁS RIZADO", True, "rizado"), ("✨", "Lineales", "SALIDA LIMPIA", None, "limpia.")), 4),
  S("el podio", "Buck, LDO... y el LM317, el *último.*", "EL *PODIO*", B("BUCK > LDO > LM317", "en autonomía")),
])

vid("rendimiento-lineal", P3, "Cuánto desperdicia un regulador lineal", "Rendimiento con batería", "reguladores", [
  S("cuenta rápida", "Batería de siete coma dos voltios, salida de cinco con un regulador lineal. ¿Cuánta energía se *pierde?*", "CUENTA *RÁPIDA*",
    A("🔋", "7,2 V → 5 V", "¿CUÁNTO SE PIERDE?")),
  S("la clave", "En un lineal, entra casi la *misma* corriente [(intensidad)] que sale. Así que el rendimiento es salida entre *entrada.*", "LA *CLAVE*",
    B("REND ≈ Vo / Vin", "misma corriente dentro y fuera"), 1),
  S("la cuenta", "Cinco entre siete coma dos... un sesenta y nueve por ciento. Casi un tercio se va en *calor.*", "LA *CUENTA*",
    B("5 / 7,2 ≈ 69 %", "un 31 % se convierte en calor"), 2),
  S("con más detalle", "Si quieres afinar, súmale la corriente de las resistencias del ajuste a la de *entrada:* el rendimiento baja un *poquito.*", "MÁS *FINO*",
    B("Vo·Io / (Vin·(Io + I R2))", "la corriente del divisor también cuenta"), 3),
  S("conclusión", "Cuanto más alta la batería respecto a la salida... *peor* rendimiento.", "CONCLUSIÓN",
    A("📉", "más diferencia entrada − salida", "PEOR RENDIMIENTO"), 4),
  S("de cabeza", "Lineal: salida entre *entrada.* Así de fácil.", "DE *CABEZA*", B("Vo / Vin", "rendimiento de un lineal")),
], pron={"η": "eta", "Vin": "uve in", "Io": "i o", "R2": "erre dos"})

vid("autonomia-dropout", P3, "Cuándo se acaba una batería de verdad", "Autonomía y dropout", "autonomía", [
  S("sorpresa", "Tu aparato se apaga... y la batería todavía tiene *carga.* No es un fallo: es el *dropout.*", "AÚN TIENE *CARGA*",
    A("🪫", "el aparato se apaga", "LA BATERÍA NO ESTÁ VACÍA")),
  S("la condición", "El regulador necesita que la batería esté por encima de la salida... *más* su dropout.", "LA *CONDICIÓN*",
    B("VB ≥ Vo + Vdropout", "para seguir regulando"), 1),
  S("el final", "Mientras la batería se descarga, su tensión [(voltaje)] *baja.* Cuando cruza ese límite... la salida deja de estar *regulada.*", "EL *FINAL*",
    A("📉", "VB < Vo + dropout", "FIN DE LA AUTONOMÍA"), 2),
  S("cómo calcular", "Para calcular la autonomía: buscas en la curva de descarga *cuándo* la batería llega a ese límite... o la carga útil entre la *corriente.*", "CÓMO *CALCULAR*",
    B("t = Q útil / I", "hasta que VB = Vo + dropout"), 3),
  S("ejemplo", "Con salida de cinco voltios y dropout de dos coma dos... la batería sirve hasta siete coma *dos.*", "*EJEMPLO*",
    B("5 + 2,2 = 7,2 V", "por debajo, no regula"), 4),
  S("idea", "La autonomía acaba cuando la batería baja de salida *más* dropout. Por eso el *LDO* aguanta más.", "LA *IDEA*",
    F(("🛏️", "Dropout grande", "ACABA ANTES", None, None), ("🤏", "LDO", "AGUANTA MÁS", True, "LDO"))),
], pron={"VB": "uve be", "Vdropout": "uve drop aut", "Q": "cu", "t": "te"})

vid("colector-abierto", P3, "Salida en colector abierto", "Y por qué necesita una resistencia", "digital", [
  S("rara", "El LP2951 tiene una salida de *error* un poco rara: solo sabe tirar hacia *abajo.*", "SOLO *TIRA ABAJO*",
    A("⬇️", "salida de error del LP2951", "COLECTOR ABIERTO")),
  S("qué es", "Por dentro es un transistor con el colector *al aire.* Encendido, pone la salida a *masa.* Apagado... la deja *flotando.*", "*COLECTOR ABIERTO*",
    F(("⬇️", "Transistor encendido", "SALIDA A MASA", True, "masa."), ("🎈", "Transistor apagado", "FLOTANDO", None, "flotando.")), 1),
  S("la resistencia", "Por eso necesita una resistencia de *pull-up* hacia la alimentación: cuando está apagado, ella sube la salida a *nivel alto.*", "EL *PULL-UP*",
    A("⬆️", "resistencia a la alimentación", "PULL-UP"), 2),
  S("push-pull", "Una salida *push-pull* lleva dos transistores: uno sube y otro baja. No necesita resistencia... pero *no* se pueden unir dos.", "PUSH-*PULL*",
    F(("↕️", "Push-pull", "SUBE Y BAJA", None, "push-pull"), ("⬇️", "Colector abierto", "SOLO BAJA", True, "baja.")), 3),
  S("en paralelo", "Las de colector abierto sí se pueden unir: si *cualquiera* tira abajo, la línea baja. Un solo LED avisa del error de *todos.*", "EN *PARALELO*",
    A("🔗", "varias salidas unidas", "CUALQUIERA AVISA"), 4),
  S("recuerda", "Colector abierto: solo *baja,* necesita pull-up... y se puede poner en *paralelo.*", "*RECUERDA*",
    F(("⬆️", "Necesita", "PULL-UP", None, "pull-up..."), ("🔗", "Se pueden unir", "SÍ", True, "paralelo."))),
])

vid("lm317-fuente-corriente", P3, "El LM317 como fuente de corriente", "Una sola resistencia", "cargador", [
  S("otro uso", "El LM317 no solo da tensión [(voltaje)] fija... con *una* resistencia también da corriente [(intensidad)] fija.", "OTRO *USO*",
    A("🔋", "LM317 + una resistencia", "CORRIENTE CONSTANTE")),
  S("cómo", "Pones la resistencia entre la salida y el pin de ajuste. El chip le mete *siempre* uno coma veinticinco voltios.", "EL *MONTAJE*",
    A("📌", "R entre OUT y ADJ", "SIEMPRE 1,25 V"), 1),
  S("la corriente", "Así que por ella pasa siempre uno coma veinticinco entre *R*... y esa corriente va directa a la *batería.*", "LA *CORRIENTE*",
    B("I = 1,25 / R", "no depende de la batería"), 2),
  S("ejemplo", "Para doscientos cincuenta miliamperios: uno coma veinticinco entre cero coma veinticinco... *cinco* ohmios.", "*EJEMPLO*",
    B("1,25 / 0,25 = 5 Ω", "y de medio vatio"), 3),
  S("trampa", "No confundas: aquí no hay divisor. La fórmula de uno más R dos entre R uno es para dar *tensión,* no *corriente.*", "LA *TRAMPA*",
    F(("🔋", "Fuente de tensión", "1,25·(1 + R2/R1)", None, "tensión,"), ("➡️", "Fuente de corriente", "1,25 / R", True, "corriente.")), 4),
  S("en una línea", "Fuente de corriente: uno coma veinticinco entre *R.*", "EN UNA *LÍNEA*", B("I = 1,25 / R", "LM317 en modo corriente")),
], pron={"R": "erre", "OUT": "aut", "ADJ": "a de jota", "R2": "erre dos", "R1": "erre uno"})

vid("cargador-cc-cv", P3, "Cómo se carga una batería de litio", "Corriente constante y luego tensión constante", "cargador", [
  S("el método", "Las baterías de litio se cargan en dos fases... y el cargador del lab hace las *dos* con un LM317 y un TL431.", "DOS *FASES*",
    F(("➡️", "Fase 1", "CORRIENTE CONSTANTE", None, None), ("🎯", "Fase 2", "TENSIÓN CONSTANTE", True, "dos"))),
  S("fase uno", "Primero, corriente [(intensidad)] *constante:* el TL431 está apagado... y la tensión [(voltaje)] de la batería va *subiendo.*", "FASE *1*",
    A("📈", "TL431 apagado", "I FIJA · V SUBE"), 1),
  S("el cambio", "Cuando la batería llega al límite, el divisor le da *dos coma cinco* voltios al TL431... y este se *despierta.*", "EL *CAMBIO*",
    B("VB = 2,5 · (1 + R3/R4)", "por ejemplo 8 V"), 2),
  S("fase dos", "Ahora, tensión *constante:* el TL431 ajusta el LM317 para que la batería no pase de ahí. Y la corriente va *bajando* sola.", "FASE *2*",
    A("📉", "TL431 regulando", "V FIJA · I BAJA"), 3),
  S("por qué", "¿Por qué no cargar siempre a corriente constante? Porque al llenarse, la batería se *sobrecarga* y se calienta *peligrosamente.*", "¿POR *QUÉ?*",
    A("🔥", "solo corriente constante", "SOBRECARGA Y CALOR", "¡OJO!"), 4),
  S("dibújalo así", "Corriente plana y tensión subiendo... luego tensión plana y corriente *cayendo.*", "DIBÚJALO *ASÍ*",
    F(("➡️", "Fase CC", "I PLANA · V SUBE", None, "subiendo..."), ("🎯", "Fase CV", "V PLANA · I BAJA", True, "cayendo."))),
], pron={"VB": "uve be", "R3": "erre tres", "R4": "erre cuatro", "CC": "ce ce", "CV": "ce uve"})

vid("pt1000-seguridad", P3, "El termómetro dentro de la batería", "PT1000 y sobrecarga", "cargador", [
  S("riesgo", "Una batería que se *sobrecarga* se calienta... y en el peor caso, puede arder.", "EL *RIESGO*",
    A("🔥", "sobrecarga", "SOBRECALENTAMIENTO")),
  S("el sensor", "Por eso llevan un sensor dentro: una *PT1000.* Es una resistencia de platino que vale mil ohmios a cero grados... y *sube* con el calor.", "LA *PT1000*",
    B("R = 1000 · (1 + 0,00385 · T)", "a 50 °C ≈ 1192 Ω"), 1),
  S("cómo se usa", "Se pone en un divisor: al calentarse, su tensión [(voltaje)] *sube.* Un comparador la mira contra un umbral *fijo.*", "CON UN *COMPARADOR*",
    F(("🌡️", "PT1000", "DIVISOR", None, "sube."), ("🎯", "Umbral", "TL431 + DIVISOR", True, "fijo.")), 2),
  S("acción", "Si pasa del umbral, el comparador abre un *relé* en serie con la batería... y la carga se *para.*", "SE *PARA*",
    A("✂️", "más de 50 °C", "RELÉ ABIERTO"), 3),
  S("redundante", "Y es *redundante:* va por su cuenta, sin tocar el cargador. Si el cargador falla... esto lo sigue *parando.*", "*REDUNDANTE*",
    A("🛡️", "independiente del cargador", "SEGURIDAD EXTRA"), 4),
  S("la idea", "PT1000: resistencia que sube con el *calor*... y un comparador que corta la *carga.*", "LA *IDEA*",
    F(("🌡️", "PT1000", "SUBE CON EL CALOR", None, "calor..."), ("✂️", "Comparador", "CORTA LA CARGA", True, "carga."))),
], pron={"R": "erre", "T": "te"})

vid("emulador-celdas", P3, "Por qué se desequilibran las celdas", "Dos celdas en serie", "baterías", [
  S("en serie", "Dos celdas en serie: por las dos pasa la *misma* corriente [(intensidad)]. Entonces... ¿por qué acaban *distintas?*", "LA MISMA *CORRIENTE*",
    A("🔗", "dos celdas en serie", "¿POR QUÉ SE SEPARAN?")),
  S("diferencias", "Porque no son *gemelas:* una tiene algo más de capacidad, otra pierde un poco más... y cada ciclo se *separan* un poco más.", "NO SON *GEMELAS*",
    F(("🔋", "Capacidad", "DISTINTA", None, "capacidad,"), ("💧", "Pérdidas", "DISTINTAS", True, "más...")), 1),
  S("el problema", "La que llega antes a llena *corta* la carga... y la que llega antes a vacía corta la *descarga.* La batería entera rinde *menos.*", "EL *PROBLEMA*",
    A("📉", "manda la peor celda", "MENOS CARGA ÚTIL"), 2),
  S("el modelo", "En el emulador, cada celda es una fuente de tensión [(voltaje)]... con una resistencia en serie y un grupo erre ce en *paralelo.*", "EL *MODELO*",
    B("Voc + Rs + RC", "el RC en paralelo; todo depende del estado de carga"), 3),
  S("solución", "La solución es *balancear:* igualar las celdas, quemando lo que sobra o *pasándolo* a la otra.", "LA *SOLUCIÓN*",
    A("⚖️", "pasivo o activo", "BALANCEO"), 4),
  S("para recordar", "En serie, manda la celda *peor.* Por eso hay que *balancear.*", "PARA *RECORDAR*",
    F(("🔗", "En serie", "MANDA LA PEOR", None, "peor."), ("⚖️", "Solución", "BALANCEAR", True, "balancear."))),
], pron={"Voc": "uve o ce", "Rs1": "erre ese uno", "Cs1": "ce ese uno"})

# =========================== RESUELTOS (cálculos de los previos) ===========================
vid("iled-bjt-calculo", P1, "La corriente del LED con un transistor", "Fórmula y margen del potenciómetro", "cálculo", [
  S("el circuito", "Siete voltios, un potenciómetro de cien kilos y cuarenta y siete kilos a la base. ¿Cuánta corriente [(intensidad)] pasa por el *LED?*", "EL *CIRCUITO*",
    F(("🔋", "Vcc", "7 V", None, None), ("🎛️", "Potenciómetro", "x · 100 kΩ", None, None), ("🔧", "Rg", "47 kΩ", None, None))),
  S("la base", "La corriente de base es lo que sobra de los siete voltios, quitando la tensión [(voltaje)] base emisor... entre las dos resistencias en *serie.*", "LA *BASE*",
    B("Ib = (Vcc − Vbe) / (x·Rpt + Rg)", "la base va por el potenciómetro y Rg"), 1),
  S("el LED", "Y en activa directa, la del LED es beta veces esa. Así sale la fórmula de la *figura.*", "EL *LED*",
    B("I LED = beta·(Vcc − Vbe)/(x·Rpt + Rg)", "beta = 3000 · Vbe = 1 V"), 2),
  S("los extremos", "Con el potenciómetro a cero: tres mil por seis entre cuarenta y siete mil... unos *trescientos ochenta* miliamperios. Al máximo... unos *ciento veinte.*", "LOS *EXTREMOS*",
    F(("0️⃣", "x = 0", "≈ 383 mA", True, "ochenta"), ("💯", "x = 1", "≈ 122 mA", None, "veinte.")), 3),
  S("el margen", "Para seguir en activa, el LED no puede pasar de unos *quinientos sesenta* miliamperios... y nunca llega. Todo el recorrido está en *activa.*", "EL *MARGEN*",
    B("I LED ≤ (7 − 3,5 − 0,7)/5 Ω = 0,56 A", "siempre por debajo → 0 < x < 1"), 4),
  S("a 300 mA", "Con trescientos miliamperios: cien microamperios de base, *dos* voltios entre colector y emisor... y cero coma *seis* vatios de calor.", "A *300 mA*",
    F(("➡️", "Ib", "0,3 / 3000 = 100 µA", None, "base,"), ("📏", "Vce", "7 − 3,5 − 1,5 = 2 V", None, "voltios"), ("🔥", "Potencia", "2 · 0,3 = 0,6 W", True, "calor.")), 5),
], pron={"Ib": "i be", "Vbe": "uve be e", "Rpt": "erre pe te", "Rg": "erre ge", "x": "equis", "Vce": "uve ce e"})

vid("iled-ao-calculo", P1, "La corriente del LED con el AO", "Ya no depende del transistor", "cálculo", [
  S("la diferencia", "Con el AO, la corriente [(intensidad)] del LED sale de una cuenta *mucho* más fácil que sin él.", "MÁS *FÁCIL*",
    A("🎛️", "transistor + AO", "SIN BETA NI Vbe")),
  S("cortocircuito", "El AO copia en la resistencia de emisor la tensión [(voltaje)] del potenciómetro. La corriente es esa tensión... entre la *resistencia.*", "EL *TRUCO*",
    B("I LED = V CTR / 5 Ω", "Rs1 y Rs2 de 10 Ω en paralelo = 5 Ω"), 1),
  S("la tensión", "El potenciómetro de cien kilos cuelga de tres resistencias de un mega en paralelo. Arriba del todo da unos *uno coma seis* voltios.", "LA *TENSIÓN*",
    B("7 · 100k / (333k + 100k) ≈ 1,6 V", "tensión máxima de control"), 2),
  S("el máximo", "Uno coma seis entre cinco ohmios... unos *trescientos veinte* miliamperios como máximo.", "EL *MÁXIMO*",
    B("1,6 / 5 ≈ 0,32 A", "I LED máxima"), 3),
  S("el límite", "Y para que el AO no se sature, su salida tiene que poder dar la tensión de emisor más la base emisor del Darlington. Si no le llega... *satura.*", "QUE NO *SATURE*",
    B("V salida AO = V CTR + Vbe", "tiene que quedar por debajo de su máximo"), 4),
  S("la regla", "Con AO: corriente igual a la tensión de control entre la resistencia de *emisor.*", "LA *REGLA*", B("I = V CTR / R", "nada de beta")),
], pron={"V": "uve", "CTR": "ce te erre", "Rs1": "erre ese uno", "Rs2": "erre ese dos", "Vbe": "uve be e"})

vid("umbrales-histeresis-calculo", P1, "Calcular los umbrales del comparador", "VTH y VTL con números", "cálculo", [
  S("el montaje", "Salida del AO, una de diez kilos hasta la entrada más... y de ahí, una de cuatro coma siete a *masa.*", "EL *MONTAJE*",
    F(("🔧", "R3", "10 kΩ (a la salida)", None, None), ("🔧", "R2", "4,7 kΩ (a masa)", None, "masa."))),
  S("el divisor", "La entrada más es la salida pasada por un divisor: cuatro coma siete entre catorce coma siete... un *cero coma treinta y dos.*", "EL *DIVISOR*",
    B("V+ = V salida · 4,7 / 14,7", "= 0,32 · V salida"), 1),
  S("abajo", "Con la salida en *menos seis,* el umbral bajo es menos seis por cero coma treinta y dos: menos uno coma *nueve.*", "UMBRAL *BAJO*",
    B("VTL = −6 · 0,32 ≈ −1,9 V", "saturación negativa"), 2),
  S("arriba", "Con la salida en *cinco coma cinco,* el umbral alto: uno coma *siete* y pico.", "UMBRAL *ALTO*",
    B("VTH = 5,5 · 0,32 ≈ 1,76 V", "saturación positiva"), 3),
  S("cuándo cambia", "Mientras está abajo, aguanta hasta que la entrada baje de menos uno coma nueve. Y arriba... hasta que suba de uno coma *siete.*", "CUÁNDO *CAMBIA*",
    F(("⬇️", "Saturación −", "HASTA Vgnr < VTL", None, "nueve."), ("⬆️", "Saturación +", "HASTA Vgnr > VTH", True, "siete.")), 4),
  S("la receta", "Umbral igual a la tensión de saturación por el *divisor.*", "LA *RECETA*", B("V umbral = V sat · R2 / (R2 + R3)", "una vez para cada saturación")),
], pron={"R3": "erre tres", "R2": "erre dos", "V+": "uve más", "Vgnr": "uve ge ene erre"})

vid("astable-tiempos-calculo", P1, "Cuánto dura cada tramo del oscilador", "Con números", "cálculo", [
  S("los datos", "Cuatro coma siete kilos, doscientos nanos, umbrales de uno coma seis y menos uno coma ocho. ¿Cuánto dura cada *tramo?*", "LOS *DATOS*",
    F(("🔧", "R4 · Cc", "4,7 kΩ · 200 nF = 0,94 ms", None, None), ("↕️", "Umbrales", "1,6 V y −1,8 V", True, "tramo?"))),
  S("la fórmula", "El condensador va hacia la saturación. El tiempo: erre ce por el logaritmo de lo que falta al *empezar* entre lo que falta al *acabar.*", "LA *FÓRMULA*",
    B("t = RC · ln((Vsat − Vini)/(Vsat − Vfin))", "va hacia Vsat"), 1),
  S("subida", "Subiendo hacia cinco coma cinco: logaritmo de *siete coma tres* entre *tres coma nueve*... cero coma cincuenta y nueve milisegundos.", "LA *SUBIDA*",
    B("0,94 · ln(7,3 / 3,9) ≈ 0,59 ms", "salida en saturación +"), 2),
  S("bajada", "Bajando hacia menos seis, de uno coma seis a menos uno coma ocho: logaritmo de *siete coma seis* entre *cuatro coma dos.*", "LA *BAJADA*",
    B("0,94 · ln(7,6 / 4,2) ≈ 0,56 ms", "salida en saturación −"), 3),
  S("periodo", "En total, un periodo de uno coma quince milisegundos... unos *ochocientos setenta* hercios.", "EL *PERIODO*",
    B("0,59 + 0,56 ≈ 1,15 ms", "≈ 870 Hz"), 4),
  S("el truco", "El truco: distancia hasta la saturación al empezar... entre la distancia al *acabar.*", "EL *TRUCO*", B("ln(distancia inicio / distancia final)", "siempre medido hasta Vsat")),
], pron={"R4": "erre cuatro", "Cc": "ce ce", "Vsat": "uve sat", "Vini": "uve ini", "Vfin": "uve fin"})

vid("nmos-pmos-por-dentro", P1, "NMOS y PMOS por dentro", "Y por qué el umbral cambia de signo", "MOSFET", [
  S("dentro", "Un NMOS por dentro es un trozo de silicio *P* con dos islas *N:* el drenador y la fuente. Encima, una capa de óxido... y el metal de la *puerta.*", "EL *NMOS*",
    F(("🟥", "Sustrato", "SILICIO P", None, "P"), ("🟦", "Drenador y fuente", "ISLAS N", None, "N:"), ("⬜", "Puerta", "METAL SOBRE ÓXIDO", True, "puerta."))),
  S("el canal", "Si pones la puerta *positiva,* atrae electrones debajo del óxido... y forma un *canal* N que une las dos islas.", "EL *CANAL*",
    A("➕", "puerta positiva", "CANAL DE ELECTRONES"), 1),
  S("umbral NMOS", "La tensión [(voltaje)] mínima para formar ese canal es el *umbral.* En un NMOS es *positivo.*", "UMBRAL *POSITIVO*",
    B("VTH > 0", "NMOS: hay que atraer electrones"), 2),
  S("el PMOS", "El PMOS es el *espejo:* sustrato N, islas P... y para formar el canal hay que atraer *huecos.* Con puerta *negativa.*", "EL *PMOS*",
    F(("🟦", "Sustrato", "SILICIO N", None, None), ("🟥", "Islas", "P", None, None), ("➖", "Puerta", "NEGATIVA", True, "negativa.")), 3),
  S("umbral PMOS", "Por eso el umbral del PMOS es *negativo.*", "UMBRAL *NEGATIVO*", B("VTH < 0", "PMOS: hay que atraer huecos"), 4),
  S("de memoria", "NMOS, electrones, umbral *positivo.* PMOS, huecos, umbral *negativo.*", "DE *MEMORIA*",
    F(("➕", "NMOS", "VTH > 0", None, "positivo."), ("➖", "PMOS", "VTH < 0", True, "negativo."))),
], pron={"P": "pe", "N": "ene"})

vid("rizado-calculo", P2, "Calcular el rizado de la fuente", "Con números del lab", "cálculo", [
  S("datos", "Secundarios de nueve voltios eficaces, carga de ciento sesenta y cinco ohmios, condensador de cuatrocientos setenta micros. ¿Cuánto *rizado?*", "LOS *DATOS*",
    F(("🔁", "Secundario", "9 V ef → 12,7 V pico", None, None), ("💡", "RL", "330 y 330 en paralelo = 165 Ω", None, None), ("🔋", "C", "470 µF", True, "rizado?"))),
  S("la salida", "La salida llega al pico menos un diodo: doce coma siete menos cero coma siete... *doce* voltios. Y la carga se lleva unos *setenta y tres* miliamperios.", "LA *SALIDA*",
    F(("📈", "Vo", "12,7 − 0,7 = 12 V", None, "voltios."), ("➡️", "io", "12 / 165 ≈ 73 mA", True, "tres")), 1),
  S("la fórmula", "Entre picos, el condensador alimenta solo... durante *medio* periodo, porque es onda completa.", "LA *FÓRMULA*",
    B("ΔVo = io / (2·f·C)", "= Vo / (2·RL·C·f)"), 2),
  S("la cuenta", "Doce entre dos por ciento sesenta y cinco por cuatrocientos setenta micros por cincuenta... *uno coma cinco cinco* voltios.", "LA *CUENTA*",
    B("12 / (2·165·470µ·50) ≈ 1,55 V", "rizado con 470 µF"), 3),
  S("la tabla", "Con cien micros sale siete coma tres, con doscientos veinte, tres coma tres. Doble de condensador... *mitad* de rizado.", "LA *TABLA*",
    F(("1️⃣", "100 µF", "7,3 V", None, None), ("2️⃣", "220 µF", "3,3 V", None, None), ("4️⃣", "470 µF", "1,55 V", True, "rizado.")), 4),
  S("ojo", "Y ojo: la fórmula siempre da algo *más* que lo medido, porque supone que se descarga los diez milisegundos *enteros.*", "*OJO*",
    A("📏", "la fórmula exagera un poco", "MEDIDO < TEÓRICO", "¡OJO!"), 5),
], pron={"RL": "erre ele", "io": "i o", "ΔVo": "delta uve o", "f": "efe", "C": "ce"})

vid("pico-diodos-calculo", P2, "Calcular el pico de corriente de los diodos", "Y la tensión que aguantan", "cálculo", [
  S("la idea", "Cada diodo tiene que devolver en un *instante* toda la carga que el condensador perdió en diez milisegundos.", "LA *IDEA*",
    A("⏱️", "poco tiempo, mucha carga", "PICO DE CORRIENTE")),
  S("la fórmula", "El pico sale de pi, por la raíz de dos veces la salida entre el rizado... por la corriente [(intensidad)] de la *carga.*", "LA *FÓRMULA*",
    B("id máx ≈ π·√(2·Vo/ΔVo)·io", "cuanto menos rizado, más pico"), 1),
  S("la cuenta", "Con doce voltios, uno coma cinco cinco de rizado y setenta y tres miliamperios: unos *cero coma nueve* amperios. Doce veces la carga.", "LA *CUENTA*",
    B("π·√(24/1,55)·73 mA ≈ 0,9 A", "con 470 µF"), 2),
  S("la raíz", "Fíjate en la raíz: cuatro veces más condensador... solo *doble* de pico.", "LA *RAÍZ*",
    A("✖️", "C × 4", "PICO × 2"), 3),
  S("en inverso", "¿Y la tensión [(voltaje)] que aguanta cada diodo apagado? Casi *dos* veces el pico: unos *veinticinco* voltios.", "EN *INVERSO*",
    B("Vd máx ≈ 2·Vp ≈ 25 V", "toma media"), 4),
  S("resumen", "Menos rizado... más pico en los diodos. Lo que gana la salida, lo *pagan* ellos.", "*RESUMEN*",
    F(("📉", "Rizado", "BAJA", None, None), ("⚡", "Pico en diodos", "SUBE", True, "pagan"))),
], pron={"π": "pi", "Vo": "uve o", "ΔVo": "delta uve o", "io": "i o", "Vp": "uve pe"})

vid("tl431-resistencias-calculo", P2, "Elegir las resistencias del TL431", "Divisor y margen de R1", "cálculo", [
  S("objetivo", "Queremos tres voltios con un TL431, que siempre compara con *dos coma cinco.*", "EL *OBJETIVO*",
    A("🎯", "TL431", "3 V A LA SALIDA")),
  S("el divisor", "Tres entre dos coma cinco, menos uno: la de arriba tiene que ser el *veinte* por ciento de la de abajo. Por ejemplo, dos kilos y *diez.*", "EL *DIVISOR*",
    B("R2/R3 = 3/2,5 − 1 = 0,2", "R2 = 2 kΩ · R3 = 10 kΩ"), 1),
  S("R1", "Por la resistencia de entrada entra la corriente [(intensidad)] que se reparten el TL431, el divisor... y la *carga.*", "LA *R1*",
    B("(Vcc − 3)/R1 = iKA + i div + iL", "i div = 3/12k = 0,25 mA"), 2),
  S("R1 máxima", "Peor caso por abajo: diez voltios y cincuenta miliamperios de carga. Así, R1 como mucho *ciento treinta y ocho.*", "R1 *MÁXIMA*",
    B("7 / (50,65 mA) → R1 ≤ 138 Ω", "Vcc mínima + carga máxima"), 3),
  S("R1 mínima", "Peor caso por arriba: quince voltios y carga mínima, diez miliamperios. Para no pasar de ciento cincuenta... R1 como mínimo *setenta y cinco.*", "R1 *MÍNIMA*",
    B("12 / (160,25 mA) → R1 ≥ 75 Ω", "Vcc máxima + carga mínima"), 4),
  S("la regla", "R1 máxima: entrada mínima y carga *máxima.* R1 mínima: entrada máxima y carga *mínima.*", "LA *REGLA*",
    F(("⬆️", "R1 máx", "Vcc MÍN + CARGA MÁX", None, "máxima."), ("⬇️", "R1 mín", "Vcc MÁX + CARGA MÍN", True, "mínima."))),
], pron={"R1": "erre uno", "R2": "erre dos", "R3": "erre tres", "iKA": "i ka", "iL": "i ele"})

vid("cuatro-estructuras-mosfet", P2, "Cuatro formas de poner un MOSFET", "Seguidor o fuente en la alimentación", "cálculo", [
  S("la clave", "Con un MOSFET de paso, todo depende de una cosa: ¿dónde está la *fuente?* ¿En la carga... o en la *alimentación?*", "¿DÓNDE ESTÁ LA *FUENTE?*",
    F(("💡", "Fuente en la carga", "SEGUIDOR", None, "fuente?"), ("🔋", "Fuente en la alimentación", "GRIFO SENSIBLE", True, "alimentación?"))),
  S("seguidor", "En *seguidor,* la salida va unos cuatro voltios por debajo del potenciómetro y lo sigue. Con un NMOS: de cero a *siete coma tres* voltios.", "*SEGUIDOR*",
    B("Vpot = Vo + VTH + √(2Vo/(beta·RL))", "6.a: Vo 0 → 7,3 V"), 1),
  S("su precio", "Fácil de ajustar, usas el sesenta y siete por ciento del potenciómetro. Pero el dropout es de casi *cinco* voltios.", "SU *PRECIO*",
    F(("🎛️", "Recorrido útil", "≈ 67 %", None, None), ("📏", "Dropout", "≈ 4,7 V", True, "voltios.")), 2),
  S("en la alimentación", "Con la fuente en la *alimentación,* como el PMOS en positivo, la salida llega casi a doce... pero todo pasa en un *nueve* por ciento del potenciómetro.", "FUENTE EN LA *ALIMENTACIÓN*",
    F(("🎛️", "Recorrido útil", "≈ 9 %", True, "nueve"), ("📏", "Dropout", "≈ 1 V", None, None)), 3),
  S("negativa", "En negativo pasa *igual,* cambiando NMOS por PMOS: el PMOS seguidor fácil, y el NMOS con poco dropout pero *difícil.*", "EN *NEGATIVO*",
    F(("➕", "Positiva LDO", "PMOS", None, None), ("➖", "Negativa LDO", "NMOS", True, "difícil.")), 4),
  S("la regla", "Seguidor: control *fácil,* dropout grande. Fuente en la alimentación: dropout *pequeño,* control difícil.", "LA *REGLA*",
    F(("🎛️", "Seguidor", "FÁCIL · DROPOUT GRANDE", None, "fácil,"), ("🤏", "Fuente en alimentación", "LDO · DIFÍCIL", True, "pequeño,"))),
], pron={"Vpot": "uve pot", "RL": "erre ele"})

vid("limitador-numeros", P2, "El limitador con números", "70 mA y el AO saturado", "cálculo", [
  S("la salida", "Referencia de dos coma cinco y divisor de uno coma dos: la fuente da *tres* voltios.", "LA *SALIDA*",
    B("Vo = 2,5 · (1 + R1/R2) = 3 V", "mientras el limitador duerme"), 0),
  S("el límite", "La resistencia de sensado es de diez ohmios. El transistor despierta cuando le caen cero coma siete: *setenta* miliamperios.", "EL *LÍMITE*",
    B("0,7 / 10 Ω = 70 mA", "Q2 empieza a conducir"), 1),
  S("la puerta", "A partir de ahí, la puerta del MOSFET tiene que estar en tres, más cero coma siete, más cuatro: *siete coma siete* voltios.", "LA *PUERTA*",
    B("VG = 3 + 0,7 + 4 = 7,7 V", "y el AO llega como mucho a 10,5 V"), 2),
  S("satura", "Lo que cae en la resistencia de puerta es lo que roba el transistor: unos cuatro miliamperios más. Con unos *setenta y cuatro,* el AO se *satura.*", "EL AO *SATURA*",
    B("(10,5 − 7,7)/680 ≈ 4 mA → 74 mA", "AO saturado"), 3),
  S("y luego", "Desde ahí la salida baja de tres voltios... y ya *no* vale el cortocircuito virtual.", "Y *LUEGO*",
    A("📉", "más de 74 mA", "Vo BAJA · SIN C.C. VIRTUAL", "¡OJO!"), 4),
  S("tres números", "Tres voltios regulados... setenta miliamperios despierta... y setenta y cuatro, *satura.*", "TRES *NÚMEROS*",
    F(("🎯", "Regulada", "3 V", None, "regulados..."), ("👀", "Despierta Q2", "70 mA", None, "despierta..."), ("🛑", "Satura el AO", "74 mA", True, "satura."))),
], pron={"R1": "erre uno", "R2": "erre dos", "VG": "uve ge", "Q2": "cu dos"})

vid("fuente-negativa-valores", P2, "Una fuente de −3,3 V con números", "El espejo de la fuente positiva", "cálculo", [
  S("el espejo", "La fuente negativa es la misma... vista en un *espejo.* Todo lo que era positivo, ahora es *negativo.*", "UN *ESPEJO*",
    A("🪞", "mismo circuito", "TODO AL REVÉS")),
  S("qué cambia", "Diodos del rectificador *girados,* el NMOS pasa a *PMOS,* el NPN del limitador a *PNP*... y los electrolíticos con el positivo a *masa.*", "QUÉ *CAMBIA*",
    F(("🔄", "Rectificador", "DIODOS GIRADOS", None, "girados,"), ("🔁", "Q1 / Q2", "PMOS / PNP", True, "PNP..."), ("💥", "Electrolíticos", "+ A MASA", None, "masa.")), 1),
  S("la referencia", "El TL431 también se gira: cátodo y referencia a masa. Así da *menos* dos coma cinco.", "LA *REFERENCIA*",
    B("Vref = −2,5 V", "TL431 girado"), 2),
  S("el divisor", "Para menos tres coma tres: tres coma tres entre dos coma cinco, menos uno... cero coma treinta y dos. Por ejemplo, tres coma tres kilos y *diez.*", "EL *DIVISOR*",
    B("R1/R2 = 3,3/2,5 − 1 = 0,32", "R1 = 3,3 kΩ · R2 = 10 kΩ"), 3),
  S("el límite", "Y para limitar a cien miliamperios: cero coma siete entre cero coma uno... *siete* ohmios. Con seis coma ocho, unos *ciento tres.*", "EL *LÍMITE*",
    B("RS = 0,7 / 0,1 = 7 Ω", "6,8 Ω → ≈ 103 mA"), 4),
  S("la regla", "Polaridad al revés: NMOS por *PMOS,* NPN por *PNP*... y mismas fórmulas con signo *menos.*", "LA *REGLA*",
    F(("🔁", "NMOS → PMOS", "NPN → PNP", True, "PNP..."), ("➖", "Fórmulas", "LAS MISMAS CON −", None, "menos."))),
], pron={"Vref": "uve ref", "R1": "erre uno", "R2": "erre dos", "RS": "erre ese", "Q1": "cu uno", "Q2": "cu dos"})

vid("lm317-lp2951-resistencias", P3, "LM317 contra LP2951: las resistencias", "La referencia está en sitios distintos", "cálculo", [
  S("trampa", "Dos reguladores, mismo divisor... y si usas la misma fórmula en los dos, uno te sale *mal.*", "LA *TRAMPA*",
    F(("🔧", "LM317", "1,25 V ARRIBA", None, None), ("🔧", "LP2951", "1,235 V ABAJO", True, "mal."))),
  S("LM317", "En el LM317, los uno coma veinticinco están en la resistencia de *arriba,* entre salida y ajuste. Con un kilo: uno coma veinticinco miliamperios.", "EL *LM317*",
    B("I R2 = 1,25 V / 1 kΩ = 1,25 mA", "resistencia de arriba"), 1),
  S("la de abajo", "Por la de abajo pasa eso más cuarenta y seis microamperios... y le tocan tres coma setenta y cinco voltios: *dos coma ocho nueve* kilos.", "LA DE *ABAJO*",
    B("3,75 V / 1,296 mA = 2,89 kΩ", "con I ADJ = 46 µA"), 2),
  S("LP2951", "En el LP2951 es al *revés:* su referencia de uno coma dos tres cinco está en la de *abajo,* entre feedback y masa.", "EL *LP2951*",
    A("🔄", "entre FEEDBACK y masa", "REFERENCIA ABAJO"), 3),
  S("la cuenta", "Así que la de arriba, de un kilo, se come tres coma siete seis cinco... y la de abajo sale de *trescientos treinta* ohmios.", "LA *CUENTA*",
    B("1 kΩ · 1,235 / 3,765 ≈ 330 Ω", "resistencia de abajo"), 4),
  S("la regla", "Antes de calcular, mira entre qué patas está la *referencia.*", "LA *REGLA*",
    F(("⬆️", "LM317", "OUT–ADJ (ARRIBA)", None, None), ("⬇️", "LP2951", "FEEDBACK–GND (ABAJO)", True, "referencia."))),
], pron={"I": "i", "R2": "erre dos", "ADJ": "a de jota", "FEEDBACK": "fid bac", "OUT": "aut", "GND": "masa"})

vid("buck-numeros", P3, "El Buck del lab con números", "Rizado y modo continuo", "cálculo", [
  S("los datos", "Siete coma dos a cinco voltios, sobre sesenta ohmios. Bobina de treinta y tres micros, y trescientos cincuenta *kilohercios.*", "LOS *DATOS*",
    F(("🔋", "Vin → Vo", "7,2 V → 5 V", None, None), ("🌀", "L · C", "33 µH · 470 µF", None, None), ("⏱️", "f", "350 kHz", True, "kilohercios."))),
  S("el ciclo", "En un Buck la salida es D por la entrada: cinco entre siete coma dos... D igual a *cero coma seis nueve.*", "EL *CICLO*",
    B("D = 5 / 7,2 ≈ 0,69", "Buck: Vo = D · Vin"), 1),
  S("la bobina", "El rizado de la bobina: uno menos D, por la salida, entre L por f. Unos *ciento treinta y dos* miliamperios.", "LA *BOBINA*",
    B("ΔI = (1 − D)·Vo / (L·f) ≈ 132 mA", "de pico a pico"), 2),
  S("continuo", "La carga pide ochenta y tres miliamperios. Le restas la mitad del rizado... y el mínimo queda en *diecisiete,* mayor que cero. Modo *continuo.*", "MODO *CONTINUO*",
    B("83 − 66 = 17 mA > 0", "nunca llega a cero → continuo"), 3),
  S("el rizado", "Y el rizado de salida: ese rizado de bobina, entre ocho por f por C... apenas *cero coma uno* milivoltios.", "EL *RIZADO*",
    B("ΔV = ΔI / (8·f·C) ≈ 0,1 mV", "casi nada"), 4),
  S("en tres pasos", "D, rizado de bobina... y comprobar que el mínimo no toca *cero.*", "EN TRES *PASOS*",
    F(("1️⃣", "D", "Vo / Vin", None, None), ("2️⃣", "ΔI", "(1 − D)·Vo/(L·f)", None, None), ("3️⃣", "Continuo", "I − ΔI/2 > 0", True, "cero."))),
], pron={"Vin": "uve in", "L": "ele", "C": "ce", "f": "efe", "ΔI": "delta i", "ΔV": "delta uve"})

vid("cargador-numeros", P3, "El cargador del lab con números", "Corriente, margen y temperatura", "cálculo", [
  S("la corriente", "Para cargar a doscientos cincuenta miliamperios con el LM317: uno coma veinticinco entre cero coma veinticinco... *cinco* ohmios.", "LA *CORRIENTE*",
    B("R1 = 1,25 / 0,25 = 5 Ω", "5,1 Ω comercial → 245 mA"), 0),
  S("el valle", "¿Regula siempre? La entrada sale del rectificador: pico de dieciséis coma tres, rizado de dos coma siete... el *valle* queda en trece coma seis.", "EL *VALLE*",
    B("16,27 − 0,25/(2·50·940µ) = 13,6 V", "entrada mínima"), 1),
  S("lo que hace falta", "Necesita ocho coma dos, más uno coma veinticinco, más dos de dropout: *once coma cuatro cinco.* Hay de sobra: *regula.*", "LO QUE HACE *FALTA*",
    F(("📉", "Valle de entrada", "13,6 V", True, "regula."), ("📏", "Necesita", "8,2 + 1,25 + 2 = 11,45 V", None, "cinco.")), 2),
  S("el calor", "¿Y la temperatura? El peor caso es *al revés:* entrada máxima y batería *mínima.* Nueve voltios por cero coma veinticinco: dos coma dos vatios.", "EL *CALOR*",
    B("(16,27 − 7,25)·0,25 ≈ 2,26 W", "pico de entrada + batería vacía"), 3),
  S("la unión", "Con veintitrés coma tres grados por vatio: veinticinco más cincuenta y tres... *setenta y siete* grados. Muy lejos de ciento cincuenta.", "LA *UNIÓN*",
    B("Tj = 25 + 23,3·2,26 ≈ 77,5 °C", "< 150 °C"), 4),
  S("los dos peores", "Para el dropout, batería *llena* y entrada en el valle. Para el calor, batería *vacía* y entrada en el pico.", "LOS DOS *PEORES*",
    F(("📏", "Dropout", "BATERÍA LLENA · VALLE", None, "llena"), ("🔥", "Calor", "BATERÍA VACÍA · PICO", True, "vacía"))),
], pron={"R1": "erre uno", "Tj": "te jota"})

vid("cargador-tl431-numeros", P3, "Cuándo deja de cargar a corriente constante", "R3, R4 y los 8 voltios", "cálculo", [
  S("pregunta", "¿En qué momento pasa el cargador de corriente [(intensidad)] constante a tensión [(voltaje)] *constante?*", "¿*CUÁNDO?*",
    A("🔀", "fase CC → fase CV", "LO DECIDE UN DIVISOR")),
  S("el divisor", "Un divisor colgado de la batería le da al TL431 una parte de su tensión. Cuando esa parte llega a *dos coma cinco...* cambia de fase.", "EL *DIVISOR*",
    B("V ref = VB · R4 / (R3 + R4)", "cambia al llegar a 2,5 V"), 1),
  S("la cuenta", "Para cambiar a ocho voltios con cuatro de diez kilos: diez kilos por ocho entre dos coma cinco menos uno... *veintidós* kilos.", "LA *CUENTA*",
    B("R3 = 10k · (8/2,5 − 1) = 22 kΩ", "resistencia de arriba"), 2),
  S("antes", "Antes de llegar, el TL431 está *apagado:* el LM317 mete sus doscientos cincuenta miliamperios, sin importar la batería.", "ANTES: *APAGADO*",
    A("😴", "VB < 8 V", "I = 250 mA CONSTANTE"), 3),
  S("después", "Al llegar, el TL431 la clava en ocho voltios... y la corriente va *bajando* sola hasta casi *cero.*", "DESPUÉS: *8 V*",
    A("📉", "VB = 8 V fija", "LA CORRIENTE CAE"), 4),
  S("en una línea", "Batería igual a dos coma cinco, por uno más R3 entre *R4.*", "EN UNA *LÍNEA*", B("VB = 2,5 · (1 + R3/R4)", "= 8 V")),
], pron={"VB": "uve be", "R3": "erre tres", "R4": "erre cuatro", "CC": "ce ce", "CV": "ce uve"})

vid("buck-cargador", P3, "Un cargador con Buck", "Ciclo de trabajo y bobina mínima", "cálculo", [
  S("la idea", "Un cargador conmutado: de dieciséis coma tres voltios a una batería de seis a ocho coma cuatro. ¿Qué *convertidor?*", "¿QUÉ *CONVERTIDOR?*",
    A("🔀", "16,3 V → 6–8,4 V", "HAY QUE BAJAR → BUCK")),
  S("el ciclo", "Como siempre baja, un *Buck.* D es batería entre entrada: de cero coma treinta y siete a cero coma *cincuenta y dos.*", "EL *CICLO*",
    B("D = VB / Vin = 0,37 → 0,52", "6/16,27 y 8,4/16,27"), 1),
  S("la condición", "Para modo continuo, la mitad del rizado de la bobina no puede pasar de la corriente de carga, doscientos *miliamperios.*", "LA *CONDICIÓN*",
    B("ΔI / 2 ≤ 0,2 A", "con ΔI = D·(1 − D)·Vin / (L·f)"), 2),
  S("el peor", "El peor caso es con D igual a cero coma *cinco,* donde D por uno menos D es máximo. Y está dentro del margen.", "EL *PEOR* CASO",
    A("🎯", "D·(1 − D) máximo en D = 0,5", "PEOR CASO"), 3),
  S("la bobina", "Cero coma veinticinco por dieciséis coma tres, entre cero coma cuatro por cien kilohercios... unos *ciento dos* microhenrios como mínimo.", "LA *BOBINA*",
    B("L ≥ 0,25·16,27 / (0,4·100k) ≈ 102 µH", "bobina mínima"), 4),
  S("la clave", "Buck, D entre cero coma treinta y siete y cero coma cincuenta y dos... y la bobina con D igual a *medio.*", "LA *CLAVE*",
    F(("🔀", "Buck", "D = 0,37–0,52", None, None), ("🌀", "L mínima", "≈ 102 µH (D = 0,5)", True, "medio."))),
], pron={"VB": "uve be", "Vin": "uve in", "ΔI": "delta i", "L": "ele", "f": "efe"})

PREVIO = {  # a qué pregunta del previo / control responde cada vídeo (se ve en la app, la voz no lo dice)
 "led-resistencia": "P1 · intro", "bjt-tres-zonas": "P1 S1.1–S1.2", "npn-o-pnp": "P1 S1.1–S1.2", "darlington": "P1 S1.3",
 "multimetro": "P1 S1.4–S1.5", "fuente-ocp": "P1 S1.6", "iled-bjt-calculo": "P1 S1.7–S1.9 · control P1-3 nº1",
 "avalancha-termica": "P1 3.1 · S1.11", "cortocircuito-virtual": "P1 S1.11", "iled-ao-calculo": "P1 S1.11 · control P1-3 nº1",
 "lineal-o-conmutacion": "P1 S2.1", "nmos-pmos-por-dentro": "P1 S2.2, S2.3, S2.5", "mosfet-interruptor": "P1 S2.4 · control nº2",
 "comparador-histeresis": "P1 S2.6–S2.7", "umbrales-histeresis-calculo": "P1 S2.6–S2.7", "astable-rc": "P1 S2.8–S2.9",
 "astable-tiempos-calculo": "P1 S2.8–S2.9", "pwm-dimmer": "P1 S2.10 · control nº2", "sondas-generador": "P1 C4–C5",
 "fuente-cuatro-bloques": "P2 intro · control nº4", "rizado-calculo": "P2 S1.1", "pico-diodos-calculo": "P2 S1.2 · control nº3",
 "transitorio-arranque": "P2 3.1.3 · control nº3", "diodo-zener": "P2 S1.3", "tl431": "P2 S1.6–S1.8",
 "tl431-resistencias-calculo": "P2 S1.4–S1.5", "cuatro-estructuras-mosfet": "P2 S2.1–S2.4", "nmos-o-pmos-regulador": "P2 S2.1–S2.4",
 "dropout-discreto": "P2 S2.5", "condensadores-utiles": "P2 S2.7 · P3 C1", "limitador-corriente": "P2 S2.8–S2.9",
 "limitador-numeros": "P2 S2.8–S2.9", "fuente-negativa-valores": "P2 S2.10 · control nº4",
 "lm317-lp2951-resistencias": "P3 S1.1, S1.4", "rendimiento-lineal": "P3 S1.2", "autonomia-dropout": "P3 S1.3, S1.5 · control nº5",
 "colector-abierto": "P3 S1.6 · control nº6", "buck-numeros": "P3 S1.7–S1.10", "tres-reguladores-autonomia": "P3 S1.11 · control nº5",
 "lm317-fuente-corriente": "P3 S2.1", "cargador-numeros": "P3 S2.1–S2.3", "cargador-cc-cv": "P3 S2.4–S2.6 · control nº6",
 "cargador-tl431-numeros": "P3 S2.5–S2.6", "pt1000-seguridad": "P3 S2.7", "buck-cargador": "P3 S2.8", "emulador-celdas": "P3 intro",
}
for v in V:
    k = v["id"][len("cesa-lab-"):]
    if k in PREVIO: v["texto"] = f'{v["texto"]} · {PREVIO[k]}'

if __name__ == "__main__":
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lab")
    os.makedirs(d, exist_ok=True)
    for v in V:
        with open(os.path.join(d, v["id"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=False, indent=1)
    print(len(V), "specs;", sum(len(s["sub"]) for v in V for s in v["segmentos"]), "caracteres")
