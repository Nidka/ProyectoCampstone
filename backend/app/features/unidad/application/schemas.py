from __future__ import annotations
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class UnidadBase(BaseModel):
    placa: str = Field(max_length=20)
    id_tipo_unidad: int
    id_subtipo_unidad: int | None = None
    id_marca: int
    modelo: str | None = Field(default=None, max_length=50)
    anio: int | None = None
    peso_tara: Decimal | None = None
    peso_maximo: Decimal | None = None
    estado_unidad: bool = True


class UnidadCreate(UnidadBase):
    pass


class UnidadRead(UnidadBase):
    id_unidad: int

    model_config = ConfigDict(from_attributes=True)
