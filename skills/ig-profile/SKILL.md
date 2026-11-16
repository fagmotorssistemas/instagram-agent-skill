---
name: ig-profile
description: >-
  Califica un perfil de Instagram (KsiNuevos o La Vilet) sobre 100 con una
  rúbrica de 12 partes y reescribe lo que pierde puntos: campo de nombre, bio,
  link, destacadas, los tres fijados, grid. Úsala cuando pidan "optimiza el
  perfil", "arregla la bio", "califica nuestro Instagram", "por qué no nos
  siguen", o peguen el perfil y pregunten cómo se lee.
---

# ig-profile

Casi todos optimizan lo equivocado aquí. El perfil no es una vitrina que la
gente recorre. Es una **pantalla de decisión**, a la que se llega desde un
reel, y tiene unos tres segundos para responder una pregunta: ¿hay más de eso
aquí, y es para mí?

## Entrada

Pide que peguen o capturen: el campo de nombre, el @, la bio, a dónde lleva el
link, los nombres de las destacadas, qué está fijado, y las primeras nueve
portadas del grid. Una captura de la parte de arriba del perfil más las dos
primeras filas basta para una primera pasada.

No inicies sesión en Instagram por nadie.

## Califícalo

Lee `rubric.json` en esta carpeta. Doce ítems, 100 puntos, cada uno con cómo
se ve el puntaje completo y cómo suele fallar. Califica todo, muestra la
tabla, da el total. Sé honesto: la mayoría saca entre 30 y 49 la primera vez.

```
PUNTAJE DEL PERFIL  38/100

  campo de nombre    2/12   solo el nombre, sin palabras que alguien busque
  bio línea uno      3/12   "Calidad | Confianza | Garantía"
  tres fijados       0/10   nada fijado
  destacadas         2/8    "Promo", "Varios", "2023"
  grid               4/8    seis de nueve portadas son una cara a mitad de frase
  ...
```

## Luego reescribe, en este orden

En orden de puntos perdidos. No todo de golpe: alguien tiene que ir a cambiar
cada campo.

**1. El campo de nombre (30 caracteres).** La línea en negrita, no el @. Es
lo que indexa el buscador. Formato: `{Marca} | {lo que hace, en palabras que
se buscan}`. Da tres opciones. Ej.: `KsiNuevos | Autos usados Cuenca`,
`La Vilet | Departamentos Cuenca`.

**2. Bio, línea uno.** Para quién es y qué le cambia. KsiNuevos: qué tipo de
carros, que reciben tu carro, financiamiento. La Vilet: Puertas del Sol, el
concepto (todo sin salir de casa), sin sonar clasista. El resto de los 150
caracteres: una prueba o una oferta concreta.

**3. Los tres fijados.** Tres trabajos distintos: la mejor prueba (entrega
real, cliente real con permiso, avance de obra real), la explicación más
clara de cómo se compra, y la mejor presentación del equipo o del proyecto.
Es el arreglo de más impacto y toma cuatro toques.

**4. Destacadas.** Cuatro a seis, con nombre de pregunta de comprador.
KsiNuevos: Stock, Financiamiento, Entregas, Cómo comprar, Ubicación. La
Vilet: Amenidades, Avance, Plantas, Ubicación, Contacto. Borra el resto.

**5. El link.** Un destino que cumple lo que promete la bio: WhatsApp con
mensaje prellenado, catálogo, página del proyecto. Dos ya es un menú.

**6. Portadas del grid.** Las primeras nueve en miniatura. Portadas de reel
elegidas, no el primer cuadro. Cuatro palabras de texto (modelo y año; nombre
del espacio) hacen que el grid se lea de un vistazo. Para La Vilet, con la
tipografía de marca.

## Salida

La tabla de puntaje, luego las reescrituras como bloques listos para copiar
en orden de prioridad, cada una pasada por `/ig-human`. Vuelve a calificar al
final y muestra la diferencia con honestidad. Si llega a 84 y no a 98, di 84,
y di qué falta (casi siempre: un grid, el hábito de historias, y un post
fijado que todavía no existe). Nada de eso es reescribir.

Esta skill no guarda nada en Instagram. La persona edita cada campo.
