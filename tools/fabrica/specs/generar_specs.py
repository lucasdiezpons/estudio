#!/usr/bin/env python3
"""Genera los specs JSON de los vídeos de CESA (estilo curiosidad)."""
import json
from pathlib import Path

D = Path(__file__).parent

def A(icono, l1, l2, stamp=None):
    v = {"tipo": "alerta", "icono": icono, "linea1": l1, "linea2": l2}
    if stamp: v["stamp"] = stamp
    return v

def F(*filas, stamp=None):
    v = {"tipo": "filas", "filas": [dict(zip(("icono", "izq", "der", "rojo", "en"), f)) for f in filas]}
    for r in v["filas"]:
        if r.get("en") is None: r.pop("en", None)
    if stamp: v["stamp"] = stamp
    return v

def B(big, small):
    return {"tipo": "big", "big": big, "small": small}

def S(tag, sub, titulo, visual, num=None):
    s = {"tag": tag, "sub": sub, "titulo": titulo, "visual": visual}
    if num: s["num"] = num
    return s

V = []

# 1 · Normativa
V.append(dict(id="cesa-normas-reglamentos-ce", titulo="Norma, reglamento y marcado CE", texto="Qué es obligatorio y qué no",
  tema="CESA · Normativa", etiqueta="normativa", pron={"UNE": "une", "CE": "ce e", "CE?": "ce e"},
  segmentos=[
    S("la curiosidad", "¿Sabías que cumplir una *norma* técnica no es obligatorio? Lo que sí es obligatorio... es otra cosa.", "NORMA *NO* ES LEY", A("📜", "una norma es una recomendación", "¿OBLIGATORIA? NO")),
    S("las normas", "Las *normas,* como las UNE, las escriben *comités* técnicos. Son recomendaciones... nadie te obliga a seguirlas.", "*NORMAS*",
      F(("📘", "Quién las escribe", "COMITÉS TÉCNICOS", None, "comités"), ("🤷", "¿Obligatorias?", "NO, VOLUNTARIAS", True, "recomendaciones...")), 1),
    S("los reglamentos", "Los *reglamentos,* en cambio, los dicta el *Gobierno.* Por ejemplo, un Real Decreto. Y esos sí son *obligatorios.*", "*REGLAMENTOS*",
      F(("🏛️", "Quién los dicta", "EL GOBIERNO", None, "Gobierno."), ("⚖️", "¿Obligatorios?", "SÍ, SIEMPRE", True, "obligatorios.")), 2),
    S("el marcado CE", "¿Y el famoso marcado *CE?* Es obligatorio para vender un producto... pero no lo pone ningún *laboratorio.*", "MARCADO *CE*",
      A("🏷️", "obligatorio para vender en Europa", "NINGÚN LABORATORIO"), 3),
    S("el marcado CE", "Lo pone el propio *fabricante.* Junto con la Declaración de Conformidad, dice: si esto incumple la ley... el responsable soy *yo.*", "LO FIRMA EL *FABRICANTE*",
      A("✍️", "Declaración de Conformidad", "RESPONSABLE: EL FABRICANTE", "OBLIGATORIO"), 3),
    S("el marcado CE", "Y esa declaración se entrega para *todos* los productos... y habla de cumplir los *reglamentos,* no las normas.", "PARA *TODO* PRODUCTO",
      F(("📦", "¿Qué productos?", "TODOS", True, "todos"), ("⚖️", "¿Cumplir qué?", "LOS REGLAMENTOS", None, "reglamentos,")), 3),
    S("en resumen", "Así que ya sabes. Norma: *recomendación.* Reglamento: *obligatorio.*", "EN *RESUMEN*",
      F(("📘", "Norma · comité técnico", "RECOMENDACIÓN", None, "recomendación."), ("🏛️", "Reglamento · Gobierno", "OBLIGATORIO", True, "obligatorio."))),
  ]))

