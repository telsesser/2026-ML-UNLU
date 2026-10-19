---
title: "Aproximación de funciones y DQN"
subtitle: "Guía de trabajos prácticos — Clase 2"
---

## Objetivo

Repasar la diferencia entre SARSA y Q-learning, entender por qué hace falta
aproximar la función de valor cuando hay muchos estados, y experimentar con
las piezas de DQN: la red, la memoria de repetición y la red objetivo.

Referencias: Sutton y Barto, *Reinforcement Learning: An Introduction*, 2ª
edición, secciones 6.4–6.5, capítulo 9 y secciones 11.3 y 16.5; Russell y
Norvig, *Artificial Intelligence: A Modern Approach*, 4ª edición, sección 23.4;
Mnih et al. (2015), *Human-level control through deep reinforcement learning*.
El [notebook de la clase](clase2-dqn.ipynb) tiene todo el código que hace
falta.

## 1. Fundamentos teóricos

Respondé las siguientes preguntas. Son del tipo de las que pueden aparecer en
el parcial: alcanzan unas pocas líneas por respuesta, pero justificá siempre.

- En CliffWalking, Q-learning aprende el camino pegado al acantilado y SARSA
  uno más alejado. ¿Cuál de los dos es mejor? ¿Depende de si el agente sigue
  explorando después de entrenar?

- ¿Por qué SARSA es *on-policy* y Q-learning *off-policy*? Señalá en qué
  término de cada regla de actualización aparece la diferencia.

- ¿Por qué una tabla no sirve cuando el estado son números reales? ¿Qué
  problemas tiene discretizar?

- ¿Qué significa que un aproximador de funciones **generalice**? ¿Por qué eso
  es una ventaja y también una fuente de problemas?

- ¿Por qué el método de aproximación que vimos se llama de *semi*-gradiente?

- ¿Por qué la red de DQN recibe solo el estado y tiene una salida por acción,
  en vez de recibir el estado y la acción?

- ¿Qué problema resuelve la memoria de repetición? ¿Por qué esa idea funciona
  con Q-learning pero no con SARSA?

- ¿Qué problema resuelve la red objetivo? ¿Qué pasa si se copia en cada paso
  ($C = 1$)? ¿Y si casi nunca se copia?

- ¿Qué es la tríada mortal? ¿Cuáles de sus tres elementos tiene DQN?

- ¿Se puede usar DQN si la acción es continua, como el ángulo de un volante?
  ¿Qué paso del algoritmo lo impide?

- ¿Qué problema intenta resolver Double DQN, y cómo?

## 2. Ejercicios a mano

### 2.1 SARSA y Q-learning

Un agente en CliffWalking está en el estado $s$, toma la acción $a$ y recibe
$r = -1$. Llega a $s'$, donde la tabla tiene estos valores:

| acción en $s'$ | ↑ | → | ↓ | ← |
|:---:|:---:|:---:|:---:|:---:|
| $Q(s', \cdot)$ | −5 | −3 | −8 | −4 |

Además, $Q(s,a) = -4$, $\alpha = 0.5$ y $\gamma = 1$. Al explorar, la política
ε-greedy elige como próxima acción $a' = {}$↓.

- Calculá el nuevo $Q(s,a)$ con Q-learning y con SARSA.

- ¿Por qué SARSA "castiga" a $Q(s,a)$ y Q-learning no? Relacionalo con lo que
  pasa en CliffWalking cuando el agente camina pegado al acantilado.

### 2.2 El objetivo de DQN

Un minibatch tiene tres transiciones. Para cada una se conocen la recompensa,
si $s'$ es terminal, la salida de la **red objetivo** para $s'$ (una por
acción) y la salida de la **red principal** para la acción tomada en $s$. Usá
$\gamma = 0.99$.

| $j$ | $r_j$ | $s'_j$ terminal | $\hat{q}(s'_j, \cdot\,; \mathbf{w}^-)$ | $\hat{q}(s_j, a_j; \mathbf{w})$ |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 1 | no | (2.0, 3.0) | 3.5 |
| 2 | 1 | sí | (1.5, 0.5) | 2.0 |
| 3 | 0 | no | (4.0, 1.0) | 3.0 |

- Calculá el objetivo $y_j$ y el error $y_j - \hat{q}(s_j, a_j; \mathbf{w})$ de
  cada transición.

- Calculá la pérdida como el promedio de los errores al cuadrado.

- Para la transición 3, la red **principal** da $\hat{q}(s'_3, \cdot\,;
  \mathbf{w}) = (0.5, 2.0)$. ¿Cuál sería el objetivo con Double DQN? ¿Por qué
  es menor?

### 2.3 Tabla contra red

- Contá los parámetros (pesos y sesgos) de la red de la clase: 4 entradas, dos
  capas ocultas de 128 y 2 salidas.

- Contá cuántos valores tiene una tabla $Q$ para CartPole discretizado con 10
  intervalos por variable.

- Son cantidades parecidas. ¿Por qué la red funciona mucho mejor?

## 3. SARSA y Q-learning con exploración decreciente

Usá la función `entrenar_cliff` del notebook de la clase.

- Modificala para que ε baje en forma lineal de 0.1 a 0 a lo largo de los
  episodios.

- Repetí la comparación entre SARSA y Q-learning (10 corridas de cada uno).
  ¿Qué camino aprende cada uno ahora? ¿Qué pasa con la recompensa de los
  últimos episodios?

- Explicá el resultado con lo que respondiste en la parte 1.

## 4. DQN en CartPole

