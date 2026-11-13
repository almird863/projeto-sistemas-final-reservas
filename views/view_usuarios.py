"""
view_usuarios.py
----------------
Tela "Usuários" (Minha conta): dados de quem está logado, reserva atual e
histórico de reservas.

É uma TelaBase como as demais: aparece DENTRO da janela principal, ao lado da
sidebar. Quem escolhe os dados é o control_usuario; aqui só desenhamos.
"""

from tkinter import ttk

import customtkinter as ctk

from controls.control_usuario import carregar_conta
from views.componentes import (
    AZUL_ESCURO, AZUL_HOVER, LARANJA, LARANJA_HOVER, TEXTO_CINZA, VERMELHO,
)
from views.view_menu_principal import TelaBase, BRANCO, BORDA_CARD, FONTE

TEXTO_ESCURO = "#1F2937"
VERDE = "#2E8B57"

COR_STATUS = {
    "Em andamento": LARANJA,
    "Futura": AZUL_ESCURO,
    "Concluída": VERDE,
    "Cancelada": VERMELHO,
}


class TelaUsuarios(TelaBase):
    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_columnconfigure((0, 1), weight=1, uniform="cards")
        self.grid_rowconfigure(3, weight=1)

        self._configurar_estilo_tabela()
        self._criar_cabecalho()
        self._criar_card_perfil()
        self._criar_card_reserva_atual()
        self._criar_card_historico()

    # --- Montagem da tela ---------------------------------------------
    def _configurar_estilo_tabela(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")  # tema que aceita cor no cabeçalho
        estilo.configure("Hotel.Treeview", background=BRANCO, fieldbackground=BRANCO,
                         foreground=TEXTO_ESCURO, rowheight=28, borderwidth=0,
                         font=(FONTE, 11))
        estilo.configure("Hotel.Treeview.Heading", background=AZUL_ESCURO,
                         foreground=BRANCO, font=(FONTE, 11, "bold"), relief="flat")
        estilo.map("Hotel.Treeview.Heading", background=[("active", AZUL_HOVER)])
        estilo.map("Hotel.Treeview", background=[("selected", "#FCE3BF")],
                   foreground=[("selected", AZUL_ESCURO)])

    def _criar_cabecalho(self):
        cab = ctk.CTkFrame(self, fg_color="transparent")
        cab.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(20, 10))

        textos = ctk.CTkFrame(cab, fg_color="transparent")
        textos.pack(side="left")
        ctk.CTkLabel(textos, text="Minha conta", font=(FONTE, 28, "bold"),
                     text_color=AZUL_ESCURO).pack(anchor="w")
        ctk.CTkLabel(textos, text="Seus dados, reserva atual e histórico de reservas.",
                     font=(FONTE, 13), text_color=TEXTO_CINZA).pack(anchor="w")

        ctk.CTkButton(
            cab, text="🔄  Atualizar", font=(FONTE, 13, "bold"), width=130, height=38,
            fg_color=LARANJA, hover_color=LARANJA_HOVER, text_color=BRANCO,
            corner_radius=8, command=self.carregar,
        ).pack(side="right")

    def _criar_card(self, titulo, **posicao):
        """Card branco com faixa azul no topo (mesmo visual dos mockups)."""
        card = ctk.CTkFrame(self, fg_color=BRANCO, corner_radius=12,
                            border_width=1, border_color=BORDA_CARD)
        card.grid(**posicao)
        faixa = ctk.CTkFrame(card, fg_color=AZUL_ESCURO, corner_radius=10, height=38)
        faixa.pack(fill="x")
        ctk.CTkLabel(faixa, text=titulo, font=(FONTE, 15, "bold"),
                     text_color=BRANCO).pack(side="left", padx=14, pady=6)
        corpo = ctk.CTkFrame(card, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=14, pady=10)
        return corpo

    def _linhas_de_dados(self, corpo, rotulos):
        """Cria pares 'Rótulo: valor' e devolve {chave: label do valor}."""
        corpo.grid_columnconfigure(1, weight=1)
        valores = {}
        for linha, (chave, rotulo) in enumerate(rotulos):
            ctk.CTkLabel(corpo, text=rotulo, font=(FONTE, 12), text_color=TEXTO_CINZA,
                         anchor="w").grid(row=linha, column=0, sticky="w", pady=2)
            valores[chave] = ctk.CTkLabel(corpo, text="—", font=(FONTE, 13, "bold"),
                                          text_color=TEXTO_ESCURO, anchor="w")
            valores[chave].grid(row=linha, column=1, sticky="w", padx=(12, 0), pady=2)
        return valores

    def _criar_card_perfil(self):
        corpo = self._criar_card("Dados do usuário", row=1, column=0,
                                 sticky="nsew", padx=(30, 8), pady=(0, 12))
        self.perfil = self._linhas_de_dados(corpo, [
            ("nome", "Nome"), ("cpf", "CPF"), ("idade", "Idade"), ("cidade", "Cidade de origem"),
        ])
        self.aviso_perfil = ctk.CTkLabel(corpo, text="", font=(FONTE, 11),
                                         text_color=VERMELHO, anchor="w")
        self.aviso_perfil.grid(row=4, column=0, columnspan=2, sticky="w", pady=(6, 0))

    def _criar_card_reserva_atual(self):
        corpo = self._criar_card("Reserva atual", row=1, column=1,
                                 sticky="nsew", padx=(8, 30), pady=(0, 12))

        # Estado "com reserva"
        self.quadro_reserva = ctk.CTkFrame(corpo, fg_color="transparent")
        self.selo_status = ctk.CTkLabel(
            self.quadro_reserva, text="", font=(FONTE, 11, "bold"), text_color=BRANCO,
            corner_radius=8, height=24, width=110)
        self.selo_status.pack(anchor="w", pady=(0, 6))
        dados = ctk.CTkFrame(self.quadro_reserva, fg_color="transparent")
        dados.pack(fill="x")
        self.reserva = self._linhas_de_dados(dados, [
            ("apartamento", "Apartamento"), ("entrada", "Check-in"),
            ("saida", "Check-out"), ("pessoas", "Pessoas"), ("valor", "Valor"),
        ])

        # Estado "sem reserva"
        self.quadro_vazio = ctk.CTkFrame(corpo, fg_color="transparent")
        ctk.CTkLabel(self.quadro_vazio, text="Você não possui uma reserva ativa.",
                     font=(FONTE, 13), text_color=TEXTO_CINZA).pack(pady=(14, 10))
        ctk.CTkButton(
            self.quadro_vazio, text="🛏  Realizar reserva", font=(FONTE, 13, "bold"),
            fg_color=AZUL_ESCURO, hover_color=AZUL_HOVER, text_color=BRANCO,
            corner_radius=8, height=38,
            command=lambda: self.app.mostrar_tela("reservas"),
        ).pack()

    def _criar_card_historico(self):
        corpo = self._criar_card("Histórico de reservas", row=3, column=0, columnspan=2,
                                 sticky="nsew", padx=30, pady=(0, 20))

        colunas = [("id", "Código", 70, "center"), ("apartamento", "Apartamento", 150, "center"),
                   ("entrada", "Check-in", 100, "center"), ("saida", "Check-out", 100, "center"),
                   ("status", "Status", 110, "center"), ("valor", "Valor", 110, "e")]

        area = ctk.CTkFrame(corpo, fg_color="transparent")
        area.pack(fill="both", expand=True)

        self.tabela = ttk.Treeview(area, columns=[c[0] for c in colunas], show="headings",
                                   height=5, style="Hotel.Treeview")
        for chave, titulo, largura, alinhamento in colunas:
            self.tabela.heading(chave, text=titulo)
            self.tabela.column(chave, width=largura, anchor=alinhamento)

        barra = ctk.CTkScrollbar(area, command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        self.tabela.pack(side="left", fill="both", expand=True)

        self.lbl_historico_vazio = ctk.CTkLabel(
            corpo, text="Nenhuma reserva anterior encontrada.",
            font=(FONTE, 12), text_color=TEXTO_CINZA)

    # --- Dados --------------------------------------------------------
    def ao_exibir(self):
        """Roda toda vez que a pessoa abre 'Usuários' (dados sempre frescos)."""
        self.carregar()

    def carregar(self):
        conta = carregar_conta(getattr(self.app, "usuario", ""))
        self._preencher_perfil(conta["perfil"])
        self._preencher_reserva_atual(conta["atual"])
        self._preencher_historico(conta["historico"])

    def _preencher_perfil(self, perfil):
        for chave, label in self.perfil.items():
            label.configure(text=str(perfil[chave]))
        self.aviso_perfil.configure(
            text="" if perfil["encontrado"] else "Usuário não encontrado no banco de dados.")

    def _preencher_reserva_atual(self, reserva):
        if not reserva:
            self.quadro_reserva.pack_forget()
            self.quadro_vazio.pack(fill="both", expand=True)
            return
        self.quadro_vazio.pack_forget()
        self.quadro_reserva.pack(fill="both", expand=True)
        self.selo_status.configure(text=reserva["status"],
                                   fg_color=COR_STATUS.get(reserva["status"], AZUL_ESCURO))
        for chave, label in self.reserva.items():
            label.configure(text=str(reserva[chave]))

    def _preencher_historico(self, reservas):
        self.tabela.delete(*self.tabela.get_children())
        for r in reservas:
            self.tabela.insert("", "end", values=(
                r["id"], r["apartamento"], r["entrada"], r["saida"], r["status"], r["valor"]))
        if reservas:
            self.lbl_historico_vazio.pack_forget()
        else:
            self.lbl_historico_vazio.pack(pady=(0, 6))