# 2 · Celda por dentro
V.append(dict(id="cesa-celda-por-dentro", titulo="Una placa solar a oscuras es un diodo", texto="Qué pasa dentro de una celda solar",
  tema="CESA · Fotovoltaica", etiqueta="energía solar", pron={"PN": "pe ene", "PN.": "pe ene", "P": "pe", "N": "ene"},
  segmentos=[
    S("la curiosidad", "¿Sabías que una placa solar, a *oscuras,* se comporta igual que un *diodo?*", "A OSCURAS = *DIODO*", A("🌑", "celda solar sin luz", "UN DIODO (UNIÓN PN)")),
    S("por dentro", "Por dentro, una celda es una unión *PN.* Una zona P y una zona N... pegadas.", "UNIÓN *PN*",
      F(("➕", "Zona P", "HUECOS"), ("➖", "Zona N", "ELECTRONES", True)), 1),
    S("la zona clave", "Justo en medio aparece la zona de carga *espacial.* Ahí hay un campo eléctrico... y es donde la luz se convierte en *corriente* [(intensidad).]", "LA ZONA *CLAVE*",
      A("⚡", "un campo eléctrico separa las cargas", "ZONA DE CARGA ESPACIAL"), 1),
    S("difusión", "Además hay otra corriente curiosa: la de *difusión.* Las cargas se mueven solas... de donde hay muchas, a donde hay *pocas.*", "*DIFUSIÓN*",
      A("🫧", "de más concentración a menos", "CORRIENTE DE DIFUSIÓN"), 2),
    S("difusión", "Como una gota de *tinta* en un vaso de agua... se reparte sola, sin que nadie la *empuje.*", "COMO LA *TINTA*",
      A("💧", "sin campo eléctrico, solo concentración", "SE REPARTE SOLA"), 2),
    S("en resumen", "Así que ya sabes. Sin luz, una celda es un *diodo.* Y la magia pasa en la zona de carga *espacial.*", "EN *RESUMEN*",
      F(("🌑", "Celda sin luz", "UN DIODO", True, "diodo."), ("⚡", "Dónde se genera", "ZONA DE CARGA ESPACIAL", None, "espacial."))),
  ]))

# 3 · Temperatura y Fill Factor
V.append(dict(id="cesa-placa-y-calor", titulo="Por qué una placa solar odia el calor", texto="Temperatura, MPPT y Fill Factor",
  tema="CESA · Fotovoltaica", etiqueta="energía solar", pron={"MPPT,": "eme pe pe te,", "MPPT": "eme pe pe te"},
  segmentos=[
    S("la curiosidad", "¿Sabías que una placa solar produce *menos* en un día de mucho calor? Aunque haga un sol *espectacular.*", "EL CALOR *RESTA*", A("🥵", "más temperatura", "MENOS POTENCIA")),
    S("qué cambia", "Con el calor, la corriente [(intensidad)] de cortocircuito *sube* un poquito. Pero la tensión [(voltaje)] de circuito abierto *baja* bastante.", "SUBE Y *BAJA*",
      F(("⬆️", "Corriente (intensidad) · Isc", "SUBE UN POCO", None, "sube"), ("⬇️", "Tensión (voltaje) · Voc", "BAJA BASTANTE", True, "baja")), 1),
    S("con MPPT", "Si usas un *MPPT,* que busca siempre el punto de máxima potencia... la potencia *baja* con el calor.", "CON *MPPT*",
      A("🌡️", "busca el punto de máxima potencia", "LA POTENCIA BAJA"), 2),
    S("conexión directa", "Pero si conectas la placa *directa* a la batería, manda la corriente [(intensidad).] Y como la corriente sube... ¡la potencia también *sube!*", "CONEXIÓN *DIRECTA*",
      A("🔋", "aquí manda la corriente (intensidad)", "LA POTENCIA SUBE", "SORPRESA"), 2),
    S("el Fill Factor", "Y para saber si una placa es buena, se mira el *Fill Factor.* La potencia máxima... dividida entre la tensión [(voltaje)] de circuito abierto por la corriente [(intensidad)] de cortocircuito.", "FILL *FACTOR*",
      B("FF", "Pmáx / (Voc · Isc)"), 3),
    S("en resumen", "Así que ya sabes. Con calor, la tensión [(voltaje)] *baja.* Y cuanto más alto el Fill Factor... *mejor* placa.", "EN *RESUMEN*",
      F(("🥵", "Con calor", "TENSIÓN (VOLTAJE) BAJA", True, "baja."), ("📈", "Fill Factor alto", "MEJOR PLACA", None, "mejor"))),
  ]))

