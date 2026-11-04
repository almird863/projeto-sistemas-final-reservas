import sqlite3

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()

def criar_db_clientes():
    cs.execute('''CREATE TABLE IF NOT EXISTS Clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER,
                cpf INTEGER,
                cidade_origem TEXT
                senha TEXT)''')

def criar_db_aptos():
    cs.execute('''CREATE TABLE IF NOT EXISTS Apartamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                numeracao INTEGER NOT NULL,
                vago BOOLEAN,
                preco_pessoa FLOAT)''')

def criar_db_reservas():
    cs.execute('''CREATE TABLE IF NOT EXISTS Reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_cliente TEXT NOT NULL,
                data_entrada DATE NOT NULL,
                data_saida DATE NOT NULL,
                tipo_apto TEXT NOT NULL,
                qt_pessoas INTEGER NOT NULL,
                valor FLOAT NOT NULL)''')


criar_db_clientes()
criar_db_aptos()
criar_db_reservas()