import sqlite3

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()

def criar_db_clientes():
    cs.execute('''CREATE TABLE IF NOT EXISTS Clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER,
                cpf INTEGER,
                cidade_origem TEXT,
                senha TEXT)''')


def inserir_db_cliente(nome, idade, cpf, cidade_origem, senha):
    cs.execute('''INSERT INTO Clientes (nome, idade, cpf, cidade_origem, senha)
               VALUES (?, ?, ?, ?, ?)''', (nome, idade, cpf, cidade_origem, senha))
    cx.commit()


def inserir_db_cliente(nome, idade, cpf, cidade_origem, senha):
    cs.execute('''INSERT INTO Clientes (nome, idade, cpf, cidade_origem, senha)
               VALUES (?, ?, ?, ?, ?)''', (nome, idade, cpf, cidade_origem, senha))
    cx.commit()

