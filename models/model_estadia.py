import sqlite3
from datetime import datetime

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()

STATUS_PERMITIDO = ["concluido", "em aberto", "check-in feito", "cancelado"]

def criar_tabela_estadia():
    cs.execute('''CREATE TABLE IF NOT EXISTS Estadias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_hospede INTEGER NOT NULL,
                id_uh INTEGER NOT NULL,
                checkin_data DATE,
                checkin_hora TIME,
                checkout_data DATE,
                checkout_hora TIME,
                qt_pessoas INTEGER NOT NULL CHECK (qt_pessoas > 0),
                status TEXT NOT NULL DEFAULT 'em aberto' CHECK (status IN ('concluido', 'em aberto', 'check-in feito', 'cancelado')),
                CHECK (checkout_data > checkin_data),
                FOREIGN KEY (id_hospede) REFERENCES Hospedes(id),
                FOREIGN KEY (id_uh) REFERENCES Unidade_Habitacional(id))''')
    cx.commit()


# -------------------------------------------------------------------------------------- INSERIR

def inserir_estadia(id_hospede, id_uh, qt_pessoas):
    try:
        cs.execute('''INSERT INTO Estadias (id_hospede, id_uh, qt_pessoas, status)
                    VALUES (?, ?, ?)''', (id_hospede, id_uh, qt_pessoas))
        cx.commit()

        return True, "Cadastro de estadia feito com sucesso."

    except sqlite3.Error as e:
        cx.rollback()

        return False, f"Erro ao realizar cadastro: {e}"


# -------------------------------------------------------------------------------------- BUSCAR


def buscar_estadia():
    try:
        cs.execute("SELECT * FROM Estadias")

        return True, cs.fetchall()
    
    except sqlite3.Error as e:
        print(f"Erro ao buscar reservas: {e}")
        
        return False, []


def buscar_estadia_por_hospede(id_hospede):
    try:
        cs.execute("SELECT * FROM Estadias ORDER BY checkin_data WHERE id_hospede = ?", (id_hospede,))
        
        return True, cs.fetchall()

    except sqlite3.Error as e:
        print(f"Erro ao buscar reservas: {e}")

        return False, []


def buscar_estadias_por_uh(id_uh):
    try:
        cs.execute("SELECT * FROM Estadias ORDER BY id WHERE id_uh = ?", (id_uh,))

        return True, cs.fetchall()

    except sqlite3.Error as e:
        print(f"Erro ao buscar reservas: {e}")


def buscar_estadia_por_checkin(checkin_dia):
    try:
        cs.execute("SELECT * FROM Estadias WHERE checkin_data = ?", (checkin_dia,))

        return True, cs.fetchall()

    except sqlite3.Error as e:
        print(f"Erro ao buscar reservas: {e}")

        return False, []


def buscar_estadia_por_checkout(checkout_dia):
    try:
        cs.execute("SELECT * FROM Estadias WHERE checkout_data = ?", (checkout_dia,))

        return True, cs.fetchall()

    except sqlite3.Error as e:
        print(f"Erro ao buscar reservas: {e}")

        return False, []


def buscar_estadia_por_status(status):
    
    if status in STATUS_PERMITIDO:
        try:
            cs.execute("SELECT * FROM Estadias WHERE status = ?", (status,))

            return True, cs.fetchall()

        except sqlite3.Error as e:
            print(f"Erro ao buscar reservas: {e}")

            return False, []
    else:
        print("Status precise ser um nome válido.")

        return False, []


# -------------------------------------------------------------------------------------- ATUALIZAR

def atualizar_checkin_data_e_hora(id):
    try:
        cs.execute('''UPDATE Estadias SET
                        checkin_data = date('now', 'localtime')
                        checkin_hora = time('now', 'localtime')
                        WHERE id = ?''', (id,))
        cx.commit()

        return True, "Check-in realizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()

        return False, f"Erro ao realizar check-in: {e}"


def atualizar_checkout_data_e_hora(id):
    try:
        cs.execute('''UPDATE Estadias SET
                        checkout_data = date('now', 'localtime')
                        checkout_hora = time('now', 'localtime')
                        WHERE id = ?''', (id,))
        cx.commit()

        return True, "Check-out realizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()

        return False, f"Erro ao realizar check-out: {e}"


def atualizar_estadia_status(status, id):
    
    if status in STATUS_PERMITIDO:
        try:
            cs.execute("UPDATE Estadias SET status = ? WHERE id = ?", (status, id))
            cx.commit()

            return True, "Status atualizado com sucesso."
        except sqlite3.Error as e:
           cx.rollback()

           return False, f"Erro ao atualizar: {e}"
    
    else:
        return False, "Status precisa ser um nome válido"


def atualizar_estadia_pessoas(qt_pessoas, id):
    try:
        cs.execute("UPDATE Estadias SET qt_pessoas = ? WHERE id = ?", (qt_pessoas, id))
        cx.commit()

        return True, "Quantidade de pessoas atualizado com sucesso."

    except sqlite3.Error as e:
        cx.rollback()

        return False, f"Erro ao atualizar: {e}"
