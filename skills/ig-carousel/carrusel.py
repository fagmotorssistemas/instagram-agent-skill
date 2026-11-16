#!/usr/bin/env python3
"""
carrusel.py - revisa y renderiza un carrusel de Instagram a partir de un JSON.

Toma el contenido diapositiva por diapositiva, lo revisa contra las reglas que
hacen que la gente deslice (portada corta, una idea por diapositiva, un solo
pedido al final), y genera los archivos 1080x1350 (4:5) listos para subir, con
la plantilla de la marca: KsiNuevos o La Vilet (ver carpeta marcas/).

No publica nada. Genera archivos; la persona los revisa y los sube.

Uso
  python3 carrusel.py contenido.json --revisar        # solo revisa, no renderiza
  python3 carrusel.py contenido.json --texto          # imprime el copy numerado
  python3 carrusel.py contenido.json --out salida/    # revisa y genera PNG
  python3 carrusel.py contenido.json --out salida/ --pdf
  python3 carrusel.py contenido.json --out salida/ --solo-html

Formato del JSON (ver ejemplos/):

  {
    "marca": "ksinuevos",                 # o "lavilet", o ruta a otro JSON de marca
    "alt": "Texto alternativo de la portada",
    "slides": [
      {"tipo": "portada", "titulo": "...", "subtitulo": "...", "imagen": "fotos/1.jpg"},
      {"tipo": "gancho", "texto": "Por qué importa, en una frase."},
      {"tipo": "idea", "titulo": "...", "texto": "...", "imagen": "opcional"},
      {"tipo": "ficha", "titulo": "Toyota Fortuner 2019", "datos": [["Kilometraje", "38.000 km"]],
       "precio": "$32.900", "imagen": "fotos/2.jpg"},
      {"tipo": "comparacion", "titulo": "...", "izquierda": {"titulo": "A", "puntos": ["..."]},
       "derecha": {"titulo": "B", "puntos": ["..."]}},
      {"tipo": "imagen", "imagen": "renders/piscina.jpg", "posicion": "30% center", "titulo": "...", "texto": "..."},
      {"tipo": "resumen", "titulo": "...", "puntos": ["...", "..."]},
      {"tipo": "cta", "titulo": "Comenta FORTUNER", "texto": "y te mando toda la info"}
    ]
  }

Requisitos para PNG: Python con playwright (pip install playwright) y Chrome o
Chromium instalado. Sin eso, usa --solo-html y abre el HTML en el navegador.
"""

import argparse
import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARCAS = HERE / "marcas"
W, H = 1080, 1350

try:                                              # opcional: califica la portada como gancho
    sys.path.insert(0, str(HERE.parent / "ig-reel"))
    from hookscore import run as score_hook       # noqa: E402
except Exception:
    score_hook = None

TIPOS = {"portada", "gancho", "idea", "ficha", "comparacion", "imagen", "resumen", "cta"}
WORD_RE = re.compile(r"[\w$%'’-]+")


def nwords(text):
    return len(WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text or "")))


def esc(text):
    return html.escape(str(text or ""))


# ----------------------------------------------------------------------------
# Carga
# ----------------------------------------------------------------------------

def load_brand(name_or_path, spec_dir):
    p = Path(name_or_path)
    if not p.suffix:
        p = MARCAS / f"{name_or_path}.json"
    elif not p.is_absolute():
        p = (spec_dir / p).resolve()
    if not p.exists():
        raise SystemExit(f"no encuentro la marca '{name_or_path}' (busqué {p})")
    brand = json.load(open(p, encoding="utf-8"))
    brand["_dir"] = p.parent
    return brand


def resolve(path, base):
    if not path:
        return None
    p = Path(os.path.expanduser(path))
    return p if p.is_absolute() else (base / p).resolve()


# ----------------------------------------------------------------------------
# Revisión
# ----------------------------------------------------------------------------

