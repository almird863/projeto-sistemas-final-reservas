import customtkinter as ctk
from tkinter import ttk

from controls.control_cliente import ControlCliente
from controls.control_reserva import ControlReserva
from views.componentes import criar_botao, criar_titulo


class ViewUsuarios(ctk.CTkToplevel):
    def __init__(self, usuario_logado, voltar_callback=None):
        super().__init__()

        self.usuario_logado = usuario_logado
        self.voltar_callback = voltar_callback

        self.control_cliente = ControlCliente()
        self.control_reserva = ControlReserva()

        self.title("Meu perfil e reservas")
        self.geometry("980x640")
        self.configure(fg_color="#FFF7ED")

        self.criar_cabecalho()
        self.criar_cartao_perfil()
        self.criar_cartao_reserva_atual()
        self.criar_tabela_historico()
        self.criar_botoes()

        self.carregar_dados()

    def criar_cabecalho(self):
        titulo = criar_titulo(self, "Minha conta")
        titulo.pack(pady=(24, 10))

    def criar_cartao_perfil(self):
        card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=16)
        card.pack(fill="x", padx=30, pady=(0, 16))

        ctk.CTkLabel(
            card,
            text="Dados do usuário",
            font=("Arial", 18, "bold"),
            text_color="#1F2937"
        ).pack(anchor="w", padx=24, pady=(18, 8))

        self.lbl_nome = ctk.CTkLabel(
            card,
            text="Nome: —",
            font=("Arial", 14),
            text_color="#374151"
        )
        self.lbl_nome.pack(anchor="w", padx=24, pady=2)

        self.lbl_email = ctk.CTkLabel(
            card,
            text="E-mail: —",
            font=("Arial", 14),
            text_color="#374151"
        )
        self.lbl_email.pack(anchor="w", padx=24, pady=2)

        self.lbl_telefone = ctk.CTkLabel(
            card,
            text="Telefone: —",
            font=("Arial", 14),
            text_color="#374151"
        )
        self.lbl_telefone.pack(anchor="w", padx=24, pady=(2, 18))

    def criar_cartao_reserva_atual(self):
        card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=16)
        card.pack(fill="x", padx=30, pady=(0, 16))

        ctk.CTkLabel(
            card,
            text="Reserva atual",
            font=("Arial", 18, "bold"),
            text_color="#1F2937"
        ).pack(anchor="w", padx=24, pady=(18, 8))

        self.lbl_reserva = ctk.CTkLabel(
            card,
            text="Você não possui uma reserva ativa.",
            font=("Arial", 14),
            text_color="#374151",
            justify="left"
        )
        self.lbl_reserva.pack(anchor="w", padx=24, pady=(2, 18))

    def criar_tabela_historico(self):
        card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=16)
        card.pack(fill="both", expand=True, padx=30, pady=(0, 16))

        ctk.CTkLabel(
            card,
            text="Histórico de reservas",
            font=("Arial", 18, "bold"),
            text_color="#1F2937"
        ).pack(anchor="w", padx=24, pady=(18, 8))

        colunas = ("id", "apartamento", "entrada", "saida", "status", "valor")

        self.tabela = ttk.Treeview(
            card,
            columns=colunas,
            show="headings",
            height=8
        )

        self.tabela.heading("id", text="Código")
        self.tabela.heading("apartamento", text="Apartamento")
        self.tabela.heading("entrada", text="Check-in")
        self.tabela.heading("saida", text="Check-out")
        self.tabela.heading("status", text="Status")
        self.tabela.heading("valor", text="Valor")

        self.tabela.column("id", width=70, anchor="center")
        self.tabela.column("apartamento", width=130, anchor="center")
        self.tabela.column("entrada", width=120, anchor="center")
        self.tabela.column("saida", width=120, anchor="center")
        self.tabela.column("status", width=120, anchor="center")
        self.tabela.column("valor", width=120, anchor="e")

        self.tabela.pack(fill="both", expand=True, padx=20, pady=(0, 18))

    def criar_botoes(self):
        area_botoes = ctk.CTkFrame(self, fg_color="transparent")
        area_botoes.pack(fill="x", padx=30, pady=(0, 24))

        criar_botao(
            area_botoes,
            texto="Atualizar",
            comando=self.carregar_dados
        ).pack(side="left", padx=(0, 12))

        criar_botao(
            area_botoes,
            texto="Voltar",
            comando=self.voltar
        ).pack(side="left")

    def voltar(self):
        self.destroy()

        if self.voltar_callback:
            self.voltar_callback()

    def carregar_dados(self):
        self.carregar_perfil()
        self.carregar_reserva_atual()
        self.carregar_historico()

    def carregar_perfil(self):
        cliente = self.control_cliente.buscar_por_id(
            self.usuario_logado.get("id")
        )

        if not cliente:
            self.lbl_nome.configure(text="Nome: usuário não encontrado")
            return

        self.lbl_nome.configure(text=f"Nome: {cliente.nome}")
        self.lbl_email.configure(text=f"E-mail: {cliente.email}")
        self.lbl_telefone.configure(text=f"Telefone: {cliente.telefone}")

    def carregar_reserva_atual(self):
        reserva = self.control_reserva.buscar_reserva_ativa(
            self.usuario_logado.get("id")
        )

        if not reserva:
            self.lbl_reserva.configure(
                text="Você não possui uma reserva ativa."
            )
            return

        self.lbl_reserva.configure(
            text=(
                f"Reserva nº {reserva.id}\n"
                f"Apartamento: {reserva.apartamento}\n"
                f"Check-in: {reserva.data_entrada}\n"
                f"Check-out: {reserva.data_saida}\n"
                f"Status: {reserva.status}"
            )
        )

    def carregar_historico(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        reservas = self.control_reserva.buscar_historico(
            self.usuario_logado.get("id")
        )

        for reserva in reservas:
            self.tabela.insert(
                "",
                "end",
                values=(
                    reserva.id,
                    reserva.apartamento,
                    reserva.data_entrada,
                    reserva.data_saida,
                    reserva.status,
                    reserva.valor
                )
            )