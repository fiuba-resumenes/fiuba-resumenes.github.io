#!/usr/bin/env python3
"""Arma el apunte de una materia sobre el shell compartido.

Es el mismo adaptador que usa el apunte de Sistemas Distribuidos, pero
parametrizado: la identidad, la paleta y el indice salen de materias.py, y los
fragmentos de fuentes/<clave>/. Agregar una materia no toca este archivo.

Uso:
    python3 armar.py redes
    python3 armar.py ebt
    python3 armar.py            # todas
"""
import re
import sys
import unicodedata
from pathlib import Path

import autoria
from materias import MATERIAS

BASE = Path(__file__).resolve().parent
REPO = BASE.parent
SHELL = BASE / "shell.html"
# Modulos que se inyectan antes de </body>, en este orden.
MODULOS = [BASE / "sync.html", BASE / "imprimir.html"]

# vocabulario propio de los fragmentos -> callouts del shell
CLASES = {
    "def": "callout",
    "idea": "callout blue",
    "ej": "callout example",
    "warn": "callout warning",
    "examen": "callout exam",
}

CSS_EXTRA = """
    /* ---- agregados para estos apuntes ---- */
    .callout.example { border-color: var(--ok); background: var(--ok-bg); color: var(--ok); }
    .callout.exam { border-color: var(--exam); background: var(--exam-bg); color: var(--exam); }
    .callout > b:first-child, .callout > strong:first-child { color: inherit; }
    .callout.blue::before { content: "Intuición"; }
    .callout.example::before { content: "Ejemplo"; }
    .callout.warning::before { content: "Ojo"; }
    .callout.exam::before { content: "Tomado en finales"; }
    .callout.blue::before, .callout.example::before,
    .callout.warning::before, .callout.exam::before {
      display: block;
      margin-bottom: 6px;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: .1em;
      text-transform: uppercase;
      opacity: .85;
    }
    p.intro {
      margin: 0 0 26px;
      color: var(--muted);
      font-size: 18px;
      line-height: 1.6;
    }
    pre {
      margin: 16px 0 22px;
      padding: 16px 18px;
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--surface-2);
      font-size: 13.5px;
      line-height: 1.55;
    }
    pre code { font-size: inherit; }
    :not(pre) > code {
      padding: 1px 6px;
      border-radius: 6px;
      background: var(--surface-2);
    }
    figure.diag {
      margin: 22px 0;
      padding: 18px 16px 12px;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: var(--surface);
      text-align: center;
    }
    /* Alias que usan los SVG de los fragmentos (ver contrato-fragmento.md).
       --linea no apunta a --line: ese token es un borde decorativo de 1.2:1 y
       como trazo de diagrama no se veria. Las flechas necesitan --muted. */
    :root, html[data-theme="dark"] {
      --linea: var(--muted);
      --acc: var(--accent);
      --acc2: var(--blue);
    }
    figure.diag svg { max-width: 100%; height: auto; color: var(--ink); }
    figure.diag figcaption {
      margin-top: 12px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
      text-align: left;
    }
    p.nota {
      margin: 14px 0;
      padding-left: 14px;
      border-left: 3px solid var(--line);
      color: var(--muted);
      font-size: 14.5px;
    }
    p.ref {
      margin: 14px 0 0;
      padding-top: 10px;
      border-top: 1px dashed var(--line);
      color: var(--muted);
      font-size: 13.5px;
    }
    dl.glo {
      display: grid;
      grid-template-columns: minmax(170px, auto) 1fr;
      gap: 9px 22px;
      margin: 12px 0 26px;
      align-items: baseline;
    }
    dl.glo dt { font-weight: 700; }
    dl.glo dd { margin: 0; color: var(--muted); font-size: 15px; }
    dl.glo dd a {
      margin-left: 4px;
      padding: 1px 6px;
      border: 1px solid var(--line);
      border-radius: 6px;
      color: var(--accent);
      font-size: 12px;
      font-weight: 700;
      text-decoration: none;
      white-space: nowrap;
    }
    dl.glo dd a:hover { border-color: var(--accent); background: var(--accent-2); }
    @media (max-width: 640px) {
      dl.glo { grid-template-columns: 1fr; gap: 2px; }
      dl.glo dt { margin-top: 12px; }
    }
"""

# sombras con tinte del shell original que quedaban fuera de los tokens
SOMBRAS_BASE = ["rgba(18, 44, 58, .1)", "rgba(15, 25, 22, .2)", "rgba(7, 23, 31, .36)"]


def slug_kw(texto: str) -> str:
    t = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode()
    t = t.lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    vistas, out = set(), []
    for w in t.split():
        if len(w) > 2 and w not in vistas:
            vistas.add(w)
            out.append(w)
    return " ".join(out)


