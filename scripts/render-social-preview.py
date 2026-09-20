"""Render the share card from project typography and colors. Requires Pillow."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SCALE = 2
image = Image.new("RGB", (1280 * SCALE, 640 * SCALE), "#0b1118")
draw = ImageDraw.Draw(image)
font_file = ROOT / "docs/assets/fonts/Manrope.ttf"


def box(bounds, fill, outline=None, radius=0, width=1):
    scaled = tuple(int(value * SCALE) for value in bounds)
    if radius:
        draw.rounded_rectangle(scaled, radius=radius * SCALE, fill=fill, outline=outline, width=width * SCALE)
    else:
        draw.rectangle(scaled, fill=fill, outline=outline, width=width * SCALE)


def text(position, content, size, color, weight=500):
    font = ImageFont.truetype(str(font_file), size * SCALE)
    font.set_variation_by_axes([weight])
    draw.text(tuple(value * SCALE for value in position), content, font=font, fill=color)


for x in range(710, 1280, 40):
    draw.line((x * SCALE, 0, x * SCALE, 640 * SCALE), fill="#152730", width=SCALE)
for y in range(0, 640, 40):
    draw.line((710 * SCALE, y * SCALE, 1280 * SCALE, y * SCALE), fill="#152730", width=SCALE)
box((24, 24, 1256, 616), None, "#425839", 22, 2)
box((65, 66, 111, 112), "#c6ff5e", radius=11)
text((76, 65), "j.", 33, "#14210b", 800)
text((130, 66), "jusmanizer_", 32, "#eef3f5", 800)
text((63, 195), "Seu argumento.", 68, "#eef3f5", 800)
text((63, 278), "Sua voz.", 81, "#c6ff5e", 800)
text((68, 389), "Revisão de estilo jurídico", 26, "#adbfcc")
text((68, 427), "para o seu assistente de IA.", 26, "#adbfcc")
box((67, 485, 240, 530), "#c6ff5e", radius=7)
text((88, 496), "32 padrões", 18, "#18240c", 750)
box((254, 485, 420, 530), "#15262e", "#36535e", 7)
text((275, 496), "Licença MIT", 18, "#bfeffa", 600)
text((68, 568), "EXEMPLOS  ·  PROMPTS  ·  INSTALAÇÃO", 14, "#839baa", 650)
box((779, 135, 1207, 533), "#21373f", "#36545c", 12)
box((756, 115, 1184, 513), "#f3f3e9", radius=12)
box((765, 115, 1175, 120), "#c6ff5e")
text((785, 145), "MINUTA / REVISÃO DE ESTILO", 12, "#64757d", 650)
draw.line((785 * SCALE, 181 * SCALE, 1155 * SCALE, 181 * SCALE), fill="#c4ccc6", width=SCALE)
text((785, 206), "Cumpre esclarecer que", 26, "#9d735f")
draw.line((785 * SCALE, 226 * SCALE, 1092 * SCALE, 226 * SCALE), fill="#a75f44", width=2 * SCALE)
text((785, 248), "a autora pagou o valor.", 26, "#435059")
box((785, 303, 824, 342), "#dce7c8", radius=19)
text((798, 306), "↓", 23, "#5b7c46", 700)
text((842, 315), "O FATO CONTINUA.", 12, "#65814b", 650)
text((785, 368), "A autora pagou", 33, "#23343b", 750)
text((785, 411), "o valor.", 33, "#23343b", 750)
draw.line((785 * SCALE, 465 * SCALE, 1155 * SCALE, 465 * SCALE), fill="#c4ccc6", width=SCALE)
text((785, 481), "EXEMPLO ILUSTRATIVO", 11, "#64757d", 600)
image.resize((1280, 640), Image.Resampling.LANCZOS).save(ROOT / "docs/assets/social-preview.png", optimize=True)
print("Rendered social-preview.png (1280 × 640).")
