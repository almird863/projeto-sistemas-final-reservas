"""
view_checkin.py
----------------
Tela de Check-in / Check-out do sistema de hotelaria (Projeto Integrador SENAC).

ATENÇÃO (leia antes de colar no projeto):
Eu não tive acesso ao conteúdo atual de 'views/componentes.py', 'models/model_reserva.py'
nem 'controls/control_reserva.py' (o acesso ao repositório não foi liberado nesta sessão).
Por isso, esta tela foi construída com:
  - CustomTkinter (customtkinter), como o resto do projeto usa;
  - Uma paleta de cores "placeholder" (tema claro, destaque laranja), coerente com a
    identidade visual mencionada (ondas laranja, cards arredondados);
  - Nomes de campos "prováveis" para a reserva (id, apartamento, cliente, data_checkin,
    data_checkout, status).

Antes de colar este arquivo na branch 'view', você PRECISA:
  1. Trocar o bloco `CORES` (abaixo) pelos valores reais de `views/componentes.py`
     (ou, melhor ainda, importar as constantes de lá em vez de duplicá-las).
  2. Conferir os nomes dos campos do objeto/linha de reserva em `models/model_reserva.py`
     e ajustar as funções `_extrair_dados_reserva` conforme necessário.
  3. Trocar as funções de acesso a dados (marcadas com `# TODO INTEGRAÇÃO`) pelas
     funções reais de `controls/control_reserva.py`.

O arquivo roda sozinho (bloco `if __name__ == "__main__"`) com dados fictícios,
para você testar o visual antes de plugar no restante do sistema.
"""

import customtkinter as ctk

# ---------------------------------------------------------------------------
# 1) CORES / FONTES — SUBSTITUA pelos valores reais de views/componentes.py
# ---------------------------------------------------------------------------
# Se componentes.py já exporta constantes (ex.: COR_PRIMARIA, COR_FUNDO, FONTE_TITULO),
# o ideal é importar de lá:
#
#   from views.componentes import COR_PRIMARIA, COR_FUNDO_CARD, COR_TEXTO, FONTE_TITULO
#
# Enquanto isso não é confirmado, uso este bloco local para a tela funcionar sozinha:

CORES = {
    "fundo_janela": "#F4F1EC",      # bege claro, para combinar com as ondas laranja
    "fundo_card": "#FFFFFF",
    "borda_card": "#E7DFD3",
    "laranja": "#E08A3C",           # cor de destaque (ajustar para o laranja real do projeto)
    "laranja_hover": "#C8752E",
    "verde_checkout": "#3C8A5B",    # cor do botão quando a ação é "Check-out"
    "verde_checkout_hover": "#2E6E47",
    "texto_titulo": "#2E2A25",
    "texto_label": "#6B6258",
    "texto_valor": "#2E2A25",
}

FONTE_TITULO = ("Segoe UI", 20, "bold")
FONTE_SUBTITULO = ("Segoe UI", 15, "bold")
FONTE_LABEL = ("Segoe UI", 12)
FONTE_VALOR = ("Segoe UI", 13, "bold")

MARGEM_TOPO = 24       # margem superior da janela, pedida na tarefa
MARGEM_LATERAL = 24


