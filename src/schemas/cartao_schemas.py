from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TipoCartaoEnum(str, Enum):
    BILHETE_UNICO = "BILHETE_UNICO"
    ESCOLAR = "ESCOLAR"
    IDOSO = "IDOSO"
    DEFICIENTE = "DEFICIENTE"
    CORPORATIVO = "CORPORATIVO"

class StatusCartaoEnum(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    BLOQUEADO = "BLOQUEADO"
    CANCELADO = "CANCELADO"

class CartaoResponse(BaseModel):
    id: str = Field(..., alias="_id")
    numero_cartao: str
    pessoa_id: str
    tipo_cartao: TipoCartaoEnum
    status: StatusCartaoEnum
    data_emissao: datetime
    data_validade: Optional[datetime] = None
    ativo: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",
                "numero_cartao": "1000123456789012",
                "pessoa_id": "123e4567-e89b-12d3-a456-426614174001",
                "tipo_cartao": "BILHETE_UNICO",
                "status": "ATIVO",
                "data_emissao": "2025-01-10T10:00:00",
                "data_validade": None,
                "ativo": True,
                "created_at": "2025-01-10T10:00:00",
                "updated_at": "2025-01-10T10:00:00"
            }
        }