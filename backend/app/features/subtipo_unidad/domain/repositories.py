from __future__ import annotations
from typing import Protocol

from app.features.subtipo_unidad.application.schemas import SubtipoUnidadCreate, SubtipoUnidadRead


class SubtipoUnidadRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[SubtipoUnidadRead]:
        ...

    def get_by_id(self, id_subtipo_unidad: int) -> SubtipoUnidadRead | None:
        ...

    def create(self, payload: SubtipoUnidadCreate) -> SubtipoUnidadRead:
        ...
