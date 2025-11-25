GET_CARTEIRA_ID = """
SELECT id FROM carteira
WHERE endereco_publico = %s;
"""

GET_SALDOS = """
SELECT m.codigo, s.saldo
FROM saldo_carteira s
JOIN moeda m ON m.id = s.moeda_id
WHERE s.carteira_id = %s;
"""
