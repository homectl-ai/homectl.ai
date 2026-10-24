# homectl logo: Bricolage Grotesque ExtraBold (OFL), the o as a lit dot.
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
font_path, out = sys.argv[1], sys.argv[2]
f = TTFont(font_path); gs = f.getGlyphSet(); cmap = f.getBestCmap()
INK, CREAM, WARM, AMBER = '#1c1917', '#fff7ed', '#ea580c', '#fb923c'
TRACK = -21  # -2px at 96px, in font units

def glyph(ch): return gs[cmap[ord(ch)]]
def bounds(ch):
    p = BoundsPen(gs); glyph(ch).draw(p); return p.bounds
xmin, xb, xmax, xh = bounds('x')  # x-height: xb..xh
XH = xh - xb
R, GAP = XH * 0.5, XH * 0.07

def layout(parts):
    """-> (path d for letters in font units, y up; dot (cx, cy, r) or None; advance)"""
    d, dot, x = [], None, 0
    for kind, s in parts:
        if kind == 'text':
            for ch in s:
                sp = SVGPathPen(gs)
                glyph(ch).draw(TransformPen(sp, (1, 0, 0, -1, x, 0)))  # flip y
                d.append(sp.getCommands())
                x += glyph(ch).width + TRACK
        else:
            dot = (x + GAP + R, -(xb + XH / 2), R)
            x += 2 * R + 2 * GAP
    return ' '.join(d), dot, x - TRACK

asc = bounds('h')[3]  # top of the h ascender
style = (f'<style>.l{{fill:{INK}}}.d{{fill:{WARM}}}'
         f'@media (prefers-color-scheme:dark){{.l{{fill:{CREAM}}}.d{{fill:{AMBER}}}}}</style>')

# wordmark: tight box around the ink
d, (cx, cy, r), adv = layout([('text', 'h'), ('dot', ''), ('text', 'mectl')])
pad = 10
vb = (-pad, -asc - pad, adv + 2 * pad, asc + 2 * pad)
open(f'{out}/homectl-wordmark.svg', 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(f"{v:.0f}" for v in vb)}" role="img" aria-label="homectl">'
    f'{style}<path class="l" d="{d}"/><circle class="d" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}"/></svg>\n')

# icon: h + dot centred on an ink tile
d, (cx, cy, r), adv = layout([('text', 'h'), ('dot', '')])
hb = bounds('h')
w = (cx + r) - hb[0]; h = asc
S_ = 512; scale = 372 / max(w, h * 1.0) * 0.98
tx = (S_ - w * scale) / 2 - hb[0] * scale
ty = (S_ - h * scale) / 2 + asc * scale
def icon(rx):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="homectl">'
            f'<rect width="512" height="512" rx="{rx}" fill="{INK}"/>'
            f'<g transform="translate({tx:.1f} {ty:.1f}) scale({scale:.5f})">'
            f'<path fill="{CREAM}" d="{d}"/><circle fill="{WARM}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}"/></g></svg>\n')
open(f'{out}/logo.svg', 'w').write(icon(112))
open(f'{out}/logo-square.svg', 'w').write(icon(0))  # Google rounds/crops it itself