### Código base

Copiá el siguiente código en un notebook y completá las secciones marcadas con
`TODO`. Es la misma estructura que el notebook de la clase.

```python
import random
from collections import deque

import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn

torch.set_num_threads(1)
GAMMA = 0.99


def crear_red(entradas=4, salidas=2):
    return nn.Sequential(
        nn.Linear(entradas, 128), nn.ReLU(),
        nn.Linear(128, 128), nn.ReLU(),
        nn.Linear(128, salidas),
    )


class MemoriaRepeticion:
    def __init__(self, capacidad):
        self.datos = deque(maxlen=capacidad)

    def guardar(self, s, a, r, s2, terminado):
        self.datos.append((s, a, r, s2, terminado))

    def muestrear(self, tamano):
        lote = random.sample(self.datos, tamano)
        s, a, r, s2, terminado = map(np.array, zip(*lote))
        return (torch.as_tensor(s, dtype=torch.float32), torch.as_tensor(a),
                torch.as_tensor(r, dtype=torch.float32),
                torch.as_tensor(s2, dtype=torch.float32),
                torch.as_tensor(terminado, dtype=torch.float32))

    def __len__(self):
        return len(self.datos)


def epsilon_lineal(paso, inicial=1.0, final=0.05, pasos_decaimiento=10_000):
    return max(final, inicial - (inicial - final) * paso / pasos_decaimiento)


def dqn(entorno="CartPole-v1", pasos_totales=100_000, semilla=0, alpha=5e-4,
        capacidad=10_000, tamano_lote=64, C=200, inicio=1000,
        pasos_decaimiento=10_000):
    random.seed(semilla); np.random.seed(semilla); torch.manual_seed(semilla)
    env = gym.make(entorno)
    entradas = env.observation_space.shape[0]
    salidas = env.action_space.n
    red = crear_red(entradas, salidas)
    red_objetivo = crear_red(entradas, salidas)
    red_objetivo.load_state_dict(red.state_dict())
    optimizador = torch.optim.Adam(red.parameters(), lr=alpha)
    memoria = MemoriaRepeticion(capacidad)

    recompensas, paso, episodio = [], 0, 0
    while paso < pasos_totales:
        s, _ = env.reset(seed=semilla * 10_000 + episodio)
        total, fin = 0, False
        while not fin:
            if random.random() < epsilon_lineal(paso, pasos_decaimiento=pasos_decaimiento):
                a = random.randrange(salidas)
            else:
                with torch.no_grad():
                    a = int(red(torch.as_tensor(s, dtype=torch.float32)).argmax())

            s2, r, terminado, truncado, _ = env.step(a)
            memoria.guardar(s, a, r, s2, terminado)
            s, total, paso = s2, total + r, paso + 1
            fin = terminado or truncado

            if len(memoria) < inicio:
                continue

            S, A, R, S2, T = memoria.muestrear(tamano_lote)

            # TODO: calcular el objetivo y con la red objetivo, sin derivar
            # (si s' es terminal, T vale 1 y no hay valor futuro)
            # with torch.no_grad():
            #     y = ...

            # TODO: valores de la red principal para las acciones tomadas
            # q_sa = red(S).gather(1, A.unsqueeze(1)).squeeze(1)

            # TODO: pérdida de Huber y paso de gradiente
            # perdida = nn.functional.smooth_l1_loss(q_sa, y)
            # ...

            # TODO: cada C pasos, copiar los pesos de la red a la red objetivo

        recompensas.append(total)
        episodio += 1
    return np.array(recompensas), red


recompensas, red = dqn()
plt.plot(recompensas)
plt.xlabel("Episodios")
plt.ylabel("Recompensa")
plt.show()
```

### Enunciado

Para cada experimento usá al menos tres semillas y graficá las curvas de
aprendizaje (conviene suavizarlas con un promedio móvil). Cada entrenamiento
de 100.000 pasos tarda entre dos y tres minutos.

- Completá los `TODO`, entrená y verificá que el agente llega a valores
  cercanos a 500.

- **Red objetivo:** probá $C \in \{1, 200, 1000, 5000\}$. ¿Qué pasa en los
  extremos?

- **Memoria:** probá capacidades de 100, 1.000, 10.000 y 50.000 transiciones.
  ¿Por qué una memoria muy chica se parece a no tener memoria?

- **Exploración:** probá `pasos_decaimiento` de 1.000 y de 30.000. ¿Qué pasa
  si el agente deja de explorar muy pronto? ¿Y si explora durante mucho
  tiempo?

- **Double DQN:** cambiá el cálculo del objetivo para que la acción de $s'$ la
  elija la red principal y la evalúe la red objetivo. Es un cambio de dos
  líneas. Compará con DQN.

## 5. Desafío: Acrobot

En **Acrobot-v1** hay que balancear un péndulo doble, aplicando torque en la
articulación del medio, hasta que la punta supere una altura. El estado tiene
6 números, hay 3 acciones, y la recompensa es −1 por paso hasta lograrlo (como
máximo 500 pasos, así que el peor retorno es −500).

Documentación: <https://gymnasium.farama.org/environments/classic_control/acrobot/>

- Entrená DQN en Acrobot con el mismo código, pasando
  `entorno="Acrobot-v1"`. ¿Qué cambia en la red?

- ¿Qué recompensa promedio obtiene la política aprendida? Compará con una
  política al azar.

- La recompensa es −1 en todos los pasos hasta el final. ¿Por qué igual sirve
  para aprender? ¿Qué rol cumple la exploración al principio?
