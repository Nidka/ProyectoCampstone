from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class TipoGastoBase(BaseModel):
    nombre: str = Field(max_length=100)
    descripcion: str | None = Field(default=None, max_length=200)
    estado_tipogasto: bool = True


class TipoGastoCreate(TipoGastoBase):
    pass


class TipoGastoRead(TipoGastoBase):
    id_tipo_gasto: int
    model_config = ConfigDict(from_attributes=True)
