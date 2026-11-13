"""
view_usuarios.py
-----------------
Tela "Minha conta" do Sistema de Reservas - Hotel.

Segue o mesmo padrão das demais telas do menu principal (TelaBase, dentro
do container da sidebar) em vez de uma janela separada (CTkToplevel), para
ficar igual a TelaInicio e TelaReservas.

Mostra:
 - Dados do usuário logado (nome, CPF, idade, cidade de origem)
 - Reserva atual (se houver)
 - Histórico de reservas já encerradas

Rodar junto do sistema: a tela é aberta pelo item "Usuários" da sidebar
(ver view_menu_principal.py -> _registrar_telas).
"""

from tkinter import ttk
import customtkinter as ctk

from controls.control_usuario import carregar_conta
from views.componentes import (
    AZUL_ESCURO, TEXTO_CINZA, FUNDO_DIREITO, criar_botao, criar_titulo,
)

try:
    from views.view_menu_principal import TelaBase
except ImportError:
    class TelaBase(ctk.CTkFrame):
        def __init__(self, master, app=None, **kwargs):
            super().__init__(master, fg_color=FUNDO_DIREITO, corner_radius=0, **kwargs)
            self.app = app

        def ao_exibir(self):
            pass

FONTE = "Segoe UI"
BORDA_CARD = "#DCE4F0"


