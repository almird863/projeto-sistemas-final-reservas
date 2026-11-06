import sqlite3

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()

COLUNAS_PERMITIDAS = {
    "tipo", "numeracao", "vago", "preco_pessoa", "limite_pessoa",
    "pet_friendly", "qt_camas", "vista_mar", "frigobar", "mesa_sinuca",
}

def criar_db_aptos():
    cs.execute('''CREATE TABLE IF NOT EXISTS Apartamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                numeracao INTEGER NOT NULL UNIQUE,
                vago INTEGER NOT NULL DEFAULT 1 CHECK (vago IN (0, 1)),
                preco_pessoa REAL CHECK (preco_pessoa >= 0),
                limite_pessoa INTEGER CHECK (limite_pessoa > 0),
                pet_friendly INTEGER NOT NULL DEFAULT 0 CHECK (pet_friendly IN (0, 1)),
                qt_camas INTEGER NOT NULL DEFAULT 1 CHECK (qt_camas > 0),
                vista_mar INTEGER NOT NULL DEFAULT 0 CHECK (vista_mar IN (0, 1)),
                frigobar INTEGER NOT NULL DEFAULT 0 CHECK (frigobar IN (0, 1)),
                mesa_sinuca INTEGER NOT NULL DEFAULT 0 CHECK (mesa_sinuca IN (0, 1)))''')
    cx.commit()

def buscar_apto(numero):
    try:
        cs.execute("SELECT * FROM Apartamentos WHERE numeracao = ?", (numero,))
        return cs.fetchone()
    except sqlite3.Error as e:
        print(f"Erro ao buscar apartamento: {e}")
        return None


def listar_aptos(somente_vagos=False):
    try:
        if somente_vagos:
            cs.execute("SELECT * FROM Apartamentos WHERE vago = 1")
        else:
            cs.execute("SELECT * FROM Apartamentos")
        return cs.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar apartamentos: {e}")
        return []


def inserir_db_apto(tipo, numeracao, vago, preco_pessoa, limite_pessoa):
    try:
        cs.execute('''INSERT INTO Apartamentos
                      (tipo, numeracao, vago, preco_pessoa, limite_pessoa)
                      VALUES (?, ?, ?, ?, ?)''',
                   (tipo, numeracao, int(vago), preco_pessoa, limite_pessoa))
        cx.commit()
        return True
    except sqlite3.IntegrityError as e:
        cx.rollback()
        print(f"Violação de regra (número duplicado ou valor inválido): {e}")
        return False
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Erro ao inserir apartamento: {e}")
        return False

def atualizar_db_apto(a_ser_atualizado, valor_atualizado, id_apto):
    if a_ser_atualizado not in COLUNAS_PERMITIDAS:
        raise ValueError(f"Coluna inválida: {a_ser_atualizado}")
    try:
        cs.execute(f"UPDATE Apartamentos SET {a_ser_atualizado} = ? WHERE id = ?",
                   (valor_atualizado, id_apto))
        cx.commit()
        return True
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Erro ao atualizar apartamento: {e}")
        return False


def excluir_db_apto(id_apto):
    try:
        cs.execute("DELETE FROM Apartamentos WHERE id = ?", (id_apto,))
        cx.commit()
        return True
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Erro ao excluir apartamento: {e}")
        return False