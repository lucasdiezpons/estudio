#!/usr/bin/env python3
"""TikToks de API (voz gratis edge-tts). Escribe specs/gratis/api-g-*.json.
Uso: python3 specs/generar_specs_api.py"""
import json
from pathlib import Path

OUT = Path(__file__).parent / "gratis"
PRON = {
    "DNS": "de ene ese", "PTR": "pe te erre", "NS": "ene ese", "MX": "eme equis", "SOA": "ese o a", "CNAME": "ce neim",
    "IP": "i pe", "IPs": "i pes", "aa": "a a", "ra": "erre a", "rd": "erre de", "REFUSED": "refiused", "NXDOMAIN": "en equis domein",
    "AXFR": "a equis efe erre", "IXFR": "i equis efe erre", "TCP": "te ce pe", "UDP": "u de pe", "NOTIFY": "nótifai",
    "in-addr.arpa": "in adr arpa", "dig": "dig", "-x": "guion equis", "lab.api": "lab punto api", "lab.api.": "lab punto api",
    "ns": "ene ese", "ns2": "ene ese dos", "www": "uve doble uve doble uve doble", "PC03": "pe ce tres", "PC08": "pe ce ocho",
    "128/25": "ciento veintiocho barra veinticinco", "SMTP": "ese eme te pe", "POP3": "pop tres", "IMAP": "ímap", "EHLO": "e hache ele o",
    "IPv6": "i pe uve seis", "IPv4": "i pe uve cuatro", "OSPFv3": "o ese pe efe versión tres", "LSA": "ele ese a", "MAC": "mac",
    "EUI-64": "e u i sesenta y cuatro", "fe80": "efe e ochenta", "ff:fe": "efe efe efe e", "6to4": "seis tu cuatro", "2002": "dos mil dos",
    "SYN": "sin", "ACK": "ak", "FIN": "fin", "MSS": "eme ese ese", "BDP": "be de pe", "RTT": "erre te te", "SACK": "sak", "ISN": "i ese ene",
    "postfix": "póstfix", "mutt": "mat", "dovecot": "dóvcot", "myhostname": "mai jóstneim", "mydomain": "mai doméin", "LSID": "ele ese i de",
    "DR": "de erre", "MAIL": "méil", "FROM": "from", "RCPT": "ricipient", "TO": "tu", "DATA": "deita", "From": "from", "To": "tu", "Subject": "sábyect", "main.cf": "mein punto ce efe", "250": "doscientos cincuenta", "ID": "i de", "RA": "erre a", "NS/NA": "ene ese y ene a",
}


def v(id_, titulo, texto, tema, etiqueta, segs, examen="PA3"):
    d = {"id": id_, "titulo": titulo, "texto": texto, "tema": tema, "etiqueta": etiqueta, "pron": PRON, "voz": "gratis",
         "segmentos": [], "examen": examen}
    n = 0
    for i, (tag, sub, tit, vis) in enumerate(segs):
        s = {"tag": tag, "sub": sub, "titulo": tit, "visual": vis}
        if 0 < i < len(segs) - 1:
            n += 1; s["num"] = n
        d["segmentos"].append(s)
    return d


A = lambda icono, l1, l2, stamp=None: {"tipo": "alerta", "icono": icono, "linea1": l1, "linea2": l2, **({"stamp": stamp} if stamp else {})}
B = lambda big, small: {"tipo": "big", "big": big, "small": small}
F = lambda filas, stamp=None: {"tipo": "filas", "filas": filas, **({"stamp": stamp} if stamp else {})}

