"""
View de Cadastro de Cliente - Sistema de Reservas - Hotel
Tkinter + CustomTkinter

Como rodar (SEMPRE a partir da pasta raiz do projeto, onde está o main.py):
    pip install customtkinter pillow validate-docbr
    python -m views.view_cadastro_cliente

Esta tela é aberta pelo botão "Cadastre-se" da tela de login.
Quem valida os dados e grava no banco é o CONTROLLER (controls/control_cliente.py).
A view só: 1) lê o que a pessoa digitou, 2) chama o controller, 3) mostra a resposta.
"""

from tkinter import messagebox
import customtkinter as ctk

from views.componentes import (
    AZUL_ESCURO, AZUL_HOVER, LARANJA, FUNDO_DIREITO, BORDA_CAMPO, TEXTO_CINZA,
    criar_barra_titulo, criar_campo, montar_imagem_lateral,
)

# ----------------------------------------------------------------------
# LIGAÇÃO COM O CONTROLLER
# ----------------------------------------------------------------------
# O controller devolve uma tupla: (sucesso, mensagem)
#   sucesso  -> True se cadastrou, False se algo deu errado
#   mensagem -> texto pronto para mostrar na tela
try:
    from controls.control_cliente import cadastra_cliente
except Exception as erro:  # ex.: faltou instalar validate-docbr, ou rodou fora da raiz
    _ERRO_IMPORTACAO = str(erro)

    def cadastra_cliente(nome, idade, cpf, cidade_origem, senha):
        return False, f"Não foi possível carregar o controller:\n{_ERRO_IMPORTACAO}"


# Tamanho da janela e das áreas (a barra azul do topo tem 40 px)
LARGURA_JANELA = 860
ALTURA_JANELA = 700
LARGURA_FOTO = 420


