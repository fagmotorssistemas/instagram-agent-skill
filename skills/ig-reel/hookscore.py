#!/usr/bin/env python3
"""
hookscore.py - califica la primera línea de un Reel en las cinco cosas que
tienen en común los ganchos fuertes, y ordena un lote de ganchos entre sí.

Adaptado al español (Ecuador). Entiende tildes, ñ, "$18.000" y "$18,000",
números dichos en voz alta ("veinte mil", "cuatro por cuatro"), y las palabras
que ponen algo en juego al vender un auto o un departamento: precio, entrada,
cuota, kilometraje, choque, papeles, plusvalía, arriendo.

Qué es:  cinco heurísticas locales, calculadas en tu máquina solo con el texto.
Miden propiedades que comparten los ganchos que retienen: una duración que se
dice en menos de tres segundos, un dato concreto, algo en juego, lo importante
al principio y no al final, y una persona a quien va dirigido.

Qué NO es:  un predictor de vistas. Separa bien un gancho real de uno malo
(saludos, preámbulos, frases sin nada concreto, ganchos de cinco segundos). No
te dice cuál de dos ganchos decentes va a funcionar mejor: eso lo decide la
cara, la edición, el audio y a quién se lo muestra Instagram. Confía más en la
gráfica de retención que en este script.

Cada chequeo devuelve de 0 a 100. Más alto es mejor.

Uso
  python3 hookscore.py ganchos.txt                 # un gancho por línea, ordenados
  python3 hookscore.py --hook "Este Fortuner 2019 tiene 38.000 km y un secreto."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py ganchos.txt --json
"""

import argparse
import json
import re
import statistics
import sys

# Una "palabra" incluye letras con tilde y ñ, cifras, $ y %.
WORD_RE = re.compile(r"[\w$%'’-]+")
THOUSANDS_RE = re.compile(r"(?<=\d)[.,](?=\d{3}\b)")
NUMBER_RE = re.compile(
    r"\$\s?\d[\d.,]*"                                   # plata
    r"|\b\d[\d.,]*\s?"                                  # una cifra, con o
    r"(?:%|k\b|x\d|km\b|kms?\b|m2\b|m²|mts?\b|hp\b|cc\b"  # sin unidad
    r"|mil\b|años?\b|meses?\b|d[ií]as?\b|horas?\b|min\b|minutos?\b|semanas?\b)?",
    re.IGNORECASE)
PROPER_RE = re.compile(r"(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñü]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Los ganchos hablados dicen los números en voz alta. "Veinte mil dólares" es
# tan concreto como "$20.000". "Uno" y "primero" no están a propósito: casi
# siempre son relleno, no una cantidad.
SPOKEN_NUMBERS = {
    "cero", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "once", "doce", "quince", "veinte", "treinta", "cuarenta",
    "cincuenta", "sesenta", "setenta", "ochenta", "noventa", "cien", "ciento",
    "doscientos", "trescientos", "quinientos", "mil", "millón", "millon",
    "millones", "docena", "mitad", "doble", "triple",
}
MONEY_WORDS = {
    "dólares", "dolares", "dólar", "dolar", "centavos", "precio", "entrada",
    "cuota", "cuotas", "financiamiento", "crédito", "credito", "interés",
    "interes", "plata", "ahorro", "ahorras", "ahorraste", "porciento",
    "kilometraje", "kilómetros", "kilometros", "plusvalía", "plusvalia",
    "arriendo", "renta", "avalúo", "avaluo", "matrícula", "matricula",
}

# Palabras que ponen algo en juego. Un gancho sin ninguna es una afirmación;
# un gancho con una es una razón para seguir mirando.
STAKES = {
    "no", "nunca", "jamás", "jamas", "nadie", "ni", "error", "errores",
    "equivocado", "equivocas", "perdí", "perdi", "pierdes", "perder", "pierde",
    "cuesta", "costó", "costo", "caro", "barato", "gratis", "pagas", "pagaste",
    "pagar", "pagué", "cobran", "multa", "estafa", "estafaron", "engaño",
    "mentira", "mienten", "verdad", "secreto", "oculto", "ocultan",
    "escondido", "problema", "problemas", "riesgo", "peligro", "cuidado",
    "ojo", "advertencia", "antes", "hasta", "sin", "solo", "sólo", "todavía",
    "todavia", "aún", "aun", "ya", "pero", "excepto", "salvo", "contra", "vs",
    "versus", "peor", "último", "ultimo", "últimos", "única", "unica", "único",
    "unico", "arrepentí", "arrepentirte", "deberías", "deberias", "deja",
    "dejes", "evita", "evitar", "revisa", "falla", "fallas", "daño", "dañado",
    "chocado", "choque", "robado", "papeles", "prenda", "deuda", "vendido",
    "vendida", "agotado", "quedan", "queda", "realmente", "nadie",
}

# Arranques que gastan el primer segundo diciendo nada.
WEAK_OPENERS = [
    "bueno", "ok", "okey", "hola", "hey", "qué tal", "que tal", "buenas",
    "chicos", "amigos", "bienvenidos", "hoy", "básicamente", "basicamente",
    "sinceramente", "este", "eh", "quería", "queria", "quiero", "uno de",
    "una de", "les traigo", "te traigo", "les cuento", "te cuento",
    "en este", "en el video", "el tema", "hay", "esto es", "este es", "es que",
    "como", "cuando se", "si has", "alguna vez", "sabías", "sabias",
]

# Imperativos que se ganan la primera posición.
IMPERATIVES = {
    "deja", "para", "no", "nunca", "mira", "revisa", "compara", "evita",
    "pregunta", "guarda", "compra", "vende", "cambia", "haz", "usa", "prueba",
    "copia", "pide", "exige", "olvida", "escucha", "aprende", "calcula",
    "verifica", "fíjate", "fijate", "ojo", "antes",
}

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:deja de hacer scroll|no hagas scroll|no deslices|no pases)"),
     "Arranca con \"deja de hacer scroll\". Pedir atención prueba que no te la ganaste."),
    (re.compile(r"(?i)\b(?:en (?:este|el) (?:video|reel)(?: de hoy)?|(?:hoy )?(?:te|les) voy a (?:mostrar|enseñar|contar)|(?:hoy )?(?:te|les) traigo)\b"),
     "Preámbulo de video. Bórralo y arranca en el resultado."),
    (re.compile(r"(?i)^\s*(?:hola|qué tal|que tal|buenas|bienvenidos|hey)\b"),
     "Saludo. Nadie entró al feed para que lo saluden."),
    (HASHTAG_RE,
     "Hashtag en el gancho. Los hashtags van al final del caption, si van."),
    (EMOJI_RE,
     "Emoji en el gancho. El texto en pantalla a tamaño gancho tiene espacio para palabras o para un emoji, no ambos."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "$18.000" es una sola palabra cuando se dice, así que aquí también.
    return WORD_RE.findall(THOUSANDS_RE.sub("", text))


def norm(token):
    return token.lower().strip("'’-")


def check_length(text):
    """Un gancho tiene que aterrizar antes de que se mueva el pulgar."""
    w = words(text)
    n = len(w)
    secs = n / 2.75                      # ~165 palabras por minuto, hablado
    chars = len(text.strip())
    if 5 <= n <= 12:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 12) * 11)
    if chars > 60:                       # dos líneas de texto grande en pantalla
        score -= 12
    return clamp(score), f"{n} palabras, {chars} caracteres, ~{secs:.1f}s hablado (ideal 5-12 palabras)"


