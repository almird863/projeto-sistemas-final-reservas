from models.model_cliente import (
    inserir_db_cliente,
    buscar_cliente_por_cpf
)

from validate_docbr import CPF
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

#------------------- CRIPTOGRAFIA ----------------------------
ph = PasswordHasher()
def gerar_hash_senha(senha):
    return ph.hash(senha)

#------------------- FUNÇÃO DE CADASTRO ----------------------------
def CadastrarCliente(nome, idade, cpf, cidade_origem, senha):
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

    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres."

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
        senha_criptografada = gerar_hash_senha(senha) # gera a senha do novo user
        resultado = inserir_db_cliente(nome, idade, cpf, cidade_origem, senha_criptografada)
        
        if resultado is False:
            return False, "Não foi possível cadastrar o cliente."
        
        sucesso, mensagem = resultado
        return sucesso, mensagem
    except Exception as e:
        return False, f"Erro ao cadastrar cliente: {e}"


#------------------- FUNÇÃO DE LOGIN ----------------------------
def AutenticarCliente(cpf, senha):
    # Buscar cliente no banco de dados
    cliente = buscar_cliente_por_cpf(cpf)

    # verificar se cliente existe
    if cliente is None:
        return False, "CPF não encontrado."

    try:
        ph.verify(cliente[5], senha)

    except VerifyMismatchError:
        return False, "Senha incorreta."
    except VerificationError:
        return False, "Não foi possível verificar a senha."

    return True, "Login realizado com sucesso."