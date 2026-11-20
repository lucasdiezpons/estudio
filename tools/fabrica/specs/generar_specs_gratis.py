"""TikToks de CESA (Control 2: normativa, fotovoltaica, baterías, protecciones) con VOZ GRATIS (tts_gratis.py).
Uso: python3 generar_specs_gratis.py  → specs/gratis/*.json"""
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

R = "en resumen"; RT = "EN *RESUMEN*"; C = "la curiosidad"
NOR, FV, BAT, PRO, CAL = "CESA · Normativa", "CESA · Fotovoltaica", "CESA · Baterías", "CESA · Protecciones", "CESA · Dimensionado FV"
P_COM = {"UNE": "une", "CE": "ce e", "TT": "te te", "TN": "te ene", "MPPT": "eme pe pe te", "PPTC": "pe pe te ce",
         "MOV": "mof", "NiMH": "níquel metal hidruro", "Li-ion": "litio ion", "HSP": "hache ese pe"}
V = []

def vid(id, titulo, texto, tema, etiqueta, segs, pron=None):
    p = dict(P_COM); p.update(pron or {})
    V.append({"id": "cesa-g-" + id, "titulo": titulo, "texto": texto, "tema": tema, "etiqueta": etiqueta, "examen": "Control 2",
              "pron": p, "voz": "gratis", "segmentos": segs})

# ======================= NORMATIVA =======================
vid("norma-o-reglamento", "Norma no es lo mismo que ley", "Quién las dicta y cuáles obligan", NOR, "normativa", [
  S(C, "¿Sabías que una *norma* técnica... no te obliga a nada?", "LAS NORMAS *NO OBLIGAN*", A("📘", "UNE, CEN, IEC...", "VOLUNTARIAS")),
  S("quién las hace", "Las normas las escriben *comités técnicos:* expertos que se ponen de acuerdo en cómo hacer bien las cosas.", "COMITÉS *TÉCNICOS*",
    A("👷", "expertos del sector", "COMITÉS TÉCNICOS"), 1),
  S("qué son", "Por eso son *recomendaciones.* Cumplirlas ayuda... pero nadie te multa por no seguirlas.", "SOLO *RECOMIENDAN*",
    A("💡", "seguirlas ayuda", "RECOMENDACIONES"), 1),
  S("los reglamentos", "Lo que sí obliga son los *reglamentos:* los dicta un gobierno o la Unión Europea... y son ley.", "LOS *REGLAMENTOS*",
    F(("📘", "Norma", "COMITÉ · VOLUNTARIA", None, "obliga"), ("⚖️", "Reglamento", "GOBIERNO · OBLIGATORIO", True, "ley.")), 2),
  S("la trampa", "Y ojo: la Comisión Europea no dicta normas. Las normas siempre salen de un *comité.*", "LA *TRAMPA*",
    A("🚫", "la Comisión Europea no dicta normas", "SIEMPRE UN COMITÉ", "¡OJO!"), 3),
  S(R, "Así que ya sabes. Norma: comité y *voluntaria.* Reglamento: gobierno y *obligatorio.*", RT,
    F(("📘", "Norma", "COMITÉ · VOLUNTARIA", None, "voluntaria."), ("⚖️", "Reglamento", "GOBIERNO · OBLIGATORIO", True, "obligatorio."))),
])

vid("real-decreto-o-une", "Real Decreto o UNE", "Cómo saber si algo obliga solo por su nombre", NOR, "normativa", [
  S(C, "¿Sabías que con leer el *nombre* de un documento ya sabes si es obligatorio?", "MIRA EL *NOMBRE*", A("🔎", "solo con el nombre", "¿OBLIGA O NO?")),
  S("UNE", "Si empieza por *UNE*... es una norma. La escribe un comité técnico... y no es obligatoria.", "SI DICE *UNE*",
    A("📘", "UNE 20503, por ejemplo", "NORMA · VOLUNTARIA"), 1),
  S("Real Decreto", "Si dice *Real Decreto*... es un reglamento. Lo dicta el Gobierno... y hay que cumplirlo sí o sí.", "SI DICE *REAL DECRETO*",
    A("⚖️", "Real Decreto 1580 de 2006, por ejemplo", "GOBIERNO · OBLIGATORIO"), 2),
  S("mismo tema", "Pueden hablar del mismo tema, como la compatibilidad *electromagnética*... y aun así uno obliga y el otro no.", "MISMO *TEMA*",
    F(("📘", "UNE 20503", "NO OBLIGA", None, "obliga"), ("⚖️", "Real Decreto 1580", "OBLIGA", True, "no.")), 3),
  S(R, "Así que ya sabes. UNE, *voluntaria.* Real Decreto, *obligatorio.*", RT,
    F(("📘", "UNE", "VOLUNTARIA", None, "voluntaria."), ("⚖️", "Real Decreto", "OBLIGATORIO", True, "obligatorio."))),
])

vid("marcado-ce", "Lo que de verdad significa el CE", "No lo pone ningún laboratorio", NOR, "normativa", [
  S(C, "¿Sabías que el *CE* de tus aparatos... no lo pone ningún laboratorio?", "EL *CE*", A("🏷️", "marcado CE", "¿QUIÉN LO PONE?")),
  S("obligatorio", "Para vender un producto en Europa, el marcado CE y la *Declaración de Conformidad* son obligatorios.", "*OBLIGATORIO*",
    A("🇪🇺", "para vender en Europa", "CE + DECLARACIÓN"), 1),
  S("quién", "Pero lo pone el propio *fabricante*... o el importador. Nadie tiene que probarlo antes.", "LO PONE EL *FABRICANTE*",
    A("🏭", "fabricante o importador", "SE LO PONE ÉL MISMO"), 2),
  S("qué significa", "Con eso firma que cumple la ley... y que se hace *responsable* si hay un accidente por no cumplirla.", "SE HACE *RESPONSABLE*",
    A("✍️", "si hay un accidente", "RESPONDE ÉL", "¡OJO!"), 2),
  S(R, "Así que ya sabes. El CE es obligatorio... y significa que el fabricante se hace *responsable.*", RT,
    F(("🏷️", "CE", "OBLIGATORIO", None, "obligatorio..."), ("✍️", "Significa", "EL FABRICANTE RESPONDE", True, "responsable."))),
])

vid("declaracion-conformidad", "La Declaración de Conformidad", "Para qué productos y por qué", NOR, "normativa", [
  S(C, "¿Sabías que *todos* los productos que se venden necesitan un papel firmado por el fabricante?", "UN *PAPEL*", A("📄", "Declaración de Conformidad", "PARA TODOS")),
  S("cuáles", "No solo los peligrosos: *todos.* Del cargador del móvil a una tostadora.", "*TODOS*",
    F(("⚠️", "Solo los peligrosos", "NO", None, None), ("✅", "Todos los productos", "SÍ", True, "todos."))),
  S("por qué", "Y se entrega para responder de los *reglamentos*... que son lo obligatorio. No de las normas.", "LOS *REGLAMENTOS*",
    F(("📘", "Normas", "NO", None, "normas."), ("⚖️", "Reglamentos", "SÍ", True, "reglamentos...")), 1),
  S("a quién", "Se entrega a la administración pública... y con ella el fabricante se hace *responsable.*", "LA *ADMINISTRACIÓN*",
    A("🏛️", "se entrega a", "LA ADMINISTRACIÓN"), 2),
  S(R, "Así que ya sabes. Para *todos* los productos... y por los *reglamentos.*", RT,
    F(("📄", "Para", "TODOS LOS PRODUCTOS", None, "todos"), ("⚖️", "Por", "LOS REGLAMENTOS", True, "reglamentos."))),
])

