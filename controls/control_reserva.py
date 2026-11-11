from models.model_reserva import (
    inserir_db_reserva, 
    buscar_db_reserva, 
    listar_db_reservas, 
    atualizar_db_reserva, 
    deletar_db_reserva
)

#-------------------------------------------------- CADASTRAR RESERVA
def CadastrarReserva(id_cliente, id_apto, data_entrada, data_saida, qt_pessoas):
    try:
        # validar preenchimento
        campos = [id_cliente, id_apto, data_entrada, data_saida, qt_pessoas]
        
        if any(campo is None or not str(campo).strip() for campo in campos):
            return False, "Preencha todos os campos."

        # conversao
        id_cliente = int(id_cliente)
        id_apto = int(id_apto)
        qt_pessoas = int(qt_pessoas)

        if id_cliente <= 0 or id_apto <= 0 or qt_pessoas <= 0:
            return False, "IDs e quantidade de pessoas devem ser positivos."

        # insersao no banco de dados
        resultado, valor = inserir_db_reserva(
            id_cliente, id_apto,
            data_entrada, data_saida,
            qt_pessoas)

        if resultado:
            return True, f"Reserva cadastrada! Valor total: R${valor:.2f}"
        return False, "Não foi possível cadastrar a reserva."

    except ValueError as erro:
        return False, str(erro)
    except Exception as erro:
        return False, f"Erro ao cadastrar reserva: {erro}"

#--------------------------------------------------
