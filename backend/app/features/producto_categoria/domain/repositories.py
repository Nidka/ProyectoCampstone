from __future__ import annotations
from typing import Protocol

from app.features.producto_categoria.application.schemas import ProductoCategoriaCreate, ProductoCategoriaRead


class ProductoCategoriaRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[ProductoCategoriaRead]:
        ...

    def get_by_id(self, id_categoria: int) -> ProductoCategoriaRead | None:
        ...

    def get_by_nombre(self, nombre: str) -> ProductoCategoriaRead | None:
        ...

    def create(self, payload: ProductoCategoriaCreate) -> ProductoCategoriaRead:
        ...
