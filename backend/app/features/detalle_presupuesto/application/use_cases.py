from __future__ import annotations
from app.features.detalle_presupuesto.application.schemas import DetallePresupuestoCreate, DetallePresupuestoRead
from app.features.detalle_presupuesto.domain.repositories import DetallePresupuestoRepository
from app.shared.exceptions import NotFoundError


class DetallePresupuestoUseCases:
    def __init__(self, repository: DetallePresupuestoRepository) -> None:
        self._repository = repository

    def list_detalles(self, limit: int, offset: int) -> list[DetallePresupuestoRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_detalle(self, id_detalle_presupuesto: int) -> DetallePresupuestoRead:
        found = self._repository.get_by_id(id_detalle_presupuesto)
        if not found:
            raise NotFoundError("DetallePresupuesto no encontrado")
        return found

    def create_detalle(self, payload: DetallePresupuestoCreate) -> DetallePresupuestoRead:
        return self._repository.create(payload)
