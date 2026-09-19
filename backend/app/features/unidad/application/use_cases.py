from __future__ import annotations
from app.features.unidad.application.schemas import UnidadCreate, UnidadRead
from app.features.unidad.domain.repositories import UnidadRepository
from app.shared.exceptions import ConflictError, NotFoundError


class UnidadUseCases:
    def __init__(self, repository: UnidadRepository) -> None:
        self._repository = repository

    def list_unidades(self, limit: int, offset: int) -> list[UnidadRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_unidad(self, id_unidad: int) -> UnidadRead:
        found = self._repository.get_by_id(id_unidad)
        if not found:
            raise NotFoundError("Unidad no encontrada")
        return found

    def create_unidad(self, payload: UnidadCreate) -> UnidadRead:
        if self._repository.get_by_placa(payload.placa):
            raise ConflictError("La placa ya existe")
        return self._repository.create(payload)
