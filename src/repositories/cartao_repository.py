from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class CartaoRepository:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client.cadastro_unificado
        self.collection = self.db.cartoes

    async def find_by_pessoa_id(self, pessoa_id: str) -> List[Dict]:
        """Busca todos os cartões de uma pessoa"""
        try:
            cursor = self.collection.find({"pessoa_id": pessoa_id})
            cartoes = await cursor.to_list(length=None)
            logger.info(f"Encontrados {len(cartoes)} cartões para pessoa {pessoa_id}")
            return cartoes
        except Exception as e:
            logger.error(f"Erro ao buscar cartões: {str(e)}")
            raise

    # Métodos existentes (simulados para compatibilidade)
    async def save(self, cartao_data: Dict):
        """Salva um novo cartão"""
        result = await self.collection.insert_one(cartao_data)
        return result.inserted_id

    async def find_by_numero(self, numero_cartao: str) -> Dict:
        """Busca cartão pelo número"""
        return await self.collection.find_one({"numero_cartao": numero_cartao})