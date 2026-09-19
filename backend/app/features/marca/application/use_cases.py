from __future__ import annotations
from app.features.marca.application.schemas import MarcaCreate, MarcaRead
from app.features.marca.domain.repositories import MarcaRepository
from app.shared.exceptions import ConflictError, NotFoundError


class MarcaUseCases:
    def __init__(self, repository: MarcaRepository) -> None:
        self._repository = repository

    def list_marcas(self, limit: int, offset: int) -> list[MarcaRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_marca(self, id_marca: int) -> MarcaRead:
        found = self._repository.get_by_id(id_marca)
        if not found:
            raise NotFoundError("Marca no encontrada")
        return found

    def create_marca(self, payload: MarcaCreate) -> MarcaRead:
        if self._repository.get_by_nombre(payload.nombre):
            raise ConflictError("El nombre de la marca ya existe")
        return self._repository.create(payload)
