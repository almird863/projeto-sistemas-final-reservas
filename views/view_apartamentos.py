"""
view_apartamentos.py
--------------------
Tela de Apartamentos (mapa estilo escolha de assento de cinema) com filtros.
Dados vindos de controllers.control_apto.ListarAptos(),
que retorna (True, lista_de_tuplas) ou (False, mensagem), na ordem:
    id, tipo, numeracao, vago, preco_pessoa, limite_pessoa,
    pet_friendly, qt_camas, vista_mar, frigobar, mesa_sinuca

Registrar em JanelaPrincipal._registrar_telas():
    self.registrar_tela(
        "apartamentos",
        lambda: __import__("views.view_apartamentos",
                           fromlist=["TelaApartamentos"]).TelaApartamentos(self.container, self))
"""

import customtkinter as ctk
from tkinter import messagebox

from views.componentes import AZUL_ESCURO, AZUL_HOVER, LARANJA, LARANJA_HOVER, TEXTO_CINZA
from views.view_menu_principal import TelaBase
from controls.control_apto import ListarAptos

BRANCO = "#FFFFFF"
BORDA_CARD = "#DCE4F0"
FONTE = "Segoe UI"

VERDE = "#2E9E5B"
VERDE_HOVER = "#237D47"
VERMELHO = "#D9534F"
VERDE_ESMAECIDO = "#CFE8DA"
VERMELHO_ESMAECIDO = "#F0CFCD"
TEXTO_ESMAECIDO = "#8A93A6"


