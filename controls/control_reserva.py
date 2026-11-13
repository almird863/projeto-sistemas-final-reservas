from models.model_reserva import (
    inserir_db_reserva,
    buscar_db_reserva,
    listar_db_reservas,
    atualizar_db_reserva,
    deletar_db_reserva,
    # NOVO: check-in / check-out
    adicionar_coluna_checkin,
    listar_db_reservas_para_checkin,
    listar_db_reservas_hospedadas,
    listar_db_reservas_concluidas,
    marcar_checkin_db,
    marcar_checkout_db,
)
from models.model_apto import atualizar_db_apto

<<<<<<< HEAD
#-------------------------------------------------- CADASTRAR RESERVA
=======

>>>>>>> view
def CadastrarReserva(id_cliente, id_apto, data_entrada, data_saida, qt_pessoas):
    try:
        # validar preenchimento
        campos = [id_cliente, id_apto, data_entrada, data_saida, qt_pessoas]
        
        if any(campo is None or not str(campo).strip() for campo in campos):
            return False, "Preencha todos os campos."

        # conversão
        id_cliente = int(id_cliente)
        id_apto = int(id_apto)
        qt_pessoas = int(qt_pessoas)

        if id_cliente <= 0 or id_apto <= 0 or qt_pessoas <= 0:
            return False, "IDs e quantidade de pessoas devem ser positivos."

        # inserção no banco de dados
        resultado, valor = inserir_db_reserva(
            id_cliente, id_apto,
            data_entrada, data_saida,
            qt_pessoas)

        if resultado:
            resultado, valor = atualizar_db_apto("vago", 0, id_apto)
            
            return True, f"Reserva cadastrada! Valor total: R${valor:.2f}"
        return False, "Não foi possível cadastrar a reserva."

    except ValueError as erro:
        return False, str(erro)
    except Exception as erro:
        return False, f"Erro ao cadastrar reserva: {erro}"

#-------------------------------------------------- ATUALIZAR RESERVA
def AtualizarReserva(id_reserva, data_entrada, data_saida, qt_pessoas):
    try:
        # validar preenchimento
        campos = [id_reserva, data_entrada, data_saida, qt_pessoas]
        
        if any(campo is None or not str(campo).strip() for campo in campos):
            return False, "Preencha todos os campos."
        
        # conversão
        id_reserva = int(id_reserva)
        qt_pessoas = int(qt_pessoas)


        if id_reserva <= 0 or qt_pessoas <= 0:
            return False, "ID da reserva e quantidade de pessoas devem ser positivos."
        
        resultado, valor = atualizar_db_reserva(
            id_reserva, data_entrada, data_saida, qt_pessoas
        )

        if resultado:
            return True, f"Reserva atualizada! Valor total: R${valor:.2f}"

        return False, "Não foi possível atualizar a reserva."

    except ValueError as erro:
        return False, str(erro)
    except Exception as erro:
        return False, f"Erro ao atualizar reserva: {erro}."


#-------------------------------------------------- BUSCAR RESERVA
def BuscarReserva(id_cliente):
    try:
        # validar preenchimento
        if id_cliente is None or not str(id_cliente).strip():
            return False, "Informe o ID do cliente."

        # conversão
        id_cliente = int(id_cliente)

        if id_cliente <= 0:
            return False, "O ID do cliente deve ser positivo."

        resultado = buscar_db_reserva(id_cliente)

        if resultado:
            return True, resultado

        return False, "Nenhuma reserva encontrada."

    except ValueError as erro:
        return False, str(erro)
    except Exception as erro:
        return False, f"Erro ao buscar reserva: {erro}."


#-------------------------------------------------- LISTAR RESERVAS
def ListarReservas():
    try:
        resultado = listar_db_reservas()

        if not resultado:
            return False, "Nenhuma reserva encontrada."

        return True, resultado

    except ValueError as erro:
        return False, str(erro)
    except Exception as erro:
        return False, f"Erro ao listar reservas: {erro}"


#-------------------------------------------------- DELETAR RESERVAS
def DeletarReserva(id_reserva):
    try:
        if id_reserva is None or not str(id_reserva).strip():
            return False, "Informe o ID da reserva."

        id_reserva = int(id_reserva)
        
        if id_reserva <= 0:
            return False, "O ID da reserva deve ser positivo."
        
        resultado = deletar_db_reserva(id_reserva)
        if resultado:
            return True, "Reserva deletada com sucesso."

        return False, "Reserva não encontrada."

    except ValueError as erro:
        return False, str(erro)
    except Exception as erro:
        return False, f"Erro ao deletar reserva: {erro}."
