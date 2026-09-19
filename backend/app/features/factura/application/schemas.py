from __future__ import annotations
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class FacturaBase(BaseModel):
    numero_factura: str = Field(max_length=50)
    id_viaje_realizado: int
    monto_total: Decimal
    estado_factura: bool = True


class FacturaCreate(FacturaBase):
    pass


class FacturaRead(FacturaBase):
    id_factura: int
    model_config = ConfigDict(from_attributes=True)
