---
title: "Aprendizaje por refuerzos — recursos"
subtitle: "Qué tema cubre cada recurso"
---

Clase 1: decisiones secuenciales, incertidumbre, utilidad, políticas, retorno,
MDP, exploración/explotación, valores de estado y acción, Q-learning.
Clase 2: aproximación de funciones con redes neuronales, DQN, memoria de
repetición y red objetivo.

## Material de la unidad

| recurso | clase | temas |
| --- | :---: | --- |
| [`clase1-decisiones-secuenciales.ipynb`](clase1-decisiones-secuenciales.ipynb) | 1 | utilidad y MEU (dos apuestas), tragamonedas (greedy, ε-greedy, UCB), mundo 4×3 (plan contra política), retorno y descuento, MDP y ecuación de Bellman, $v$ y $q$, ecuación de optimalidad, iteración de valores (mundo 4×3 y apostador), TD(0), Q-learning (grilla 5×5) |
| [`clase2-dqn.ipynb`](clase2-dqn.ipynb) | 2 | Q-learning en CliffWalking, SARSA, on-policy y off-policy, ε decreciente, CartPole, discretización, aproximación de funciones y semi-gradiente, red neuronal como aproximador, Q-learning con red (inestabilidad), tríada mortal, memoria de repetición, red objetivo, DQN, ablación, Double DQN |
| `presentaciones/C3-1_ Decisiones secuenciales y Q-learning.pptx` | 1 | los mismos temas que el notebook 1, solo conceptos y fórmulas |
| `presentaciones/C3-2_ Aproximación de funciones y DQN.pptx` | 2 | los mismos temas que el notebook 2, solo conceptos y fórmulas |
| [`enunciado-clase1.md`](enunciado-clase1.md) | 1 | preguntas conceptuales; a mano: retorno, tragamonedas (ε-greedy, UCB), iteración de valores, Q-learning; apostador con otras probabilidades; Q-learning en FrozenLake |
| [`enunciado-clase2.md`](enunciado-clase2.md) | 2 | preguntas conceptuales; a mano: SARSA contra Q-learning, objetivo y pérdida de DQN, Double DQN, tabla contra red; SARSA y Q-learning con ε decreciente; DQN en CartPole (red objetivo, memoria, exploración, Double DQN); desafío con Acrobot |

## Bibliografía en `info/`

### Sutton y Barto, *Reinforcement Learning: An Introduction*, 2ª ed. (2018)

`info/RLbook2020trimmed.pdf`. Es la referencia principal de las dos clases.
Las páginas son las del libro; en el PDF hay que sumar 22.

| tema | sección | páginas |
| --- | --- | --- |
| agente, entorno, recompensa | 1.1, 1.3 | 1–2, 6–7 |
| tragamonedas, valor de una acción | 2.1–2.2 | 25–28 |
| actualización incremental | 2.4 | 30–32 |
| valores iniciales optimistas (opcional) | 2.6 | 34–35 |
| UCB | 2.7 | 35–36 |
| interfaz agente–entorno, MDP finito | 3.1 | 47–53 |
| recompensas, retorno, tareas episódicas y continuas | 3.2–3.4 | 53–58 |
| políticas, $v_\pi$, $q_\pi$, ecuación de Bellman | 3.5 | 58–62 |
| política y valores óptimos, ecuación de optimalidad | 3.6 | 62–67 |
| evaluación y mejora de políticas, iteración de políticas | 4.1–4.3 | 74–82 |
| iteración de valores; ejemplo 4.3, el apostador | 4.4 | 82–85 |
| Monte Carlo (opcional, ya no se da en clase) | 5.1–5.3 | 92–100 |
| TD(0), error TD | 6.1 | 119–124 |
| SARSA | 6.4 | 129–131 |
| Q-learning; ejemplo 6.6, CliffWalking | 6.5 | 131–133 |
| sesgo de maximización, Double Q-learning | 6.7 | 134–136 |
| aproximación de funciones de valor | 9.1–9.2 | 198–200 |
| gradiente y semi-gradiente | 9.3 | 200–204 |
| redes neuronales como aproximador | 9.7 | 223–228 |
| control con aproximación (semi-gradiente para $q$) | 10.1 | 243–247 |
| tríada mortal | 11.3 | 264–266 |
| DQN en Atari: memoria de repetición, red objetivo, ablación | 16.5 | 436–441 |

