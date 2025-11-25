from fastapi import FastAPI
from app.carteira import router as carteira_router

app = FastAPI()

app.include_router(carteira_router)
