#!/usr/bin/env python3
"""Circuitos dibujados con schemdraw para el visual {"tipo": "circuito"}.

Cada circuito es una función (rojo: set, v: dict) -> schemdraw.Drawing.
- rojo: nombres de piezas que se pintan en rojo (lo que se está explicando).
- v: valores que se escriben en el dibujo (si falta uno, sale solo el nombre).

Añadir un circuito nuevo = escribir otra función y meterla en CIRCUITOS.
Probar: python3 circuitos.py lm317 R1,R2   → crea out/_circ_lm317.png
"""
import hashlib, json, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import schemdraw
import schemdraw.elements as e

RED = "#de2929"
INK = "#141414"
CACHE = Path(__file__).parent / "out" / "_circ"


def _c(el, nombre, rojo):
    return el.color(RED) if nombre in rojo else el


def _lbl(nombre, v):
    return f"{nombre} = {v[nombre]}" if nombre in v else nombre


def lm317(rojo, v):
    d = schemdraw.Drawing(show=False)
    ic = e.Ic(pins=[e.IcPin("IN", side="left"), e.IcPin("OUT", side="right"), e.IcPin("ADJ", side="bottom")],
              edgepadW=2.0, edgepadH=0.7, label="LM317", lblofst=0.4, lblloc="top")
    d += _c(ic, "LM317", rojo)
    d += e.Line().at(ic.IN).left(1).label(v.get("Vin", "Vin"), loc="left")
    d += e.Line().at(ic.OUT).right(1.2)
    out = d.here
    d += e.Dot()
    d += _c(e.Line().right(0.8).label(v.get("Vout", "Vout"), loc="right"), "Vout", rojo)
    r1 = _c(e.Resistor().down().at(out).label(_lbl("R1", v), loc="bottom", ofst=0.4), "R1", rojo)
    d += r1
    d += e.Dot()
    mid = d.here
    if "1,25" in rojo:
        d += e.Label().at((out[0] - 1.1, (out[1] + mid[1]) / 2 - 0.4)).label("1,25 V").color(RED)
    if "I" in rojo:
        d += e.CurrentLabelInline(direction="in").at(r1).color(RED).label(v.get("I", "I"), ofst=0.15)
    d += e.Line().left().to((ic.ADJ[0], mid[1]))
    d += e.Line().up().to(ic.ADJ)
    d += _c(e.Resistor().down().at(mid).label(_lbl("R2", v), loc="bottom", ofst=0.4), "R2", rojo)
    d += e.Ground()
    return d


def divisor(rojo, v):
    d = schemdraw.Drawing(show=False)
    src = e.SourceV().up().label(v.get("Vin", "Vin"))
    d += _c(src, "Vin", rojo)
    d += e.Line().right(2)
    d += _c(e.Resistor().down().label(_lbl("R1", v), loc="bottom", ofst=0.4), "R1", rojo)
    d += e.Dot()
    mid = d.here
    d += _c(e.Resistor().down().label(_lbl("R2", v), loc="bottom", ofst=0.4), "R2", rojo)
    d += e.Line().left().tox(src.start[0])
    d += e.Line().up().to(src.start)
    d += _c(e.Line().right(1.5).at(mid).label(v.get("Vout", "Vout"), loc="right"), "Vout", rojo)
    return d


def zener(rojo, v):
    d = schemdraw.Drawing(show=False)
    d += _c(e.SourceV().up().label(v.get("Vin", "Vin")), "Vin", rojo)
    d += _c(e.Resistor().right().label(_lbl("Rs", v), ofst=0.3), "Rs", rojo)
    d += e.Dot()
    n = d.here
    d += _c(e.Zener().down().reverse().label(_lbl("Dz", v), loc="bottom", ofst=0.4), "Dz", rojo)
    d += e.Dot()
    d += e.Line().left().tox(0)
    d += e.Line().right(2.2).at(n)
    d += _c(e.Resistor().down().label(_lbl("RL", v), loc="bottom", ofst=0.4), "RL", rojo)
    d += e.Line().left(2.2)
    return d