# 4 · Inclinación
V.append(dict(id="cesa-inclinacion-placas", titulo="Cuánto inclinar una placa solar", texto="Verano, invierno y hemisferio sur",
  tema="CESA · Fotovoltaica", etiqueta="energía solar",
  pron={"55°.": "cincuenta y cinco grados.", "15°.": "quince grados.", "55°": "cincuenta y cinco grados", "15°": "quince grados"},
  segmentos=[
    S("la curiosidad", "¿Sabías que la misma placa solar hay que inclinarla *distinto* en verano que en *invierno?*", "¿CUÁNTO *INCLINO*?", A("📐", "depende de la estación del año", "VERANO VS INVIERNO")),
    S("invierno", "En *invierno,* el sol va muy bajo. Así que la placa se pone muy *inclinada...* unos 55°.", "INVIERNO: *55°*", B("55°", "sol bajo · placa muy inclinada"), 1),
    S("verano", "En *verano,* el sol va alto. Así que la placa va casi *tumbada...* unos 15°.", "VERANO: *15°*", B("15°", "sol alto · placa casi plana"), 2),
    S("el hemisferio sur", "Pero ojo... en el hemisferio *sur,* las estaciones van al revés. En Buenos Aires, *junio* es pleno invierno.", "EL SUR, *AL REVÉS*",
      F(("❄️", "Buenos Aires · junio", "INVIERNO · 55°", True, "junio"), ("☀️", "Buenos Aires · diciembre", "VERANO · 15°")), 3),
    S("el hemisferio sur", "Y allí la placa no mira al sur... mira al *norte,* porque es por donde pasa el sol.", "MIRA AL *NORTE*",
      A("🧭", "en el hemisferio sur", "ORIENTADA AL NORTE"), 3),
    S("en resumen", "Así que ya sabes. Sol bajo, placa *inclinada.* Sol alto, placa *tumbada.*", "EN *RESUMEN*",
      F(("❄️", "Invierno · sol bajo", "UNOS 55°", True, "inclinada."), ("☀️", "Verano · sol alto", "UNOS 15°", None, "tumbada."))),
  ]))

# 5 · Tipos de placa
V.append(dict(id="cesa-tipos-de-placa", titulo="Mono, poli y amorfa: cuál es mejor", texto="Los 3 tipos de placa solar",
  tema="CESA · Fotovoltaica", etiqueta="energía solar", pron={},
  segmentos=[
    S("la curiosidad", "¿Sabías que no todas las placas solares son iguales? Hay tres tipos... y se distinguen a simple *vista.*", "3 TIPOS DE *PLACA*", B("3", "tipos de placa solar")),
    S("monocristalina", "La *monocristalina:* un solo cristal perfecto. Es la que más rinde... y la más *cara.*", "*MONO*CRISTALINA",
      F(("🥇", "Rendimiento", "EL MÁS ALTO", True, "rinde..."), ("💸", "Precio", "LA MÁS CARA", None, "cara.")), 1),
    S("policristalina", "La *policristalina:* muchos cristales pequeños juntos. Rinde un poco menos... y es más *barata.*", "*POLI*CRISTALINA",
      F(("🥈", "Rendimiento", "INTERMEDIO", None, "menos..."), ("💰", "Precio", "INTERMEDIO", None, "barata.")), 2),
    S("amorfa", "Y la *amorfa:* sin red cristalina, átomos desordenados. Es la que menos rinde... pero la más *barata.*", "*AMORFA*",
      F(("🥉", "Rendimiento", "EL MÁS BAJO", None, "rinde..."), ("🪙", "Precio", "LA MÁS BARATA", True, "barata.")), 3),
    S("el truco", "El truco: cuanto más *ordenado* el cristal... más rinde, y más *cuesta.*", "EL *TRUCO*", A("🧩", "más orden en el cristal", "MÁS RINDE Y MÁS CUESTA")),
    S("en resumen", "Así que ya sabes. De mejor a peor, y de más cara a más barata... mono, poli y *amorfa.*", "EN *RESUMEN*",
      F(("1️⃣", "La mejor y más cara", "MONO", True), ("2️⃣", "En medio", "POLI"), ("3️⃣", "La peor y más barata", "AMORFA", None, "amorfa."))),
  ]))

