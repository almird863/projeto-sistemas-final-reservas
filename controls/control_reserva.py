from models.model_reserva import (
    inserir_db_reserva, 
    buscar_db_reserva, 
    listar_db_reservas, 
    atualizar_db_reserva, 
    deletar_db_reserva
)

def CadastrarReserva(id_cliente, id_apto, data_entrada, data_saida, qt_pessoas):
    try:
        if not all([id_cliente, id_apto, data_entrada, data_saida, qt_pessoas]):
            return False, "Preencha todos os campos."

        qt_pessoas = int(qt_pessoas)
        resultado, valor = inserir_db_resreva(
            id_cliente, id_apto,
            data_entrada, data_saida,
            qt_pessoas
        )

        if resultado:
            return True, f"Reserva cadastrada! Valor total: R${valor:.2f}"
        return False, "Não foi possível cadastrar a reserva."
    
    except ValueError as erro:
        return False, str(erro)
    except Exception as erro:
        return False, f"Erro ao cadastrar reserva: {erro}"