def transformar(frag: str, uid: str, numero: str) -> str:
    m = re.search(r"<h2[^>]*>(.*?)</h2>", frag, re.S)
    if not m:
        raise SystemExit(f"!! el fragmento {uid} no tiene <h2>")
    titulo = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    titulo = re.sub(r"^[A-Z]?\d+\.\s*", "", titulo)

    heads = [re.sub(r"<[^>]+>", "", h) for h in
             re.findall(r"<h[34][^>]*>(.*?)</h[34]>", frag, re.S)]
    kw = slug_kw(titulo + " " + " ".join(heads))

    cuerpo = frag[m.end():].rstrip()
    if cuerpo.endswith("</section>"):
        cuerpo = cuerpo[: -len("</section>")]

    for viejo, nuevo in CLASES.items():
        cuerpo = cuerpo.replace(f'<div class="{viejo}">', f'<div class="{nuevo}">')

    def fix_details(mm):
        interior = mm.group(2)
        s = re.search(r"<summary>(.*?)</summary>", interior, re.S)
        if not s:
            return mm.group(0)
        return (f"<details><summary>{s.group(1)}</summary>"
                f'<div class="details-body">{interior[s.end():]}</div></details>')

    cuerpo = re.sub(r'<details class="(mas|preg)">(.*?)</details>',
                    fix_details, cuerpo, flags=re.S)

    # tablas: el shell las quiere envueltas para poder scrollearlas
    cuerpo = re.sub(r'<div class="tablewrap">\s*(<table>.*?</table>)\s*</div>',
                    r'<div class="table-wrap">\1</div>', cuerpo, flags=re.S)
    cuerpo = re.sub(r'(?<!<div class="table-wrap">)(<table>.*?</table>)',
                    lambda mm: f'<div class="table-wrap">{mm.group(1)}</div>',
                    cuerpo, flags=re.S)
    cuerpo = cuerpo.replace("<ul>\n    <li><b>", '<ul class="study-list">\n    <li><b>')

    return (f'    <section class="chapter" id="{uid}" data-title="{kw}">\n'
            f'      <div class="chapter-head">\n'
            f'        <div class="chapter-number">{numero}</div>\n'
            f'        <div><h2>{titulo}</h2></div>\n'
            f'      </div>' + cuerpo + "\n    </section>\n")


def sidebar(grupos) -> str:
    partes = []
    for titulo, items in grupos:
        partes.append(f'    <div class="nav-title">{titulo}</div>')
        partes.append(f'    <nav class="toc" aria-label="{titulo}">')
        for uid, num, nombre in items:
            partes.append(f'      <a href="#{uid}"><span>{num}</span>{nombre}</a>')
        partes.append("    </nav>")
    return "\n".join(partes)


def favicon_de(hexcolor: str) -> str:
    """Icono propio por materia: la inicial no sirve, se usa un glifo de nodos."""
    return ("data:image/svg+xml,"
            "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
            f"%3Crect width='64' height='64' rx='14' fill='%23{hexcolor}'/%3E"
            "%3Cg stroke='white' stroke-width='3' fill='white'%3E"
            "%3Cline x1='32' y1='32' x2='32' y2='14' /%3E"
            "%3Cline x1='32' y1='32' x2='16' y2='44' /%3E"
            "%3Cline x1='32' y1='32' x2='48' y2='44' /%3E"
            "%3Ccircle cx='32' cy='32' r='6'/%3E"
            "%3Ccircle cx='32' cy='13' r='5'/%3E"
            "%3Ccircle cx='15' cy='45' r='5'/%3E"
            "%3Ccircle cx='49' cy='45' r='5'/%3E"
            "%3C/g%3E%3C/svg%3E")


