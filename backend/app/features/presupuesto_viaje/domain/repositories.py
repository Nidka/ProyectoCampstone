from __future__ import annotations
from typing import Protocol

from app.features.presupuesto_viaje.application.schemas import PresupuestoViajeCreate, PresupuestoViajeRead


class PresupuestoViajeRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[PresupuestoViajeRead]:
        ...

    def get_by_id(self, id_presupuesto: int) -> PresupuestoViajeRead | None:
        ...

    def create(self, payload: PresupuestoViajeCreate) -> PresupuestoViajeRead:
        ...
