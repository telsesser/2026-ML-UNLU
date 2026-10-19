---
title: "Agentes basados en conocimiento"
subtitle: "Guía de laboratorio"
---

## Objetivo

Modelar un problema como una base de conocimiento en lógica proposicional,
consultarla por implicación lógica con SymPy, y distinguir con claridad las
tres respuestas posibles: lo que se deduce, lo que se refuta y lo que queda
desconocido.

Referencia: Russell y Norvig, *Artificial Intelligence: A Modern Approach*,
4ª edición, capítulo 7. El [notebook de la clase](agentes.ipynb) tiene todo
el código que hace falta.

## 1. Un ejemplo pequeño para razonar

Considerá la siguiente base de conocimiento, con tres símbolos:

```
R1:  Llueve ⇒ Mojada
R2:  Riego ⇒ Mojada
R3:  Mojada
```

Razoná primero sin ejecutar código:

- ¿Cuántos modelos posibles hay? ¿En cuántos de ellos es verdadera la base?

- ¿Se sigue `Llueve`? ¿Se sigue `¬Llueve`? ¿Qué respondería `consultar` a cada
  pregunta, y por qué las dos respuestas no se contradicen?

- Agregá `R4: ¬Riego`. ¿Cambia alguna de las respuestas anteriores? Explicá por
  qué la lluvia sigue sin poder afirmarse.

- Reemplazá `R1` y `R2` por una sola sentencia, `Mojada ⇔ (Llueve ∨ Riego)`.
  Con `R3` y `R4`, ¿qué se sigue ahora? ¿Qué diferencia hay entre decir "si
  llueve, se moja" y "se moja exactamente cuando llueve o se riega"?

- Escribí cada versión de la base en forma normal conjuntiva. ¿Cuáles de sus
  cláusulas son definidas? ¿Alguna de las versiones podría resolverse por
  encadenamiento hacia adelante?

## 2. De la idea a la implementación

En esta parte usamos SymPy y la función `consultar` de la clase. El entorno del
curso ya tiene SymPy instalado; no hace falta programar ningún motor de
inferencia ni definir clases.

```python
from sympy import symbols, And, Or, Not, Implies, Equivalent, to_cnf
from sympy.logic.boolalg import truth_table
from sympy.logic.inference import satisfiable


def consultar(base, proposicion):
    if satisfiable(base) is False:
        return "Base inconsistente"
    if satisfiable(And(base, Not(proposicion))) is False:
        return "Verdadero"
    if satisfiable(And(base, proposicion)) is False:
        return "Falso"
    return "Desconocido"


Llueve, Riego, Mojada = symbols("Llueve Riego Mojada")
base = And(Implies(Llueve, Mojada), Implies(Riego, Mojada), Mojada)

print(consultar(base, Llueve))
print(to_cnf(base))
```

Ejecutá las consultas de la parte 1 sobre las tres versiones de la base y reuní
evidencias de su comportamiento.

- Informá, para cada versión, la respuesta a `Llueve` y a `¬Llueve`, y compará
  con lo que razonaste.

- Contá los modelos de cada versión con `truth_table` y verificá tu cuenta a
  mano.

- Convertí cada versión con `to_cnf`. Sobre la que sea de cláusulas definidas,
  corré el encadenamiento hacia adelante del notebook (`pl_fc_entails`) y
  comparalo con `consultar`. Registrá cuándo coinciden y cuándo no, y qué
  significa cada `False` del encadenamiento.

## 3. Desafío: ¿podemos lanzar el experimento?

Un equipo prepara experimentos de aprendizaje automático. Antes de ejecutarlos,
necesita decidir qué recurso puede usar y qué tareas pendientes debe resolver.
El asistente **no elige el mejor modelo ni ejecuta el experimento**: revisa
condiciones declaradas.

El equipo acordó este protocolo:

- Los datos están listos cuando fueron validados y su uso fue autorizado. Ambas
  condiciones son necesarias; el protocolo define «datos listos» exactamente de
  esa manera.

- El entorno está listo si están instaladas las dependencias y la prueba mínima
  de ejecución funciona. También se define exactamente por esas dos
  condiciones.

- Si los datos y el entorno están listos, el experimento está técnicamente
  preparado.

- Si está preparado y hay una GPU disponible, se puede lanzar en GPU.

- Si está preparado, el experimento admite CPU y hay una CPU disponible, se
  puede lanzar en CPU.

- Basta con que pueda lanzarse en alguno de esos recursos para recomendar
  iniciar una ejecución.

