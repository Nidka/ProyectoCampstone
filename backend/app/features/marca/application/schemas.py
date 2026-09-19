from __future__ import annotations
from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class MarcaBase(BaseModel):
    nombre: str = Field(max_length=100)
    pais_origen: str | None = Field(default=None, max_length=100)
    fecha_fundacion: date | None = None
    descripcion: str | None = Field(default=None, max_length=50)
    estado_marca: bool = True


class MarcaCreate(MarcaBase):
    pass


class MarcaRead(MarcaBase):
    id_marca: int
    model_config = ConfigDict(from_attributes=True)
