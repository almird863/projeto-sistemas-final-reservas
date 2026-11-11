"""
Ponto de entrada do Sistema de Reservas - Hotel
Conduz o fluxo entre a tela de Login e o Menu Principal.

Como rodar (a partir da raiz do projeto):
    python main.py
"""

from views.view_login import LoginView
from views.view_menu_principal import JanelaPrincipal


def main():
    while True:
        # 1. Abre a tela de Login
        login = LoginView()
        login.mainloop()

        # Se fechou a tela no 'X' sem logar, encerra a aplicação
        if not getattr(login, "autenticado", False):
            break

        # 2. Usuário autenticado -> abre o Menu Principal
        usuario = getattr(login, "usuario_logado", "Usuário")
        menu = JanelaPrincipal(usuario=usuario)
        menu.mainloop()

        # Se saiu da conta (clicou em Sair no menu), volta para o Login
        if not getattr(menu, "saiu_da_conta", False):
            break


if __name__ == "__main__":
    main()