# ======================= FOTOVOLTAICA =======================
vid("zona-carga-espacial", "Dónde atrapa la luz una placa", "La zona de carga espacial", FV, "celdas", [
  S(C, "¿Sabías que en una placa solar... no todo el silicio sirve para generar electricidad?", "NO TODO *SIRVE*", A("☀️", "dentro de una celda", "¿DÓNDE SE GENERA?")),
  S("la unión", "Una celda es una unión de silicio *P* con silicio *N.* Justo en la frontera aparece una zona especial.", "LA *UNIÓN PN*",
    F(("🟥", "Zona P", "SILICIO P", None, None), ("🟦", "Zona N", "SILICIO N", None, None)), 1, ),
  S("la zona", "Es la zona de carga *espacial:* allí hay un campo eléctrico que separa los electrones de los huecos.", "CARGA *ESPACIAL*",
    A("⚡", "aquí hay campo eléctrico", "ZONA DE CARGA ESPACIAL"), 2),
  S("por qué", "Si la luz crea un par lejos de ahí... se vuelve a juntar y se pierde. Solo en esa zona se *aprovecha.*", "SOLO AHÍ *SIRVE*",
    A("🎯", "el campo separa el par", "ZONA FOTOSENSIBLE"), 3),
  S(R, "Así que ya sabes. La zona fotosensible no es la P ni la N... es la zona de carga *espacial.*", RT,
    B("ZONA DE CARGA ESPACIAL", "= zona fotosensible")),
], pron={"P": "pe", "N": "ene", "PN": "pe ene"})

vid("difusion-y-arrastre", "Las dos corrientes de una celda", "Difusión y arrastre", FV, "celdas", [
  S(C, "¿Sabías que dentro de una celda solar hay dos corrientes [(intensidades)] que se mueven por motivos *distintos?*", "DOS *CORRIENTES*", A("🔀", "dentro de la celda", "DOS MOTIVOS")),
  S("difusión", "La de *difusión:* los portadores van de donde hay muchos... a donde hay pocos. Como el olor de un perfume.", "*DIFUSIÓN*",
    A("🌸", "de mucha concentración a poca", "DIFUSIÓN"), 1),
  S("arrastre", "La de *arrastre:* la empuja un campo eléctrico, como el de la zona de carga espacial.", "*ARRASTRE*",
    A("⚡", "la empuja un campo eléctrico", "ARRASTRE"), 2),
  S("no confundir", "No confundas: difusión es por *concentración*... arrastre es por *campo.* Y la de la luz es la fotogenerada.", "NO LAS *CONFUNDAS*",
    F(("🌸", "Difusión", "CONCENTRACIÓN", None, "concentración..."), ("⚡", "Arrastre", "CAMPO ELÉCTRICO", True, "campo."), ("☀️", "Fotogenerada", "LA LUZ", None, "fotogenerada.")), 3),
  S(R, "Así que ya sabes. Difusión: los portadores se reparten de donde hay más... a donde hay *menos.*", RT,
    B("DIFUSIÓN", "= diferencias de concentración")),
])

vid("celda-a-oscuras", "Una placa solar a oscuras", "Se convierte en otra cosa", FV, "celdas", [
  S(C, "¿Sabías que una celda solar a oscuras... se convierte en un componente de lo más *normal?*", "A *OSCURAS*", A("🌑", "sin nada de luz", "¿QUÉ QUEDA?")),
  S("qué es", "Una celda es una unión PN muy grande. Sin luz, no genera nada... y lo que queda es un *diodo.*", "UN *DIODO*",
    A("🔻", "unión PN sin luz", "UN DIODO"), 1),
  S("las trampas", "No es un circuito abierto, ni una resistencia, ni un transistor. Es un *diodo.*", "NI ABIERTO *NI* RESISTENCIA",
    F(("❌", "Circuito abierto", "NO", None, None), ("❌", "Resistencia", "NO", None, None), ("✅", "Diodo", "SÍ", True, "diodo.")), 2),
  S("con luz", "Con luz, es ese mismo diodo... con una fuente de corriente [(intensidad)] en paralelo que crece con la *luz.*", "CON *LUZ*",
    A("☀️", "diodo + fuente de corriente", "LA LUZ AÑADE CORRIENTE"), 3),
  S(R, "Así que ya sabes. Celda a oscuras... *diodo.*", RT, B("A OSCURAS = DIODO", "una unión PN")),
], pron={"PN": "pe ene"})

vid("calor-isc-voc", "Qué le hace el calor a una placa", "Corriente y tensión no van igual", FV, "temperatura", [
  S(C, "¿Sabías que cuando una placa se calienta... una cosa sube y otra *baja?*", "UNA SUBE, *OTRA BAJA*", A("🌡️", "placa caliente", "¿QUÉ CAMBIA?")),
  S("la corriente", "La corriente [(intensidad)] de cortocircuito *sube...* pero solo un poquito.", "LA CORRIENTE *SUBE*",
    A("⬆️", "corriente de cortocircuito", "SUBE UN POCO"), 1),
  S("la tensión", "La tensión [(voltaje)] de circuito abierto *baja...* y bastante más.", "LA TENSIÓN *BAJA*",
    A("⬇️", "tensión de circuito abierto", "BAJA BASTANTE"), 1),
  S("la potencia", "Como baja más la tensión de lo que sube la corriente... la potencia máxima *baja.*", "LA POTENCIA *BAJA*",
    F(("⬆️", "Corriente", "+ UN POCO", None, None), ("⬇️", "Tensión", "− BASTANTE", None, None), ("🔥", "Potencia máxima", "BAJA", True, "baja.")), 2),
  S(R, "Así que ya sabes. Con calor... corriente *arriba,* tensión *abajo.*", RT,
    F(("⬆️", "Isc", "SUBE", None, "arriba,"), ("⬇️", "Voc", "BAJA", True, "abajo."))),
])

vid("calor-directa-vs-mppt", "Cuándo el calor da más energía", "Conexión directa contra MPPT", FV, "temperatura", [
  S(C, "¿Sabías que una placa caliente puede dar *más* energía... o menos, según cómo la conectes?", "MÁS... *O MENOS*", A("🔌", "depende de la conexión", "DIRECTA O MPPT")),
  S("directa", "En conexión *directa,* la batería fija la tensión [(voltaje)]... y la energía depende de la corriente [(intensidad)]. Con calor, *sube.*", "DIRECTA: *SUBE*",
    B("Vbat · Icc", "conexión directa: manda la corriente"), 1),
  S("MPPT", "Con un *MPPT,* sacas la potencia máxima. Y esa, con calor... *baja.*", "MPPT: *BAJA*",
    B("REND · Pmpp", "MPPT: manda la potencia máxima"), 1),
  S("peor caso", "Por eso el peor caso cambia: en directa, el día más *frío.* Con MPPT, el día más *caluroso.*", "EL *PEOR* CASO",
    F(("🥶", "Directa", "TEMPERATURA MÍNIMA", None, "frío."), ("🥵", "MPPT", "TEMPERATURA MÁXIMA", True, "caluroso.")), 2),
  S(R, "Así que ya sabes. Con calor, la directa *gana*... y el MPPT *pierde.*", RT,
    F(("🔌", "Directa", "MÁS ENERGÍA", None, "gana..."), ("📉", "MPPT", "MENOS ENERGÍA", True, "pierde."))),
], pron={"Vbat": "uve bat", "Icc": "i ce ce", "Pmpp": "pe eme pe pe"})