def review(spec, spec_dir):
    slides = spec.get("slides") or []
    checks = []

    def add(status, name, detail):
        checks.append((status, name, detail))

    n = len(slides)
    if n < 3:
        add("FALLA", "CANTIDAD", f"{n} diapositivas. Menos de 3 no es un carrusel")
    elif n < 5:
        add("AVISO", "CANTIDAD", f"{n} diapositivas. Con menos de 5 el deslizar nunca arranca")
    elif n > 20:
        add("FALLA", "CANTIDAD", f"{n} diapositivas. Instagram acepta hasta 20")
    elif n > 10:
        add("AVISO", "CANTIDAD", f"{n} diapositivas. Pasando de 10 casi nadie llega al final")
    else:
        add("OK", "CANTIDAD", f"{n} diapositivas")

    for i, s in enumerate(slides, 1):
        if s.get("tipo") not in TIPOS:
            add("FALLA", f"DIAPO {i}", f"tipo '{s.get('tipo')}' desconocido. Usa: {', '.join(sorted(TIPOS))}")

    if not slides:
        return checks
    cover = slides[0]
    if cover.get("tipo") != "portada":
        add("FALLA", "PORTADA", "la primera diapositiva tiene que ser tipo 'portada'")
    else:
        t = cover.get("titulo", "")
        w = nwords(t)
        status = "OK" if w <= 6 else ("AVISO" if w <= 10 else "FALLA")
        detail = f"{w} palabras: \"{t}\"" + ("" if w <= 6 else ". La portada es el 80% del resultado: 6 palabras o menos")
        if score_hook and t:
            _, overall, verdict, flags = score_hook(t)
            detail += f"  ·  gancho {overall:.0f} {verdict}"
            if flags:
                detail += f" ({flags[0]})"
        add(status, "PORTADA", detail)

    if len(slides) > 1 and slides[1].get("tipo") in ("gancho", "idea", "ficha", "imagen"):
        add("OK", "SEGUNDA", "la 2 se sostiene sola (Instagram puede volver a mostrar el carrusel desde ahí)")
    elif len(slides) > 1:
        add("AVISO", "SEGUNDA", "la 2 debería ser el 'por qué importa'. Instagram a veces muestra el carrusel desde ella")

    ctas = [i for i, s in enumerate(slides, 1) if s.get("tipo") == "cta"]
    if not ctas:
        add("AVISO", "PEDIDO", "no hay diapositiva 'cta'. Decide qué quieres que hagan: comentar, escribir o agendar")
    elif len(ctas) > 1:
        add("AVISO", "PEDIDO", f"{len(ctas)} diapositivas de pedido. Un solo pedido, al final")
    elif ctas[0] != len(slides):
        add("AVISO", "PEDIDO", f"el pedido está en la {ctas[0]}, no en la última")
    else:
        add("OK", "PEDIDO", "un solo pedido, al final")

    if len(slides) >= 6 and not any(s.get("tipo") == "resumen" for s in slides):
        add("AVISO", "RESUMEN", "no hay diapositiva 'resumen'. Es la que la gente captura y reenvía")

    for i, s in enumerate(slides, 1):
        tipo = s.get("tipo")
        if tipo in ("idea", "imagen") and s.get("titulo"):
            w = nwords(s["titulo"])
            if not 2 <= w <= 8:
                add("AVISO", f"DIAPO {i}", f"título de {w} palabras (ideal 3 a 7)")
        texto = s.get("texto", "")
        if tipo not in ("portada",) and texto:
            w = nwords(texto)
            if w > 40:
                add("FALLA", f"DIAPO {i}", f"{w} palabras de texto. Eso es un párrafo: pártelo en dos diapositivas")
            elif w > 25:
                add("AVISO", f"DIAPO {i}", f"{w} palabras de texto (máximo 25)")
        if tipo == "ficha":
            datos = s.get("datos") or []
            if len(datos) > 6:
                add("AVISO", f"DIAPO {i}", f"{len(datos)} datos en la ficha. Más de 6 no se leen en el celular")
            if not s.get("precio"):
                add("INFO", f"DIAPO {i}", "ficha sin precio. Si es a propósito, prepárate para que el comentario más común sea '¿precio?'")
        if tipo == "resumen":
            pts = s.get("puntos") or []
            if len(pts) > 6:
                add("AVISO", f"DIAPO {i}", f"{len(pts)} puntos en el resumen. Para que lo capturen, 6 o menos")
        if tipo == "comparacion":
            for lado in ("izquierda", "derecha"):
                if not (s.get(lado) or {}).get("titulo"):
                    add("FALLA", f"DIAPO {i}", f"la comparación no tiene '{lado}.titulo'")
        img = s.get("imagen")
        if img:
            p = resolve(img, spec_dir)
            if not p.exists():
                add("FALLA", f"DIAPO {i}", f"no existe la imagen {img}")
        elif tipo == "imagen":
            add("FALLA", f"DIAPO {i}", "tipo 'imagen' sin 'imagen'")
        blob = json.dumps(s, ensure_ascii=False)
        if "{{" in blob:
            add("FALLA", f"DIAPO {i}", "quedó un {{hueco}} sin llenar. No se publica con datos inventados ni vacíos")

    if not spec.get("alt"):
        add("AVISO", "ALT", "sin texto alternativo para la portada. Lo usan los lectores de pantalla e Instagram")
    return checks


