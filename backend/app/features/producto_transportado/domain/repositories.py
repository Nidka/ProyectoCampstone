from __future__ import annotations
from typing import Protocol

from app.features.producto_transportado.application.schemas import ProductoTransportadoCreate, ProductoTransportadoRead


class ProductoTransportadoRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[ProductoTransportadoRead]:
        ...

    def get_by_id(self, id_producto_transportado: int) -> ProductoTransportadoRead | None:
        ...

    def create(self, payload: ProductoTransportadoCreate) -> ProductoTransportadoRead:
        ...
