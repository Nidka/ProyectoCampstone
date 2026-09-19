from __future__ import annotations
from app.features.producto_transportado.application.schemas import ProductoTransportadoCreate, ProductoTransportadoRead
from app.features.producto_transportado.domain.repositories import ProductoTransportadoRepository
from app.shared.exceptions import NotFoundError


class ProductoTransportadoUseCases:
    def __init__(self, repository: ProductoTransportadoRepository) -> None:
        self._repository = repository

    def list_productos(self, limit: int, offset: int) -> list[ProductoTransportadoRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_producto(self, id_producto_transportado: int) -> ProductoTransportadoRead:
        found = self._repository.get_by_id(id_producto_transportado)
        if not found:
            raise NotFoundError("ProductoTransportado no encontrado")
        return found

    def create_producto(self, payload: ProductoTransportadoCreate) -> ProductoTransportadoRead:
        return self._repository.create(payload)