def render_review(checks, out=sys.stdout):
    print("\nREVISIÓN DEL CARRUSEL", file=out)
    print("=" * 72, file=out)
    for status, name, detail in checks:
        print(f"  {status:<5} {name:<10} {detail}", file=out)
    fails = sum(1 for c in checks if c[0] == "FALLA")
    warns = sum(1 for c in checks if c[0] == "AVISO")
    verdict = "CORREGIR" if fails else ("REVISAR" if warns else "LISTO")
    print("-" * 72, file=out)
    print(f"  VEREDICTO  {verdict}\n", file=out)
    return verdict


def copy_text(spec):
    lines = [f"CARRUSEL  ·  {len(spec['slides'])} diapositivas", ""]
    for i, s in enumerate(spec["slides"], 1):
        tipo = s.get("tipo", "").upper()
        head = s.get("titulo") or s.get("texto") or ""
        lines.append(f"{i:>2}  {tipo:<12} {head}")
        if s.get("titulo") and s.get("texto"):
            lines.append(f"{'':>16}{s['texto']}")
        if s.get("subtitulo"):
            lines.append(f"{'':>16}{s['subtitulo']}")
        for k, v in s.get("datos") or []:
            lines.append(f"{'':>16}{k}: {v}")
        if s.get("precio"):
            lines.append(f"{'':>16}Precio: {s['precio']}")
        for p in s.get("puntos") or []:
            lines.append(f"{'':>16}- {p}")
        for lado in ("izquierda", "derecha"):
            if s.get(lado):
                lines.append(f"{'':>16}{s[lado].get('titulo', '')}: " + "; ".join(s[lado].get("puntos", [])))
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# HTML
# ----------------------------------------------------------------------------

def font_css(brand):
    seen, faces = set(), []
    for role, f in brand["fuentes"].items():
        path = resolve(f["archivo"], brand["_dir"])
        key = (f["familia"], str(path))
        if key in seen:
            continue
        seen.add(key)
        if path and path.exists():
            faces.append(
                f"@font-face{{font-family:'{f['familia']}';src:url('{path.as_uri()}');"
                f"font-weight:100 900;font-stretch:62% 125%;}}")
    vars_ = []
    for role, f in brand["fuentes"].items():
        vars_.append(f"--f-{role}:'{f['familia']}',Inter,Arial,sans-serif;"
                     f"--w-{role}:{f['peso']};--s-{role}:{f['ancho']}%;"
                     f"--t-{role}:{'uppercase' if f.get('mayusculas') else 'none'};"
                     f"--l-{role}:{f.get('espaciado', '0')};")
    return "\n".join(faces), "".join(vars_)


CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#777}
body{display:flex;flex-direction:column;align-items:center;gap:40px;padding:40px 0}
.slide{--k:1;width:1080px;height:1350px;position:relative;overflow:hidden;
  background:var(--fondo);color:var(--texto);display:flex;flex-direction:column;
  padding:110px 110px 0 110px}
.slide.oscura{background:var(--fondo_alt);color:#fff;--texto_suave:rgba(255,255,255,.72)}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.velo{position:absolute;inset:0}
.content{position:relative;flex:1;display:flex;flex-direction:column;min-height:0}
.foot{position:relative;height:120px;display:flex;align-items:center;justify-content:space-between;
  font-family:var(--f-etiqueta);font-weight:var(--w-etiqueta);font-stretch:var(--s-etiqueta);
  text-transform:var(--t-etiqueta);letter-spacing:var(--l-etiqueta);font-size:24px;color:var(--texto_suave)}
.foot .logo{height:44px}
.titulo{font-family:var(--f-titulo);font-weight:var(--w-titulo);font-stretch:var(--s-titulo);
  text-transform:var(--t-titulo);letter-spacing:var(--l-titulo);line-height:1.02}
.texto{font-family:var(--f-texto);font-weight:var(--w-texto);font-stretch:var(--s-texto);
  text-transform:var(--t-texto);letter-spacing:var(--l-texto);line-height:1.32;font-size:calc(var(--k)*42px)}
.etiqueta{font-family:var(--f-etiqueta);font-weight:var(--w-etiqueta);font-stretch:var(--s-etiqueta);
  text-transform:var(--t-etiqueta);letter-spacing:var(--l-etiqueta);font-size:26px;color:var(--acento)}
.cifra{font-family:var(--f-cifras);font-weight:var(--w-cifras);font-stretch:var(--s-cifras);letter-spacing:var(--l-cifras)}
.suave{color:var(--texto_suave)}
.grow{flex:1}

/* portada */
.portada .titulo{font-size:calc(var(--k)*128px);margin-top:auto}
.portada .sub{margin-top:28px;font-size:calc(var(--k)*44px)}
.portada .content{padding-bottom:30px}
.portada.con-foto{color:#fff;--texto_suave:rgba(255,255,255,.8)}
.portada.con-foto .velo{background:linear-gradient(180deg,rgba(0,0,0,.05) 25%,rgba(0,0,0,.82) 78%)}

/* gancho */
.gancho .content{justify-content:center}
.gancho .titulo{font-size:calc(var(--k)*84px)}

/* idea */
.idea .num{font-size:calc(var(--k)*150px);line-height:.9;color:var(--acento);margin-bottom:30px}
.idea .titulo{font-size:calc(var(--k)*80px);margin-bottom:36px}
.idea .foto{height:500px;border-radius:var(--radio);background-size:cover;background-position:center;margin-bottom:44px;flex:none}
.idea .content{justify-content:center}

/* ficha */
.ficha{padding:0}
.ficha .foto{height:640px;background-size:cover;background-position:center;flex:none;position:relative}
.ficha .foto.vacia{background:var(--fondo_alt)}
.ficha .content{padding:56px 110px 0}
.ficha .titulo{font-size:calc(var(--k)*72px);margin-bottom:34px}
.ficha .grid{display:grid;grid-template-columns:1fr 1fr;gap:26px 50px}
.ficha .dato .k{font-size:22px;margin-bottom:6px}
.ficha .dato .v{font-size:calc(var(--k)*44px);line-height:1.1}
.ficha .precio{position:absolute;right:110px;bottom:-46px;background:var(--acento);color:var(--texto_sobre_acento);
  font-size:64px;padding:14px 34px;border-radius:var(--radio)}
.ficha .foot{padding:0 110px}

/* comparacion */
.comparacion .titulo{font-size:calc(var(--k)*76px);margin-bottom:56px}
.comparacion .cols{display:grid;grid-template-columns:1fr 1fr;gap:44px;flex:1;min-height:0}
.comparacion .col{border-top:var(--linea) solid var(--acento);padding-top:30px}
.comparacion .col h3{margin-bottom:26px;font-size:calc(var(--k)*54px)}
.comparacion .col li{list-style:none;margin-bottom:22px;font-size:calc(var(--k)*36px)}

/* imagen */
.imagen{color:#fff;--texto_suave:rgba(255,255,255,.8)}
.imagen .velo{background:linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(0,0,0,.78) 88%)}
.imagen .content{justify-content:flex-end;padding-bottom:20px}
.imagen .titulo{font-size:calc(var(--k)*88px);margin-bottom:20px}

/* resumen */
.resumen .titulo{font-size:calc(var(--k)*76px);margin-bottom:50px}
.resumen ol{list-style:none;counter-reset:n}
.resumen li{counter-increment:n;display:flex;gap:28px;align-items:baseline;margin-bottom:30px;font-size:calc(var(--k)*40px)}
.resumen li::before{content:counter(n,decimal-leading-zero);font-family:var(--f-cifras);font-weight:var(--w-cifras);
  font-stretch:var(--s-cifras);color:var(--acento);font-size:calc(var(--k)*46px);min-width:70px}

/* cta */
.cta .content{justify-content:center}
.cta .titulo{font-size:calc(var(--k)*110px);margin-bottom:34px}
.cta .texto{font-size:calc(var(--k)*46px)}
.cta .boton{margin-top:60px;align-self:flex-start;background:var(--acento);color:var(--texto_sobre_acento);
  padding:22px 40px;border-radius:var(--radio);font-size:30px}
.cta .cierre{margin-top:auto;padding-bottom:20px;font-size:30px}

/* ---- estilo enérgico (KsiNuevos) ---- */
.energico{--radio:18px;--linea:8px}
.energico .titulo .marca{color:var(--acento)}
.energico.gancho .titulo::after,.energico.cta .titulo::after{content:"";display:block;width:160px;height:14px;background:var(--acento);margin-top:40px}
.energico.idea .num{color:var(--acento)}

/* ---- estilo elegante (La Vilet) ---- */
.elegante{--radio:0;--linea:1px;padding-left:120px;padding-right:120px}
.elegante .titulo{line-height:1.08}
.elegante.portada .titulo{font-size:calc(var(--k)*132px)}
.elegante .regla{width:120px;height:1px;background:var(--acento);margin:0 0 44px}
.elegante.gancho .titulo{font-size:calc(var(--k)*78px)}
.elegante.idea .num{font-size:calc(var(--k)*120px)}
.elegante.cta .boton{background:transparent;border:1px solid var(--acento);color:inherit}
.elegante.ficha .precio{background:var(--fondo);color:var(--texto);border:1px solid var(--acento)}
.elegante .foot{font-size:20px}
"""

FIT_JS = r"""
async () => {
  await document.fonts.ready;
  for (const s of document.querySelectorAll('.slide')) {
    const c = s.querySelector('.content');
    let k = 1;
    const over = () => c.scrollHeight > c.clientHeight + 2 ||
      [...c.querySelectorAll('.titulo,.texto,.v')].some(e => e.scrollWidth > e.clientWidth + 2);
    while (over() && k > 0.5) {
      k -= 0.03; s.style.setProperty('--k', k.toFixed(2));
    }
  }
}
"""


def bg(path, cls="bg", pos=None):
    if not path:
        return ""
    style = f"background-image:url('{path.as_uri()}')" + (f";background-position:{pos}" if pos else "")
    return f'<div class="{cls}" style="{style}"></div>'


def slide_html(s, i, n, brand, spec_dir):
    tipo = s["tipo"]
    estilo = brand.get("estilo", "energico")
    img = resolve(s.get("imagen"), spec_dir)
    pos = s.get("posicion")            # encuadre de la foto: "30% center", "right", etc.
    titulo = esc(s.get("titulo"))
    texto = esc(s.get("texto"))
    regla = '<div class="regla"></div>' if estilo == "elegante" else ""
    classes = [tipo, estilo]
    pre, body, after = "", "", ""

    if tipo == "portada":
        if img:
            classes.append("con-foto")
            pre = bg(img, pos=pos) + '<div class="velo"></div>'
        etq = esc(s.get("etiqueta", ""))
        body = (f'<div class="etiqueta">{etq}</div>' if etq else "") + \
            f'<div class="titulo">{titulo}</div>' + \
            (f'<div class="texto sub">{esc(s.get("subtitulo"))}</div>' if s.get("subtitulo") else "")
    elif tipo == "gancho":
        classes.append("oscura")
        body = regla + f'<div class="titulo">{texto or titulo}</div>'
    elif tipo == "idea":
        num = s.get("numero")
        body = (f'<div class="num cifra">{esc(num)}</div>' if num else "") + \
            (bg(img, "foto", pos) if img else "") + regla + \
            f'<div class="titulo">{titulo}</div><div class="texto suave">{texto}</div>'
    elif tipo == "ficha":
        foto = bg(img, "foto", pos) if img else '<div class="foto vacia"></div>'
        precio = f'<div class="precio cifra">{esc(s["precio"])}</div>' if s.get("precio") else ""
        foto = foto.replace("></div>", f">{precio}</div>", 1) if precio else foto
        datos = "".join(
            f'<div class="dato"><div class="k etiqueta">{esc(k)}</div><div class="v cifra">{esc(v)}</div></div>'
            for k, v in (s.get("datos") or []))
        pre = foto
        body = f'<div class="titulo">{titulo}</div><div class="grid">{datos}</div>'
    elif tipo == "comparacion":
        cols = ""
        for lado in ("izquierda", "derecha"):
            d = s.get(lado) or {}
            pts = "".join(f'<li class="texto">{esc(p)}</li>' for p in d.get("puntos", []))
            cols += f'<div class="col"><h3 class="titulo">{esc(d.get("titulo"))}</h3><ul>{pts}</ul></div>'
        body = f'<div class="titulo">{titulo}</div><div class="cols">{cols}</div>'
    elif tipo == "imagen":
        pre = bg(img, pos=pos) + '<div class="velo"></div>'
        body = regla + f'<div class="titulo">{titulo}</div>' + (f'<div class="texto">{texto}</div>' if texto else "")
    elif tipo == "resumen":
        pts = "".join(f'<li class="texto">{esc(p)}</li>' for p in s.get("puntos") or [])
        body = regla + f'<div class="titulo">{titulo}</div><ol>{pts}</ol>'
    elif tipo == "cta":
        classes.append("oscura")
        boton = s.get("boton")
        cierre = s.get("cierre", brand.get("cierre", ""))
        body = regla + f'<div class="titulo">{titulo}</div>' + \
            (f'<div class="texto">{texto}</div>' if texto else "") + \
            (f'<div class="boton etiqueta">{esc(boton)}</div>' if boton else "") + \
            (f'<div class="cierre etiqueta suave">{esc(cierre)}</div>' if cierre else "")

    logo = resolve(brand.get("logo"), brand["_dir"]) if brand.get("logo") else None
    left = f'<img class="logo" src="{logo.as_uri()}">' if logo and logo.exists() else esc(brand.get("handle", ""))
    foot = f'<div class="foot"><span>{left}</span><span>{i}/{n}</span></div>'
    return (f'<section class="slide {" ".join(classes)}" data-n="{i}">{pre}'
            f'<div class="content">{body}</div>{foot}{after}</section>')


def build_html(spec, brand, spec_dir):
    faces, fvars = font_css(brand)
    c = brand["colores"]
    cvars = "".join(f"--{k}:{v};" for k, v in c.items())
    n = len(spec["slides"])
    slides = "\n".join(slide_html(s, i, n, brand, spec_dir) for i, s in enumerate(spec["slides"], 1))
    return (f"<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'>"
            f"<title>{esc(brand.get('nombre'))} - carrusel</title>"
            f"<style>{faces}\n:root{{{cvars}{fvars}}}\n{CSS}</style></head>"
            f"<body>{slides}<script>({FIT_JS})()</script></body></html>")


# ----------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------

def find_browser():
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    return mac if os.path.exists(mac) else None


def render(html_path, out_dir, n, pdf=False):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("falta playwright: pip install playwright  (o usa --solo-html)")
    files = []
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            exe = find_browser()
            if not exe:
                raise SystemExit("no encuentro Chrome/Chromium. Instala uno o corre: playwright install chromium")
            browser = p.chromium.launch(executable_path=exe)
        page = browser.new_page(viewport={"width": W + 200, "height": H + 200}, device_scale_factor=1)
        page.goto(html_path.as_uri())
        page.evaluate(FIT_JS)
        page.wait_for_timeout(300)
        for i in range(1, n + 1):
            el = page.locator(f'section.slide[data-n="{i}"]')
            f = out_dir / f"diapo-{i:02d}.png"
            el.screenshot(path=str(f))
            files.append(f)
        if pdf:
            page.add_style_tag(content="html,body{background:none}body{padding:0;gap:0}"
                                       f"@page{{size:{W}px {H}px;margin:0}}")
            f = out_dir / "carrusel.pdf"
            page.pdf(path=str(f), width=f"{W}px", height=f"{H}px", print_background=True)
            files.append(f)
        browser.close()
    return files


def main():
    ap = argparse.ArgumentParser(description="Revisa y renderiza un carrusel de Instagram.")
    ap.add_argument("spec", help="archivo JSON con el contenido del carrusel")
    ap.add_argument("--out", help="carpeta de salida para el HTML y los PNG")
    ap.add_argument("--marca", help="sobrescribe la marca del JSON (ksinuevos, lavilet o ruta)")
    ap.add_argument("--revisar", action="store_true", help="solo revisa, no genera archivos")
    ap.add_argument("--texto", action="store_true", help="imprime el copy numerado y sale")
    ap.add_argument("--solo-html", action="store_true", help="genera el HTML sin PNG")
    ap.add_argument("--pdf", action="store_true", help="genera también un PDF con todas las diapositivas")
    ap.add_argument("--forzar", action="store_true", help="renderiza aunque la revisión tenga FALLAS")
    args = ap.parse_args()

    spec_path = Path(args.spec).resolve()
    spec = json.load(open(spec_path, encoding="utf-8"))
    spec_dir = spec_path.parent

    if args.texto:
        print(copy_text(spec))
        return

    checks = review(spec, spec_dir)
    verdict = render_review(checks)
    if args.revisar:
        sys.exit(0 if verdict == "LISTO" else 1)
    if verdict == "CORREGIR" and not args.forzar:
        print("No genero archivos con FALLAS. Corrige o usa --forzar.", file=sys.stderr)
        sys.exit(1)
    if not args.out:
        print("Usa --out carpeta/ para generar los archivos.", file=sys.stderr)
        sys.exit(0)

    brand = load_brand(args.marca or spec.get("marca", "ksinuevos"), spec_dir)
    out_dir = Path(os.path.expanduser(args.out)).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    html_path = out_dir / "carrusel.html"
    html_path.write_text(build_html(spec, brand, spec_dir), encoding="utf-8")
    print(f"escrito {html_path}")
    if args.solo_html:
        return
    for f in render(html_path, out_dir, len(spec["slides"]), pdf=args.pdf):
        print(f"escrito {f}")
    if spec.get("alt"):
        (out_dir / "alt.txt").write_text(spec["alt"] + "\n", encoding="utf-8")
        print(f"escrito {out_dir / 'alt.txt'}")


if __name__ == "__main__":
    main()
