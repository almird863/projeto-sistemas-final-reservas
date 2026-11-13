import sqlite3

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()


def criar_tabela_uh():
    cs.execute('''CREATE TABLE IF NOT EXISTS Unidade_Habitacional (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numeracao INTEGER NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'Livre e limpa' CHECK (status IN ('Livre e limpa', 'Em limpeza', 'Hospede na casa', 'Reservado', 'Indisponível')),
                ultima_att_dia DATE DEFAULT (date('now', 'localtime')),
                ultima_att_hora TIME DEFAULT (time('now', 'localtime')),
                vista_mar INTEGER NOT NULL DEFAULT 0 CHECK (vista_mar IN (0, 1)),
                vista_rua INTEGER NOT NULL DEFAULT 0 CHECK (vista_rua IN (0, 1)),
                acessivel INTEGER NOT NULL DEFAULT 0 CHECK (acessivel IN (0, 1)))''')
    cx.commit()

def buscar_uh(numero):
    try:
        cs.execute("SELECT * FROM Apartamentos WHERE numeracao = ?", (numero,))
        return True, cs.fetchone()
    except sqlite3.Error as e:
        print(f"Erro ao buscar apartamento: {e}")
        return False, []