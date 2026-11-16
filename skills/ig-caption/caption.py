#!/usr/bin/env python3
"""
caption.py - revisa un caption de Instagram y muestra exactamente lo que se ve
en el feed antes del "... más".

Instagram le da al caption unos 125 caracteres en el feed y esconde el resto
detrás de un toque. Casi todos los captions que fallan, fallan ahí: el gancho
está en la tercera oración, la primera línea es un saludo, o todo arranca con un
hashtag. Este script imprime la ventana visible en una caja para que la leas
como la lee un desconocido haciendo scroll, y luego revisa lo que vale la pena
revisar.

El corte de 125 caracteres es aproximado. El número real cambia con el
dispositivo, el tamaño de letra y dónde caen tus saltos de línea; por eso
conviene dejar margen. Cámbialo con --truncate si quieres probar uno más corto.

Uso
  python3 caption.py caption.txt
  python3 caption.py caption.txt --keywords "autos usados Cuenca,Toyota Fortuner"
  pbpaste | python3 caption.py -
  python3 caption.py caption.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200             # Límite duro de Instagram para el caption.
TRUNCATE = 125           # Más o menos donde el feed corta a "... más".
HASHTAG_LIMIT = 5        # Tope de Instagram por post o reel desde el 18 de
                         # diciembre de 2025 (antes eran 30).

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|ec|com\.ec|co|io|net|org|ai|app)/\S*",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CONCRETE_RE = re.compile(r"\$\s?\d|\b\d[\d,.]*|(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñü]{2,}\b",
                         re.MULTILINE)

# Llamados a la acción. Un caption con dos de estos es un caption sin ninguno.
ASKS = [
    (re.compile(r"(?i)\bcom[eé]nta(?:nos|me)?\b(?: la palabra)?\s*[\"“«]?[A-ZÁÉÍÓÚÑ0-9]{2,}"),
     "comentar una palabra clave"),
    (re.compile(r"(?i)\b(?:escr[ií]be(?:me|nos)|m[aá]nd(?:a|e)(?:me|nos) un (?:dm|mensaje)"
                r"|env[ií](?:a|e)(?:me|nos) un (?:dm|mensaje)|(?:al|por) (?:dm|interno|privado))\b"),
     "mandar DM"),
    (re.compile(r"(?i)\bwh?ats?app\b|\bwasap\b"), "escribir al WhatsApp"),
    (re.compile(r"(?i)\bgu[aá]rd(?:a|alo|ala|en|enlo)\b"), "guardar"),
    (re.compile(r"(?i)\bcomp[aá]rt(?:e|elo|ela|an)\b|\b(?:env|m[aá]nd)[aá]selo\b"), "compartir"),
    (re.compile(r"(?i)\bs[ií]g(?:ue|ueme|uenos)\b"), "seguir"),
    (re.compile(r"(?i)\b(?:link|enlace) (?:en|de) (?:la|mi|nuestra) bio\b"), "link en la bio"),
    (re.compile(r"(?i)\bdesliza\b"), "deslizar"),
    (re.compile(r"(?i)\b(?:vis[ií]ta(?:nos)?|agend(?:a|e)\s+(?:tu|su)\s+(?:cita|visita|prueba de manejo|recorrido)"
                r"|ven (?:al|a nuestro) (?:patio|showroom|proyecto)|test drive|prueba de manejo)\b"),
     "agendar visita"),
    (re.compile(r"(?i)\bcu[eé]nta(?:me|nos)\b|\bcu[aá]l (?:prefieres|elegir[ií]as|te llevas|te gusta)\b"
                r"|\bqu[eé] (?:har[ií]as|opinas)\b"),
     "responder una pregunta"),
]

FILLER_TAGS = {"#viral", "#fyp", "#parati", "#paratii", "#foryou", "#explore", "#explorar",
               "#explorepage", "#tendencia", "#trending", "#instagood", "#love", "#follow",
               "#seguidores", "#likes", "#megusta", "#reels", "#reelsinstagram", "#viralreels",
               "#instadaily", "#ecuador"}


def visible_window(text, cut):
    """Lo que muestra el feed. Instagram corta a mitad de palabra; esto también."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  LO QUE MUESTRA EL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... más" if truncated else "(el caption entra completo)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LARGO", "FALLA" if chars > LIMIT else "OK",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} sobre el límite"
                                           if chars > LIMIT else ""))

    if not first_line:
        add("PRIMERA LÍNEA", "FALLA", "el caption arranca con una línea en blanco")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("PRIMERA LÍNEA", "FALLA",
            "arranca con un hashtag o una mención, en la única posición que vale una frase")
    elif re.match(r"(?i)^\s*(?:hola|buenas|qué tal|que tal|bienvenid)", first_line):
        add("PRIMERA LÍNEA", "FALLA", "arranca con un saludo. Nadie lee el caption para que lo saluden")
    elif len(first_line) > cut:
        add("PRIMERA LÍNEA", "AVISO",
            f"{len(first_line)} caracteres, así que se corta en {cut} a mitad de idea. "
            "Bien si el corte deja intriga, mal si corta una subordinada")
    else:
        add("PRIMERA LÍNEA", "OK", f"{len(first_line)} caracteres, entra completa")

    add("GANCHO CONCRETO", "OK" if CONCRETE_RE.search(window) else "AVISO",
        f"{len(CONCRETE_RE.findall(window))} número(s) o nombre(s) en la ventana visible"
        + ("" if CONCRETE_RE.search(window) else " - nada verificable antes del toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FALLA", f"{len(tags)} hashtags, sobre el tope de Instagram de "
                                 f"{HASHTAG_LIMIT}. Los que pasan del quinto no cuentan")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAGS", "AVISO", f"{len(tags)} hashtags, en el tope, y {len(filler)} "
                                 "son genéricos. Usa los cinco en temas")
    elif filler:
        add("HASHTAGS", "AVISO", f"{len(tags)} hashtags, {len(filler)} genéricos "
                                 f"({', '.join(filler[:3])}). Esos no describen nada")
    else:
        add("HASHTAGS", "OK", f"{len(tags)} hashtag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("UBICACIÓN TAGS", "OK", "no hay hashtags que ubicar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("UBICACIÓN TAGS", "AVISO", "hay un hashtag dentro de la ventana visible, "
                                       "gastando espacio del feed en una etiqueta")
    else:
        add("UBICACIÓN TAGS", "OK", "los hashtags están debajo del corte")

    add("LINKS", "AVISO" if links else "OK",
        f"{len(links)} link(s) en el caption, y los captions no son clicables. "
        f"Pásalo a la bio, a una historia con sticker o al DM" if links
        else "no hay links muertos en el texto")

    if len(asks) == 1:
        add("UN SOLO PEDIDO", "OK", f"un llamado a la acción: {asks[0]}")
    elif not asks:
        add("UN SOLO PEDIDO", "AVISO", "no hay llamado a la acción. Decide para qué es este post")
    else:
        add("UN SOLO PEDIDO", "AVISO", f"{len(asks)} pedidos ({', '.join(asks)}). "
                                       "Dos pedidos es lo mismo que ninguno")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJIS", "AVISO" if density > 4 else "OK",
        f"{len(emoji)} emoji, {density:.1f} por cada 100 caracteres"
        + (" - se lee como decoración" if density > 4 else ""))

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "OK" if not missing else ("AVISO" if found else "FALLA")
        add("BÚSQUEDA", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} en la ventana visible" if found else "")
            + (f". Faltan: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FALLA")
    warns = sum(1 for c in checks if c["status"] == "AVISO")
    verdict = "CORREGIR" if fails else ("REVISAR" if warns else "LISTO")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"REVISIÓN DE CAPTION  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} pedido(s)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<5} {c['check']:<16} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDICTO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa un caption de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del caption, o - para stdin")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"caracteres visibles antes de '... más' (por defecto {TRUNCATE})")
    ap.add_argument("--keywords", default="",
                    help="términos separados por coma por los que quieres que te encuentren")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "LISTO" else 1)


if __name__ == "__main__":
    main()
