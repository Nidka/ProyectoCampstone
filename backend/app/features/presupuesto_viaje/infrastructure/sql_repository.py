from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.presupuesto_viaje.application.schemas import PresupuestoViajeCreate, PresupuestoViajeRead
from app.features.presupuesto_viaje.domain.repositories import PresupuestoViajeRepository
from app.infrastructure.db.models import PresupuestoViajeModel


class PresupuestoViajeSqlRepository(PresupuestoViajeRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[PresupuestoViajeRead]:
        stmt = select(PresupuestoViajeModel).offset(offset).limit(limit).order_by(PresupuestoViajeModel.id_presupuesto)
        rows = self._db.scalars(stmt).all()
        return [PresupuestoViajeRead.model_validate(row) for row in rows]

    def get_by_id(self, id_presupuesto: int) -> PresupuestoViajeRead | None:
        row = self._db.get(PresupuestoViajeModel, id_presupuesto)
        if not row:
            return None
        return PresupuestoViajeRead.model_validate(row)

    def create(self, payload: PresupuestoViajeCreate) -> PresupuestoViajeRead:
        row = PresupuestoViajeModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return PresupuestoViajeRead.model_validate(row)
