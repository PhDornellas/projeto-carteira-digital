from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.queries.saldos_queries import (
    GET_CARTEIRA_ID,
    GET_SALDOS
)

router = APIRouter()

@router.get("/carteiras/{endereco}/saldos")
def consultar_saldos(endereco: str):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(GET_CARTEIRA_ID, (endereco,))
        carteira = cur.fetchone()

        if not carteira:
            raise HTTPException(404, "Carteira não encontrada")

        carteira_id = carteira[0]

        cur.execute(GET_SALDOS, (carteira_id,))
        saldos = cur.fetchall()

        lista_saldos = [
            {"moeda": row[0], "saldo": float(row[1])}
            for row in saldos
        ]

        return {
            "endereco_publico": endereco,
            "saldos": lista_saldos
        }

    except Exception as e:
        raise HTTPException(500, str(e))

    finally:
        cur.close()
        conn.close()
