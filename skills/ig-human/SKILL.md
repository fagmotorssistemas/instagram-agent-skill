---
name: ig-human
description: >-
  Quita la huella de máquina de cualquier borrador en español (rayas largas,
  palabras de relleno de IA, frases de plantilla inmobiliaria o de venta de
  autos, caracteres invisibles) y lo califica con un panel de cinco chequeos
  antes de publicar. Úsala cuando el texto tenga que sonar humano, cuando
  digan "humaniza esto", "¿suena a IA?", "suena a ChatGPT", "quita las
  rayas", o antes de mostrar cualquier caption, guion, comentario, respuesta
  o DM.
---

# ig-human

Dos herramientas viven en esta carpeta y las dos funcionan. Úsalas.

```bash
python3 humanize.py borrador.txt --report        # lo limpia y muestra qué cambió
python3 detect.py borrador.txt                    # lo califica, cinco chequeos
python3 detect.py antes.txt despues.txt           # demuestra la diferencia
```

Las dos leen `slop.json`: unas 160 palabras y frases de relleno en español con
reemplazos simples, 18 clases de caracteres invisibles, 13 sustituciones
tipográficas y 18 patrones estructurales. Tiene bloques propios del negocio:
frases de plantilla inmobiliaria ("oasis de tranquilidad", "el hogar de tus
sueños", "donde el lujo se encuentra con"), de venta de autos ("el carro de
tus sueños", "la joya de la corona") y de Instagram ("deja de hacer scroll",
"sígueme para más"). **Está hecho para editarse.** Si la marca usa a propósito
una frase que el léxico quita, sácala del archivo. Ojo: "un nuevo estilo de
vida" es un concepto de La Vilet y no está en la lista.

## Por qué importa más en Instagram de lo que parece

Los captions son cortos y los guiones se dicen en voz alta. Una línea que
suena escrita en un caption de 600 caracteres pesa más que en un ensayo, y una
voz en off que nadie diría naturalmente se nota en la primera toma. El
problema no es que un detector marque el post. El problema es una persona que
pasa de largo porque se lee como plantilla, o un vendedor que se traba con su
propio guion.

## Qué se arregla solo

**1. Caracteres invisibles.** Espacios de ancho cero, unidores, guiones
suaves, BOM, caracteres de etiqueta Unicode, espacios duros. Un teclado no los
produce. `humanize.py` los borra todos.

**2. Tipografía.** Raya larga (—) a coma, raya media a guion, comillas curvas
y angulares (« ») a rectas, elipsis (…) a tres puntos. Los signos de apertura
¿ ¡ se respetan: son español correcto.

**3. El léxico de relleno.** crucial, fundamental, potenciar, sumergirnos en,
"en el vertiginoso mundo actual", "cabe destacar que", "una amplia gama de",
"sin lugar a dudas", más los bloques inmobiliario, autos e Instagram. Cada uno
se cambia por una palabra simple o se borra, respetando mayúsculas y sin tocar
los links. Si al borrar queda "¡!" o puntuación suelta, se limpia.

## Qué NO se arregla solo

Los patrones estructurales se **marcan, no se reescriben**, porque cambiar la
forma de una oración necesita criterio:

- "No es solo X, es Y" y "No solo X sino también Y"
- "No se trata de X. Se trata de Y."
- Tríadas de tres adjetivos ("rápido, cómodo y seguro.")
- Preguntas retóricas de una palabra: "¿El resultado?"
- Arranques "Imagina..." y "Descubre..." (muy de plantilla inmobiliaria)
- El preámbulo de video: "en este video te voy a mostrar"
- Listas con emojis de viñeta (✅)
- Tres o más palabras gritadas seguidas
- Muros de hashtags
- Cebos reflejos: "sígueme para más", "etiqueta a alguien", "dale like si"

Esa lista te toca a ti. Reescribe cada línea marcada a mano, conservando el
sentido, y vuelve a correr `detect.py`. Esto es lo que mueve el puntaje de
REVISAR a PASA.

## Los cinco chequeos

`detect.py` califica cinco señales de 0 a 100; más alto es más humano:

| chequeo | qué mide | cómo se ve la máquina |
| --- | --- | --- |
| VARIACIÓN | variación en el largo de las oraciones | todas del mismo largo |
| CONCRECIÓN | números, nombres, datos por cada 100 palabras | sustantivos abstractos, sin cifras |
| RELLENO | términos del léxico por cada 100 palabras | vocabulario de plantilla |
| HUELLA | invisibles, rayas, comillas tipográficas por cada 1.000 caracteres | tipografía perfecta |
| VOZ | marcas orales (¿? ¡! "mira", "ojo", "full", "pana"), pronombres, patrones | nadie habla, revelaciones montadas |

El español casi no tiene contracciones, así que la señal de VOZ usa marcas de
habla oral en vez de contracciones. En La Vilet el registro es más formal:
es normal que VOZ salga algo más baja; compénsalo con datos concretos y
oraciones de largo variado, no con muletillas.

El veredicto pesa el promedio al 60% y el **chequeo más débil** al 40%.
PASA necesita 70 o más, sin ningún chequeo bajo 55.

## Dilo con honestidad

Son cinco heurísticas locales basadas en lo que miran los detectores
públicos. Corren en el computador y no suben nada. **No** son GPTZero,
Originality, Copyleaks, Winston ni Turnitin, y no pueden prometer su
veredicto. No le digas a nadie que su texto es "indetectable".

## Orden de trabajo

1. `humanize.py borrador.txt -o limpio.txt --report`
2. Lee los patrones marcados. Reescribe esas líneas tú.
3. `detect.py borrador.txt limpio.txt` para mostrar el antes y después.
4. Si no PASA, arregla el chequeo más débil y repite. Dos rondas es normal.
   Cinco significa que el borrador se escribió por fórmula: hace falta otro
   borrador, no más pasadas.
5. Muestra el texto limpio y el puntaje. Nunca solo el puntaje.
