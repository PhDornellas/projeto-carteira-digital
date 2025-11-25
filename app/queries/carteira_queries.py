CRIAR_CARTEIRA = """
INSERT INTO carteira (endereco_publico, hash_chave_privada, status)
VALUES (%s, %s, 'ATIVA')
RETURNING id, endereco_publico, criado_em;
"""

OBTER_CARTEIRA = """
SELECT endereco_publico, criado_em, status
FROM carteira
WHERE endereco_publico = %s;
"""
