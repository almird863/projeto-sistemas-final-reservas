"""
view_menu_principal.py
----------------------
Janela principal do Sistema de Reservas - Hotel.

Estrutura:
    JanelaPrincipal (CTk)
     ├── Sidebar (fixa, à esquerda)
     └── container (à direita) -> mostra UMA tela por vez

Rodar SEMPRE da raiz do projeto:  python -m views.view_menu_principal

Para adicionar uma tela nova (Reservas, Apartamentos...), basta:
    1. Criar uma classe que herda de TelaBase
    2. Registrar em JanelaPrincipal._registrar_telas()
A sidebar não precisa ser alterada.
"""

from tkinter import messagebox

import customtkinter as ctk

from views.componentes import (
    AZUL_ESCURO, AZUL_HOVER, LARANJA, LARANJA_HOVER, FUNDO_DIREITO, TEXTO_CINZA,
    carregar_imagem, criar_barra_titulo, montar_imagem_lateral,
)

# Cores/fonte usadas só aqui (as demais vêm do componentes.py)
BRANCO = "#FFFFFF"
HOVER_CARD = "#E8EEF8"
BORDA_CARD = "#DCE4F0"
FONTE = "Segoe UI"
LARGURA_SIDEBAR = 210


# ----------------------------------------------------------------------
# Tela base: toda tela do sistema herda daqui
# ----------------------------------------------------------------------
class TelaBase(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, fg_color=FUNDO_DIREITO, corner_radius=0, **kwargs)
        self.app = app  # JanelaPrincipal: use self.app.mostrar_tela("nome")

    def ao_exibir(self):
        """Chamado toda vez que a tela aparece (útil para recarregar dados)."""
        pass


class TelaEmConstrucao(TelaBase):
    """Placeholder para as telas que ainda não foram feitas."""

    def __init__(self, master, app, titulo="Em construção"):
        super().__init__(master, app)
        ctk.CTkLabel(
            self, text=titulo, font=(FONTE, 28, "bold"), text_color=AZUL_ESCURO
        ).pack(pady=(40, 6), padx=30, anchor="w")
        ctk.CTkLabel(
            self, text="Esta tela será implementada em breve.",
            font=(FONTE, 14), text_color=TEXTO_CINZA,
        ).pack(padx=30, anchor="w")


# ----------------------------------------------------------------------
# Tela Início
# ----------------------------------------------------------------------
class TelaInicio(TelaBase):
    # (texto, ícone, tela de destino)
    ATALHOS = [
        ("Verificar\nDisponibilidade", "📅", "reservas"),
        ("Realizar\nReserva", "🛏", "reservas"),
        ("Check-in", "✔", "checkinout"),
        ("Check-out", "🚪", "checkinout"),
    ]

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="Bem-vindo(a) ao Sistema!",
            font=(FONTE, 30, "bold"), text_color=AZUL_ESCURO,
        ).grid(row=0, column=0, sticky="w", padx=30, pady=(24, 0))

        ctk.CTkLabel(
            self, text="Gerencie suas reservas de forma simples e rápida.",
            font=(FONTE, 14), text_color=TEXTO_CINZA,
        ).grid(row=1, column=0, sticky="w", padx=30, pady=(0, 14))

        self._criar_banner().grid(row=2, column=0, sticky="ew", padx=30)
        self._criar_atalhos().grid(row=3, column=0, sticky="ew", padx=30, pady=18)

    def _criar_banner(self):
        # >>> IMAGEM: assets/lobby.jpg (700x190). Enquanto não existir, usa a
        # foto do quarto com a onda; se nem ela existir, um bloco azul.
        imagem = carregar_imagem("banner_interno.png", (700, 200)) or montar_imagem_lateral(700, 190, altura_onda=60)
        if imagem:
            self.img_banner = imagem  # guarda a referência
            return ctk.CTkLabel(self, text="", image=imagem)
        # Fallback caso a imagem ainda não esteja na pasta assets
        quadro = ctk.CTkFrame(self, fg_color=AZUL_ESCURO, corner_radius=16, height=190)
        quadro.grid_propagate(False)
        ctk.CTkLabel(
            quadro, text="(coloque assets/lobby.jpg para exibir o banner)",
            text_color=BRANCO, font=(FONTE, 13),
        ).place(relx=0.5, rely=0.5, anchor="center")
        return quadro

    def _criar_atalhos(self):
        linha = ctk.CTkFrame(self, fg_color="transparent")
        for col, (texto, icone, destino) in enumerate(self.ATALHOS):
            linha.grid_columnconfigure(col, weight=1, uniform="cards")
            ctk.CTkButton(
                linha,
                text=f"{icone}\n{texto}",
                font=(FONTE, 13, "bold"),
                text_color=AZUL_ESCURO,
                fg_color=BRANCO,
                hover_color=HOVER_CARD,
                border_width=1,
                border_color=BORDA_CARD,
                corner_radius=12,
                height=100,
                command=lambda d=destino: self.app.mostrar_tela(d),
            ).grid(row=0, column=col, padx=6, sticky="ew")
        return linha


