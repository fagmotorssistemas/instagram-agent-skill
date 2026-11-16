---
name: ig-repurpose
description: >-
  Convierte un material largo (un video del patio, un recorrido por La
  Vilet, una transmisión en vivo, una entrevista, un post de blog, una
  conversación con un cliente) en una semana de reels y carruseles. Úsala
  cuando digan "reutiliza esto", "saca reels de aquí", "tengo un video
  largo", "córtalo", o peguen algo largo y lo quieran en Instagram.
---

# ig-repurpose

Un buen material largo contiene cuatro a seis posts. La mayoría saca uno y
bota el resto.

## Entrada

Una transcripción, un artículo, un guion, un resumen de llamada, un en vivo.
Si dan un link y la sesión tiene herramienta de transcripción, úsala; si no,
pide que peguen. Lee todo antes de extraer nada. Si es un video propio, pide
también el archivo: un Reel con el material real (el vendedor diciendo la
frase, el motor arrancando, la luz real en el piso modelo) le gana a uno
regrabado.

## Extrae, no resumas

Un resumen de un video no es un Reel. Saca lo que se sostiene solo:

| saca | qué es |
| --- | --- |
| **Afirmaciones** | cada frase que iniciaría una discusión |
| **Números** | cada cifra: año, km, precio, cuota, m², piso, plazo |
| **Historias** | cada momento con una persona, una escena y un costo |
| **Mecanismos** | cada "así es como funciona" (cómo se avalúa, cómo se financia) |
| **Errores** | cada admisión de algo que salió mal |
| **Frases** | cada oración ya citable tal cual |

Lista lo encontrado, con conteos, antes de escribir. Si salen menos de
cuatro, el material es flaco y cuatro posts sacados de ahí también lo serán.
Dilo.

## Elige el formato por extracto

- **Afirmación, error, historia** a Reel. Necesitan voz y cara.
- **Mecanismo, lista, comparación, ficha** a carrusel (`/ig-carousel`).
  Necesitan releerse.
- **Una frase citable** a un cuadro de historia, no a un post.

## Arma la semana

Cada extracto es un post y cada post se sostiene completamente solo. Quien lo
ve no vio el original y nunca lo verá. Nunca escribas "como dije en mi último
video".

Asigna a cada uno una fórmula de `ig-reel/hooks.json` y varíalas. Cinco posts
del mismo material con la misma forma de gancho se leen como fábrica de
contenido.

Ordena la semana: la afirmación más fuerte primero, la historia a mitad de
semana, el mecanismo al final.

## Salida

```
FUENTE: recorrido por La Vilet con el arquitecto (18 min, 2.900 palabras)

ENCONTRADO  4 afirmaciones, 7 números, 2 historias, 3 mecanismos, 1 error, 5 frases

SEMANA
MAR  REEL      #3  Nadie Te Dice    la amenidad que más se usa no es la piscina
                                    usa el clip del 06:40, él se ríe al final
JUE  CARRUSEL  Trabajo B            las 4 amenidades, una por diapositiva
VIE  REEL      #21 Media Frase      "...y ahí decidimos subir la piscina al último piso"
DOM  REEL      #26 Superlativo      el único edificio de la zona con spa y gimnasio en el mismo piso

Di "escribe el martes" y lo redacto.
```

Luego redacta a pedido, uno por uno, cada uno por `/ig-reel` (o
`/ig-carousel`) y `/ig-human`. No entregues cuatro guiones terminados de
golpe: van a sonar iguales y no se grabará ninguno.