vid("fill-factor", "El Fill Factor de una placa", "Qué tan cuadrada es su curva", FV, "celdas", [
  S(C, "¿Sabías que las placas solares tienen una nota de *calidad*... que se llama Fill Factor?", "EL *FILL FACTOR*", A("📏", "factor de forma", "FILL FACTOR")),
  S("el sueño", "Lo ideal sería sacar a la vez la tensión [(voltaje)] de circuito *abierto*... y la corriente [(intensidad)] de *cortocircuito.*", "EL *SUEÑO*",
    B("Voc · Isc", "lo imposible: las dos a la vez"), 1),
  S("la realidad", "Pero eso es imposible. Lo máximo que sacas de verdad es la potencia del punto de máxima *potencia.*", "LA *REALIDAD*",
    B("Pmpp", "lo que sacas de verdad"), 1),
  S("la fórmula", "El Fill Factor es la potencia máxima... entre ese producto *imposible.* Cuanto más cerca de uno, *mejor.*", "LA *FÓRMULA*",
    B("FF = Pmpp / (Voc · Isc)", "cuanto más cerca de 1, mejor"), 2),
  S(R, "Así que ya sabes. Fill Factor: potencia máxima, entre tensión de vacío por corriente de *cortocircuito.*", RT,
    B("Pmpp / (Voc · Isc)", "Fill Factor")),
], pron={"Fill": "fil", "Factor": "fáctor", "Voc": "uve o ce", "Isc": "i ese ce", "Pmpp": "pe eme pe pe"})

vid("mono-poli-amorfo", "Mono, poli y amorfo", "El orden que nunca cambia", FV, "paneles", [
  S(C, "¿Sabías que con *un* solo orden ya sabes qué placa rinde más... y cuál es más cara?", "UN SOLO *ORDEN*", A("🥇", "rendimiento y coste", "MISMO ORDEN")),
  S("el orden", "Monocristalino... policristalino... y amorfo. Más orden en el cristal, *más* rendimiento.", "EL *ORDEN*",
    F(("🥇", "Monocristalino", "UN CRISTAL", True, "Monocristalino..."), ("🥈", "Policristalino", "MUCHOS CRISTALES", None, "policristalino..."), ("🥉", "Amorfo", "SIN RED CRISTALINA", None, "amorfo.")), 1),
  S("el precio", "Y el precio va *igual:* el mono es el más caro... y el amorfo el más *barato.*", "EL *PRECIO*",
    A("💶", "de mayor a menor", "MONO > POLI > AMORFO"), 2),
  S("la trampa", "Ojo cuando te lo pidan al revés, de *menor* a mayor: amorfo, poli... y mono.", "AL *REVÉS*",
    A("🔄", "de menor a mayor", "AMORFO < POLI < MONO", "¡OJO!"), 3),
  S(R, "Así que ya sabes. Mono, poli, amorfo... en rendimiento y en *precio.*", RT, B("MONO > POLI > AMORFO", "rendimiento y coste")),
])

vid("punto-caliente-serie", "Una celda a la sombra en serie", "El punto caliente", FV, "sombras", [
  S(C, "¿Sabías que una sola hoja encima de una placa... puede *quemar* una celda?", "UNA *HOJA*", A("🍂", "una celda tapada", "PUNTO CALIENTE")),
  S("en serie", "Si las celdas van en *serie,* todas comparten la misma corriente [(intensidad)]. La tapada no la puede generar.", "EN *SERIE*",
    A("🔗", "misma corriente para todas", "LA TAPADA NO PUEDE"), 1),
  S("qué pasa", "Las demás la empujan igual... queda en *inverso* y se come la energía. Se calienta: un punto *caliente.*", "PUNTO *CALIENTE*",
    A("🔥", "polarizada en inverso", "SE CALIENTA", "¡OJO!"), 2),
  S("la solución", "La solución: un diodo de *bypass* en paralelo con las celdas. La corriente se va por el diodo... y la celda se *salva.*", "DIODO EN *PARALELO*",
    F(("🔗", "Celdas en serie", "DIODO EN PARALELO", True, "bypass"), ("🛟", "La corriente", "SE DESVÍA", None, "salva.")), 3),
  S(R, "Así que ya sabes. Celda tapada en serie: punto caliente... y diodo en *paralelo.*", RT,
    F(("🔗", "En serie", "PUNTO CALIENTE", None, "caliente..."), ("🛟", "Solución", "DIODO EN PARALELO", True, "paralelo."))),
], pron={"bypass": "bai pas"})

vid("punto-caliente-paralelo", "Una celda a la sombra en paralelo", "Aquí la solución es al revés", FV, "sombras", [
  S(C, "¿Sabías que si las celdas van en *paralelo*... la solución a la sombra es justo la contraria?", "AL *REVÉS*", A("🔀", "celdas en paralelo", "OTRA SOLUCIÓN")),
  S("qué pasa", "La celda tapada no genera... y las demás le *meten* corriente [(intensidad)] a ella. Se calienta: punto *caliente.*", "LE METEN *CORRIENTE*",
    A("🔥", "las demás la alimentan", "PUNTO CALIENTE"), 1),
  S("la solución", "Para cortarlo, un diodo en *serie* con cada celda: deja salir la corriente... pero no la deja *entrar.*", "DIODO EN *SERIE*",
    A("⛔", "deja salir, no entrar", "DIODO DE BLOQUEO"), 2),
  S("la regla", "La regla es fácil: en serie, diodo en *paralelo.* En paralelo, diodo en *serie.*", "LA *REGLA*",
    F(("🔗", "Celdas en serie", "DIODO EN PARALELO", None, "paralelo."), ("🔀", "Celdas en paralelo", "DIODO EN SERIE", True, "serie.")), 3),
  S(R, "Así que ya sabes. Siempre punto caliente... y el diodo, al *revés* que las celdas.", RT,
    B("SERIE / PARALELO", "el diodo, al revés que las celdas")),
])

vid("cuantas-celdas-en-serie", "Cuántas celdas para cargar una batería", "El peor caso manda", FV, "dimensionado", [
  S(C, "¿Sabías que para cargar una batería directamente con una placa... hay que contar las celdas con el *peor* caso?", "EL *PEOR* CASO", A("🔋", "placa directa a batería", "¿CUÁNTAS CELDAS?")),
  S("la regla", "La placa tiene que superar la tensión [(voltaje)] *máxima* de la batería... aunque cada celda dé su tensión *mínima.*", "LA *REGLA*",
    B("Vbat máx / Vcelda mín", "y redondeas hacia arriba"), 1),
  S("ejemplo", "Batería hasta 4,2 voltios, celdas de 0,5 como mínimo: 4,2 entre 0,5... 8,4. Necesitas *más* de ocho.", "*EJEMPLO*",
    B("4,2 / 0,5 = 8,4", "con 8 solo llegas a 4 V"), 2),
  S("la respuesta", "Con ocho solo llegas a 4 voltios: no carga. Así que la siguiente opción... *diez.*", "*DIEZ*",
    A("🔟", "8 · 0,5 = 4 V < 4,2 V", "10 CELDAS"), 2),
  S("otro", "Y si la batería llega a 3,6: 3,6 entre 0,5 da 7,2... así que *ocho.*", "OTRO *EJEMPLO*",
    B("3,6 / 0,5 = 7,2 → 8", "8 · 0,5 = 4 V > 3,6 V"), 3),
  S(R, "Así que ya sabes. Tensión máxima de la batería, entre la mínima de la celda... y *hacia arriba.*", RT,
    B("Vbat máx / Vcelda mín", "número de celdas en serie")),
], pron={"Vbat": "uve bat", "Vcelda": "uve celda"})

