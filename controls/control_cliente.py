from models.model_cliente import inserir_db_cliente
from validate_docbr import CPF

def cadastra_cliente(nome, idade, cpf, cidade_origem, senha):
    """
    Validar dados da View e solicitar cadastro ao Model

    argumentos:
        nome do cliente - string
        idade do cliente - integer
        cpf - string 
        cidade_origem - string
        senha - string

    o padrão é retornar uma tupla:
        return(sucesso, mensagem) - para puxar um messagebox na view
    """

    # verificação para campos vazios
    if not nome.strip():
        return False, "O nome é obrigatório."

    if not cpf.strip():
        return False, "O CPF é obrigatório"

    if not cidade_origem.strip():
        return False, "A cidade de origem é obrigatória."

    if not senha:
        return False, "A senha é obrigatória."

    # verificação CPF válido
    documento = CPF()
    
    if not documento.validate(cpf):
        return False, "CPF inválido."

    # verificação para idade
    # 1 - tipo errado
    try:
        idade = int(idade)
    except (ValueError, TypeError):
        return False, "A idade deve ser um número inteiro."

    # 2 - nula
    if idade <= 0:
        return False, "A idade deve ser maior que zero."
    # 3 - idade impossivel
    elif idade > 130:
        return False, "A idade deve ser menor que 130."
    #=================== INSERINDO CLIENTE =====================
    try:
        inserir_db_cliente(nome, idade, cpf, cidade_origem, senha)
        return True, "Sucesso ao cadastrar cliente."
    except Exception as e:
        return False, f"Erro, ao cadastrar cliente: {e}"
