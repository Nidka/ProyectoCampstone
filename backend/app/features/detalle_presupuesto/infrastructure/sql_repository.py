from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.detalle_presupuesto.application.schemas import DetallePresupuestoCreate, DetallePresupuestoRead
from app.features.detalle_presupuesto.domain.repositories import DetallePresupuestoRepository
from app.infrastructure.db.models import DetallePresupuestoModel


class DetallePresupuestoSqlRepository(DetallePresupuestoRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[DetallePresupuestoRead]:
        stmt = select(DetallePresupuestoModel).offset(offset).limit(limit).order_by(DetallePresupuestoModel.id_detalle_presupuesto)
        rows = self._db.scalars(stmt).all()
        return [DetallePresupuestoRead.model_validate(row) for row in rows]

    def get_by_id(self, id_detalle_presupuesto: int) -> DetallePresupuestoRead | None:
        row = self._db.get(DetallePresupuestoModel, id_detalle_presupuesto)
        if not row:
            return None
        return DetallePresupuestoRead.model_validate(row)

    def create(self, payload: DetallePresupuestoCreate) -> DetallePresupuestoRead:
        row = DetallePresupuestoModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return DetallePresupuestoRead.model_validate(row)
