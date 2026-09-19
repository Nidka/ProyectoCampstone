from __future__ import annotations
from typing import Protocol

from app.features.detalle_presupuesto.application.schemas import DetallePresupuestoCreate, DetallePresupuestoRead


class DetallePresupuestoRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[DetallePresupuestoRead]:
        ...

    def get_by_id(self, id_detalle_presupuesto: int) -> DetallePresupuestoRead | None:
        ...

    def create(self, payload: DetallePresupuestoCreate) -> DetallePresupuestoRead:
        ...
