from src.schemas.cartao_schemas import CartaoResponse
from src.repositories.cartao_repository import CartaoRepository
from src.services.pessoa_client import PessoaClient
from fastapi import HTTPException, status
from typing import List
import logging

logger = logging.getLogger(__name__)


class CartaoService:
    def __init__(self, repository: CartaoRepository, pessoa_client: PessoaClient):
        self.repository = repository
        self.pessoa_client = pessoa_client

    async def list_cartoes_by_pessoa(self, cpf_cnpj: str) -> List[CartaoResponse]:
        """Lista todos os cartões de uma pessoa"""
        try:
            # 1. Validar pessoa existe
            pessoa = await self.pessoa_client.get_pessoa_by_cpf(cpf_cnpj)

            if not pessoa:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Não existe cadastro para o CPF/CNPJ {cpf_cnpj}"
                )
            # 3. Converter para CartaoResponse
            cartoes_response = []
            for doc in pessoa:
                cartao = CartaoResponse(
                    id=doc.get('id'),
                    numero_cartao=doc.get('numero_cartao'),
                    pessoa_id=doc.get('pessoa_id'),
                    tipo_cartao=doc.get('tipo_cartao'),
                    status=doc.get('status'),
                    data_emissao=doc.get('data_emissao'),
                    data_validade=doc.get('data_validade'),
                    ativo=doc.get('ativo'),
                    created_at=doc.get('created_at'),
                    updated_at=doc.get('updated_at')
                )
                cartoes_response.append(cartao)

            return cartoes_response

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erro ao listar cartões: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ID da pessoa não encontrado"
            )