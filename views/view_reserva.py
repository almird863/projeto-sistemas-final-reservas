"""
View de Reservas - Sistema de Reservas - Hotel
Compatível tanto como tela embutida (TelaBase no menu principal)
quanto executável de forma independente para testes.

Seguindo o design da imagem:
- Topo: Ícone e Título "Reservas - Confira a disponibilidade e faça sua reserva"
- Painel Esquerdo: "Filtros de Busca" (Data Entrada, Data Saída com Calendário Popup, Tipo de Apto, Botão Buscar)
- Painel Direito: "Apartamentos Disponíveis" (Cards com foto, tipo, descrição, diária e botão Reservar)
"""

import calendar
import os
from datetime import date, datetime, timedelta
from tkinter import messagebox, simpledialog
import customtkinter as ctk
from controls.control_reserva import CadastrarReserva
from controls.control_cliente import buscar_cliente
from controls.control_apto import BuscarApto
from views.view_usuarios import carregar_conta

from views.componentes import (
    AZUL_ESCURO, AZUL_HOVER, LARANJA, LARANJA_HOVER, FUNDO_DIREITO,
    BORDA_CAMPO, TEXTO_CINZA, carregar_imagem, criar_barra_titulo
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

# Import do Model/Controller de Apartamentos (se disponível)
try:
    from models.model_apto import listar_aptos
except Exception:
    def listar_aptos(somente_vagos=False):
        return []

FONTE = "Segoe UI"
BORDA_CARD = "#DCE4F0"
AZUL_CABECALHO = "#14376E"


# ----------------------------------------------------------------------
# POPUP DE CALENDÁRIO VISUAL NATIVO (CustomTkinter)
# ----------------------------------------------------------------------
class PopupCalendario(ctk.CTkToplevel):
    """
    Janelinha modal com calendário interativo para seleção de data.
    Não necessita de nenhuma biblioteca externa!
    """

    MESES = [
        "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    DIAS_SEMANA = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    def __init__(self, master, data_inicial=None, ao_selecionar=None):
        super().__init__(master)
        self.ao_selecionar = ao_selecionar

        if data_inicial:
            try:
                dt = datetime.strptime(data_inicial, "%d/%m/%Y").date()
                self.ano_atual = dt.year
                self.mes_atual = dt.month
                self.dia_selecionado = dt.day
            except Exception:
                hoje = date.today()
                self.ano_atual = hoje.year
                self.mes_atual = hoje.month
                self.dia_selecionado = hoje.day
        else:
            hoje = date.today()
            self.ano_atual = hoje.year
            self.mes_atual = hoje.month
            self.dia_selecionado = hoje.day

        self.title("Selecionar Data")
        self.geometry("310x330")
        self.resizable(False, False)
        self.configure(fg_color="white")

        if master is not None and master.winfo_viewable():
            self.transient(master)

        self._criar_ui()

        # Foco e posicionamento
        self.after(100, self._centralizar_e_focar)

    def _centralizar_e_focar(self):
        self.lift()
        self.focus_force()
        self.grab_set()

    def _criar_ui(self):
        # 1. Barra de Navegação de Mês/Ano
        nav = ctk.CTkFrame(self, fg_color=AZUL_CABECALHO, corner_radius=0, height=44)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        btn_ant = ctk.CTkButton(
            nav, text="◀", width=32, height=32,
            fg_color="transparent", hover_color=AZUL_HOVER,
            font=(FONTE, 12, "bold"), command=self._mes_anterior
        )
        btn_ant.pack(side="left", padx=8)

        self.lbl_mes_ano = ctk.CTkLabel(
            nav, text="", font=ctk.CTkFont(family=FONTE, size=14, weight="bold"),
            text_color="white"
        )
        self.lbl_mes_ano.pack(side="left", expand=True)

        btn_prox = ctk.CTkButton(
            nav, text="▶", width=32, height=32,
            fg_color="transparent", hover_color=AZUL_HOVER,
            font=(FONTE, 12, "bold"), command=self._mes_proximo
        )
        btn_prox.pack(side="right", padx=8)

        # 2. Dias da Semana (Seg, Ter, Qua...)
        semana = ctk.CTkFrame(self, fg_color="#F1F5F9", height=28, corner_radius=0)
        semana.pack(fill="x")
        for i, d in enumerate(self.DIAS_SEMANA):
            ctk.CTkLabel(
                semana, text=d, font=(FONTE, 11, "bold"),
                text_color=AZUL_ESCURO if i < 5 else LARANJA, width=42
            ).pack(side="left")

        # 3. Grade dos Dias do Mês
        self.frame_dias = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.frame_dias.pack(fill="both", expand=True, padx=8, pady=8)

        self._desenhar_dias()

    def _desenhar_dias(self):
        for w in self.frame_dias.winfo_children():
            w.destroy()

        self.lbl_mes_ano.configure(
            text=f"{self.MESES[self.mes_atual]} {self.ano_atual}"
        )

        # Matriz de semanas do calendário (0 = dia fora do mês)
        cal = calendar.monthcalendar(self.ano_atual, self.mes_atual)
        hoje = date.today()

        for r, sem in enumerate(cal):
            for c, dia in enumerate(sem):
                if dia == 0:
                    lbl = ctk.CTkLabel(self.frame_dias, text="", width=36, height=30)
                    lbl.grid(row=r, column=c, padx=2, pady=2)
                else:
                    e_selecionado = (dia == self.dia_selecionado)
                    e_hoje = (
                        dia == hoje.day and
                        self.mes_atual == hoje.month and
                        self.ano_atual == hoje.year
                    )

                    fg = LARANJA if e_selecionado else ("#E2E8F0" if e_hoje else "transparent")
                    tc = "white" if e_selecionado else AZUL_ESCURO

                    btn = ctk.CTkButton(
                        self.frame_dias,
                        text=str(dia),
                        width=36, height=30,
                        corner_radius=6,
                        fg_color=fg,
                        hover_color=LARANJA_HOVER if e_selecionado else "#E2E8F0",
                        text_color=tc,
                        font=ctk.CTkFont(family=FONTE, size=12, weight="bold" if (e_selecionado or e_hoje) else "normal"),
                        command=lambda d=dia: self._escolher_dia(d)
                    )
                    btn.grid(row=r, column=c, padx=2, pady=2)

    def _mes_anterior(self):
        if self.mes_atual == 1:
            self.mes_atual = 12
            self.ano_atual -= 1
        else:
            self.mes_atual -= 1
        self._desenhar_dias()

    def _mes_proximo(self):
        if self.mes_atual == 12:
            self.mes_atual = 1
            self.ano_atual += 1
        else:
            self.mes_atual += 1
        self._desenhar_dias()

    def _escolher_dia(self, dia):
        data_escolhida = f"{dia:02d}/{self.mes_atual:02d}/{self.ano_atual}"
        if self.ao_selecionar:
            self.ao_selecionar(data_escolhida)
        self.destroy()


# ----------------------------------------------------------------------
# TELA DE RESERVAS
# ----------------------------------------------------------------------
class TelaReservas(TelaBase):
    """
    Tela de Consulta e Reserva de Apartamentos.
    Pode ser instanciada dentro do container do menu principal.
    """

    def __init__(self, master, app=None, **kwargs):
        super().__init__(master, app, **kwargs)
        self.numero_filtro = getattr(app, "apartamento_selecionado", None)
        if app is not None:
            app.apartamento_selecionado = None  
        # Referências de imagens para evitar garbage collection do Tkinter
        self._imagens_cache = []
        # Referências dos labels das ondas (para poder elevá-las ao topo do z-order)
        self._lbl_onda_sup = None
        self._lbl_onda_inf = None

        # Corpo e cabeçalho são criados ANTES das ondas,
        # para que as ondas fiquem no topo da pilha de renderização
        self._criar_cabecalho()
        self._criar_corpo()

        # Ondas decorativas DEPOIS do corpo — assim ficam na frente de tudo
        self._adicionar_onda_superior()
        # self._adicionar_onda_inferior()

        # Garantia extra: eleva as ondas após o Tkinter terminar o layout
        self.after(50, self._elevar_ondas)

    def _adicionar_onda_superior(self):
        """Onda laranja/azul decorativa no canto superior direito."""
        img_onda = carregar_imagem("onda_reserva_superior.png", (380, 75))
        if img_onda:
            self._imagens_cache.append(img_onda)
            self._lbl_onda_sup = ctk.CTkLabel(self, text="", image=img_onda, fg_color="transparent")
            self._lbl_onda_sup.place(relx=1.0, y=0, anchor="ne")

    # def _adicionar_onda_inferior(self):
    #     """Onda laranja/azul decorativa no canto inferior direito."""
    #     img_onda = carregar_imagem("onda_reserva_inferior.png", (380, 65))
    #     if img_onda:
    #         self._imagens_cache.append(img_onda)
    #         self._lbl_onda_inf = ctk.CTkLabel(self, text="", image=img_onda, fg_color="transparent")
    #         self._lbl_onda_inf.place(relx=1.0, rely=1.0, anchor="se")

    def _elevar_ondas(self):
        """Eleva os labels das ondas ao topo do z-order após o layout ser concluído."""
        if self._lbl_onda_sup:
            self._lbl_onda_sup.lift()
        if self._lbl_onda_inf:
            self._lbl_onda_inf.lift()

    def ao_exibir(self):
        """Lê o apto escolhido no mapa; chamadas sem valor novo não apagam o filtro."""
        numero = getattr(self.app, "apartamento_selecionado", None)
        if numero is not None:
            self.numero_filtro = numero
            self.app.apartamento_selecionado = None
        self.renderizar_apartamentos(self.combo_tipo.get())

    # ------------------------------------------------------------------
    # 1. CABEÇALHO DA TELA
    # ------------------------------------------------------------------
    def _criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(self, fg_color="transparent")
        cabecalho.pack(fill="x", padx=25, pady=(15, 10))

        # Ícone do calendário / reservas
        # >>> IMAGEM: coloque 'icone_reservas.png' (42x42) em views/assets/ <<<
        img_cal = carregar_imagem("icone_reservas.png", (42, 42))
        if img_cal:
            self._imagens_cache.append(img_cal)
            lbl_ico = ctk.CTkLabel(cabecalho, text="", image=img_cal)
        else:
            lbl_ico = ctk.CTkLabel(
                cabecalho, text="📅", font=(FONTE, 32), text_color=AZUL_ESCURO
            )
        lbl_ico.pack(side="left", padx=(0, 12))

        textos = ctk.CTkFrame(cabecalho, fg_color="transparent")
        textos.pack(side="left", fill="both")

        ctk.CTkLabel(
            textos, text="Reservas",
            font=ctk.CTkFont(family=FONTE, size=24, weight="bold"),
            text_color=AZUL_ESCURO,
        ).pack(anchor="w")

        ctk.CTkLabel(
            textos, text="Confira a disponibilidade e faça sua reserva",
            font=ctk.CTkFont(family=FONTE, size=13),
            text_color=TEXTO_CINZA,
        ).pack(anchor="w")

    # ------------------------------------------------------------------
    # 2. CORPO (Filtros à Esquerda + Apartamentos à Direita)
    # ------------------------------------------------------------------
    def _criar_corpo(self):
        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=25, pady=(5, 20))

        self._criar_painel_filtros(corpo)
        self._criar_painel_apartamentos(corpo)

    # --- PAINEL ESQUERDO: FILTROS DE BUSCA -----------------------------
    def _criar_painel_filtros(self, master):
        card_filtros = ctk.CTkFrame(
            master, width=280, fg_color="white", corner_radius=12,
            border_width=1, border_color=BORDA_CARD
        )
        card_filtros.pack(side="left", fill="y", padx=(0, 16))
        card_filtros.pack_propagate(False)

        # Barra do título do filtro (azul como topo do card)
        barra_tit = ctk.CTkFrame(
            card_filtros, height=44, fg_color=AZUL_CABECALHO, corner_radius=12
        )
        barra_tit.pack(fill="x")
        barra_tit.pack_propagate(False)

        ctk.CTkLabel(
            barra_tit, text="Filtros de Busca",
            font=ctk.CTkFont(family=FONTE, size=14, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=14)

        conteudo = ctk.CTkFrame(card_filtros, fg_color="transparent")
        conteudo.pack(fill="both", expand=True, padx=14, pady=10)

        # 1. Data de Entrada
        ctk.CTkLabel(
            conteudo, text="Data de Entrada:",
            font=ctk.CTkFont(family=FONTE, size=12, weight="bold"),
            text_color=AZUL_ESCURO
        ).pack(anchor="w", pady=(4, 2))

        hoje_str = date.today().strftime("%d/%m/%Y")
        saida_str = (date.today() + timedelta(days=3)).strftime("%d/%m/%Y")

        self.entry_entrada = self._criar_campo_data(conteudo, hoje_str)

        # 2. Data de Saída
        ctk.CTkLabel(
            conteudo, text="Data de Saída:",
            font=ctk.CTkFont(family=FONTE, size=12, weight="bold"),
            text_color=AZUL_ESCURO
        ).pack(anchor="w", pady=(10, 2))

        self.entry_saida = self._criar_campo_data(conteudo, saida_str)

        # 3. Tipo de Apartamento
        ctk.CTkLabel(
            conteudo, text="Tipo de Apartamento:",
            font=ctk.CTkFont(family=FONTE, size=12, weight="bold"),
            text_color=AZUL_ESCURO
        ).pack(anchor="w", pady=(10, 2))

        self.combo_tipo = ctk.CTkComboBox(
            conteudo,
            values=["Todos", "Standard", "Duplo", "Luxo", "Super Luxo", "Presidencial"],
            font=ctk.CTkFont(family=FONTE, size=13),
            dropdown_font=ctk.CTkFont(family=FONTE, size=13),
            fg_color="white",
            border_color=BORDA_CAMPO,
            border_width=1,
            corner_radius=8,
            button_color="#E2E7F0",
            button_hover_color="#CBD5E1",
            text_color="#1E293B",
            height=38
        )
        self.combo_tipo.pack(fill="x", pady=(0, 16))
        self.combo_tipo.set("Todos")
        
        ctk.CTkLabel(
            conteudo, text="Quantidade de pessoas:",
            font=ctk.CTkFont(family=FONTE, size=12, weight="bold"),
            text_color=AZUL_ESCURO
        ).pack(anchor="w", pady=(10, 2))
        
        self.combo_qt_pessoas = ctk.CTkComboBox(
            conteudo,
            values=["1", "2", "3", "4", "5", "6"],
            font=ctk.CTkFont(family=FONTE, size=13),
            dropdown_font=ctk.CTkFont(family=FONTE, size=13),
            fg_color="white",
            border_color=BORDA_CAMPO,
            border_width=1,
            corner_radius=8,
            button_color="#E2E7F0",
            button_hover_color="#CBD5E1",
            text_color="#1E293B",
            height=38
        )
        self.combo_qt_pessoas.pack(fill="x", pady=(0, 5))
        self.combo_qt_pessoas.set("1")
        
        # 4. Botão Buscar Disponibilidade (Laranja com Lupa)
        # >>> IMAGEM: coloque 'icone_lupa.png' (18x18) em views/assets/ <<<
        img_lupa = carregar_imagem("icone_lupa.png", (18, 18))
        self.btn_buscar = ctk.CTkButton(
            conteudo,
            text=" Buscar Disponibilidade",
            image=img_lupa,
            compound="left",
            font=ctk.CTkFont(family=FONTE, size=13, weight="bold"),
            fg_color=LARANJA,
            hover_color=LARANJA_HOVER,
            text_color="white",
            corner_radius=8,
            height=42,
            command=self.ao_clicar_buscar
        )
        if not img_lupa:
            self.btn_buscar.configure(text="🔍  Buscar Disponibilidade")
        self.btn_buscar.pack(fill="x", pady=(10, 0))

    def _criar_campo_data(self, master, valor_inicial):
        moldura = ctk.CTkFrame(
            master, fg_color="white", corner_radius=8,
            border_width=1, border_color=BORDA_CAMPO, height=38
        )
        moldura.pack(fill="x", pady=(0, 4))
        moldura.pack_propagate(False)

        entry = ctk.CTkEntry(
            moldura,
            font=ctk.CTkFont(family=FONTE, size=13, weight="bold"),
            fg_color="white",
            border_width=0,
            text_color=AZUL_ESCURO,
        )
        entry.insert(0, valor_inicial)
        entry.pack(side="left", fill="both", expand=True, padx=(10, 4), pady=3)

        # Botão com o ícone do calendário para abrir o popup seletor de data
        # >>> IMAGEM: 'icone_calendario_campo.png' (18x18) em views/assets/ <<<
        img_cal = carregar_imagem("icone_calendario_campo.png", (18, 18))
        if img_cal:
            self._imagens_cache.append(img_cal)
            btn_cal = ctk.CTkButton(
                moldura, text="", image=img_cal, width=28, height=28,
                fg_color="transparent", hover_color="#E2E8F0", cursor="hand2",
                command=lambda e=entry: self._abrir_seletor_data(e)
            )
        else:
            btn_cal = ctk.CTkButton(
                moldura, text="📅", width=28, height=28,
                fg_color="transparent", hover_color="#E2E8F0", cursor="hand2",
                font=(FONTE, 14), text_color=AZUL_ESCURO,
                command=lambda e=entry: self._abrir_seletor_data(e)
            )
        btn_cal.pack(side="right", padx=(0, 6), pady=3)
        return entry

    def _abrir_seletor_data(self, entry_alvo):
        """Abre o popup do calendário e atualiza o campo ao selecionar o dia."""
        def atualizar(data_formatada):
            entry_alvo.delete(0, "end")
            entry_alvo.insert(0, data_formatada)

        data_atual = entry_alvo.get().strip()
        PopupCalendario(self, data_inicial=data_atual, ao_selecionar=atualizar)

    # --- PAINEL DIREITO: LISTA DE APARTAMENTOS -------------------------
    def _criar_painel_apartamentos(self, master):
        self.card_aptos = ctk.CTkFrame(
            master, fg_color="white", corner_radius=12,
            border_width=1, border_color=BORDA_CARD
        )
        self.card_aptos.pack(side="left", fill="both", expand=True)

        # Barra do topo azul como cabeçalho do card
        barra_tit = ctk.CTkFrame(
            self.card_aptos, height=44, fg_color=AZUL_CABECALHO, corner_radius=12
        )
        barra_tit.pack(fill="x")
        barra_tit.pack_propagate(False)

        ctk.CTkLabel(
            barra_tit, text="Apartamentos Disponíveis",
            font=ctk.CTkFont(family=FONTE, size=14, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=14)
        
        self.btn_ver_todos = ctk.CTkButton(
            barra_tit, text="Ver todos", width=90, height=28,
            font=ctk.CTkFont(family=FONTE, size=12, weight="bold"),
            fg_color=LARANJA, hover_color=LARANJA_HOVER, text_color="white",
            command=self.ao_clicar_ver_todos
        )

        # Container scrollável para acomodar os cards de apartamentos lado a lado
        self.container_cards = ctk.CTkScrollableFrame(
            self.card_aptos, fg_color="transparent", orientation="horizontal"
        )
        self.container_cards.pack(fill="both", expand=True, padx=10, pady=10)

        # Carrega os apartamentos iniciais
        self.renderizar_apartamentos()

    def renderizar_apartamentos(self, tipo_filtro="Todos"):
        """Limpa e redesenha os cards dos apartamentos disponíveis."""
        for widget in self.container_cards.winfo_children():
            widget.destroy()

        dados_banco = listar_aptos(somente_vagos=True)

        # Se o banco ainda não tiver quartos, usamos modelos visuais padrão
        if not dados_banco:
            aptos_exemplo = [
                {
                    "tipo": "Standard",
                    "descricao": "Conforto e praticidade",
                    "preco": 180.00,
                    "foto": "apto_standard.png",
                    "numero": 101,
                },
                {
                    "tipo": "Luxo",
                    "descricao": "Mais espaço e conforto",
                    "preco": 280.00,
                    "foto": "apto_luxo.png",
                    "numero": 201,
                },
                {
                    "tipo": "Suíte",
                    "descricao": "Experiência premium",
                    "preco": 420.00,
                    "foto": "apto_suite.png",
                    "numero": 301,
                },
            ]
        else:
            # Converte as linhas do banco SQLite:
            # (id, tipo, numeracao, vago, preco_pessoa, limite_pessoa, ...)
            descricoes = {
                "Standard": "Conforto e praticidade",
                "Luxo": "Mais espaço e conforto",
                "Suíte": "Experiência premium",
                "Suite": "Experiência premium",
            }
            fotos = {
                "Standard": "apto_standard.png",
                "Luxo": "apto_luxo.png",
                "Suíte": "apto_suite.png",
                "Suite": "apto_suite.png",
            }
            aptos_exemplo = []
            for linha in dados_banco:
                tipo = linha[1]
                numeracao = linha[2]
                preco = linha[4] or 0.0
                aptos_exemplo.append({
                    "tipo": tipo,
                    "descricao": descricoes.get(tipo, "Acomodação completa"),
                    "preco": preco,
                    "foto": fotos.get(tipo, "foto_quarto.png"),
                    "numero": numeracao,
                })

        # Apto específico (vindo do mapa) tem prioridade sobre o filtro de tipo
        if self.numero_filtro is not None:
            aptos_exemplo = [a for a in aptos_exemplo if a["numero"] == self.numero_filtro]
            self.btn_ver_todos.pack(side="right", padx=10)
        else:
            self.btn_ver_todos.pack_forget()
            if tipo_filtro and tipo_filtro != "Todos":
                aptos_exemplo = [
                    a for a in aptos_exemplo
                    if a["tipo"].lower() == tipo_filtro.lower()
                ]

        if not aptos_exemplo:
            ctk.CTkLabel(
                self.container_cards,
                text="Nenhum apartamento disponível para os filtros selecionados.",
                font=(FONTE, 14),
                text_color=TEXTO_CINZA,
            ).pack(padx=20, pady=40)
            return

        for apto in aptos_exemplo:
            self._criar_card_apto(self.container_cards, apto)

    def _criar_card_apto(self, master, dados):
        """Cria o card individual de um apartamento."""
        card = ctk.CTkFrame(
            master, width=230, fg_color="white", corner_radius=12,
            border_width=1, border_color=BORDA_CARD
        )
        card.pack(side="left", padx=8, pady=4, fill="y")
        card.pack_propagate(False)

        # 1. Título do Quarto + numeração
        topo = ctk.CTkFrame(card, fg_color="transparent")
        topo.pack(fill="x", padx=12, pady=(10, 6))

        ctk.CTkLabel(
            topo, text=dados["tipo"],
            font=ctk.CTkFont(family=FONTE, size=16, weight="bold"),
            text_color=AZUL_ESCURO
        ).pack(side="left")

        ctk.CTkLabel(
            topo, text=f"Nº {dados.get('numero', 'S/N')}",
            font=ctk.CTkFont(family=FONTE, size=12, weight="bold"),
            text_color="white", fg_color=LARANJA,
            corner_radius=6, width=52, height=22
        ).pack(side="right")

        # 2. Foto do Quarto
        # >>> IMAGEM: coloque as fotos dos quartos em views/assets/ <<<
        # ex.: apto_standard.png, apto_luxo.png, apto_suite.png (206x115)
        img_quarto = carregar_imagem(dados.get("foto", ""), (206, 115))
        if not img_quarto:
            # Fallback para a foto geral do quarto ou bloco ilustrado
            img_quarto = carregar_imagem("foto_quarto.png", (206, 115))

        if img_quarto:
            self._imagens_cache.append(img_quarto)
            lbl_foto = ctk.CTkLabel(card, text="", image=img_quarto, corner_radius=8)
        else:
            lbl_foto = ctk.CTkFrame(card, height=115, fg_color="#E2E8F0", corner_radius=8)
            ctk.CTkLabel(
                lbl_foto, text="[ FOTO DO QUARTO ]",
                font=(FONTE, 11), text_color="#64748B"
            ).place(relx=0.5, rely=0.5, anchor="center")

        lbl_foto.pack(fill="x", padx=12, pady=(0, 8))

        # 3. Descrição
        ctk.CTkLabel(
            card, text=dados["descricao"],
            font=ctk.CTkFont(family=FONTE, size=12),
            text_color=TEXTO_CINZA
        ).pack(anchor="w", padx=12, pady=(2, 6))

        # 4. Preço (R$ 180,00 / noite)
        preco_frame = ctk.CTkFrame(card, fg_color="transparent")
        preco_frame.pack(anchor="w", padx=12, pady=(4, 12))

        ctk.CTkLabel(
            preco_frame,
            text=f"R$ {dados['preco']:.2f}".replace(".", ","),
            font=ctk.CTkFont(family=FONTE, size=16, weight="bold"),
            text_color=AZUL_ESCURO
        ).pack(side="left")

        ctk.CTkLabel(
            preco_frame,
            text=" / noite",
            font=ctk.CTkFont(family=FONTE, size=12),
            text_color=TEXTO_CINZA
        ).pack(side="left")

        # 5. Botão Reservar (Azul com ícone de cama)
        # >>> IMAGEM: 'icone_cama_btn.png' (18x18) em views/assets/ <<<
        img_cama = carregar_imagem("icone_cama_btn.png", (18, 18))
        btn_res = ctk.CTkButton(
            card,
            text=" Reservar",
            image=img_cama,
            compound="left",
            font=ctk.CTkFont(family=FONTE, size=13, weight="bold"),
            fg_color=AZUL_ESCURO,
            hover_color=AZUL_HOVER,
            text_color="white",
            corner_radius=8,
            height=38,
            command=lambda d=dados: self.ao_clicar_reservar(d)
        )
        if not img_cama:
            btn_res.configure(text="🛏  Reservar")
        btn_res.pack(fill="x", padx=12, pady=(0, 12), side="bottom")

    # ------------------------------------------------------------------
    # AÇÕES
    # ------------------------------------------------------------------
    def ao_clicar_buscar(self):
        """Busca por tipo; sai do modo 'apto específico'."""
        self.numero_filtro = None
        self.renderizar_apartamentos(tipo_filtro=self.combo_tipo.get())

    def ao_clicar_ver_todos(self):
        self.numero_filtro = None
        self.renderizar_apartamentos(self.combo_tipo.get())

    def ao_clicar_reservar(self, dados_apto):
        """Dispara o fluxo de confirmação de reserva."""
        data_in = self.entry_entrada.get().strip()
        data_out = self.entry_saida.get().strip()
        qt_pessoas = self.combo_qt_pessoas.get()
        
        conta = carregar_conta(getattr(self.app, "usuario", ""))
        dados = conta['perfil']
        # cpf_cliente = simpledialog.askstring(title="Confirme seu CPF", prompt="Confirme o CPF para realizar a reserva.")
        
        if dados:
            Status, dados_cliente = buscar_cliente(dados['cpf'])
            
            mensagem = (
                f"Deseja confirmar a reserva do apartamento {dados_apto['tipo']}"
                f"(Nº {dados_apto.get('numero', 'S/N')})?\n\n"
                f"👤 CPF: {dados['cpf']}\n"
                f"📅 Entrada: {data_in}\n"
                f"📅 Saída: {data_out}\n"
                f"💵 Diária: R$ {float(dados_apto['preco'])*int(qt_pessoas):.2f}\n"
            )
            
            confirmou = messagebox.askyesno("Confirmar Reserva", mensagem, parent=self)
            
            if confirmou:
                Status, dados_ap = BuscarApto(dados_apto.get('numero'))
                
                CadastrarReserva(dados_cliente[0], dados_ap[0], data_in, data_out, qt_pessoas)
                messagebox.showinfo(
                    "Reserva Concluída",
                    f"Reserva para o apartamento {dados_apto['tipo']} realizada com sucesso!",
                    parent=self
                )


# ----------------------------------------------------------------------
# TESTE ISOLADO DA TELA: python -m views.view_reserva
# ----------------------------------------------------------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    janela = ctk.CTk()
    janela.title("Sistema de Reservas - Hotel")
    janela.geometry("1020x620")
    criar_barra_titulo(janela)

    tela = TelaReservas(janela)
    tela.pack(fill="both", expand=True)

    janela.mainloop()
    
    # preciso fazer implementar a quantidade de pessoas na view_reserva.py e armazenar em uma variavel
