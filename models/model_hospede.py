import sqlite3

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()

def criar_tabela_hospedes():
    cs.execute('''
               CREATE TABLE IF NOT EXISTS Hospedes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   cpf TEXT NOT NULL,
                   telefone TEXT NOT NULL,
                   email TEXT NOT NULL,
                   data_nascimento DATE,
                   cep TEXT,
                   residencia_permanente TEXT,
                   bairro TEXT,
                   cidade TEXT,
                   estado TEXT,
                   pais TEXT
               )''')

def listar_hospedes():
    try:
        cs.execute("SELECT * FROM Hospedes")
        return cs.fetchall()
    except sqlite3.Error as e:
        return []

def listar_hospedes_por_cpf(cpf):
    try:
        cs.execute(
            "SELECT * FROM Hospedes WHERE cpf = ?",
            (cpf,)
        )
        return True, cs.fetchone()
    except sqlite3.Error:
        return False, []
    
def listar_hospedes_por_nome(nome):
    try:
        cs.execute(
            "SELECT * FROM Hospedes WHERE nome = ?",
            (nome,)
        )
        return True, cs.fetchone()
    except sqlite3.Error:
        return False, []

def registrar_hospede(nome, idade, cpf, cidade_origem, senha):
    try:
        cs.execute('''INSERT INTO Clientes (nome, idade, cpf, cidade_origem, senha)
                      VALUES (?, ?, ?, ?, ?)''',
                   (nome, idade, cpf, cidade_origem, senha))
        cx.commit()
        return True, "Registro de cliente criado com sucesso"
    except sqlite3.IntegrityError:
        cx.rollback()
        return False, "Erro de integridade"
    except sqlite3.Error as e:
        cx.rollback()
        return False, f"Erro: {e}"