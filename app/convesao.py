from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.utils import hash_chave_privada
from app.queries.conversao_queries import (
    GET_CARTEIRA_ID,
    GET_MOEDA,
    GET_SALDO,
    CRIAR_SALDO,
    ATUALIZAR_SALDO,
    REGISTRAR_CONVERSAO
)
import requests
import os
from decimal import Decimal

router = APIRouter()

@router.post("/carteiras/{endereco}/conversoes")
def converter_moedas(endereco: str, moeda_origem: str, moeda_destino: str, valor: float, chave_privada: str):
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

        cur.execute(GET_MOEDA, (moeda_origem,))
        moeda_origem_row = cur.fetchone()
        if not moeda_origem_row:
            raise HTTPException(404, "Moeda de origem inválida")
        moeda_origem_id = moeda_origem_row[0]

        cur.execute(GET_MOEDA, (moeda_destino,))
        moeda_destino_row = cur.fetchone()
        if not moeda_destino_row:
            raise HTTPException(404, "Moeda de destino inválida")
        moeda_destino_id = moeda_destino_row[0]

        cur.execute(GET_SALDO, (carteira_id, moeda_origem_id))
        saldo_origem_row = cur.fetchone()
        if not saldo_origem_row:
            raise HTTPException(400, "Saldo insuficiente")

        saldo_origem_id = saldo_origem_row[0]
        saldo_origem = Decimal(saldo_origem_row[1])

        valor_decimal = Decimal(str(valor))

        url = f"https://api.coinbase.com/v2/prices/{moeda_origem}-{moeda_destino}/spot"
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(500, "Erro ao consultar cotação")

        cotacao = Decimal(response.json()["data"]["amount"])

        taxa_percentual = Decimal(str(os.getenv("TAXA_CONVERSAO_PERCENTUAL")))
        taxa = valor_decimal * taxa_percentual
        valor_convertido = (valor_decimal - taxa) * cotacao  # taxa desconta da moeda de origem

        if saldo_origem < valor_decimal:
            raise HTTPException(400, "Saldo insuficiente")

        novo_saldo_origem = saldo_origem - valor_decimal

        cur.execute(GET_SALDO, (carteira_id, moeda_destino_id))
        saldo_destino_row = cur.fetchone()

        if saldo_destino_row:
            saldo_destino_id = saldo_destino_row[0]
            saldo_destino_atual = Decimal(saldo_destino_row[1])
            novo_saldo_destino = saldo_destino_atual + valor_convertido
            cur.execute(ATUALIZAR_SALDO, (novo_saldo_destino, saldo_destino_id))
        else:
            cur.execute(CRIAR_SALDO, (carteira_id, moeda_destino_id, valor_convertido))

        # atualizar saldo da moeda de origem
        cur.execute(ATUALIZAR_SALDO, (novo_saldo_origem, saldo_origem_id))

        # registrar no histórico
        cur.execute(REGISTRAR_CONVERSAO, (
            carteira_id,
            moeda_origem_id,
            moeda_destino_id,
            valor_decimal,
            valor_convertido,
            cotacao,
            taxa
        ))

        conn.commit()

        return {
            "mensagem": "Conversão realizada com sucesso",
            "valor_origem": float(valor_decimal),
            "valor_convertido": float(valor_convertido),
            "cotacao": float(cotacao),
            "taxa": float(taxa)
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(500, str(e))

    finally:
        cur.close()
        conn.close()
