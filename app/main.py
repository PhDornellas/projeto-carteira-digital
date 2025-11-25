from fastapi import FastAPI
from app.carteira import router as carteira_router
from app.movimentos import router as movimento_router
from app.convesao import router as convesao_router
from app.transferencia import router as transferencia_router
from app.saldos import router as saldos_router

app = FastAPI()

app.include_router(carteira_router)
app.include_router(movimento_router)
app.include_router(convesao_router)
app.include_router(transferencia_router)
app.include_router(saldos_router)