VIDEOS = [
    # ---------------- tanda 1 · DNS
    v("api-g-aa-vs-ra", "aa y ra: quién sabe y quién busca", "Los dos flags que lo explican todo", "API · DNS", "dns", [
        ("la curiosidad", "¿Sabías que un servidor DNS puede contestarte... sin saber *nada* de lo que preguntas?", "AA *VS* RA",
         A("🌐", "dos flags en cada respuesta", "aa · ra")),
        ("aa", "Si lleva *aa*... el dato está en su propio fichero. Es el dueño de esa zona.", "AA = *ES SUYO*",
         A("📒", "autoritativo", "LO TIENE EN SU FICHERO")),
        ("ra", "Si lleva *ra*... no es suyo, pero acepta buscarlo por ti. Pregunta a otros y te lo pasa.", "RA = *LO BUSCA*",
         A("🔎", "recursión disponible", "BUSCA POR TI")),
        ("refused", "¿Y si no tiene ni una ni otra? Ni es suyo... ni quiere buscar. Te responde *REFUSED.*", "NI UNO *NI OTRO*",
         A("⛔", "no es suyo y no busca", "REFUSED", "¡NO!")),
        ("el truco", "Por eso, en una captura... la respuesta con *aa* te dice quién guarda cada zona.", "EL *TRUCO*",
         F([{"icono": "✅", "izq": "aa", "der": "es su zona", "en": "*aa*"}, {"icono": "🔁", "izq": "ra sin aa", "der": "lo ha buscado"}])),
        ("en resumen", "Así que ya sabes. *aa*, lo tiene en su fichero. *ra*, lo busca por ti.", "EN *RESUMEN*",
         B("aa = suyo · ra = busca", "dos flags de cada respuesta")),
    ]),
    v("api-g-ptr-al-reves", "La IP se escribe al revés", "Así funciona la búsqueda inversa", "API · DNS", "dns", [
        ("la curiosidad", "¿Sabías que para saber el nombre de una IP... hay que escribirla *al revés?*", "LA IP *AL REVÉS*",
         A("🔄", "de IP a nombre", "BÚSQUEDA INVERSA")),
        ("el registro", "El registro que da el nombre de una IP se llama *PTR.* Y vive en una rama especial: in-addr.arpa.", "EL *PTR*",
         B("in-addr.arpa.", "la rama de las IPs")),
        ("al revés", "Diez punto cero punto uno punto cinco... se pregunta como cinco, uno, cero, diez, y *in-addr.arpa.*", "OCTETOS *GIRADOS*",
         B("5.1.0.10.in-addr.arpa", "10.0.1.5 al revés")),
        ("por qué", "¿Por qué? Porque en el árbol lo general va arriba... y en una IP lo general va a la *izquierda.*", "¿POR *QUÉ*?",
         A("🌳", "se lee de la hoja a la raíz", "LO GENERAL, AL FINAL")),
        ("el atajo", "Y si no quieres girarla tú... dig con guion equis lo hace *solo.*", "EL *ATAJO*",
         B("dig -x 10.0.1.5", "gira la IP por ti")),
        ("en resumen", "Así que ya sabes. IP al revés, más in-addr.arpa, y pides el *PTR.*", "EN *RESUMEN*",
         B("IP al revés + in-addr.arpa", "→ registro PTR")),
    ]),
    v("api-g-punto-final", "El punto que rompe tu zona", "Nombres relativos y absolutos", "API · DNS", "dns", [
        ("la curiosidad", "¿Sabías que en una zona DNS... olvidar un *punto* cambia el nombre entero?", "UN *PUNTO*",
         A("•", "el punto final", "LO CAMBIA TODO", "¡OJO!")),
        ("relativo", "Sin punto final, el nombre es *relativo:* se le pega el origen. ns se convierte en ns.lab.api.", "SIN PUNTO = *RELATIVO*",
         B("ns → ns.lab.api.", "se le pega el origen")),
        ("absoluto", "Con punto final es *absoluto:* se queda tal cual. ns.lab.api. con punto, ya está completo.", "CON PUNTO = *ABSOLUTO*",
         B("ns.lab.api.", "con punto: completo")),
        ("el error", "Si escribes ns.lab.api sin punto... bind lo convierte en ns.lab.api.lab.api. Un nombre *imposible.*", "EL *ERROR*",
         A("💥", "sin punto final", "ns.lab.api.lab.api.", "¡MAL!")),
        ("la inversa", "En la zona inversa, el origen es in-addr.arpa. Así que los nombres van *siempre* con punto.", "EN LA *INVERSA*",
         B("5 PTR www.lab.api.", "siempre con punto")),
        ("en resumen", "Así que ya sabes. Sin punto, se le pega el origen. Con punto, es el nombre *completo.*", "EN *RESUMEN*",
         F([{"icono": "➕", "izq": "sin punto", "der": "+ origen", "en": "Sin"}, {"icono": "✅", "izq": "con punto", "der": "completo", "en": "Con"}])),
    ]),
    v("api-g-delegacion-glue", "Cómo se regala un trozo de dominio", "Delegar: NS + pegamento", "API · DNS", "dns", [
        ("la curiosidad", "¿Sabías que un servidor DNS puede *regalar* un trozo de su dominio a otro?", "REGALAR *UN TROZO*",
         A("🎁", "delegar un subdominio", "SUBGRUP.LAB.API")),
        ("el NS", "Primera línea: subgrup, NS, y el servidor nuevo. Es decir: de aquí para abajo... *pregúntale* a él.", "LÍNEA 1: *NS*",
         B("subgrup NS ns.subgrup", "de aquí abajo, él")),
        ("el pegamento", "Segunda línea: la IP de ese servidor. Se llama *pegamento*, glue en inglés.", "LÍNEA 2: *GLUE*",
         B("ns.subgrup A 10.0.1.130", "su IP")),
        ("sin glue", "Sin el pegamento... sabes *a quién* preguntar, pero no dónde está. Y se queda atascado.", "SIN *GLUE*",
         A("🧩", "sabes el nombre, no la IP", "SE QUEDA ATASCADO", "¡OJO!")),
        ("en una captura", "En una captura lo ves así: una respuesta sin answer... con un NS y una IP. Eso es una *delegación.*", "EN LA *CAPTURA*",
         F([{"icono": "📭", "izq": "answer", "der": "vacía"}, {"icono": "➡️", "izq": "NS + A", "der": "delegación", "en": "*delegación.*"}])),
        ("en resumen", "Así que ya sabes. Para delegar: NS en el corte... y la A del servidor, el *pegamento.*", "EN *RESUMEN*",
         B("NS + A (glue)", "para delegar")),
    ]),
    v("api-g-serial-esclavo", "Por qué el esclavo no se entera", "El número de serie del SOA", "API · DNS", "dns", [
        ("la curiosidad", "¿Sabías que puedes cambiar tu zona DNS... y que la copia *no* se entere?", "LA COPIA *NO SE ENTERA*",
         A("🙈", "máster y esclavo", "DOS SERVIDORES")),
        ("el esclavo", "El esclavo no escribe nada. Le *pide* la zona entera al máster. Con una pregunta AXFR, por TCP.", "EL *ESCLAVO*",
         B("AXFR · TCP", "dame toda la zona")),
        ("el serial", "Pero antes mira el número de serie del SOA. Si no ha *subido*... cree que no ha cambiado nada.", "EL *SERIAL*",
         B("2018111201", "número de serie")),
        ("el fallo", "Resultado: el máster contesta lo nuevo... y el esclavo sigue diciendo que no *existe.*", "EL *FALLO*",
         F([{"icono": "✅", "izq": "máster", "der": "lo nuevo"}, {"icono": "❌", "izq": "esclavo", "der": "NXDOMAIN", "rojo": True, "en": "*existe.*"}])),
        ("la regla", "La regla: cada vez que toques el máster, sube el serial en uno. Entonces avisa con NOTIFY... y el esclavo *copia.*", "LA *REGLA*",
         A("⬆️", "cambias algo", "SERIAL + 1", "SIEMPRE")),
        ("en resumen", "Así que ya sabes. El esclavo solo copia si el serial del máster es *mayor.*", "EN *RESUMEN*",
         B("serial + 1", "o no hay copia")),
    ]),
]

