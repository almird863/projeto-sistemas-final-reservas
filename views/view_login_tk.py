import tkinter as tk
from tkinter import messagebox

root = tk.Tk()

root.title('Sistema de Reservas - Hotel')
root.geometry('800x500')
root.resizable(False, False)

# Cor de fundo da janela
root.configure(bg='#EEF2F7')

# Painel que agrupa os componentes do login
painel_login = tk.Frame(
    root,
    bg='#FFFFFF',
    padx=35,
    pady=30
)

# Posiciona o painel à direita
painel_login.pack(
    side='right',
    padx=10,
    pady=70
)

# Título
titulo = tk.Label(
    painel_login,
    text='Login',
    font=('Arial', 18, 'bold'),
    bg='#FFFFFF'
)
titulo.pack(pady=10)

# Texto de orientação
label_login = tk.Label(
    painel_login,
    text='Acesse sua conta para continuar',
    bg='#FFFFFF'
)
label_login.pack(pady=10)

# Campo de usuário
label_usuario = tk.Label(
    painel_login,
    text='Usuário:',
    bg='#FFFFFF'
)
label_usuario.pack(anchor='w')

entrada_login = tk.Entry(painel_login, width=30)
entrada_login.pack(pady=5)

# Campo de senha
label_senha = tk.Label(
    painel_login,
    text='Senha:',
    bg='#FFFFFF'
)
label_senha.pack(anchor='w')

entrada_senha = tk.Entry(
    painel_login,
    width=30,
    show='*'
)
entrada_senha.pack(pady=5)

# Botão de login
btn_login = tk.Button(
    painel_login,
    text='Entrar',
    width=20
)
btn_login.pack(pady=15)

# Opção de cadastro
label_cadastro = tk.Label(
    painel_login,
    text='Não tem conta?',
    bg='#FFFFFF'
)
label_cadastro.pack()

btn_cadastro = tk.Button(
    painel_login,
    text='Cadastre-se',
    width=20
)
btn_cadastro.pack(pady=5)

root.mainloop()