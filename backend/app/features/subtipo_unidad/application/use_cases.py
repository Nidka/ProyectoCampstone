from __future__ import annotations
from app.features.subtipo_unidad.application.schemas import SubtipoUnidadCreate, SubtipoUnidadRead
from app.features.subtipo_unidad.domain.repositories import SubtipoUnidadRepository
from app.shared.exceptions import NotFoundError


class SubtipoUnidadUseCases:
    def __init__(self, repository: SubtipoUnidadRepository) -> None:
        self._repository = repository

    def list_subtipos(self, limit: int, offset: int) -> list[SubtipoUnidadRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_subtipo(self, id_subtipo_unidad: int) -> SubtipoUnidadRead:
        found = self._repository.get_by_id(id_subtipo_unidad)
        if not found:
            raise NotFoundError("SubtipoUnidad no encontrado")
        return found

    def create_subtipo(self, payload: SubtipoUnidadCreate) -> SubtipoUnidadRead:
        return self._repository.create(payload)
