from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class DireccionBase(BaseModel):
    codigo_ubigeo: int
    direccion_detallada: str = Field(max_length=200)
    referencia: str | None = Field(default=None, max_length=50)
    descripcion: str | None = Field(default=None, max_length=50)
    estado_direccion: bool = True


class DireccionCreate(DireccionBase):
    pass


class DireccionRead(DireccionBase):
    id_direccion: int
    model_config = ConfigDict(from_attributes=True)
