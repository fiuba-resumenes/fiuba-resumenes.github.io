#!/usr/bin/env python3
"""Genera las figuras SVG del apunte de CDD (fuentes/cdd/figuras/*.html).

Es el generador de graficos de la guia de Ciencia de Datos de echepereza
adaptado a este repo: en vez de la paleta fija azul + teal, los SVG salen con
los alias de tokens del contrato (currentColor, --acc, --acc2, --acc3, --acc4,
--linea, --grid), asi que se ven bien en cualquier materia y en los dos temas
sin tocar nada. Los tooltips CSS del original (.hv/.tip, que dependian del CSS
de aquella guia) se reemplazan por <title> nativo, como en las demas figuras
del repo, y la leyenda va en el <div class="legend"> comun.

Los fragmentos las referencian con <!--FIG:nombre--> y armar.py las inyecta
dentro de figure.diag y las valida en cada build (ver contrato-fragmento.md).
El resultado esta commiteado: este script solo hay que correrlo si se cambia
una figura.

Datos: los graficos con valores impresos en la fuente los conservan tal cual
(box plot, pie, stacked bar, heatmap, line, lollipop, radar, codo, venn); los
que la fuente generaba con numpy (violin, scatter, dendograma, voronoi) usan
un dataset representativo equivalente generado con la stdlib (random + math),
para que el script corra sin dependencias.

Uso:  python3 fuentes/gen_figuras_cdd.py   (reescribe fuentes/cdd/figuras/)
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cdd', 'figuras')

# Paleta por tokens: INK hereda la tinta del tema via figure.diag.
INK, MUT, GRID = 'currentColor', 'var(--linea)', 'var(--grid)'
ACC, ACC2, ACC3, ACC4 = 'var(--acc)', 'var(--acc2)', 'var(--acc3)', 'var(--acc4)'
CAT4 = [ACC, ACC2, ACC3, ACC4]
# seis series con cuatro tokens: los dos ultimos repiten acc/acc2 atenuados
CAT6 = [(ACC, None), (ACC2, None), (ACC3, None), (ACC4, None),
        (ACC, 0.55), (ACC2, 0.55)]

# ---------------------------------------------------------------- helpers


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def f(v):
    """Formatea un numero para el atributo SVG, sin decimales de mas."""
    return ('%.2f' % v).rstrip('0').rstrip('.')


def tit(*lines):
    """Tooltip nativo: la primera linea con ':', el resto separado con ';'."""
    lines = [l for l in lines if l]
    txt = lines[0] if len(lines) == 1 else lines[0] + ': ' + '; '.join(lines[1:])
    return '<title>%s</title>' % esc(txt)


def legend(*items):
    """Leyenda de series: pares (color, rotulo). Va dentro de la figura."""
    spans = ''.join('<span><i style="background:%s"></i>%s</span>' % (c, esc(t))
                    for c, t in items)
    return '<div class="legend">%s</div>' % spans


def svg(inner, w, h, label):
    return ('<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" '
            'role="img" aria-label="%s">\n    ' % (w, h, esc(label))
            + '\n    '.join(inner) + '\n  </svg>')


def axes(W, H, L, R, T, B, xlab='', ylab='', yticks=(), xticks=()):
    """Marco comun: grilla horizontal, eje x y etiquetas."""
    o = []
    x0, x1, y1 = L, W - R, H - B
    for val, ypx in yticks:
        o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
                 'stroke-width="1" stroke-dasharray="2 4" />'
                 % (f(x0), f(ypx), f(x1), f(ypx), GRID))
        o.append('<text x="%s" y="%s" font-size="11" fill="%s" '
                 'text-anchor="end">%s</text>' % (f(x0 - 8), f(ypx + 4), MUT, esc(val)))
    o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.6" />'
             % (f(x0), f(y1), f(x1), f(y1), INK))
    for val, xpx in xticks:
        o.append('<text x="%s" y="%s" font-size="11" fill="%s" '
                 'text-anchor="middle">%s</text>' % (f(xpx), f(y1 + 18), MUT, esc(val)))
    if xlab:
        o.append('<text x="%s" y="%s" font-size="12" fill="%s" font-weight="600" '
                 'text-anchor="middle">%s</text>'
                 % (f((x0 + x1) / 2), f(H - 6), INK, esc(xlab)))
    if ylab:
        o.append('<text transform="translate(13 %s) rotate(-90)" font-size="12" '
                 'fill="%s" font-weight="600" text-anchor="middle">%s</text>'
                 % (f((T + y1) / 2), INK, esc(ylab)))
    return o


def percentile(sorted_vals, p):
    idx = (len(sorted_vals) - 1) * p / 100.0
    lo = int(math.floor(idx))
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (idx - lo) * (sorted_vals[hi] - sorted_vals[lo])


# ================================================================ 01 box plot
# datos leidos de la captura de la fuente (Boxplot of Score)
def box_plot():
    W, H, L, R, T, B = 720, 380, 58, 20, 20, 52
    data = [
        ('Method 1', 18.0, 21.5, 24.8, 28.2, 31.5, []),
        ('Method 2', 20.0, 23.3, 25.2, 27.0, 30.0, [35.0]),
        ('Method 3', 10.0, 19.5, 28.1, 31.8, 38.8, []),
        ('Method 4', 23.4, 29.4, 31.5, 36.1, 39.6, []),
    ]
    lo, hi = 8, 41
    y1 = H - B
    sy = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - T)
    yt = [(str(v), sy(v)) for v in range(10, 41, 5)]
    xs = [L + (i + 0.5) * (W - R - L) / len(data) for i in range(len(data))]
    bw = 62

    o = axes(W, H, L, R, T, B, 'Teaching Method', 'Score', yt,
             [(d[0], x) for d, x in zip(data, xs)])
    for i, ((lab, mn, q1, med, q3, mx, outs), x) in enumerate(zip(data, xs)):
        c = CAT4[i]
        o.append('<g>' + tit(lab, 'máx %.1f, Q3 %.1f' % (mx, q3),
                             'mediana %.1f' % med, 'Q1 %.1f, mín %.1f' % (q1, mn)))
        for xa, ya, xb, yb in ((x, sy(mn), x, sy(mx)),
                               (x - 16, sy(mn), x + 16, sy(mn)),
                               (x - 16, sy(mx), x + 16, sy(mx))):
            o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
                     'stroke-width="1.6" />' % (f(xa), f(ya), f(xb), f(yb), MUT))
        o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="%s" '
                 'fill-opacity="0.55" stroke="%s" stroke-width="1.6" />'
                 % (f(x - bw / 2), f(sy(q3)), f(bw), f(sy(q1) - sy(q3)), c, c))
        o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
                 'stroke-width="2.6" />'
                 % (f(x - bw / 2), f(sy(med)), f(x + bw / 2), f(sy(med)), c))
        for ov in outs:
            o.append('<circle cx="%s" cy="%s" r="4" fill="none" stroke="%s" '
                     'stroke-width="1.8" />' % (f(x), f(sy(ov)), ACC4))
            o.append('<text x="%s" y="%s" font-size="10.5" fill="%s" '
                     'text-anchor="middle">outlier</text>' % (f(x), f(sy(ov) - 9), ACC4))
        o.append('</g>')
    return svg(o, W, H,
               'Box plot del score por método de enseñanza, con los cuartiles '
               'de cada grupo')


# ================================================================ 02 violin
# split violin: edad por clase, partido segun sobrevivio (dataset representativo)
def _kde(samples, grid, bw):
    k = 1.0 / (len(samples) * bw * math.sqrt(2 * math.pi))
    out = []
    for g in grid:
        s = 0.0
        for x in samples:
            d = (g - x) / bw
            s += math.exp(-0.5 * d * d)
        out.append(s * k)
    return out


def violin():
    W, H, L, R, T, B = 720, 400, 58, 20, 22, 56
    rng = random.Random(7)
    # mezclas elegidas para reproducir las medianas visibles en la captura
    spec = [
        ('First', [(42, 13, .7), (22, 7, .3)], [(34, 14, .75), (9, 6, .25)]),
        ('Second', [(31, 11, .85), (10, 6, .15)], [(27, 13, .7), (6, 5, .3)]),
        ('Third', [(26, 10, .9), (8, 5, .10)], [(23, 10, .75), (7, 5, .25)]),
    ]
    lo, hi = -8, 88
    y1 = H - B
    sy = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - T)
    grid = [lo + i * (hi - lo) / 129.0 for i in range(130)]
    yt = [(str(v), sy(v)) for v in range(0, 81, 20)]
    xs = [L + (i + 0.5) * (W - R - L) / len(spec) for i in range(len(spec))]
    half = 74

    def draw(comps, x, side):
        s = []
        for mu, sd, wgt in comps:
            s += [rng.gauss(mu, sd) for _ in range(int(1400 * wgt))]
        s = [v for v in s if lo < v < hi]
        dens = _kde(s, grid, 4.2)
        dmax = max(dens)
        pts = ['%s,%s' % (f(x + side * d / dmax * half), f(sy(g)))
               for g, d in zip(grid, dens)]
        s.sort()
        med = percentile(s, 50)
        q1, q3 = percentile(s, 25), percentile(s, 75)
        path = ('M%s,%s L' % (f(x), f(sy(grid[0]))) + ' '.join(pts)
                + ' L%s,%s Z' % (f(x), f(sy(grid[-1]))))
        return path, med, q1, q3

    o = axes(W, H, L, R, T, B, 'class', 'age', yt,
             [(s[0], x) for s, x in zip(spec, xs)])
    for (lab, comps_no, comps_yes), x in zip(spec, xs):
        for side, comps, color, sname in ((-1, comps_no, ACC, 'no sobrevivió'),
                                          (1, comps_yes, ACC2, 'sí sobrevivió')):
            path, med, q1, q3 = draw(comps, x, side)
            o.append('<g>' + tit('%s, %s' % (lab, sname),
                                 'mediana %.0f años' % med,
                                 'Q1 %.0f, Q3 %.0f' % (q1, q3)))
            o.append('<path d="%s" fill="%s" fill-opacity="0.5" stroke="%s" '
                     'stroke-width="1.5" />' % (path, color, color))
            o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
                     'stroke-width="2" stroke-dasharray="4 3" />'
                     % (f(x), f(sy(med)), f(x + side * half * .55), f(sy(med)), color))
            o.append('</g>')
    return (legend((ACC, 'no sobrevivió'), (ACC2, 'sí sobrevivió')) + '\n'
            + svg(o, W, H, 'Violin plot de la edad por clase, partido según '
                           'si sobrevivió'))


# ================================================================ 03 pie
# porcentajes exactos de la captura; los rotulos van AFUERA de las porciones
# para que currentColor siga legible en los dos temas
def pie():
    W, H = 720, 400
    data = [('Children 0-18', 23.59), ('Seniors 65+', 16.53), ('Adults 55-64', 13.18),
            ('Adults 35-54', 25.52), ('Adults 26-34', 12.47), ('Adults 19-25', 8.71)]
    cx, cy, r = 250, 200, 138
    o = []
    ang = -math.pi / 2
    for i, (lab, pct) in enumerate(data):
        col, op = CAT6[i]
        sweep = pct / 100 * 2 * math.pi
        a0, a1 = ang, ang + sweep
        mid = (a0 + a1) / 2
        # la porcion destacada se separa del centro, como en el original
        off = 14 if lab == 'Adults 55-64' else 0
        ox, oy = cx + math.cos(mid) * off, cy + math.sin(mid) * off
        x0, y0 = ox + r * math.cos(a0), oy + r * math.sin(a0)
        x1, y1 = ox + r * math.cos(a1), oy + r * math.sin(a1)
        large = 1 if sweep > math.pi else 0
        d = ('M%s,%s L%s,%s A%s,%s 0 %d 1 %s,%s Z'
             % (f(ox), f(oy), f(x0), f(y0), f(r), f(r), large, f(x1), f(y1)))
        opat = '' if op is None else ' fill-opacity="%s"' % f(op)
        o.append('<g>' + tit(lab, '%.2f %% del total' % pct))
        o.append('<path d="%s" fill="%s"%s stroke="%s" stroke-width="1.5" />'
                 % (d, col, opat, GRID))
        lx = ox + math.cos(mid) * (r + 20)
        ly = oy + math.sin(mid) * (r + 20)
        o.append('<text x="%s" y="%s" font-size="11.5" font-weight="700" fill="%s" '
                 'text-anchor="middle">%s%%</text>'
                 % (f(lx), f(ly + 4), INK, '%.2f' % pct))
        o.append('</g>')
        ang = a1
    # leyenda al costado
    for i, (lab, pct) in enumerate(data):
        col, op = CAT6[i]
        yy = 74 + i * 30
        opat = '' if op is None else ' fill-opacity="%s"' % f(op)
        o.append('<rect x="470" y="%s" width="13" height="13" rx="3" fill="%s"%s />'
                 % (f(yy), col, opat))
        o.append('<text x="492" y="%s" font-size="12.5" fill="%s">%s</text>'
                 % (f(yy + 11), INK, esc(lab)))
        o.append('<text x="700" y="%s" font-size="12" fill="%s" '
                 'text-anchor="end">%.2f%%</text>' % (f(yy + 11), MUT, pct))
    return svg(o, W, H,
               'Pie chart de la distribución de la población por franja etaria')


# ================================================================ 04 stacked bar
def stacked_bar():
    W, H, L, R, T, B = 720, 400, 58, 20, 26, 56
    cats = ['A', 'B', 'C', 'D']
    segs = ['Segmento 1', 'Segmento 2', 'Segmento 3', 'Segmento 4']
    vals = [[270, 115, 295, 205], [165, 145, 180, 135],
            [100, 85, 85, 205], [205, 180, 110, 205]]
    y1 = H - B
    sy = lambda v: y1 - v / 1000.0 * (y1 - T)
    yt = [(str(v), sy(v)) for v in range(0, 1001, 200)]
    xs = [L + (i + 0.5) * (W - R - L) / len(cats) for i in range(len(cats))]
    bw = 78

    o = axes(W, H, L, R, T, B, '', 'Valor', yt, [(c, x) for c, x in zip(cats, xs)])
    for ci, (cname, x) in enumerate(zip(cats, xs)):
        total = sum(vals[ci])
        acc = 0
        for si in range(len(segs)):
            v = vals[ci][si]
            yb, ya = sy(acc), sy(acc + v)
            o.append('<g>' + tit('%s, %s' % (cname, segs[si]),
                                 '%d (%.0f %% de la barra)' % (v, 100.0 * v / total)))
            o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" />'
                     % (f(x - bw / 2), f(ya), f(bw), f(yb - ya), CAT4[si]))
            o.append('</g>')
            acc += v
        o.append('<text x="%s" y="%s" font-size="12" font-weight="700" fill="%s" '
                 'text-anchor="middle">%d</text>' % (f(x), f(sy(total) - 8), INK, total))
    return (legend(*[(CAT4[i], s) for i, s in enumerate(segs)]) + '\n'
            + svg(o, W, H, 'Barras apiladas de cuatro categorías con cuatro '
                           'segmentos cada una'))


# ================================================================ 05 scatter
# Palmer penguins: dataset representativo generado con normales correlacionadas
def scatter():
    W, H, L, R, T, B = 720, 420, 62, 20, 24, 56
    rng = random.Random(3)
    groups = [
        ('Adelie', 190.0, 6.5, 3700.0, 460.0, 0.45, ACC2, 132),
        ('Chinstrap', 196.0, 7.2, 3733.0, 385.0, 0.42, ACC3, 60),
        ('Gentoo', 217.0, 6.5, 5076.0, 500.0, 0.62, ACC, 110),
    ]
    xlo, xhi, ylo, yhi = 168, 234, 2600, 6500
    x0, x1, y1 = L, W - R, H - B
    sx = lambda v: x0 + (v - xlo) / (xhi - xlo) * (x1 - x0)
    sy = lambda v: y1 - (v - ylo) / (yhi - ylo) * (y1 - T)
    yt = [(str(v), sy(v)) for v in range(3000, 6001, 1000)]
    xt = [(str(v), sx(v)) for v in range(170, 231, 10)]

    o = axes(W, H, L, R, T, B, 'Flipper length (mm)', 'Body mass (g)', yt, xt)
    for name, mx, sdx, my, sdy, rho, col, n in groups:
        for _ in range(n):
            z1, z2 = rng.gauss(0, 1), rng.gauss(0, 1)
            px = mx + sdx * z1
            py = my + sdy * (rho * z1 + math.sqrt(1 - rho * rho) * z2)
            if not (xlo < px < xhi and ylo < py < yhi):
                continue
            o.append('<circle cx="%s" cy="%s" r="4.4" fill="%s">'
                     '%s</circle>'
                     % (f(sx(px)), f(sy(py)), col,
                        tit('%s: %.0f mm, %.0f g' % (name, px, py))))
    return (legend(*[(g[6], g[0]) for g in groups]) + '\n'
            + svg(o, W, H, 'Scatter plot de largo de aleta contra masa corporal '
                           'para tres especies de pingüino'))


# ================================================================ 06 heatmap
# los 49 valores exactos de la captura; la rampa secuencial es un solo token
# con fill-opacity creciente, asi respeta la paleta de cada materia
def _op(t):
    """Opacidad de la rampa secuencial: casi transparente -> casi pleno."""
    t = max(0.0, min(1.0, t))
    return 0.05 + 0.80 * (t ** 0.85)


def heatmap():
    W, H = 720, 500
    rows = ['cucumber', 'tomato', 'lettuce', 'asparagus', 'potato', 'wheat', 'barley']
    cols = ['Farmer Joe', 'Upland Bros.', 'Smith Gardening', 'Agrifun',
            'Organiculture', 'BioGoods Ltd.', 'Cornylee Corp.']
    V = [[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
         [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
         [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
         [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
         [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
         [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
         [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]]
    L, T = 118, 20
    cw, ch = 78, 44
    vmax = max(max(r) for r in V)
    o = []
    # etiquetas de columna a 45 grados y ancladas al final: cuelgan hacia
    # abajo-izquierda sin pisarse entre si
    for j, c in enumerate(cols):
        o.append('<text transform="translate(%s %s) rotate(-45)" font-size="11" '
                 'fill="%s" text-anchor="end">%s</text>'
                 % (f(L + j * cw + cw / 2 + 6), f(T + 7 * ch + 16), MUT, esc(c)))
    for i, rname in enumerate(rows):
        o.append('<text x="%s" y="%s" font-size="11" fill="%s" '
                 'text-anchor="end">%s</text>'
                 % (f(L - 10), f(T + i * ch + ch / 2 + 4), MUT, esc(rname)))
        for j, cname in enumerate(cols):
            v = V[i][j]
            x, y = L + j * cw, T + i * ch
            o.append('<g>' + tit('%s × %s' % (rname, cname), '%.1f toneladas/año' % v))
            o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" '
                     'fill-opacity="%s" />'
                     % (f(x), f(y), f(cw - 2), f(ch - 2), ACC, f(_op(v / vmax))))
            o.append('<text x="%s" y="%s" font-size="11.5" font-weight="600" '
                     'fill="%s" text-anchor="middle">%.1f</text>'
                     % (f(x + (cw - 2) / 2), f(y + ch / 2 + 4), INK, v))
            o.append('</g>')
    # escala de color
    sx0, sy0 = L, T + 7 * ch + 128
    for k in range(60):
        o.append('<rect x="%s" y="%s" width="5" height="12" fill="%s" '
                 'fill-opacity="%s" />' % (f(sx0 + k * 5), f(sy0), ACC, f(_op(k / 59.0))))
    o.append('<text x="%s" y="%s" font-size="11" fill="%s" '
             'text-anchor="end">0</text>' % (f(sx0 - 8), f(sy0 + 10), MUT))
    o.append('<text x="%s" y="%s" font-size="11" fill="%s">%.1f t/año</text>'
             % (f(sx0 + 308), f(sy0 + 10), MUT, vmax))
    return svg(o, W, H,
               'Heatmap de la cosecha por producto y productor, en toneladas por año')


# ================================================================ 07 line plot
# valores exactos de la captura
def line_plot():
    W, H, L, R, T, B = 720, 400, 62, 20, 26, 56
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep',
              'Oct', 'Nov', 'Dic']
    series = [
        ('Producto A', [1000, 1500, 1200, 2000, 1800, 2200, 1500, 1800, 2000,
                        2300, 1900, 2100], ACC),
        ('Producto B', [800, 1200, 1500, 1800, 2000, 2300, 1600, 1900, 2200,
                        2500, 1800, 2000], ACC2),
        ('Producto C', [1200, 1300, 1100, 1400, 1600, 1900, 1300, 1500, 1700,
                        1900, 1500, 1700], ACC3),
    ]
    lo, hi = 700, 2600
    x0, x1, y1 = L, W - R, H - B
    sx = lambda i: x0 + i * (x1 - x0) / (len(months) - 1)
    sy = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - T)
    yt = [(str(v), sy(v)) for v in range(750, 2501, 250)]
    xt = [(m, sx(i)) for i, m in enumerate(months)]

    o = axes(W, H, L, R, T, B, 'Mes', 'Ventas ($100K)', yt, xt)
    for name, vals, col in series:
        pts = ' '.join('%s,%s' % (f(sx(i)), f(sy(v))) for i, v in enumerate(vals))
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.6" '
                 'stroke-linecap="round" />' % (pts, col))
        for i, v in enumerate(vals):
            o.append('<circle cx="%s" cy="%s" r="4" fill="%s">%s</circle>'
                     % (f(sx(i)), f(sy(v)), col,
                        tit('%s: %s, %d' % (name, months[i], v))))
    return (legend(*[(s[2], s[0]) for s in series]) + '\n'
            + svg(o, W, H, 'Line plot de las ventas mensuales de tres productos'))


# ================================================================ 08 lollipop
def lollipop():
    W, H, L, R, T, B = 720, 360, 52, 18, 24, 50
    labels = [chr(ord('A') + i) for i in range(26)]
    vals = [0.76, 0.18, 0.39, 1.68, 0.03, 0.27, 0.27, 1.05, 1.47, 0.70, 0.91,
            0.18, 0.31, 1.94, 0.28, 0.02, 1.30, 0.20, 0.24, 0.36, 0.71, 0.32,
            0.07, 0.57, 1.00, 0.09]
    x0, x1, y1 = L, W - R, H - B
    sx = lambda i: x0 + (i + 0.5) * (x1 - x0) / len(labels)
    sy = lambda v: y1 - v / 2.05 * (y1 - T)
    yt = [('%.1f' % v, sy(v)) for v in (0.0, 0.5, 1.0, 1.5, 2.0)]
    xt = [(l, sx(i)) for i, l in enumerate(labels)]
    o = axes(W, H, L, R, T, B, 'x', 'y', yt, xt)
    for i, v in enumerate(vals):
        o.append('<g>' + tit('%s = %.2f' % (labels[i], v)))
        o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
                 'stroke-width="2" />' % (f(sx(i)), f(sy(0)), f(sx(i)), f(sy(v)), MUT))
        o.append('<circle cx="%s" cy="%s" r="5" fill="%s" />'
                 % (f(sx(i)), f(sy(v)), ACC))
        o.append('</g>')
    return svg(o, W, H, 'Lollipop plot con un valor por cada letra del alfabeto')


# ================================================================ 09 venn
# 4 conjuntos, como el original "Cooking Bacon"
def venn():
    W, H = 720, 430
    cx, cy, r = 360, 205, 118
    d = 78
    sets = [('Smoke', cx - d, cy - d, ACC), ('Fat', cx + d, cy - d, ACC2),
            ('Salt', cx - d, cy + d, ACC3), ('Meat', cx + d, cy + d, ACC4)]
    inter = [('Cuban Cigar', cx, cy - d - 22), ('Smoked Salt', cx - d - 26, cy),
             ('Pork Belly', cx + d + 26, cy), ('Corned Beef', cx, cy + d + 22)]
    o = []
    for name, x, y, col in sets:
        o.append('<g>' + tit(name, 'las regiones compartidas son las intersecciones'))
        o.append('<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="0.38" '
                 'stroke="%s" stroke-width="2" />' % (f(x), f(y), f(r), col, col))
        lx = x + (-1 if x < cx else 1) * (r * .58)
        ly = y + (-1 if y < cy else 1) * (r * .58)
        o.append('<text x="%s" y="%s" font-size="14" font-weight="700" fill="%s" '
                 'text-anchor="middle">%s</text>' % (f(lx), f(ly), col, esc(name)))
        o.append('</g>')
    for name, x, y in inter:
        o.append('<text x="%s" y="%s" font-size="11.5" fill="%s" '
                 'text-anchor="middle">%s</text>' % (f(x), f(y + 4), INK, esc(name)))
    o.append('<text x="%s" y="%s" font-size="15" font-weight="800" fill="%s" '
             'text-anchor="middle">Bacon!</text>' % (f(cx), f(cy + 5), INK))
    o.append('<text x="%s" y="%s" font-size="11" fill="%s" text-anchor="middle">'
             'el centro es la intersección de los cuatro conjuntos</text>'
             % (f(cx), f(H - 12), MUT))
    return svg(o, W, H,
               'Diagrama de Venn de cuatro conjuntos con sus intersecciones nombradas')


# ================================================================ 10 radar
def radar():
    W, H = 720, 420
    axes_ = ['Dribbling', 'Passing', 'Shooting', 'Defending', 'Speed', 'Physical']
    vals = [92, 78, 74, 42, 88, 65]
    cx, cy, R = 300, 215, 148
    n = len(axes_)
    ang = lambda i: -math.pi / 2 + i * 2 * math.pi / n
    o = []
    for ring in (25, 50, 75, 100):
        pts = ' '.join('%s,%s' % (f(cx + math.cos(ang(i)) * R * ring / 100),
                                  f(cy + math.sin(ang(i)) * R * ring / 100))
                       for i in range(n))
        o.append('<polygon points="%s" fill="none" stroke="%s" '
                 'stroke-width="1" />' % (pts, GRID))
        # a la izquierda del eje vertical: sobre el eje se pisaban con el vertice
        o.append('<text x="%s" y="%s" font-size="10.5" fill="%s" '
                 'text-anchor="end">%d</text>'
                 % (f(cx - 7), f(cy - R * ring / 100 + 12), MUT, ring))
    for i, a in enumerate(axes_):
        x, y = cx + math.cos(ang(i)) * R, cy + math.sin(ang(i)) * R
        o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
                 'stroke-width="1" />' % (f(cx), f(cy), f(x), f(y), GRID))
        lx, ly = cx + math.cos(ang(i)) * (R + 26), cy + math.sin(ang(i)) * (R + 26)
        anchor = 'middle' if abs(lx - cx) < 12 else ('start' if lx > cx else 'end')
        o.append('<text x="%s" y="%s" font-size="12.5" font-weight="600" fill="%s" '
                 'text-anchor="%s">%s</text>' % (f(lx), f(ly + 4), INK, anchor, esc(a)))
    pts = ' '.join('%s,%s' % (f(cx + math.cos(ang(i)) * R * vals[i] / 100),
                              f(cy + math.sin(ang(i)) * R * vals[i] / 100))
                   for i in range(n))
    o.append('<polygon points="%s" fill="%s" fill-opacity="0.38" stroke="%s" '
             'stroke-width="2.4" />' % (pts, ACC, ACC))
    for i, v in enumerate(vals):
        x = cx + math.cos(ang(i)) * R * v / 100
        y = cy + math.sin(ang(i)) * R * v / 100
        o.append('<circle cx="%s" cy="%s" r="5" fill="%s">%s</circle>'
                 % (f(x), f(y), ACC, tit('%s: %d / 100' % (axes_[i], v))))
    for i, (a, v) in enumerate(zip(axes_, vals)):
        yy = 100 + i * 32
        o.append('<text x="524" y="%s" font-size="12.5" fill="%s">%s</text>'
                 % (f(yy), INK, esc(a)))
        o.append('<rect x="524" y="%s" width="60" height="8" rx="4" fill="%s" '
                 'fill-opacity="0.28" />' % (f(yy + 6), ACC))
        o.append('<rect x="524" y="%s" width="%s" height="8" rx="4" fill="%s" />'
                 % (f(yy + 6), f(max(v * .60, 4)), ACC))
        o.append('<text x="598" y="%s" font-size="12" fill="%s">%d</text>'
                 % (f(yy + 14), MUT, v))
    return svg(o, W, H, 'Radar chart del perfil de un jugador sobre seis atributos')


# ================================================================ 11 dendograma
# clustering jerarquico average-linkage calculado aca (dataset representativo)
def dendograma():
    W, H, L, R, T, B = 720, 400, 56, 20, 24, 62
    rng = random.Random(11)
    centers = [(1.0, 1.0), (5.2, 1.4), (3.0, 5.0)]
    pts = [(rng.gauss(cx, 0.55), rng.gauss(cy, 0.55))
           for cx, cy in centers for _ in range(5)]
    names = ['p%d' % (i + 1) for i in range(len(pts))]

    def dist(p, q):
        return math.hypot(p[0] - q[0], p[1] - q[1])

    # average linkage a mano
    clusters = {i: [i] for i in range(len(pts))}
    heights, merges = {}, []
    nxt = len(pts)
    while len(clusters) > 1:
        best, bi, bj = None, None, None
        keys = list(clusters)
        for a in range(len(keys)):
            for b in range(a + 1, len(keys)):
                ia, ib = keys[a], keys[b]
                ds = [dist(pts[p], pts[q])
                      for p in clusters[ia] for q in clusters[ib]]
                d = sum(ds) / len(ds)
                if best is None or d < best:
                    best, bi, bj = d, ia, ib
        merges.append((nxt, bi, bj, best))
        clusters[nxt] = clusters[bi] + clusters[bj]
        heights[nxt] = best
        del clusters[bi], clusters[bj]
        nxt += 1

    # posiciones: hojas en el orden en que quedan agrupadas
    order = []

    def walk(node):
        if node < len(pts):
            order.append(node)
            return
        _, a, b, _ = next(m for m in merges if m[0] == node)
        walk(a)
        walk(b)

    walk(merges[-1][0])
    xpos = {leaf: L + (k + 0.5) * (W - R - L) / len(order)
            for k, leaf in enumerate(order)}
    hmax = max(heights.values()) * 1.08
    y1 = H - B
    sy = lambda h: y1 - h / hmax * (y1 - T)
    for nid, a, b, d in merges:
        xpos[nid] = (xpos[a] + xpos[b]) / 2

    yt = [('%.1f' % (hmax * k / 4), sy(hmax * k / 4)) for k in range(5)]
    o = axes(W, H, L, R, T, B, '', 'distancia de fusión', yt,
             [(names[l], xpos[l]) for l in order])
    cols = [ACC, ACC2, ACC3]
    members = {i: 1 for i in range(len(pts))}
    for k, (nid, a, b, d) in enumerate(merges):
        ya, yb, yd = sy(heights.get(a, 0.0)), sy(heights.get(b, 0.0)), sy(d)
        members[nid] = members[a] + members[b]
        # las fusiones altas (la estructura de arriba) van en tinta neutra
        col = INK if d >= hmax * .55 else cols[k % 3]
        o.append('<g>' + tit('fusión a distancia %.2f' % d,
                             'cluster de %d elementos' % members[nid]))
        o.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%s" fill="none" stroke="%s" '
                 'stroke-width="2.2" />'
                 % (f(xpos[a]), f(ya), f(xpos[a]), f(yd), f(xpos[b]), f(yd),
                    f(xpos[b]), f(yb), col))
        o.append('<circle cx="%s" cy="%s" r="4.5" fill="%s" />'
                 % (f(xpos[nid]), f(yd), col))
        o.append('</g>')
    o.append('<text x="%s" y="%s" font-size="11" fill="%s" text-anchor="middle">'
             'cortando a distinta altura salen distintas cantidades de clusters</text>'
             % (f(W / 2), f(H - 8), MUT))
    return svg(o, W, H, 'Dendograma de quince puntos agrupados por average linkage')


# ================================================================ 12 voronoi
# sin scipy: se recorta el rectangulo con semiplanos (Sutherland-Hodgman)
def _clip(poly, a, b):
    """Deja la parte del poligono mas cerca de `a` que de `b`."""
    mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
    nx, ny = b[0] - a[0], b[1] - a[1]
    inside = lambda p: (p[0] - mx) * nx + (p[1] - my) * ny <= 0
    out = []
    for i in range(len(poly)):
        cur, prv = poly[i], poly[i - 1]
        ic, ip = inside(cur), inside(prv)
        if ic != ip:
            dx, dy = cur[0] - prv[0], cur[1] - prv[1]
            den = nx * dx + ny * dy
            if abs(den) > 1e-12:
                t = (nx * (mx - prv[0]) + ny * (my - prv[1])) / den
                out.append((prv[0] + t * dx, prv[1] + t * dy))
        if ic:
            out.append(cur)
    return out


def voronoi():
    W, H = 720, 400
    pad = 14
    x0, y0, x1, y1 = pad, pad, W - pad, H - 46
    rng = random.Random(5)
    k = 14
    sites = [(rng.uniform(x0 + 22, x1 - 22), rng.uniform(y0 + 22, y1 - 22))
             for _ in range(k)]
    box = [(float(x0), float(y0)), (float(x1), float(y0)),
           (float(x1), float(y1)), (float(x0), float(y1))]
    o = []
    for i, s in enumerate(sites):
        poly = list(box)
        for j, t in enumerate(sites):
            if i == j:
                continue
            poly = _clip(poly, s, t)
            if not poly:
                break
        if not poly:
            continue
        pts = ' '.join('%s,%s' % (f(p[0]), f(p[1])) for p in poly)
        col, op = CAT6[i % len(CAT6)]
        o.append('<g>' + tit('centroide %d' % (i + 1),
                             'su celda son los puntos más cercanos a él'))
        o.append('<polygon points="%s" fill="%s" fill-opacity="%s" stroke="%s" '
                 'stroke-width="1.4" />'
                 % (pts, col, f(0.30 if op is None else 0.15), col))
        o.append('<circle cx="%s" cy="%s" r="4" fill="%s" />'
                 % (f(s[0]), f(s[1]), INK))
        o.append('</g>')
    o.append('<text x="%s" y="%s" font-size="11" fill="%s" text-anchor="middle">'
             'las fronteras entre clusters de K-Means son siempre rectas</text>'
             % (f(W / 2), f(H - 14), MUT))
    return svg(o, W, H, 'Diagrama de Voronoi de catorce centroides')


# ================================================================ 13 codo
# valores leidos de la captura
def codo():
    W, H, L, R, T, B = 720, 380, 74, 20, 26, 56
    ks = list(range(1, 11))
    inertia = [33800, 15750, 3400, 900, 840, 780, 690, 590, 540, 450]
    x0, x1, y1 = L, W - R, H - B
    sx = lambda k: x0 + (k - 1) * (x1 - x0) / (len(ks) - 1)
    sy = lambda v: y1 - v / 36000.0 * (y1 - T)
    yt = [(('%d' % v) if v < 1000 else '%dk' % (v // 1000), sy(v))
          for v in range(0, 35001, 5000)]
    xt = [(str(k), sx(k)) for k in ks]
    o = axes(W, H, L, R, T, B, 'Número de clusters (k)',
             'Suma de distancias al cuadrado', yt, xt)
    pts = ' '.join('%s,%s' % (f(sx(k)), f(sy(v))) for k, v in zip(ks, inertia))
    o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round" />' % (pts, ACC))
    # marca del codo
    kc = 4
    o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
             'stroke-width="1.6" stroke-dasharray="5 4" />'
             % (f(sx(kc)), f(T + 6), f(sx(kc)), f(y1), ACC4))
    o.append('<text x="%s" y="%s" font-size="12" font-weight="700" fill="%s" '
             'text-anchor="middle">el codo: k = %d</text>'
             % (f(sx(kc) + 62), f(T + 18), ACC4, kc))
    for k, v in zip(ks, inertia):
        o.append('<circle cx="%s" cy="%s" r="5" fill="%s">%s</circle>'
                 % (f(sx(k)), f(sy(v)), ACC4 if k == kc else ACC,
                    tit('k = %d' % k,
                        'inercia %s' % ('{:,}'.format(v).replace(',', '.')))))
    return svg(o, W, H, 'Curva del codo: suma de distancias al cuadrado contra '
                        'el número de clusters')


# ----------------------------------------------------------------
FIGURAS = [
    ('box-plot', box_plot), ('violin', violin), ('pie', pie),
    ('stacked-bar', stacked_bar), ('scatter', scatter), ('heatmap', heatmap),
    ('line', line_plot), ('lollipop', lollipop), ('venn', venn),
    ('radar', radar), ('dendograma', dendograma), ('voronoi', voronoi),
    ('codo', codo),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for nombre, fn in FIGURAS:
        cuerpo = fn()
        with open(os.path.join(OUT, nombre + '.html'), 'w', encoding='utf-8',
                  newline='\n') as fh:
            fh.write(cuerpo + '\n')
        print('  %s.html  (%d chars)' % (nombre, len(cuerpo)))
    print('\n%d figuras generadas en %s' % (len(FIGURAS), OUT))


if __name__ == '__main__':
    main()
