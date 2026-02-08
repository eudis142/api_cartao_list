# main.py - VERSÃO CORRETA E TESTADA
from fastapi import FastAPI
from src.routers.cartao_router import router as cartao_router

app = FastAPI()

app.include_router(cartao_router)
@app.get("/")
async def root():
    return {"message": "API de Cartões - Time 04"}

@app.get("/cartoes")
async def listar_cartoes():
    return {
        "cartoes": [
            {"id": 1, "numero": "1234", "saldo": 100.50},
            {"id": 2, "numero": "5678", "saldo": 200.75},
        ]
    }