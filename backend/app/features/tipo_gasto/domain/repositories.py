from __future__ import annotations
from typing import Protocol

from app.features.tipo_gasto.application.schemas import TipoGastoCreate, TipoGastoRead


class TipoGastoRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[TipoGastoRead]:
        ...

    def get_by_id(self, id_tipo_gasto: int) -> TipoGastoRead | None:
        ...

    def get_by_nombre(self, nombre: str) -> TipoGastoRead | None:
        ...

    def create(self, payload: TipoGastoCreate) -> TipoGastoRead:
        ...
