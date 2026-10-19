"""
Las ilustraciones estaticas del notebook.

A diferencia de web.py y wumpus_web.py, aca no hay pasos que recorrer.
Devuelven HTML para meter directo en una celda, sin iframe, asi heredan la
tipografia de la pagina.

    ver_modelos   los modelos posibles, uno por cuadrito, con lo que vale en
                  cada uno marcado abajo (figura 7.5)
"""

from html import escape

from IPython.display import HTML

# Los colores son los mismos de plantilla.html, que a su vez los saca del
# tema cosmo del sitio. Van escritos a mano porque esto no es una pagina
# aparte: se mete adentro de una que ya tiene su CSS.
CSS = """
<style>
.mv { margin: 1.2em 0; }
.mv-grilla {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(148px, 1fr));
  gap: 14px;
}
.mv-modelo {
  margin: 0; padding: 9px 9px 7px;
  border: 1px solid #DEE2E6; border-radius: 4px; background: #FFFFFF;
}
/* Los modelos donde la KB es falsa quedan atras: en el libro son los que
   caen afuera de la linea solida. */
.mv-modelo.mv-fuera { opacity: .45; }
.mv-modelo.mv-dentro { border-color: #00769E; background: rgba(0, 118, 158, .05); }

.mv-n {
  font: 400 10px/1 SFMono-Regular, Menlo, Consolas, monospace;
  color: #999CA0; letter-spacing: .06em; text-transform: uppercase;
}
.mv-cueva { display: grid; gap: 3px; margin: 5px 0 7px; }
.mv-c {
  position: relative; aspect-ratio: 1 / 1;
  border: 1px solid #DEE2E6; border-radius: 3px; background: #FFFFFF;
  display: flex; flex-direction: column; justify-content: center;
  align-items: center; gap: 1px; overflow: hidden;
}
.mv-c.mv-nada { background: #F8F9FA; border-style: dashed; }
.mv-c.mv-visitada { background: rgba(0, 118, 158, .07); border-color: #00769E; }
.mv-c.mv-pozo { background: rgba(173, 0, 0, .09); border-color: #AD0000; }
.mv-xy {
  position: absolute; top: 2px; left: 3px;
  font: 400 8px/1 SFMono-Regular, Menlo, Consolas, monospace; color: #999CA0;
}
.mv-marca { font: 700 9.5px/1.1 system-ui, sans-serif; letter-spacing: .03em; }
.mv-marca.mv-p { color: #AD0000; }
.mv-marca.mv-a { color: #00769E; font-size: 12px; }
.mv-marca.mv-v { color: #5E5E5E; }
.mv-sensor { font: 400 8px/1.1 system-ui, sans-serif; color: #5E5E5E; }

.mv-chips { display: flex; flex-wrap: wrap; gap: 4px; }
.mv-chip {
  font: 400 10.5px/1 system-ui, sans-serif;
  color: #999CA0; border: 1px solid #DEE2E6; border-radius: 3px;
  padding: 3px 5px;
}
.mv-chip.mv-on { color: #20794D; border-color: #20794D; font-weight: 600; }
.mv-pie {
  margin: 12px 0 0; font-size: 13px; color: #5E5E5E;
  padding-left: 10px; border-left: 2px solid #DEE2E6;
}
</style>
"""


def _coords(nombre):
    """De "[1,2]" a (1, 2)."""
    x, y = nombre.strip("[]").split(",")
    return int(x), int(y)


def ver_modelos(modelos, habitaciones, pruebas, visitadas=None, agente=None,
                pie=None):
    """Dibuja un cuadrito por modelo, con lo que vale en el marcado abajo.

    modelos       la lista de modelos: dicts habitacion -> hay pozo o no
    habitaciones  las que estan en duda, o sea los simbolos del problema
    pruebas       dict nombre -> f(modelo) -> bool. La primera es la que
                  decide si el modelo queda adentro o afuera: la KB.
    visitadas     dict habitacion -> que se percibio ahi
    agente        en cual de ellas esta parado ahora
    pie           el texto de abajo; si no se pasa, se arma solo
    """
    visitadas = visitadas or {}
    en_juego = list(habitaciones) + list(visitadas)
    ancho = max(_coords(h)[0] for h in en_juego)
    alto = max(_coords(h)[1] for h in en_juego)
    nombre_kb = next(iter(pruebas))

    tarjetas = []
    for i, m in enumerate(modelos, start=1):
        dentro = pruebas[nombre_kb](m)

        celdas = []
        # La fila de arriba es la y mas grande: el eje y del libro va para
        # arriba y el de una grilla HTML va para abajo.
        for y in range(alto, 0, -1):
            for x in range(1, ancho + 1):
                casilla = f"[{x},{y}]"
                clase, marcas = "mv-c", []
                if casilla in visitadas:
                    clase += " mv-visitada"
                    if casilla == agente:
                        marcas.append('<span class="mv-marca mv-a">A</span>')
                    else:
                        marcas.append('<span class="mv-marca mv-v">V</span>')
                    if visitadas[casilla]:
                        marcas.append(f'<span class="mv-sensor">'
                                      f'{escape(visitadas[casilla])}</span>')
                elif casilla in habitaciones:
                    if m[casilla]:
                        clase += " mv-pozo"
                        marcas.append('<span class="mv-marca mv-p">POZO</span>')
                else:
                    clase += " mv-nada"
                celdas.append(f'<div class="{clase}">'
                              f'<span class="mv-xy">{x},{y}</span>'
                              f'{"".join(marcas)}</div>')

        chips = "".join(
            f'<span class="mv-chip{" mv-on" if f(m) else ""}">{escape(n)}</span>'
            for n, f in pruebas.items())

        tarjetas.append(
            f'<figure class="mv-modelo {"mv-dentro" if dentro else "mv-fuera"}">'
            f'<span class="mv-n">modelo {i}</span>'
            f'<div class="mv-cueva" style="grid-template-columns:'
            f' repeat({ancho}, 1fr)">{"".join(celdas)}</div>'
            f'<figcaption class="mv-chips">{chips}</figcaption>'
            f'</figure>')

    if pie is None:
        cuantos = sum(1 for m in modelos if pruebas[nombre_kb](m))
        otras = [n for n in pruebas if n != nombre_kb]
        partes = [f"Los {len(modelos)} modelos posibles. En {cuantos} de ellos "
                  f"{nombre_kb} es verdadera: son los resaltados."]
        consistentes = [m for m in modelos if pruebas[nombre_kb](m)]
        for n in otras:
            donde = sum(1 for m in consistentes if pruebas[n](m))
            if donde == len(consistentes):
                partes.append(f"{n} es verdadera en los {donde}, "
                              f"así que {nombre_kb} ⊨ {n}.")
            else:
                partes.append(f"{n} es verdadera en {donde} de esos {cuantos} y "
                              f"falsa en el resto, así que {nombre_kb} ⊭ {n}.")
        pie = " ".join(partes)

    return HTML(f'{CSS}<div class="mv"><div class="mv-grilla">'
                f'{"".join(tarjetas)}</div>'
                f'<p class="fg-pie">{pie}</p></div>')
