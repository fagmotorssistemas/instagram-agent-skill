---
name: ig-carousel
description: >-
  Arma un carrusel de Instagram para KsiNuevos o La Vilet: la portada que hace
  deslizar, el copy diapositiva por diapositiva, la revisión automática y los
  PNG 1080x1350 listos para subir con la plantilla de la marca. Úsala cuando
  pidan "carrusel", "slides", "post para deslizar", "ficha del carro",
  "amenidades en carrusel", "convierte esto en carrusel", o cuando una idea
  tiene pasos, lista o comparación y se moriría como imagen suelta.
---

# ig-carousel

El carrusel es el formato con más tiempo de permanencia del grid, porque
deslizar es una interacción y hacer scroll no. Además tiene segunda
oportunidad: Instagram puede volver a mostrarlo desde una diapositiva
posterior a quien no interactuó la primera vez, así que la 2 también tiene
que sostenerse sola.

El formato premia una idea partida en pasos. Castiga un caption cortado en
pedazos.

Hay una herramienta en esta carpeta y funciona:

```bash
python3 carrusel.py contenido.json --texto           # el copy numerado, para aprobar
python3 carrusel.py contenido.json --revisar         # revisión sin generar nada
python3 carrusel.py contenido.json --out salida/     # revisa y genera los PNG
python3 carrusel.py contenido.json --out salida/ --pdf
```

Plantillas en `marcas/` (`ksinuevos.json`, `lavilet.json`), fuentes de marca
en `fuentes/`, ejemplos completos en `ejemplos/`.

## Primero: ¿qué marca?

Pregunta o deduce si es **KsiNuevos** (autos usados, Cuenca) o **La Vilet**
(proyecto inmobiliario premium, Puertas del Sol). Lee
`~/.claude/instagram/<marca>/voz.md` si existe. Las dos marcas no se mezclan
nunca en la misma pieza.

| | KsiNuevos | La Vilet |
| --- | --- | --- |
| Plantilla | `ksinuevos` (enérgica, oscura, acento fuerte) | `lavilet` (elegante, marfil y oscuro, líneas finas) |
| Tono | directo, cercano, de pana | sobrio, premium, nunca clasista |
| Datos estrella | año, km, motor, caja, precio, cuota | m², piso, amenidades, ubicación, avance de obra |
| Pedido típico | "Comenta FORTUNER y te mando toda la info" | "Agenda tu visita al departamento modelo" |
| Fotos | fotos reales del carro en el patio | solo renders fieles a la realidad (carpeta RENDERS NUEVOS) y fotos de obra |

## Cuándo usarlo en vez de un Reel

Carrusel cuando la idea tiene **secuencia y se relee**: pasos, una lista para
capturar, una comparación, una ficha técnica, un antes y después, un recorrido
por amenidades. Reel cuando la idea tiene movimiento, una cara, o un resultado
que hay que ver pasar (el motor arrancando, el recorrido por el lobby).

Si la idea es una sola afirmación, no es ninguno de los dos. Pásala a
`/ig-reel` y dilo.

## Los tipos de diapositiva

| tipo | para qué | campos |
| --- | --- | --- |
| `portada` | el gancho. 6 palabras o menos | `titulo`, `subtitulo`, `etiqueta`, `imagen` |
| `gancho` | por qué importa, en una frase (fondo oscuro) | `texto` |
| `idea` | una idea por diapositiva | `numero`, `titulo`, `texto`, `imagen` |
| `ficha` | ficha técnica de un auto o de una unidad | `titulo`, `datos` (pares), `precio`, `imagen` |
| `comparacion` | A contra B, dos columnas | `titulo`, `izquierda`, `derecha` |
| `imagen` | foto o render a sangre con título encima | `imagen`, `titulo`, `texto` |
| `resumen` | todo en una lista: la diapositiva que capturan | `titulo`, `puntos` |
| `cta` | un solo pedido | `titulo`, `texto`, `boton`, `cierre` |

## Estructura

6 a 10 diapositivas. El tope es 20, y 20 es un libro que nadie termina. Con
menos de 5 el deslizar nunca arranca.

