from __future__ import annotations
from app.features.viaje_realizado.application.schemas import ViajeRealizadoCreate, ViajeRealizadoRead
from app.features.viaje_realizado.domain.repositories import ViajeRealizadoRepository
from app.shared.exceptions import NotFoundError


class ViajeRealizadoUseCases:
    def __init__(self, repository: ViajeRealizadoRepository) -> None:
        self._repository = repository

    def list_viajes_realizados(self, limit: int, offset: int) -> list[ViajeRealizadoRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_viaje_realizado(self, id_viaje_realizado: int) -> ViajeRealizadoRead:
        found = self._repository.get_by_id(id_viaje_realizado)
        if not found:
            raise NotFoundError("ViajeRealizado no encontrado")
        return found

    def create_viaje_realizado(self, payload: ViajeRealizadoCreate) -> ViajeRealizadoRead:
        return self._repository.create(payload)
