from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class SubtipoUnidadBase(BaseModel):
    id_tipo_unidad: int
    nombre: str = Field(max_length=50)
    descripcion: str | None = Field(default=None, max_length=50)
    estado_subtipounidad: bool = True


class SubtipoUnidadCreate(SubtipoUnidadBase):
    pass


class SubtipoUnidadRead(SubtipoUnidadBase):
    id_subtipo_unidad: int
    model_config = ConfigDict(from_attributes=True)