class TelaCheckin(ctk.CTkFrame):
    """
    Tela de Check-in / Check-out.

    Estrutura:
      - Card superior (respeitando a margem de topo) com:
          * número da reserva (id)
          * apartamento
          * data de check-in
          * botão que alterna entre "Fazer Check-in" e "Fazer Check-out"
      - Lista abaixo com todas as reservas já concluídas (check-out feito),
        no mesmo estilo da tela de usuários.
    """

    def __init__(self, master, reserva_atual: dict, reservas_concluidas: list[dict], **kwargs):
        """
        master: janela/frame pai.
        reserva_atual: dict com a reserva que está em destaque no card superior.
            Formato esperado (ajustar nomes conforme model_reserva.py):
                {
                    "id": 101,
                    "apartamento": "204",
                    "data_checkin": "12/11/2026",
                    "status": "pendente",   # "pendente" ou "hospedado"
                }
        reservas_concluidas: lista de dicts no mesmo formato, já com check-out feito.
        """
        super().__init__(master, fg_color=CORES["fundo_janela"], **kwargs)

        self.reserva_atual = reserva_atual
        self.reservas_concluidas = reservas_concluidas

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._montar_card_reserva()
        self._montar_lista_concluidas()

    # ------------------------------------------------------------------
    # CARD SUPERIOR
    # ------------------------------------------------------------------
    def _montar_card_reserva(self):
        self.card = ctk.CTkFrame(
            self,
            fg_color=CORES["fundo_card"],
            border_color=CORES["borda_card"],
            border_width=1,
            corner_radius=16,
        )
        # pady=(MARGEM_TOPO, 12) -> respeita a margem de topo pedida
        self.card.grid(
            row=0, column=0, sticky="ew",
            padx=MARGEM_LATERAL, pady=(MARGEM_TOPO, 12),
        )
        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_columnconfigure(1, weight=0)

        # --- coluna da esquerda: informações da reserva ---
        info = ctk.CTkFrame(self.card, fg_color="transparent")
        info.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        titulo = ctk.CTkLabel(
            info,
            text=f"Reserva #{self.reserva_atual['id']}",
            font=FONTE_TITULO,
            text_color=CORES["texto_titulo"],
        )
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        self._linha_info(info, 1, "Apartamento:", str(self.reserva_atual["apartamento"]))
        self._linha_info(info, 2, "Data de check-in:", str(self.reserva_atual["data_checkin"]))

        # --- coluna da direita: botão de ação ---
        acao = ctk.CTkFrame(self.card, fg_color="transparent")
        acao.grid(row=0, column=1, sticky="e", padx=20, pady=20)

        self.botao_acao = ctk.CTkButton(
            acao,
            text="",  # definido em _atualizar_botao()
            width=160,
            height=42,
            corner_radius=10,
            font=FONTE_SUBTITULO,
            command=self._on_clicar_botao,
        )
        self.botao_acao.grid(row=0, column=0)

        self._atualizar_botao()

    def _linha_info(self, parent, row, rotulo, valor):
        ctk.CTkLabel(
            parent, text=rotulo, font=FONTE_LABEL, text_color=CORES["texto_label"],
        ).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=2)
        ctk.CTkLabel(
            parent, text=valor, font=FONTE_VALOR, text_color=CORES["texto_valor"],
        ).grid(row=row, column=1, sticky="w", pady=2)

    def _atualizar_botao(self):
        """Ajusta texto e cor do botão conforme o status atual da reserva."""
        status = self.reserva_atual["status"]

        if status == "pendente":
            # ainda não fez check-in -> botão oferece "Check-in"
            self.botao_acao.configure(
                text="Fazer Check-in",
                fg_color=CORES["laranja"],
                hover_color=CORES["laranja_hover"],
            )
        else:
            # já hospedado -> botão agora oferece "Check-out"
            self.botao_acao.configure(
                text="Fazer Check-out",
                fg_color=CORES["verde_checkout"],
                hover_color=CORES["verde_checkout_hover"],
            )

    def _on_clicar_botao(self):
        status = self.reserva_atual["status"]

        if status == "pendente":
            self._fazer_checkin()
        else:
            self._fazer_checkout()

    # ------------------------------------------------------------------
    # AÇÕES — TODO INTEGRAÇÃO: trocar pelas chamadas reais do controller
    # ------------------------------------------------------------------
    def _fazer_checkin(self):
        # TODO INTEGRAÇÃO: chamar o controller real, por exemplo:
        #   control_reserva.fazer_checkin(self.reserva_atual["id"])
        self.reserva_atual["status"] = "hospedado"
        self._atualizar_botao()

    def _fazer_checkout(self):
        # TODO INTEGRAÇÃO: chamar o controller real, por exemplo:
        #   control_reserva.fazer_checkout(self.reserva_atual["id"])
        self.reservas_concluidas.insert(0, dict(self.reserva_atual))
        self._adicionar_linha_concluida(self.reserva_atual)

        # TODO INTEGRAÇÃO: aqui você normalmente buscaria a PRÓXIMA reserva
        # pendente no banco e substituiria self.reserva_atual por ela.
        # Por enquanto, deixo o card com o status "encerrado" para feedback visual:
        self.reserva_atual["status"] = "encerrado"
        self.botao_acao.configure(text="Concluída", state="disabled", fg_color=CORES["borda_card"])

    # ------------------------------------------------------------------
    # LISTA DE RESERVAS CONCLUÍDAS (mesmo padrão da tela de usuários)
    # ------------------------------------------------------------------
    def _montar_lista_concluidas(self):
        subtitulo = ctk.CTkLabel(
            self, text="Reservas concluídas", font=FONTE_SUBTITULO,
            text_color=CORES["texto_titulo"],
        )
        subtitulo.grid(row=1, column=0, sticky="nw", padx=MARGEM_LATERAL + 4, pady=(0, 4))

        self.lista_scroll = ctk.CTkScrollableFrame(
            self, fg_color=CORES["fundo_card"],
            corner_radius=16, border_width=1, border_color=CORES["borda_card"],
        )
        self.lista_scroll.grid(
            row=2, column=0, sticky="nsew",
            padx=MARGEM_LATERAL, pady=(0, MARGEM_LATERAL),
        )
        self.grid_rowconfigure(2, weight=1)
        self.lista_scroll.grid_columnconfigure(0, weight=1)

        for reserva in self.reservas_concluidas:
            self._adicionar_linha_concluida(reserva)

    def _adicionar_linha_concluida(self, reserva: dict):
        linha = ctk.CTkFrame(self.lista_scroll, fg_color="transparent")
        linha.grid(sticky="ew", pady=6, padx=8)
        linha.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            linha, text=f"Reserva #{reserva['id']}", font=FONTE_VALOR,
            text_color=CORES["texto_valor"],
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            linha, text=f"Apto {reserva['apartamento']}", font=FONTE_LABEL,
            text_color=CORES["texto_label"],
        ).grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            linha, text=f"Check-in: {reserva['data_checkin']}", font=FONTE_LABEL,
            text_color=CORES["texto_label"],
        ).grid(row=0, column=2, sticky="w")


# ---------------------------------------------------------------------------
# Execução isolada para você testar o visual sem o restante do projeto
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("light")

    app = ctk.CTk()
    app.title("Check-in / Check-out — teste isolado")
    app.geometry("760x560")

    reserva_exemplo = {
        "id": 101,
        "apartamento": "204",
        "data_checkin": "12/11/2026",
        "status": "pendente",
    }

    reservas_concluidas_exemplo = [
        {"id": 97, "apartamento": "101", "data_checkin": "05/11/2026"},
        {"id": 98, "apartamento": "305", "data_checkin": "07/11/2026"},
    ]

    tela = TelaCheckin(app, reserva_exemplo, reservas_concluidas_exemplo)
    tela.pack(fill="both", expand=True)

    app.mainloop()