VIDEOS += [
    # ---------------- tanda 2 · IPv6 + OSPFv3
    v("api-g-eui64", "Tu MAC dentro de tu IPv6", "fe80 + la MAC con ff:fe", "API · IPv6", "ipv6", [
        ("la curiosidad", "¿Sabías que tu tarjeta de red se inventa su propia IPv6... a partir de su *MAC?*", "TU MAC *EN TU IPv6*",
         A("🪪", "dirección de enlace", "SE LA INVENTA SOLA")),
        ("el prefijo", "Empieza siempre por fe80. Es la dirección *link-local:* solo vale dentro de ese cable.", "EMPIEZA POR *FE80*",
         B("fe80::/64", "solo dentro del enlace")),
        ("el relleno", "La MAC tiene cuarenta y ocho bits... y faltan dieciséis. Se meten en *medio:* ff:fe.", "ff:fe *EN MEDIO*",
         B("00:0c:29 ff:fe 3a:4b:5c", "MAC partida en dos")),
        ("el bit", "Y un detalle: el séptimo bit del primer byte se *invierte.* Cero cero pasa a ser cero dos.", "EL BIT *GIRADO*",
         A("🔁", "séptimo bit del primer byte", "00 → 02", "¡OJO!")),
        ("resultado", "Resultado: fe80, dos puntos, dos c, veintinueve ff, fe tres a, cuatro b cinco *c.*", "EL *RESULTADO*",
         B("fe80::20c:29ff:fe3a:4b5c", "EUI-64")),
        ("en resumen", "Así que ya sabes. fe80, la MAC partida con ff:fe... y el séptimo bit *girado.*", "EN *RESUMEN*",
         B("fe80 + MAC(ff:fe) + bit 7", "EUI-64")),
    ]),
    v("api-g-ospfv3-sin-ips", "El OSPF que no sabe de IPs", "Router ID y vecinos en OSPFv3", "API · OSPFv3", "ospfv3", [
        ("la curiosidad", "¿Sabías que OSPF para IPv6... sigue usando un nombre con *pinta* de IPv4?", "UN NOMBRE *DE IPv4*",
         A("🏷️", "router ID", "32 BITS, COMO IPv4")),
        ("el ID", "El router ID son treinta y dos bits. Se escribe como uno punto uno punto uno punto uno... pero no es una *IP.*", "NO ES *UNA IP*",
         B("router-id 1.1.1.1", "solo un nombre")),
        ("los vecinos", "Los vecinos se hablan con su dirección *link-local*, la de fe80. Nunca con la global.", "VECINOS POR *FE80*",
         A("🤝", "hello entre vecinos", "SIEMPRE fe80")),
        ("el siguiente salto", "Por eso en la tabla de rutas... el siguiente salto también es una fe80, y va con su *interfaz.*", "EL *SIGUIENTE SALTO*",
         B("via fe80::2, eth1", "link-local + interfaz")),
        ("el despiste", "Si el router no tiene IPv4... el router ID hay que ponerlo a *mano.* Si no, OSPFv3 no arranca.", "SIN IPv4, *A MANO*",
         A("✋", "sin IPv4 que copiar", "PONLO A MANO", "¡OJO!")),
        ("en resumen", "Así que ya sabes. Nombre de treinta y dos bits... y todo lo demás, por *link-local.*", "EN *RESUMEN*",
         F([{"icono": "🏷️", "izq": "router ID", "der": "32 bits"}, {"icono": "🔗", "izq": "vecinos y saltos", "der": "fe80", "en": "*link-local.*"}])),
    ]),
    v("api-g-lsa-link-intra", "Dónde viven los prefijos en OSPFv3", "Link LSA e Intra-Area-Prefix", "API · OSPFv3", "ospfv3", [
        ("la curiosidad", "¿Sabías que en OSPFv3 el mapa de la red... ya *no* lleva direcciones?", "UN MAPA *SIN DIRECCIONES*",
         A("🗺️", "router LSA y network LSA", "SOLO QUIÉN CON QUIÉN")),
        ("la topología", "Las LSA de router y de red solo dicen quién está conectado con *quién.* Nada de prefijos.", "SOLO *TOPOLOGÍA*",
         F([{"icono": "🖥️", "izq": "Router LSA", "der": "enlaces"}, {"icono": "🔀", "izq": "Network LSA", "der": "quién hay", "en": "*quién.*"}])),
        ("los prefijos", "Los prefijos van aparte, en la *Intra-Area-Prefix.* Esa es la que dice qué redes hay.", "LOS *PREFIJOS*",
         B("Intra-Area-Prefix", "qué redes IPv6 hay")),
        ("la de enlace", "Y la *Link* LSA no sale del cable: lleva tu fe80 y tus prefijos a los vecinos de ese enlace.", "LA *LINK* LSA",
         A("🔗", "no sale del enlace", "fe80 + PREFIJOS")),
        ("la ventaja", "¿La gracia? Si cambias un prefijo... no se recalcula todo el *árbol.* Solo cambia una LSA.", "LA *VENTAJA*",
         A("🌳", "cambias un prefijo", "SIN RECALCULAR TODO")),
        ("en resumen", "Así que ya sabes. Router y Network, topología. Intra-Area-Prefix, las *redes.* Link, el enlace.", "EN *RESUMEN*",
         B("topología ≠ prefijos", "separados en OSPFv3")),
    ]),
    v("api-g-6to4", "IPv6 escondido en IPv4", "Los túneles 6to4", "API · IPv6", "ipv6", [
        ("la curiosidad", "¿Sabías que se puede viajar en IPv6... por una red que solo entiende *IPv4?*", "IPv6 *POR IPv4*",
         A("🚇", "un túnel", "IPv6 DENTRO DE IPv4")),
        ("el prefijo", "El truco se llama 6to4. Sus direcciones empiezan siempre por *2002.*", "EMPIEZA POR *2002*",
         B("2002::/16", "prefijo 6to4")),
        ("la IP dentro", "Detrás va la IPv4 pública del router... pasada a *hexadecimal.* Ocho dígitos.", "LA IPv4 *EN HEXA*",
         B("2002:c000:0201::/48", "192.0.2.1 en hexa")),
        ("cómo se lee", "Ciento noventa y dos es c cero. Cero, cero cero. Dos, cero dos. Uno, cero *uno.*", "CÓMO SE *LEE*",
         F([{"icono": "1️⃣", "izq": "192.0", "der": "c000"}, {"icono": "2️⃣", "izq": "2.1", "der": "0201", "en": "*uno.*"}])),
        ("el viaje", "Así el router sabe a dónde mandar el paquete IPv4... sin tabla de túneles: la dirección ya lo *dice.*", "EL *VIAJE*",
         A("📦", "IPv6 metido en IPv4", "EL DESTINO VA DENTRO")),
        ("en resumen", "Así que ya sabes. 2002, más la IPv4 en hexadecimal... y tienes tu barra *cuarenta y ocho.*", "EN *RESUMEN*",
         B("2002 : IPv4 hexa ::/48", "6to4")),
    ]),
    # ---------------- tanda 3 · TCP
    v("api-g-syn-gasta", "El SYN que cuesta un byte", "Números de secuencia en el handshake", "API · TCP", "tcp", [
        ("la curiosidad", "¿Sabías que un SYN de TCP no lleva datos... pero gasta un número como si llevara *uno?*", "UN BYTE *FANTASMA*",
         A("👻", "SYN sin datos", "GASTA 1")),
        ("el saludo", "Primer paquete: SYN con un número inicial, el *ISN.* Digamos mil.", "EL *SYN*",
         B("SYN seq=1000", "número inicial")),
        ("la respuesta", "El otro responde SYN y ACK. Y su ACK es mil *uno*, no mil.", "ACK = *1001*",
         B("SYN+ACK ack=1001", "1000 + 1")),
        ("el FIN", "Con el FIN pasa *igual:* no lleva datos, pero el ACK que lo confirma suma uno.", "EL FIN, *IGUAL*",
         A("🚪", "FIN sin datos", "TAMBIÉN GASTA 1", "¡OJO!")),
        ("la regla", "La regla: el ACK es el siguiente byte que *esperas.* Por eso SYN y FIN cuentan como uno.", "LA *REGLA*",
         B("ACK = seq + datos (+1 SYN/FIN)", "el siguiente que espero")),
        ("en resumen", "Así que ya sabes. SYN y FIN no llevan datos... pero cada uno gasta un *número.*", "EN *RESUMEN*",
         B("SYN +1 · FIN +1", "números de secuencia")),
    ]),
    v("api-g-mss-1448", "Por qué caben 1448 bytes y no 1460", "MSS y timestamps", "API · TCP", "tcp", [
        ("la curiosidad", "¿Sabías que en una red normal TCP podría mandar mil cuatrocientos sesenta bytes... pero manda *mil cuatrocientos cuarenta y ocho?*", "1460 *O 1448*",
         A("📏", "datos por segmento", "¿CUÁNTOS CABEN?")),
        ("la cuenta", "Ethernet deja mil quinientos. Menos veinte de IP, menos veinte de TCP: mil cuatrocientos *sesenta.*", "LA *CUENTA*",
         B("1500 − 20 − 20 = 1460", "MSS anunciado")),
        ("el ladrón", "Pero si se usan *timestamps*... cada segmento lleva doce bytes más de opciones.", "EL *LADRÓN*",
         A("⏱️", "opción timestamps", "+12 BYTES", "¡OJO!")),
        ("el resultado", "Mil cuatrocientos sesenta menos doce: mil cuatrocientos cuarenta y *ocho.* Eso es lo que ves en la captura.", "EL *RESULTADO*",
         B("1460 − 12 = 1448", "datos reales")),
        ("dónde se ve", "El MSS solo aparece en el *SYN.* Los siguientes segmentos simplemente miden eso.", "DÓNDE SE *VE*",
         F([{"icono": "🤝", "izq": "SYN", "der": "MSS 1460", "en": "*SYN.*"}, {"icono": "📦", "izq": "datos", "der": "len 1448"}])),
        ("en resumen", "Así que ya sabes. Mil quinientos, menos cuarenta de cabeceras... y menos doce si hay *timestamps.*", "EN *RESUMEN*",
         B("1500 − 40 − 12 = 1448", "MSS con timestamps")),
    ]),
    v("api-g-bdp-ventana", "La ventana que frena tu descarga", "Producto ancho de banda por retardo", "API · TCP", "tcp", [
        ("la curiosidad", "¿Sabías que con fibra rapidísima... TCP puede ir *lento* solo por la distancia?", "RÁPIDO *PERO LENTO*",
         A("🐢", "mucha velocidad, mucho retardo", "TCP SE FRENA")),
        ("la ventana", "TCP solo puede tener en vuelo lo que dice la *ventana.* Luego espera el ACK.", "LA *VENTANA*",
         A("🪟", "bytes sin confirmar", "LUEGO ESPERA")),
        ("el tubo", "Para llenar el tubo hace falta velocidad por RTT. Eso es el *BDP.*", "EL *BDP*",
         B("BDP = C · RTT", "bytes en vuelo")),
        ("ejemplo", "Cien megabits y cien milisegundos: diez megabits... un millón doscientos cincuenta mil *bytes.*", "*EJEMPLO*",
         B("100 Mb/s · 0,1 s = 1,25 MB", "ventana necesaria")),
        ("el límite", "Pero la ventana normal llega a sesenta y cinco mil quinientos treinta y cinco. Por eso existe el *window scaling.*", "EL *LÍMITE*",
         F([{"icono": "🚫", "izq": "sin escala", "der": "65535 B", "rojo": True}, {"icono": "📈", "izq": "window scaling", "der": "× 2^n", "en": "*window"}])),
        ("en resumen", "Así que ya sabes. Velocidad por RTT... y si la ventana es más pequeña, vas *frenado.*", "EN *RESUMEN*",
         B("vel. máx = ventana / RTT", "si ventana < BDP")),
    ]),
    v("api-g-tres-acks", "Tres ACK repetidos", "Fast retransmit", "API · TCP", "tcp", [
        ("la curiosidad", "¿Sabías que TCP puede saber que se perdió un paquete... *antes* de que salte el temporizador?", "ANTES DEL *TIMEOUT*",
         A("⏰", "sin esperar al reloj", "FAST RETRANSMIT")),
        ("el hueco", "Si se pierde un segmento, el receptor sigue pidiendo el *mismo* byte una y otra vez.", "EL *HUECO*",
         B("ACK 5000 · 5000 · 5000", "sigue pidiendo lo mismo")),
        ("los tres", "Al tercer ACK *duplicado*... el emisor no espera más y reenvía ese segmento.", "TRES *DUPLICADOS*",
         A("3️⃣", "ACK duplicados", "REENVÍA YA", "¡YA!")),
        ("la ventana", "Y la ventana de congestión se queda a la *mitad*, no vuelve a uno.", "VENTANA A LA *MITAD*",
         F([{"icono": "⚡", "izq": "3 ACK dup", "der": "cwnd / 2", "en": "*mitad*"}, {"icono": "⏰", "izq": "timeout", "der": "cwnd = 1", "rojo": True}])),
        ("SACK", "Con *SACK*, el receptor además dice qué trozos sí tiene. Así solo se reenvía el hueco.", "CON *SACK*",
         B("SACK 6448-9344", "esto ya lo tengo")),
        ("en resumen", "Así que ya sabes. Tres ACK repetidos, reenvío inmediato... y ventana a la *mitad.*", "EN *RESUMEN*",
         B("3 dup ACK → reenvío", "fast retransmit")),
    ]),
]