# 6 · Celdas en serie y sombras
V.append(dict(id="cesa-celdas-y-sombras", titulo="Una hoja puede calentar tu placa solar", texto="Sombras, diodos y celdas en serie",
  tema="CESA · Fotovoltaica", etiqueta="energía solar",
  pron={"4,2": "cuatro coma dos", "4.": "cuatro.", "8": "ocho", "10.": "diez.", "0,5...": "cero coma cinco..."},
  segmentos=[
    S("la curiosidad", "¿Sabías que una sola *hoja* encima de una placa solar... puede hacer que se *caliente* peligrosamente?", "UNA *HOJA*", A("🍂", "una celda tapada", "PUNTO CALIENTE")),
    S("celdas en serie", "En una placa, las celdas van en *serie.* Si una queda a oscuras... las demás la obligan a conducir *al revés.*", "CELDAS EN *SERIE*",
      A("🔥", "la celda tapada trabaja en inverso", "SE CALIENTA", "PUNTO CALIENTE"), 1),
    S("la solución", "La solución: un diodo en *paralelo* con las celdas. El diodo de bypass. La corriente [(intensidad)] se lo salta... y *listo.*", "DIODO *BYPASS*",
      F(("🔀", "Celdas en serie", "DIODO EN PARALELO", True, "paralelo"), ("✅", "Resultado", "SIN PUNTO CALIENTE", None, "listo.")), 1),
    S("celdas en paralelo", "Si las celdas van en *paralelo,* pasa al revés: la tapada recibe corriente [(intensidad)] de las demás. Ahí el diodo va en *serie,* para bloquearla.", "EN *PARALELO*",
      F(("🔀", "Celdas en paralelo", "DIODO EN SERIE", True, "serie,"), ("🚫", "Para qué", "BLOQUEA LA CORRIENTE")), 2),
    S("cuántas celdas", "¿Y cuántas celdas en serie para cargar una batería *directamente?* Cada celda da, como mínimo, medio voltio de *tensión* [(voltaje).]", "¿CUÁNTAS *CELDAS*?",
      B("0,5 V", "tensión (voltaje) mínima por celda"), 3),
    S("cuántas celdas", "Si la batería llega a 4,2 voltios... con 8 celdas solo llegas a 4. Te quedas *corto.* Necesitas *10.*", "NI UNA *MENOS*",
      F(("❌", "8 celdas × 0,5 V", "4 V · TE QUEDAS CORTO", None, "corto."), ("✅", "10 celdas × 0,5 V", "5 V · TE SOBRA", True, "10.")), 3),
    S("en resumen", "Así que ya sabes. Divide la tensión [(voltaje)] máxima de la batería entre 0,5... y redondea hacia *arriba.*", "LA *REGLA*",
      F(("➗", "Tensión (voltaje) máx. ÷ 0,5", "REDONDEA ARRIBA", True, "arriba."), ("🍂", "Celdas en serie + sombra", "DIODO EN PARALELO"))),
  ]))