vid("inclinacion-hemisferios", "Junio no es verano en todas partes", "Inclinar placas en el hemisferio sur", FV, "inclinación", [
  S(C, "¿Sabías que en Buenos Aires, en junio... la placa se inclina como en *invierno?*", "JUNIO = *INVIERNO*", A("🌎", "hemisferio sur", "ESTACIONES AL REVÉS")),
  S("la regla", "Verano: el sol va *alto,* la placa casi plana. Invierno: el sol va *bajo,* la placa muy de pie.", "LA *REGLA*",
    F(("☀️", "Verano", "≈ 15 GRADOS", None, "alto,"), ("❄️", "Invierno", "≈ 55 GRADOS", True, "bajo,")), 1),
  S("al norte", "En el hemisferio norte: junio, verano... unos *quince* grados. Diciembre, invierno... unos *cincuenta y cinco.*", "HEMISFERIO *NORTE*",
    F(("☀️", "Junio", "≈ 15°", None, "quince"), ("❄️", "Diciembre", "≈ 55°", True, "cinco.")), 2),
  S("al sur", "En el sur, *al revés:* junio es invierno, cincuenta y cinco... y diciembre es verano, *quince.*", "HEMISFERIO *SUR*",
    F(("❄️", "Junio", "≈ 55°", True, "invierno,"), ("☀️", "Diciembre", "≈ 15°", None, "quince.")), 2),
  S(R, "Así que ya sabes. Primero mira el *hemisferio*... y luego si es verano o *invierno.*", RT,
    F(("🌎", "Primero", "EL HEMISFERIO", None, "hemisferio..."), ("❄️", "Invierno", "MÁS INCLINADA", True, "invierno."))),
])

vid("placa-hacia-el-norte", "Placas que miran al norte", "En el hemisferio sur", FV, "inclinación", [
  S(C, "¿Sabías que en Argentina las placas solares miran al *norte?*", "MIRAN AL *NORTE*", A("🧭", "hemisferio sur", "HACIA EL NORTE")),
  S("por qué", "La placa siempre mira hacia el *ecuador,* que es por donde pasa el sol. Al sur del ecuador... eso es el *norte.*", "HACIA EL *ECUADOR*",
    F(("🌍", "Hemisferio norte", "MIRA AL SUR", None, "ecuador,"), ("🌎", "Hemisferio sur", "MIRA AL NORTE", True, "norte.")), 1),
  S("cómo se escribe", "Por eso verás inclinaciones como diez grados *norte* o cincuenta y cinco grados *norte.*", "GRADOS *NORTE*",
    A("📐", "inclinación + hacia dónde mira", "10°N · 55°N"), 2),
  S("ejemplo", "Buenos Aires en diciembre, verano: poca inclinación, unos *diez* grados norte. En junio, invierno: unos *cincuenta y cinco.*", "BUENOS *AIRES*",
    F(("☀️", "Diciembre", "≈ 10°N", None, "diez"), ("❄️", "Junio", "≈ 55°N", True, "cinco.")), 3),
  S(R, "Así que ya sabes. La placa mira siempre hacia el *ecuador.*", RT, B("MIRA AL ECUADOR", "sur → norte · norte → sur")),
])

# ======================= DIMENSIONADO (problema) =======================
vid("consumo-diario", "Cuánta energía gasta un aparato al día", "Potencia por tiempo, y sumar", CAL, "consumo", [
  S(C, "¿Sabías que para dimensionar una instalación solar... todo empieza por una *suma?*", "UNA *SUMA*", A("➕", "consumo de un día", "EMPIEZA AQUÍ")),
  S("la fórmula", "Energía es potencia por *tiempo.* Haces eso para cada modo del aparato... y lo *sumas.*", "POTENCIA × *TIEMPO*",
    B("E = Σ P · t", "y sumas cada modo"), 1),
  S("eventos", "Si te dan la energía de cada *evento,* como una transmisión... la multiplicas por las veces que pasa.", "LOS *EVENTOS*",
    B("+ E evento · nº", "energía por las veces"), 1),
  S("la trampa", "Ojo: si dicen potencia *total,* ese tiempo se lo restas al reposo. Si dicen potencia *extra,* lo sumas encima.", "TOTAL O *EXTRA*",
    F(("➖", "Potencia total", "RESTA AL REPOSO", True, "total,"), ("➕", "Potencia extra", "SUMA ENCIMA", None, "extra,")), 2),
  S("unidades", "Y cuidado con las unidades: los miliwatios hora entre mil... son watios *hora.*", "LAS *UNIDADES*",
    A("📏", "mWh / 1000 = Wh", "UNIDADES"), 3),
  S(R, "Así que ya sabes. Potencia por tiempo, más eventos... y *total* se resta, *extra* se suma.", RT,
    F(("➕", "Consumo", "Σ P · t + EVENTOS", None, "eventos..."), ("⚠️", "Total / extra", "RESTA / SUMA", True, "suma."))),
], pron={"E": "e"})

vid("radiacion-tf", "La radiación sobre una placa inclinada", "El factor de la tabla", CAL, "radiación", [
  S(C, "¿Sabías que inclinar la placa cambia la energía que recibe... y una *tabla* te dice cuánto?", "UNA *TABLA*", A("📋", "mes × inclinación", "FACTOR TF")),
  S("la fórmula", "La radiación sobre la placa es la radiación en horizontal... por un factor de *corrección.*", "LA *FÓRMULA*",
    B("H = TF · H0", "radiación sobre la placa inclinada"), 1),
  S("la tabla", "Ese factor lo sacas de la tabla: buscas tu *mes* en la columna... y tu inclinación en la *fila.*", "LA *TABLA*",
    F(("📅", "Columna", "EL MES", None, "mes"), ("📐", "Fila", "LA INCLINACIÓN", True, "fila.")), 2),
  S("hemisferio sur", "Truco del hemisferio sur: los meses van *desplazados* seis meses. Diciembre en el sur... es la columna de *junio.*", "HEMISFERIO *SUR*",
    A("🔄", "diciembre sur → columna junio", "+6 MESES", "¡OJO!"), 3),
  S("la mejor", "Y si te piden la inclinación óptima de un mes... es la fila con el factor más *grande* de esa columna.", "LA *ÓPTIMA*",
    A("🏆", "en la columna del mes", "EL TF MÁS GRANDE"), 4),
  S(R, "Así que ya sabes. Radiación en horizontal por el *factor*... y en el sur, seis meses *desplazados.*", RT,
    F(("📋", "Radiación", "TF · H0", None, "factor..."), ("🔄", "Sur", "+6 MESES", True, "desplazados."))),
], pron={"TF": "te efe", "H₀": "hache cero"})

