"""
Seed da tabela Apartamentos.

Regras aplicadas:
  - 5 andares x 6 apartamentos (numeração = andar * 100 + número do quarto)
  - 1 apartamento acessível por andar
  - Vista mar em todos os quartos, exceto no 1º andar
  - 3 quartos com frigobar por andar
  - Os maiores quartos ficam nas pontas (quartos 1 e 6)
  - Apenas 2 quartos com mesa de sinuca no hotel todo
  - Pelo menos 2 quartos pet friendly por andar
  - Tipos permitidos: Standard, Duplo, Luxo, Super Luxo, Presidencial

Uso:
    python seed_apartamentos.py                # usa hotel.db
    python seed_apartamentos.py caminho/db.db  # banco customizado
"""

import sqlite3
import sys

DB_PATH = "databank/sistema-hotelaria.db"

ANDARES = 5
QUARTOS_POR_ANDAR = 6

# Perfis por tipo (do menor para o maior). Preço é por pessoa, sem vista mar.
PERFIS = {
    "Standard":     {"preco_base": 100.0, "limite_pessoa": 2, "qt_camas": 1},
    "Duplo":        {"preco_base": 130.0, "limite_pessoa": 4, "qt_camas": 2},
    "Luxo":         {"preco_base": 180.0, "limite_pessoa": 5, "qt_camas": 3},
    "Super Luxo":   {"preco_base": 230.0, "limite_pessoa": 6, "qt_camas": 3},
    "Presidencial": {"preco_base": 350.0, "limite_pessoa": 8, "qt_camas": 4},
}
ORDEM_TIPOS = list(PERFIS)  # usado na validação (menor -> maior)

ADICIONAL_VISTA_MAR = 30.0

# Posição dos quartos (1 a 6) que recebem cada característica, em cada andar
PONTAS = {1, 6}               # maiores quartos
ACESSIVEL = {2}               # 1 por andar (perto do elevador)
FRIGOBAR = {1, 3, 6}          # 3 por andar
PET_FRIENDLY = {4, 5}         # 2 por andar (mínimo exigido)

# Apenas 2 quartos no hotel todo (numeração completa): pontas do último andar
MESA_SINUCA = {501, 506}

# Tipo dos quartos do meio (posições 2 a 5)
TIPO_MEIO = {2: "Standard", 3: "Duplo", 4: "Duplo", 5: "Standard"}

# Tipo dos quartos das pontas (posições 1 e 6), por andar
TIPO_PONTA_POR_ANDAR = {
    1: "Luxo",
    2: "Luxo",
    3: "Super Luxo",
    4: "Super Luxo",
    5: "Presidencial",
}

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS Apartamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    numeracao INTEGER NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'vago' CHECK (status IN ('vago', 'ocupado', 'indisponivel')),
    preco_pessoa REAL CHECK (preco_pessoa >= 0),
    limite_pessoa INTEGER CHECK (limite_pessoa > 0),
    pet_friendly INTEGER NOT NULL DEFAULT 0 CHECK (pet_friendly IN (0, 1)),
    qt_camas INTEGER NOT NULL DEFAULT 1 CHECK (qt_camas > 0),
    vista_mar INTEGER NOT NULL DEFAULT 0 CHECK (vista_mar IN (0, 1)),
    frigobar INTEGER NOT NULL DEFAULT 0 CHECK (frigobar IN (0, 1)),
    mesa_sinuca INTEGER NOT NULL DEFAULT 0 CHECK (mesa_sinuca IN (0, 1)),
    acessivel INTEGER NOT NULL DEFAULT 0 CHECK (acessivel IN (0, 1))
)
"""

INSERT = """
INSERT OR IGNORE INTO Apartamentos
    (tipo, numeracao, status, preco_pessoa, limite_pessoa, pet_friendly,
     qt_camas, vista_mar, frigobar, mesa_sinuca, acessivel)
VALUES
    (:tipo, :numeracao, :status, :preco_pessoa, :limite_pessoa, :pet_friendly,
     :qt_camas, :vista_mar, :frigobar, :mesa_sinuca, :acessivel)
"""


def escolher_tipo(andar, quarto):
    if quarto in PONTAS:
        return TIPO_PONTA_POR_ANDAR[andar]
    return TIPO_MEIO[quarto]


def gerar_apartamentos():
    apartamentos = []
    for andar in range(1, ANDARES + 1):
        for quarto in range(1, QUARTOS_POR_ANDAR + 1):
            numeracao = andar * 100 + quarto
            tipo = escolher_tipo(andar, quarto)
            perfil = PERFIS[tipo]
            vista_mar = andar != 1

            preco = perfil["preco_base"] + (ADICIONAL_VISTA_MAR if vista_mar else 0)

            apartamentos.append(
                {
                    "tipo": tipo,
                    "numeracao": numeracao,
                    "status": "vago",
                    "preco_pessoa": preco,
                    "limite_pessoa": perfil["limite_pessoa"],
                    "pet_friendly": int(quarto in PET_FRIENDLY),
                    "qt_camas": perfil["qt_camas"],
                    "vista_mar": int(vista_mar),
                    "frigobar": int(quarto in FRIGOBAR),
                    "mesa_sinuca": int(numeracao in MESA_SINUCA),
                    "acessivel": int(quarto in ACESSIVEL),
                }
            )
    return apartamentos


def validar_regras(apartamentos):
    """Garante que os dados gerados respeitam todas as regras de negócio."""
    assert len(apartamentos) == ANDARES * QUARTOS_POR_ANDAR

    for a in apartamentos:
        assert a["tipo"] in PERFIS, f"Tipo inválido: {a['tipo']}"

    for andar in range(1, ANDARES + 1):
        do_andar = [a for a in apartamentos if a["numeracao"] // 100 == andar]
        assert len(do_andar) == QUARTOS_POR_ANDAR
        assert sum(a["acessivel"] for a in do_andar) == 1, f"Andar {andar}: acessível"
        assert sum(a["frigobar"] for a in do_andar) == 3, f"Andar {andar}: frigobar"
        assert sum(a["pet_friendly"] for a in do_andar) >= 2, f"Andar {andar}: pet"

        pontas = [a for a in do_andar if a["numeracao"] % 100 in PONTAS]
        meio = [a for a in do_andar if a["numeracao"] % 100 not in PONTAS]

        # As pontas são os maiores quartos do andar (tipo, capacidade e camas)
        for p in pontas:
            for m in meio:
                assert ORDEM_TIPOS.index(p["tipo"]) > ORDEM_TIPOS.index(m["tipo"]), \
                    f"Andar {andar}: pontas devem ter tipo maior que o meio"
                assert p["limite_pessoa"] > m["limite_pessoa"], f"Andar {andar}: limite"
                assert p["qt_camas"] > m["qt_camas"], f"Andar {andar}: camas"

        for a in do_andar:
            assert a["vista_mar"] == (1 if andar != 1 else 0), f"Andar {andar}: vista"

    assert sum(a["mesa_sinuca"] for a in apartamentos) == 2, "Mesa de sinuca"


def main():
    apartamentos = gerar_apartamentos()
    validar_regras(apartamentos)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(CREATE_TABLE)
        cursor = conn.executemany(INSERT, apartamentos)
        inseridos = cursor.rowcount

    print(f"Seed concluído em '{DB_PATH}': {inseridos} apartamento(s) inserido(s) "
          f"({len(apartamentos) - inseridos} já existiam).")


if __name__ == "__main__":
    main()