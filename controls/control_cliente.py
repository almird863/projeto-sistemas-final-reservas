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


#------------------- CONTROLE DE SESSÃO ----------------------------

cliente_logado = None


def VerificarLogin(id_cliente):
    try:
        return (
            cliente_logado is not None
            and cliente_logado == int(id_cliente)
        )
    except (ValueError, TypeError):
        return False


def DeslogarCliente():
    global cliente_logado
    cliente_logado = None


#------------------- FUNÇÃO DE CADASTRO ----------------------------

def CadastrarCliente(nome, idade, cpf, cidade_origem, senha):

    if not nome.strip():
        return False, "O nome é obrigatório."

    if not cpf.strip():
        return False, "O CPF é obrigatório."

    if not cidade_origem.strip():
        return False, "A cidade de origem é obrigatória."

    if not senha:
        return False, "A senha é obrigatória."

    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres."

    documento = CPF()

    if not documento.validate(cpf):
        return False, "CPF inválido."

    try:
        idade = int(idade)
    except (ValueError, TypeError):
        return False, "A idade deve ser um número inteiro."

    if idade <= 0:
        return False, "A idade deve ser maior que zero."

    elif idade > 130:
        return False, "A idade deve ser menor que 130."

    try:
        senha_criptografada = gerar_hash_senha(senha)

        resultado = inserir_db_cliente(
            nome,
            idade,
            cpf,
            cidade_origem,
            senha_criptografada
        )

        if resultado is False:
            return False, "Não foi possível cadastrar o cliente."

        sucesso, mensagem = resultado
        return sucesso, mensagem

    except Exception as e:
        return False, f"Erro ao cadastrar cliente: {e}"


#------------------- FUNÇÃO DE LOGIN ----------------------------

def AutenticarCliente(cpf, senha):
    global cliente_logado

    if not cpf.strip():
        return False, "O CPF é obrigatório."

    if not senha:
        return False, "A senha é obrigatória."

    cliente = buscar_cliente_por_cpf(cpf)

    if cliente is None:
        return False, "CPF não encontrado."

    try:
        ph.verify(cliente[5], senha)

    except VerifyMismatchError:
        return False, "Senha incorreta."

    except VerificationError:
        return False, "Não foi possível verificar a senha."

    cliente_logado = cliente[0]

    return True, "Login realizado com sucesso."
