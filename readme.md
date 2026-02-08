# API de Cartões - Time 04

API para gerenciamento de cartões, parte do sistema de cadastro unificado.

## Endpoints

### GET /pessoas/{cpf_cnpj}/cartoes

Lista todos os cartões vinculados a uma pessoa.

#### Parâmetros
- `cpf_cnpj` (path): CPF (11 dígitos) ou CNPJ (14 dígitos) da pessoa

#### Response 200 OK (com cartões):
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "numero_cartao": "1000123456789012",
    "pessoa_id": "123e4567-e89b-12d3-a456-426614174001",
    "tipo_cartao": "BILHETE_UNICO",
    "status": "ATIVO",
    "data_emissao": "2025-01-10T10:00:00",
    "data_validade": null,
    "ativo": true,
    "created_at": "2025-01-10T10:00:00",
    "updated_at": "2025-01-10T10:00:00"
  }
]