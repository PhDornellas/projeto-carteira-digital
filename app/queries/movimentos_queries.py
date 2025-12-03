GET_CARTEIRA_ID = """
SELECT id, hash_chave_privada FROM carteira
WHERE endereco_publico = %s;
"""

GET_SALDO = """
SELECT id, saldo FROM saldo_carteira
WHERE carteira_id = %s AND moeda_id = %s;
"""

CRIAR_SALDO = """
INSERT INTO saldo_carteira (carteira_id, moeda_id, saldo)
VALUES (%s, %s, %s)
RETURNING id, saldo;
"""

ATUALIZAR_SALDO = """
UPDATE saldo_carteira
SET saldo = %s
WHERE id = %s;
"""

GET_MOEDA = """
SELECT id FROM moeda WHERE codigo = %s;
"""

REGISTRAR_MOVIMENTO = """
INSERT INTO deposito_saque (carteira_id, moeda_id, tipo, valor, taxa)
VALUES (%s, %s, %s, %s, %s)
RETURNING id;
"""