- Si se comprobó que los datos no fueron validados, se recomienda validar los
  datos. Si se comprobó que falta autorización, se recomienda gestionarla. Si se
  comprobó que la prueba mínima falla, se recomienda revisar el entorno.

Que un experimento pueda usar ambos recursos no obliga a elegir uno: la
prioridad, el costo y la planificación quedan fuera de este protocolo.

| Observación | Caso A | Caso B | Caso C |
|:---|:---:|:---:|:---:|
| Datos validados | Sí | Sí | Sí |
| Uso autorizado | Sí | Sí | ? |
| Dependencias instaladas | Sí | Sí | Sí |
| Prueba mínima funciona | Sí | Sí | Sí |
| GPU disponible | Sí | No | Sí |
| Admite CPU | No | Sí | No |
| CPU disponible | No | Sí | No |

`?` significa que no tenemos esa información, no que la respuesta sea negativa.

1. Modelen el protocolo. Distingan las expresiones «si» de las definiciones
   «exactamente cuando»: ¿qué conector corresponde en cada caso?

2. Para cada caso, consulten si los datos están listos, si se puede usar cada
   recurso y si se recomienda iniciar. Fundamenten las respuestas con las reglas
   y observaciones relevantes.

3. Completen el caso C primero con autorización positiva y luego con
   autorización negativa, en **dos bases separadas**. Comparen las conclusiones
   y las recomendaciones.

4. Construyan un caso inconsistente y comprueben que se detecta antes de
   recomendar acciones. No confundan una imposibilidad de ejecución con una
   contradicción lógica.

## 4. Desafío: ¿qué conviene revisar en una sala de lectura?

Una biblioteca recibe quejas porque algunas salas están demasiado oscuras.
Quiere un asistente sencillo que sugiera comprobaciones sin atribuir causas que
todavía no se verificaron.

El protocolo de mantenimiento establece:

- Una sala se considera bien iluminada exactamente cuando tiene suficiente luz
  natural **o** iluminación artificial suficiente; también puede tener ambas.

- Si la sala está ocupada y no está bien iluminada, se recomienda intervenir.

- Si se recomienda intervenir y las cortinas están cerradas, se recomienda
  abrirlas.

- Si se recomienda intervenir y las lámparas están apagadas, se recomienda
  encenderlas.

- Si se recomienda intervenir, las lámparas están encendidas y la iluminación
  artificial no es suficiente, se recomienda revisar las luminarias.

No sabemos de antemano si abrir las cortinas o encender las lámparas resolverá
el problema. Las reglas recomiendan acciones; **no incorporan sus resultados
como hechos**.

| Observación | Sala A | Sala B | Sala C |
|:---|:---:|:---:|:---:|
| Está ocupada | Sí | Sí | Sí |
| Luz natural suficiente | No | No | ? |
| Iluminación artificial suficiente | No | No | No |
| Cortinas cerradas | Sí | No | Sí |
| Lámparas encendidas | No | Sí | No |

1. Definan el vocabulario y modelen el protocolo. Presten atención a que
   «lámparas encendidas» e «iluminación artificial suficiente» no significan lo
   mismo.

2. Consulten si cada sala está bien iluminada y qué acciones se recomiendan.
   Expliquen cualquier diferencia entre desconocido y falso.

3. Para la sala A, supongan que se abrieron las cortinas. Armen **una nueva
   observación**, cambiando ese dato y dejando desconocido si ahora la luz
   natural alcanza. ¿Se puede afirmar que el problema se resolvió? Luego
   incorporen el resultado de una nueva medición y vuelvan a consultar.

4. Propongan una nueva regla útil, justifíquenla y construyan un caso que
   muestre su efecto. No cambien el motor: cambien el conocimiento del dominio.

## 5. Un problema nuevo

Elegí un protocolo, reglamento o lista de control que conozcas bien —las
condiciones para rendir una materia, el checklist de un despliegue, los
requisitos de un préstamo— y construí con él un asistente como el de la clase.

- Definí el vocabulario: qué proposiciones hay, qué significa cada una, cuáles
  son observaciones y cuáles recomendaciones.

- Escribí las reglas y armá al menos tres casos, uno de ellos con una
  observación desconocida. Consultá las conclusiones y separá lo demostrado, lo
  refutado y lo desconocido.

Para cerrar, comparen los modelos entre grupos: ¿usan los mismos símbolos?, ¿hay
reglas que parecen razonables pero afirman más de lo que dice el protocolo?,
¿cuándo una recomendación no demostrada se confundió con una recomendación
prohibida? Una base puede ser consistente y, aun así, representar mal el
problema.
