from datetime import datetime
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field
from src.schemas.cartao_schemas import TipoCartaoEnum, StatusCartaoEnum

class CartaoModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    numero_cartao: str = Field(..., min_length=16, max_length=16)
    pessoa_id: str
    tipo_cartao: TipoCartaoEnum
    status: StatusCartaoEnum
    data_emissao: datetime = Field(default_factory=datetime.utcnow)
    data_validade: Optional[datetime] = None
    ativo: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "numero_cartao": "1000123456789012",
                "pessoa_id": "123e4567-e89b-12d3-a456-426614174001",
                "tipo_cartao": "BILHETE_UNICO",
                "status": "ATIVO",
                "data_emissao": "2025-01-10T10:00:00",
                "ativo": True
            }
        }