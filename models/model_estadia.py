import sqlite3
from datetime import datetime

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()

def criar_tabela_estadia():
    cs.execute('''CREATE TABLE IF NOT EXISTS Estadias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_hospede INTEGER NOT NULL,
                id_uh INTEGER NOT NULL,
                checkin_data DATE NOT NULL,
                checkin_hora TIME NOT NULL,
                checkout_data DATE NOT NULL,
                checkout_hora TIME NOT NULL,
                qt_pessoas INTEGER NOT NULL CHECK (qt_pessoas > 0),
                status TEXT NOT NULL DEFAULT 'em aberto' CHECK (status IN ('concluido', 'em aberto', 'check-in feito', 'cancelado')),
                CHECK (checkout_data > checkin_data),
                FOREIGN KEY (id_hospede) REFERENCES Hospedes(id),
                FOREIGN KEY (id_uh) REFERENCES Unidade_Habitacional(id))''')
    cx.commit()


# -------------------------------------------------------------------------------------- BUSCAR


def buscar_estadia():
    try:
        cs.execute("SELECT * FROM Estadias")

        return True, cs.fetchall()
    
    except sqlite3.Error as e:
        print(f"Erro ao listar reservas: {e}")
        
        return False, []


def buscar_estadia_por_hospede(id_hospede):
    try:
        cs.execute("SELECT * FROM Estadias ORDER BY checkin_data WHERE id_hospede = ?", (id_hospede,))
        return True, cs.fetchall

    except sqlite3.Error as e:
        print(f"Erro ao listar reservas: {e}")

        return False, []

