"""
View de Login - Sistema de Reservas - Hotel
Tkinter + CustomTkinter

Instalação:  pip install customtkinter pillow

Estrutura de imagens sugerida (pasta "assets" ao lado deste arquivo):
    assets/
        icone_janela.ico      -> ícone da janela (opcional)
        icone_cama.png        -> ícone pequeno da barra de título (24x24)
        foto_quarto.png       -> foto do quarto (lado esquerdo)
        icone_usuario.png     -> ícone grande do topo do login (64x64)
        icone_campo_user.png  -> ícone do campo "Usuário" (20x20)
        icone_campo_senha.png -> ícone do campo "Senha" (20x20)
        icone_seta.png        -> ícone da seta no botão "Entrar" (20x20)
        onda_laranja.png      -> (opcional) onda decorativa laranja/azul
"""

import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image

# ----------------------------------------------------------------------
# CONFIGURAÇÕES GERAIS
# ----------------------------------------------------------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Paleta de cores (aproximada da imagem)
AZUL_ESCURO = "#1B3A7A"
AZUL_HOVER = "#142C5E"
LARANJA = "#F59A1B"
FUNDO_DIREITO = "#F4F6FB"
BORDA_CAMPO = "#D5DAE6"
TEXTO_CINZA = "#555B6E"


def carregar_imagem(nome_arquivo, tamanho):
    """
    Carrega uma imagem da pasta assets e devolve um CTkImage.
    Se o arquivo não existir, retorna None (o layout continua funcionando
    com um espaço reservado no lugar da imagem).
    """
    caminho = os.path.join(ASSETS_DIR, nome_arquivo)
    if not os.path.exists(caminho):
        return None
    img = Image.open(caminho)
    return ctk.CTkImage(light_image=img, dark_image=img, size=tamanho)