### Russell y Norvig, *Artificial Intelligence: A Modern Approach*, 4ª ed., edición global

Los dos PDF siguen la numeración de la edición **global**, que corre los
capítulos en uno respecto de la edición de Estados Unidos: el capítulo 16 de
acá es el 17 de la otra, y el 23 es el 22. Las páginas son las del PDF.

`info/russell-norvig-cap17-18.pdf`. A pesar del nombre, trae los capítulos 16
(decisiones complejas) y 17 (decisiones multiagente, que no se usa).

| tema | sección | páginas del PDF |
| --- | --- | --- |
| decisiones secuenciales, mundo 4×3, política | 16.1 | 1–3 |
| utilidad a lo largo del tiempo, descuento | 16.1.1 | 3–6 |
| política óptima y utilidad de los estados | 16.1.2 | 6–8 |
| escala de las recompensas | 16.1.3 | 8–9 |
| representación de un MDP | 16.1.4 | 9–11 |
| iteración de valores | 16.2.1 | 11–15 |
| iteración de políticas | 16.2.2 | 15–17 |
| tragamonedas (con el índice de Gittins, más avanzado que en clase) | 16.3 | 20–27 |

El capítulo 15 (decisiones simples: utilidad, MEU, loterías) **no está** en
`info/`. Para la clase 1 alcanza con 16.1.

`info/russell-norvig-cap22-23.pdf`: capítulos 22 (deep learning) y 23
(aprendizaje por refuerzo).

| tema | sección | páginas del PDF |
| --- | --- | --- |
| redes feedforward, gradientes (repaso) | 22.1 | 2–7 |
| deep learning aplicado a refuerzo (panorama) | 22.8.3 | 34–35 |
| aprender de recompensas | 23.1 | 40–42 |
| aprendizaje pasivo, diferencias temporales | 23.2.3 | 44–48 |
| exploración | 23.3.1 | 48–50 |
| Q-learning | 23.3.3 | 52–54 |
| generalización, aproximación de funciones | 23.4–23.4.2 | 54–57 |
| deep RL, DQN, memoria de repetición | 23.4.3 | 57–58 |

## Artículos

| artículo | temas |
| --- | --- |
| Watkins y Dayan (1992), *Q-learning*, Machine Learning 8, 279–292 | demostración de que Q-learning converge |
| Auer, Cesa-Bianchi y Fischer (2002), *Finite-time analysis of the multiarmed bandit problem*, Machine Learning 47, 235–256 | UCB |
| Lin (1992), *Self-improving reactive agents based on reinforcement learning, planning and teaching*, Machine Learning 8, 293–321 | origen de la memoria de repetición |
| Mnih et al. (2013), *Playing Atari with Deep Reinforcement Learning*, arXiv:1312.5602 | primera versión de DQN, con memoria de repetición y sin red objetivo |
| Mnih et al. (2015), *Human-level control through deep reinforcement learning*, Nature 518, 529–533 | DQN completo con red objetivo; algoritmo 1; ablación en 5 juegos |
| van Hasselt, Guez y Silver (2016), *Deep Reinforcement Learning with Double Q-learning*, AAAI | sobreestimación y Double DQN |

## En línea

| recurso | temas |
| --- | --- |
| [Gymnasium](https://gymnasium.farama.org) | documentación de FrozenLake, CliffWalking, CartPole y Acrobot |
| [PyTorch, *Reinforcement Learning (DQN) Tutorial*](https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html) | DQN en CartPole con memoria de repetición y red objetivo (actualización suave) |
| [CleanRL, DQN](https://docs.cleanrl.dev/rl-algorithms/dqn/) | implementación de referencia de DQN en un solo archivo |
| [Hugging Face, *Deep RL Course*](https://huggingface.co/learn/deep-rl-course) | unidad 1: introducción; unidad 2: Q-learning; unidad 3: deep Q-learning en Atari |
| [D. Silver, *UCL Course on RL* (2015)](https://www.davidsilver.uk/teaching/) | clase 2: MDP; clase 3: programación dinámica; clase 5: SARSA y Q-learning; clase 6: aproximación de funciones y DQN |
| [OpenAI, *Spinning Up*](https://spinningup.openai.com) | parte 1: conceptos clave y notación |
