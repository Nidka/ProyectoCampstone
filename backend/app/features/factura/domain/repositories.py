from __future__ import annotations
from typing import Protocol

from app.features.factura.application.schemas import FacturaCreate, FacturaRead


class FacturaRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[FacturaRead]:
        ...

    def get_by_id(self, id_factura: int) -> FacturaRead | None:
        ...

    def get_by_numero(self, numero_factura: str) -> FacturaRead | None:
        ...

    def create(self, payload: FacturaCreate) -> FacturaRead:
        ...
