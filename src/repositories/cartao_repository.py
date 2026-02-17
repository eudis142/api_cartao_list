from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class CartaoRepository:
    def __init__(self, db_client):
        """
        Inicializa o repositório com um cliente Database (databases library)

        Args:
            db_client: Uma instância de databases.Database
        """
        self.db = db_client

    async def find_by_pessoa_id(self, cpf_cnpj: str) -> List[Dict]:
        """Busca todos os cartões de uma pessoa"""
        try:
            query = "SELECT id, pessoa_id, numero_cartao, status, tipo_cartao, ativo, data_emissao, data_validade, created_at, updated_at FROM public.cartoes WHERE pessoa_id = :pessoa_id"
            cartoes = await self.db.fetch_all(query=query, values={"pessoa_id": cpf_cnpj})
            result = [dict(row) for row in cartoes]
            logger.info(f"Encontrados {len(result)} cartões para pessoa {cartoes}")
            return result
        except Exception as e:
            logger.error(f"Erro ao buscar cartões: {str(e)}")
            raise

    async def find_by_id(self, id: str) -> List[Dict]:
        """Busca todos os cartões de uma pessoa"""
        try:
            query = "SELECT id, pessoa_id, numero_cartao, status, tipo_cartao, ativo, data_emissao, data_validade, created_at, updated_at FROM public.cartoes WHERE id = :id"
            cartoes = await self.db.fetch_all(query=query, values={"id": id})
            result = [dict(row) for row in cartoes]
            logger.info(f"Encontrados {len(result)} cartões para pessoa {id}")
            return result
        except Exception as e:
            logger.error(f"Erro ao buscar cartões: {str(e)}")
            raise

    async def save(self, cartao_data: Dict):
        """Salva um novo cartão"""
        try:
            columns = ", ".join(cartao_data.keys())
            placeholders = ", ".join([f":{key}" for key in cartao_data.keys()])
            query = f"INSERT INTO cartoes ({columns}) VALUES ({placeholders}) RETURNING id"
            result = await self.db.execute(query=query, values=cartao_data)
            logger.info(f"Cartão salvo com ID: {result}")
            return result
        except Exception as e:
            logger.error(f"Erro ao salvar cartão: {str(e)}")
            raise

    async def find_by_numero(self, numero_cartao: str) -> Dict:
        """Busca cartão pelo número"""
        try:
            query = "SELECT * FROM cartoes WHERE numero_cartao = :numero_cartao"
            cartao = await self.db.fetch_one(query=query, values={"numero_cartao": numero_cartao})
            return dict(cartao) if cartao else None
        except Exception as e:
            logger.error(f"Erro ao buscar cartão: {str(e)}")
            raise
