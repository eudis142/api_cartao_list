from motor.motor_asyncio import AsyncIOMotorClient
from src.config.settings import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_db_client() -> AsyncIOMotorClient:
    if db.client is None:
        db.client = AsyncIOMotorClient(settings.POSTGRESSQL_URL)
    return db.client

async def close_db_client():
    if db.client:
        db.client.close()