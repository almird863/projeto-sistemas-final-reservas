import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title('Sistema de Reservas - Hotel')
root.geometry('400x600')
root.resizable(False, False)

titulo = tk.Label(
    root,
    text='Login',
    font=('Arial', 18, 'bold')
)
titulo.pack()

labe_login = tk.Label(root, text='Acesse sua conta para continuar')