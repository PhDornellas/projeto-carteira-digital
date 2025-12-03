from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.utils import hash_chave_privada
from app.queries.movimentos_queries import (
    GET_CARTEIRA_ID,
    GET_SALDO,
    CRIAR_SALDO,
    ATUALIZAR_SALDO,
    GET_MOEDA,
    REGISTRAR_MOVIMENTO
)
import os
from decimal import Decimal

router = APIRouter()


@router.post("/carteiras/{endereco}/depositos")
def realizar_deposito(endereco: str, moeda: str, valor: float):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(GET_CARTEIRA_ID, (endereco,))
        carteira = cur.fetchone()
        if not carteira:
            raise HTTPException(404, "Carteira não encontrada")
        carteira_id = carteira[0]

        cur.execute(GET_MOEDA, (moeda,))
        moeda_row = cur.fetchone()
        if not moeda_row:
            raise HTTPException(404, "Moeda inválida")
        moeda_id = moeda_row[0]

        valor_decimal = Decimal(str(valor))

        cur.execute(GET_SALDO, (carteira_id, moeda_id))
        saldo_row = cur.fetchone()

        if saldo_row:
            saldo_id = saldo_row[0]
            saldo_atual = saldo_row[1]
            novo_saldo = Decimal(saldo_atual) + valor_decimal
            cur.execute(ATUALIZAR_SALDO, (novo_saldo, saldo_id))
        else:
            cur.execute(CRIAR_SALDO, (carteira_id, moeda_id, valor_decimal))

        cur.execute(REGISTRAR_MOVIMENTO, (carteira_id, moeda_id, "DEPOSITO", valor_decimal, 0))
        conn.commit()

        return {"mensagem": "Depósito realizado com sucesso", "valor": valor}

    except Exception as e:
        conn.rollback()
        raise HTTPException(500, str(e))

    finally:
        cur.close()
        conn.close()


@router.post("/carteiras/{endereco}/saques")
def realizar_saque(endereco: str, moeda: str, valor: float, chave_privada: str):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(GET_CARTEIRA_ID, (endereco,))
        carteira = cur.fetchone()
        if not carteira:
            raise HTTPException(404, "Carteira não encontrada")

        carteira_id = carteira[0]
        hash_no_banco = carteira[1]





        if hash_chave_privada(chave_privada) != hash_no_banco:
            raise HTTPException(401, "Chave privada inválida")

        cur.execute(GET_MOEDA, (moeda,))
        moeda_row = cur.fetchone()
        if not moeda_row:
            raise HTTPException(404, "Moeda inválida")
        moeda_id = moeda_row[0]

        cur.execute(GET_SALDO, (carteira_id, moeda_id))
        saldo_row = cur.fetchone()
        if not saldo_row:
            raise HTTPException(400, "Saldo insuficiente")

        saldo_id = saldo_row[0]
        saldo_atual = Decimal(saldo_row[1])

        valor_decimal = Decimal(str(valor))
        taxa_percentual = Decimal(str(os.getenv("TAXA_SAQUE_PERCENTUAL")))
        taxa = valor_decimal * taxa_percentual
        total = valor_decimal + taxa

        if saldo_atual < total:
            raise HTTPException(400, "Saldo insuficiente para saque + taxa")

        novo_saldo = saldo_atual - total

        cur.execute(ATUALIZAR_SALDO, (novo_saldo, saldo_id))
        cur.execute(REGISTRAR_MOVIMENTO, (carteira_id, moeda_id, "SAQUE", valor_decimal, taxa))

        conn.commit()

        return {
            "mensagem": "Saque realizado com sucesso",
            "valor": float(valor_decimal),
            "taxa": float(taxa)
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(500, str(e))

    finally:
        cur.close()
        conn.close()
