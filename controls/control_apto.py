from models.model_apto import (
    inserir_db_apto,
    buscar_apto,
    listar_aptos,
    atualizar_db_apto,
    excluir_db_apto,
    COLUNAS_PERMITIDAS
)

import math

def _converter_booleano(valor):
    if isinstance(valor, bool):
        return int(valor)
    
    if valor in (0, 1):
        return int(valor)

    if isinstance(valor, str):
        valor = valor.strip().lower()
        
        if valor in ("sim", "1", "true"):
            return 1
        
        if valor in ("não", "nao", "0", "false"):
            return 0

    raise ValueError("Valor booleano inválido.")

# --------------------------------------------- CADASTRAR APARTAMENTOS
def CadastrarApto(tipo, numeracao, vago, preco_pessoa, limite_pessoa):
    try:
        if not all([
            tipo, numeracao is not None, vago is not None,
            preco_pessoa is not None, limite_pessoa is not None
        ]):
            return False, "Preencha todos os campos."
        
        tipo = str(tipo).strip()
        numeracao = int(numeracao)
        vago = _converter_booleano(vago)
        preco_pessoa = float(preco_pessoa)
        if not math.isfinite(preco_pessoa):
            return False, "O preço deve ser um número finito."
        limite_pessoa = int(limite_pessoa)
        
        if not tipo:
            return False, "O tipo de apartamento é obrigatório."
        
        if numeracao <= 0:
            return False, "A numeração deve ser positiva."
        
        if preco_pessoa < 0:
            return False, "O preço não pode ser negativo."
        
        if limite_pessoa <= 0:
            return False, "O limite de pessoas deve ser positivo."
        
        resultado = inserir_db_apto(tipo, numeracao, vago, preco_pessoa, limite_pessoa)
        if resultado:
            return True, "Apartamento cadastrado com sucesso."
        
        return False, "Não foi possível cadastrar o apartamento."
    except (ValueError, TypeError) as erro:
        return False, str(erro)
    except Exception as erro:
        return False, f"Erro ao cadastrar apartamento: {erro}"

        
# --------------------------------------------- ATUALIZAR APARTAMENTOS
def AtualizarApto(coluna, novo_valor, id_apto):

    if coluna not in COLUNAS_PERMITIDAS:
        return False, "Não é permitido alterar essa coluna."

    if novo_valor is None or (
        isinstance(novo_valor, str) and not novo_valor.strip()
    ):
        return False, "Valor não pode ser vazio."

    try:
        id_apto = int(id_apto)
        
        if id_apto <= 0:
            return False, "ID inválido."
        
        # conversões
        if coluna == "preco_pessoa":
            novo_valor = float(novo_valor)

        elif coluna in ("numeracao", "limite_pessoa", "qt_camas"):
            novo_valor = int(novo_valor)

        elif coluna in (
            "vago", "pet_friendly", "vista_mar",
            "frigobar", "mesa_sinuca"
        ):
            novo_valor = _converter_booleano(novo_valor)

        elif coluna == "tipo":
            novo_valor = str(novo_valor).strip()

        # validações
        if coluna == "preco_pessoa" and novo_valor < 0:
            return False, "O preço não pode ser negativo."

        if coluna == "preco_pessoa" and not math.isfinite(novo_valor):
            return False, "O preço deve ser um número finito."

        if coluna == "numeracao" and novo_valor <= 0:
            return False, "A numeração deve ser positiva."

        if coluna == "limite_pessoa" and novo_valor <= 0:
            return False, "O número de pessoas deve ser positivo."

        if coluna == "qt_camas" and novo_valor < 0:
            return False, "O número de camas deve ser positivo."

        if coluna == "tipo" and not novo_valor:
            return False, "O tipo é obrigatório."

        # atualizar
        resultado = atualizar_db_apto(coluna, novo_valor, id_apto)

        if resultado:
            return True, "Apartamento atualizado com sucesso."

        return False, "Não foi possível atualizar o apartamento."
    
    except (ValueError, TypeError) as erro:
        return False, f"Valor inválido: {erro}."

    except Exception as erro:
        return False, f"Erro ao atualizar apartamento: {erro}."


# --------------------------------------------- EXLCUIR APARTAMENTOS
def ExcluirApto(id_apto):
    try:
        id_apto = int(id_apto)

        if id_apto <= 0:
            return False, "ID inválido."

        resultado = excluir_db_apto(id_apto)
        if resultado:
            return True, "Apartamento excluído com sucesso."
    
        return False, "Não foi possível excluir o apartamento."        
    except (ValueError, TypeError):
        return False, "ID inválido."
    except Exception as erro:
        return False, f"Erro ao excluir apartamento: {erro}."

        
# --------------------------------------------- LISTAR APARTAMENTOS
def ListarAptos(somente_vagos=False):
    try:
        resultado = listar_aptos(somente_vagos)
        return True, resultado
    except Exception as erro:
        return False, f"Erro ao listar apartamentos: {erro}."


# --------------------------------------------- BUSCAR APARTAMENTOS
def BuscarApto(numero):
    try:
        numero = int(numero)
        if numero <= 0:
            return False, "Numeração inválida."

        resultado = buscar_apto(numero)

        if resultado:
            return True, resultado

        return False, "Apartamento não encontrado."
    except Exception as erro:
        return False, f"Erro ao buscar apartamento: {erro}."