vid("formula-temperatura", "Corregir una placa por temperatura", "Una fórmula para todo", CAL, "temperatura", [
  S(C, "¿Sabías que una sola fórmula corrige la potencia, la tensión [(voltaje)] y la corriente [(intensidad)] por temperatura?", "UNA *FÓRMULA*", A("🌡️", "potencia, tensión, corriente", "LA MISMA FÓRMULA")),
  S("la fórmula", "El valor a veinticinco grados... por uno, más el coeficiente por la diferencia de *temperatura.*", "LA *FÓRMULA*",
    B("X(T) = X(25)·(1 + c·(T−25))", "c en tanto por uno por grado"), 1),
  S("el signo", "El coeficiente lleva su *signo:* la corriente es positivo, y la tensión y la potencia, *negativo.*", "EL *SIGNO*",
    F(("➕", "Corriente", "COEFICIENTE +", None, "positivo,"), ("➖", "Tensión y potencia", "COEFICIENTE −", True, "negativo.")), 2),
  S("ejemplo", "Ejemplo: treinta watios a cuarenta y cinco grados, con menos cero coma treinta y ocho por ciento: veintisiete coma *siete.*", "*EJEMPLO*",
    B("30·(1 − 0,0038·20) = 27,7 W", "potencia a 45 °C"), 3),
  S("ojo", "Y ojo: el porcentaje, pásalo a tanto por *uno.* Cero coma treinta y ocho por ciento... es cero coma cero cero treinta y *ocho.*", "TANTO POR *UNO*",
    A("➗", "−0,38 % → −0,0038", "DIVIDE ENTRE 100", "¡OJO!"), 3),
  S(R, "Así que ya sabes. Valor a veinticinco... por uno más coeficiente por la *diferencia.*", RT, B("X(25)·(1 + c·ΔT)", "corrección por temperatura")),
])

vid("horas-sol-pico", "Las horas de sol pico", "Pasar radiación a horas", CAL, "radiación", [
  S(C, "¿Sabías que la radiación de un día entero... se puede contar en *horas?*", "EN *HORAS*", A("⏱️", "horas de sol pico", "HSP")),
  S("la idea", "Una hora de sol pico es una hora con mil watios por metro cuadrado: el sol *perfecto.*", "EL SOL *PERFECTO*",
    A("☀️", "1000 W/m² durante 1 hora", "1 HORA DE SOL PICO"), 1),
  S("la cuenta", "Así que coges la radiación del día... y la divides entre *mil.*", "LA *CUENTA*",
    B("HSP = H / 1000", "H en Wh/m² · resultado en horas"), 2),
  S("ejemplo", "Mil novecientos cuarenta y cuatro entre mil... casi dos horas de sol *perfecto.*", "*EJEMPLO*",
    B("1944 / 1000 = 1,94 h", "horas de sol pico"), 2),
  S("para qué", "Y lo bueno: las placas dan su potencia nominal con ese sol. Así que energía es potencia por esas *horas.*", "PARA *QUÉ*",
    B("E = P · HSP", "energía de la placa en un día"), 3),
  S(R, "Así que ya sabes. Radiación entre *mil*... y ya tienes las horas de sol *pico.*", RT, B("H / 1000", "horas de sol pico")),
])

vid("energia-con-mppt", "La energía de una placa con MPPT", "Rendimiento, potencia y horas", CAL, "MPPT", [
  S(C, "¿Sabías que con un MPPT la energía de una placa sale de multiplicar solo *tres* cosas?", "TRES *COSAS*", A("🧮", "con MPPT", "3 FACTORES")),
  S("la fórmula", "Rendimiento del MPPT... por la potencia máxima a esa temperatura... por las horas de sol *pico.*", "LA *FÓRMULA*",
    B("E = REND · Pmpp(T) · HSP", "energía de una placa al día"), 1),
  S("el peor caso", "La temperatura, la más *alta:* con calor la potencia máxima baja, y ese es el peor caso.", "EL *PEOR* CASO",
    A("🥵", "con MPPT", "TEMPERATURA MÁXIMA"), 2),
  S("serie o paralelo", "Y con MPPT da *igual* poner las placas en serie o en paralelo: la energía total es la misma.", "SERIE = *PARALELO*",
    A("🟰", "con MPPT", "SERIE = PARALELO"), 3),
  S("ojo", "Ojo: si el MPPT consume, su potencia por veinticuatro horas se *suma* al consumo.", "SU *CONSUMO*",
    A("➕", "P del MPPT · 24 h", "SE SUMA AL CONSUMO", "¡OJO!"), 4),
  S(R, "Así que ya sabes. Rendimiento, por potencia máxima, por horas de *sol.*", RT, B("REND · Pmpp · HSP", "energía con MPPT")),
], pron={"Pmpp(T)": "pe eme pe pe"})

vid("energia-directa", "La energía de una placa en directa", "Aquí manda la batería", CAL, "directa", [
  S(C, "¿Sabías que en conexión directa a la batería... la potencia máxima de la placa *no* sirve?", "SIN *MPPT*", A("🔌", "placa directa a batería", "NO SIRVE Pmpp")),
  S("por qué", "La batería *obliga* a la placa a ir a su tensión [(voltaje)]... y ahí la placa da casi su corriente de *cortocircuito.*", "MANDA LA *BATERÍA*",
    A("🔋", "la placa trabaja a la tensión de la batería", "DA CASI Icc"), 1),
  S("la fórmula", "Así que energía es tensión de batería... por corriente de cortocircuito... por horas de *sol.* Sin rendimiento.", "LA *FÓRMULA*",
    B("E = Vbat · Icc(T) · HSP", "sin rendimiento · por cada columna en serie"), 2),
  S("el peor caso", "El peor caso: la tensión de batería *mínima*... y la temperatura más *baja,* porque con frío la corriente baja.", "EL *PEOR* CASO",
    F(("🔋", "Batería", "TENSIÓN MÍNIMA", None, "mínima..."), ("🥶", "Temperatura", "MÍNIMA", True, "baja,")), 3),
  S("en serie", "Y poner más placas en serie de las necesarias *no* da más energía: la tensión la sigue fijando la batería.", "MÁS EN SERIE *NO*",
    A("🚫", "más placas en serie", "NO DA MÁS ENERGÍA"), 4),
  S(R, "Así que ya sabes. Directa: tensión de batería por corriente de *cortocircuito*... y sin *rendimiento.*", RT, B("Vbat · Icc · HSP", "energía en directa")),
], pron={"Pmpp": "pe eme pe pe", "Icc": "i ce ce"})

vid("mejor-de-los-peores", "Cómo elegir la inclinación de todo el año", "El mejor de los peores", CAL, "inclinación", [
  S(C, "¿Sabías que la mejor inclinación para todo el año se elige pensando en el *peor* mes?", "EL *PEOR* MES", A("📅", "sistema autónomo", "TODO EL AÑO")),
  S("paso uno", "Para cada inclinación, calculas cuántas placas harían falta en cada *mes.*", "PASO *1*",
    A("🧮", "inclinación × mes", "N = CONSUMO / ENERGÍA"), 1),
  S("paso dos", "En cada fila te quedas con el peor mes: el que pide *más* placas. Ese es el que manda.", "PASO *2*",
    A("📉", "en cada inclinación", "EL MES QUE PIDE MÁS"), 2),
  S("paso tres", "Y entre esas inclinaciones, eliges la que pide *menos.* El mejor... de los *peores.*", "PASO *3*",
    A("🏆", "comparas las filas", "EL MEJOR DE LOS PEORES"), 3),
  S("redondeo", "Por último, el número de placas siempre hacia *arriba:* cero coma siete... es *una* placa.", "HACIA *ARRIBA*",
    B("0,73 → 1", "placas: siempre hacia arriba"), 4),
  S(R, "Así que ya sabes. El peor mes de cada inclinación... y de ahí, el *mejor.*", RT,
    F(("📉", "Por fila", "EL PEOR MES", None, "inclinación..."), ("🏆", "Entre filas", "EL MEJOR", True, "mejor."))),
])

