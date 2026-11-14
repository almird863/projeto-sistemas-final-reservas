from models import (model_estadia)

def listar_estadias():
    sucesso, estadias = model_estadia.buscar_estadia()
    
    if not sucesso:
        return False, "Erro ao listar estadias."

    return True, estadias


def buscar_estadia_por_hospede(id_hospede):
    try:
        id_hospede = int(id_hospede)

        if id_hospede <= 0:
            return False, "ID do hóspede inválido."

    except (ValueError, TypeError):
            return False, "O ID deve ser um número."

    sucesso, estadias = model_estadia.buscar_estadia_por_hospede(id_hospede)

    if not sucesso:
        return False, "Erro ao buscar estadias do hóspede."
    
    return True, estadias