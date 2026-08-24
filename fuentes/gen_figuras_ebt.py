#!/usr/bin/env python3
"""Genera las figuras SVG del apunte de EBT (fuentes/ebt/figuras/*.html).

Es el generador del apunte de echepereza adaptado a este repo: en vez de
colores de una paleta fija, los SVG salen con los alias de tokens del
contrato (currentColor, --acc, --acc2, --acc3, --acc4, --linea, --grid),
asi que se ven bien en cualquier materia y en los dos temas sin tocar nada.

Los fragmentos las referencian con <!--FIG:nombre--> y armar.py las inyecta
y las valida en cada build (ver contrato-fragmento.md). El resultado esta
commiteado: este script solo hay que correrlo si se cambia una figura.

Datos: los graficos de mercado usan el ejemplo de los helados de la fuente;
el ejemplo de prestamos (P=1000, i=10%, n=4) se construye aplicando las
formulas de la materia y esta marcado como tal en el apunte.

Uso:  python3 fuentes/gen_figuras_ebt.py   (reescribe fuentes/ebt/figuras/)
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ebt', 'figuras')

# Paleta por tokens: INK hereda la tinta del tema via figure.diag / .elast-card.
INK, MUT, GRID = 'currentColor', 'var(--linea)', 'var(--grid)'
ACC, DEM, OFE, RIESGO = 'var(--acc)', 'var(--acc2)', 'var(--acc3)', 'var(--acc4)'

# ---------------------------------------------------------------- helpers


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def legend(*items):
    """Leyenda de series: pares (color, rotulo). Va dentro de la figura."""
    spans = ''.join(f'<span><i style="background:{c}"></i>{esc(t)}</span>'
                    for c, t in items)
    return f'<div class="legend">{spans}</div>'


class Plot:
    """Sistema de coordenadas con margenes, en un viewBox de w x h."""

    def __init__(self, w=640, h=400, l=62, r=18, t=34, b=48,
                 xmax=12.0, ymax=3.0):
        self.w, self.h, self.l, self.r, self.t, self.b = w, h, l, r, t, b
        self.xmax, self.ymax = float(xmax), float(ymax)

    def x(self, q):
        return self.l + q / self.xmax * (self.w - self.l - self.r)

    def y(self, p):
        return (self.h - self.b) - p / self.ymax * (self.h - self.b - self.t)

    def frame(self, xlabel, ylabel, xticks, yticks, yfmt='{:.2f}'):
        o = []
        x0, y0 = self.x(0), self.y(0)
        for q in xticks:
            xx = self.x(q)
            o.append(f'<line x1="{xx:.1f}" y1="{y0:.1f}" x2="{xx:.1f}" y2="{self.t:.1f}" '
                     f'stroke="{GRID}" stroke-width="1" stroke-dasharray="2 4" />')
            o.append(f'<text x="{xx:.1f}" y="{y0 + 16:.1f}" font-size="11" fill="{MUT}" '
                     f'text-anchor="middle">{q:g}</text>')
        for p in yticks:
            yy = self.y(p)
            o.append(f'<line x1="{x0:.1f}" y1="{yy:.1f}" x2="{self.w - self.r:.1f}" y2="{yy:.1f}" '
                     f'stroke="{GRID}" stroke-width="1" stroke-dasharray="2 4" />')
            o.append(f'<text x="{x0 - 8:.1f}" y="{yy + 4:.1f}" font-size="11" fill="{MUT}" '
                     f'text-anchor="end">{yfmt.format(p)}</text>')
        o.append(f'<line x1="{x0:.1f}" y1="{self.t:.1f}" x2="{x0:.1f}" y2="{y0:.1f}" '
                 f'stroke="{INK}" stroke-width="1.6" />')
        o.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{self.w - self.r:.1f}" y2="{y0:.1f}" '
                 f'stroke="{INK}" stroke-width="1.6" />')
        o.append(f'<text x="{self.w - self.r:.1f}" y="{y0 + 34:.1f}" font-size="12" '
                 f'fill="{INK}" text-anchor="end" font-weight="600">{esc(xlabel)}</text>')
        # el rotulo del eje Y va ARRIBA del eje, no al costado, para no pisar
        # ni al eje ni a la primera marca
        o.append(f'<text x="4" y="12" font-size="12" fill="{INK}" '
                 f'font-weight="600">{esc(ylabel)}</text>')
        return o

    def polyline(self, pts, color, width=2.6, dash=None):
        d = ' '.join(f'{self.x(q):.1f},{self.y(p):.1f}' for q, p in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        return (f'<polyline points="{d}" fill="none" stroke="{color}" '
                f'stroke-width="{width}" stroke-linecap="round"{da} />')

    def dot(self, q, p, color):
        return (f'<circle cx="{self.x(q):.1f}" cy="{self.y(p):.1f}" r="4.5" '
                f'fill="{color}" />')


def svg(inner, w=640, h=400, label=''):
    a = f' role="img" aria-label="{esc(label)}"' if label else ''
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"{a}>\n    '
            + '\n    '.join(inner) + '\n  </svg>')


# ---------------------------------------------------------------- 1. tablas de oferta y demanda
DEMANDA = [(0.00, 12), (0.50, 10), (1.00, 8), (1.50, 6), (2.00, 4), (2.50, 2), (3.00, 0)]
OFERTA = [(0.00, 0), (0.50, 0), (1.00, 1), (1.50, 2), (2.00, 3), (2.50, 4), (3.00, 5)]


def fig_schedules():
    p = Plot(xmax=12.0, ymax=3.0)
    o = p.frame('Cantidad de helados', 'Precio ($)', range(0, 13), [0, .5, 1, 1.5, 2, 2.5, 3])
    o.append(p.polyline([(q, pr) for pr, q in DEMANDA], DEM))
    o.append(p.polyline([(q, pr) for pr, q in OFERTA], OFE))
    for pr, q in DEMANDA:
        o.append(p.dot(q, pr, DEM))
    for pr, q in OFERTA:
        o.append(p.dot(q, pr, OFE))
    o.append(f'<text x="{p.x(9.6):.1f}" y="{p.y(0.62):.1f}" font-size="13" fill="{DEM}" '
             f'font-weight="700">Demanda</text>')
    o.append(f'<text x="{p.x(4.6):.1f}" y="{p.y(2.72):.1f}" font-size="13" fill="{OFE}" '
             f'font-weight="700">Oferta</text>')
    return svg(o, label='Curvas de demanda y oferta de helados construidas con las tablas de la fuente')


# ---------------------------------------------------------------- 2. equilibrio y desplazamiento
def fig_equilibrio(shift=False):
    p = Plot(xmax=14.0, ymax=4.0)
    o = p.frame('Cantidad de helados', 'Precio ($)', range(0, 15), [0, 1, 2, 3, 4], '{:.0f}')

    def D(q, qe, pe):        # pendiente -0,15
        return pe - 0.15 * (q - qe)

    def S(q):                # pasa por (7, 2) y (10, 2.5)
        return 2.0 + (0.5 / 3.0) * (q - 7)

    o.append(p.polyline([(1, S(1)), (14, S(14))], OFE))
    o.append(f'<text x="{p.x(13.2):.1f}" y="{p.y(S(13.2)) - 10:.1f}" font-size="13" '
             f'fill="{OFE}" font-weight="700" text-anchor="end">Oferta</text>')

    d1 = [(1, D(1, 7, 2)), (14, D(14, 7, 2))]
    if shift:
        o.append(p.polyline(d1, DEM, 2.2, '6 5'))
        o.append(f'<text x="{p.x(13.6):.1f}" y="{p.y(D(13.6, 7, 2)) + 16:.1f}" font-size="12" '
                 f'fill="{DEM}" text-anchor="end">D<tspan dy="4" font-size="9">1</tspan></text>')
        d2 = [(1, D(1, 10, 2.5)), (14, D(14, 10, 2.5))]
        o.append(p.polyline(d2, DEM))
        o.append(f'<text x="{p.x(13.6):.1f}" y="{p.y(D(13.6, 10, 2.5)) + 16:.1f}" font-size="12" '
                 f'fill="{DEM}" font-weight="700" text-anchor="end">D<tspan dy="4" font-size="9">2</tspan></text>')
    else:
        o.append(p.polyline(d1, DEM))
        o.append(f'<text x="{p.x(13.6):.1f}" y="{p.y(D(13.6, 7, 2)) + 16:.1f}" font-size="13" '
                 f'fill="{DEM}" font-weight="700" text-anchor="end">Demanda</text>')

    def marca(q, pr, txt, color, tip):
        g = [f'<g><title>{esc(tip)}</title>']
        g.append(f'<line x1="{p.x(q):.1f}" y1="{p.y(pr):.1f}" x2="{p.x(q):.1f}" y2="{p.y(0):.1f}" '
                 f'stroke="{color}" stroke-width="1.2" stroke-dasharray="3 3" />')
        g.append(f'<line x1="{p.x(0):.1f}" y1="{p.y(pr):.1f}" x2="{p.x(q):.1f}" y2="{p.y(pr):.1f}" '
                 f'stroke="{color}" stroke-width="1.2" stroke-dasharray="3 3" />')
        g.append(f'<circle cx="{p.x(q):.1f}" cy="{p.y(pr):.1f}" r="6" fill="{color}" />')
        g.append(f'<text x="{p.x(q) + 12:.1f}" y="{p.y(pr) - 10:.1f}" font-size="12" '
                 f'fill="{INK}" font-weight="700">{esc(txt)}</text></g>')
        return '\n    '.join(g)

    o.append(marca(7, 2.0, 'Equilibrio inicial', ACC,
                   'Equilibrio inicial: 7 helados a $2,00'))
    if shift:
        o.append(marca(10, 2.5, 'Nuevo equilibrio', RIESGO,
                       'Nuevo equilibrio: 10 helados a $2,50, sube el precio y la cantidad'))
    else:
        # zonas de exceso SIEMPRE visibles: la info no puede depender del hover
        for pr, rotulo, sub, col in (
                (3.35, 'Exceso de OFERTA', 'sobra mercadería y el precio baja', OFE),
                (0.75, 'Exceso de DEMANDA', 'falta mercadería y el precio sube', DEM)):
            yy = p.y(pr)
            o.append(f'<rect x="{p.x(0):.1f}" y="{yy - 26:.1f}" '
                     f'width="{p.x(14) - p.x(0):.1f}" height="52" fill="{col}" opacity="0.09" />')
            o.append(f'<text x="{p.x(2.2):.1f}" y="{yy - 2:.1f}" font-size="12.5" fill="{col}" '
                     f'font-weight="700">{esc(rotulo)}</text>')
            o.append(f'<text x="{p.x(2.2):.1f}" y="{yy + 13:.1f}" font-size="11" fill="{col}">'
                     f'{esc(sub)}</text>')
    return svg(o, label='Equilibrio del mercado de helados')


# ---------------------------------------------------------------- 3. elasticidad
# 'Ep' se expande a E<sub>p</sub> al renderizar
ELAST = [
    ('Perfectamente inelástica', 'Ep = 0', 'Var.% Q = 0', 'No varía'),
    ('Inelástica', '0 &lt; Ep &lt; 1', 'Var.% Q &lt; Var.% P', 'Varía menos que proporcional'),
    ('Unitaria', 'Ep = 1', 'Var.% Q = Var.% P', 'Varía directamente proporcional'),
    ('Elástica', '1 &lt; Ep &lt; ∞', 'Var.% Q &gt; Var.% P', 'Varía más que proporcional'),
    ('Perfectamente elástica', 'Ep = ∞', 'Var.% P = 0', 'Precio constante'),
]
# trazos (x1,y1,x2,y2) en un lienzo 100x70, ejes en x=14 e y=58
CURVAS_D = [(50, 6, 50, 58), (24, 6, 46, 58), (22, 6, 74, 58), (20, 20, 92, 50), (18, 30, 96, 30)]
CURVAS_O = [(50, 6, 50, 58), (24, 58, 46, 6), (22, 58, 74, 6), (20, 50, 92, 20), (18, 30, 96, 30)]


def mini(trazo, color):
    x1, y1, x2, y2 = trazo
    return ('<svg viewBox="0 0 100 70" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<line x1="14" y1="6" x2="14" y2="58" stroke="{INK}" stroke-width="1.5" />'
            f'<line x1="14" y1="58" x2="96" y2="58" stroke="{INK}" stroke-width="1.5" />'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            'stroke-width="3" stroke-linecap="round" /></svg>')


# ejemplos: la fuente solo da los de la demanda
EJEMPLOS_D = ['Pan', 'Electricidad', 'Casos particulares',
              'Pasajes de avión, golosinas', 'Frutas y verduras (ideal)']


def fig_elast(curvas, color, pref, ejemplos=None):
    o = [f'<div class="elast-row" id="{pref}">']
    for idx, ((nombre, ep, var, q), tr) in enumerate(zip(ELAST, curvas)):
        o.append('  <div class="elast-card">')
        o.append('    ' + mini(tr, color))
        o.append(f'    <b>{nombre}</b>'
                 f'<span class="ep">{ep.replace("Ep", "E<sub>p</sub>")}</span>')
        ej = f'<br /><em>ej.: {ejemplos[idx]}</em>' if ejemplos else ''
        o.append(f'    <small>{var}<br />{q}{ej}</small>')
        o.append('  </div>')
    o.append('</div>')
    return '\n'.join(o)


# ---------------------------------------------------------------- 4. arboles y flujos
def caja(x, y, w, txt, sub=None, color=None, h=None):
    """Caja de arbol/flujo centrada verticalmente en y, con subtitulo opcional."""
    h = h or (44 if sub else 34)
    o = [f'<rect x="{x}" y="{y - h // 2}" width="{w}" height="{h}" rx="8" '
         f'fill="none" stroke="{color or GRID_BOX}" stroke-width="1.5" />']
    if sub:
        o.append(f'<text x="{x + w / 2:.0f}" y="{y - 3}" font-size="13" fill="{INK}" '
                 f'text-anchor="middle">{esc(txt)}</text>')
        o.append(f'<text x="{x + w / 2:.0f}" y="{y + 13}" font-size="10" fill="{MUT}" '
                 f'text-anchor="middle">{esc(sub)}</text>')
    else:
        o.append(f'<text x="{x + w / 2:.0f}" y="{y + 4}" font-size="13" fill="{INK}" '
                 f'text-anchor="middle">{esc(txt)}</text>')
    return '\n    '.join(o)


GRID_BOX = MUT  # trazo de las cajas: el mismo neutro que --linea


def rama(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUT}" fill="none" />'


def fig_ramas_economia():
    """Arbol de tipos y ramas de la economia (reemplaza al mermaid de la
    fuente): positiva (descriptiva, teoria -> micro y macro) y normativa
    (politica economica y sus cuatro politicas)."""
    C0, C1, C2, C3 = 10, 170, 380, 590
    W0, W1, W2, W3 = 120, 170, 170, 170
    o = []
    o.append(caja(C0, 148, W0, 'Economía', color=ACC))
    o.append(caja(C1, 60, W1, 'Economía positiva'))
    o.append(caja(C1, 237, W1, 'Economía normativa'))
    o.append(caja(C2, 30, W2, 'Economía descriptiva'))
    o.append(caja(C2, 90, W2, 'Teoría económica'))
    o.append(caja(C2, 237, W2, 'Política económica'))
    o.append(caja(C3, 67, W3, 'Microeconomía', color=DEM))
    o.append(caja(C3, 113, W3, 'Macroeconomía', color=DEM))
    o.append(caja(C3, 168, W3, 'Política fiscal'))
    o.append(caja(C3, 214, W3, 'Política monetaria'))
    o.append(caja(C3, 260, W3, 'Política exterior'))
    o.append(caja(C3, 306, W3, 'Política de rentas'))
    o.append(rama(C0 + W0, 148, C1, 60))
    o.append(rama(C0 + W0, 148, C1, 237))
    o.append(rama(C1 + W1, 60, C2, 30))
    o.append(rama(C1 + W1, 60, C2, 90))
    o.append(rama(C1 + W1, 237, C2, 237))
    o.append(rama(C2 + W2, 90, C3, 67))
    o.append(rama(C2 + W2, 90, C3, 113))
    for y in (168, 214, 260, 306):
        o.append(rama(C2 + W2, 237, C3, y))
    return svg(o, 770, 340,
               'Arbol de tipos y ramas de la economia: positiva (descriptiva y '
               'teoria economica, que se divide en micro y macro) y normativa '
               '(politica economica: fiscal, monetaria, exterior y de rentas)')


def fig_circuito_contable():
    """Flujo del circuito contable (reemplaza al mermaid de la fuente): del
    hecho economico a los estados contables."""
    o = ['<defs><marker id="fig-cc-flecha" viewBox="0 0 10 10" refX="8" refY="5" '
         'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{MUT}" /></marker></defs>']

    def flecha(x1, y1, x2, y2):
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUT}" '
                'fill="none" marker-end="url(#fig-cc-flecha)" />')

    o.append(caja(10, 90, 150, 'Hecho económico', 'modifica el patrimonio'))
    o.append(caja(200, 90, 160, 'Libro diario', 'orden cronológico'))
    o.append(caja(400, 90, 160, 'Libro mayor', 'saldo por cuenta'))
    o.append(caja(600, 42, 170, 'Balance', 'A = P + PN', color=ACC))
    o.append(caja(600, 138, 170, 'Cuadro de resultados', 'cuentas transitorias', color=ACC))
    o.append(flecha(160, 90, 196, 90))
    o.append(flecha(360, 90, 396, 90))
    o.append(flecha(560, 90, 596, 50))
    o.append(flecha(560, 90, 596, 130))
    o.append(flecha(685, 112, 685, 68))
    o.append(f'<text x="700" y="94" font-size="10" fill="{MUT}">el resultado</text>')
    o.append(f'<text x="700" y="106" font-size="10" fill="{MUT}">pasa al PN</text>')
    return svg(o, 790, 180,
               'Circuito contable: el hecho economico se asienta en el libro '
               'diario, pasa al libro mayor y de ahi salen el balance y el '
               'cuadro de resultados, cuyo resultado alimenta el patrimonio neto')


# ---------------------------------------------------------------- 5. prestamos
P0, TASA, NPER = 1000.0, 0.10, 4


def tabla_frances():
    c = P0 * TASA / (1 - (1 + TASA) ** -NPER)
    saldo, filas = P0, []
    for n in range(1, NPER + 1):
        i = saldo * TASA
        a = c - i
        saldo -= a
        filas.append((n, c, i, a, max(saldo, 0)))
    return filas


def tabla_aleman():
    a = P0 / NPER
    saldo, filas = P0, []
    for n in range(1, NPER + 1):
        i = saldo * TASA
        saldo -= a
        filas.append((n, a + i, i, a, max(saldo, 0)))
    return filas


def tabla_bullet():
    filas = []
    for n in range(1, NPER + 1):
        i = P0 * TASA
        a = P0 if n == NPER else 0.0
        filas.append((n, i + a, i, a, 0.0 if n == NPER else P0))
    return filas


def tabla_directo():
    a, i = P0 / NPER, P0 * TASA
    filas, saldo = [], P0
    for n in range(1, NPER + 1):
        saldo -= a
        filas.append((n, a + i, i, a, max(saldo, 0)))
    return filas


SISTEMAS = [('frances', 'Francés', tabla_frances), ('aleman', 'Alemán', tabla_aleman),
            ('bullet', 'Bullet', tabla_bullet), ('directo', 'Directo', tabla_directo)]

A_COL, I_COL = ACC, OFE
SIS_COL = {'frances': ACC, 'aleman': DEM, 'bullet': RIESGO, 'directo': OFE}


def barras(filas, ymax):
    # escala COMUN a los cuatro sistemas: al cambiar de grafico se ve de un
    # golpe que el bullet dispara la ultima cuota
    w, h, l, b, t = 640, 366, 58, 46, 34
    o = []
    plot_h = h - b - t
    bw = (w - l - 18) / len(filas) * 0.52
    for k in range(0, int(ymax) + 1, 200):
        yy = (h - b) - k / ymax * plot_h
        o.append(f'<line x1="{l}" y1="{yy:.1f}" x2="{w - 18}" y2="{yy:.1f}" stroke="{GRID}" '
                 f'stroke-width="1" stroke-dasharray="2 4" />')
        o.append(f'<text x="{l - 8}" y="{yy + 4:.1f}" font-size="11" fill="{MUT}" '
                 f'text-anchor="end">{k}</text>')
    for idx, (n, c, i, a, s) in enumerate(filas):
        cx = l + (idx + 0.5) * (w - l - 18) / len(filas)
        ha = a / ymax * plot_h
        hi = i / ymax * plot_h
        ya = (h - b) - ha
        yi = ya - hi
        o.append(f'<g><title>Período {n}: cuota ${c:,.2f} = amortización ${a:,.2f} '
                 f'+ interés ${i:,.2f}. Saldo tras pagar: ${s:,.2f}</title>'
                 f'<rect x="{cx - bw / 2:.1f}" y="{ya:.1f}" width="{bw:.1f}" height="{ha:.1f}" '
                 f'fill="{A_COL}" rx="3" />'
                 f'<rect x="{cx - bw / 2:.1f}" y="{yi:.1f}" width="{bw:.1f}" height="{hi:.1f}" '
                 f'fill="{I_COL}" rx="3" />'
                 f'<text x="{cx:.1f}" y="{yi - 7:.1f}" font-size="11.5" fill="{INK}" '
                 f'text-anchor="middle" font-weight="700">{c:,.0f}</text></g>')
        o.append(f'<text x="{cx:.1f}" y="{h - b + 17:.1f}" font-size="11.5" fill="{MUT}" '
                 f'text-anchor="middle">n = {n}</text>')
    o.append(f'<line x1="{l}" y1="{h - b}" x2="{w - 18}" y2="{h - b}" stroke="{INK}" stroke-width="1.6" />')
    o.append(f'<line x1="{l}" y1="{t}" x2="{l}" y2="{h - b}" stroke="{INK}" stroke-width="1.6" />')
    o.append(f'<text x="4" y="12" font-size="12" fill="{INK}" font-weight="600">Cuota ($)</text>')
    return (legend((A_COL, 'Amortización'), (I_COL, 'Interés')) + '\n'
            + svg(o, w, h, 'Composición de cada cuota entre amortización e interés'))


def fig_saldos():
    """Saldo de deuda periodo a periodo para los cuatro sistemas.

    Es la comparacion que realmente importa: al refinanciar, lo que te queda
    debiendo.
    """
    p = Plot(w=680, h=380, xmax=4.0, ymax=1000.0)
    o = p.frame('Período', 'Saldo de deuda ($)', [0, 1, 2, 3, 4],
                [0, 250, 500, 750, 1000], '{:.0f}')
    # aleman y directo dan EXACTAMENTE el mismo saldo (ambos amortizan P/n),
    # asi que el directo va punteado para que no quede tapado
    for slug, nombre, fn in SISTEMAS:
        filas = fn()
        pts = [(0, P0)] + [(n, s) for n, c, i, a, s in filas]
        col = SIS_COL[slug]
        o.append(p.polyline(pts, col, 3.4 if slug == 'directo' else 2.6,
                            '7 5' if slug == 'directo' else None))
        if slug != 'directo':
            for q, val in pts:
                o.append(f'<circle cx="{p.x(q):.1f}" cy="{p.y(val):.1f}" r="4" fill="{col}" />')
    # marca del momento de refinanciacion
    xx = p.x(3)
    o.append(f'<line x1="{xx:.1f}" y1="{p.t:.1f}" x2="{xx:.1f}" y2="{p.y(0):.1f}" '
             f'stroke="{INK}" stroke-width="1.4" stroke-dasharray="5 4" />')
    o.append(f'<text x="{xx - 8:.1f}" y="{p.t + 14:.1f}" font-size="11.5" fill="{INK}" '
             f'text-anchor="end" font-weight="600">tras 3 de 4 cuotas</text>')
    # arriba de la linea roja hay lugar libre; a la derecha se salia del viewBox
    o.append(f'<text x="{p.x(0.15):.1f}" y="{p.y(1000) - 9:.1f}" font-size="11.5" '
             f'fill="{SIS_COL["bullet"]}" font-weight="700">bullet: seguís debiendo TODO</text>')
    o.append(f'<text x="{p.x(3.06):.1f}" y="{p.y(250) - 8:.1f}" font-size="11.5" '
             f'fill="{SIS_COL["aleman"]}" font-weight="700">alemán y directo: sólo $250</text>')
    return (legend((SIS_COL['frances'], 'Francés'), (SIS_COL['aleman'], 'Alemán'),
                   (SIS_COL['bullet'], 'Bullet'), (SIS_COL['directo'], 'Directo (punteado)'))
            + '\n' + svg(o, 680, 380, 'Saldo de deuda de los cuatro sistemas de amortización'))


def money(v):
    return f'{v:,.2f}'.replace(',', '@').replace('.', ',').replace('@', '.')


def tabla_html(filas):
    # <table> pelada: armar.py la envuelve en .table-wrap como a cualquier otra
    o = ['<table>',
         '<thead><tr><th>n</th><th>Cuota</th><th>Interés</th><th>Amortización</th>'
         '<th>Saldo</th></tr></thead>', '<tbody>']
    tc = ti = ta = 0.0
    for n, c, i, a, s in filas:
        tc, ti, ta = tc + c, ti + i, ta + a
        o.append(f'<tr><td>{n}</td><td>${money(c)}</td><td>${money(i)}</td>'
                 f'<td>${money(a)}</td><td>${money(s)}</td></tr>')
    o.append(f'<tr><td><b>Σ</b></td><td><b>${money(tc)}</b></td>'
             f'<td><b>${money(ti)}</b></td><td><b>${money(ta)}</b></td>'
             f'<td></td></tr>')
    o += ['</tbody>', '</table>']
    return '\n'.join(o)


def main():
    os.makedirs(OUT, exist_ok=True)
    w = {}
    w['schedules.html'] = fig_schedules()
    w['equilibrio.html'] = fig_equilibrio(False)
    w['equilibrio-shift.html'] = fig_equilibrio(True)
    w['elast-demanda.html'] = fig_elast(CURVAS_D, DEM, 'elast-d', EJEMPLOS_D)
    w['elast-oferta.html'] = fig_elast(CURVAS_O, OFE, 'elast-o')

    w['ramas-economia.html'] = fig_ramas_economia()
    w['circuito-contable.html'] = fig_circuito_contable()

    w['amort-saldos.html'] = fig_saldos()

    ymax = 1200.0
    for slug, nombre, fn in SISTEMAS:
        filas = fn()
        w[f'amort-{slug}.html'] = barras(filas, ymax)
        w[f'amort-{slug}-tabla.html'] = tabla_html(filas)

    for k, v in w.items():
        with open(os.path.join(OUT, k), 'w', encoding='utf-8', newline='\n') as f:
            f.write(v + '\n')
        print(f'  {k}  ({len(v)} chars)')

    print('\nResumen numérico del ejemplo de préstamos '
          f'(P={P0:.0f}, i={TASA:.0%}, n={NPER}):')
    for slug, nombre, fn in SISTEMAS:
        filas = fn()
        ti = sum(r[2] for r in filas)
        am3 = sum(r[3] for r in filas[:3])
        print(f'  {nombre:<9} interés total ${money(ti):>9} | '
              f'amortizado tras 3 cuotas ${money(am3):>9}')


if __name__ == '__main__':
    main()
