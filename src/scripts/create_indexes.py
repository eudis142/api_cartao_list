import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from src.config.settings import settings


async def create_indexes():
    """Cria índices no MongoDB para otimizar queries"""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client.cadastro_unificado
    collection = db.cartoes

    # Criar índice no campo pessoa_id
    await collection.create_index("pessoa_id", name="idx_pessoa_id")
    print("Índice idx_pessoa_id criado com sucesso!")

    # Verificar índices existentes
    indexes = await collection.index_information()
    print(f"Índices existentes: {list(indexes.keys())}")

    client.close()


if __name__ == "__main__":
    asyncio.run(create_indexes())