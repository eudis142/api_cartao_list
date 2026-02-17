"""
Teste de validação do CartaoRepository corrigido
Verifica se o método find_by_pessoa_id funciona corretamente
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock
from src.repositories.cartao_repository import CartaoRepository


async def test_find_by_pessoa_id():
    """Testa se o repositório retorna corretamente a lista de cartões"""

    # Criar um mock do cliente database
    mock_db = MagicMock()

    # Simular dados que a query retornaria
    mock_rows = [
        MagicMock(
            id='123e4567-e89b-12d3-a456-426614174000',
            pessoa_id='pessoa-001',
            numero_cartao='1000123456789012',
            status='ATIVO',
            tipo_cartao='BILHETE_UNICO',
            ativo=True,
            data_emissao='2025-01-10T10:00:00',
            data_validade=None,
            created_at='2025-01-10T10:00:00',
            updated_at='2025-01-10T10:00:00'
        ),
        MagicMock(
            id='223e4567-e89b-12d3-a456-426614174000',
            pessoa_id='pessoa-001',
            numero_cartao='2000987654321098',
            status='ATIVO',
            tipo_cartao='ESCOLAR',
            ativo=True,
            data_emissao='2025-01-11T14:00:00',
            data_validade=None,
            created_at='2025-01-11T14:00:00',
            updated_at='2025-01-11T14:00:00'
        )
    ]

    # Configurar mock para retornar dados
    mock_db.fetch_all = AsyncMock(return_value=mock_rows)

    # Criar repositório
    repo = CartaoRepository(mock_db)

    # Executar busca
    resultado = await repo.find_by_pessoa_id("pessoa-001")

    # Validações
    print("=" * 60)
    print("TESTE: find_by_pessoa_id")
    print("=" * 60)

    # 1. Verificar que fetch_all foi chamado com parâmetros corretos
    assert mock_db.fetch_all.called, "fetch_all não foi chamado"
    call_args = mock_db.fetch_all.call_args
    assert "WHERE pessoa_id" in call_args.kwargs['query'], "Query não filtra por pessoa_id"
    assert call_args.kwargs['values']['pessoa_id'] == "pessoa-001", "Parâmetro pessoa_id incorreto"
    print("✓ fetch_all foi chamado com query correta")

    # 2. Verificar que retornou lista
    assert isinstance(resultado, list), "Resultado não é uma lista"
    print("✓ Resultado é uma lista")

    # 3. Verificar que retornou 2 cartões
    assert len(resultado) == 2, f"Esperava 2 cartões, obteve {len(resultado)}"
    print(f"✓ Retornou {len(resultado)} cartões")

    # 4. Verificar que são dicts
    for item in resultado:
        assert isinstance(item, dict), f"Item não é dict: {type(item)}"
    print("✓ Todos os items são dicts")

    # 5. Verificar estrutura do primeiro cartão
    cartao1 = resultado[0]
    assert cartao1['id'] == '123e4567-e89b-12d3-a456-426614174000'
    assert cartao1['numero_cartao'] == '1000123456789012'
    assert cartao1['tipo_cartao'] == 'BILHETE_UNICO'
    assert cartao1['status'] == 'ATIVO'
    print("✓ Primeiro cartão tem dados corretos")

    # 6. Verificar estrutura do segundo cartão
    cartao2 = resultado[1]
    assert cartao2['id'] == '223e4567-e89b-12d3-a456-426614174000'
    assert cartao2['numero_cartao'] == '2000987654321098'
    assert cartao2['tipo_cartao'] == 'ESCOLAR'
    print("✓ Segundo cartão tem dados corretos")

    print("\n✓ TODOS OS TESTES PASSARAM!")
    print("=" * 60)


async def test_find_by_pessoa_id_empty():
    """Testa se o repositório retorna lista vazia quando não há cartões"""

    mock_db = MagicMock()
    mock_db.fetch_all = AsyncMock(return_value=[])

    repo = CartaoRepository(mock_db)
    resultado = await repo.find_by_pessoa_id("pessoa-inexistente")

    print("\n" + "=" * 60)
    print("TESTE: find_by_pessoa_id (sem cartões)")
    print("=" * 60)

    assert isinstance(resultado, list), "Resultado não é uma lista"
    assert len(resultado) == 0, f"Esperava lista vazia, obteve {len(resultado)} items"
    print("✓ Retornou lista vazia para pessoa sem cartões")
    print("=" * 60)


async def main():
    """Executa todos os testes"""
    try:
        await test_find_by_pessoa_id()
        await test_find_by_pessoa_id_empty()
        print("\n✅ VALIDAÇÃO COMPLETA: CartaoRepository está funcionando corretamente!")
        return 0
    except AssertionError as e:
        print(f"\n❌ ERRO DE VALIDAÇÃO: {str(e)}")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {str(e)}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)

