import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title('Sistema de Reservas - Hotel')
root.geometry('800x500')
root.resizable(False, False)

titulo = tk.Label(
    root,
    text='Login',
    font=('Arial', 18, 'bold')
)
titulo.pack()

label_login = tk.Label(root, text='Acesse sua conta para continuar')
label_login.pack()

label_usuario = tk.Label(root, text='Usuário: ')
label_usuario.pack()
entrada_login = tk.Entry(root, )
entrada_login.pack()


label_senha = tk.Label(root, text=' Senha: ')
label_senha.pack()
entrada_senha = tk.Entry(root, )
entrada_senha.pack()

btn_login = tk.Button(root, text='✅ Entrar', width=10)
btn_login.pack()

label_cadastro = tk.Label(root, text='Não tem conta? ')
label_cadastro.pack()
entrada_cadastro = tk.Entry(root)

btn_cadastro = tk.Button(root, text='Cadastre-se')
btn_cadastro.pack()


root.mainloop()