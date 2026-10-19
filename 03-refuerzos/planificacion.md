---
title: "Aprendizaje por refuerzos — planificación 2026"
subtitle: "Qué hay, qué falta y qué leer, tema por tema"
---

## Estado al 18 de octubre

Ya está armado:

| pieza | archivo |
| --- | --- |
| clase 1 | `clase1-decisiones-secuenciales.ipynb`, que sale del notebook 2025 |
| clase 2 | `clase2-dqn.ipynb`, nuevo |
| prácticos | `enunciado-clase1.md` y `enunciado-clase2.md` |
| presentaciones | `presentaciones/`, sobre la plantilla de `utils/`; se regeneran con `armar_presentaciones.py` |
| bibliografía por tema | `recursos.md` |

Cambios respecto de lo que sigue en este documento:

- **Se mantienen el apostador y la grilla 5×5** en la clase 1, para tocar lo
  mínimo el material 2025. El mundo 4×3 aparece solo en la parte nueva de
  utilidad, plan y política. El ejercicio del apostador con otra probabilidad
  pasó al práctico.
- **De Monte Carlo** quedó solo el párrafo que lo explica como idea, como
  puente hacia TD. Blackjack salió.
- **Las capturas de libros** (3 diagramas) quedaron como estaban en el
  notebook.
- **El TP06 no aprendía:** con `np.argmax` sobre la tabla en cero, FrozenLake
  da 0 % de éxito. La guía nueva desempata al azar y lo pregunta.
- **DQN** usa tasa de aprendizaje 5e-4, red objetivo copiada cada C = 200
  pasos y 100.000 pasos de entrenamiento: con eso, las tres semillas aprenden
  (382, 456 y 442 en los últimos 20 episodios, y 500 en evaluación). Con
  50.000 pasos o con C = 500 el resultado dependía mucho de la semilla.
  Ejecutar el notebook completo lleva unos 40 minutos, casi todos en la
  comparación de variantes.
- **La numeración de Russell y Norvig** en los PDF de `info/` es la de la
  edición global: el capítulo de MDP es el 16 y el de refuerzo, el 23. Los
  materiales nuevos citan así. Las secciones de abajo usan la numeración de
  Estados Unidos (17 y 22).

## Punto de partida

El año pasado fue una sola clase. Este año son dos, con este programa:

- **Clase 1 — Decisiones secuenciales.** Incertidumbre, utilidad, políticas,
  retorno y procesos de decisión de Markov. Aprendizaje por refuerzo.
  Exploración/explotación, valores de estado y acción, Q-learning.
- **Clase 2 — Aproximación de funciones con redes neuronales.** Introducción a
  DQN, memoria de repetición y red objetivo.

Material en [`anterior/`](anterior/):

| archivo | qué tiene |
| --- | --- |
| `Semana 8 - Aprendizaje por Refuerzos.ipynb` | bandidos (greedy, ε-greedy, UCB), MDP y ecuación de Bellman, iteración de valores (apostador), Monte Carlo (Blackjack), TD y Q-learning (grilla 5×5 y CliffWalking) |
| `TP06_ Aprendizaje por refuerzos.ipynb` | un único ejercicio: Q-learning en FrozenLake con código a completar |

En resumen: **la clase 1 está cubierta en un ~70 %**, y le faltan sobre todo
la parte de decisión y utilidad y algunos cierres. **La clase 2 no tiene
nada:** hay que armarla entera.

Referencias abreviadas (detalle al final):
**S&B** = Sutton y Barto, *Reinforcement Learning: An Introduction*, 2ª ed.
**R&N** = Russell y Norvig, *AIMA*, 4ª ed.

## Reparto de las 3 horas

Si se sumaba todo lo de arriba, la clase 1 llegaba a unos 190 minutos y la
clase 2 a unos 140. Para emparejarlas:

- **Se saca** lo que no está en el cronograma 2026:
  - Monte Carlo completo (Blackjack, predicción y control MC-ES).
  - El problema del apostador. Pasa al práctico como ejercicio opcional.
  - Iteración de políticas, que queda solo mencionada.
  - La grilla 5×5 duplicada.
- **Pasa a la clase 2:** la parte práctica de Q-learning, que es CliffWalking
  con la comparación SARSA vs. Q-learning y el ε decreciente. La clase 2
  arranca mostrando que la tabla funciona ahí y que no alcanza en CartPole.
- **Un solo ejemplo para la clase 1:** el mundo 4×3 de R&N, desde la utilidad
  hasta Q-learning.
- Los alumnos ya vieron redes neuronales, así que no hace falta un repaso.

