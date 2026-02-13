from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from src.routers.cartao_router import router as cartao_router
from src.config.database import close_db_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await close_db_client()


app = FastAPI(
    title="API Cartão List",
    description="API para listar cartões de pessoas",
    version="1.0.0",
    lifespan=lifespan
)

# Registrar routers
app.include_router(cartao_router)

@app.get("/")
def read_root():
    return {"message": "Funcionando!"}

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
