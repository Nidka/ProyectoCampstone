from __future__ import annotations
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class ProductoTransportadoBase(BaseModel):
    id_guia_transportista: int
    id_categoria: int
    descripcion_producto: str = Field(max_length=200)
    cantidad: int
    peso: Decimal
    estado_producto: bool = True


class ProductoTransportadoCreate(ProductoTransportadoBase):
    pass


class ProductoTransportadoRead(ProductoTransportadoBase):
    id_producto_transportado: int
    model_config = ConfigDict(from_attributes=True)
