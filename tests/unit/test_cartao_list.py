#import pytest
from unittest.mock import AsyncMock, MagicMock

import pytest_asyncio
import pytest
from fastapi import HTTPException
from src.services.cartao_service import CartaoService
from src.schemas.cartao_schemas import CartaoResponse

@pytest.mark.asyncio
async def test_list_cartoes_success():
    """Testa listagem com sucesso (2 cartões)"""
    mock_repo = MagicMock()
    mock_repo.find_by_pessoa_id = AsyncMock(return_value=[
        {
            'id': 'cartao-1',
            'numero_cartao': '1000123456789012',
            'pessoa_id': '12345678901',
            'tipo_cartao': 'BILHETE_UNICO',
            'status': 'ATIVO',
            'data_emissao': '2025-01-10T10:00:00',
            'data_validade': None,
            'ativo': True,
            'created_at': '2025-01-10T10:00:00',
            'updated_at': '2025-01-10T10:00:00'
        },
        {
            'id': 'cartao-2',
            'numero_cartao': '2000987654321098',
            'pessoa_id': 'pessoa-456',
            'tipo_cartao': 'ESCOLAR',
            'status': 'ATIVO',
            'data_emissao': '2025-01-11T14:00:00',
            'data_validade': None,
            'ativo': True,
            'created_at': '2025-01-11T14:00:00',
            'updated_at': '2025-01-11T14:00:00'
        }
    ])

    mock_pessoa_client = MagicMock()
    mock_pessoa_client.get_pessoa_by_cpf = AsyncMock(return_value=[{
            'id': 'cartao-2',
            'numero_cartao': '2000987654321098',
            'pessoa_id': '12345678901',
            'tipo_cartao': 'ESCOLAR',
            'status': 'ATIVO',
            'data_emissao': '2025-01-11T14:00:00',
            'data_validade': None,
            'ativo': True,
            'created_at': '2025-01-11T14:00:00',
            'updated_at': '2025-01-11T14:00:00'
    }])

    service = CartaoService(mock_repo, mock_pessoa_client)
    result = await service.list_cartoes_by_pessoa("12345678901")

    assert len(result) == 1
    assert isinstance(result[0], CartaoResponse)
    assert result[0].numero_cartao == '2000987654321098'
    assert result[0].tipo_cartao.value == 'ESCOLAR'

@pytest.mark.asyncio
async def test_list_cartoes_pessoa_not_found():
    """Testa erro 404 quando pessoa não existe"""
    mock_pessoa_client = MagicMock()
    mock_pessoa_client.get_pessoa_by_cpf = AsyncMock(return_value=None)

    service = CartaoService(MagicMock(), mock_pessoa_client)

    with pytest.raises(HTTPException) as exc:
        await service.list_cartoes_by_pessoa("99999999999")

    assert exc.value.status_code == 404
    assert "Não existe cadastro" in exc.value.detail


@pytest.mark.asyncio
async def test_list_cartoes_pessoa_sem_id():
    """Testa erro quando resposta do Time 02 não tem ID"""
    mock_pessoa_client = MagicMock()
    mock_pessoa_client.get_pessoa_by_cpf = AsyncMock(return_value={
        'nome_razao_social': 'João Silva',
        'cpf_cnpj': '12345678901'
        # Sem campo 'id'
    })

    service = CartaoService(MagicMock(), mock_pessoa_client)

    with pytest.raises(HTTPException) as exc:
        await service.list_cartoes_by_pessoa("12345678901")

    assert exc.value.status_code == 500
    assert "ID da pessoa não encontrado" in exc.value.detail