# Aprendizaje Automático — UNLU 2026

Material de clase. Cada unidad numerada tiene su notebook y su trabajo
práctico; todas se publican juntas en un mismo sitio.

Referencias a Russell & Norvig, *Artificial Intelligence: A Modern Approach*,
4ª edición.

## Las carpetas

| carpeta | qué hay |
| --- | --- |
| [`00-lib/`](00-lib/) | lo común a todas las unidades: `Problem`, `Node`, la frontera, el narrador (`view`, `web`) y los cinco algoritmos de búsqueda. Nada de esto sabe de ningún problema en particular. |
| [`01-busqueda/`](01-busqueda/) | **búsqueda no informada** sobre el mapa de Rumania, y el práctico del [8-puzzle](01-busqueda/8-puzzle/). |
| [`02-agentes/`](02-agentes/) | **agentes basados en conocimiento**: lógica proposicional e inferencia. |

Cada unidad guarda las piezas que solo le sirven a ella:
`01-busqueda/romania.py` es el mapa; `01-busqueda/8-puzzle/puzzle.py`,
`web_puzzle.py` y `plantilla_puzzle.html` son el tablero y su dibujo.

Para agregar una unidad: crear `NN-nombre/` con su notebook y su
`enunciado.md`, y sumar las dos páginas a `render:` y a la navegación en
[`_quarto.yml`](_quarto.yml), más su fila en [`index.qmd`](index.qmd).

## Cómo se corre

```bash
uv sync

# el sitio entero, con el indice y todas las unidades
quarto preview

# los algoritmos solos, contra el mapa de Rumania
uv run python 00-lib/breadth_first_search.py --view

# la tabla comparativa del 8-puzzle
uv run python 01-busqueda/8-puzzle/puzzle.py
```

Las páginas paso a paso que escriben esos scripts van a `salidas/`, que no se
versiona.

## Publicar

El sitio sale de la raíz, y son todas las unidades a la vez:

```bash
quarto publish gh-pages
```

Queda en <https://telsesser.github.io/2026-ML-UNLU/>.

## Qué no se publica

`_quarto.yml` trae una lista explícita en `render:`: Quarto renderiza solo lo
que figura ahí. Quedan deliberadamente afuera del sitio público los
solucionarios y los notebooks con la resolución de los prácticos —hoy
`01-busqueda/8-puzzle/solucionario.md` y `01-busqueda/8-puzzle/8-puzzle.ipynb`—.
Están versionados en el repositorio, que es público: si tienen que ser
privados, hay que sacarlos del repositorio, no solo del sitio.