VIDEOS += [
    # ---------------- tanda 4 · correo
    v("api-g-smtp-imap", "Un protocolo para enviar, otro para leer", "SMTP, IMAP y POP3", "API · Correo", "correo", [
        ("la curiosidad", "¿Sabías que tu correo usa un protocolo para *enviar*... y otro distinto para leer?", "ENVIAR *Y LEER*",
         A("✉️", "dos caminos", "IDA Y LECTURA")),
        ("enviar", "Para enviar: *SMTP*, puerto veinticinco. Va de tu cliente al servidor... y de servidor a servidor.", "ENVIAR: *SMTP*",
         B("SMTP · 25", "empuja el correo")),
        ("leer", "Para leer: *POP3* en el ciento diez, o IMAP en el ciento cuarenta y tres.", "LEER: *POP3 / IMAP*",
         F([{"icono": "📥", "izq": "POP3", "der": "110", "en": "*POP3*"}, {"icono": "🗂️", "izq": "IMAP", "der": "143"}])),
        ("la diferencia", "POP3 se lo *descarga* y suele borrarlo. IMAP lo deja en el servidor, con sus carpetas.", "LA *DIFERENCIA*",
         F([{"icono": "⬇️", "izq": "POP3", "der": "descarga", "en": "*descarga*"}, {"icono": "☁️", "izq": "IMAP", "der": "se queda"}])),
        ("el destino", "¿Y cómo sabe SMTP a qué servidor ir? Pregunta al DNS por el registro *MX* del dominio.", "EL *MX*",
         B("lab.api. MX 10 mail", "quién recibe el correo")),
        ("en resumen", "Así que ya sabes. SMTP empuja, el MX dice a dónde... y POP3 o IMAP para *leer.*", "EN *RESUMEN*",
         B("SMTP → MX → POP3/IMAP", "el viaje de un correo")),
    ]),
    v("api-g-sobre-y-carta", "El correo tiene sobre y carta", "MAIL FROM vs From:", "API · Correo", "correo", [
        ("la curiosidad", "¿Sabías que un correo puede decir que es de una persona... y venir de *otra?*", "DE QUIÉN *DE VERDAD*",
         A("🎭", "remitente", "¿CUÁL ES EL REAL?")),
        ("el sobre", "En SMTP, MAIL FROM y RCPT TO son el *sobre.* Es lo que usan los servidores para entregar.", "EL *SOBRE*",
         B("MAIL FROM / RCPT TO", "para los servidores")),
        ("la carta", "Después de DATA va la *carta:* las cabeceras From, To y Subject... y el texto.", "LA *CARTA*",
         B("DATA → From: To: Subject:", "lo que ve el usuario")),
        ("pueden diferir", "Y no tienen por qué *coincidir.* Por eso existe la copia oculta: va en el sobre, pero no en la carta.", "NO *COINCIDEN*",
         A("🙈", "copia oculta", "SOLO EN EL SOBRE", "¡OJO!")),
        ("el final", "La carta termina con una línea que solo tiene un *punto.* Ahí el servidor contesta doscientos cincuenta.", "EL *PUNTO*",
         B(".  → 250 OK", "fin del mensaje")),
        ("en resumen", "Así que ya sabes. MAIL FROM y RCPT TO, el sobre. From y To, la *carta.*", "EN *RESUMEN*",
         F([{"icono": "✉️", "izq": "sobre", "der": "MAIL FROM"}, {"icono": "📄", "izq": "carta", "der": "From:", "en": "*carta.*"}])),
    ]),
    v("api-g-mydestination", "Cuando tu servidor rechaza tu propio correo", "mydestination en postfix", "API · Correo", "correo", [
        ("la curiosidad", "¿Sabías que tu servidor de correo puede rechazar correo... para su *propio* dominio?", "RECHAZA *LO SUYO*",
         A("📪", "correo para ti", "RELAY DENIED")),
        ("la lista", "En postfix, *mydestination* es la lista de dominios que entrega aquí, en sus buzones.", "LA *LISTA*",
         B("mydestination = lab.api", "esto es mío")),
        ("si falta", "Si tu dominio no está... cree que el correo es para otro sitio. Y como no reenvía para extraños, lo *rechaza.*", "SI *FALTA*",
         A("⛔", "dominio no listado", "554 RELAY DENIED", "¡MAL!")),
        ("los nombres", "Ojo también con myhostname y mydomain: son los nombres con los que el servidor se *presenta.*", "SUS *NOMBRES*",
         F([{"icono": "🖥️", "izq": "myhostname", "der": "mail.lab.api"}, {"icono": "🌐", "izq": "mydomain", "der": "lab.api", "en": "*presenta.*"}])),
        ("y después", "Tras cambiar el main.cf... hay que *recargar* postfix. Si no, sigue con lo viejo.", "Y *RECARGA*",
         B("postfix reload", "o no cambia nada")),
        ("en resumen", "Así que ya sabes. Si el dominio no está en mydestination... tu servidor no lo considera *suyo.*", "EN *RESUMEN*",
         B("mydestination", "los dominios que son míos")),
    ]),
]

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for d in VIDEOS:
        (OUT / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), "utf-8")
    print(len(VIDEOS), "specs →", OUT)
