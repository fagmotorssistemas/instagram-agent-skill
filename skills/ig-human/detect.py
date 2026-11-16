#!/usr/bin/env python3
"""
detect.py - un panel de cinco chequeos que califica qué tan "escrito por
máquina" se ve un borrador. Adaptado al español.

Qué es:  cinco heurísticas locales basadas en las señales que miden los
detectores públicos de IA: variación en el largo de las oraciones, concreción,
vocabulario de relleno, huella tipográfica y voz. Todo se calcula en tu máquina
solo con el texto. No se sube nada.

Qué NO es:  GPTZero, Originality, Copyleaks, Winston ni Turnitin. No llama a sus
APIs y no puede prometer su veredicto. Detecta lo mismo que ellos miran, por eso
arreglarlo suele mover sus números, pero la única promesa honesta es esta línea.

Diferencia con la versión en inglés: el español casi no tiene contracciones, así
que la señal de VOZ usa marcadores de habla oral (¿...? ¡...!, "mira", "ojo",
"full", "pana", "o sea", "¿cachas?") y pronombres de primera y segunda persona.

Cada chequeo devuelve un puntaje HUMANO de 0 a 100. Más alto es mejor.

Uso
  python3 detect.py borrador.txt
  pbpaste | python3 detect.py -
  python3 detect.py borrador.txt --json
  python3 detect.py antes.txt despues.txt      # compara dos borradores
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?")
PRONOUNS = re.compile(
    r"\b(yo|me|mi|mis|conmigo|nosotros|nosotras|nos|nuestro|nuestra|nuestros|nuestras"
    r"|tú|tu|tus|te|ti|contigo|usted|ustedes|vos)\b", re.IGNORECASE)
# Marcas de que alguien está hablando, no redactando.
ORAL = re.compile(
    r"[¿¡]|\b(?:mira|miren|ojo|full|pana|chévere|chevere|bacán|bacan|o sea|pues|dale|listo"
    r"|ya mismo|de una|fíjate|fijate|cachas|ve|oye|ahí|tipo|bueno)\b", re.IGNORECASE)
NUMBERS = re.compile(r"\b\d[\d,.]*%?|\$\s?\d")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñü]{2,}\b", re.MULTILINE)


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Lleva value a 0-100 donde `human` -> 100 y `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def check_burstiness(text):
    """Los humanos varían mucho el largo de las oraciones. Los modelos escriben parejo."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "muy corto para juzgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variación {cv:.2f} en {len(lens)} oraciones (ideal 0.55+)"


def check_specificity(text):
    """Números, nombres y cosas concretas. El relleno es abstracto."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    per100 = 100 / len(w)
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} datos concretos, {density:.1f} por cada 100 palabras (ideal 4+)"


def lexicon_patterns(lex):
    out = []
    for entry in lex["words"] + lex["phrases"]:
        out.append((entry["find"], re.compile(
            r"(?<!\w)" + re.escape(entry["find"]).replace(r"\ ", r"\s+") + r"(?!\w)",
            re.IGNORECASE)))
    return out


def check_slop(text, lex):
    """Densidad de vocabulario de relleno según el léxico."""
    w = words(text)
    if not w:
        return 50.0, "vacío"
    hits, found = 0, []
    for name, pattern in lexicon_patterns(lex):
        n = len(pattern.findall(text))
        if n:
            hits += n
            found.append(name)
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} términos de relleno, {density:.1f} por cada 100 palabras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Caracteres que un teclado de celular no produce."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”«»")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisibles, {em} raya(s) larga(s), {curly} comilla(s) tipográfica(s), "
              f"{ellip} elipsis, {nbsp} espacio(s) duro(s)")
    return score, detail


def check_voice(text, lex):
    """Habla oral, persona gramatical, y las formas a las que tiende un modelo."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    per100 = 100 / len(w)
    oral = len(ORAL.findall(text)) * per100
    person = len(PRONOUNS.findall(text)) * per100
    tells = 0
    names = []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(oral, human=3.0, machine=0.0) * 0.35
             + scale(person, human=8.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("viñetas-uniformes")
    detail = (f"{oral:.1f} marcas orales, {person:.1f} pronombres personales "
              f"por cada 100 palabras, {tells} patrón(es) de máquina")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["VARIACIÓN", "CONCRECIÓN", "RELLENO", "HUELLA", "VOZ"]


def run(text, lex):
    results = {}
    results["VARIACIÓN"] = check_burstiness(text)
    results["CONCRECIÓN"] = check_specificity(text)
    results["RELLENO"] = check_slop(text, lex)
    results["HUELLA"] = check_fingerprint(text)
    results["VOZ"] = check_voice(text, lex)
    scores = [results[c][0] for c in CHECKS]
    # El chequeo más débil arrastra el veredicto: a un detector le basta una señal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASA" if overall >= 70 and min(scores) >= 55 else (
        "REVISAR" if overall >= 50 else "MARCADO")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PANEL DE DETECCIÓN IA" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HUMANO':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASA":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Señal más débil: {weakest}. Arregla esa primero.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Califica qué tan escrito por máquina se ve un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("compare", nargs="?", help="segundo archivo, para mostrar antes/después")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASA" else 1)


if __name__ == "__main__":
    main()
