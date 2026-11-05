import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title('Sistema de Reservas - Hotel')
root.geometry('600x400')
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

root.mainloop()