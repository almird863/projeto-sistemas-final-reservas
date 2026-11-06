"""
Componentes e estilos compartilhados entre as telas (views).

A ideia: tudo que se repete entre telas (cores, carregar imagem, campo com
ícone, barra azul do topo, imagem lateral com a onda) fica AQUI, em um lugar só.
Assim, se mudar uma cor ou o estilo do campo, muda em todas as telas.

Uso nas telas:
    from views.componentes import AZUL_ESCURO, criar_campo, criar_barra_titulo
"""

import os
import customtkinter as ctk
from PIL import Image, ImageOps

# ----------------------------------------------------------------------
# CAMINHOS
# ----------------------------------------------------------------------
# As imagens ficam em views/assets/  (a pasta onde este arquivo está + "assets")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# ----------------------------------------------------------------------
# PALETA DE CORES (mesma do login)
# ----------------------------------------------------------------------
AZUL_ESCURO = "#1B3A7A"
AZUL_HOVER = "#142C5E"
LARANJA = "#F59A1B"
LARANJA_HOVER = "#D98310"
FUNDO_DIREITO = "#F4F6FB"
BORDA_CAMPO = "#D5DAE6"
TEXTO_CINZA = "#555B6E"
VERMELHO = "#C0392B"


def carregar_imagem(nome_arquivo, tamanho):
    """
    Carrega uma imagem da pasta assets e devolve um CTkImage.
    Se o arquivo não existir, devolve None (a tela continua funcionando,
    mostrando um texto/emoji no lugar da imagem).
    """
    caminho = os.path.join(ASSETS_DIR, nome_arquivo)
    if not os.path.exists(caminho):
        return None
    img = Image.open(caminho)
    return ctk.CTkImage(light_image=img, dark_image=img, size=tamanho)


def montar_imagem_lateral(largura, altura, altura_onda=120):
    """
    Junta a foto do quarto + a onda decorativa numa única imagem.

    >>> IMAGEM: assets/foto_quarto.png   (foto do quarto)
    >>> IMAGEM: assets/onda_laranja.png  (PNG com fundo transparente)

    A foto é "recortada para preencher" (como o object-fit: cover do CSS):
    ela mantém a proporção e corta o excesso, em vez de ficar esticada.
    Por isso funciona bem em telas de alturas diferentes (login e cadastro).
    """
    caminho_foto = os.path.join(ASSETS_DIR, "foto_quarto.png")
    caminho_onda = os.path.join(ASSETS_DIR, "onda_laranja.png")

    if os.path.exists(caminho_foto):
        foto = Image.open(caminho_foto).convert("RGBA")
        base = ImageOps.fit(foto, (largura, altura), Image.LANCZOS)
    else:
        base = Image.new("RGBA", (largura, altura), "#E9E4DA")  # espaço reservado

    if os.path.exists(caminho_onda):
        onda = Image.open(caminho_onda).convert("RGBA").resize((largura, altura_onda))
        base.alpha_composite(onda, (0, altura - altura_onda))

    if not os.path.exists(caminho_foto) and not os.path.exists(caminho_onda):
        return None

    return ctk.CTkImage(light_image=base, dark_image=base, size=(largura, altura))


def criar_barra_titulo(parent):
    """Barra azul escura do topo, com o ícone da cama e o nome do sistema."""
    barra = ctk.CTkFrame(parent, height=40, fg_color=AZUL_ESCURO, corner_radius=0)
    barra.pack(side="top", fill="x")
    barra.pack_propagate(False)

    # >>> IMAGEM: assets/icone_cama.png (24x24)
    img_cama = carregar_imagem("icone_cama.png", (24, 24))
    lbl_icone = ctk.CTkLabel(
        barra,
        text="" if img_cama else "🛏",
        image=img_cama,
        text_color="white",
        font=ctk.CTkFont(size=18),
    )
    lbl_icone.pack(side="left", padx=(14, 6))
    lbl_icone.imagem_ref = img_cama  # guarda a referência da imagem

    ctk.CTkLabel(
        barra,
        text="Sistema de Reservas - Hotel",
        text_color="white",
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
    ).pack(side="left")
    return barra


def criar_campo(parent, placeholder, icone_arquivo, icone_fallback, mostrar=None, largura=340):
    """
    Campo de texto com ícone à esquerda e borda arredondada.
    Devolve o CTkEntry (use .get() para ler o que a pessoa digitou).

    icone_arquivo  -> nome do PNG em assets/ (ex.: "icone_campo_user.png", 20x20)
    icone_fallback -> emoji mostrado enquanto o PNG não existir
    mostrar        -> "•" para campos de senha
    """
    moldura = ctk.CTkFrame(
        parent, width=largura, height=46, corner_radius=10,
        fg_color="white", border_width=1, border_color=BORDA_CAMPO,
    )
    moldura.pack(pady=6)
    moldura.pack_propagate(False)

    # >>> IMAGEM: ícone do campo (20x20) -> assets/<icone_arquivo>
    img = carregar_imagem(icone_arquivo, (20, 20))

    # fg_color explícito + pady=3: mantém a borda arredondada visível
    lbl = ctk.CTkLabel(
        moldura,
        text="" if img else icone_fallback,
        image=img,
        text_color=AZUL_ESCURO,
        fg_color="white",
        width=30,
        font=ctk.CTkFont(size=15),
    )
    lbl.pack(side="left", padx=(10, 0), pady=3)
    lbl.imagem_ref = img  # guarda a referência da imagem

    entry = ctk.CTkEntry(
        moldura,
        placeholder_text=placeholder,
        show=mostrar if mostrar else "",
        border_width=0, fg_color="white",
        text_color="#222", placeholder_text_color="#6B7080",
        font=ctk.CTkFont(family="Segoe UI", size=14),
    )
    entry.pack(side="left", fill="both", expand=True, padx=(4, 8), pady=3)
    return entry
