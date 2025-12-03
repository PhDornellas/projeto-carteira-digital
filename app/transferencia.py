from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.utils import hash_chave_privada
from app.queries.transferencia_queries import (
    GET_CARTEIRA_ID,
    GET_MOEDA,
    GET_SALDO,
    CRIAR_SALDO,
    ATUALIZAR_SALDO,
    REGISTRAR_TRANSFERENCIA
)
import os
from decimal import Decimal

router = APIRouter()

@router.post("/carteiras/{endereco_origem}/transferencias")
def transferir_valores(endereco_origem: str, endereco_destino: str, moeda: str, valor: float, chave_privada: str):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(GET_CARTEIRA_ID, (endereco_origem,))
        origem = cur.fetchone()

        if endereco_origem == endereco_destino:
            raise HTTPException(400, "Não é permitido transferir para a mesma carteira")

        if not origem:
            raise HTTPException(404, "Carteira de origem não encontrada")

        origem_id = origem[0]
        hash_origem = origem[1]

        if hash_chave_privada(chave_privada) != hash_origem:
            raise HTTPException(401, "Chave privada inválida para carteira de origem")

        cur.execute(GET_CARTEIRA_ID, (endereco_destino,))
        destino = cur.fetchone()
        if not destino:
            raise HTTPException(404, "Carteira de destino não encontrada")

        destino_id = destino[0]

        cur.execute(GET_MOEDA, (moeda,))
        moeda_row = cur.fetchone()
        if not moeda_row:
            raise HTTPException(404, "Moeda inválida")

        moeda_id = moeda_row[0]

        cur.execute(GET_SALDO, (origem_id, moeda_id))
        saldo_origem_row = cur.fetchone()
        if not saldo_origem_row:
            raise HTTPException(400, "Saldo insuficiente")

        saldo_origem_id = saldo_origem_row[0]
        saldo_origem = Decimal(saldo_origem_row[1])

        valor_decimal = Decimal(str(valor))

        taxa_percentual = Decimal(str(os.getenv("TAXA_TRANSFERENCIA_PERCENTUAL")))
        taxa = valor_decimal * taxa_percentual
        total = valor_decimal + taxa

        if saldo_origem < total:
            raise HTTPException(400, "Saldo insuficiente")

        novo_saldo_origem = saldo_origem - total

        cur.execute(GET_SALDO, (destino_id, moeda_id))
        saldo_destino_row = cur.fetchone()

        if saldo_destino_row:
            destino_saldo_id = saldo_destino_row[0]
            destino_saldo_atual = Decimal(saldo_destino_row[1])
            novo_saldo_destino = destino_saldo_atual + valor_decimal
            cur.execute(ATUALIZAR_SALDO, (novo_saldo_destino, destino_saldo_id))
        else:
            cur.execute(CRIAR_SALDO, (destino_id, moeda_id, valor_decimal))

        cur.execute(ATUALIZAR_SALDO, (novo_saldo_origem, saldo_origem_id))

        cur.execute(REGISTRAR_TRANSFERENCIA, (
            origem_id,
            destino_id,
            moeda_id,
            valor_decimal,
            taxa
        ))

        conn.commit()

        return {
            "mensagem": "Transferência realizada com sucesso",
            "valor": float(valor_decimal),
            "taxa": float(taxa)
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(500, str(e))

    finally:
        cur.close()
        conn.close()