def check_specificity(text):
    """Una cosa concreta le gana a tres abstractas."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = [norm(w) for w in words(text)]
    spoken = [w for w in low if w in SPOKEN_NUMBERS or w in MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} dato(s) concreto(s)" + (f": {found}" if found else
                   " - sin número, sin nombre, nada que se pueda verificar"))


def check_stakes(text):
    """Tensión, costo, negación. Algo que el que mira podría perder."""
    w = [norm(x) for x in words(text)]
    hits = [x for x in w if x in STAKES]
    markers = sorted(set(hits))
    if re.search(r"\$\s?\d", text):
        markers.append("un precio")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marcador(es) de tensión" + (f": {', '.join(markers[:4])}" if markers else
                                               " - no hay nada en juego en esta línea")
    return clamp(score), detail


def check_frontload(text):
    """Lo interesante no puede estar en la palabra nueve."""
    w = words(text)
    if not w:
        return 0.0, "vacío"
    low = [norm(x) for x in w]
    opener = " ".join(low[:2])
    penalty = 0
    hit_opener = None
    for weak in WEAK_OPENERS:
        if opener.startswith(weak + " ") or opener == weak or low[0] == weak:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS or token in MONEY_WORDS
                or NUMBER_RE.match(w[i]) or (i and PROPER_RE.match(w[i]))):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "no hay palabra fuerte en ninguna parte de la línea"
    elif payload <= 3:
        base = 100.0
        where = f"lo fuerte está en la palabra {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"lo fuerte está en la palabra {payload + 1}, puede ir antes"
    else:
        base = 40.0
        where = f"lo fuerte está en la palabra {payload + 1}, demasiado tarde"
    detail = where + (f"; arranque débil \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Dirigido a una persona, o flotando en el aire."""
    low = text.lower()
    w = [norm(x) for x in words(text)]
    if re.search(r"\b(tú|tu|tus|te|ti|contigo|usted|ustedes|vos)\b", low):
        return 100.0, "le habla a quien mira"
    if w and w[0] in IMPERATIVES:
        return 90.0, f"arranca en imperativo (\"{w[0]}\")"
    if re.search(r"\b(yo|mi|mis|me|conmigo|nosotros|nos|nuestro|nuestra|nuestros|nuestras)\b", low):
        return 70.0, "primera persona, sin nombrar a quien mira"
    return 35.0, "tercera persona, no hay nadie en la sala"


CHECKS = ["LONGITUD", "CONCRECIÓN", "TENSIÓN", "ARRANQUE", "DESTINATARIO"]


def run(text):
    results = {
        "LONGITUD": check_length(text),
        "CONCRECIÓN": check_specificity(text),
        "TENSIÓN": check_stakes(text),
        "ARRANQUE": check_frontload(text),
        "DESTINATARIO": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # La propiedad más débil pone el techo: basta una mala para que el pulgar
    # siga de largo.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "FUERTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "DÉBIL")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nPUNTAJE DEL GANCHO", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'TOTAL':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  ELIMINATORIO  {f}", file=out)
    if verdict != "FUERTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Propiedad más débil: {weakest}. Arregla esa y vuelve a correrlo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING DE GANCHOS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}", file=out)
        print(f"        más débil: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        eliminatorio: {f}", file=out)
    print("\nGraba el primero. Si el primero está bajo 50, ninguno de estos es el gancho.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Califica un gancho de Reel en cinco propiedades.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con un gancho por línea, o -")
    ap.add_argument("--hook", help="califica un solo gancho escrito en la línea de comandos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("no hay nada que calificar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0])
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