# ----------------------------------------------------------------------
# Janela principal (sidebar + container de telas)
# ----------------------------------------------------------------------
class JanelaPrincipal(ctk.CTk):
    # (chave da tela, texto, ícone)
    MENU = [
        ("inicio", "Início", "🏠"),
        ("reservas", "Reservas", "📅"),
        ("apartamentos", "Apartamentos", "🏢"),
        ("usuarios", "Usuários", "👥"),
        ("checkinout", "Check-in /\nCheck-out", "✔"),
    ]

    def __init__(self, usuario: str = "", ao_sair=None):
        """
        usuario: nome de quem fez login (para uso futuro nas telas)
        ao_sair: função chamada ao clicar em Sair (ex.: reabrir o login)
        """
        super().__init__()
        self.usuario = usuario
        self.ao_sair = ao_sair

        self.title("Sistema de Reservas - Hotel")
        self.geometry("1000x620")
        self.minsize(900, 560)
        self.configure(fg_color=FUNDO_DIREITO)

        criar_barra_titulo(self)
        self.corpo = ctk.CTkFrame(self, fg_color=FUNDO_DIREITO, corner_radius=0)
        self.corpo.pack(side="top", fill="both", expand=True)
        self.corpo.grid_columnconfigure(1, weight=1)
        self.corpo.grid_rowconfigure(0, weight=1)

        self._telas_registradas = {}  # chave -> função que cria a tela
        self._telas_criadas = {}      # chave -> instância já criada
        self._botoes = {}             # chave -> botão da sidebar
        self._tela_atual = None

        self._criar_sidebar()
        self.container = ctk.CTkFrame(self.corpo, fg_color=FUNDO_DIREITO, corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self._registrar_telas()
        self.mostrar_tela("inicio")

    # --- Sidebar -------------------------------------------------------
    def _criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self.corpo, width=LARGURA_SIDEBAR, fg_color=AZUL_ESCURO, corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        for chave, texto, icone in self.MENU:
            self._botoes[chave] = self._botao_sidebar(
                f"{icone}   {texto}", lambda c=chave: self.mostrar_tela(c)
            )

        # Empurra o "Sair" para ficar após os outros, com espaço próprio
        self._botoes["sair"] = self._botao_sidebar("🚪   Sair", self._sair)

    def _botao_sidebar(self, texto, comando):
        botao = ctk.CTkButton(
            self.sidebar,
            text=texto,
            anchor="w",
            font=(FONTE, 14, "bold"),
            text_color=BRANCO,
            fg_color="transparent",
            hover_color=AZUL_HOVER,
            corner_radius=8,
            height=52,
            command=comando,
        )
        botao.pack(fill="x", padx=10, pady=(8, 0))
        return botao

    def _destacar_botao(self, chave):
        for k, botao in self._botoes.items():
            if k == "sair":
                continue
            ativo = k == chave
            botao.configure(
                fg_color=LARANJA if ativo else "transparent",
                hover_color=LARANJA_HOVER if ativo else AZUL_HOVER,
            )

    # --- Telas ---------------------------------------------------------
    def _registrar_telas(self):
        """Ponto único para plugar novas telas. Troque os placeholders
        pelas classes reais conforme forem ficando prontas."""
        self.registrar_tela("inicio", lambda: TelaInicio(self.container, self))
        self.registrar_tela(
            "reservas", lambda: TelaEmConstrucao(self.container, self, "Reservas"))
        self.registrar_tela(
            "apartamentos", lambda: TelaEmConstrucao(self.container, self, "Apartamentos"))
        self.registrar_tela(
            "usuarios", lambda: TelaEmConstrucao(self.container, self, "Usuários"))
        self.registrar_tela(
            "checkinout", lambda: TelaEmConstrucao(self.container, self, "Check-in / Check-out"))

    def registrar_tela(self, chave, fabrica):
        self._telas_registradas[chave] = fabrica

    def mostrar_tela(self, chave):
        if chave not in self._telas_registradas:
            return

        if self._tela_atual is not None:
            self._tela_atual.grid_forget()

        # Cria a tela só na primeira vez e reaproveita depois
        if chave not in self._telas_criadas:
            self._telas_criadas[chave] = self._telas_registradas[chave]()

        tela = self._telas_criadas[chave]
        tela.grid(row=0, column=0, sticky="nsew")
        tela.ao_exibir()

        self._tela_atual = tela
        self._destacar_botao(chave)

    # --- Sair ----------------------------------------------------------
    def _sair(self):
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            self.destroy()
            if self.ao_sair:
                self.ao_sair()


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    JanelaPrincipal(usuario="teste").mainloop()
