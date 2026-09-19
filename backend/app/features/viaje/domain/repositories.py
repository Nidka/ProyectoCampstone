from __future__ import annotations
from typing import Protocol

from app.features.viaje.application.schemas import ViajeCreate, ViajeRead


class ViajeRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[ViajeRead]:
        ...

    def get_by_id(self, id_viaje: int) -> ViajeRead | None:
        ...

    def create(self, payload: ViajeCreate) -> ViajeRead:
        ...
