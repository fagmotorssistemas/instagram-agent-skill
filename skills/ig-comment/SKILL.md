---
name: ig-comment
description: >-
  Escribe comentarios en posts y reels de otras cuentas que se lean como una
  persona con criterio, no como un bot, desde la cuenta de KsiNuevos o de La
  Vilet. Úsala cuando peguen un post o reel y quieran un comentario, digan
  "comenta esto", "qué pongo aquí", o quieran un lote para la ronda diaria de
  interacción.
---

# ig-comment

Comentar son los veinte minutos de más impacto en Instagram y los más fáciles
de hacer mal. Un comentario arriba en un reel de 40.000 vistas lo ve más gente
que la mayoría de posts propios, y es el único lugar donde un desconocido
toca directo hacia el perfil.

Un comentario genérico es peor que ninguno. Desde la cuenta de una marca,
además, se lee como publicidad.

## Entrada

Pegan el texto del post o reel, o una captura, con el nombre de la cuenta. Si
dan un link que no puedes abrir, pide que lo peguen. No uses el navegador
para recorrer el feed y no publiques nada.

## Los nueve tipos de comentario

Elige según lo que es el post. Nunca el tipo 1 por defecto.

| # | tipo | cuándo | forma |
| --- | --- | --- | --- |
| 1 | **Aporta un dato** | el post afirma algo que puedes respaldar | "Igual en el patio: de cada 10..." |
| 2 | **El caso que falta** | el post tiene razón pero está incompleto | "Esto vale hasta que {condición}." |
| 3 | **Desacuerdo respetuoso** | de verdad crees que está mal | primero el acuerdo, después la diferencia |
| 4 | **Extiende una línea** | una línea es la buena | cítala y construye sobre ella |
| 5 | **La pregunta real** | el post se saltó lo difícil | una pregunta, específica |
| 6 | **El comprobante** | ya hiciste eso que describen | qué pasó, dos oraciones |
| 7 | **La corrección** | hay un error de hecho | ten razón, sé breve, amable y seguro |
| 8 | **El reencuadre** | datos bien, marco mal | "Otra forma de verlo:" |
| 9 | **La de una línea** | el post no necesita nada | menos de 10 palabras, tiene que ser gracioso o verdadero |

## Reglas

- **Una a tres oraciones.** Un párrafo se colapsa detrás de "más".
- **Nunca abras con** "Excelente post", "Me encanta", "Qué verdad", "👏", "Lo
  necesitaba", ni el nombre del creador con signo de exclamación.
- **Nada de comentarios solo con emoji**, ni emoji como primer carácter.
- **No repitas el reel.** Todos acaban de verlo.
- **Una idea.**
- **Di lo específico.** Si el comentario sirve bajo cualquier post del tema,
  es ruido.
- **Nunca vendas.** Ni el carro, ni el proyecto, ni "visita nuestro perfil".
  Es la forma más rápida de que te bloquee justo la cuenta a la que querías
  llegar.
- **La Vilet comenta con su registro:** sobrio, nada de jerga. KsiNuevos
  puede ser más cercano.
- **Temprano importa.** Un comentario en la primera hora de un reel que luego
  viaja, viaja con él.

## Salida

**Dos opciones de tipos distintos**, etiquetadas, y una línea de cuál
publicarías y por qué. Pásalas por `/ig-human` primero.

```
OPCIONES  (en el reel de @cuenta sobre revisar carros usados)

[6 · Comprobante]
En el patio lo primero que miramos son los pernos del capó. Si tienen
marcas de llave, ya sabemos que hubo golpe de frente antes de abrir nada.

[5 · La pregunta real]
¿Y con los híbridos qué recomiendas revisar? La batería es lo que más nos
preguntan y casi nadie lo explica.

Publica la primera. Aporta algo que solo sabe alguien del rubro.
```

## Modo lote

Para una ronda de interacción, pide los 5 a 10 posts pegados en un solo
mensaje, devuelve un comentario por cada uno en un bloque, y lleva una nota en
`~/.claude/instagram/<marca>/log.md` de a quién se comentó esta semana.

## Nunca

No publiques solo, no automatices comentarios, no uses el navegador para
publicar por nadie. La interacción automática viola los Términos de Instagram
y bloquea cuentas. Esta skill escribe el comentario; la persona lo publica.
