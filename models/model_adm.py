import sqlite3

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()

def criar_tabela_adm():
    cs.execute('''CREATE TABLE IF NOT EXISTS Administradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                senha TEXT NOT NULL)''')
    cx.commit()


# -------------------------------------------------------------------------------------- INSERIR

def inserir_administrador(usuario, senha):
    try:
        cs.execute("INSERT INTO Administradores (usuario, senha) VALUES (?, ?)", (usuario, senha))
        cx.commit()

        return True, "Administrador cadastrado com sucesso"

    except sqlite3.Error as e:
        cx.rollback()

        return False, f"Erro ao cadastrar administrador: {e}"


# -------------------------------------------------------------------------------------- BUSCAR


def buscar_administrador():
    try:
        cs.execute("SELECT usuario FROM Administradores")
        
        return True, cs.fetchall()

    except sqlite3.Error as e:

        return False, []


def buscar_administrador_por_usuario(usuario):
    try:
        cs.execute("SELECT * FROM Administradores WHERE usuario = ?", (usuario,))

        return True, cs.fetchone()

    except sqlite3.Error as e:

        return False, []


# -------------------------------------------------------------------------------------- ATUALIZAR


def atualizar_senha(senha, id):
    try:
        cs.execute("UPDATE Administradores SET senha = ? WHERE id = ?", (senha, id))
        cx.commit()

        return True, "Senha atualizada com sucesso"

    except sqlite3.Error as e:
        cx.rollback()

        return False, f"Erro ao atualizar a senha: {e}"


def atualizar_usuario(usuario, id):
    try:
        cs.execute("UPDATE Administradores SET usuario = ? WHERE id = ?", (usuario, id))
        cx.commit()

        return True, "Usuario atualizado com sucesso"

    except sqlite3.Error as e:
        cx.rollback()

        return False, f"Erro ao atualizar o usuário: {e}"


# -------------------------------------------------------------------------------------- DELETAR


def deletar_administrador(id):
    try:
        cs.execute("DELETE FROM Administradores WHERE id = ?", (id,))
        cx.commit()

        return True, "Usuário deletado com sucesso."

    except sqlite3.Error as e:
        cx.rollback()

        return False, f"Erro ao deletar usuário: {e}"

