from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class ProductoCategoriaBase(BaseModel):
    nombre: str = Field(max_length=100)
    descripcion: str | None = Field(default=None, max_length=200)
    estado_categoria: bool = True


class ProductoCategoriaCreate(ProductoCategoriaBase):
    pass


class ProductoCategoriaRead(ProductoCategoriaBase):
    id_categoria: int
    model_config = ConfigDict(from_attributes=True)
