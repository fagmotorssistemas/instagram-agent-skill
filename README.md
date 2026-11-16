# instagram-agent-skill · edición KsiNuevos / La Vilet

Trece skills de Claude para manejar Instagram, adaptadas al español de Ecuador
y a dos marcas: **KsiNuevos** (autos usados, Cuenca) y **La Vilet** (proyecto
inmobiliario premium en Puertas del Sol, Cuenca). Incluye un generador de
carruseles con la plantilla de cada marca.

Nada aquí publica en Instagram. Cada skill termina en un bloque listo para
copiar, o en archivos listos para subir, y una persona los publica. Sin API
keys, sin conexiones.

Fork de [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
(licencia MIT, ver `LICENSE`).

## Qué cambió respecto al original

- **Todo en español.** Las 13 skills, los mensajes de los scripts, la rúbrica
  del perfil y las plantillas.
- **Scripts que entienden español.** Tildes y ñ, "$18.000" y "$18,000",
  números dichos en voz alta, palabras de tensión del rubro (precio, entrada,
  cuota, kilometraje, choque, papeles, plusvalía, arriendo), llamados a la
  acción típicos (comenta el modelo, escríbenos al WhatsApp, agenda tu
  visita).
- **26 fórmulas de gancho en español**, con ejemplos de autos y, cuando
  aplica, de La Vilet.
- **Léxico anti-IA en español**: ~160 muletillas de IA, frases de plantilla
  inmobiliaria y automotriz, y cebos de Instagram, más 18 patrones
  estructurales ("No es solo X, es Y", "Imagina...", "Descubre...").
- **Detector adaptado**: el español no tiene contracciones, así que la señal
  de voz mide marcas de habla oral (¿? ¡! "mira", "ojo", "pana").
- **Generador de carruseles** (`skills/ig-carousel/carrusel.py`): JSON →
  revisión → PNG 1080x1350, con plantilla enérgica para KsiNuevos y elegante
  para La Vilet (tipografía de marca Italiana + Archivo Expanded incluida).
- **Datos por marca**: cada marca guarda su voz, swipe, log y plan en
  `~/.claude/instagram/<marca>/`.

## Instalación

```bash
git clone https://github.com/fagmotorssistemas/instagram-agent-skill.git
mkdir -p ~/.claude/skills ~/.claude/instagram/ksinuevos ~/.claude/instagram/lavilet
cp -r instagram-agent-skill/skills/* ~/.claude/skills/
cp instagram-agent-skill/templates/voz-ksinuevos.md ~/.claude/instagram/ksinuevos/voz.md
cp instagram-agent-skill/templates/voz-lavilet.md ~/.claude/instagram/lavilet/voz.md
```

Completa los `{{...}}` de cada `voz.md`. Para los PNG de carruseles:

```bash
pip install playwright && playwright install chromium   # o usa el Chrome que ya tengas
```

Los scripts solo usan la librería estándar de Python 3, salvo el render del
carrusel (Playwright).

## Las skills

| skill | qué hace |
| --- | --- |
| `/ig-reel` | gancho (26 fórmulas, calificado), guion, texto en pantalla y hoja de beats con tiempos |
| `/ig-carousel` | copy diapositiva por diapositiva, revisión y PNG con la plantilla de la marca |
| `/ig-caption` | caption con la línea que sobrevive al "... más", un solo pedido y términos de búsqueda |
| `/ig-human` | quita la huella de IA y califica el texto con cinco chequeos |
| `/ig-viral` | investiga qué está funcionando en el nicho y arma un archivo swipe |
| `/ig-story` | secuencia de historias del día con stickers |
| `/ig-profile` | califica el perfil sobre 100 y reescribe lo que pierde puntos |
| `/ig-plan` | plan semanal por marca: qué, cuándo, en qué formato, con quién interactuar |
| `/ig-comment` | comentarios en otras cuentas que no suenan a bot ni a publicidad |
| `/ig-reply` | ordena y responde los comentarios propios (incluido el "¿precio?") |
| `/ig-dm` | entrega de palabra clave, primer mensaje, propuestas y seguimientos |
| `/ig-repurpose` | convierte un video largo o recorrido en una semana de posts |
| `/ig-audit` | qué funcionó de verdad, por múltiplo y mensajes por alcance |

## Herramientas que se pueden correr solas

```bash
python3 skills/ig-reel/hookscore.py --hook "Esta Fortuner 2019 tiene 38.000 km y un detalle que nadie revisa."
python3 skills/ig-reel/beats.py guion.txt --target 30 --wpm 175
python3 skills/ig-caption/caption.py caption.txt --keywords "autos usados Cuenca"
python3 skills/ig-human/humanize.py borrador.txt --report
python3 skills/ig-human/detect.py borrador.txt
python3 skills/ig-viral/swipe.py capturados.tsv
python3 skills/ig-carousel/carrusel.py skills/ig-carousel/ejemplos/lavilet-amenidades.json --out salida/
```

## Carruseles en dos minutos

1. Copia un ejemplo de `skills/ig-carousel/ejemplos/` y cambia el texto.
2. Pon las fotos (o renders) en una carpeta junto al JSON y referéncialas en
   `"imagen"`.
3. `python3 carrusel.py tu-carrusel.json --texto` para revisar el copy.
4. `python3 carrusel.py tu-carrusel.json --out salida/` genera `diapo-01.png`…
   y `alt.txt`. Si queda un `{{dato}}` sin llenar o falta una foto, no genera.

Colores, @ y logo de cada marca: `skills/ig-carousel/marcas/*.json`. La paleta
de KsiNuevos es provisional hasta tener la oficial.

## Reglas que no cambian

- **No publica, no comenta, no sigue, no manda DMs.** La automatización de
  esas acciones viola los Términos de Instagram y bloquea cuentas.
- **No inventa datos.** Ni precios, ni kilometrajes, ni m², ni testimonios. Si
  falta un dato, deja `{{dato}}` y avisa.
- **Los detectores son heurísticas locales**, no GPTZero ni similares. Nadie
  puede prometer "indetectable".
- **Las respuestas automáticas por palabra clave** se hacen con las
  herramientas de Instagram o socios aprobados, y solo a quien comentó primero.

## Licencias

Código: MIT (ver `LICENSE`, autor original Jake Schincariol). Fuentes Italiana
y Archivo: SIL Open Font License (ver `skills/ig-carousel/fuentes/`).
