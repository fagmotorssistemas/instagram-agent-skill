---
name: ig-reel
description: >-
  Escribe un Reel de Instagram para KsiNuevos o La Vilet a partir de una idea
  cruda: opciones de gancho con 26 fórmulas, el guion hablado, el texto en
  pantalla y una hoja de beats con tiempos, en la voz de la marca y calificado
  antes de grabar. Úsala cuando pidan un Reel, un guion de video corto, un
  gancho, una voz en off, "haz un reel de este carro", "qué digo en este
  video", o cuando alguien va a grabar y no tiene la primera línea.
---

# ig-reel

Convierte una idea cruda en un Reel que alguien termina de ver.

Dos herramientas viven en esta carpeta y las dos funcionan. Úsalas. No
calcules el gancho a ojo ni adivines la duración.

```bash
python3 hookscore.py ganchos.txt               # ordena tus opciones de gancho
python3 hookscore.py --hook "una línea"        # califica una sola
python3 beats.py guion.txt --target 30         # hoja de beats con tiempos, antes de grabar
```

## Antes de escribir

1. **Define la marca.** KsiNuevos o La Vilet. Lee
   `~/.claude/instagram/<marca>/voz.md` (plantillas en `templates/`). Si no
   existe, pide **tres reels propios** de la marca, transcríbelos, deduce la
   voz y escribe el archivo. Un guion en la voz equivocada no sirve, porque
   alguien lo tiene que decir en voz alta.
2. **Lee `hooks.json`** en esta carpeta. 26 fórmulas, cada una con plantilla,
   ejemplo de autos (y de La Vilet cuando aplica), versión en pantalla, para
   qué sirve y cómo se arruina.
3. **Si la idea es flaca, no la rellenes.** Haz una sola pregunta agrupada:
   qué carro / qué unidad, qué dato concreto (año, km, precio, cuota, m²), y
   qué le cambia a quien mira. Un Reel necesita una cosa específica y
   verdadera. Consíguela antes de escribir.
4. Si existe `~/.claude/instagram/<marca>/swipe.md`, léelo. Lo escribe
   `/ig-viral` y es la evidencia propia de qué fórmulas funcionan ahora. Le
   gana a lo que dice este archivo.

## El objetivo, según la marca

- **KsiNuevos:** retener al posible comprador y llevarlo a escribir, no
  hacerse viral. El carro es el centro, sin exagerar, presentado como la
  opción que esa persona busca. Llamado a la acción presente, estructura de
  ganchos, música que acompañe. Para camionetas y pickups, la estructura que
  ya funciona: **gancho → trabajo (motor, platón, capacidad) → confort y
  tecnología → cierre con CTA**. Cierre de marca: "KsiNuevos, tu pana de
  confianza". CTA de marca: "Comenta {MODELO} y te mando toda la info".
- **La Vilet:** elegante y premium, nada animado ni informal. Escenas con
  personas usando los espacios. Vende "un nuevo estilo de vida", "todo lo que
  necesitas sin salir de casa", el proyecto mejor ubicado de Puertas del Sol,
  amenidades estilo club. Nunca clasista.

## La forma

Un Reel se decide en los primeros dos segundos y se sostiene con los cinco
siguientes.

```
0:00 - 0:02   GANCHO      la afirmación. Línea hablada y línea en pantalla,
                          escritas por separado. Movimiento en el primer cuadro:
                          el carro en marcha, un detalle en primer plano, una
                          puerta que se abre. No una cara quieta.
0:02 - 0:07   LO QUE ESTÁ EN JUEGO  por qué le importa a quien mira. Una línea.
0:07 - ...    EL CUERPO   una idea por beat, y el plano cambia en cada beat.
ÚLTIMOS 3s    EL PAGO     entrega lo que prometió el gancho, y el único pedido.
ÚLTIMA LÍNEA  EL LOOP     repite una palabra del gancho (el modelo, el dato)
                          para que la repetición enganche limpia.
```

Duración: 15 a 45 segundos es el rango útil. Para pauta pagada de un carro
puntual, 20 a 30.

## El ciclo

**1. Elige tres ganchos, no uno.** Pasa la idea por `hooks.json`, elige tres
fórmulas que de verdad encajen y escribe la línea hablada y la de pantalla de
cada una. Fórmulas distintas, no tres versiones de la misma.

