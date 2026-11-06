import sqlite3
from tkinter import messagebox

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()

COLUNAS_PERMITIDAS = {"nome", "idade", "cpf", "cidade_origem", "senha"}


def criar_db_clientes():
    cs.execute('''CREATE TABLE IF NOT EXISTS Clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER,
                cpf TEXT UNIQUE,
                cidade_origem TEXT,
                senha TEXT)''')
    cx.commit()

def buscar_cliente(nome):
    try:
        cs.execute("SELECT * FROM Clientes WHERE nome = ?", (nome,))
        return cs.fetchone()
    except sqlite3.Error as e:
        print(f"Erro ao buscar cliente: {e}")
        return None

def listar_clientes():
    try:
        cs.execute("SELECT * FROM Clientes")
        return cs.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar clientes: {e}")
        return []


def inserir_db_cliente(nome, idade, cpf, cidade_origem, senha):
    try:
        cs.execute('''INSERT INTO Clientes (nome, idade, cpf, cidade_origem, senha)
                      VALUES (?, ?, ?, ?, ?)''',
                   (nome, idade, cpf, cidade_origem, senha))
        cx.commit()
    except sqlite3.IntegrityError:
        cx.rollback()
        messagebox.showerror("Erro!", "Já existe um cliente com esse CPF.")
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Erro ao inserir: {e}")
        messagebox.showerror("Erro!", "Erro ao registrar cliente. Tente novamente.")


def atualizar_db_clientes(a_ser_atualizado, valor_atualizado, id_cliente):
    if a_ser_atualizado not in COLUNAS_PERMITIDAS:
        raise ValueError(f"Coluna inválida: {a_ser_atualizado}")
    try:
        cs.execute(f"UPDATE Clientes SET {a_ser_atualizado} = ? WHERE id = ?",
                   (valor_atualizado, id_cliente))
        cx.commit()
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Erro ao atualizar: {e}")
        messagebox.showerror("Erro!", "Erro ao atualizar cliente. Tente novamente.")


def excluir_db_clientes(id_cliente):
    try:
        cs.execute("DELETE FROM Clientes WHERE id = ?", (id_cliente,))
        cx.commit()
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Erro ao deletar: {e}")
        messagebox.showerror("Erro!", "Erro ao deletar cliente. Tente novamente.")