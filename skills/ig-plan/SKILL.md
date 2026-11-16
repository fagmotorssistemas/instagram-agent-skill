---
name: ig-plan
description: >-
  Arma la semana de Instagram para KsiNuevos o La Vilet: qué publicar, en qué
  formato, cuándo, y con quién interactuar. Úsala cuando pidan "planifica la
  semana", "qué publicamos", "calendario de contenido", "no tengo de qué
  publicar", o quieran un horario de publicación y una lista de interacción.
---

# ig-plan

La sala de control. Todo lo demás en este paquete ejecuta; esto decide qué se
ejecuta. Córrelo una vez por semana, el mismo día, **una vez por marca**.

## Entrada

Lee, si existen, `~/.claude/instagram/<marca>/voz.md`, `swipe.md` y `log.md`.
El swipe es la evidencia propia de `/ig-viral` sobre qué fórmulas funcionan
ahora, y manda sobre cualquier cosa de este archivo. El log evita repetir un
tema de las últimas dos semanas.

Si no existen, pide cuatro cosas y anótalas:

1. Qué se vende y a quién. (KsiNuevos: inventario de esta semana, qué llegó,
   qué se vendió, por categoría SUV / sedán / camioneta. La Vilet: qué tipo
   de unidad se empuja: locales en arriendo, suites, departamentos,
   penthouses; para uso personal o inversión.)
2. Los tres o cuatro temas por los que quieren ser conocidos.
3. Qué pasó de verdad esta semana: un carro que llegó, una entrega, una
   pregunta de cliente, un avance de obra, una visita al piso modelo. De aquí
   salen los posts.
4. Diez cuentas a las que vale la pena ser visibles.

## Qué publicar

Cuatro o cinco posts a la semana, al menos tres Reels. Los Reels son el único
formato que llega de forma fiable a quien no sigue la cuenta. Los carruseles
profundizan con los que ya siguen. Las historias son diarias y van aparte.

Mezcla en la semana, nunca dos del mismo tipo seguidos:

| tipo | cuánto | trabajo |
| --- | --- | --- |
| **Prueba** | 1 por semana | algo que pasó, con un dato. Entrega, avance de obra. Reel. |
| **Enseñar** | 1 a 2 por semana | algo que quien mira puede hacer hoy. Reel o carrusel. |
| **Opinión** | 1 por semana | una postura que algunos no compartirían. Reel. |
| **Historia** | 1 cada dos semanas | una escena con un costo. Reel. |
| **Oferta** | 1 a 2 por semana | qué se vende, dicho claro, sin disculparse. Carrusel ficha o Reel. |

Para KsiNuevos, la oferta pesa más (objetivo: ventas directas con pauta), así
que puede ser 2 por semana, siempre con el carro como centro y un solo
pedido.

Para cada espacio da: el tema, el ángulo específico de lo que pasó esta
semana, el formato y el número de fórmula de `ig-reel/hooks.json`. No un
tema: un ángulo. "Autos" no es un plan. "La Tucson que llegó con todos los
mantenimientos y por qué eso vale $1.500 más" es un Reel.

## Cuándo publicar

Cuando la audiencia está despierta y no trabajando. En Cuenca, para público
general, temprano en la noche (19:00 a 21:00); para un público de inversión o
profesionales, temprano en la mañana o al mediodía.

Pero dilo claro: **la hora importa mucho menos que los primeros dos
segundos.** Si la marca está optimizando horarios antes de que sus ganchos
funcionen, está puliendo lo equivocado.

## La ronda de interacción, que no es opcional

20 minutos al día, antes de publicar. Lista de 10:

- **5 de alcance** - cuentas con la audiencia que la marca quiere (medios
  locales de Cuenca, creadores de autos, de arquitectura). Comenta temprano.
- **3 pares** - mismo tamaño, mismo rubro o rubro vecino.
- **2 compradores** - gente o negocios que podrían comprar o arrendar.
  Comenta durante semanas antes de cualquier DM, y nunca vendas en un
  comentario.

Pasa la lista a `/ig-comment`.

## Salida

```
SEMANA DEL 17 DE NOV  ·  KsiNuevos

LUN  solo interacción  (20 min, lista abajo)
MAR  19:30  REEL      OFERTA     #24 La Revelación   - la Fortuner que acaba de llegar
MIÉ  historias + interacción
JUE  19:00  CARRUSEL  ENSEÑAR    Trabajo B           - 6 cosas que revisar antes de firmar
VIE  19:30  REEL      OPINIÓN    #2  Orden Negativa  - no compres sin pedir el historial
SÁB  11:00  REEL      OFERTA     #17 Cara a Cara     - Hilux vs D-Max: para quién es cada una
DOM  -

HISTORIAS  todos los días, 3 a 5 cuadros, caja de preguntas el jueves.

INTERACCIÓN  (5 alcance / 3 pares / 2 compradores)
  ...

Di "escribe el martes" y lo redacto.
```

Guarda el plan en `~/.claude/instagram/<marca>/plan.md`. No se programa ni se
publica nada. Es un plan y el equipo lo ejecuta.