class TelaApartamentos(TelaBase):
    CAMPOS = ("id", "tipo", "numeracao", "vago", "preco_pessoa", "limite_pessoa",
              "pet_friendly", "qt_camas", "vista_mar", "frigobar", "mesa_sinuca", "acessivel")
    EXTRAS = (("pet_friendly", "Pet friendly"), ("vista_mar", "Vista mar"),
              ("frigobar", "Frigobar"), ("mesa_sinuca", "Mesa de sinuca"), ("acessivel", "Acessível"))

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.apartamentos = {}   # numeracao -> dict
        self.botoes = {}         # numeracao -> botão
        self.selecionado = None
        self.vars_extras = {campo: ctk.BooleanVar() for campo, _ in self.EXTRAS}

        self._criar_cabecalho().grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 8))
        self._criar_filtros().grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 10))

        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        corpo.grid_columnconfigure(0, weight=1)
        corpo.grid_rowconfigure(0, weight=1)
        self._criar_mapa(corpo).grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        self._criar_detalhes(corpo).grid(row=0, column=1, sticky="ns")

    # --- Construção da interface --------------------------------------
    def _criar_cabecalho(self):
        cab = ctk.CTkFrame(self, fg_color="transparent")
        cab.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(cab, text="Apartamentos", font=(FONTE, 28, "bold"),
                     text_color=AZUL_ESCURO).grid(row=0, column=0, sticky="w")
        self.lbl_resumo = ctk.CTkLabel(cab, text="", font=(FONTE, 14), text_color=TEXTO_CINZA)
        self.lbl_resumo.grid(row=1, column=0, sticky="w")

        legenda = ctk.CTkFrame(cab, fg_color="transparent")
        legenda.grid(row=0, column=1, rowspan=2, sticky="e")
        itens = [("Disponível", VERDE), ("Ocupado", VERMELHO), ("Selecionado", LARANJA)]
        for i, (texto, cor) in enumerate(itens):
            ctk.CTkFrame(legenda, width=16, height=16, corner_radius=4, fg_color=cor
                         ).grid(row=0, column=i * 2, padx=(10, 5))
            ctk.CTkLabel(legenda, text=texto, font=(FONTE, 12), text_color=TEXTO_CINZA
                         ).grid(row=0, column=i * 2 + 1)
        return cab

    def _criar_filtros(self):
        card = ctk.CTkFrame(self, fg_color=BRANCO, corner_radius=14,
                            border_width=1, border_color=BORDA_CARD)
        for col in range(6):
            card.grid_columnconfigure(col, weight=1, uniform="f")

        self.om_tipo = self._filtro_menu(card, 0, "Tipo", ["Todos"])
        self.om_andar = self._filtro_menu(card, 1, "Andar", ["Todos"])
        self.om_status = self._filtro_menu(card, 2, "Status", ["Todos", "Disponível", "Ocupado"])
        self.om_cap = self._filtro_menu(card, 3, "Capacidade mín.", ["Qualquer", "1", "2", "3", "4", "5", "6"])
        self.om_camas = self._filtro_menu(card, 4, "Camas mín.", ["Qualquer", "1", "2", "3", "4"])

        ctk.CTkLabel(card, text="Preço máx. (pessoa)", font=(FONTE, 11), text_color=TEXTO_CINZA
                     ).grid(row=0, column=5, sticky="w", padx=8, pady=(8, 0))
        self.ent_preco = ctk.CTkEntry(card, height=28, placeholder_text="R$")
        self.ent_preco.grid(row=1, column=5, sticky="ew", padx=8)
        self.ent_preco.bind("<KeyRelease>", lambda e: self._aplicar_filtros())

        for i, (campo, texto) in enumerate(self.EXTRAS):
            ctk.CTkCheckBox(
                card, text=texto, variable=self.vars_extras[campo],
                command=self._aplicar_filtros, font=(FONTE, 12), text_color=TEXTO_CINZA,
                checkbox_width=18, checkbox_height=18, fg_color=LARANJA, hover_color=LARANJA_HOVER,
            ).grid(row=2, column=i, sticky="w", padx=8, pady=(8, 10))

        ctk.CTkButton(
            card, text="Limpar filtros", height=28, font=(FONTE, 12, "bold"),
            fg_color=AZUL_ESCURO, hover_color=AZUL_HOVER, command=self._limpar_filtros,
        ).grid(row=2, column=5, sticky="e", padx=8, pady=(8, 10))
        return card

    def _filtro_menu(self, card, col, titulo, valores):
        ctk.CTkLabel(card, text=titulo, font=(FONTE, 11), text_color=TEXTO_CINZA
                     ).grid(row=0, column=col, sticky="w", padx=8, pady=(8, 0))
        menu = ctk.CTkOptionMenu(
            card, values=valores, height=28, font=(FONTE, 12), dynamic_resizing=False,
            fg_color=AZUL_ESCURO, button_color=AZUL_HOVER, button_hover_color=AZUL_HOVER,
            command=lambda _v: self._aplicar_filtros(),
        )
        menu.grid(row=1, column=col, sticky="ew", padx=8)
        return menu

    def _criar_mapa(self, master):
        card = ctk.CTkFrame(master, fg_color=BRANCO, corner_radius=14,
                            border_width=1, border_color=BORDA_CARD)
        card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            card, text="ENTRADA / ELEVADOR", font=(FONTE, 11, "bold"),
            text_color=BRANCO, fg_color=AZUL_ESCURO, corner_radius=8, height=26,
        ).grid(row=0, column=0, sticky="ew", padx=40, pady=(14, 8))
        self.grade = ctk.CTkFrame(card, fg_color="transparent")
        self.grade.grid(row=1, column=0, pady=(0, 12))
        return card

    def _criar_detalhes(self, master):
        card = ctk.CTkFrame(master, fg_color=BRANCO, corner_radius=14, width=240,
                            border_width=1, border_color=BORDA_CARD)
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(card, text="Detalhes", font=(FONTE, 18, "bold"), text_color=AZUL_ESCURO
                     ).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 4))
        self.lbl_num = ctk.CTkLabel(card, text="—", font=(FONTE, 32, "bold"), text_color=AZUL_ESCURO)
        self.lbl_num.grid(row=1, column=0, sticky="w", padx=18)
        self.lbl_info = ctk.CTkLabel(card, text="", font=(FONTE, 13), text_color=TEXTO_CINZA,
                                     justify="left", anchor="nw")
        self.lbl_info.grid(row=2, column=0, sticky="nw", padx=18, pady=(4, 0))
        self.btn_reservar = ctk.CTkButton(
            card, text="Reservar", font=(FONTE, 14, "bold"), height=40,
            fg_color=LARANJA, hover_color=LARANJA_HOVER, text_color=BRANCO,
            state="disabled", command=self._reservar)
        self.btn_reservar.grid(row=3, column=0, sticky="ew", padx=18, pady=(10, 16))
        return card

    # --- Dados ---------------------------------------------------------
    def _carregar(self):
        ok, dados = ListarAptos()
        if not ok:
            messagebox.showerror("Apartamentos", dados)
            return
        self.apartamentos = {}
        for linha in dados:
            ap = dict(zip(self.CAMPOS, linha))
            self.apartamentos[ap["numeracao"]] = ap
        self.selecionado = None

        tipos = sorted({a["tipo"] for a in self.apartamentos.values()})
        andares = sorted({n // 100 for n in self.apartamentos})
        self._atualizar_opcoes(self.om_tipo, ["Todos"] + tipos)
        self._atualizar_opcoes(self.om_andar, ["Todos"] + [str(a) for a in andares])

        self._montar_mapa()
        self._atualizar_detalhes()
        self._atualizar_resumo()

    @staticmethod
    def _atualizar_opcoes(menu, valores):
        atual = menu.get()
        menu.configure(values=valores)
        menu.set(atual if atual in valores else valores[0])

    # --- Mapa ----------------------------------------------------------
    def _montar_mapa(self):
        for w in self.grade.winfo_children():
            w.destroy()
        self.botoes = {}

        if not self.apartamentos:
            ctk.CTkLabel(self.grade, text="Nenhum apartamento cadastrado.",
                         font=(FONTE, 13), text_color=TEXTO_CINZA).pack(pady=30, padx=30)
            return

        andares = sorted({n // 100 for n in self.apartamentos}, reverse=True)
        for lin, andar in enumerate(andares):
            ctk.CTkLabel(self.grade, text=f"{andar}º andar", width=62, anchor="w",
                         font=(FONTE, 12, "bold"), text_color=AZUL_ESCURO
                         ).grid(row=lin, column=0, padx=(0, 8), pady=4)
            numeros = sorted(n for n in self.apartamentos if n // 100 == andar)
            for col, num in enumerate(numeros, start=1):
                btn = ctk.CTkButton(
                    self.grade, text=str(num), width=54, height=42, corner_radius=8,
                    font=(FONTE, 13, "bold"), text_color=BRANCO,
                    command=lambda n=num: self._selecionar(n))
                btn.grid(row=lin, column=col, padx=3, pady=4)
                self.botoes[num] = btn
                self._pintar(num)

    def _pintar(self, num):
        ap = self.apartamentos[num]
        vago = bool(ap["vago"])
        btn = self.botoes[num]
        if not self._passa_filtros(ap):
            cor = VERDE_ESMAECIDO if vago else VERMELHO_ESMAECIDO
            btn.configure(fg_color=cor, hover_color=cor, state="disabled",
                          text_color_disabled=TEXTO_ESMAECIDO)
        elif not vago:
            btn.configure(fg_color=VERMELHO, hover_color=VERMELHO, state="disabled",
                          text_color_disabled=BRANCO)
        elif num == self.selecionado:
            btn.configure(fg_color=LARANJA, hover_color=LARANJA_HOVER, state="normal")
        else:
            btn.configure(fg_color=VERDE, hover_color=VERDE_HOVER, state="normal")

    def _selecionar(self, num):
        anterior = self.selecionado
        self.selecionado = None if anterior == num else num  # clicar de novo desmarca
        if anterior is not None:
            self._pintar(anterior)
        self._pintar(num)
        self._atualizar_detalhes()

    # --- Filtros -------------------------------------------------------
    def _passa_filtros(self, ap):
        tipo = self.om_tipo.get()
        if tipo != "Todos" and ap["tipo"] != tipo:
            return False
        andar = self.om_andar.get()
        if andar.isdigit() and ap["numeracao"] // 100 != int(andar):
            return False
        status = self.om_status.get()
        if (status == "Disponível" and not ap["vago"]) or (status == "Ocupado" and ap["vago"]):
            return False
        cap = self.om_cap.get()
        if cap.isdigit() and (ap["limite_pessoa"] or 0) < int(cap):
            return False
        camas = self.om_camas.get()
        if camas.isdigit() and (ap["qt_camas"] or 0) < int(camas):
            return False
        texto = self.ent_preco.get().strip().replace(",", ".")
        if texto:
            try:
                if (ap["preco_pessoa"] or 0) > float(texto):
                    return False
            except ValueError:
                pass  # valor inválido: ignora o filtro
        for campo, var in self.vars_extras.items():
            if var.get() and not ap[campo]:
                return False
        return True

    def _aplicar_filtros(self):
        if self.selecionado is not None and not self._passa_filtros(self.apartamentos[self.selecionado]):
            self.selecionado = None
        for num in self.botoes:
            self._pintar(num)
        self._atualizar_detalhes()
        self._atualizar_resumo()

    def _limpar_filtros(self):
        for menu, padrao in ((self.om_tipo, "Todos"), (self.om_andar, "Todos"),
                             (self.om_status, "Todos"), (self.om_cap, "Qualquer"),
                             (self.om_camas, "Qualquer")):
            menu.set(padrao)
        self.ent_preco.delete(0, "end")
        for var in self.vars_extras.values():
            var.set(False)
        self._aplicar_filtros()

    # --- Painel / resumo -----------------------------------------------
    def _atualizar_detalhes(self):
        if self.selecionado is None:
            self.lbl_num.configure(text="—")
            self.lbl_info.configure(text="Selecione um apartamento\ndisponível no mapa.")
            self.btn_reservar.configure(state="disabled")
            return
        ap = self.apartamentos[self.selecionado]
        preco = f"R$ {(ap['preco_pessoa'] or 0):.2f}".replace(".", ",")
        extras = [texto for campo, texto in self.EXTRAS if ap[campo]]
        self.lbl_num.configure(text=str(self.selecionado))
        self.lbl_info.configure(text=(
            f"Tipo: {ap['tipo']}\n"
            f"Andar: {self.selecionado // 100}º\n"
            f"Preço/pessoa: {preco}\n"
            f"Limite: {ap['limite_pessoa']} pessoa(s)\n"
            f"Camas: {ap['qt_camas']}\n"
            f"Extras: {', '.join(extras) if extras else 'nenhum'}"
        ))
        self.btn_reservar.configure(state="normal")

    def _atualizar_resumo(self):
        total = len(self.apartamentos)
        vagos = sum(1 for a in self.apartamentos.values() if a["vago"])
        filtrados = sum(1 for a in self.apartamentos.values() if self._passa_filtros(a))
        self.lbl_resumo.configure(
            text=f"{vagos} disponíveis  •  {total - vagos} ocupados  •  {filtrados} no filtro")

    def _reservar(self):
        self.app.apartamento_selecionado = self.selecionado  # para a tela de reservas usar
        self.app.mostrar_tela("reservas")

    def ao_exibir(self):
        self._carregar()