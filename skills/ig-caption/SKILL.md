---
name: ig-caption
description: >-
  Escribe el caption de Instagram para KsiNuevos o La Vilet: la línea que
  sobrevive al corte de "... más", el cuerpo, el único pedido, los términos de
  búsqueda y los hashtags, y lo revisa antes de publicar. Úsala cuando pidan
  "escribe el caption", "la descripción", "el copy del post", tengan un reel o
  carrusel listo y necesiten el texto, o pregunten por hashtags.
---

# ig-caption

Una herramienta vive en esta carpeta y funciona:

```bash
python3 caption.py caption.txt
python3 caption.py caption.txt --keywords "autos usados Cuenca,Toyota Fortuner"
```

Imprime el caption como lo imprime el feed: los primeros 125 caracteres en una
caja, todo lo demás detrás del toque. Lee esa caja antes que cualquier otra
cosa que escribiste.

## Primero: ¿qué trabajo tiene este caption?

Esta es la decisión que arruina captions cuando se salta.

**Trabajo A: el video ya enganchó.** Un Reel trae su propio gancho en los
primeros dos segundos. El caption no es un segundo gancho, y competir con el
video es la forma de perder los dos. Su trabajo es el pedido, el contexto que
hace que el pedido tenga sentido, y las palabras que la gente busca.

**Trabajo B: el caption es el contenido.** Una foto, un carrusel cuya portada
abre una pregunta. Aquí la línea uno es el gancho y funciona igual que el de
un Reel: concreta, corta, y cortada en una intriga, no a mitad de frase.

Di cuál estás escribiendo.

## La forma

```
Línea 1     125 caracteres visibles. Trabajo A: el pedido, claro.
            Trabajo B: el gancho.
            Nunca un saludo, nunca un hashtag, nunca un emoji de primer carácter.
Cuerpo      párrafos cortos, una línea en blanco entre cada uno. Dos a seis.
            Aquí van los términos de búsqueda y los datos (año, km, m²).
El pedido   uno. Comentar una palabra, escribir al WhatsApp, o agendar visita.
Hashtags    hasta cinco, en su propia línea al final, o ninguno.
```

El límite es 2.200 caracteres y casi nada los necesita.

## Por marca

**KsiNuevos.** Datos primero: modelo, año, kilometraje, dueños, motor, caja.
Luego lo que resuelve (parte de pago, financiamiento). Pedido de marca:
"Comenta {MODELO} y te mando toda la info". Términos de búsqueda: "autos
usados Cuenca", "{marca} {modelo} {año}", "camionetas usadas Cuenca", "SUV
usada Cuenca".

**La Vilet.** Frases sobrias, sin signos de exclamación en cadena, sin emojis
de fuego. Datos en cifras: m², piso, amenidades, ubicación (Puertas del Sol).
Concepto: un nuevo estilo de vida, todo sin salir de casa, el proyecto mejor
ubicado de la zona. Nunca clasista. Pedido: agendar visita al departamento
modelo, o escribir. Términos: "departamentos en Cuenca", "departamentos
Puertas del Sol", "suites en Cuenca", "locales comerciales en arriendo Cuenca"
cuando el post es de locales.

## Hashtags, con honestidad

Instagram limitó los hashtags a **cinco por post desde el 18 de diciembre de
2025** (antes eran 30) y ha dicho que son una etiqueta de tema, no una palanca
de alcance. Entonces: hasta cinco, específicos. `#viral`, `#parati`, `#fyp`,
`#explorar` no describen nada; el revisor los marca.

## Los términos de búsqueda importan más que los hashtags

El buscador de Instagram lee el texto del caption. La frase por la que la
marca quiere aparecer va en el caption como la escribiría una persona, dentro
de una oración normal. "Autos usados en Cuenca" como palabras en la línea 3,
no "#autosusadoscuenca" en un bloque al final.

## Reglas

- **Sin links en el caption.** No se puede hacer clic. Bio, historia con
  sticker de link, o DM.
- **Un solo pedido.** Dos pedidos es lo mismo que ninguno. `caption.py` los
  cuenta (incluye "escríbenos al WhatsApp" y "agenda tu visita").
- **La palabra clave tiene que poder escribirse.** Una palabra, sin espacios,
  sin emoji, y dicha también en el video. `Comenta FORTUNER` funciona.
  `Comenta "la info de la camioneta"` no.
- **Emojis como puntuación, no como decoración.** El revisor marca más de 4
  por cada 100 caracteres. En La Vilet, idealmente cero o uno.
- **Nunca inventes datos.** Precio, km o m² que no tengas: `{{precio}}`.
- **Texto alternativo** para carruseles y fotos: 20 segundos que valen.

## El ciclo

1. Decide Trabajo A o B y dilo.
2. Redáctalo.
3. Pásalo por `/ig-human`. Los captions son cortos: el relleno se nota más
   aquí que en cualquier otro lado.
4. Corre `caption.py` con los términos de búsqueda. Arregla cada FALLA.
   Decide en voz alta cada AVISO.
5. Entrega el bloque listo para copiar, y el resumen:

```
CAPTION LISTO  ·  KsiNuevos
trabajo:    A - el reel trae el gancho
visible:    118 de 125 caracteres antes del corte
pedido:     uno, comentar FORTUNER
hashtags:   3
búsqueda:   "autos usados Cuenca" en la línea 3, "Toyota Fortuner" en la línea 1
revisión:   LISTO
```

No se publica nada. La persona lo pega.
