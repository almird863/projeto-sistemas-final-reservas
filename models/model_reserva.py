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
                status TEXT NOT NULL DEFAULT 'em aberto' CHECK (status IN ('concluido', 'em aberto', 'cancelado'))
                CHECK (data_saida > data_entrada),
                FOREIGN KEY (id_cliente) REFERENCES Clientes(id),
                FOREIGN KEY (id_apto) REFERENCES Apartamentos(id))''')
    cx.commit()
    adicionar_coluna_checkin()


# ----------------------------------------------------------------------
# NOVO: controle de check-in / check-out
# ----------------------------------------------------------------------
# A tabela Reservas já tinha "status" ('em aberto' / 'concluido' / 'cancelado'),
# mas isso descreve a reserva em si (se ela existe/foi cancelada/terminou).
# Não existia nada dizendo "o hóspede já chegou (fez check-in) mas ainda não saiu".
#
# Em vez de mexer no CHECK de "status" (o que exigiria recriar a tabela inteira
# no SQLite), foi adicionada uma coluna separada: checkin_feito.
#   checkin_feito = 0 -> reserva em aberto, hóspede ainda não chegou (aguardando check-in)
#   checkin_feito = 1 -> hóspede já chegou (já pode fazer check-out)
# Quando o check-out é feito, a reserva passa para status = 'concluido' (como já era).

def adicionar_coluna_checkin():
    """Migration simples e segura: adiciona a coluna checkin_feito se ainda não existir."""
    try:
        cs.execute(
            "ALTER TABLE Reservas ADD COLUMN checkin_feito INTEGER NOT NULL DEFAULT 0")
        cx.commit()
    except sqlite3.OperationalError:
        pass  # a coluna já existe, não faz nada


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


# ----------------------------------------------------------------------
# NOVO: consultas e ações para a tela de Check-in / Check-out
# ----------------------------------------------------------------------
#
# Observação sobre o JOIN com Apartamentos:
# Estou assumindo que a tabela Apartamentos tem uma coluna chamada "numero"
# com o número do apartamento (ex.: "204"). Se o nome real for outro
# (ex.: "numero_apto", "identificacao"), troque "a.numero" pelo nome certo
# nas três consultas abaixo (está marcado com # AJUSTAR).

def listar_db_reservas_para_checkin():
    """Reservas em aberto cujo hóspede ainda não chegou (aguardando check-in)."""
    try:
        cs.execute('''
            SELECT r.id, r.id_cliente, r.id_apto, r.data_entrada, r.data_saida,
                   r.qt_pessoas, r.valor, r.status, r.checkin_feito,
                   a.numero AS numero_apto
            FROM Reservas r
            LEFT JOIN Apartamentos a ON a.id = r.id_apto  -- AJUSTAR: nome da coluna "numero"
            WHERE r.status = 'em aberto' AND r.checkin_feito = 0
            ORDER BY r.data_entrada
        ''')
        return cs.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar reservas para check-in: {e}")
        return []


def listar_db_reservas_hospedadas():
    """Reservas em aberto cujo hóspede já fez check-in (aguardando check-out)."""
    try:
        cs.execute('''
            SELECT r.id, r.id_cliente, r.id_apto, r.data_entrada, r.data_saida,
                   r.qt_pessoas, r.valor, r.status, r.checkin_feito,
                   a.numero AS numero_apto
            FROM Reservas r
            LEFT JOIN Apartamentos a ON a.id = r.id_apto  -- AJUSTAR: nome da coluna "numero"
            WHERE r.status = 'em aberto' AND r.checkin_feito = 1
            ORDER BY r.data_entrada
        ''')
        return cs.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar reservas hospedadas: {e}")
        return []


def listar_db_reservas_concluidas():
    """Reservas já finalizadas (check-out feito)."""
    try:
        cs.execute('''
            SELECT r.id, r.id_cliente, r.id_apto, r.data_entrada, r.data_saida,
                   r.qt_pessoas, r.valor, r.status, r.checkin_feito,
                   a.numero AS numero_apto
            FROM Reservas r
            LEFT JOIN Apartamentos a ON a.id = r.id_apto  -- AJUSTAR: nome da coluna "numero"
            WHERE r.status = 'concluido'
            ORDER BY r.data_saida DESC
        ''')
        return cs.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar reservas concluídas: {e}")
        return []


def marcar_checkin_db(id_reserva):
    """Marca que o hóspede chegou. Retorna True se encontrou e atualizou a reserva."""
    try:
        cs.execute('''UPDATE Reservas SET checkin_feito = 1
                      WHERE id = ? AND status = 'em aberto' ''', (id_reserva,))
        cx.commit()
        return cs.rowcount > 0
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Erro ao marcar check-in: {e}")
        raise


def marcar_checkout_db(id_reserva):
    """Marca a saída do hóspede: encerra a reserva (status = 'concluido')."""
    try:
        cs.execute('''UPDATE Reservas SET status = 'concluido'
                      WHERE id = ? AND status = 'em aberto' AND checkin_feito = 1''',
                   (id_reserva,))
        cx.commit()
        return cs.rowcount > 0
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Erro ao marcar check-out: {e}")
        raise