def puente(rojo, v):
    """Rectificador en puente de Graetz con condensador de filtro. W/E = alterna, N = +, S = -."""
    d = schemdraw.Drawing(show=False)
    b = e.Rectifier()
    d += _c(b, "puente", rojo)
    d += e.Line().at(b.W).left(1.2)
    d += _c(e.SourceSin().down().label(v.get("Vac", "Vac"), loc="bottom", ofst=0.4), "Vac", rojo)
    d += e.Line().down().toy(b.S[1] - 1.2)
    d += e.Line().right().tox(b.E[0] + 0.6)
    d += e.Line().up().toy(b.E[1])
    d += e.Line().left().to(b.E)
    xo = b.E[0] + 2.0
    d += e.Line().at(b.N).right().tox(xo)
    d += e.Dot()
    d += _c(e.Capacitor().down().toy(b.S[1]).label(_lbl("C", v), loc="bottom", ofst=0.3), "C", rojo)
    d += e.Dot()
    d += e.Line().left().to(b.S)
    d += e.Line().at((xo, b.N[1])).right(1.6)
    d += _c(e.Resistor().down().toy(b.S[1]).label(_lbl("RL", v), loc="bottom", ofst=0.3), "RL", rojo)
    d += e.Line().left().tox(xo)
    return d


def buck(rojo, v):
    d = schemdraw.Drawing(show=False)
    d += _c(e.SourceV().up().label(v.get("Vin", "Vin")), "Vin", rojo)
    d += _c(e.Switch().right().label("S", ofst=0.3), "S", rojo)
    d += e.Dot()
    n = d.here
    d += _c(e.Inductor2().right().label(_lbl("L", v), ofst=0.3), "L", rojo)
    d += e.Dot()
    o = d.here
    d += _c(e.Capacitor().down().label(_lbl("C", v), loc="bottom", ofst=0.3), "C", rojo)
    d += e.Line().left().tox(0)
    d += _c(e.Diode().up().at((n[0], o[1] - 3)).to(n).label("D", loc="bottom", ofst=0.3), "D", rojo)
    d += e.Line().right(1.6).at(o)
    d += _c(e.Resistor().down().label(v.get("Vout", "Vout"), loc="bottom", ofst=0.3), "Vout", rojo)
    d += e.Line().left(1.6)
    return d


def boost(rojo, v):
    d = schemdraw.Drawing(show=False)
    d += _c(e.SourceV().up().label(v.get("Vin", "Vin")), "Vin", rojo)
    d += _c(e.Inductor2().right().label(_lbl("L", v), ofst=0.3), "L", rojo)
    d += e.Dot()
    n = d.here
    d += _c(e.Diode().right().label("D", ofst=0.3), "D", rojo)
    d += e.Dot()
    o = d.here
    d += _c(e.Capacitor().down().label(_lbl("C", v), loc="bottom", ofst=0.3), "C", rojo)
    d += e.Line().left().tox(0)
    d += _c(e.Switch().down().at(n).toy(o[1] - 3).label("S", loc="bottom", ofst=0.3), "S", rojo)
    d += e.Line().right(1.6).at(o)
    d += _c(e.Resistor().down().label(v.get("Vout", "Vout"), loc="bottom", ofst=0.3), "Vout", rojo)
    d += e.Line().left(1.6)
    return d


CIRCUITOS = {"lm317": lm317, "divisor": divisor, "zener": zener, "puente": puente, "buck": buck, "boost": boost}


def png(nombre, rojo=(), valores=None):
    """Devuelve la ruta de un PNG transparente del circuito (cacheado)."""
    rojo, valores = set(rojo), dict(valores or {})
    key = hashlib.md5(json.dumps([nombre, sorted(rojo), valores], sort_keys=True).encode()).hexdigest()[:12]
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"{nombre}-{key}.png"
    if not p.exists():
        schemdraw.config(fontsize=17, lw=2.4, color=INK)
        d = CIRCUITOS[nombre](rojo, valores)
        d.save(str(p), dpi=160, transparent=True)
    return p


if __name__ == "__main__":
    n = sys.argv[1] if len(sys.argv) > 1 else "lm317"
    r = sys.argv[2].split(",") if len(sys.argv) > 2 else []
    print(png(n, r))
