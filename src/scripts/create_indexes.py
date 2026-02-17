import asyncio
from src.config.database import get_db_client, close_db_client


async def create_indexes():
    """Cria índices no PostgreSQL para otimizar queries"""
    db_client = await get_db_client()

    try:
        # Criar índice no campo pessoa_id
        query = "CREATE INDEX IF NOT EXISTS idx_cartoes_pessoa_id ON cartoes(pessoa_id)"
        await db_client.execute(query=query)
        print("Índice idx_cartoes_pessoa_id criado com sucesso!")

        # Criar índice no campo numero_cartao
        query = "CREATE INDEX IF NOT EXISTS idx_cartoes_numero ON cartoes(numero_cartao)"
        await db_client.execute(query=query)
        print("Índice idx_cartoes_numero criado com sucesso!")

        print("Todos os índices foram criados!")

    except Exception as e:
        print(f"Erro ao criar índices: {str(e)}")
    finally:
        await close_db_client()

if __name__ == "__main__":
    asyncio.run(create_indexes())