def armar(cfg: dict) -> int:
    doc = SHELL.read_text(encoding="utf-8")
    frag_dir = BASE / cfg["clave"]

    # 1. capitulos
    ini = doc.find('<section class="chapter"')
    fin = doc.rfind("</section>") + len("</section>")
    capitulos, faltan = [], []
    for _, items in cfg["grupos"]:
        for uid, num, _ in items:
            f = frag_dir / f"{uid}.html"
            if not f.exists():
                faltan.append(f.name)
                continue
            capitulos.append(transformar(f.read_text(encoding="utf-8"), uid, num))
    if faltan:
        print(f"!! faltan fragmentos de {cfg['clave']}: {faltan}", file=sys.stderr)
        return 1
    doc = doc[:ini] + "\n".join(capitulos).lstrip() + doc[fin:]

    # 2. sidebar
    s_ini = doc.find('<div class="nav-title">')
    s_fin = doc.rfind("</nav>", 0, doc.find('class="side-actions"')) + len("</nav>")
    doc = doc[:s_ini] + sidebar(cfg["grupos"]).lstrip() + doc[s_fin:]

    # 3. identidad
    doc = re.sub(r"<title>.*?</title>", f"<title>{cfg['titulo_tab']}</title>",
                 doc, flags=re.S)
    doc = doc.replace("<strong>Aprendizaje Automático</strong>",
                      f"<strong>{cfg['marca']}</strong>")
    doc = re.sub(r'<header class="hero">.*?</header>',
                 f'<header class="hero">\n        <h1>{cfg["h1"]}</h1>\n'
                 f'        <p>{cfg["hero"]}</p>\n      </header>', doc, flags=re.S)
    doc = re.sub(r'<meta name="description" content="[^"]*"',
                 f'<meta name="description" content="{cfg["descripcion"]}"', doc)
    doc = doc.replace('content="Aprendizaje Automático"', f'content="{cfg["marca"]}"')

    # 4. estado propio en localStorage: los apuntes comparten dominio
    doc = re.sub(r"'aa-([a-z0-9-]+)'", rf"'{cfg['prefijo_ls']}-\1'", doc)

    # 5. paleta
    doc, n_l = re.subn(r":root\s*\{[^}]*\}", lambda _: cfg["paleta_light"], doc, count=1)
    doc, n_d = re.subn(r'html\[data-theme="dark"\]\s*\{[^}]*\}',
                       lambda _: cfg["paleta_dark"], doc, count=1)
    if not (n_l and n_d):
        print(f"!! no se pudo reemplazar la paleta (light={n_l}, dark={n_d})",
              file=sys.stderr)
        return 1
    for s in SOMBRAS_BASE:
        doc = doc.replace(s, "rgba(20, 20, 20, .18)")
    doc = doc.replace('content="#167e9e"', f'content="{cfg["theme_color"]}"')
    doc = doc.replace("</style>", CSS_EXTRA + "  </style>", 1)

    # 5 bis. firma de autoria al pie de la barra lateral
    try:
        doc = autoria.inyectar(doc, cfg.get("autores"))
    except ValueError as e:
        print(f"!! autoria de {cfg['clave']}: {e}", file=sys.stderr)
        return 1

    # 6. PWA y botones de la otra materia
    doc = re.sub(r'\s*<link rel="manifest"[^>]*>', "", doc)
    doc = re.sub(r'\s*<link rel="apple-touch-icon"[^>]*>', "", doc)
    doc = re.sub(r"\s*<script>[^<]*serviceWorker.*?</script>", "", doc, flags=re.S)
    doc = re.sub(r'\s*<a class="icon-button wide" href="resumen\.html">.*?</a>', "",
                 doc, flags=re.S)
    doc = re.sub(r'<link rel="icon" href="data:image/png;base64,[^"]+"',
                 f'<link rel="icon" href="{favicon_de(cfg["favicon_hex"])}"', doc)

    # 7. sincronizacion entre dispositivos
    # Va al final del body: el modulo se cuelga solo del .side-actions y no
    # necesita que el shell le reserve nada. Un unico archivo para todos los
    # apuntes, para no tener tres copias divergiendo.
    # El reemplazo va como lambda y no como string: re.sub interpreta las
    # secuencias de escape del reemplazo, y convertiria los \n del JavaScript
    # en saltos de linea reales, partiendo los literales de texto al medio.
    for modulo in MODULOS:
        cuerpo = modulo.read_text(encoding="utf-8")
        marca = re.search(r'id="([a-z]+-dialog)"', cuerpo).group(1)
        # Si el shell ya lo trae (pasa cuando se refresca shell-aa.html desde el
        # apunte de Aprendizaje Automatico, que ya lo tiene inyectado), no se
        # duplica. El reemplazo va como lambda: re.sub interpreta los escapes
        # del string de reemplazo y convertiria los \n del JavaScript en saltos
        # de linea reales, partiendo los literales de texto al medio.
        if marca in doc:
            continue
        doc, n = re.subn(r"</body>", lambda _, c=cuerpo: c + "</body>", doc, count=1)
        if not n:
            print(f"!! no se encontro </body> para inyectar {modulo.name}", file=sys.stderr)
            return 1

    out = REPO / cfg["salida"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")

    # 7. validacion
    ids = re.findall(r'\sid="([^"]+)"', doc)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    rotos = sorted({h for h in re.findall(r'href="#([^"]+)"', doc)} - set(ids))
    usados = set(re.findall(r"var\(\s*(--[a-z0-9-]+)", doc))
    huerfanos = sorted(usados - set(re.findall(r"(--[a-z0-9-]+)\s*:", doc)))
    externos = re.findall(r'(?:src|href)="https?://[^"]*"', doc)
    externos = [e for e in externos if "github.com" not in e]

    print(f"escrito: {out.relative_to(REPO)}  "
          f"({len(doc.encode())//1024} KB, {len(capitulos)} capitulos)")
    print(f"  h3={len(re.findall(r'<h3', doc))} "
          f"callouts={len(re.findall(r'class=.callout', doc))} "
          f"svg={doc.count('<svg')} tablas={doc.count('<table')}")
    if dup:
        print(f"  !! ids duplicados: {dup[:8]}")
    if rotos:
        print(f"  !! anclas rotas: {rotos[:8]}")
    if huerfanos:
        print(f"  !! tokens CSS sin definir: {huerfanos}")
    if externos:
        print(f"  !! recursos externos: {externos[:4]}")
    if not (dup or rotos or huerfanos or externos):
        print("  ids unicos, anclas resuelven, tokens definidos, sin recursos externos")
    return 1 if (dup or rotos or huerfanos or externos) else 0


def main(argv) -> int:
    claves = argv or list(MATERIAS)
    malas = [c for c in claves if c not in MATERIAS]
    if malas:
        print(f"!! materia desconocida: {malas}. Hay: {list(MATERIAS)}", file=sys.stderr)
        return 1
    return max(armar(MATERIAS[c]) for c in claves)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
