import sqlite3

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()

def criar_tabela_adm():
    cs.execute('''CREATE TABLE IF NOT EXISTS Administradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                senha TEXT NOT NULL)''')
    cx.commit()
