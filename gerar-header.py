#!/usr/bin/env python3
"""Cabecalho do README da organizacao DBA BRABO no GitHub.

Regrava profile/assets/header.png. Rode de dentro da pasta do repositorio:

    python gerar-header.py

Mesmo desenho do cabecalho do perfil pessoal (acaciolr/acaciolr), com a marca
da organizacao no lugar do nome e um emblema de banco no lugar da badge.
Requer Pillow:  pip install pillow
As fontes Poppins sao procuradas no sistema ou em ./fontes; sem elas cai no DejaVu.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1280, 340
BG    = (7, 9, 13)
FG    = (240, 245, 250)
MUT   = (146, 163, 181)
BRAND = (255, 138, 76)
CYAN  = (46, 216, 195)
AQUI = os.path.dirname(os.path.abspath(__file__))
def fonte(nome, tam):
    """Procura Poppins no sistema; se nao achar, usa DejaVu."""
    for base in ("/usr/share/fonts/truetype/google-fonts/",
                 "C:/Windows/Fonts/", os.path.join(AQUI, "fontes")):
        p = os.path.join(base, nome)
        if os.path.exists(p):
            return ImageFont.truetype(p, tam)
    for base in ("/usr/share/fonts/truetype/dejavu/", "C:/Windows/Fonts/"):
        for alt in ("DejaVuSans-Bold.ttf", "arialbd.ttf", "arial.ttf"):
            p = os.path.join(base, alt)
            if os.path.exists(p):
                return ImageFont.truetype(p, tam)
    return ImageFont.load_default()
f_nome  = fonte("Poppins-Bold.ttf", 66)
f_role  = fonte("Poppins-Medium.ttf", 27)
f_sub   = fonte("Poppins-Light.ttf", 21)
f_eye   = fonte("Poppins-Medium.ttf", 15)

im = Image.new("RGB", (W, H), BG)
glow = Image.new("RGB", (W, H), BG)
g = ImageDraw.Draw(glow)
g.ellipse((-320, -300, 700, 420), fill=(78, 36, 18))
g.ellipse((900, -180, 1560, 300), fill=(9, 48, 46))
im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(140)), 0.88)

grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gg = ImageDraw.Draw(grid)
for x in range(0, W, 44): gg.line([(x, 0), (x, H)], fill=(255, 255, 255, 9))
for y in range(0, H, 44): gg.line([(0, y), (W, y)], fill=(255, 255, 255, 9))
im = Image.alpha_composite(im.convert("RGBA"), grid).convert("RGB")

d = ImageDraw.Draw(im)
X = 76
d.line([(X, 96), (X, 262)], fill=BRAND, width=4)
x = X + 30
# olho: letras espacadas
eyebrow = "M E N T O R I A   T É C N I C A   P A R A   D B A s"
d.text((x, 92), eyebrow, font=f_eye, fill=BRAND)
d.text((x, 118), "DBA BRABO", font=f_nome, fill=FG)
d.text((x, 202), "Oracle · MySQL · SQL Server · PostgreSQL · MongoDB", font=f_role, fill=MUT)
d.text((x, 240), "Laboratórios reais, trilha por tecnologia, acompanhamento de perto", font=f_sub, fill=(110, 128, 146))

# lado direito: emblema de banco (tres discos empilhados), com halo — a
# organizacao nao tem badge propria, e o cilindro e o simbolo universal de banco
halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(halo).ellipse((W-330, 62, W-102, 290), fill=(255, 138, 76, 46))
im = Image.alpha_composite(im.convert("RGBA"), halo.filter(ImageFilter.GaussianBlur(46)))
emb = Image.new("RGBA", (W, H), (0, 0, 0, 0))
e = ImageDraw.Draw(emb)
cx, rx, ry, topo, passo = W - 216, 74, 22, 104, 46
for i, cor in enumerate((BRAND, BRAND, CYAN)):
    y = topo + i * passo
    # corpo do disco: laterais + elipse de baixo
    e.rectangle((cx - rx, y, cx + rx, y + passo - 10), fill=(14, 18, 24, 255))
    e.ellipse((cx - rx, y + passo - 10 - ry, cx + rx, y + passo - 10 + ry), fill=(14, 18, 24, 255), outline=cor, width=4)
    e.line([(cx - rx, y), (cx - rx, y + passo - 10)], fill=cor, width=4)
    e.line([(cx + rx, y), (cx + rx, y + passo - 10)], fill=cor, width=4)
    # tampa
    e.ellipse((cx - rx, y - ry, cx + rx, y + ry), fill=(20, 26, 34, 255), outline=cor, width=4)
im = Image.alpha_composite(im, emb).convert("RGB")

SAIDA = os.path.join(AQUI, "profile", "assets", "header.png")
os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
im.save(SAIDA, "PNG", optimize=True)
print("gravado:", SAIDA, im.size)
