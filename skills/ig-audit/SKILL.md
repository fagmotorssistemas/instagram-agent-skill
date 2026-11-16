---
name: ig-audit
description: >-
  Análisis de lo que KsiNuevos o La Vilet ya publicaron: qué reels
  funcionaron de verdad, por qué, y qué dejar de hacer. Úsala cuando peguen
  estadísticas de Instagram o posts anteriores y pregunten "qué está
  funcionando", "por qué este no pegó", "lee las estadísticas", "audita el
  contenido", o quieran saber de qué hacer más.
---

# ig-audit

La única fuente honesta de qué funciona para una cuenta es esa cuenta. Cada
regla de cada guía de Instagram, incluidas las de este paquete, es una
suposición previa. Los últimos 30 posts de la marca son la evidencia.

Esto alimenta directo la automatización de formatos: el objetivo es converger
a los formatos que de verdad retienen y venden.

## Entrada

Pide lo que tengan:

- Estadísticas por post: vistas, alcance, interacciones, tiempo de
  reproducción, guardados, compartidos, seguidores ganados, y el % de alcance
  a no seguidores. Capturas sirven.
- O la gráfica de retención de sus mejores y peores reels. Esa captura vale
  más que todo lo demás junto.
- Para KsiNuevos, si existe: cuántos mensajes o WhatsApps generó cada post o
  anuncio, y si hubo visitas o ventas atribuibles. Es la métrica que más
  importa para la marca.
- O solo los posts y sus vistas, que alcanza para una primera pasada.

Lee también `~/.claude/instagram/<marca>/log.md` si existe: registra qué
fórmula usó cada post.

**Separa orgánico de pagado.** Un reel con pauta no se compara con uno
orgánico por vistas. Compáralos por costo por mensaje o por retención.

## Qué medir de verdad

Las vistas crudas son el número menos útil, porque dependen sobre todo de
cuántos ya siguen la cuenta. Calcula esto y muestra el cálculo:

| métrica | cómo | qué te dice |
| --- | --- | --- |
| **Múltiplo** | vistas / mediana de vistas de la cuenta | si fue un acierto real o un día normal |
| **Alcance a no seguidores** | % del alcance de gente que no sigue | si viajó |
| **Retención a 3s** | quienes siguen a los 3s / quienes empezaron | si el gancho funcionó. Es la nota del gancho. |
| **Tiempo promedio** | directo de estadísticas | si el medio funcionó |
| **Compartidos por alcance** | compartidos / alcance | la señal más fuerte que se puede ganar |
| **Mensajes por alcance** | DMs o WhatsApps / alcance | para KsiNuevos, la métrica de negocio |
| **Seguidores por alcance** | seguidores / alcance | si el perfil convirtió la atención |

Ordena por múltiplo y por compartidos (o mensajes) por alcance, no por
vistas. Un reel con 4.000 vistas y 30 mensajes le ganó al de 60.000 con 2.

## Luego busca el patrón

Con los cinco de arriba y los cinco de abajo lado a lado, busca qué los
separa, y atrévete a concluir algo que no les va a gustar:

- **Retención a 3 segundos.** Si arriba y abajo difieren aquí, es el gancho y
  nada más.
- **Fórmula de gancho.** ¿Qué números de `ig-reel/hooks.json` están arriba?
- **Formato de edición.** Vendedor a cámara, letras 3D con datos del carro,
  editorial de lujo, recorrido, voz en off. Esta es la variable que la
  automatización de formatos está probando: dila explícitamente.
- **Categoría.** SUV, sedán, camioneta (KsiNuevos); tipo de unidad o
  amenidad (La Vilet).
- **Duración.** Menos de 15s, 15 a 30, 30 a 60, más de 60.
- **Quién aparece.** Qué vendedor, o si hay personas en escena (La Vilet).
- **Si se respondió a los comentarios en la primera hora.**
- **Día y hora.** Revísalo **al final**, y solo si lo demás no muestra nada.

Di el hallazgo como afirmación con la evidencia al lado, y qué tan seguro es.
Con 30 posts se ve un patrón. Con 6 no, y decirlo es mejor que inventarlo.

## La distinción que ahorra meses

**Un reel con vistas y sin seguidores ni mensajes no es un reel fallido, es
un problema de perfil o de oferta.** Un reel sin vistas es un problema de
gancho. Sepáralos antes de recomendar nada. Si el alcance a no seguidores es
alto y los mensajes por alcance bajos, deja de reescribir ganchos y ve a
`/ig-profile` (o revisa el pedido y el precio).

## Salida

```
AUDITORÍA  ·  KsiNuevos  ·  31 posts  ·  12 jun - 5 sep  ·  mediana 4.100 vistas

TOP 5 POR MÚLTIPLO
  18.2x  #3  Nadie Te Dice   74.600 vistas  62% no seguidores  ret@3s 71%  38 mensajes
   6.4x  #17 Cara a Cara     26.300 vistas  48% no seguidores  ret@3s 64%  21 mensajes
  ...

ÚLTIMOS 5
   0.3x  #11 Lista            1.200 vistas   9% no seguidores  ret@3s 31%   0 mensajes
  ...

QUÉ DICEN LOS DATOS
1. La retención a 3 segundos es toda la historia. Arriba promedian 66%, abajo 33%.
2. El formato de letras 3D con los datos del carro: 8,1x de media contra 0,9x
   del resto. n=5. La señal más fuerte aquí.
3. Las listas de "5 carros para..." dan vistas y nada más. Sin mensajes.
4. El día de la semana no muestra nada. Dejen de optimizarlo.

DEJAR: listas genéricas.
HACER MÁS: un carro, datos en pantalla, un pedido.
```

Pasa las conclusiones a `/ig-plan` para que la semana siguiente se arme con
la evidencia propia, y a `/ig-viral` para filtrar el swipe a las fórmulas que
funcionan para esta cuenta.