class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --------------------------------------------------------------
        # JANELA
        # --------------------------------------------------------------
        self.title("Sistema de Reservas - Hotel")
        self.geometry("860x600")
        self.resizable(False, False)
        self.configure(fg_color=FUNDO_DIREITO)

        # >>> IMAGEM: ÍCONE DA JANELA (.ico) <<<
        # caminho_ico = os.path.join(ASSETS_DIR, "icone_janela.ico")
        # if os.path.exists(caminho_ico):
        #     self.iconbitmap(caminho_ico)

        self._criar_barra_titulo_interna()
        self._criar_painel_esquerdo()
        self._criar_painel_direito()

    # ------------------------------------------------------------------
    # BARRA SUPERIOR (visual de "título" azul escuro)
    # ------------------------------------------------------------------
    def _criar_barra_titulo_interna(self):
        self.barra = ctk.CTkFrame(self, height=40, fg_color=AZUL_ESCURO, corner_radius=0)
        self.barra.pack(side="top", fill="x")
        self.barra.pack_propagate(False)

        # >>> IMAGEM: ÍCONE DA CAMA (barra de título) - 24x24 <<<
        self.img_icone_cama = carregar_imagem("icone_cama.png", (24, 24))
        lbl_icone = ctk.CTkLabel(
            self.barra,
            text="" if self.img_icone_cama else "🛏",
            image=self.img_icone_cama,
            text_color="white",
            font=ctk.CTkFont(size=18),
        )
        lbl_icone.pack(side="left", padx=(14, 6))

        ctk.CTkLabel(
            self.barra,
            text="Sistema de Reservas - Hotel",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        ).pack(side="left")

        # Botão fechar (X) - opcional, pois a janela já tem o seu próprio
        ctk.CTkButton(
            self.barra, text="✕", width=36, height=28,
            fg_color="transparent", hover_color="#C0392B",
            text_color="white", corner_radius=4,
            command=self.destroy,
        ).pack(side="right", padx=8)

    # ------------------------------------------------------------------
    # PAINEL ESQUERDO (foto do quarto + onda decorativa)
    # ------------------------------------------------------------------
    def _criar_painel_esquerdo(self):
        self.painel_esq = ctk.CTkFrame(self, width=420, corner_radius=0, fg_color="#E9E4DA")
        self.painel_esq.pack(side="left", fill="y")
        self.painel_esq.pack_propagate(False)

        # >>> IMAGEM: FOTO DO QUARTO (lado esquerdo) - ~420x560 <<<
        # Coloque o arquivo em assets/foto_quarto.png
        self.img_quarto = carregar_imagem("img_login.jpg", (420, 560))
        self.lbl_foto = ctk.CTkLabel(
            self.painel_esq,
            text="" if self.img_quarto else "[ FOTO DO QUARTO ]\nassets/foto_quarto.png",
            image=self.img_quarto,
            text_color="#8A8577",
            font=ctk.CTkFont(size=14),
        )
        self.lbl_foto.place(x=0, y=0, relwidth=1, relheight=1)

        # >>> IMAGEM: ONDA DECORATIVA (laranja/azul na base da foto) <<<
        # Opcional: PNG com fundo transparente, ~420x120
        self.img_onda = carregar_imagem("onda_laranja.png", (420, 120))
        if self.img_onda:
            lbl_onda = ctk.CTkLabel(self.painel_esq, text="", image=self.img_onda,
                                    fg_color="transparent")
            lbl_onda.place(x=0, rely=1.0, anchor="sw")

    # ------------------------------------------------------------------
    # PAINEL DIREITO (formulário de login)
    # ------------------------------------------------------------------
    def _criar_painel_direito(self):
        self.painel_dir = ctk.CTkFrame(self, corner_radius=0, fg_color=FUNDO_DIREITO)
        self.painel_dir.pack(side="left", fill="both", expand=True)

        form = ctk.CTkFrame(self.painel_dir, fg_color="transparent")
        form.place(relx=0.5, rely=0.5, anchor="center")

        # >>> IMAGEM: ÍCONE DE USUÁRIO (topo do login) - 64x64 <<<
        self.img_user_topo = carregar_imagem("icone_usuario.png", (64, 64))
        ctk.CTkLabel(
            form,
            text="" if self.img_user_topo else "👤",
            image=self.img_user_topo,
            text_color=AZUL_ESCURO,
            font=ctk.CTkFont(size=52),
        ).pack(pady=(0, 6))

        ctk.CTkLabel(
            form, text="Login",
            text_color=AZUL_ESCURO,
            font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
        ).pack()

        ctk.CTkLabel(
            form, text="Acesse sua conta para continuar",
            text_color=TEXTO_CINZA,
            font=ctk.CTkFont(family="Segoe UI", size=13),
        ).pack(pady=(2, 22))

        # --- Campo Usuário ---
        self.entry_usuario = self._criar_campo(
            form, placeholder="Usuário",
            icone_arquivo="icone_campo_user.png", icone_fallback="👤",
        )

        # --- Campo Senha ---
        self.entry_senha = self._criar_campo(
            form, placeholder="Senha", mostrar="•",
            icone_arquivo="icone_campo_senha.png", icone_fallback="🔒",
        )

        # --- Botão Entrar ---
        # >>> IMAGEM: ÍCONE DA SETA (botão Entrar) - 20x20 <<<
        self.img_seta = carregar_imagem("icone_seta.png", (20, 20))
        self.btn_entrar = ctk.CTkButton(
            form,
            text="  Entrar",
            image=self.img_seta,
            compound="left",
            width=340, height=48,
            corner_radius=10,
            fg_color=AZUL_ESCURO, hover_color=AZUL_HOVER,
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            command=self.ao_clicar_entrar,
        )
        if not self.img_seta:
            self.btn_entrar.configure(text="→  Entrar")
        self.btn_entrar.pack(pady=(10, 22))

        # Linha separadora
        ctk.CTkFrame(form, height=1, width=340, fg_color=BORDA_CAMPO).pack(pady=(0, 14))

        # --- Rodapé: "Não tem conta? Cadastre-se" ---
        rodape = ctk.CTkFrame(form, fg_color="transparent")
        rodape.pack()
        ctk.CTkLabel(
            rodape, text="Não tem conta?",
            text_color=TEXTO_CINZA,
            font=ctk.CTkFont(family="Segoe UI", size=12),
        ).pack(side="left")

        lbl_cadastro = ctk.CTkLabel(
            rodape, text=" Cadastre-se",
            text_color=LARANJA, cursor="hand2",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold", underline=True),
        )
        lbl_cadastro.pack(side="left")
        lbl_cadastro.bind("<Button-1>", lambda e: self.ao_clicar_cadastrar())

        # Enter no teclado dispara o login
        self.bind("<Return>", lambda e: self.ao_clicar_entrar())

    # ------------------------------------------------------------------
    # COMPONENTE REUTILIZÁVEL: campo com ícone à esquerda
    # ------------------------------------------------------------------
    def _criar_campo(self, parent, placeholder, icone_arquivo, icone_fallback, mostrar=None):
        moldura = ctk.CTkFrame(
            parent, width=340, height=46, corner_radius=10,
            fg_color="white", border_width=1, border_color=BORDA_CAMPO,
        )
        moldura.pack(pady=7)
        moldura.pack_propagate(False)

        # >>> IMAGEM: ÍCONE DO CAMPO - 20x20 <<<
        img = carregar_imagem(icone_arquivo, (20, 20))
        # Guarda a referência para o Python não descartar a imagem
        if not hasattr(self, "_refs_imagens"):
            self._refs_imagens = []
        self._refs_imagens.append(img)

        # CORREÇÃO DA BORDA:
        # - fg_color explícito ("white") em vez de "transparent", para o ícone
        #   e o campo terem exatamente a mesma cor da moldura;
        # - pady/padx deixam uma folga para a borda arredondada ficar visível
        #   (antes os widgets cobriam a borda e os cantos).
        ctk.CTkLabel(
            moldura,
            text="" if img else icone_fallback,
            image=img,
            text_color=AZUL_ESCURO,
            fg_color="white",
            width=30,
            font=ctk.CTkFont(size=15),
        ).pack(side="left", padx=(10, 0), pady=3)

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

    # ------------------------------------------------------------------
    # AÇÕES (conecte aqui ao seu controller / banco de dados)
    # ------------------------------------------------------------------
    def ao_clicar_entrar(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()
        print(f"Tentativa de login -> usuário: {usuario!r}, senha: {'*' * len(senha)}")
        # TODO: validar credenciais e abrir a próxima tela

    def ao_clicar_cadastrar(self):
        print("Abrir tela de cadastro")
        # TODO: abrir a view de cadastro


if __name__ == "__main__":
    app = LoginView()
    app.mainloop()