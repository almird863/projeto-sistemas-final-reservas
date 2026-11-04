import sqlite3

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()

def criar_db_aptos():
    cs.execute('''CREATE TABLE IF NOT EXISTS Apartamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                numeracao INTEGER NOT NULL,
                vago BOOLEAN,
                preco_pessoa FLOAT)''')
