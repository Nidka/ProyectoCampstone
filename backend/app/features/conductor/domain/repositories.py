from __future__ import annotations
from typing import Protocol

from app.features.conductor.application.schemas import ConductorCreate, ConductorRead


class ConductorRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[ConductorRead]:
        ...

    def get_by_id(self, id_conductor: int) -> ConductorRead | None:
        ...

    def get_by_dni(self, dni: str) -> ConductorRead | None:
        ...

    def create(self, payload: ConductorCreate) -> ConductorRead:
        ...
