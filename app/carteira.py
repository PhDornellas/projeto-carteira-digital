from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.utils import gerar_chave_privada, gerar_chave_publica, hash_chave_privada
from app.queries.carteira_queries import CRIAR_CARTEIRA, OBTER_CARTEIRA

router = APIRouter()

@router.post("/carteiras")
def criar_carteira():
    chave_privada = gerar_chave_privada()
    hash_priv = hash_chave_privada(chave_privada)
    chave_publica = gerar_chave_publica()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(CRIAR_CARTEIRA, (chave_publica, hash_priv))
        result = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(500, detail=str(e))
    finally:
        cur.close()
        conn.close()

    return {
        "endereco_publico": chave_publica,
        "chave_privada": chave_privada,
        "criado_em": result[2]
    }

@router.get("/carteiras/{endereco}")
def obter_carteira(endereco: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(OBTER_CARTEIRA, (endereco,))
    carteira = cur.fetchone()

    cur.close()
    conn.close()

    if not carteira:
        raise HTTPException(404, "Carteira não encontrada")

    return {
        "endereco_publico": carteira[0],
        "criado_em": carteira[1],
        "status": carteira[2]
    }