| Clase 1 | min | | Clase 2 | min |
| --- | --- | --- | --- | --- |
| 1.1 Utilidad e incertidumbre | 20 | | 2.1 Q-learning en práctica | 30 |
| 1.2 Políticas y retorno | 15 | | 2.2 La tabla no escala | 20 |
| 1.3 MDP, Bellman, iteración de valores | 40 | | 2.3 Red como aproximador | 20 |
| 1.4 Bandidos | 30 | | 2.4 Q-learning con red: inestabilidad | 20 |
| 1.5 Valores de estado y acción, TD | 20 | | 2.5 Memoria de repetición | 20 |
| 1.6 Q-learning en la grilla | 30 | | 2.6 Red objetivo y DQN | 35 |
| margen | 10 | | ablación y cierre | 15 |
| **total** | **~165** | | **total** | **~160** |

DQN y las ablaciones se entrenan antes de la clase y las salidas quedan
guardadas en el notebook, como hace el resto del repo. En vivo se corre solo
un entrenamiento corto.

---

## Clase 1 — Decisiones secuenciales y Q-learning

### 1.1 Decisiones secuenciales, incertidumbre y utilidad

- **Hay:** solo el párrafo de "términos clave" del inicio (agente, política,
  recompensa, valor).
- **Falta:**
  - El puente con las unidades 01 y 02: en búsqueda la acción tenía un
    resultado seguro y alcanzaba con un *plan*. Con transiciones estocásticas
    eso deja de servir y hace falta una *política*.
  - Utilidad y el principio de máxima utilidad esperada (MEU), con un ejemplo
    de lotería.
  - La recompensa como utilidad repartida en el tiempo (hipótesis de la
    recompensa).
  - Un ejemplo que acompañe toda la clase. Recomiendo el mundo 4×3 de R&N:
    80 % de éxito al moverse y 10 % de desvío a cada lado.
- **Leer:** R&N cap. 16 (16.1–16.3) y 17.1 · S&B 3.1–3.2 · R&N cap. 12 si
  hace falta repasar probabilidad.

### 1.2 Políticas y retorno

- **Hay:** definiciones de $G_t$, $\gamma$ y $\pi(a|s)$ en forma de lista.
- **Falta:**
  - Tareas episódicas frente a continuas.
  - Por qué se descuenta: que la suma converja, y la preferencia por lo
    inmediato.
  - Un retorno calculado a mano sobre una trayectoria corta.
  - Política determinista frente a estocástica.
  - Ver en el mundo 4×3 cómo cambia la política óptima según la recompensa
    por paso (la figura clásica de R&N 17.2).
- **Leer:** S&B 3.3–3.4 y 3.5 · R&N 17.1.

### 1.3 Procesos de decisión de Markov

- **Hay:**
  - Propiedad de Markov, ecuación de Bellman para $v_\pi$ e iteración de
    valores con el problema del apostador.
  - Dos diagramas que son capturas pegadas como imagen.
- **Falta:**
  - Definir el MDP como tupla $(\mathcal S, \mathcal A, P, R, \gamma)$.
  - La ecuación de optimalidad de Bellman para $v_*$ y para $q_*$; $q$
    recién aparece en la sección de Monte Carlo.
  - Iteración de valores sobre el mundo 4×3, mostrando cómo crecen los
    valores iteración a iteración. Reemplaza al apostador.
  - Rehacer los diagramas con `00-lib/figuras.py`.
- **Sacar:**
  - El problema del apostador. Pasa al práctico como opcional.
  - Iteración de políticas: solo nombrarla como la alternativa.
- **Leer:** S&B 3.5–3.6 y cap. 4 (4.1–4.4; el apostador es el ejemplo 4.3)
  · R&N 17.2.

### 1.4 Aprendizaje por refuerzo: exploración y explotación

- **Hay:** completo. Bandidos de $k$ brazos, greedy, ε-greedy y UCB, con
  simulaciones y preguntas.
- **Falta:**
  - Una frase que marque el cambio de contexto: ahora no se conoce $P$ ni $R$,
    y hay que aprender interactuando.
  - No sumar valores iniciales optimistas: no entran. El ε decreciente se ve
    en la clase 2.
- **Sacar:** nada. UCB no figura explícito en el programa, pero ya está hecho
  y es corto.
- **Leer:** S&B cap. 2 (2.1–2.7) · R&N 17.3 y 22.1–22.3.

### 1.5 Valores de estado y acción

- **Hay:**
  - $v_\pi$ y $q_\pi$ definidos.
  - Estimación por Monte Carlo y control MC-ES en Blackjack, con gráficos 3D.
- **Falta:**
  - Presentar $v$ y $q$ juntos, junto con la relación
    $v_\pi(s) = \sum_a \pi(a|s)\, q_\pi(s,a)$, y explicar por qué $q$ permite
    elegir la acción sin modelo.
  - Llegar a TD(0) con una sola frase sobre Monte Carlo: "MC promedia
    retornos al final del episodio; TD actualiza en cada paso".
