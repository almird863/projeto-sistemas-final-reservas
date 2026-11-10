# Projeto Integrador Hotel — Próximos passos

Nov 9, 2026 · @Wallace Duarte

## Onde o projeto está

Dá para avançar sem esperar o Derek: a `main` já tem os models completos e a `view` tem as telas de login e cadastro.

| Branch | Responsável | Estado |
| --- | --- | --- |
| `main` | Almir | Models com CRUD completo. O banco versionado tem o esquema novo, mas as três tabelas estão vazias, sem nenhum apartamento cadastrado. O CPF virou `TEXT UNIQUE`, o que resolve o problema do zero à esquerda. |
| `view` | Wallace | Login e cadastro prontos. Ainda não tem os models novos do Almir. |
| `controller/cliente` | Derek | Controller com as validações (foi o usado no teste). Ainda não foi para a `main`. |

## Passos que dá para dar agora

O menu principal é o melhor começo: é só tela e não depende de ninguém.

1. **Menu principal.** Barra lateral e os quatro cartões do layout. Os botões ficam prontos para ligar às próximas telas.
2. **Script de apartamentos de teste.** Cadastra Standard, Luxo e Suíte com o `inserir_db_apto` do Almir. Sem isso, a tela de Reservas não tem o que mostrar.
3. **Tela de Reservas.** Filtros de busca e cartões de apartamentos, depois que houver apartamentos no banco.
4. **Login funcionando.** Fica por último porque depende de uma decisão do grupo (próxima seção).

## Para combinar com o grupo

Duas coisas precisam de acordo antes de ligar o login ao banco.

- **Erro silencioso no cadastro.** O controller do Derek ignora o retorno de `inserir_db_cliente`. Com o model novo do Almir, um CPF duplicado devolve `False`, mas o controller responde "Sucesso ao cadastrar". A correção é uma linha no controller. Vale sugerir também que o model sempre devolva `(sucesso, mensagem)`, porque hoje devolve uma tupla em um caso e só `False` no outro.
- **Login com qual campo?** A tabela `Clientes` não tem usuário. O model tem `buscar_cliente(nome)`, mas o nome pode repetir e a busca devolve só o primeiro. A sugestão é entrar com **CPF e senha**, porque o CPF é único.

## Na branch view

Traga os models novos com `git merge origin/main` na `view`. Pode haver conflito entre `views/views.py` (da `main`) e `views/view_reserva.py` (da `view`). Os dois arquivos estão vazios, então mantenha o `view_reserva.py`.
