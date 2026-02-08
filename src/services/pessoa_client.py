import httpx
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PessoaClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_pessoa_by_cpf(self, cpf_cnpj: str) -> Optional[Dict]:
        """Consulta pessoa no Time 02"""
        try:
            url = f"{self.base_url}/pessoas/{cpf_cnpj}"
            logger.info(f"Consultando pessoa em: {url}")

            response = await self.client.get(url)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                logger.error(f"Erro ao consultar pessoa: {response.status_code}")
                return None

        except httpx.RequestError as e:
            logger.error(f"Erro de conexão com Time 02: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return None

    async def close(self):
        await self.client.aclose()