- **Sacar:** Monte Carlo completo (Blackjack, predicción y MC-ES, con sus
  gráficos 3D). No está en el programa y ocupa unos 35 minutos.
- **Leer:** S&B 3.5 y 6.1 · R&N 22.2 · opcional: S&B cap. 5.

### 1.6 Q-learning

- **Hay:** actualización TD(0), la regla de Q-learning, una grilla 5×5 y
  CliffWalking con Gymnasium.
- **Falta:**
  - Q-learning sobre el mundo 4×3, en lugar de la grilla 5×5.
  - Visualizar la tabla Q como flechas de política sobre la grilla.
- **Mover a la clase 2 (2.1):** CliffWalking y la comparación con SARSA.
- **Sacar:** la grilla 5×5, que repite lo mismo.
- **Leer:** S&B 6.1–6.5 · R&N 22.3 · Watkins y Dayan (1992).

---

## Clase 2 — Aproximación de funciones y DQN

Salvo CliffWalking, que viene de la clase 1, todo lo de esta clase falta. La
propuesta es un notebook que lleve el Q-learning tabular a CartPole, paso a
paso.

### 2.1 Q-learning en práctica (viene de la clase 1)

- **Hay:** CliffWalking con Q-learning y Gymnasium.
- **Falta:**
  - Comparar SARSA con Q-learning en CliffWalking (S&B, ejemplo 6.6). Es el
    mejor ejemplo para explicar *on-policy* frente a *off-policy*.
  - ε decreciente, que se reusa en DQN.
  - Medir la tasa de éxito en evaluación, no un solo episodio.
  - Cerrar con la pregunta que abre 2.2: ¿y si el estado es continuo?
- **Leer:** S&B 6.4–6.5 (ejemplo 6.6).

### 2.2 Por qué no alcanza la tabla

- **Falta:**
  - Contar estados: FrozenLake tiene 16, Atari tiene $256^{84\cdot84}$ y
    CartPole tiene un estado continuo.
  - Discretizar CartPole como primer intento, y ver que generaliza mal.
  - Introducir $\hat q(s,a;\mathbf w) \approx q_*(s,a)$, primero lineal.
  - El objetivo de Q-learning como problema de regresión: pérdida cuadrática
    sobre el error TD y gradiente semi-gradiente.
- **Leer:** S&B 9.1–9.3 y 10.1 · R&N 22.4 · Silver, clase 6.

### 2.3 Redes neuronales como aproximador

- **Falta:**
  - Un MLP en PyTorch con entrada $s$ y salida $Q(s,\cdot)$ (una salida por
    acción), y por qué esa arquitectura es mejor que recibir $(s,a)$.
  - No hace falta repasar redes, porque ya las vieron. Alcanza con recordar
    la API de PyTorch que se usa.
- **Leer:** S&B 9.7 · R&N cap. 21 · Goodfellow, Bengio y Courville, cap. 6.

### 2.4 Introducción a DQN: Q-learning con red e inestabilidad

- **Falta:**
  - Q-learning "ingenuo" con red, entrenando con cada transición al
    vuelo. Mostrar que la curva de recompensa oscila o diverge.
  - Diagnosticar las dos causas: muestras correlacionadas y objetivo que se
    mueve con los mismos pesos que se entrenan.
  - Mencionar la *tríada mortal*: aproximación + bootstrapping +
    off-policy.
- **Leer:** S&B 11.3 y 16.5 · Mnih et al. (2013).

### 2.5 Memoria de repetición (*experience replay*)

