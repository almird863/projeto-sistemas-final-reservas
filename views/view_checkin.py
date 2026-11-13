"""
view_checkin.py
----------------
Tela de Check-in / Check-out do Sistema de Reservas - Hotel.

Segue o mesmo padrão das outras telas do menu principal (TelaBase, dentro
do container da sidebar), igual TelaInicio, TelaReservas e ViewUsuarios —
não é uma janela separada.

Mostra:
  - Card no topo com a PRÓXIMA reserva aguardando check-in (nº da reserva,
    apartamento, data de check-in) e um botão que alterna entre
    "Fazer Check-in" e "Fazer Check-out".
  - Lista abaixo com todas as reservas já concluídas (check-out feito),
    no mesmo estilo de card usado nas outras telas.

Rodar junto do sistema: a tela é aberta pelo item "Check-in / Check-out"
da sidebar (ver view_menu_principal.py -> _registrar_telas).

Depende de controls/control_reserva.py (ListarReservasParaCheckin,
ListarReservasConcluidas, FazerCheckin, FazerCheckout) e da coluna
checkin_feito em models/model_reserva.py.
"""

from datetime import datetime

import customtkinter as ctk

from views.componentes import (
    AZUL_ESCURO, AZUL_HOVER, LARANJA, LARANJA_HOVER, FUNDO_DIREITO,
    BORDA_CAMPO, TEXTO_CINZA, criar_titulo, criar_botao,
)
from controls.control_reserva import (
    ListarReservasParaCheckin,
    ListarReservasConcluidas,
    FazerCheckin,
    FazerCheckout,
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
MARGEM_LATERAL = 25

# Índices da tupla devolvida por ListarReservasParaCheckin / ListarReservasConcluidas
# (ver listar_db_reservas_para_checkin / listar_db_reservas_concluidas em model_reserva.py):
# (id, id_cliente, id_apto, data_entrada, data_saida, qt_pessoas, valor,
#  status, checkin_feito, numero_apto)


def _linha_para_dict(linha):
    (id_reserva, id_cliente, id_apto, data_entrada, data_saida,
     qt_pessoas, valor, status, checkin_feito, numero_apto) = linha
    return {
        "id": id_reserva,
        "id_cliente": id_cliente,
        "id_apto": id_apto,
        "apartamento": numero_apto if numero_apto is not None else f"(ID {id_apto})",
        "data_entrada": data_entrada,
        "data_saida": data_saida,
        "qt_pessoas": qt_pessoas,
        "valor": valor,
        "status": status,
        "checkin_feito": bool(checkin_feito),
    }


def _formatar_data(data_iso):
    """Converte 'AAAA-MM-DD' para 'DD/MM/AAAA'. Se não conseguir, devolve como veio."""
    try:
        return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return data_iso or "-"


class TelaCheckin(TelaBase):
    """Tela de Check-in / Check-out."""

    def __init__(self, master, app=None, **kwargs):
        super().__init__(master, app, **kwargs)

        self.fila_pendentes = []   # reservas aguardando check-in, nesta sessão
        self.reserva_atual = None  # dict da reserva em destaque no card (ou None)

        self._criar_cabecalho()
        self._montar_card_reserva()
        self._montar_lista_concluidas()

    def ao_exibir(self):
        """Chamado toda vez que a tela é exibida pela sidebar: recarrega os dados."""
        self.atualizar_tudo()

    # ------------------------------------------------------------------
    # CABEÇALHO (mesmo padrão de ViewUsuarios)
    # ------------------------------------------------------------------
    def _criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(self, fg_color="transparent")
        cabecalho.pack(fill="x", padx=MARGEM_LATERAL, pady=(15, 10))

        criar_titulo(cabecalho, "Check-in / Check-out").pack(anchor="w")

        ctk.CTkLabel(
            cabecalho, text="Registre a chegada e a saída dos hóspedes",
            font=ctk.CTkFont(family=FONTE, size=13),
            text_color=TEXTO_CINZA,
        ).pack(anchor="w")

    # ------------------------------------------------------------------
    # CARREGAMENTO DE DADOS
    # ------------------------------------------------------------------
    def atualizar_tudo(self):
        """Recarrega a fila de check-in e a lista de concluídas a partir do banco."""
        linhas = ListarReservasParaCheckin()
        self.fila_pendentes = [_linha_para_dict(linha) for linha in linhas]
        self.reserva_atual = self.fila_pendentes.pop(
            0) if self.fila_pendentes else None

        self._atualizar_card()
        self._recarregar_lista_concluidas()

    # ------------------------------------------------------------------
    # CARD SUPERIOR
    # ------------------------------------------------------------------
    def _montar_card_reserva(self):
        self.card = ctk.CTkFrame(
            self, fg_color="white", corner_radius=12,
            border_width=1, border_color=BORDA_CAMPO,
        )
        self.card.pack(fill="x", padx=MARGEM_LATERAL, pady=(0, 14))
        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_columnconfigure(1, weight=0)

        self.info_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.info_frame.grid(row=0, column=0, sticky="w", padx=20, pady=18)

        acao_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        acao_frame.grid(row=0, column=1, sticky="e", padx=20, pady=18)

        self.botao_acao = criar_botao(
            acao_frame, texto="", comando=self._on_clicar_botao, destaque=True,
        )
        self.botao_acao.configure(width=170)
        self.botao_acao.grid(row=0, column=0)

    def _atualizar_card(self):
        """Redesenha as informações do card de acordo com self.reserva_atual."""
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        if self.reserva_atual is None:
            ctk.CTkLabel(
                self.info_frame,
                text="Nenhuma reserva aguardando check-in no momento.",
                font=ctk.CTkFont(family=FONTE, size=15, weight="bold"),
                text_color=TEXTO_CINZA,
            ).grid(row=0, column=0, sticky="w")
            self.botao_acao.configure(
                text="—", state="disabled", fg_color=BORDA_CAMPO)
            return

        r = self.reserva_atual

        ctk.CTkLabel(
            self.info_frame,
            text=f"Reserva #{r['id']}",
            font=ctk.CTkFont(family=FONTE, size=18, weight="bold"),
            text_color=AZUL_ESCURO,
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        self._linha_info(self.info_frame, 1,
                          "Apartamento:", str(r["apartamento"]))
        self._linha_info(self.info_frame, 2, "Data de check-in:",
                          _formatar_data(r["data_entrada"]))

        self.botao_acao.configure(state="normal")
        if r["checkin_feito"]:
            self.botao_acao.configure(
                text="Fazer Check-out",
                fg_color=AZUL_ESCURO,
                hover_color=AZUL_HOVER,
            )
        else:
            self.botao_acao.configure(
                text="Fazer Check-in",
                fg_color=LARANJA,
                hover_color=LARANJA_HOVER,
            )

    def _linha_info(self, parent, row, rotulo, valor):
        ctk.CTkLabel(
            parent, text=rotulo, font=(FONTE, 12), text_color=TEXTO_CINZA,
        ).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=2)
        ctk.CTkLabel(
            parent, text=valor, font=(FONTE, 13, "bold"), text_color="#222",
        ).grid(row=row, column=1, sticky="w", pady=2)

    def _on_clicar_botao(self):
        if self.reserva_atual is None:
            return

        if self.reserva_atual["checkin_feito"]:
            self._fazer_checkout()
        else:
            self._fazer_checkin()

    # ------------------------------------------------------------------
    # AÇÕES
    # ------------------------------------------------------------------
    def _fazer_checkin(self):
        sucesso, mensagem = FazerCheckin(self.reserva_atual["id"])
        if sucesso:
            self.reserva_atual["checkin_feito"] = True
            self._atualizar_card()
        else:
            self._mostrar_aviso(mensagem, erro=True)

    def _fazer_checkout(self):
        sucesso, mensagem = FazerCheckout(self.reserva_atual["id"])
        if not sucesso:
            self._mostrar_aviso(mensagem, erro=True)
            return

        # a reserva atual foi concluída: tira do card e coloca a próxima da fila
        self.reserva_atual = self.fila_pendentes.pop(
            0) if self.fila_pendentes else None
        self._atualizar_card()
        self._recarregar_lista_concluidas()

    def _mostrar_aviso(self, mensagem, erro=False):
        from tkinter import messagebox
        if erro:
            messagebox.showerror("Check-in / Check-out", mensagem)
        else:
            messagebox.showinfo("Check-in / Check-out", mensagem)

    # ------------------------------------------------------------------
    # LISTA DE RESERVAS CONCLUÍDAS (mesmo padrão de cards das outras telas)
    # ------------------------------------------------------------------
    def _montar_lista_concluidas(self):
        ctk.CTkLabel(
            self, text="Reservas concluídas",
            font=ctk.CTkFont(family=FONTE, size=16, weight="bold"),
            text_color=AZUL_ESCURO,
        ).pack(anchor="w", padx=MARGEM_LATERAL + 4, pady=(0, 4))

        self.lista_scroll = ctk.CTkScrollableFrame(
            self, fg_color="white", corner_radius=12,
            border_width=1, border_color=BORDA_CAMPO,
        )
        self.lista_scroll.pack(
            fill="both", expand=True, padx=MARGEM_LATERAL, pady=(0, 20))
        self.lista_scroll.grid_columnconfigure((0, 1, 2, 3), weight=1)

    def _recarregar_lista_concluidas(self):
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()

        linhas = ListarReservasConcluidas()
        concluidas = [_linha_para_dict(linha) for linha in linhas]

        if not concluidas:
            ctk.CTkLabel(
                self.lista_scroll, text="Nenhuma reserva concluída ainda.",
                font=(FONTE, 12), text_color=TEXTO_CINZA,
            ).grid(row=0, column=0, sticky="w", padx=8, pady=8)
            return

        for i, r in enumerate(concluidas):
            self._linha_concluida(i, r)

    def _linha_concluida(self, row, r):
        ctk.CTkLabel(
            self.lista_scroll, text=f"Reserva #{r['id']}",
            font=(FONTE, 13, "bold"), text_color="#222",
        ).grid(row=row, column=0, sticky="w", padx=8, pady=6)

        ctk.CTkLabel(
            self.lista_scroll, text=f"Apto {r['apartamento']}",
            font=(FONTE, 12), text_color=TEXTO_CINZA,
        ).grid(row=row, column=1, sticky="w", padx=8, pady=6)

        ctk.CTkLabel(
            self.lista_scroll,
            text=f"{_formatar_data(r['data_entrada'])} - {_formatar_data(r['data_saida'])}",
            font=(FONTE, 12), text_color=TEXTO_CINZA,
        ).grid(row=row, column=2, sticky="w", padx=8, pady=6)

        ctk.CTkLabel(
            self.lista_scroll, text=f"R$ {r['valor']:.2f}",
            font=(FONTE, 12), text_color=TEXTO_CINZA,
        ).grid(row=row, column=3, sticky="w", padx=8, pady=6)


# ----------------------------------------------------------------------
# TESTE ISOLADO DA TELA: python -m views.view_checkin
# ----------------------------------------------------------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    janela = ctk.CTk()
    janela.title("Sistema de Reservas - Hotel")
    janela.geometry("1000x680")

    tela = TelaCheckin(janela, app=None)
    tela.pack(fill="both", expand=True)
    tela.ao_exibir()

    janela.mainloop()
