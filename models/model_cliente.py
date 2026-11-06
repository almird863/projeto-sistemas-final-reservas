import sqlite3

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
        return []

def listar_clientes():
    try:
        cs.execute("SELECT * FROM Clientes")
        return cs.fetchall()
    except sqlite3.Error as e:
        return []


def inserir_db_cliente(nome, idade, cpf, cidade_origem, senha):
    try:
        cs.execute('''INSERT INTO Clientes (nome, idade, cpf, cidade_origem, senha)
                      VALUES (?, ?, ?, ?, ?)''',
                   (nome, idade, cpf, cidade_origem, senha))
        cx.commit()
        return True, "Registro de cliente criado com sucesso"
    except sqlite3.IntegrityError:
        cx.rollback()
        return False
    except sqlite3.Error as e:
        cx.rollback()
        return False


def atualizar_db_clientes(a_ser_atualizado, valor_atualizado, id_cliente):
    if a_ser_atualizado not in COLUNAS_PERMITIDAS:
        raise ValueError(f"Coluna inválida: {a_ser_atualizado}")
    try:
        cs.execute(f"UPDATE Clientes SET {a_ser_atualizado} = ? WHERE id = ?",
                   (valor_atualizado, id_cliente))
        cx.commit()
        return True, "Cliente atualizado com sucesso"
    except sqlite3.Error as e:
        cx.rollback()
        return False
        


def excluir_db_clientes(id_cliente):
    try:
        cs.execute("DELETE FROM Clientes WHERE id = ?", (id_cliente,))
        cx.commit()
        return True, "Cliente removido com sucesso"
    except sqlite3.Error as e:
        cx.rollback()
        return False