vid("capacidad-bateria", "Qué batería necesita tu placa", "Días, consumo y descarga", CAL, "batería", [
  S(C, "¿Sabías que una batería solar se calcula para aguantar *días* sin sol?", "DÍAS *SIN SOL*", A("☁️", "días de autonomía", "LA BATERÍA AGUANTA")),
  S("la fórmula", "Capacidad: días de autonomía por consumo diario... entre tensión de batería por profundidad de *descarga.*", "LA *FÓRMULA*",
    B("Q ≥ días · E / (Vbat · PD)", "capacidad en amperios hora"), 1),
  S("la profundidad", "La profundidad de descarga es cuánto la dejas *vaciar.* Si es el setenta por ciento... divides entre cero coma *siete.*", "LA *PROFUNDIDAD*",
    A("🪫", "cuánto la dejas vaciar", "PD = 0,7 → ÷ 0,7"), 2),
  S("ejemplo", "Seis días, treinta y dos watios hora, doce voltios, setenta por ciento: veintidós coma nueve amperios *hora.*", "*EJEMPLO*",
    B("6·32 / (12·0,7) = 22,9 Ah", "capacidad mínima"), 3),
  S("peor caso", "Y el peor caso: la tensión de batería *mínima*... porque con menos voltios necesitas más amperios hora.", "EL *PEOR* CASO",
    A("🔋", "si la tensión varía", "USA LA MÍNIMA", "¡OJO!"), 4),
  S(R, "Así que ya sabes. Días por consumo, entre tensión por *profundidad* de descarga.", RT, B("días · E / (V · PD)", "capacidad de la batería")),
], pron={"Q": "cu", "E": "e", "Vbat": "uve bat", "PD": "pe de"})

# ======================= BATERÍAS =======================
vid("quimica-o-no", "Qué guarda energía con química", "Baterías, pilas de combustible y supercondensadores", BAT, "almacenamiento", [
  S(C, "¿Sabías que un supercondensador guarda energía... *sin* ninguna reacción química?", "SIN *QUÍMICA*", A("🧪", "¿química o no?", "3 DISPOSITIVOS")),
  S("con química", "Las *baterías* y las pilas de *combustible* sí funcionan con reacciones químicas.", "CON *QUÍMICA*",
    F(("🔋", "Baterías", "QUÍMICA", None, "baterías"), ("⛽", "Pilas de combustible", "QUÍMICA", True, "combustible")), 1),
  S("sin química", "El supercondensador no: solo *desplaza* iones, que se pegan a sus placas. Nada se transforma.", "SIN *QUÍMICA*",
    A("⚡", "solo desplaza iones", "SUPERCONDENSADOR"), 2),
  S("la consecuencia", "Y como no se desgasta con reacciones... aguanta muchísimos más *ciclos* que una batería.", "MÁS *CICLOS*",
    A("♾️", "no hay reacción que lo gaste", "VIDA ÚTIL MAYOR"), 3),
  S(R, "Así que ya sabes. Baterías y pilas de combustible, química. Supercondensador, *iones*... y más *vida.*", RT,
    F(("🧪", "Baterías y pilas", "QUÍMICA", None, "química."), ("⚡", "Supercondensador", "IONES · MÁS VIDA", True, "vida.")))
])

vid("supercondensador-ventajas", "Supercondensador contra batería", "Quién gana en qué", BAT, "almacenamiento", [
  S(C, "¿Sabías que el supercondensador gana a la batería en algunas cosas... pero en otras *pierde?*", "QUIÉN *GANA*", A("🥊", "supercondensador vs batería", "CARA A CARA")),
  S("gana", "Gana en *ciclos:* aguanta cientos de miles de cargas. Y su resistencia interna es más *baja.*", "GANA EN",
    F(("♾️", "Ciclos de vida", "MUCHOS MÁS", True, "ciclos:"), ("⚡", "Resistencia interna", "MÁS BAJA", None, "baja.")), 1),
  S("pierde", "Pierde en *energía:* para el mismo tamaño guarda mucha menos que una batería.", "PIERDE EN",
    A("🪫", "densidad de energía", "MUCHO MENOR"), 2),
  S("la descarga", "Y su tensión [(voltaje)] no es constante: al descargarse va cayendo en *línea* recta, como un condensador.", "LA *DESCARGA*",
    A("📉", "la tensión cae en recta", "NO ES CONSTANTE", "¡OJO!"), 3),
  S(R, "Así que ya sabes. Su gran ventaja son los *ciclos*... no la *energía.*", RT,
    F(("✅", "Ventaja", "MÁS CICLOS", True, "ciclos..."), ("❌", "No", "MÁS ENERGÍA", None, "energía."))),
])

vid("carga-segun-quimica", "Cómo se carga cada batería", "Plomo, litio y níquel", BAT, "carga", [
  S(C, "¿Sabías que cada tipo de batería tiene su propia forma de *cargarse?*", "CADA UNA *A SU MANERA*", A("🔌", "plomo, litio, níquel", "3 FORMAS")),
  S("plomo", "La de *plomo* es la más flexible: a tensión [(voltaje)] constante... o corriente constante y luego tensión constante.", "*PLOMO*",
    A("🚗", "tensión constante o CC/CV", "DOS OPCIONES"), 1),
  S("litio", "La de *litio* solo admite una: corriente [(intensidad)] constante y luego tensión constante. Solo esa.", "*LITIO*",
    A("📱", "corriente constante → tensión constante", "SOLO CC/CV"), 2),
  S("níquel", "Y la de níquel metal hidruro, al revés: solo corriente *constante,* y se corta por temperatura.", "*NÍQUEL*",
    A("🔋", "y se corta por temperatura", "SOLO CORRIENTE CONSTANTE"), 3),
  S(R, "Así que ya sabes. Plomo, las *dos.* Litio, CC/CV. Níquel, corriente *constante.*", RT,
    F(("🚗", "Plomo", "CV o CC/CV", None, "dos."), ("📱", "Litio", "SOLO CC/CV", True, "CC/CV."), ("🔋", "NiMH", "SOLO CC", None, "constante."))),
], pron={"CC/CV": "ce ce, ce uve"})

vid("arranque-traccion-estacionaria", "Arranque, tracción y estacionaria", "Tres baterías para tres trabajos", BAT, "tipos", [
  S(C, "¿Sabías que la batería de un coche y la de un carrito de golf... están hechas *distinto?*", "HECHAS *DISTINTO*", A("🚗", "arranque, tracción, estacionaria", "3 TRABAJOS")),
  S("arranque", "La de *arranque* da mucha corriente [(intensidad)] de golpe: placas finas, más superficie... y menos electrolito.", "*ARRANQUE*",
    F(("⚡", "Necesita", "ALTA CORRIENTE", True, "golpe:"), ("📄", "Por dentro", "+ SUPERFICIE, − ELECTROLITO", None, "electrolito.")), 1),
  S("tracción", "La de *tracción* mueve vehículos durante horas: lo suyo es la descarga *profunda.*", "*TRACCIÓN*",
    A("🛺", "carritos, carretillas...", "DESCARGA PROFUNDA"), 2),
  S("estacionaria", "Y para una instalación solar aislada, la *estacionaria:* ciclos lentos y profundos, día tras día.", "*ESTACIONARIA*",
    A("🏠", "instalación solar autónoma", "ESTACIONARIA"), 3),
  S(R, "Así que ya sabes. Arranque, *corriente.* Tracción, *profundidad.* Y la solar, *estacionaria.*", RT,
    F(("⚡", "Arranque", "CORRIENTE", None, "corriente."), ("🛺", "Tracción", "PROFUNDIDAD", None, "profundidad."), ("🏠", "Solar", "ESTACIONARIA", True, "estacionaria."))),
])

