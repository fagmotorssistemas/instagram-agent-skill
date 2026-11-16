---
name: ig-reply
description: >-
  Maneja los comentarios en los reels y posts propios de KsiNuevos o La
  Vilet: redacta respuestas para los que valen la pena, ordenados por
  prioridad (palabra clave, posibles clientes, preguntas de precio). Úsala
  cuando peguen sus comentarios, digan "responde estos", "contesta los
  comentarios", "alguien puso X en el reel", o tengan un crítico, un hater o
  un posible cliente en los comentarios.
---

# ig-reply

Los comentarios bajo tus propios posts son donde se decide el alcance. Cada
respuesta es otra interacción, las respuestas en la primera hora hacen casi
todo el trabajo, y una respuesta también puede ser un Reel, que es la jugada
más desaprovechada de la plataforma.

Pero no todos los comentarios valen lo mismo, así que esta skill ordena antes
de escribir.

## Entrada

Pegan los comentarios, idealmente con el @. Capturas sirven. No recorras el
hilo con el navegador.

## Primero, clasificar

Pon cada comentario en uno de siete grupos y di los conteos:

| grupo | qué es | qué recibe |
| --- | --- | --- |
| **PALABRA CLAVE** | comentaron la palabra que pediste (FORTUNER, LISTA) | lo prometido, a mano o con la herramienta aprobada |
| **PRECIO** | "¿precio?", "info", "cuánto" | respuesta pública breve + invitación al DM o WhatsApp |
| **CLIENTE** | alguien describe lo que la marca resuelve | una respuesta real en público, luego una puerta |
| **SUSTANCIA** | aporta un dato, discrepa, extiende | la respuesta más larga del hilo |
| **PREGUNTA** | una duda que tiene mucha gente | se vuelve Reel, no solo respuesta |
| **APOYO** | "🔥", "qué bonito", una etiqueta | un like y 3 a 8 palabras como mucho |
| **RUIDO** | spam, mala fe, provocación | nada, o una línea y fuera |

Escribe en ese orden y para cuando se acabe el valor.

## El "¿precio?"

Es el comentario más común de KsiNuevos y el que más se pierde. Reglas:

- **Respóndelo siempre, rápido y en público.** Quien pregunta precio y no
  recibe respuesta se va a otro patio.
- **Si el precio es público, dilo.** "$00.000, y recibimos tu carro como
  parte de pago." Esconderlo por sistema genera desconfianza.
- **Si la marca decidió darlo por interno, dilo con una razón y una puerta,
  no con "te escribo al DM" a secas.** "Depende de si entra tu carro como
  parte de pago; te escribo con los números." Y escríbele de verdad.
- **Nunca inventes un precio.** Si no lo tienes: `{{precio}}`.

En La Vilet, la pregunta de precio se responde con el rango si es público, o
con una invitación al departamento modelo; siempre sobrio.

## La jugada que casi nadie hace

Si una pregunta en los comentarios la tienen treinta personas más,
**respóndela con un Reel**. Instagram pega el comentario como sticker en el
video nuevo y avisa a quien preguntó. Marca cada PREGUNTA que califica y pásala
a `/ig-reel` como fórmula #16.

## Cómo responder

- **Responde la pregunta de verdad.** Si preguntan cómo, di cómo.
- **Usa su nombre una vez**, al inicio, sin signo de exclamación.
- **Iguala el largo.** Un comentario de cuatro palabras no recibe cuatro líneas.
- **A un crítico:** primero concede lo que es cierto, con sus palabras, y
  luego sostén tu posición. Nunca borres, nunca te pongas a la defensiva, nunca
  respondas dos veces en el mismo hilo.
- **A un hater:** nada. Responder es darle alcance. Oculta el comentario si es
  ofensivo.
- **A un posible cliente:** responde completo en público. La puerta es una
  frase al final y es una oferta de ayuda, no un discurso de venta.

## Comentarios de palabra clave

Si el post pidió una palabra clave, esos comentarios son todo el punto del
post. Cada uno es alguien que levantó la mano. Responde a cada uno y manda lo
prometido. Si la marca tiene automatización con las herramientas de Instagram
o un socio aprobado, dilo y déjala correr. Nunca mandes DMs masivos a quien no
comentó.

## Salida

Un bloque, agrupado, cada respuesta lista para copiar y ya humanizada:

```
RESPUESTAS  ·  84 comentarios  ·  31 PALABRA CLAVE, 18 PRECIO, 2 CLIENTE, 1 SUSTANCIA, 2 PREGUNTA, 28 APOYO, 2 RUIDO

PALABRA CLAVE  (31)  manda la info. Una línea cada uno, mismo tono, sin copiar y pegar idéntico.

PRECIO  (18)
> $00.000. Si tienes carro para dar como parte de pago, te hacemos el avalúo
> ese mismo día. Te escribo con los números.

CLIENTE
@usuario - "busco algo para la familia que aguante viajes a la Costa"
> Esta es justo para eso: 7 asientos y motor 2.7. Si quieres te mando un
> video de la tercera fila abierta para que veas el espacio real.

PREGUNTA -> REEL
@usuario - "¿aceptan carros con prenda?"
  21 likes en este comentario. Eso es un Reel, no una respuesta. Fórmula #16.

RUIDO  (2)  omitidos. Responder les da alcance.
```

Nada se publica hasta que la persona diga que sí. Ella pega las respuestas.
