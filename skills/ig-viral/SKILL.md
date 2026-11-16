---
name: ig-viral
description: >-
  Busca los reels que de verdad están funcionando ahora en el nicho de
  KsiNuevos (autos usados) o de La Vilet (inmobiliaria premium), los ordena
  por cuánto superaron a su propia cuenta, nombra la fórmula de gancho de cada
  uno y arma un archivo swipe para grabar. Úsala cuando pidan "busca videos
  virales", "qué está funcionando", "qué publica la competencia", "analiza
  esta cuenta", "arma un swipe file", "por qué este reel pegó", o pregunten
  qué hacer después sin tener evidencia.
---

# ig-viral

La skill de investigación. Todo lo demás en este paquete escribe; esta va y
mira. Córrela una vez al mes, no todos los días. Las fórmulas duran una
temporada.

Una herramienta vive en esta carpeta y funciona:

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/<marca>/swipe.md
```

Encaja directo con la automatización de formatos de reels: esto es lo que
dice cuál formato probar después, con evidencia y no con intuición.

## La idea que hace que valga la pena

**Las vistas crudas no son evidencia.** Una cuenta de dos millones de
seguidores con 400.000 vistas tuvo un martes tranquilo. Una de cuatro mil con
400.000 vistas encontró algo, y eso se puede copiar.

Todo aquí se ordena por el **múltiplo**: vistas divididas para la mediana
reciente de esa misma cuenta. Más de 3x es una señal. Menos de 1,5x es un día
normal de esa cuenta y no enseña nada, por grande que se vea el número.

Junta cuentas **de hasta unas 10 veces el tamaño de la marca**. Una fórmula
que funciona con 2M de seguidores muchas veces funciona porque tiene 2M.

## Paso 1: elegir las cuentas

Pide 6 a 12 cuentas, o propónlas y pide aprobación:

- **4 directas** - mismo nicho, un poco más adelante. KsiNuevos: patios y
  concesionarios de usados de Ecuador y Latinoamérica. La Vilet: proyectos
  inmobiliarios premium de Ecuador, Colombia, México.
- **4 adyacentes** - otro nicho, misma audiencia. KsiNuevos: creadores de
  reseñas de autos, mecánicos que explican. La Vilet: arquitectura, diseño
  interior, hoteles boutique. De aquí salen formatos antes de que los tenga la
  competencia.
- **2 a 4 grandes** - cuentas mucho más grandes, solo para formato, nunca
  para ritmo ni tono.

Pide también que abran su colección de **Guardados**. Es el corpus más rápido
y relevante que existe, y ya está filtrado por su gusto.

## Paso 2: ir a mirar

Usa la herramienta de navegación que tenga la sesión: el navegador de la app,
la extensión en el Chrome del usuario, o uso del computador. No hay API para
esto y no hace falta: el volumen es lo bastante chico para leerlo.

**Reglas que no se negocian:**

- **Nunca inicies sesión en Instagram por el usuario y nunca pidas una
  contraseña.** Si una página pide login, quien ya está logueado es el
  usuario. Maneja su navegador con él presente, o pídele que pegue.
- **Esto es leer, no hacer scraping.** Diez cuentas, una docena de reels
  cada una, a velocidad humana. La recolección automática a volumen viola los
  Términos de Instagram y bloquea cuentas. No construyas un crawler, no uses
  un servicio de scraping, no lo dejes corriendo de fondo.
- **Copia la fórmula, nunca el video.** La forma del gancho, la estructura,
  la duración, el ritmo de cortes. No el guion, no la voz, no la edición.
  Atribuye cada fila del swipe a la cuenta de donde salió.

**Qué capturar por reel**, con las palabras del creador:

| campo | notas |
| --- | --- |
| cuenta | el @ |
| seguidores | del perfil |
| mediana | mira los últimos 12 reels y toma las vistas del del medio |
| vistas | de este reel |
| gancho | la primera línea, hablada o en pantalla, tal cual, con errores incluidos |
| pantalla | la primera tarjeta de texto, si es distinta |
| duración | segundos |
| cta | qué pidieron al final |
| formato | vendedor a cámara, voz en off, letras 3D, editorial, recorrido, etc. |

La mediana es la importante. Sin ella vuelves a ordenar por seguidores, que es
justo lo que esta skill existe para evitar.

**Cuando Instagram no muestra suficiente:** la misma gramática de ganchos
corre en YouTube Shorts, donde las vistas y transcripciones son públicas y no
hace falta login:

```bash
# vistas de los shorts de un canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@CANAL/shorts" > canal.json

# la primera línea hablada de un short, desde sus subtítulos automáticos
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "es.*" \
  --sub-format json3 -o gancho "https://www.youtube.com/watch?v=VIDEO_ID"
```

Toma cada palabra con marca de tiempo menor a 3,0 segundos. Ese es el gancho,
como se dijo.

## Paso 3: ordenar

Llena un archivo separado por tabulaciones (encabezados en español o en
inglés) y corre el script:

```
cuenta	seguidores	mediana	vistas	gancho
@patio_x	48000	11000	412000	nadie te dice que el precio es lo de menos
```

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/<marca>/swipe.md
```

Calcula el múltiplo, nombra la fórmula con las mismas 26 de `/ig-reel`,
califica cada gancho con `hookscore.py`, e imprime qué separa al tercio de
arriba del de abajo.

## Paso 4: decir qué significa, con cuidado

Reporta tres cosas y nada más:

1. **Qué fórmulas sobresalen** en el tercio de arriba, con conteos.
2. **Qué tiene en común el tercio de arriba** que no tiene el de abajo: largo
   del gancho, si el pago es visual, si el primer cuadro se mueve, dónde está
   el pedido, qué formato de edición.
3. **Las filas sin clasificar.** Cada gancho que el clasificador no pudo
   nombrar es ruido o una fórmula que todavía no está en `hooks.json`. Léelos
   a mano. Es la columna más valiosa.

Luego di el tamaño de la muestra y la confianza en palabras simples. Cuarenta
reels en seis cuentas sostienen una afirmación. Doce no.

## Paso 5: convertirlo en algo para grabar

Para las tres fórmulas de arriba, escribe **la versión de la marca**: su
carro, su dato, su unidad, en la forma que está funcionando. Pasa cada una a
`/ig-reel` con la fórmula ya elegida. Nunca entregues "haz un reel como este".
Entrega una línea de gancho que se pueda decir mañana.

## Salida

```
SWIPE  ·  38 reels  ·  7 cuentas  ·  línea base: mediana de la cuenta

SOBRE 3x
  38.4x  gancho 86  #3  Nadie Te Dice   @cuenta_a   412.000  (mediana 10.700)
  11.2x  gancho 79  #17 Cara a Cara     @cuenta_c   180.000  (mediana 16.100)
  ...

QUÉ SOBRESALE
  #3 Nadie Te Dice    x5 arriba, 0 abajo
  #17 Cara a Cara     x4
  largo del gancho    8 palabras arriba, 19 abajo

SIN CLASIFICAR (6)
  Dos tienen la misma forma y no está en hooks.json: el vendedor lee en voz
  alta el comentario de un cliente. Vale la pena agregarla.

TU VERSIÓN
  #3  "Nadie te dice que una SUV usada se revisa primero por los pernos."
```

Guarda el swipe en `~/.claude/instagram/<marca>/swipe.md`. `/ig-reel` y
`/ig-plan` lo leen.

Esta skill no publica, no sigue, no da like ni manda mensajes. Lee.
