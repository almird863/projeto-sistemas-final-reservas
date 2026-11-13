import sqlite3
from datetime import date


def carregar_conta(cpf):
    """Carrega o perfil e as reservas vinculadas ao CPF autenticado."""
    conexao = sqlite3.connect("databank/sistema-hotelaria.db")
    try:
        cursor = conexao.cursor()
        cursor.execute(
            """SELECT id, nome, cpf, idade, cidade_origem
               FROM Clientes
               WHERE cpf = ?""",
            (cpf,),
        )
        cliente = cursor.fetchone()

        perfil = {
            "nome": "—",
            "cpf": "—",
            "idade": "—",
            "cidade": "—",
            "encontrado": cliente is not None,
        }
        if cliente is None:
            return {"perfil": perfil, "atual": None, "historico": []}

        perfil.update({
            "nome": cliente[1] or "—",
            "cpf": cliente[2] or "—",
            "idade": cliente[3] if cliente[3] is not None else "—",
            "cidade": cliente[4] or "—",
        })

        cursor.execute(
            """SELECT r.id, a.numeracao, r.data_entrada, r.data_saida,
                      r.qt_pessoas, r.valor, r.status
               FROM Reservas AS r
               LEFT JOIN Apartamentos AS a ON a.id = r.id_apto
               WHERE r.id_cliente = ?
               ORDER BY r.data_entrada, r.id""",
            (cliente[0],),
        )

        hoje = date.today().isoformat()
        reservas = []
        for reserva in cursor.fetchall():
            if reserva[6] == "cancelado":
                status = "Cancelada"
            elif reserva[6] == "concluido" or reserva[3] <= hoje:
                status = "Concluída"
            elif reserva[2] <= hoje:
                status = "Em andamento"
            else:
                status = "Futura"

            reservas.append({
                "id": reserva[0],
                "apartamento": reserva[1] if reserva[1] is not None else "—",
                "entrada": reserva[2],
                "saida": reserva[3],
                "pessoas": reserva[4],
                "valor": f"R$ {reserva[5]:.2f}",
                "status": status,
            })

        ativas = [r for r in reservas if r["status"] in ("Em andamento", "Futura")]
        atual = next(
            (r for r in ativas if r["status"] == "Em andamento"),
            ativas[0] if ativas else None,
        )
        historico = [
            r for r in reservas if r["status"] in ("Concluída", "Cancelada")
        ]

        return {"perfil": perfil, "atual": atual, "historico": historico}
    finally:
        conexao.close()
