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


# -------------------------------------------------------------------------------------- BUSCAS

def buscar_hospedes():
    try:
        cs.execute("SELECT * FROM Hospedes")
        return cs.fetchall()
    except sqlite3.Error as e:
        return []

def buscar_hospede_por_cpf(cpf):
    try:
        cs.execute(
            "SELECT * FROM Hospedes WHERE cpf = ?",
            (cpf,)
        )
        return True, cs.fetchone()
    except sqlite3.Error:
        return False, []
    
def buscar_hospede_por_nome(nome):
    try:
        cs.execute(
            "SELECT * FROM Hospedes WHERE nome = ?",
            (nome,)
        )
        return True, cs.fetchone()
    except sqlite3.Error:
        return False, []


# -------------------------------------------------------------------------------------- REGISTRO


def registrar_hospede(nome, cpf, telefone, email):
    try:
        cs.execute('''INSERT INTO Hospedes (nome, cpf, telefone, email)
                      VALUES (?, ?, ?, ?)''',
                   (nome, cpf, telefone, email))
        cx.commit()
        return True, "Registro de cliente criado com sucesso"
    except sqlite3.Error as e:
        cx.rollback()
        return False, f"Erro: {e}"
    
    
# -------------------------------------------------------------------------------------- ATUALIZAÇÕES


def atualizar_nome(nome, id):
    try:
        cs.execute("UPDATE Hospedes SET nome = ? WHERE id = ?", (nome, id))
        cx.commit()
        
        return True, "Registro de nome atualizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"

def atualizar_cpf(cpf, id):
    try:
        cs.execute("UPDATE Hospedes SET cpf = ? WHERE id = ?", (cpf, id))
        cx.commit()
        
        return True, "Registro de CPF atualizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"

def atualizar_telefone(telefone, id):
    try:
        cs.execute("UPDATE Hospedes SET telefone = ? WHERE id = ?", (telefone, id))
        cx.commit()
        
        return True, "Registro de CPF atualizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"
    
def atualizar_email(email, id):
    try:
        cs.execute("UPDATE Hospedes SET email = ? WHERE id = ?", (email, id))
        cx.commit()
        
        return True, "Registro de Email atualizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"

def atualizar_data_nascimento(data, id):
    try:
        cs.execute("UPDATE Hospedes SET data_nascimento = ? WHERE id = ?", (data, id))
        cx.commit()
        
        return True, "Registro de Data de Nascimento atualizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"

def atualizar_cep(cep, id):
    try:
        cs.execute("UPDATE Hospedes SET cep = ? WHERE id = ?", (cep, id))
        cx.commit()
        
        return True, "Registro de CEP atualizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"

def atualizar_residencia(residencia, id):
    try:
        cs.execute("UPDATE Hospedes SET residencia_permanente = ? WHERE id = ?", (residencia, id))
        cx.commit()
        
        return True, "Registro de Residência Permanente atualizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"

def atualizar_bairro(bairro, id):
    try:
        cs.execute("UPDATE Hospedes SET bairro = ? WHERE id = ?", (bairro, id))
        cx.commit()
        
        return True, "Registro de Bairro atualizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"
    
def atualizar_cidade(cidade, id):
    try:
        cs.execute("UPDATE Hospedes SET cidade = ? WHERE id = ?", (cidade, id))
        cx.commit()
        
        return True, "Registro de Cidade atualizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"
    
def atualizar_estado(estado, id):
    try:
        cs.execute("UPDATE Hospedes SET estado = ? WHERE id = ?", (estado, id))
        cx.commit()
        
        return True, "Registro de Estado atualizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"
    
def atualizar_pais(pais, id):
    try:
        cs.execute("UPDATE Hospedes SET pais = ? WHERE id = ?", (pais, id))
        cx.commit()
        
        return True, "Registro de Estado atualizado com sucesso."
    
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"
    
    
# -------------------------------------------------------------------------------------- EXCLUSÕES

def excluir_hospede(id):
    try:
        cs.execute("DELETE FROM Hospedes WHERE id = ?", (id,))
        cx.commit()
        
        return True, "Registro de hospede deletado com sucesso."
    except sqlite3.Error as e:
        cx.rollback()
        
        return False, f"Erro: {e}"