```
1         PORTADA   el gancho, 6 palabras o menos, legible en miniatura.
                    Una línea de promesa debajo.
2         GANCHO    por qué le importa a quien mira, en una frase.
                    También es una segunda portada: no puede ser preparación.
3 a N     IDEA / FICHA / COMPARACIÓN / IMAGEN
                    Una idea por diapositiva. Título de 3 a 7 palabras,
                    máximo 25 palabras de texto. Si necesita un párrafo, son dos.
N+1       RESUMEN   todo en una lista. Es la que capturan y reenvían.
ÚLTIMA    CTA       un solo pedido. Comentar una palabra, escribir o agendar.
```

Para un **carro puntual** la forma cambia: portada con foto, ficha, 2 o 3
fotos con un dato cada una (`imagen`), para quién es, cómo se compra
(parte de pago, financiamiento), CTA. Ver `ejemplos/ksinuevos-ficha-auto.json`.

## Reglas del copy

- **La portada es el 80% del resultado.** Seis palabras, grandes. Nada en el
  resto del carrusel salva una portada que nadie desliza. El script la
  califica también como gancho con `hookscore.py`.
- **Números en vez de adjetivos.** "38.000 km, un dueño" le gana a "excelente
  estado". "120 m² y dos balcones" le gana a "amplio y luminoso".
- **Nunca inventes.** Ni kilometraje, ni precio, ni m², ni fecha de entrega,
  ni testimonios. Si falta un dato, pon `{{km}}` o `{{precio}}`: el script
  bloquea el render mientras quede un hueco.
- **La Vilet no suena clasista.** Lujo y elegancia sí; "exclusivo para unos
  pocos" no. Vende la mejor ubicación de Puertas del Sol y "todo lo que
  necesitas sin salir de casa".
- **KsiNuevos empareja, no humilla.** En comparaciones, cada carro es para un
  perfil de comprador; no hay perdedor.
- **El @ en cada diapositiva** (la plantilla lo pone). Las capturas viajan sin ti.
- **Numeración** (3/8) automática. Ver el final sube la tasa de finalización.
- **Texto alternativo** en `"alt"` del JSON. Lo leen los lectores de pantalla
  e Instagram.

## El flujo

1. Arma el JSON del carrusel (parte de un ejemplo de `ejemplos/`).
2. Muestra el copy con `--texto` como lista numerada que se lee en diez
   segundos, y pásalo por `/ig-human`. Deja que la persona edite.
3. Corre `--revisar`. Corrige todo lo que diga FALLA; decide en voz alta cada
   AVISO.
4. **Solo con el copy aprobado**, genera: `--out carpeta/`. Abre las
   imágenes y míralas antes de entregarlas: textos cortados, fotos mal
   recortadas, contraste.
5. Escribe el caption con `/ig-caption`. Para carrusel casi siempre es
   Trabajo B: la portada ya gastó sus seis palabras.

Las fotos van en una carpeta junto al JSON (rutas relativas). Si la foto viene
de Drive o del computador del usuario, cópiala primero ahí.

## Salida

```
CARRUSEL  ·  8 diapositivas  ·  KsiNuevos

 1  PORTADA     Revisa esto antes de firmar
                6 cosas que en el patio miramos primero.
 2  GANCHO      Un carro usado no se compra por la foto...
 3  IDEA        Los pernos del capó
 ...
 7  RESUMEN     La lista completa
 8  CTA         Comenta LISTA

revisión:  LISTO  ·  portada 5 palabras, gancho 74 FUERTE
archivos:  diapo-01.png ... diapo-08.png, alt.txt
caption:   corre /ig-caption (Trabajo B)
```

No se sube nada. La persona lo publica.

## Personalizar las plantillas

Edita `marcas/<marca>.json`: colores, `handle`, `logo` (PNG transparente),
`cierre` y fuentes. La paleta de KsiNuevos es provisional hasta tener la
oficial. La Vilet usa su tipografía de marca: Italiana para títulos y cifras,
Archivo Expanded (125%) para textos y etiquetas.