**2. Califícalos.** Pon las tres líneas habladas en un archivo, una por línea,
y corre `hookscore.py`. Muestra el ranking. Si el primero está bajo 50, todavía
no tienes el gancho y ninguna edición lo arregla.

**3. Escribe el guion** sobre el gancho ganador. Español hablado, como habla
de verdad el vendedor o la voz de la marca. Frases cortas. Nada que haya que
ensayar.

**4. Mide.** Corre `beats.py guion.txt --target {duración}` (usa `--wpm` con el
ritmo real de quien habla; los vendedores rápidos andan por 175-185). Arregla
cada marca: gancho de más de 3 segundos, beats de más de 4, rachas sin nada
concreto, sin loop. Repite hasta que salga limpio.

**5. Humaniza.** Pasa el guion por `/ig-human` antes de mostrarlo. Una línea
que suena escrita se nota apenas alguien la dice.

**6. Entrega el bloque.** El guion en un bloque, el texto en pantalla como
lista aparte con tiempos, y luego:

```
REEL LISTO  ·  KsiNuevos
gancho:      #3 Nadie Te Dice, 86 FUERTE
duración:    27.8s en 9 beats a 175 ppm
pantalla:    6 tarjetas
humanizador: 4 rastros quitados, humano 81 PASA
caption:     corre /ig-caption

Responde "sí" para registrarlo, o dime qué cambio.
```

**7. Nunca publiques.** Esta skill produce un guion. El equipo lo graba y lo
sube. Con el "sí", agrega a `~/.claude/instagram/<marca>/log.md` la fecha, la
fórmula y la primera línea, para que `/ig-audit` tenga historial.

## El texto en pantalla es otro guion

Escríbelo aparte, siempre. Se lee antes de oírse.

- **Seis palabras o menos por tarjeta.** Lo lee alguien que todavía no está
  escuchando.
- **La tarjeta del gancho aparece en el cuadro 1**, no después de un silencio.
- **Los datos del carro en pantalla no se repiten en los subtítulos.** Si el
  año y el km van en letras grandes detrás del vendedor, el subtítulo dice
  otra cosa.
- **Dentro de la zona segura.** En 1080x1920, nada arriba de y=230 ni debajo
  de y=1440, y deja libres los 230 px de la derecha. Ahí la interfaz tapa todo.
- **Subtítulos quemados en el cuerpo.** Casi todos miran sin sonido primero.
- **La Vilet:** tipografía de marca (Italiana para títulos y cifras/m²,
  Archivo Expanded para el resto).

## Reglas que hacen la diferencia

- **Una idea por Reel.** Si el guion tiene dos, son dos Reels. Dilo.
- **Números en vez de adjetivos.** "38.000 km" le gana a "poco recorrido".
  Si no hay número, pídelo en vez de escribir alrededor del hueco.
- **Corta la intro.** Sin saludo, sin "en este video", sin logo al inicio.
- **Cambia el plano en cada beat.** Un plano quieto de 8 segundos es donde la
  gente se va, y `beats.py` lo marca.
- **Un solo pedido al final.**
- **Nunca inventes.** Ni kilometraje, ni precio, ni clientes, ni testimonios,
  ni fechas de entrega. Si falta, deja `{{tu dato}}` y avísalo.
- **No uses datos que no son ciertos para la marca** (por ejemplo, años en el
  mercado que no se pueden respaldar).

## Ejemplo

```
/ig-reel Fortuner 2019 que acaba de llegar, un dueño, mantenimientos en concesionario
```

```
GANCHOS  (calificados)
  86  FUERTE  #3  Nadie Te Dice   "Nadie te dice que una Fortuner usada se revisa por los pernos."
                                  pantalla: REVISA LOS PERNOS
  74  FUERTE  #24 La Revelación   "Esta Fortuner 2019 acaba de llegar y tiene un solo dueño."
                                  pantalla: ACABA DE LLEGAR
  52  OK      #11 Lista           "3 cosas que revisar en una Fortuner usada."
                                  pantalla: 3 COSAS

Grabamos el #3: enseña algo útil, deja al carro como la respuesta, y el
dato es verificable en cámara.
```
