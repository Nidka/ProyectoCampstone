from __future__ import annotations
from typing import Protocol

from app.features.viaje_realizado.application.schemas import ViajeRealizadoCreate, ViajeRealizadoRead


class ViajeRealizadoRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[ViajeRealizadoRead]:
        ...

    def get_by_id(self, id_viaje_realizado: int) -> ViajeRealizadoRead | None:
        ...

    def create(self, payload: ViajeRealizadoCreate) -> ViajeRealizadoRead:
        ...
