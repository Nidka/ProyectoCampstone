from __future__ import annotations
from app.features.conductor_unidad.application.schemas import ConductorUnidadCreate, ConductorUnidadRead
from app.features.conductor_unidad.domain.repositories import ConductorUnidadRepository
from app.shared.exceptions import NotFoundError


class ConductorUnidadUseCases:
    def __init__(self, repository: ConductorUnidadRepository) -> None:
        self._repository = repository

    def list_asignaciones(self, limit: int, offset: int) -> list[ConductorUnidadRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_asignacion(self, id_conductor_unidad: int) -> ConductorUnidadRead:
        found = self._repository.get_by_id(id_conductor_unidad)
        if not found:
            raise NotFoundError("Asignacion no encontrada")
        return found

    def create_asignacion(self, payload: ConductorUnidadCreate) -> ConductorUnidadRead:
        return self._repository.create(payload)
