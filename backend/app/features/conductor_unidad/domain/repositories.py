from __future__ import annotations
from typing import Protocol

from app.features.conductor_unidad.application.schemas import ConductorUnidadCreate, ConductorUnidadRead


class ConductorUnidadRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[ConductorUnidadRead]:
        ...

    def get_by_id(self, id_conductor_unidad: int) -> ConductorUnidadRead | None:
        ...

    def create(self, payload: ConductorUnidadCreate) -> ConductorUnidadRead:
        ...
