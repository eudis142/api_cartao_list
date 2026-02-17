import httpx
from typing import Dict, Optional
import logging
from src.repositories.cartao_repository import CartaoRepository
logger = logging.getLogger(__name__)


class PessoaClient:
    def __init__(self, base_url: str, cartao_repository: CartaoRepository):
        self.cartao_repository = cartao_repository
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_pessoa_by_cpf(self, cpf_cnpj: str) -> Optional[Dict]:
        """Consulta pessoa no Time 02"""
        try:

            response = await self.cartao_repository.find_by_pessoa_id(cpf_cnpj)

            if response.__len__() != None:
                return response
            elif response == 404:
                return None
            else:
                logger.error(f"Erro ao consultar pessoa: {response}")
                return None

        except httpx.RequestError as e:
            logger.error(f"Erro de conexão com Time 02: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return None

    async def close(self):
        await self.client.aclose()