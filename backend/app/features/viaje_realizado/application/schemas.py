from __future__ import annotations
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class ViajeRealizadoBase(BaseModel):
    id_guia_transportista: int
    flete: Decimal
    fecha_llegada: datetime
    observaciones: str | None = Field(default=None, max_length=200)
    estado_viaje_realizado: bool = True


class ViajeRealizadoCreate(ViajeRealizadoBase):
    pass


class ViajeRealizadoRead(ViajeRealizadoBase):
    id_viaje_realizado: int
    model_config = ConfigDict(from_attributes=True)
