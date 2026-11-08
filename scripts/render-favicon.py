# /// script
# requires-python = ">=3.10"
# dependencies = ["fonttools>=4.50"]
# ///
"""Gera docs/assets/favicon.svg, a marca "J." com o ponto vermelho, em contornos de letra.

A capa do README e a imagem de compartilhamento saem de scripts/render-capa.py, que
fotografa a página docs/capa.html. Uso: uv run scripts/render-favicon.py
"""

import re
from html import escape
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "docs/assets/fonts"

# Papel e lápis de revisão.
PAPER, INK, LINE_STRONG = "#f6f3ec", "#1d1b18", "#c4b9a5"
RED = "#b23a2a"


def load(name, **axes):
    font = TTFont(FONTS / name)
    if "fvar" in font:
        valid = {a.axisTag for a in font["fvar"].axes}
        font = instantiateVariableFont(font, {k: v for k, v in axes.items() if k in valid})
    return font


FACES = {
    "serif": load("Newsreader.ttf", wght=420, opsz=48),
}


def text(value, x, y, size, color, face="serif", tracking=0.0):
    """Outline `value` with its baseline at (x, y). Returns (svg, width)."""
    font = FACES[face]
    cmap = font.getBestCmap()
    glyphs = font.getGlyphSet()
    hmtx = font["hmtx"]
    upm = font["head"].unitsPerEm
    scale = size / upm
    paths, cursor = [], 0.0
    for char in value:
        name = cmap.get(ord(char))
        if name is None:
            continue
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        # Coordenadas em unidades da fonte: frações não mudam o desenho e só pesam.
        d = re.sub(r"-?\d+\.\d+", lambda m: str(round(float(m.group()))), pen.getCommands())
        if d:
            paths.append(f'<path transform="translate({cursor:.0f} 0)" d="{d}"/>')
        cursor += hmtx[name][0] + tracking * upm
    width = cursor * scale
    svg = (f'<g fill="{color}" transform="translate({x:.1f} {y:.1f}) scale({scale:.6f} {-scale:.6f})">'
           + "".join(paths) + "</g>")
    return svg, width


def mark(x, y, size, ink=INK, dot=RED):
    """A marca "J." com o ponto como círculo vermelho. Devolve (svg, largura)."""
    letter, width = text("J", x, y, size, ink)
    r = size * 0.095
    cx = x + width + size * 0.05 + r
    return letter + f'<circle cx="{cx:.1f}" cy="{y - r:.1f}" r="{r:.1f}" fill="{dot}"/>', cx + r - x


def svg(w, h, body, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title>'
            f'<desc id="desc">{escape(desc)}</desc>{body}</svg>\n')


def favicon():
    _, lw = mark(0, 0, 48)
    logo, _ = mark(32 - lw / 2, 47, 48)
    body = f'<rect width="64" height="64" rx="12" fill="{PAPER}" stroke="{LINE_STRONG}"/>' + logo
    (ROOT / "docs/assets/favicon.svg").write_text(svg(64, 64, body, "Jusmanizer", "Marca J. com o ponto vermelho."), encoding="utf-8")


favicon()
print("Rendered docs/assets/favicon.svg.")
