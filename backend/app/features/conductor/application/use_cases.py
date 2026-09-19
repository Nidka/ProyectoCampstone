from __future__ import annotations
from app.features.conductor.application.schemas import ConductorCreate, ConductorRead
from app.features.conductor.domain.repositories import ConductorRepository
from app.shared.exceptions import ConflictError, NotFoundError


class ConductorUseCases:
    def __init__(self, repository: ConductorRepository) -> None:
        self._repository = repository

    def list_conductores(self, limit: int, offset: int) -> list[ConductorRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_conductor(self, id_conductor: int) -> ConductorRead:
        found = self._repository.get_by_id(id_conductor)
        if not found:
            raise NotFoundError("Conductor no encontrado")
        return found

    def create_conductor(self, payload: ConductorCreate) -> ConductorRead:
        if self._repository.get_by_dni(payload.dni):
            raise ConflictError("El DNI del conductor ya existe")
        return self._repository.create(payload)
