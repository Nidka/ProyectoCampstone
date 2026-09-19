from __future__ import annotations
from app.features.viaje.application.schemas import ViajeCreate, ViajeRead
from app.features.viaje.domain.repositories import ViajeRepository
from app.shared.exceptions import NotFoundError


class ViajeUseCases:
    def __init__(self, repository: ViajeRepository) -> None:
        self._repository = repository

    def list_viajes(self, limit: int, offset: int) -> list[ViajeRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_viaje(self, id_viaje: int) -> ViajeRead:
        found = self._repository.get_by_id(id_viaje)
        if not found:
            raise NotFoundError("Viaje no encontrado")
        return found

    def create_viaje(self, payload: ViajeCreate) -> ViajeRead:
        return self._repository.create(payload)
