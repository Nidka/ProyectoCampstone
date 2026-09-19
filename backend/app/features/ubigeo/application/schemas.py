from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class UbigeoBase(BaseModel):
    provincia: str = Field(max_length=25)
    distrito: str = Field(max_length=25)
    departamento: str = Field(max_length=25)
    estado_ubigeo: bool = True


class UbigeoCreate(UbigeoBase):
    codigo_ubigeo: int


class UbigeoRead(UbigeoBase):
    codigo_ubigeo: int
    model_config = ConfigDict(from_attributes=True)
