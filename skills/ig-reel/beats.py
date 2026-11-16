#!/usr/bin/env python3
"""
beats.py - convierte el guion de un Reel en una hoja de beats con tiempos,
antes de grabarlo.

Estima cuánto toma decir cada línea, las apila en códigos de tiempo y marca las
cuatro cosas que matan un Reel en la edición: un gancho que pasa de los tres
segundos, un beat tan largo que la gente se va, una racha de líneas sin nada
concreto, y una duración total que no cuadra con lo que querías hacer.

Los tiempos son una estimación por cantidad de palabras a un ritmo de palabras
por minuto. Sirven para planear la edición, no reemplazan grabar. Pon tu ritmo
con --wpm cuando te hayas cronometrado leyendo un guion en voz alta: en español
la mayoría cae entre 150 y 190; el valor por defecto es 165. Para vendedores
que hablan rápido frente a cámara, prueba 175-185.

Uso
  python3 beats.py guion.txt
  python3 beats.py guion.txt --target 30
  python3 beats.py guion.txt --wpm 180 --target 45
  pbpaste | python3 beats.py -
  python3 beats.py guion.txt --json
"""

import argparse
import json
import re
import sys

WORD_RE = re.compile(r"[\w$%'’-]+")
THOUSANDS_RE = re.compile(r"(?<=\d)[.,](?=\d{3}\b)")
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CONCRETE_RE = re.compile(r"\$\s?\d|\b\d[\d,.]*|(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñü]{2,}\b",
                         re.MULTILINE)
STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero",
    "si", "de", "del", "a", "al", "en", "con", "por", "para", "que", "qué",
    "este", "esta", "esto", "ese", "esa", "eso", "es", "son", "era", "fue",
    "ser", "está", "están", "tu", "tú", "te", "ti", "yo", "mi", "me", "nos",
    "nosotros", "su", "sus", "se", "lo", "le", "les", "ya", "no", "sí", "muy",
    "más", "tiene", "tienes", "hay", "como", "cómo", "cuando", "todo", "toda",
    "todos", "uno", "solo", "sólo", "así", "pues", "bueno",
}

HOOK_WINDOW = 3.0        # segundos. Después de esto el pulgar ya decidió.
MAX_BEAT = 4.0           # segundos en una idea sin que cambie la pantalla.
ABSTRACT_RUN = 3         # beats seguidos sin nada verificable.


def words(text):
    # "$18.000" es una sola palabra al decirla, así que aquí también.
    return WORD_RE.findall(THOUSANDS_RE.sub("", text))


def pretty(token):
    """Vuelve a poner el separador de miles (punto) para mostrar."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1.", token)


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def split_beats(raw, wps):
    """Una línea es un beat, salvo que sea demasiado larga para serlo."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Párrafo largo: córtalo en los puntos para que los tiempos tengan
        # sentido, y que el reporte diga que se partió.
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=165, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({
            "n": i + 1,
            "start": round(clock, 2),
            "dur": round(dur, 2),
            "words": n,
            "text": text,
            "concrete": len(CONCRETE_RE.findall(text)),
            "label": "",
            "flags": [],
        })
        clock += dur
    total = clock

    # Etiqueta las posiciones estructurales sobre las que se arma un Reel.
    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "GANCHO"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "GANCHO" else "GANCHO/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MITAD"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(
            f"el gancho dura {rows[0]['dur']:.1f}s, pasa la marca de {HOOK_WINDOW:.0f}s")
        notes.append(f"El beat 1 toma {rows[0]['dur']:.1f}s en decirse. Bájalo a "
                     f"{int(HOOK_WINDOW * wps)} palabras o menos, o el gancho llega cuando "
                     "la decisión ya está tomada.")
    if rows[0]["concrete"] == 0:
        notes.append("El beat 1 no tiene ni número ni nombre. Los ganchos sin algo "
                     "verificable (año, km, precio, modelo, m²) son los que se pasan de largo.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f}s en un solo beat")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Beat(s) {', '.join(map(str, long_beats))} pasan de {MAX_BEAT:.0f}s. "
                     "Parte la línea o cambia lo que se ve en pantalla dentro de ella. "
                     "Un plano quieto es donde la gente se va.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Los beats {start}-{r['n']} no tienen nada concreto. "
                             "Mete un número, un nombre o un precio en alguno.")
        else:
            run, start = 0, None

    # ¿La última línea te devuelve a la primera?
    first = {w.lower() for w in words(rows[0]["text"]) if w.lower() not in STOPWORDS}
    last = {w.lower() for w in words(rows[-1]["text"]) if w.lower() not in STOPWORDS}
    loop = sorted(pretty(w) for w in first & last)
    if loop:
        notes.append(f"Hay loop: el último beat repite \"{', '.join(loop[:3])}\" del gancho. "
                     "Las segundas vistas son alcance gratis.")
    else:
        notes.append("No hay loop. El último beat no comparte ninguna palabra con el gancho, "
                     "así que el video termina plano. Repetir una palabra del beat 1 es la "
                     "repetición más barata que vas a conseguir.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"La duración está en el objetivo ({total:.1f}s contra {target:.0f}s).")
        elif delta > 0:
            notes.append(f"{delta:.1f}s por encima del objetivo. Corta unas "
                         f"{int(delta * wps)} palabras.")
        else:
            notes.append(f"{-delta:.1f}s por debajo del objetivo. Agrega {int(-delta * wps)} "
                         "palabras o grábalo corto. Corto casi siempre es lo correcto.")

    return {
        "wpm": wpm, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"HOJA DE BEATS  ·  {a['total_words']} palabras  ·  ~{a['total_seconds']:.1f}s "
            f"a {a['wpm']:.0f} ppm" + (f"  ·  objetivo {a['target']:.0f}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<11}" if r["label"] else " " * 11
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<11}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Convierte un guion de Reel en una hoja de beats.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del guion, o - para stdin")
    ap.add_argument("--wpm", type=float, default=165,
                    help="ritmo al hablar en palabras por minuto (por defecto 165)")
    ap.add_argument("--target", type=float, help="duración objetivo en segundos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, wpm=args.wpm, target=args.target)
    if not a:
        print("guion vacío", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
