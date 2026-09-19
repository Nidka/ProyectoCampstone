from __future__ import annotations
from app.features.producto_categoria.application.schemas import ProductoCategoriaCreate, ProductoCategoriaRead
from app.features.producto_categoria.domain.repositories import ProductoCategoriaRepository
from app.shared.exceptions import ConflictError, NotFoundError


class ProductoCategoriaUseCases:
    def __init__(self, repository: ProductoCategoriaRepository) -> None:
        self._repository = repository

    def list_categorias(self, limit: int, offset: int) -> list[ProductoCategoriaRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_categoria(self, id_categoria: int) -> ProductoCategoriaRead:
        found = self._repository.get_by_id(id_categoria)
        if not found:
            raise NotFoundError("Categoria no encontrada")
        return found

    def create_categoria(self, payload: ProductoCategoriaCreate) -> ProductoCategoriaRead:
        if self._repository.get_by_nombre(payload.nombre):
            raise ConflictError("El nombre de la categoria ya existe")
        return self._repository.create(payload)
