"""Render the Jusmanizer share card from project fonts. Requires Pillow."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "docs/assets/fonts"
SCALE = 2
OUT = ROOT / "docs/assets/social-preview.png"

image = Image.new("RGB", (1280 * SCALE, 640 * SCALE), "#0b1118")
draw = ImageDraw.Draw(image)


def font(name, size, weight=400):
    result = ImageFont.truetype(str(FONTS / name), size * SCALE)
    axes = [weight]
    if name.startswith("Newsreader"):
        axes.append(min(size, 72))
    result.set_variation_by_axes(axes)
    return result


def label(x, y, value, name, size, color, weight=400):
    draw.text((x * SCALE, y * SCALE), value, fill=color, font=font(name, size, weight), anchor="lt")


def box(x1, y1, x2, y2, fill, outline=None, radius=0, width=1):
    bounds = tuple(value * SCALE for value in (x1, y1, x2, y2))
    draw.rounded_rectangle(bounds, radius=radius * SCALE, fill=fill, outline=outline, width=width * SCALE)


def line(x1, y1, x2, y2, color, width=1):
    draw.line((x1 * SCALE, y1 * SCALE, x2 * SCALE, y2 * SCALE), fill=color, width=width * SCALE)


box(24, 24, 1256, 616, "#0b1118", "#2c3e50", 9, 2)
label(64, 71, "j.", "JetBrainsMono.ttf", 40, "#ccff80", 600)
label(126, 71, "jusmanizer", "JetBrainsMono.ttf", 40, "#dde3ed", 600)
label(366, 71, "_", "JetBrainsMono.ttf", 40, "#ccff80", 600)
box(397, 76, 408, 113, "#ccff80")
line(64, 142, 1216, 142, "#2c3e50")
label(65, 171, "SKILL ABERTA · PORTUGUÊS JURÍDICO", "JetBrainsMono.ttf", 18, "#ccff80", 600)
label(62, 217, "O argumento é seu.", "Newsreader.ttf", 78, "#dde3ed")
label(62, 307, "A escrita também.", "Newsreader-Italic.ttf", 78, "#ccff80")
label(66, 435, "A IA ajuda no rascunho.", "Manrope.ttf", 26, "#9aa9b9", 450)
label(66, 475, "A escrita precisa continuar sendo sua.", "Manrope.ttf", 26, "#9aa9b9", 450)
box(64, 543, 246, 590, "#ccff80", radius=4)
label(84, 557, "32 PADRÕES", "JetBrainsMono.ttf", 17, "#213600", 600)
box(258, 543, 422, 590, "#131d27", "#2c3e50", 4)
label(279, 557, "6 GRUPOS", "JetBrainsMono.ttf", 17, "#dde3ed")

box(774, 177, 1214, 568, "#131d27", "#2c3e50", 8)
label(802, 205, "MINUTA / REVISÃO DE ESTILO", "JetBrainsMono.ttf", 15, "#ccff80", 600)
line(802, 239, 1186, 239, "#2c3e50")
label(802, 263, "O EXCESSO", "JetBrainsMono.ttf", 17, "#fca5a5")
label(802, 289, "Cumpre esclarecer que", "Newsreader.ttf", 31, "#c6c3c8")
line(802, 309, 1090, 309, "#fca5a5", 2)
label(802, 329, "a autora pagou o valor indicado.", "Newsreader.ttf", 29, "#c6c3c8")
label(802, 389, "↓  AFIRMAR, EM VEZ DE ANUNCIAR", "JetBrainsMono.ttf", 15, "#ccff80")
label(802, 441, "O ARGUMENTO", "JetBrainsMono.ttf", 17, "#86efac")
label(802, 466, "A autora pagou o valor indicado.", "Newsreader.ttf", 29, "#dde3ed")
line(802, 524, 1186, 524, "#2c3e50")
label(802, 541, "J06 · PREÂMBULO ENCENADO", "JetBrainsMono.ttf", 14, "#9aa9b9")

image.resize((1280, 640), Image.Resampling.LANCZOS).save(OUT, optimize=True)
print("Rendered social-preview.png (1280 × 640).")