# 7 · Supercondensador
V.append(dict(id="cesa-supercondensador", titulo="Supercondensador vs batería", texto="Química, iones y autodescarga",
  tema="CESA · Baterías", etiqueta="baterías", pron={},
  segmentos=[
    S("la curiosidad", "¿Sabías que hay algo que se carga y descarga cientos de miles de veces... casi sin gastarse? Se llama *supercondensador.*", "*SUPER*CONDENSADOR",
      A("⚡", "cientos de miles de ciclos", "SUPERCONDENSADOR")),
    S("la batería", "Una batería, o una pila de combustible, funcionan con reacciones *químicas.* Y la química... se va *desgastando.*", "BATERÍA = *QUÍMICA*",
      F(("🔋", "Batería", "REACCIÓN QUÍMICA", None, "químicas."), ("⛽", "Pila de combustible", "REACCIÓN QUÍMICA", True, "desgastando.")), 1),
    S("el supercondensador", "El supercondensador no tiene química. Solo mueve *iones* de un lado a otro. Por eso aguanta muchísimos más *ciclos.*", "SIN *QUÍMICA*",
      A("🔁", "solo desplaza iones", "MUCHOS MÁS CICLOS"), 2),
    S("el pero", "¿El precio? Guarda mucha menos *energía* que una batería. Y al descargarse, su tensión [(voltaje)] cae en *línea* recta.", "EL *PERO*",
      F(("📉", "Energía guardada", "MUCHA MENOS", None, "energía"), ("📏", "Tensión (voltaje) al descargar", "CAE EN LÍNEA RECTA", True, "línea")), 2),
    S("autodescarga", "Otra curiosidad: una batería se descarga *sola,* aunque no la uses. Pero si la guardas en *frío...* se descarga más despacio.", "*AUTO*DESCARGA",
      A("🧊", "las reacciones van más lentas", "FRÍO = MENOS AUTODESCARGA"), 3),
    S("el modelo", "Y por dentro, una batería se modela como una resistencia en *serie...* con grupos de resistencia y condensador en *paralelo.*", "EL *MODELO*",
      A("🧮", "su respuesta cambia con el tiempo", "R EN SERIE + GRUPOS R Y C"), 3),
    S("en resumen", "Así que ya sabes. Batería: *química.* Supercondensador: *iones...* y muchos más ciclos.", "EN *RESUMEN*",
      F(("🔋", "Batería", "QUÍMICA", None, "química."), ("⚡", "Supercondensador", "IONES · MÁS CICLOS", True, "iones..."))),
  ]))

# 8 · Cómo se carga cada batería
V.append(dict(id="cesa-como-cargar-baterias", titulo="Cada batería se carga a su manera", texto="Plomo, litio y níquel",
  tema="CESA · Baterías", etiqueta="baterías", pron={"CC/CV.": "corriente constante y tensión constante.", "NiMH": "níquel metal hidruro"},
  segmentos=[
    S("la curiosidad", "¿Sabías que la batería del coche, la del móvil y unas pilas recargables... se cargan de formas *distintas?*", "3 BATERÍAS, *3 CARGAS*",
      A("🔌", "plomo, litio y NiMH", "CADA UNA A SU MANERA")),
    S("plomo", "La de *plomo,* la del coche, admite dos: tensión [(voltaje)] constante... o corriente [(intensidad)] constante y luego tensión *constante.*", "*PLOMO*",
      F(("🚗", "Opción 1", "TENSIÓN CONSTANTE"), ("🚗", "Opción 2", "CC/CV", True, "constante.")), 1),
    S("litio", "La de *litio,* la del móvil, solo una: primero corriente [(intensidad)] constante... y al final, tensión [(voltaje)] *constante.*", "*LITIO*",
      A("📱", "corriente constante, luego tensión constante", "SOLO CC/CV"), 2),
    S("litio", "¿Por qué no solo tensión constante? Porque con la batería vacía, la corriente [(intensidad)] sería *enorme.*", "¿POR *QUÉ*?",
      A("💥", "batería vacía + tensión (voltaje) fija", "CORRIENTE ENORME", "PELIGRO"), 2),
    S("níquel", "Y las de *níquel,* las pilas recargables, solo a corriente [(intensidad)] *constante.* Se para cuando se calientan... o cuando la tensión [(voltaje)] cae un poquito.", "*NÍQUEL*",
      A("🔋", "se corta por temperatura o por −ΔV", "SOLO CORRIENTE CONSTANTE"), 3),
    S("en resumen", "Así que ya sabes. Plomo: *dos* opciones. Litio: solo *CC/CV.* Níquel: solo corriente [(intensidad)] *constante.*", "EN *RESUMEN*",
      F(("🚗", "Plomo", "TENSIÓN CTE. O CC/CV", None, "dos"), ("📱", "Litio", "SOLO CC/CV", True, "CC/CV."), ("🔋", "Níquel (NiMH)", "SOLO CORRIENTE CTE.", None, "constante."))),
  ]))