class CadastroView(ctk.CTkToplevel):
    """
    Janela de cadastro. É uma CTkToplevel: uma janela "filha" da janela de login.
    Ao fechar esta janela, a de login continua aberta.
    """

    def __init__(self, master=None):
        super().__init__(master)

        # --------------------------------------------------------------
        # JANELA
        # --------------------------------------------------------------
        self.title("Cadastro - Sistema de Reservas - Hotel")
        self.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}")
        self.resizable(False, False)
        self.configure(fg_color=FUNDO_DIREITO)

        # Mantém esta janela na frente da janela de login
        if master is not None and master.winfo_viewable():
            self.transient(master)

        criar_barra_titulo(self)
        self._criar_painel_esquerdo()
        self._criar_painel_direito()

        # Enter no teclado confirma o cadastro
        self.bind("<Return>", lambda e: self.ao_clicar_confirmar())

        # "Modal": enquanto o cadastro está aberto, o login fica bloqueado.
        # O after() espera a janela aparecer antes de pedir o foco.
        self.after(150, self._ativar)

    def _ativar(self):
        self.lift()
        self.focus_force()
        self.grab_set()
        self.entry_nome.focus()

    # ------------------------------------------------------------------
    # PAINEL ESQUERDO (foto do quarto + onda)
    # ------------------------------------------------------------------
    def _criar_painel_esquerdo(self):
        altura_painel = ALTURA_JANELA - 40  # menos a barra azul do topo
        self.painel_esq = ctk.CTkFrame(
            self, width=LARGURA_FOTO, corner_radius=0, fg_color="#E9E4DA"
        )
        self.painel_esq.pack(side="left", fill="y")
        self.painel_esq.pack_propagate(False)

        # >>> IMAGEM: foto do quarto + onda (veja montar_imagem_lateral em componentes.py)
        self.img_lateral = montar_imagem_lateral(LARGURA_FOTO, altura_painel, altura_onda=120)
        ctk.CTkLabel(
            self.painel_esq,
            text="" if self.img_lateral else "[ FOTO DO QUARTO ]\nviews/assets/foto_quarto.png",
            image=self.img_lateral,
            text_color="#8A8577",
            font=ctk.CTkFont(size=14),
        ).place(x=0, y=0, relwidth=1, relheight=1)

    # ------------------------------------------------------------------
    # PAINEL DIREITO (formulário)
    # ------------------------------------------------------------------
    def _criar_painel_direito(self):
        painel = ctk.CTkFrame(self, corner_radius=0, fg_color=FUNDO_DIREITO)
        painel.pack(side="left", fill="both", expand=True)

        form = ctk.CTkFrame(painel, fg_color="transparent")
        form.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            form, text="Cadastro",
            text_color=AZUL_ESCURO,
            font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
        ).pack()

        ctk.CTkLabel(
            form, text="Crie sua conta para fazer reservas",
            text_color=TEXTO_CINZA,
            font=ctk.CTkFont(family="Segoe UI", size=13),
        ).pack(pady=(2, 18))

        # --- Campos -----------------------------------------------------
        # Cada campo: (placeholder, nome do PNG do ícone, emoji enquanto não há PNG)
        # >>> IMAGEM: coloque os ícones (20x20) em views/assets/ com estes nomes
        self.entry_nome = criar_campo(form, "Nome completo", "icone_campo_user.png", "👤")
        self.entry_idade = criar_campo(form, "Idade", "icone_campo_idade.png", "🎂")
        self.entry_cpf = criar_campo(form, "CPF (somente números)", "icone_campo_cpf.png", "🪪")
        self.entry_cidade = criar_campo(form, "Cidade de origem", "icone_campo_cidade.png", "📍")
        self.entry_senha = criar_campo(
            form, "Senha", "icone_campo_senha.png", "🔒", mostrar="•"
        )
        self.entry_confirmar = criar_campo(
            form, "Confirmar senha", "icone_campo_senha.png", "🔒", mostrar="•"
        )

        # --- Botão Cadastrar -------------------------------------------
        self.btn_cadastrar = ctk.CTkButton(
            form,
            text="Cadastrar",
            width=340, height=48,
            corner_radius=10,
            fg_color=AZUL_ESCURO, hover_color=AZUL_HOVER,
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            command=self.ao_clicar_confirmar,
        )
        self.btn_cadastrar.pack(pady=(14, 18))

        # Linha separadora
        ctk.CTkFrame(form, height=1, width=340, fg_color=BORDA_CAMPO).pack(pady=(0, 12))

        # --- Rodapé: "Já tem conta? Entrar" -----------------------------
        rodape = ctk.CTkFrame(form, fg_color="transparent")
        rodape.pack()
        ctk.CTkLabel(
            rodape, text="Já tem conta?",
            text_color=TEXTO_CINZA,
            font=ctk.CTkFont(family="Segoe UI", size=12),
        ).pack(side="left")

        lbl_entrar = ctk.CTkLabel(
            rodape, text=" Entrar",
            text_color=LARANJA, cursor="hand2",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold", underline=True),
        )
        lbl_entrar.pack(side="left")
        lbl_entrar.bind("<Button-1>", lambda e: self.ao_clicar_voltar())

    # ------------------------------------------------------------------
    # AÇÕES
    # ------------------------------------------------------------------
    def ao_clicar_confirmar(self):
        """Lê os campos, chama o controller e mostra o resultado."""
        nome = self.entry_nome.get().strip()
        idade = self.entry_idade.get().strip()
        cpf = self.entry_cpf.get().strip()
        cidade = self.entry_cidade.get().strip()
        senha = self.entry_senha.get()
        confirmar = self.entry_confirmar.get()

        # Esta checagem é da TELA (o controller não recebe a "confirmação")
        if senha != confirmar:
            messagebox.showerror("Cadastro", "As senhas não conferem.", parent=self)
            return

        # Todo o resto (campos vazios, CPF válido, idade...) o controller valida
        sucesso, mensagem = cadastra_cliente(nome, idade, cpf, cidade, senha)

        if sucesso:
            messagebox.showinfo("Cadastro", mensagem, parent=self)
            self.destroy()  # fecha o cadastro e volta para o login
        else:
            messagebox.showerror("Cadastro", mensagem, parent=self)

    def ao_clicar_voltar(self):
        """Fecha o cadastro sem salvar (volta para o login)."""
        self.destroy()


# ----------------------------------------------------------------------
# TESTE ISOLADO: python -m views.view_cadastro_cliente
# ----------------------------------------------------------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    raiz = ctk.CTk()
    raiz.withdraw()  # esconde a janela "pai" vazia
    tela = CadastroView(raiz)
    # Quando a tela de cadastro fechar (X, "Entrar" ou cadastro feito), encerra o programa
    tela.bind("<Destroy>", lambda e: raiz.destroy() if e.widget is tela else None)
    raiz.mainloop()
    
    
    
    
    

# from controls.control_cliente import cadastra_cliente

# get

# def cadastra():
#     if cadastra_cliente("a", 1, 1, 1, 1):
#         alert(deu certo)
#     else:
#         alert(deu ruim)