class ViewUsuarios(TelaBase):
    """
    Tela "Minha conta". Instanciada dentro do container do menu principal,
    assim como TelaInicio e TelaReservas.

    O usuário logado é identificado por app.usuario (o CPF, guardado em
    JanelaPrincipal a partir do login — ver main.py / view_login.py).
    """

    def __init__(self, master, app=None, **kwargs):
        super().__init__(master, app, **kwargs)

        self._criar_cabecalho()
        self._criar_cartao_perfil()
        self._criar_cartao_reserva_atual()
        self._criar_tabela_historico()
        self._criar_botoes()

    def ao_exibir(self):
        """Chamado toda vez que a tela é exibida pela sidebar: recarrega os dados."""
        self.carregar_dados()

    # ------------------------------------------------------------------
    # 1. CABEÇALHO
    # ------------------------------------------------------------------
    def _criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(self, fg_color="transparent")
        cabecalho.pack(fill="x", padx=25, pady=(15, 10))

        ctk.CTkLabel(
            cabecalho, text="👤", font=(FONTE, 32), text_color=AZUL_ESCURO
        ).pack(side="left", padx=(0, 12))

        textos = ctk.CTkFrame(cabecalho, fg_color="transparent")
        textos.pack(side="left", fill="both")

        criar_titulo(textos, "Minha conta").pack(anchor="w")

        ctk.CTkLabel(
            textos, text="Seus dados, sua reserva atual e o histórico de estadias",
            font=ctk.CTkFont(family=FONTE, size=13),
            text_color=TEXTO_CINZA,
        ).pack(anchor="w")

    # ------------------------------------------------------------------
    # 2. CARTÃO DE DADOS DO USUÁRIO
    # ------------------------------------------------------------------
    def _criar_cartao_perfil(self):
        card = ctk.CTkFrame(
            self, fg_color="white", corner_radius=12,
            border_width=1, border_color=BORDA_CARD
        )
        card.pack(fill="x", padx=25, pady=(0, 14))

        ctk.CTkLabel(
            card, text="Dados do usuário",
            font=ctk.CTkFont(family=FONTE, size=16, weight="bold"),
            text_color=AZUL_ESCURO
        ).pack(anchor="w", padx=20, pady=(16, 8))

        self.lbl_nome = ctk.CTkLabel(
            card, text="Nome: —", font=(FONTE, 13), text_color=TEXTO_CINZA
        )
        self.lbl_nome.pack(anchor="w", padx=20, pady=2)

        self.lbl_cpf = ctk.CTkLabel(
            card, text="CPF: —", font=(FONTE, 13), text_color=TEXTO_CINZA
        )
        self.lbl_cpf.pack(anchor="w", padx=20, pady=2)

        self.lbl_idade = ctk.CTkLabel(
            card, text="Idade: —", font=(FONTE, 13), text_color=TEXTO_CINZA
        )
        self.lbl_idade.pack(anchor="w", padx=20, pady=2)

        self.lbl_cidade = ctk.CTkLabel(
            card, text="Cidade de origem: —", font=(FONTE, 13), text_color=TEXTO_CINZA
        )
        self.lbl_cidade.pack(anchor="w", padx=20, pady=(2, 16))

    # ------------------------------------------------------------------
    # 3. CARTÃO DE RESERVA ATUAL
    # ------------------------------------------------------------------
    def _criar_cartao_reserva_atual(self):
        card = ctk.CTkFrame(
            self, fg_color="white", corner_radius=12,
            border_width=1, border_color=BORDA_CARD
        )
        card.pack(fill="x", padx=25, pady=(0, 14))

        ctk.CTkLabel(
            card, text="Reserva atual",
            font=ctk.CTkFont(family=FONTE, size=16, weight="bold"),
            text_color=AZUL_ESCURO
        ).pack(anchor="w", padx=20, pady=(16, 8))

        self.lbl_reserva = ctk.CTkLabel(
            card, text="Você não possui uma reserva ativa.",
            font=(FONTE, 13), text_color=TEXTO_CINZA, justify="left"
        )
        self.lbl_reserva.pack(anchor="w", padx=20, pady=(2, 16))

    # ------------------------------------------------------------------
    # 4. TABELA DE HISTÓRICO
    # ------------------------------------------------------------------
    def _criar_tabela_historico(self):
        card = ctk.CTkFrame(
            self, fg_color="white", corner_radius=12,
            border_width=1, border_color=BORDA_CARD
        )
        card.pack(fill="both", expand=True, padx=25, pady=(0, 14))

        ctk.CTkLabel(
            card, text="Histórico de reservas",
            font=ctk.CTkFont(family=FONTE, size=16, weight="bold"),
            text_color=AZUL_ESCURO
        ).pack(anchor="w", padx=20, pady=(16, 8))

        colunas = ("id", "apartamento", "entrada", "saida", "status", "valor")

        self.tabela = ttk.Treeview(
            card, columns=colunas, show="headings", height=8
        )

        self.tabela.heading("id", text="Código")
        self.tabela.heading("apartamento", text="Apartamento")
        self.tabela.heading("entrada", text="Check-in")
        self.tabela.heading("saida", text="Check-out")
        self.tabela.heading("status", text="Status")
        self.tabela.heading("valor", text="Valor")

        self.tabela.column("id", width=70, anchor="center")
        self.tabela.column("apartamento", width=160, anchor="center")
        self.tabela.column("entrada", width=110, anchor="center")
        self.tabela.column("saida", width=110, anchor="center")
        self.tabela.column("status", width=110, anchor="center")
        self.tabela.column("valor", width=110, anchor="e")

        self.tabela.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    # ------------------------------------------------------------------
    # 5. BOTÕES
    # ------------------------------------------------------------------
    def _criar_botoes(self):
        area_botoes = ctk.CTkFrame(self, fg_color="transparent")
        area_botoes.pack(fill="x", padx=25, pady=(0, 20))

        criar_botao(
            area_botoes, texto="Atualizar", comando=self.carregar_dados
        ).pack(side="left")

    # ------------------------------------------------------------------
    # CARREGAMENTO DE DADOS
    # ------------------------------------------------------------------
    def carregar_dados(self):
        conta = carregar_conta(self._cpf_usuario_logado())
        self._carregar_perfil(conta["perfil"])
        self._carregar_reserva_atual(conta["atual"])
        self._carregar_historico(conta["historico"])

    def _cpf_usuario_logado(self):
        """app.usuario guarda o CPF de quem fez login (string), não um dict."""
        return getattr(self.app, "usuario", "") if self.app else ""

    def _carregar_perfil(self, perfil):
        if not perfil["encontrado"]:
            self.lbl_nome.configure(text="Nome: usuário não encontrado")
            self.lbl_cpf.configure(text="CPF: —")
            self.lbl_idade.configure(text="Idade: —")
            self.lbl_cidade.configure(text="Cidade de origem: —")
            return

        self.lbl_nome.configure(text=f"Nome: {perfil['nome']}")
        self.lbl_cpf.configure(text=f"CPF: {perfil['cpf']}")
        self.lbl_idade.configure(text=f"Idade: {perfil['idade']}")
        self.lbl_cidade.configure(text=f"Cidade de origem: {perfil['cidade']}")

    def _carregar_reserva_atual(self, reserva):
        if not reserva:
            self.lbl_reserva.configure(text="Você não possui uma reserva ativa.")
            return

        self.lbl_reserva.configure(
            text=(
                f"Reserva nº {reserva['id']}\n"
                f"Apartamento: {reserva['apartamento']}\n"
                f"Check-in: {reserva['entrada']}\n"
                f"Check-out: {reserva['saida']}\n"
                f"Status: {reserva['status']}"
            )
        )

    def _carregar_historico(self, reservas):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for reserva in reservas:
            self.tabela.insert(
                "", "end",
                values=(
                    reserva["id"],
                    reserva["apartamento"],
                    reserva["entrada"],
                    reserva["saida"],
                    reserva["status"],
                    reserva["valor"].replace(".", ","),
                )
            )


# ----------------------------------------------------------------------
# TESTE ISOLADO DA TELA: python -m views.view_usuarios
# ----------------------------------------------------------------------
if __name__ == "__main__":
    class _AppFake:
        usuario = "12345678900"  # troque por um CPF cadastrado no banco p/ testar

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    janela = ctk.CTk()
    janela.title("Sistema de Reservas - Hotel")
    janela.geometry("1000x680")

    tela = ViewUsuarios(janela, app=_AppFake())
    tela.pack(fill="both", expand=True)
    tela.ao_exibir()

    janela.mainloop()