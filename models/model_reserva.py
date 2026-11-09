import sqlite3
from datetime import datetime

cx = sqlite3.connect('databank/sistema-hotelaria.db')
cs = cx.cursor()

colunas_permitidas = {"id", "data_entrada",
                      "data_saida", "qt_pessoas", "valor"}


def criar_db_reservas():
    cs.execute('''CREATE TABLE IF NOT EXISTS Reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                id_apto INTEGER NOT NULL,
                data_entrada TEXT NOT NULL,
                data_saida TEXT NOT NULL,
                qt_pessoas INTEGER NOT NULL CHECK (qt_pessoas > 0),
                valor REAL NOT NULL CHECK (valor >= 0),
                CHECK (data_saida > data_entrada),
                FOREIGN KEY (id_cliente) REFERENCES Clientes(id),
                FOREIGN KEY (id_apto) REFERENCES Apartamentos(id))''')
    cx.commit()


def _validar_e_calcular(id_apto, data_entrada, data_saida, qt_pessoas, ignorar_id=None):
    """Valida as regras da reserva e devolve o valor total.
    Levanta ValueError com mensagem pronta para exibir ao usuário."""
    cs.execute("SELECT preco_pessoa, limite_pessoa FROM Apartamentos WHERE id = ?",
               (id_apto,))
    apto = cs.fetchone()
    if apto is None:
        raise ValueError("Apartamento não encontrado.")
    preco_pessoa, limite_pessoa = apto
    if preco_pessoa is None:
        raise ValueError("Este apartamento não tem preço cadastrado.")

    try:
        entrada = datetime.strptime(data_entrada, "%Y-%m-%d")
        saida = datetime.strptime(data_saida, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Datas devem estar no formato AAAA-MM-DD.")

    dias = (saida - entrada).days
    if dias <= 0:
        raise ValueError("A data de saída deve ser após a data de entrada.")

    if qt_pessoas <= 0:
        raise ValueError("A quantidade de pessoas deve ser maior que zero.")
    if limite_pessoa is not None and qt_pessoas > limite_pessoa:
        raise ValueError(
            f"Este apartamento comporta no máximo {limite_pessoa} pessoa(s).")

    cs.execute('''SELECT 1 FROM Reservas
                  WHERE id_apto = ? AND data_entrada < ? AND data_saida > ?
                  AND id != ? LIMIT 1''',
               (id_apto, data_saida, data_entrada, ignorar_id or -1))
    if cs.fetchone():
        raise ValueError("Este apartamento já está reservado nesse período.")

    return preco_pessoa * qt_pessoas * dias


def buscar_db_reserva(id_cliente):
    try:
        cs.execute("SELECT * FROM Reservas WHERE id_cliente = ?", (id_cliente,))
        return cs.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar reservas: {e}")
        return []


def listar_db_reservas():
    try:
        cs.execute("SELECT * FROM Reservas ORDER BY data_entrada")
        return cs.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar reservas: {e}")
        return []


def inserir_db_reserva(id_cliente, id_apto, data_entrada, data_saida, qt_pessoas):
    """Retorna o valor total. Levanta ValueError (regra violada) ou sqlite3.Error."""
    valor = _validar_e_calcular(id_apto, data_entrada, data_saida, qt_pessoas)
    try:
        cs.execute('''INSERT INTO Reservas
                      (id_cliente, id_apto, data_entrada, data_saida, qt_pessoas, valor)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (id_cliente, id_apto, data_entrada, data_saida, qt_pessoas, valor))
        cx.commit()
        return True, valor
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Erro ao inserir reserva: {e}")
        raise


def atualizar_db_reserva(id_reserva, data_entrada, data_saida, qt_pessoas):
    """Atualiza datas e quantidade de pessoas, recalculando o valor."""
    cs.execute("SELECT id_apto FROM Reservas WHERE id = ?", (id_reserva,))
    linha = cs.fetchone()
    if linha is None:
        raise ValueError("Reserva não encontrada.")

    valor = _validar_e_calcular(linha[0], data_entrada, data_saida, qt_pessoas,
                                ignorar_id=id_reserva)
    try:
        cs.execute('''UPDATE Reservas
                      SET data_entrada = ?, data_saida = ?, qt_pessoas = ?, valor = ?
                      WHERE id = ?''',
                   (data_entrada, data_saida, qt_pessoas, valor, id_reserva))
        cx.commit()
        return True, valor
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Erro ao atualizar reserva: {e}")
        raise


def deletar_db_reserva(id_reserva):
    """Retorna True se removeu, False se a reserva não existia."""
    try:
        cs.execute("DELETE FROM Reservas WHERE id = ?", (id_reserva,))
        cx.commit()
        return cs.rowcount > 0
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Erro ao deletar reserva: {e}")
        raise
