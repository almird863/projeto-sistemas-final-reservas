import sqlite3

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()


def criar_db_reservas():
    cs.execute('''CREATE TABLE IF NOT EXISTS Reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_cliente TEXT NOT NULL,
                data_entrada DATE NOT NULL,
                data_saida DATE NOT NULL,
                tipo_apto TEXT NOT NULL,
                qt_pessoas INTEGER NOT NULL,
                valor FLOAT NOT NULL)''')
