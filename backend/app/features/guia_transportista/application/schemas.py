from __future__ import annotations
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class GuiaTransportistaBase(BaseModel):
    numero_guia: str = Field(max_length=50)
    id_viaje: int
    guias_remitente: str | None = Field(default=None, max_length=500)
    peso_total: Decimal
    estado_guia: bool = True


class GuiaTransportistaCreate(GuiaTransportistaBase):
    pass


class GuiaTransportistaRead(GuiaTransportistaBase):
    id_guia_transportista: int
    model_config = ConfigDict(from_attributes=True)
