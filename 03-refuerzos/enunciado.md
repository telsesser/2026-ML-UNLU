---
title: "Aprendizaje por refuerzos"
subtitle: "Práctica opcional — Clases 1 y 2"
---

## Objetivo

El objetivo de este trabajo es afianzar los conceptos básicos del aprendizaje por refuerzo: el modelado de problemas de decisión secuencial como procesos de decisión de Markov, el cálculo de valores y políticas con iteración de valores y Q-learning, y el uso de redes neuronales para aproximar la función de valor en DQN.

Los ejercicios se resuelven sin computadora. Los notebooks de la
[clase 1](clase1-decisiones-secuenciales.ipynb) y de la [clase 2](clase2-dqn.ipynb)
sirven de consulta.

## Ejercicios

**1. Conceptos.** Un robot aspiradora limpia un departamento de tres
habitaciones. Cada movimiento gasta batería, y puede volver a la base a
cargar. A veces las ruedas patinan y no llega a la habitación elegida.

a. Proponga estados, acciones y recompensas para modelarlo como un proceso de
   decisión de Markov.
b. ¿Por qué no alcanza con un plan fijo y hace falta una política?
c. ¿Qué representa el factor de descuento γ? ¿Qué comportamiento espera con
   γ cercano a 0?
d. ¿Qué es el dilema entre exploración y explotación? ¿Cómo lo resuelve una
   política ε-greedy?

**2. Iteración de valores y Q-learning.** Un MDP tiene dos estados, A y B, y
un estado terminal T. Las transiciones son deterministas:

| estado | acción | va a | recompensa |
|:---:|:---:|:---:|:---:|
| A | avanzar | B | 0 |
| A | quedarse | A | +1 |
| B | salir | T | +10 |
| B | volver | A | 0 |

a. Con γ = 0.9 y valores iniciales $V(A) = V(B) = 0$, haga dos iteraciones de
   la iteración de valores. En cada una, indique la mejor acción en A.
b. Ahora el agente no conoce la tabla. Con todos los $Q(s,a)$ en cero,
   α = 0.5 y γ = 0.9, vive el episodio
   A →avanzar→ B →salir→ T. Aplique la regla de Q-learning en cada paso.
c. ¿Qué necesita conocer la iteración de valores que Q-learning no necesita?

**3. Aproximación de funciones y DQN.** En CartPole el estado son 4 números
reales y hay 2 acciones. Se usa la red Input(4) → Dense(64, ReLU) → Dense(2).

a. ¿Por qué no se puede usar una tabla $Q$?
b. ¿Cuántos parámetros entrenables tiene la red? ¿Qué representa cada salida?
c. Si se entrena la red con cada transición a medida que llega, el agente no
   aprende. ¿Qué agrega DQN para resolverlo y qué resuelve cada parte?
d. Con γ = 0.9, la red objetivo da $(2.0, 3.0)$ para el estado siguiente de
   una transición con recompensa 1. Calcule el objetivo $y$. ¿Cuánto valdría
   si el estado siguiente fuera terminal?
