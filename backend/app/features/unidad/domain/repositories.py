from __future__ import annotations
from typing import Protocol

from app.features.unidad.application.schemas import UnidadCreate, UnidadRead


class UnidadRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[UnidadRead]:
        ...

    def get_by_id(self, id_unidad: int) -> UnidadRead | None:
        ...

    def get_by_placa(self, placa: str) -> UnidadRead | None:
        ...

    def create(self, payload: UnidadCreate) -> UnidadRead:
        ...
