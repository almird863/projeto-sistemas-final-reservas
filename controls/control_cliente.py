from models.model_cliente import inserir_db_cliente

def cadastra_cliente(nome, idade, cpf, cidade_origem, senha):
    """
    Validar dados da View e solicitar cadastro ao Model

    argumentos:
        nome do cliente - string
        idade do cliente - integer
        cpf - string 
        cidade_origem - string
        senha - string

    retorna uma tupla:
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


    # verificação para idade
    # - tipo errado
    try:
        idade = int(idade)
    except (ValueError, TypeError):
        return False, "A idade deve ser um número inteiro."

    # - nula
    if idade <= 0:
        return False, "A idade deve ser maior que zero."

    #=================== INSERINDO CLIENTE =====================
    inserir_db_cliente(nome, idade, cpf, cidade_origem, senha)
    return True