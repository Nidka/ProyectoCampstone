from __future__ import annotations
from app.features.presupuesto_viaje.application.schemas import PresupuestoViajeCreate, PresupuestoViajeRead
from app.features.presupuesto_viaje.domain.repositories import PresupuestoViajeRepository
from app.shared.exceptions import NotFoundError


class PresupuestoViajeUseCases:
    def __init__(self, repository: PresupuestoViajeRepository) -> None:
        self._repository = repository

    def list_presupuestos(self, limit: int, offset: int) -> list[PresupuestoViajeRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_presupuesto(self, id_presupuesto: int) -> PresupuestoViajeRead:
        found = self._repository.get_by_id(id_presupuesto)
        if not found:
            raise NotFoundError("Presupuesto no encontrado")
        return found

    def create_presupuesto(self, payload: PresupuestoViajeCreate) -> PresupuestoViajeRead:
        return self._repository.create(payload)
