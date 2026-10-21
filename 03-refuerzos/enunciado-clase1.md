---
title: "Decisiones secuenciales y Q-learning"
subtitle: "Guía de trabajos prácticos — Clase 1"
---

## Objetivo

Repasar los conceptos de decisión bajo incertidumbre, procesos de decisión de
Markov y aprendizaje por refuerzo vistos en la clase, resolver a mano algunos
cálculos que conviene saber hacer sin computadora, y aplicar Q-learning a un
entorno de Gymnasium.

Referencias: Russell y Norvig, *Artificial Intelligence: A Modern Approach*,
4ª edición, capítulos 15, 16 y 23; Sutton y Barto, *Reinforcement Learning: An
Introduction*, 2ª edición, capítulos 2, 3, 4 y 6. El [notebook de la
clase](clase1-decisiones-secuenciales.ipynb) tiene todo el código que hace
falta.

Notación: usamos la de Sutton y Barto, igual que en el notebook. Lo que Russell
y Norvig llaman utilidad de un estado, $U^\pi(s)$ y $U(s)$, acá es el valor
$v_\pi(s)$ y $v_*(s)$. Su $Q(s,a)$ es nuestro $q_*(s,a)$. Su modelo
$P(s' \mid s,a)$ y $R(s,a,s')$ es nuestra dinámica $p(s',r \mid s,a)$. Las
mayúsculas $V$ y $Q$ son estimaciones.

## 1. Fundamentos teóricos

Respondé las siguientes preguntas. Son del tipo de las que pueden aparecer en
el parcial: alcanzan unas pocas líneas por respuesta, pero justificá siempre.

- ¿Qué diferencia hay entre un plan, como los que devuelven los algoritmos de
  búsqueda, y una política? ¿En qué tipo de entornos alcanza con un plan?

- ¿Qué dice el principio de máxima utilidad esperada? Si una apuesta tiene una
  ganancia esperada de 60 pesos, ¿puede ser racional preferir 50 pesos seguros?

- ¿Qué significa que un proceso cumpla la propiedad de Markov? Pensá un
  ejemplo en el que el estado, tal como está descrito, no la cumpla —por
  ejemplo, una sola foto de una pelota en movimiento— y cómo se podría
  completar el estado para que sí la cumpla.

- ¿Qué representa el factor de descuento $\gamma$? ¿Qué tipo de política
  esperás con $\gamma$ cercano a 0 y con $\gamma$ cercano a 1? ¿Por qué en
  una tarea continua no se puede usar $\gamma = 1$?

- ¿Qué diferencia hay entre $v_\pi(s)$ y $q_\pi(s,a)$? ¿Por qué conociendo
  $q_*$ se puede elegir la mejor acción sin conocer el modelo del mundo, y
  conociendo solo $v_*$ no?

- Explicá con tus palabras la ecuación de Bellman para $v_\pi$. ¿Qué cambia
  en la ecuación de optimalidad?

- ¿Qué necesita conocer la iteración de valores que no necesita Q-learning?
  ¿Por qué eso la vuelve difícil de aplicar en muchos problemas reales?

- En el problema de las tragamonedas, ¿por qué la política greedy puede
  quedarse para siempre en una máquina que no es la mejor? ¿Cómo lo resuelve
  ε-greedy? ¿Y UCB?

- ¿Qué es el error de diferencia temporal? ¿Qué ventaja tienen los métodos de
  diferencias temporales frente a Monte Carlo?

- ¿Por qué se dice que Q-learning es *off-policy*?

## 2. Ejercicios a mano

### 2.1 Retorno

Un agente recibe, en un episodio, las recompensas
$R_1, \dots, R_5 = -1, -1, -1, -1, +10$, y el episodio termina.

- Calculá $G_0$ con $\gamma = 1$ y con $\gamma = 0.9$.

- Calculá $G_3$ con $\gamma = 0.9$, y verificá que se cumple
  $G_t = R_{t+1} + \gamma G_{t+1}$ para $t = 2$.

### 2.2 Tragamonedas

Después de 10 jugadas en tres máquinas se tiene:

| máquina | veces jugada $N(a)$ | promedio $Q(a)$ |
|:---:|:---:|:---:|
| 1 | 6 | 1.0 |
| 2 | 3 | 1.4 |
| 3 | 1 | 0.4 |

- ¿Qué máquina elige la política greedy?

- Con ε-greedy y $\varepsilon = 0.1$, ¿con qué probabilidad se juega cada
  máquina en la próxima jugada?

- Calculá el valor UCB de cada máquina con $c = 2$ y $t = 10$. ¿Cuál elige?
  ¿Por qué elige esa, si es la de menor promedio?

- En la máquina 3 sale una recompensa de 2.0. Actualizá su promedio con la
  fórmula incremental $Q \leftarrow Q + \frac{1}{N}(R - Q)$.

### 2.3 Iteración de valores

Un MDP tiene dos estados, A y B, y un estado terminal T. Las transiciones son
deterministas:

| estado | acción | va a | recompensa |
|:---:|:---:|:---:|:---:|
| A | avanzar | B | 0 |
| A | quedarse | A | +1 |
| B | salir | T | +10 |
| B | volver | A | 0 |

- Con $\gamma = 0.9$ y valores iniciales $V(A) = V(B) = 0$, hacé tres
  iteraciones de la iteración de valores. En cada una, anotá qué acción es la
  mejor en A.

- ¿Cuánto vale quedarse en A para siempre? ¿Y avanzar y salir? ¿Cuál es la
  política óptima con $\gamma = 0.9$?

- Repetí la comparación con $\gamma = 0.8$. ¿Cambia la política? Explicá por
  qué.

### 2.4 Q-learning

Sobre el mismo MDP, con todos los $Q(s,a)$ en cero, $\alpha = 0.5$ y
$\gamma = 0.9$, el agente vive este episodio:

```
A --avanzar--> B --volver--> A --avanzar--> B --salir--> T   (recompensa +10 al salir)
```

- Aplicá la regla de Q-learning en cada paso y escribí la tabla $Q$ al final
  del episodio.

- ¿Por qué $Q(A, \text{avanzar})$ sigue en cero, si avanzar lleva a la meta?

- El agente repite exactamente el mismo episodio. Escribí la tabla al final.
  ¿Cuántos episodios hacen falta para que la recompensa "llegue" hasta A?

## 3. Iteración de valores: el apostador

Usá el código del apostador del notebook de la clase.

- Corré la iteración de valores con probabilidad de cara 0.25 y 0.55.
  Graficá en cada caso la función de valor y la política final.

- Con probabilidad 0.55 la política óptima es muy distinta. Explicá el
  resultado: ¿por qué, cuando la moneda perjudica al jugador, conviene hacer
  pocas apuestas grandes, y cuando lo favorece, muchas apuestas de 1? ¿Por
  qué con 0.25, teniendo 50, apuesta todo, y teniendo 51 no?

- ¿Cuántas iteraciones hacen falta para que el cambio total (`delta`) sea
  menor que $10^{-9}$? Para contarlas, sacá el límite de 12 iteraciones y
  graficá solo al final, fuera del ciclo.

## 4. Q-learning en FrozenLake

### Contexto

El entorno **FrozenLake-v1** representa un lago congelado donde el agente debe
desplazarse desde el punto de inicio (**S**) hasta la meta (**G**) sin caer en
los agujeros (**H**). El lago tiene zonas seguras (**F**) y es resbaladizo: las
acciones pueden no resultar en el movimiento esperado.

El entorno puede configurarse como:

- **Determinista** (`is_slippery=False`): los movimientos siempre resultan como
  se eligen.
- **Estocástico** (`is_slippery=True`): el agente se mueve en la dirección
  elegida con probabilidad 1/3, y hacia cada costado con probabilidad 1/3.

El agente recibe **+1** si llega a la meta y **0** en cualquier otro caso
(caminar o caer).

Documentación: <https://gymnasium.farama.org/environments/toy_text/frozen_lake/>

### Código base

Copiá el siguiente código en un notebook y completá las secciones marcadas con
`TODO`.

```python
import gymnasium as gym
import numpy as np
from collections import defaultdict

# Hiperparámetros
ALPHA = 0.1        # Tasa de aprendizaje
GAMMA = 0.99       # Factor de descuento
EPSILON = 0.1      # Exploración epsilon-greedy
EPISODES = 2000    # Cantidad de episodios de entrenamiento

# Crear entorno (usar mapa 4x4 por defecto)
env = gym.make("FrozenLake-v1", is_slippery=True)

# Q-Table inicial
Q = defaultdict(lambda: np.zeros(env.action_space.n))

def epsilon_greedy_policy(state):
    """Devuelve una acción siguiendo política epsilon-greedy."""
    if np.random.random() < EPSILON:
        return env.action_space.sample()  # acción aleatoria
    # mejor acción conocida; si hay empate, se elige al azar entre las mejores
    mejores = np.flatnonzero(Q[state] == Q[state].max())
    return int(np.random.choice(mejores))

# Entrenamiento
rewards_per_episode = []

for episode in range(EPISODES):
    state, _ = env.reset()
    done = False
    total_reward = 0

    while not done:
        # TODO: seleccionar acción con política epsilon-greedy
        # action = ...

        # TODO: ejecutar acción en el entorno
        # next_state, reward, terminated, truncated, _ = env.step(action)

        # TODO: calcular el objetivo TD y el error TD
        # (si el estado siguiente es terminal, no hay valor futuro)
        # td_target = ...
        # td_error = ...

        # TODO: actualizar Q[state][action]
        # Q[state][action] += ALPHA * td_error

        # TODO: actualizar estado y acumulador de recompensa
        # state = next_state
        # total_reward += reward
        # done = terminated or truncated

    rewards_per_episode.append(total_reward)

print("Entrenamiento completado")


def tasa_de_exito(Q, is_slippery=True, episodios=1000):
    """Fracción de episodios en que la política greedy llega a la meta."""
    env = gym.make("FrozenLake-v1", is_slippery=is_slippery)
    exitos = 0
    for ep in range(episodios):
        state, _ = env.reset(seed=ep)
        done = False
        while not done:
            state, reward, terminated, truncated, _ = env.step(int(np.argmax(Q[state])))
            done = terminated or truncated
        exitos += reward
    return exitos / episodios


def mostrar_politica(Q, mapa=("SFFF", "FHFH", "FFFH", "HFFG")):
    """Dibuja la acción greedy de cada casilla sobre el mapa."""
    flechas = "←↓→↑"   # el orden de las acciones en FrozenLake
    n = len(mapa[0])
    for fila in range(len(mapa)):
        print(" ".join(mapa[fila][col] if mapa[fila][col] in "HG"
                       else flechas[int(np.argmax(Q[fila * n + col]))]
                       for col in range(n)))


print(f"Tasa de éxito: {tasa_de_exito(Q):.1%}")
mostrar_politica(Q)
```

### Enunciado

- Completá los `TODO` y entrená al agente en el lago resbaladizo. Informá la
  tasa de éxito de la política aprendida y mostrá la política sobre el mapa.

- En el código base, la política ε-greedy desempata **al azar** entre las
  acciones de mayor valor. Reemplazá esa línea por `np.argmax(Q[state])` y
  volvé a entrenar. ¿Qué pasa? Explicá por qué, pensando en cómo arranca la
  tabla y en cuándo el agente recibe una recompensa distinta de cero.

- Repetí con `is_slippery=False`. ¿Qué tasa de éxito se obtiene? ¿Hacen falta
  tantos episodios? Ojo: para evaluar en el lago que no resbala hay que
  llamar a `tasa_de_exito(Q, is_slippery=False)`; por defecto evalúa en el
  resbaladizo.

- Probá $\alpha \in \{0.01, 0.1, 0.5\}$ y $\gamma \in \{0.9, 0.99\}$ en el lago
  resbaladizo. Armá una tabla con la tasa de éxito, usando al menos dos
  semillas por combinación. ¿Por qué con $\alpha = 0.1$ y $0.5$ el valor de
  $\gamma$ cambia tanto el resultado, si la única recompensa es la de la
  meta? ¿Y por qué con $\alpha = 0.01$ casi no cambia nada?

- En el lago resbaladizo, la política aprendida a veces elige moverse **contra
  un borde o alejándose de la meta**. Buscá un ejemplo en tu política y
  explicá por qué tiene sentido.

- *Opcional:* probá el mapa de 8×8 (`map_name="8x8"`). ¿Qué hay que cambiar
  para que el agente aprenda?