# 9 · Arranque, tracción, estacionaria
V.append(dict(id="cesa-tipos-de-bateria", titulo="Batería de coche vs carrito de golf", texto="Arranque, tracción y estacionaria",
  tema="CESA · Baterías", etiqueta="baterías", pron={},
  segmentos=[
    S("la curiosidad", "¿Sabías que la batería de un coche y la de un carrito de golf son *totalmente* distintas por dentro?", "ARRANQUE *VS* TRACCIÓN",
      A("🚗", "parecen iguales por fuera", "POR DENTRO, NO")),
    S("arranque", "La de *arranque* tiene que dar un chute de corriente [(intensidad)] *enorme...* durante unos segundos, para mover el motor.", "*ARRANQUE*",
      A("⚡", "corriente (intensidad) muy alta, muy poco rato", "MUCHA CORRIENTE"), 1),
    S("arranque", "Por eso lleva muchas placas *finas:* más superficie de electrodos... y menos *electrolito.*", "PLACAS *FINAS*",
      F(("📄", "Electrodos", "MÁS SUPERFICIE", True, "finas:"), ("💧", "Electrolito", "MENOS VOLUMEN", None, "electrolito.")), 1),
    S("tracción", "La de *tracción,* la de un carrito o una carretilla, tiene que aguantar horas... y descargarse casi *entera.*", "*TRACCIÓN*",
      A("🏌️", "horas de uso seguidas", "DESCARGA PROFUNDA"), 2),
    S("estacionaria", "Y para guardar la energía de unas placas solares, se usa la *estacionaria:* ciclos lentos y profundos, sin moverse de *sitio.*", "*ESTACIONARIA*",
      A("☀️", "sistema solar autónomo", "CICLOS LENTOS Y PROFUNDOS"), 3),
    S("en resumen", "Así que ya sabes. Arranque: *corriente.* Tracción: *profundidad.* Y para el sol... *estacionaria.*", "EN *RESUMEN*",
      F(("🚗", "Arranque", "MUCHA CORRIENTE", True, "corriente."), ("🏌️", "Tracción", "DESCARGA PROFUNDA", None, "profundidad."), ("☀️", "Placas solares", "ESTACIONARIA", None, "estacionaria."))),
  ]))

# 10 · Balanceo
V.append(dict(id="cesa-balanceo-baterias", titulo="Cómo se igualan las celdas de una batería", texto="Balanceo pasivo vs activo",
  tema="CESA · Baterías", etiqueta="baterías", pron={},
  segmentos=[
    S("la curiosidad", "¿Sabías que dentro de una batería hay muchas *celdas...* y nunca se cargan exactamente *igual?*", "CELDAS *DESIGUALES*",
      A("🔋", "unas se llenan antes que otras", "HAY QUE IGUALARLAS")),
    S("el balanceo", "Para igualarlas existe el *balanceo.* Y hay dos formas: el pasivo... y el *activo.*", "*BALANCEO*", B("2", "formas de igualar las celdas")),
    S("pasivo", "El *pasivo* es el bruto: a la celda más cargada le quita energía con una *resistencia...* y la quema en calor.", "*PASIVO*",
      A("🔥", "disipa la energía de la celda más cargada", "CON UNA RESISTENCIA", "SE PIERDE"), 1),
    S("activo", "El *activo* es el listo: con un convertidor conmutado, *pasa* la energía de la celda más cargada... a la menos cargada.", "*ACTIVO*",
      A("🔁", "de la más cargada a la menos cargada", "CONVERTIDOR CONMUTADO", "SE APROVECHA"), 2),
    S("en resumen", "Así que ya sabes. Pasivo: *quema.* Activo: *reparte.*", "EN *RESUMEN*",
      F(("🔥", "Pasivo", "QUEMA EN UNA RESISTENCIA", None, "quema."), ("🔁", "Activo", "REPARTE CON CONVERTIDOR", True, "reparte."))),
  ]))