- **Falta:**
  - Un buffer circular de transiciones $(s,a,r,s',\text{terminal})$ y el
    muestreo de minibatches al azar.
  - Explicar qué rompe (la correlación) y qué permite: reusar cada
    experiencia muchas veces.
- **Leer:** Lin (1992) · Mnih et al. (2013, 2015).

### 2.6 Red objetivo

- **Falta:**
  - Una copia congelada $\hat Q(\cdot;\mathbf w^-)$ para calcular
    $y = r + \gamma \max_{a'} \hat Q(s',a';\mathbf w^-)$, con copia dura cada
    $C$ pasos o actualización suave.
  - Cerrar con el algoritmo DQN completo (algoritmo 1 de Mnih 2015).
  - Entrenar en CartPole-v1, alcanzable en CPU en pocos minutos.
  - Comparar con y sin replay, y con y sin red objetivo. Estos
    entrenamientos se corren antes y las salidas quedan guardadas.
  - Opcional: mencionar Double DQN, pérdida de Huber y ε decreciente.
- **Leer:** Mnih et al. (2015) · tutorial DQN de PyTorch · CleanRL `dqn.py` ·
  Hugging Face Deep RL Course, unidad 3.

---

## Práctico

- **Hay:** TP06 con un ejercicio de Q-learning en FrozenLake.
- **Falta:**
  - **Corregir el TP06:** la evaluación usa `render_mode="human"`, que no
    anda en Colab ni sin pantalla. Además pide una grabación pero no dice
    cómo hacerla (`RecordVideo` necesita `moviepy`). Conviene medir la tasa de
    éxito sobre muchos episodios y comparar `is_slippery` en True y False.
  - **Sumar un ejercicio de la clase 1:** barrer α, γ y ε en FrozenLake y
    explicar los efectos.
  - **Opcional:** el problema del apostador, que sale de la clase. Iteración
    de valores con p = 0.4 y p = 0.6, explicando la forma de la política
    óptima. La consigna ya existe en la celda 23 del notebook anterior.
  - **Sumar un ejercicio de la clase 2:** DQN en CartPole a partir de un
    esqueleto. Pedir la curva de aprendizaje y una ablación sin red objetivo
    o con buffer chico.
  - Pasar la guía a `enunciado.md`, como en `02-agentes`.

## Arreglos al material del año pasado

- La celda de preguntas del apostador (celda 23) tiene pegadas lo que parecen
  respuestas o notas. Hay que sacarlas antes de publicar.
- Tres imágenes son capturas de libros, pegadas en base64. Conviene
  redibujarlas.
- Hay erratas, y el título dice "Aprendizaje Reforzado" en lugar de
  "Aprendizaje por refuerzos".
- Partir el notebook en dos, uno por clase, siguiendo el esquema del repo:
  - Al de la clase 1 van bandidos, MDP, TD y Q-learning.
  - Al de la clase 2 va CliffWalking.
  - Las celdas 24–30 (Monte Carlo) y 32–34 (grilla 5×5) salen.
  - El apostador (celdas 21–23) pasa al práctico.

## Infraestructura del repo

- Agregar `gymnasium[toy-text,classic-control]` y `torch` a
  `pyproject.toml`. Para `torch`, usar la rueda solo-CPU
  (`https://download.pytorch.org/whl/cpu`) para no bajar varios GB de CUDA.
  `moviepy` hace falta solo si se graban videos.
- Renombrar la carpeta a `03-refuerzos`, en minúscula como `01-busqueda` y
  `02-agentes`.
- Sumar las páginas a `render:` y a la navegación en `_quarto.yml`, agregar
  la fila en `index.qmd` y en la tabla del `README.md`.

---

## Bibliografía

**Principal**

- Sutton, R. S. y Barto, A. G. (2018). *Reinforcement Learning: An
  Introduction*, 2ª ed. MIT Press. Libre en
  <http://incompleteideas.net/book/the-book-2nd.html>. Es la base de las
  dos clases: caps. 2–4 y 6 para la clase 1, y 6.4–6.5, 9, 11.3 y 16.5
  para la clase 2. El cap. 5, de Monte Carlo, queda como lectura opcional.
- Russell, S. y Norvig, P. (2020). *Artificial Intelligence: A Modern
  Approach*, 4ª ed. Pearson. Caps. 16–17 (decisiones, utilidad, MDP) y 22
  (aprendizaje por refuerzo). Mantiene la continuidad con las unidades 01
  y 02.

**Artículos**

- Watkins, C. y Dayan, P. (1992). Q-learning. *Machine Learning*, 8,
  279–292.
- Lin, L.-J. (1992). Self-improving reactive agents based on reinforcement
  learning, planning and teaching. *Machine Learning*, 8, 293–321. Es el
  origen del *experience replay*.
- Mnih, V. et al. (2013). Playing Atari with Deep Reinforcement Learning.
  arXiv:1312.5602.
- Mnih, V. et al. (2015). Human-level control through deep reinforcement
  learning. *Nature*, 518, 529–533. Es el DQN con red objetivo.
- van Hasselt, H., Guez, A. y Silver, D. (2016). Deep Reinforcement Learning
  with Double Q-learning. *AAAI*. Opcional.

**Complementaria y práctica**

- Goodfellow, I., Bengio, Y. y Courville, A. (2016). *Deep Learning*, cap. 6.
  <https://www.deeplearningbook.org>. Sirve para el repaso de redes.
- D. Silver, *UCL Course on RL* (2015), clases 1–6, en video y diapositivas:
  <https://www.davidsilver.uk/teaching/>.
- Gymnasium, documentación de los entornos: <https://gymnasium.farama.org>.
- PyTorch, *Reinforcement Learning (DQN) Tutorial*, sobre CartPole:
  <https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html>.
- Hugging Face, *Deep RL Course*, unidades 1–3:
  <https://huggingface.co/learn/deep-rl-course>.
- CleanRL, implementación de DQN en un solo archivo:
  <https://docs.cleanrl.dev/rl-algorithms/dqn/>.
- OpenAI, *Spinning Up*, parte 1 (conceptos clave):
  <https://spinningup.openai.com>.
