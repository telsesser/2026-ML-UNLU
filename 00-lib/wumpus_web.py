"""
El view web del mundo del wumpus.

Hermano de web.py: graba lo que va haciendo el agente y despues escribe
una pagina HTML que se recorre paso a paso. No cambia nada del agente ni
de la inferencia; es el mismo objeto narrador que Silent, pero que en vez
de descartar los avisos los guarda.

Un cuadro por cada instante t: lo que percibio el agente, lo que le
pregunto a la base de conocimiento, lo que quedo probado en cada casilla
y que accion hizo.
"""

import json
import webbrowser
from pathlib import Path

PLANTILLA = Path(__file__).with_name("plantilla_wumpus.html")

LEYENDA_SABER = (
    "<span><b>V</b> visitada</span>"
    "<span><b>OK</b> probada segura</span>"
    "<span><b>¿pozo?</b> posible, no probado</span>"
    "<span><b>POZO</b> probado</span>"
    "<span><b>A</b> el agente</span>"
    "<span>abajo de cada casilla visitada, lo que percibio ahi</span>"
)

LEYENDA_CUEVA = (
    "<span>La cueva de verdad, la que el agente no ve.</span>"
    "<span>Las casillas azules son las que llego a pisar.</span>"
)


class Silent:
    """View nulo: el agente no narra nada."""

    def PERCEPT(self, t, pos, percept): pass
    def ASK(self, pregunta, respuesta): pass
    def MODELOS(self, que, consistentes, total): pass
    def PLAN(self, plan): pass
    def STEP(self, saber, accion, nota=None): pass
    def DONE(self, kind, texto): pass


silent = Silent()


class Cueva(Silent):
    """Graba un cuadro por cada instante del agente."""

    def __init__(self, mundo, name="EL MUNDO DEL WUMPUS", label="", sub=""):
        self.mundo = mundo
        self.name = name
        self.label = label
        self.sub = sub
        self.frames = []
        self._nuevo()

    def _nuevo(self):
        self.t = 0
        self.pos = (1, 1)
        self.percept = {}
        self.asks = []
        self.modelos = {}
        self.plan = []

    # ---- lo que le avisa el agente ----

    def PERCEPT(self, t, pos, percept):
        self._nuevo()
        self.t = t
        self.pos = tuple(pos)
        self.percept = dict(percept)

    def ASK(self, pregunta, respuesta):
        self.asks.append([pregunta, bool(respuesta)])

    def MODELOS(self, que, consistentes, total):
        self.modelos[que] = [consistentes, total]

    def PLAN(self, plan):
        self.plan = [str(p) for p in plan]

    def STEP(self, saber, accion, nota=None):
        self.frames.append({
            "t": self.t,
            "pos": list(self.pos),
            "percept": self.percept,
            "asks": self.asks,
            "modelos": self.modelos or None,
            "plan": self.plan,
            "accion": str(accion),
            "nota": nota,
            "casillas": {f"{x},{y}": datos for (x, y), datos in saber.items()},
            "oroTomado": any(d.get("tomado") for d in saber.values()),
            "wumpusVivo": True,
            "done": None,
        })

    def DONE(self, kind, texto):
        if self.frames:
            self.frames[-1]["done"] = {"kind": kind, "texto": texto}

    # ---- la pagina ----

    def datos(self):
        mundo = self.mundo
        brisas = sorted({v for p in mundo.pozos for v in mundo.vecinas(p)})
        hedores = sorted(mundo.vecinas(mundo.wumpus))
        return {
            "name": self.name,
            "label": self.label,
            "sub": self.sub,
            "n": mundo.n,
            "cueva": {
                "pozos": [list(p) for p in sorted(mundo.pozos)],
                "wumpus": list(mundo.wumpus),
                "oro": list(mundo.oro),
                "brisas": [list(c) for c in brisas],
                "hedores": [list(c) for c in hedores],
            },
            "leyenda": {"saber": LEYENDA_SABER, "cueva": LEYENDA_CUEVA},
            "frames": self.frames,
        }

    def html(self):
        """La pagina entera, en un string."""
        return PLANTILLA.read_text(encoding="utf-8").replace(
            "__DATA__", json.dumps(self.datos(), ensure_ascii=False)
        )

    def write(self, destino, open_browser=True):
        # Las paginas generadas van todas juntas a salidas/, fuera de 00-lib.
        carpeta = Path(__file__).resolve().parent.parent / "salidas"
        carpeta.mkdir(exist_ok=True)
        salida = carpeta / destino
        salida.write_text(self.html(), encoding="utf-8")
        if open_browser:
            webbrowser.open(salida.as_uri())
        return salida