# 12 · Rayo vs neutro
V.append(dict(id="cesa-rayo-vs-neutro", titulo="Un rayo vs un neutro cortado", texto="Dos sobretensiones muy distintas",
  tema="CESA · Protecciones", etiqueta="protecciones", pron={},
  segmentos=[
    S("la curiosidad", "¿Sabías que un rayo y un cable de neutro cortado... pueden freír tus aparatos de formas *muy* distintas?", "RAYO *VS* NEUTRO",
      A("⚡", "dos sobretensiones distintas", "CORTA O LARGA")),
    S("el rayo", "Un rayo que cae en una línea da un pico *brutal...* pero muy *corto.* Microsegundos.", "RAYO: *CORTO*",
      A("🌩️", "pico enorme de tensión (voltaje)", "MUY CORTA DURACIÓN"), 1),
    S("el rayo", "Y pasa sobre todo en líneas *aéreas,* que son las que reciben el golpe. Las *enterradas* están más a salvo.", "LÍNEAS *AÉREAS*",
      F(("🗼", "Líneas aéreas", "MÁS EXPUESTAS", True, "aéreas,"), ("⛏️", "Líneas enterradas", "MÁS A SALVO", None, "enterradas")), 1),
    S("el rayo", "¿Cómo te proteges? Con limitadores o descargadores, en *paralelo* con la carga. Desvían el pico... y *listo.*", "*LIMITADORES*",
      A("🛡️", "en paralelo con la carga", "DESVÍAN EL PICO"), 1),
    S("el neutro", "En cambio, si se corta el *neutro,* la tensión [(voltaje)] se queda alta... y *no* baja. Es una sobretensión de larga duración.", "NEUTRO: *LARGO*",
      A("✂️", "la tensión (voltaje) se queda alta", "LARGA DURACIÓN"), 2),
    S("el neutro", "Y eso no lo aguanta ningún limitador. La única solución es *desconectar* la red.", "*DESCONECTA*",
      A("🔌", "ningún limitador lo aguanta", "DESCONECTAR LA RED", "ÚNICA SALIDA"), 2),
    S("en resumen", "Así que ya sabes. Rayo: corto, *limitador.* Neutro cortado: largo, *desconectar.*", "EN *RESUMEN*",
      F(("⚡", "Rayo · corta duración", "LIMITADOR EN PARALELO", None, "limitador."), ("✂️", "Neutro cortado · larga", "DESCONECTAR", True, "desconectar."))),
  ]))

