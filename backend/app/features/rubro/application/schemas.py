from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class RubroBase(BaseModel):
    nombre: str = Field(max_length=100)
    descripcion: str | None = Field(default=None, max_length=100)
    estado_rubro: bool = True


class RubroCreate(RubroBase):
    pass


class RubroRead(RubroBase):
    id_rubro: int
    model_config = ConfigDict(from_attributes=True)
