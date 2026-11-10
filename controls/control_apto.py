from models.model_apto import (
    inserir_db_apto,
    buscar_apto,
    listar_aptos,
    atualizar_db_apto,
    excluir_db_apto,
    COLUNAR_PERMITIDAS
)

def _converter_booleano(valor):
    if isinstance(valor, bool):
        return int(valor)
    
    if valor in (0, 1):
        return int(valor)

    if isinstance(valor, str):
        valor = valor.strip().lower()
        
        if valor in ("sim", "1", "true"):
            return 1
        
        if valor in ("não", "nao", 0, "false"):
            return 0

    raise ValueError("Valor booleano inválido.")


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
