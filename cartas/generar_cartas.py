"""Genera cartas.html con una carta por objetivo de objetivos.js (tamaño póquer, 9 por A4).

Las cartas no llevan texto: solo dados de colores, caras de dado, números y símbolos.
Uso:  python3 cartas/generar_cartas.py   (luego se imprime a PDF con imprimir_pdf.js)
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / 'cartas.html'

COLORS = {'azul': '#2f6fdb', 'naranja': '#ee8420', 'verde': '#2a9a58', 'morado': '#8a4fd1', 'amarillo': '#f1c232'}
ORDER = list(COLORS)
INK = '#18202c'
MUTED = '#8a94a6'
RED = '#d23b3b'
GOLD = '#e8a317'
CARD_W, CARD_H = 63.5, 88.9  # mm (póquer)
FONT = "'DejaVu Sans', sans-serif"

# Advance widths of DejaVu Sans Bold, in em.
CHAR_W = {**{d: 0.70 for d in '0123456789'}, '=': 0.84, '≤': 0.84, '≥': 0.84, '>': 0.84, '×': 0.84, 'Σ': 0.72,
          '#': 0.84, '*': 0.52, '→': 0.84, '+': 0.84, '★': 0.84, '…': 1.0, '✓': 0.84, '♛': 0.9, '▲': 0.77, '▼': 0.77}
MAX_ROW = CARD_W - 12

PIPS = {
    1: [(50, 50)], 2: [(28, 28), (72, 72)], 3: [(26, 26), (50, 50), (74, 74)],
    4: [(28, 28), (72, 28), (28, 72), (72, 72)], 5: [(26, 26), (74, 26), (50, 50), (26, 74), (74, 74)],
    6: [(28, 24), (72, 24), (28, 50), (72, 50), (28, 76), (72, 76)],
}


def load_objectives():
    """objetivos.js -> lista de dicts (evaluando el array con node)."""
    js = (ROOT / 'objetivos.js').read_text()
    out = subprocess.run(
        ['node', '-e', 'global.window={};eval(require("fs").readFileSync(0,"utf8"));'
         'process.stdout.write(JSON.stringify(window.BLINDSPOTS_OBJETIVOS))'],
        input=js, capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


# ---------- drawing primitives (all sizes in mm) ----------
class Row:
    """A horizontal run of glyphs, centred on the card."""

    def __init__(self, gap=1.6):
        self.items, self.gap = [], gap

    def die(self, colour, size=11, face=None, pip=None):
        self.items.append(('die', size, dict(colour=colour, face=face, pip=pip)))
        return self

    def any_die(self, size=11, face=None):
        self.items.append(('any', size, dict(face=face)))
        return self

    def text(self, s, size=9, colour=INK, width=None):
        w = width if width is not None else size * sum(CHAR_W.get(ch, 0.72) for ch in s)
        self.items.append(('text', w, dict(s=s, size=size, colour=colour)))
        return self

    def wheel(self, size=12, centre=''):
        self.items.append(('wheel', size, dict(centre=centre)))
        return self

    def faces(self, values, size=8, colour='#ffffff', pip=INK, overlap=0.0, fill_any=False):
        self.items.append(('faces', len(values) * size - (len(values) - 1) * overlap + (len(values) - 1) * 0.8,
                           dict(values=values, size=size, colour=colour, pip=pip, overlap=overlap, fill_any=fill_any)))
        return self

    def width(self):
        return sum(w for _, w, _ in self.items) + self.gap * (len(self.items) - 1)

    def svg(self, cy):
        w = self.width()
        if w > MAX_ROW:  # scale the whole row down around the card centre
            k = MAX_ROW / w
            return (f'<g transform="translate({CARD_W / 2:.2f},{cy:.2f}) scale({k:.3f}) translate({-CARD_W / 2:.2f},{-cy:.2f})">'
                    + self._svg(cy) + '</g>')
        return self._svg(cy)

    def _svg(self, cy):
        x = (CARD_W - self.width()) / 2
        parts = []
        for kind, w, o in self.items:
            if kind == 'die':
                parts.append(die_svg(x, cy - w / 2, w, COLORS[o['colour']], o['face'], o['pip']))
            elif kind == 'any':
                parts.append(any_die_svg(x, cy - w / 2, w, o['face']))
            elif kind == 'text':
                parts.append(f'<text x="{x + w / 2:.2f}" y="{cy + o["size"] * 0.35:.2f}" font-size="{o["size"]}" '
                             f'text-anchor="middle" font-weight="700" fill="{o["colour"]}" font-family="{FONT}">{o["s"]}</text>')
            elif kind == 'wheel':
                parts.append(wheel_svg(x + w / 2, cy, w / 2, o['centre']))
            elif kind == 'faces':
                s, xx = o['size'], x
                for v in o['values']:
                    if o['fill_any']:
                        parts.append(any_die_svg(xx, cy - s / 2, s, v))
                    else:
                        parts.append(die_svg(xx, cy - s / 2, s, o['colour'], v, o['pip'], stroke=INK))
                    xx += s - o['overlap'] + 0.8
            x += w + self.gap
        return ''.join(parts)


def pips_svg(x, y, size, face, colour):
    r = size * 0.095
    return ''.join(f'<circle cx="{x + px / 100 * size:.2f}" cy="{y + py / 100 * size:.2f}" r="{r:.2f}" fill="{colour}"/>'
                   for px, py in PIPS[face])


def die_svg(x, y, size, fill, face=None, pip=None, stroke=None):
    pip = pip or ('#3b2c00' if fill == COLORS['amarillo'] else '#ffffff')
    st = f' stroke="{stroke}" stroke-width="0.35"' if stroke else ' stroke="rgba(0,0,0,.25)" stroke-width="0.3"'
    out = f'<rect x="{x:.2f}" y="{y:.2f}" width="{size:.2f}" height="{size:.2f}" rx="{size * 0.2:.2f}" fill="{fill}"{st}/>'
    if face:
        out += pips_svg(x, y, size, face, pip)
    return out


_any_id = [0]


def any_die_svg(x, y, size, face=None):
    """A die of any colour: four colour quadrants."""
    _any_id[0] += 1
    cid = f'anyclip{_any_id[0]}'
    h = size / 2
    quads = [(0, 0, 'azul'), (h, 0, 'naranja'), (0, h, 'verde'), (h, h, 'morado')]
    out = (f'<clipPath id="{cid}"><rect x="{x:.2f}" y="{y:.2f}" width="{size:.2f}" height="{size:.2f}" rx="{size * 0.2:.2f}"/></clipPath>'
           f'<g clip-path="url(#{cid})">' +
           ''.join(f'<rect x="{x + dx:.2f}" y="{y + dy:.2f}" width="{h:.2f}" height="{h:.2f}" fill="{COLORS[c]}" opacity="0.55"/>' for dx, dy, c in quads) +
           '</g>' +
           f'<rect x="{x:.2f}" y="{y:.2f}" width="{size:.2f}" height="{size:.2f}" rx="{size * 0.2:.2f}" fill="none" stroke="{INK}" stroke-width="0.35"/>')
    if face:
        out += pips_svg(x, y, size, face, INK)
    return out


def wheel_svg(cx, cy, r, centre):
    import math
    out, n = [], len(ORDER)
    for i, c in enumerate(ORDER):
        a0, a1 = -math.pi / 2 + i * 2 * math.pi / n, -math.pi / 2 + (i + 1) * 2 * math.pi / n
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        out.append(f'<path d="M{cx:.2f},{cy:.2f} L{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 0 1 {x1:.2f},{y1:.2f} Z" fill="{COLORS[c]}"/>')
    out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r * 0.52:.2f}" fill="#ffffff"/>')
    if centre:
        fs = r * (0.85 if len(centre) == 1 else 0.62)
        out.append(f'<text x="{cx:.2f}" y="{cy + fs * 0.36:.2f}" font-size="{fs:.2f}" text-anchor="middle" font-weight="700" fill="{INK}" font-family="{FONT}">{centre}</text>')
    return ''.join(out)


def ban(cx, cy, r):
    """Red 'not allowed' sign drawn over a glyph."""
    return (f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="none" stroke="{RED}" stroke-width="1.6"/>'
            f'<line x1="{cx - r * 0.7:.2f}" y1="{cy + r * 0.7:.2f}" x2="{cx + r * 0.7:.2f}" y2="{cy - r * 0.7:.2f}" stroke="{RED}" stroke-width="1.6"/>')


EVEN, ODD = [2, 4, 6], [1, 3, 5]
BONUS = {'al_menos', 'como_maximo', 'total_al_menos', 'total_como_maximo', 'repetidos_al_menos', 'numero_al_menos',
         'suma_al_menos', 'suma_total_minima', 'suma_total_maxima'}


def card_content(o):
    """Returns (svg for the middle of the card, bonus value or None)."""
    t, c, c2, n, v = o['tipo'], o.get('color'), o.get('color2'), o.get('n'), o.get('numero')
    cy = CARD_H / 2 + 2
    if t == 'ninguno':
        return Row().die(c, 20).svg(cy) + ban(CARD_W / 2, cy, 15), None
    if t == 'al_menos':
        return Row().text(str(n), 16).text('×', 10).die(c, 16).svg(cy), n
    if t == 'exactamente':
        return Row().text(f'={n}', 16).text('×', 10).die(c, 16).svg(cy), None
    if t == 'como_maximo':
        return Row().text(f'≤{n}', 16).text('×', 10).die(c, 16).svg(cy), n
    if t == 'suma_mayor':
        return Row(1.2).text('Σ', 12).die(c, 12).text('>', 13).text('Σ', 12).die(c2, 12).svg(cy), None
    if t == 'mas_dados':
        return Row(1.2).text('#', 12).die(c, 12).text('>', 13).text('#', 12).die(c2, 12).svg(cy), None
    if t == 'suma_al_menos':
        return Row().text('Σ', 14).die(c, 15).text(f'≥{n}', 15).svg(cy), n
    if t == 'colores_exactos':
        return Row().text('=', 16).wheel(26, str(n)).svg(cy), None
    if t == 'todos_colores':
        return Row().wheel(28, '✓').svg(cy), None
    if t == 'total_al_menos':
        return Row().text(str(n), 16).text('×', 10).any_die(16).svg(cy), n
    if t == 'total_como_maximo':
        return Row().text(f'≤{n}', 16).text('×', 10).any_die(16).svg(cy), n
    if t == 'sin_pares':
        return Row().faces(EVEN, 11).svg(cy) + ban(CARD_W / 2, cy, 20), None
    if t == 'sin_impares':
        return Row().faces(ODD, 11).svg(cy) + ban(CARD_W / 2, cy, 20), None
    if t == 'pares_exactos':
        return (Row().text(f'={n}', 16).text('×', 10).svg(cy - 9) + Row().faces(EVEN, 10).svg(cy + 9)), None
    if t == 'impares_exactos':
        return (Row().text(f'={n}', 16).text('×', 10).svg(cy - 9) + Row().faces(ODD, 10).svg(cy + 9)), None
    if t == 'mas_pares':
        return (Row().text('#', 11).faces(EVEN, 8).svg(cy - 9) + Row().text('>', 13).svg(cy + 1)
                + Row().text('#', 11).faces(ODD, 8).svg(cy + 11)), None
    if t == 'mas_impares':
        return (Row().text('#', 11).faces(ODD, 8).svg(cy - 9) + Row().text('>', 13).svg(cy + 1)
                + Row().text('#', 11).faces(EVEN, 8).svg(cy + 11)), None
    if t == 'repetidos_exactos':
        return (Row().text(f'={n}', 16).text('×', 10).svg(cy - 9) + Row().faces([5] * n, 10, overlap=0).svg(cy + 9)), None
    if t == 'repetidos_al_menos':
        return (Row().text(str(n), 16).text('×', 10).svg(cy - 9) + Row().faces([5] * n, 10, overlap=0).svg(cy + 9)), n
    if t == 'valor_maximo':
        return Row().any_die(15).text('≤', 16).faces([n], 15).svg(cy), None
    if t == 'valor_minimo':
        return Row().any_die(15).text('≥', 16).faces([n], 15).svg(cy), None
    if t == 'sin_numero':
        return Row().faces([v], 20).svg(cy) + ban(CARD_W / 2, cy, 15), None
    if t == 'numero_al_menos':
        return Row().text(str(n), 16).text('×', 10).faces([v], 16).svg(cy), n
    if t == 'suma_total_maxima':
        return Row().text('Σ', 14).any_die(15).text(f'≤{n}', 15).svg(cy), n
    if t == 'suma_total_minima':
        return Row().text('Σ', 14).any_die(15).text(f'≥{n}', 15).svg(cy), n
    if t == 'suma_total_par':
        return (Row().text('Σ', 14).any_die(14).text('=', 14).svg(cy - 9) + Row().faces(EVEN, 9).text('…', 10).svg(cy + 9)), None
    if t == 'escalera':
        size = 8.6 if n >= 6 else 9.5
        return Row().faces(list(range(1, n + 1)), size).svg(cy), None
    if t == 'escalera_color':
        size = 9.5
        return (Row().wheel(12, '1').svg(cy - 10)
                + Row().faces(list(range(1, n + 1)), size, colour=COLORS['azul'], pip='#ffffff').svg(cy + 6)), None
    if t == 'dos_parejas':
        return Row(4).faces([2, 2], 11, overlap=0).faces([5, 5], 11, overlap=0).svg(cy), None
    if t == 'full':
        return Row(3.5).faces([3, 3, 3], 10, overlap=0).faces([6, 6], 10, overlap=0).svg(cy), None
    # Comparisons with the other players: a crown, then up (most) or down (fewest).
    rank = {'mas_dados_que_nadie': ('▲', lambda r: r.text('#', 14).any_die(16)),
            'menos_dados_que_nadie': ('▼', lambda r: r.text('#', 14).any_die(16)),
            'mas_puntos_que_nadie': ('▲', lambda r: r.text('Σ', 14).any_die(16)),
            'menos_puntos_que_nadie': ('▼', lambda r: r.text('Σ', 14).any_die(16)),
            'mas_puntos_color_que_nadie': ('▲', lambda r: r.text('Σ', 14).die(c, 16)),
            'menos_puntos_color_que_nadie': ('▼', lambda r: r.text('Σ', 14).die(c, 16)),
            'mas_dados_color_que_nadie': ('▲', lambda r: r.text('#', 14).die(c, 16)),
            'mas_colores_que_nadie': ('▲', lambda r: r.wheel(20)),
            'mas_numero_que_nadie': ('▲', lambda r: r.text('#', 14).faces([v], 16))}
    if t in rank:
        arrow, subject = rank[t]
        top = Row(1.5).text('♛', 16, GOLD).text(arrow, 14, INK)
        return top.svg(cy - 11) + subject(Row()).svg(cy + 9), None
    raise ValueError(f'tipo sin dibujo: {t}')


def stars_svg(s, y):
    total_w = 5 * 7.2
    x0 = (CARD_W - total_w) / 2 + 3.6
    return ''.join(
        f'<text x="{x0 + i * 7.2:.2f}" y="{y:.2f}" font-size="7.6" text-anchor="middle" font-family="{FONT}" '
        f'fill="{GOLD if i < s else "#d9dde4"}">★</text>' for i in range(5))


def card_svg(o, idx):
    mid, bonus = card_content(o)
    s = o['estrellas']
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CARD_W} {CARD_H}" width="{CARD_W}mm" height="{CARD_H}mm">',
        f'<rect x="0.6" y="0.6" width="{CARD_W - 1.2}" height="{CARD_H - 1.2}" rx="3.2" fill="#fdfcf7" stroke="#c9cfd8" stroke-width="0.3"/>',
        f'<rect x="3" y="3" width="{CARD_W - 6}" height="{CARD_H - 6}" rx="2.4" fill="none" stroke="#e7e9ee" stroke-width="0.4"/>',
        stars_svg(s, 11.5),
        mid,
    ]
    if bonus is not None:
        y = CARD_H - 15
        parts.append(f'<line x1="9" y1="{y - 6}" x2="{CARD_W - 9}" y2="{y - 6}" stroke="#e1e4ea" stroke-width="0.3"/>')
        parts.append(Row(1.4).text('*', 9, MUTED).text(f'={bonus}', 9, MUTED).text('→', 9, MUTED).text('+1', 9, GOLD).text('★', 9, GOLD, width=5).svg(y))
    parts.append(f'<text x="{CARD_W - 6}" y="{CARD_H - 5.2}" font-size="2.6" text-anchor="end" fill="#b3bac6" font-family="{FONT}">{idx}</text>')
    parts.append('</svg>')
    return ''.join(parts)


def back_svg():
    dots = ''.join(f'<rect x="{12 + i * 8.4:.2f}" y="{CARD_H / 2 + 8:.2f}" width="6" height="6" rx="1.3" fill="{COLORS[c]}"/>'
                   for i, c in enumerate(ORDER))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CARD_W} {CARD_H}" width="{CARD_W}mm" height="{CARD_H}mm">'
            f'<rect x="0.6" y="0.6" width="{CARD_W - 1.2}" height="{CARD_H - 1.2}" rx="3.2" fill="#263247" stroke="#c9cfd8" stroke-width="0.3"/>'
            '<pattern id="st" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="2" height="4" fill="#2f3d56"/></pattern>'
            f'<rect x="3" y="3" width="{CARD_W - 6}" height="{CARD_H - 6}" rx="2.4" fill="url(#st)"/>'
            f'<circle cx="{CARD_W / 2}" cy="{CARD_H / 2 - 6}" r="11" fill="rgba(255,255,255,.1)"/>'
            f'<text x="{CARD_W / 2}" y="{CARD_H / 2 - 1}" font-size="15" text-anchor="middle" font-weight="700" fill="#e7ebf1" font-family="{FONT}">?</text>'
            f'{dots}</svg>')


def main():
    objs = load_objectives()
    cards = [card_svg(o, i + 1) for i, o in enumerate(objs)]
    pages = [cards[i:i + 9] for i in range(0, len(cards), 9)]
    html = ['<!doctype html><html><head><meta charset="utf-8"><title>BlindSpots · Objetivos</title><style>',
            '@page { size: A4; margin: 0; }',
            'body { margin: 0; }',
            '.page { width: 210mm; height: 297mm; display: grid; grid-template-columns: repeat(3, 63.5mm); grid-auto-rows: 88.9mm;',
            '  justify-content: center; align-content: center; page-break-after: always; break-after: page; }',
            '.page:last-child { page-break-after: auto; }',
            '.page svg { display: block; }',
            '</style></head><body>']
    for p in pages:
        html.append('<div class="page">' + ''.join(p) + '</div>')
    html.append('<div class="page">' + back_svg() * 9 + '</div>')
    html.append('</body></html>')
    OUT.write_text(''.join(html))
    print(f'{len(cards)} cartas, {len(pages)} hojas + 1 de reversos -> {OUT}')


if __name__ == '__main__':
    main()