# 13 · Protectores tipo 1, 2, 3
V.append(dict(id="cesa-protectores-tipo-1-2-3", titulo="Protectores tipo 1, 2 y 3", texto="Cómo proteger un ordenador de un rayo",
  tema="CESA · Protecciones", etiqueta="protecciones",
  pron={"1": "uno", "2": "dos", "3": "tres", "1,": "uno,", "3.": "tres.", "*tipo": "tipo"},
  segmentos=[
    S("la curiosidad", "¿Sabías que para proteger un ordenador de un rayo... a veces necesitas *dos* protectores?", "TIPO *1, 2 Y 3*",
      A("💻", "protección contra sobretensiones", "TIPO 1, 2 Y 3")),
    S("tipo 1", "El tipo 1 aguanta hasta un rayo *directo.* Pero deja pasar demasiada tensión [(voltaje)] para los equipos *delicados.*", "*TIPO 1*",
      F(("🌩️", "Rayo directo", "LO AGUANTA", None, "directo."), ("💻", "Equipos delicados (cat. I)", "NO LOS PROTEGE", True, "delicados.")), 1),
    S("tipo 2", "El tipo 2 solo aguanta rayos *indirectos...* y tampoco protege los equipos *delicados.*", "*TIPO 2*",
      F(("☁️", "Rayo indirecto", "LO AGUANTA", None, "indirectos..."), ("💻", "Equipos delicados (cat. I)", "NO LOS PROTEGE", True, "delicados.")), 2),
    S("tipo 3", "El tipo 3 también es solo para rayos indirectos... pero este sí protege los equipos *delicados.* Va pegado al aparato.", "*TIPO 3*",
      F(("☁️", "Rayo indirecto", "LO AGUANTA"), ("💻", "Equipos delicados (cat. I)", "SÍ LOS PROTEGE", True, "delicados.")), 3),
    S("qué pongo", "Entonces... ¿rayo *indirecto?* Con un tipo 3 junto al ordenador te basta. ¿Rayo *directo?* Tipo 1 para el golpe gordo... y tipo 3 para el ordenador.", "¿QUÉ *PONGO*?",
      F(("☁️", "Rayo indirecto", "TIPO 3", None, "indirecto?"), ("🌩️", "Rayo directo", "TIPO 1 + TIPO 3", True, "directo?"))),
    S("en resumen", "Así que ya sabes. El tipo 1 aguanta el *golpe.* El tipo 3 protege el *aparato.*", "EN *RESUMEN*",
      F(("🥊", "Tipo 1", "AGUANTA EL RAYO DIRECTO", None, "golpe."), ("💻", "Tipo 3", "PROTEGE EL APARATO", True, "aparato."))),
  ]))

# 14 · Varistor, bimetal, PPTC
V.append(dict(id="cesa-varistor-bimetal-pptc", titulo="Varistor, bimetal y PPTC", texto="Los pequeños guardianes de un circuito",
  tema="CESA · Protecciones", etiqueta="protecciones",
  pron={"MOV,": "o eme o uve,", "PPTC": "pe pe te ce", "*PPTC*": "pe pe te ce", "PPTC,": "pe pe te ce,", "PPTC.": "pe pe te ce."},
  segmentos=[
    S("la curiosidad", "¿Sabías que hay protecciones que se *rearman* solas... y otras que solo cambian su *resistencia?*", "PEQUEÑOS *GUARDIANES*",
      A("🛡️", "varistor, bimetal y PPTC", "3 PROTECCIONES")),
    S("varistor", "El *varistor,* o MOV, protege de *sobretensiones.* Va en paralelo: cuando la tensión [(voltaje)] sube, su resistencia cae... y se come el pico.", "*VARISTOR*",
      F(("⚡", "Protege de", "SOBRETENSIONES", True, "sobretensiones."), ("🔀", "Conexión", "EN PARALELO · LIMITADOR")), 1),
    S("bimetal", "El *bimetal* protege de *sobrecorrientes.* Va en serie: la corriente [(intensidad)] lo calienta, se dobla... y abre el circuito.", "*BIMETAL*",
      F(("🔥", "Protege de", "SOBRECORRIENTES", True, "sobrecorrientes."), ("➡️", "Conexión", "EN SERIE")), 2),
    S("PPTC", "El PPTC es un fusible que se *rearma* solo. También protege de *sobrecorrientes.*", "*PPTC*",
      A("♻️", "fusible rearmable", "SOBRECORRIENTES"), 3),
    S("arrancar un motor", "¿Y al arrancar un motor? Hay picos de corriente [(intensidad)] *normales.* Por eso se usa algo *lento,* como un térmico... que no salte por nada.", "ARRANQUE *LENTO*",
      A("🐢", "picos normales al arrancar", "TÉRMICO LENTO"), 4),
    S("en resumen", "Así que ya sabes. Sobretensión: *varistor,* en paralelo. Sobrecorriente: *bimetal* o PPTC, en serie.", "EN *RESUMEN*",
      F(("⚡", "Sobretensión", "VARISTOR · PARALELO", None, "varistor,"), ("🔥", "Sobrecorriente", "BIMETAL / PPTC · SERIE", True, "bimetal"))),
  ]))

for v in V:
    (D / f"{v['id']}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), "utf-8")
print(len(V), "specs")