vid("balanceo-en-un-minuto", "Balanceo pasivo y activo", "Quemar o repartir", BAT, "balanceo", [
  S(C, "¿Sabías que las celdas de una batería nunca se cargan exactamente *igual?*", "NUNCA *IGUALES*", A("⚖️", "celdas en serie", "HAY QUE IGUALARLAS")),
  S("pasivo", "El balanceo *pasivo* es el bruto: a la celda más cargada le pone una resistencia... y *quema* lo que le sobra.", "*PASIVO*",
    A("🔥", "resistencia en la más cargada", "DISIPA ENERGÍA"), 1),
  S("activo", "El *activo* es el listo: con un convertidor conmutado *pasa* energía de la más cargada a la menos.", "*ACTIVO*",
    A("🔁", "convertidor conmutado", "TRANSFIERE ENERGÍA"), 2),
  S("la trampa", "No tiene nada que ver con corrientes de sostenimiento ni con descansos durante la carga. Eso es *otra* cosa.", "LA *TRAMPA*",
    A("🚫", "ni sostenimiento ni descansos", "NO ES BALANCEO", "¡OJO!"), 3),
  S(R, "Así que ya sabes. Pasivo, *quema.* Activo, *reparte.*", RT,
    F(("🔥", "Pasivo", "QUEMA EN UNA RESISTENCIA", None, "quema."), ("🔁", "Activo", "REPARTE CON UN CONVERTIDOR", True, "reparte."))),
])

vid("autodescarga-y-modelo", "Por qué se descarga una batería guardada", "Autodescarga y su modelo", BAT, "baterías", [
  S(C, "¿Sabías que una batería guardada en un cajón... se va *vaciando* sola?", "SE VACÍA *SOLA*", A("🗄️", "sin usarla", "AUTODESCARGA")),
  S("por qué", "Es la autodescarga: pequeñas reacciones *químicas* que siguen ocurriendo dentro, aunque no la uses.", "REACCIONES *QUÍMICAS*",
    A("🧪", "siguen ocurriendo", "AUTODESCARGA"), 1),
  S("el frío", "Y como toda reacción química, con *frío* va más lenta. Por eso la autodescarga baja al bajar la *temperatura.*", "CON FRÍO, *MENOS*",
    A("🥶", "menos temperatura", "MENOS AUTODESCARGA"), 2),
  S("el modelo", "Otra cosa: por dentro, una batería se modela como una resistencia en *serie*... con grupos de resistencia y condensador en *paralelo.*", "EL *MODELO*",
    B("R + RC + RC", "R en serie con grupos RC en paralelo"), 3),
  S(R, "Así que ya sabes. Autodescarga: baja con el *frío.* Y el modelo: R en serie con grupos R C en *paralelo.*", RT,
    F(("🥶", "Autodescarga", "BAJA CON FRÍO", None, "frío."), ("🔧", "Modelo", "R + GRUPOS RC", True, "paralelo."))),
], pron={"R": "erre", "C": "ce"})

# ======================= PROTECCIONES =======================
vid("tt-tn-en-un-minuto", "Redes TT y TN", "A tierra o al neutro", PRO, "redes", [
  S(C, "¿Sabías que el cable de tierra de tu enchufe no va al mismo sitio en *todos* los países?", "¿A DÓNDE *VA?*", A("🔌", "conductor de protección", "TT O TN")),
  S("TT", "En la red TT, la protección va a *tierra.* Un defecto da poca corriente [(intensidad)]... y la detecta el *diferencial.*", "RED *TT*",
    F(("🌍", "Protección a", "TIERRA", None, "tierra."), ("🛡️", "Choques eléctricos", "DIFERENCIAL", True, "diferencial.")), 1),
  S("TN", "En una red TN va al *neutro.* Un defecto es un cortocircuito... y salta el *magnetotérmico.*", "RED *TN*",
    F(("🔵", "Protección a", "NEUTRO", None, "neutro."), ("⚡", "Choques eléctricos", "MAGNETOTÉRMICO", True, "magnetotérmico.")), 2),
  S("sobrecorrientes", "Y las sobrecorrientes, en las dos redes, siempre con *magnetotérmico.*", "SOBRE*CORRIENTES*",
    A("⚡", "en TT y en TN", "MAGNETOTÉRMICO"), 3),
  S(R, "Así que ya sabes. TT: tierra y *diferencial.* TN: neutro y *magnetotérmico.*", RT,
    F(("🌍", "TT", "TIERRA + DIFERENCIAL", None, "diferencial."), ("🔵", "TN", "NEUTRO + MAGNETOTÉRMICO", True, "magnetotérmico."))),
])

vid("paises-tt-tn", "Italia o Alemania", "Qué red usa cada país", PRO, "redes", [
  S(C, "¿Sabías que en Alemania y en Italia los enchufes están protegidos de forma *distinta?*", "DOS *PAÍSES*", A("🗺️", "Alemania vs Italia", "TN O TT")),
  S("cálidos", "En países *cálidos,* como Italia o España, se suele usar la red *TT*... con interruptores diferenciales.", "PAÍSES *CÁLIDOS*",
    A("☀️", "Italia, España", "TT + DIFERENCIAL"), 1),
  S("fríos", "En países *fríos,* como Alemania, se usa la red *TN*... y el magnetotérmico protege también de los choques.", "PAÍSES *FRÍOS*",
    A("❄️", "Alemania", "TN + MAGNETOTÉRMICO"), 2),
  S("truco", "Truco para acordarte: el *diferencial,* con el calor del sur. El *magnetotérmico,* con el frío del norte.", "EL *TRUCO*",
    F(("☀️", "Cálido", "TT · DIFERENCIAL", None, "diferencial,"), ("❄️", "Frío", "TN · MAGNETOTÉRMICO", True, "magnetotérmico,")), 3),
  S(R, "Así que ya sabes. Italia, TT y *diferencial.* Alemania, TN y *magnetotérmico.*", RT,
    F(("☀️", "Italia", "TT + DIFERENCIAL", None, "diferencial."), ("❄️", "Alemania", "TN + MAGNETOTÉRMICO", True, "magnetotérmico."))),
])

