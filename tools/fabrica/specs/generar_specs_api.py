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
    "DR": "de erre", "ID": "i de", "RA": "erre a", "NS/NA": "ene ese y ene a",
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

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for d in VIDEOS:
        (OUT / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), "utf-8")
    print(len(VIDEOS), "specs →", OUT)
