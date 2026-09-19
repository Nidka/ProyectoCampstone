from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class TipoUnidadBase(BaseModel):
    nombre: str = Field(max_length=50)
    descripcion: str | None = Field(default=None, max_length=50)
    estado_tipounidad: bool = True


class TipoUnidadCreate(TipoUnidadBase):
    pass


class TipoUnidadRead(TipoUnidadBase):
    id_tipo_unidad: int
    model_config = ConfigDict(from_attributes=True)