vid("rayo-o-neutro-cortado", "Rayo o neutro cortado", "Sobretensión corta o larga", PRO, "sobretensiones", [
  S(C, "¿Sabías que hay sobretensiones que duran *microsegundos*... y otras que no se van?", "CORTAS Y *LARGAS*", A("⚡", "dos tipos de sobretensión", "CORTA O LARGA")),
  S("el rayo", "Un rayo sobre una línea da una sobretensión *corta.* Y es más probable en líneas *aéreas,* que están expuestas.", "EL *RAYO*",
    F(("⏱️", "Duración", "CORTA", True, "corta."), ("🗼", "Más probable en", "LÍNEAS AÉREAS", None, "aéreas,")), 1),
  S("cómo se para", "Como es corta, se para con limitadores o descargadores en *paralelo* con la carga.", "EN *PARALELO*",
    A("🛡️", "limitadores o descargadores", "EN PARALELO"), 2),
  S("el neutro", "Si se corta el *neutro,* la sobretensión se queda: es *larga.* Ningún limitador aguanta eso.", "EL *NEUTRO*",
    A("✂️", "neutro desconectado", "SOBRETENSIÓN LARGA"), 3),
  S("la solución", "La única solución es *desconectar* la red.", "*DESCONECTAR*", A("🔌", "sobretensión larga", "DESCONECTAR LA RED", "¡OJO!"), 3),
  S(R, "Así que ya sabes. Rayo: corta y *limitador.* Neutro cortado: larga y *desconectar.*", RT,
    F(("⚡", "Rayo", "CORTA · LIMITADOR", None, "limitador."), ("✂️", "Neutro", "LARGA · DESCONECTAR", True, "desconectar."))),
])

vid("tipos-1-2-3", "Protectores tipo 1, 2 y 3", "Quién aguanta qué", PRO, "sobretensiones", [
  S(C, "¿Sabías que el protector que aguanta un rayo directo... no sirve para proteger tu *ordenador?*", "AGUANTA, *PERO...*", A("🛡️", "protectores de sobretensión", "TIPO 1, 2 Y 3")),
  S("tipo 1", "El *tipo 1* aguanta rayos directos... pero deja pasar demasiada tensión [(voltaje)] para los equipos sensibles, los de categoría *uno.*", "TIPO *1*",
    F(("⚡", "Rayo directo", "SÍ", None, "directos..."), ("💻", "Categoría I", "NO", True, "uno.")), 1),
  S("tipo 2", "El *tipo 2* solo aguanta rayos indirectos... y tampoco protege la categoría *uno.*", "TIPO *2*",
    F(("⚡", "Rayo directo", "NO", None, "indirectos..."), ("💻", "Categoría I", "NO", True, "uno.")), 2),
  S("tipo 3", "El *tipo 3* solo aguanta indirectos... pero es el único que sí protege la categoría *uno.*", "TIPO *3*",
    F(("⚡", "Rayo directo", "NO", None, "indirectos..."), ("💻", "Categoría I", "SÍ", True, "uno.")), 3),
  S(R, "Así que ya sabes. Tipo uno, el *rayo.* Tipo tres, el *equipo.* Y el dos, ninguna de las dos.", RT,
    F(("1️⃣", "Tipo 1", "AGUANTA EL DIRECTO", None, "rayo."), ("2️⃣", "Tipo 2", "SOLO INDIRECTOS", None, "dos."), ("3️⃣", "Tipo 3", "PROTEGE CATEGORÍA I", True, "equipo."))),
])

vid("proteger-un-ordenador", "Cómo proteger un ordenador de un rayo", "Directo o indirecto", PRO, "sobretensiones", [
  S(C, "¿Sabías que para proteger un ordenador de un rayo... a veces basta con *uno* y a veces hacen falta *dos?*", "¿UNO O *DOS?*", A("💻", "ordenador", "¿QUÉ PROTECTOR?")),
  S("indirecto", "Si el rayo es *indirecto,* basta un *tipo 3* junto al ordenador: aguanta indirectos y protege la categoría uno.", "RAYO *INDIRECTO*",
    A("3️⃣", "rayo indirecto", "BASTA UN TIPO 3"), 1),
  S("directo", "Si es *directo,* el tipo 3 no aguanta. Necesitas un *tipo 1* en la entrada para el golpe gordo.", "RAYO *DIRECTO*",
    A("1️⃣", "en la entrada", "TIPO 1 PARA EL GOLPE"), 2),
  S("los dos", "Pero el tipo 1 deja pasar demasiado para el ordenador... así que también el tipo 3. Hacen falta los *dos.*", "LOS *DOS*",
    F(("1️⃣", "Entrada", "TIPO 1", None, None), ("3️⃣", "Junto al ordenador", "TIPO 3", True, "dos.")), 3),
  S(R, "Así que ya sabes. Indirecto: tipo *tres.* Directo: tipo uno más tipo *tres.*", RT,
    F(("☁️", "Indirecto", "TIPO 3", None, "tres."), ("⚡", "Directo", "TIPO 1 + TIPO 3", True, "tres."))),
])

vid("serie-o-paralelo-protecciones", "En serie o en paralelo", "La regla de las protecciones", PRO, "dispositivos", [
  S(C, "¿Sabías que con saber de qué protege un dispositivo... ya sabes cómo se *conecta?*", "UNA *REGLA*", A("🔌", "protecciones", "¿SERIE O PARALELO?")),
  S("sobretensión", "Contra *sobretensiones,* en *paralelo:* el dispositivo se pone a conducir y desvía el exceso.", "SOBRETENSIÓN → *PARALELO*",
    A("⚡", "desvía el exceso", "EN PARALELO"), 1),
  S("sobrecorriente", "Contra *sobrecorrientes,* en *serie:* toda la corriente [(intensidad)] pasa por él, y él la corta.", "SOBRECORRIENTE → *SERIE*",
    A("🔗", "corta el paso", "EN SERIE"), 2),
  S("ejemplos", "El varistor, o MOV, es un *limitador* de sobretensión: en paralelo. El bimetal y el PPTC protegen de sobrecorriente: en *serie.*", "LOS *EJEMPLOS*",
    F(("⚡", "MOV / varistor", "PARALELO · LIMITADOR", None, "limitador"), ("🔥", "Bimetal", "SERIE", True, None), ("♻️", "PPTC", "SERIE", True, "serie.")), 3),
  S(R, "Así que ya sabes. Tensión, en *paralelo.* Corriente, en *serie.*", RT,
    F(("⚡", "Sobretensión", "EN PARALELO", None, "paralelo."), ("🔗", "Sobrecorriente", "EN SERIE", True, "serie."))),
])

vid("arranque-proteccion-lenta", "Por qué no salta al arrancar un motor", "Protecciones lentas", PRO, "dispositivos", [
  S(C, "¿Sabías que al encender un motor hay un pico de corriente [(intensidad)] enorme... y la protección *no* debe saltar?", "QUE *NO* SALTE", A("⚙️", "transitorio de arranque", "PICO NORMAL")),
  S("el problema", "Ese pico es *normal:* dura un momento. Si la protección fuera rápida... saltaría cada vez que *enciendes.*", "EL *PROBLEMA*",
    A("⏱️", "dura un momento", "PICO NORMAL"), 1),
  S("la solución", "Por eso se usan dispositivos *lentos*... que suelen ser *térmicos:* necesitan tiempo para calentarse.", "*LENTOS* Y TÉRMICOS",
    A("🔥", "necesitan tiempo para calentarse", "LENTO = TÉRMICO"), 2),
  S("los rápidos", "Los *rápidos* suelen ser magnéticos: esos son para los cortocircuitos de verdad.", "LOS *RÁPIDOS*",
    F(("🐢", "Lento", "TÉRMICO · ARRANQUES", None, None), ("⚡", "Rápido", "MAGNÉTICO · CORTOCIRCUITOS", True, "magnéticos:")), 3),
  S(R, "Así que ya sabes. Arranques, protección *lenta* y *térmica.*", RT, B("LENTO = TÉRMICO", "para los transitorios de arranque")),
])

if __name__ == "__main__":
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gratis")
    os.makedirs(d, exist_ok=True)
    for v in V:
        with open(os.path.join(d, v["id"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=False, indent=1)
    print(len(V), "specs →", d)
