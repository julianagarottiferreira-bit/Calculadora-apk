"""Gera o ícone de calculadora (512x512) usado pelo app.

Uso: python gera_icone.py assets/icon.png
"""
import os
import sys

from PIL import Image, ImageDraw

saida = sys.argv[1] if len(sys.argv) > 1 else "assets/icon.png"
os.makedirs(os.path.dirname(saida) or ".", exist_ok=True)

S = 2  # supersampling para bordas suaves
T = 512 * S

AZUL = (75, 90, 148)
AZUL_CLARO = (157, 176, 255)
BEGE = (235, 229, 216)
BEGE_ESCURO = (220, 216, 201)
FUNDO_VISOR = (228, 227, 222)
VERMELHO = (209, 64, 31)

img = Image.new("RGBA", (T, T), (0, 0, 0, 0))
d = ImageDraw.Draw(img)


def rr(box, raio, cor):
    d.rounded_rectangle([v * S for v in box], radius=raio * S, fill=cor)


def circ(cx, cy, r, cor):
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=cor)


# Fundo (quadrado arredondado azul)
rr((0, 0, 512, 512), 112, AZUL)

# Visor
rr((56, 56, 456, 176), 30, FUNDO_VISOR)
rr((300, 96, 420, 112), 8, (140, 140, 134))
rr((340, 128, 420, 144), 8, (190, 190, 184))

# Teclas: 4 colunas x 3 linhas
r = 36
colunas = [56 + r + i * ((400 - 2 * r) / 3) for i in range(4)]
linhas = [224, 312, 400]

for j, cy in enumerate(linhas):
    for i, cx in enumerate(colunas):
        cor = AZUL_CLARO if i == 3 else BEGE
        if j == 0 and i == 0:
            cor = BEGE_ESCURO
        circ(cx, cy, r, cor)

# Tecla "=" em destaque
cx, cy = colunas[3], linhas[2]
circ(cx, cy, r, VERMELHO)
rr((cx - 18, cy - 15, cx + 18, cy - 5), 5, (255, 255, 255))
rr((cx - 18, cy + 5, cx + 18, cy + 15), 5, (255, 255, 255))

# "+" e "−" nas teclas azul-claras
cx = colunas[3]
rr((cx - 20, linhas[0] - 5, cx + 20, linhas[0] + 5), 5, AZUL)
rr((cx - 5, linhas[0] - 20, cx + 5, linhas[0] + 20), 5, AZUL)
rr((cx - 20, linhas[1] - 5, cx + 20, linhas[1] + 5), 5, AZUL)

img = img.resize((512, 512), Image.LANCZOS)
img.save(saida)
print("ok", saida)
