from controls.control_cliente import cadastra_cliente

get

def cadastra():
    if cadastra_cliente("a", 1, 1, 1, 1):
        alert(deu certo)
    else:
        alert(deu ruim)