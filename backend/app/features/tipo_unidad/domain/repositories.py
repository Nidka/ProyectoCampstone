from __future__ import annotations
from typing import Protocol

from app.features.tipo_unidad.application.schemas import TipoUnidadCreate, TipoUnidadRead


class TipoUnidadRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[TipoUnidadRead]:
        ...

    def get_by_id(self, id_tipo_unidad: int) -> TipoUnidadRead | None:
        ...

    def get_by_nombre(self, nombre: str) -> TipoUnidadRead | None:
        ...

    def create(self, payload: TipoUnidadCreate) -> TipoUnidadRead:
        ...
