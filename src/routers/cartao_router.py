from fastapi import APIRouter, Path, status, HTTPException
from src.schemas.cartao_schemas import CartaoResponse
from src.services.cartao_service import CartaoService
from src.repositories.cartao_repository import CartaoRepository
from src.services.pessoa_client import PessoaClient
from src.config.database import get_db_client
from src.config.settings import settings
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/pessoas", tags=["Cartões"])


@router.get(
    "/{cpf_cnpj}/cartoes",
    response_model=List[CartaoResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar cartões de uma pessoa",
    description="Lista todos os cartões vinculados a uma pessoa pelo CPF/CNPJ"
)
async def list_cartoes(
        cpf_cnpj: str = Path(...,
                             min_length=11,
                             max_length=14,
                             description="CPF (11 dígitos) ou CNPJ (14 dígitos) da pessoa",
                             examples=["12345678901", "12345678901234"]
                             )
):
    """Lista cartões de uma pessoa"""
    try:
        logger.info(f"GET /pessoas/{cpf_cnpj}/cartoes")

        db_client = await get_db_client()
        repository = CartaoRepository(db_client)
        pessoa_client = PessoaClient(base_url=settings.PESSOA_API_URL, cartao_repository=repository)

        service = CartaoService(repository, pessoa_client)
        cartoes = await service.list_cartoes_by_pessoa(cpf_cnpj)

        return cartoes

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na rota: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno"
        )