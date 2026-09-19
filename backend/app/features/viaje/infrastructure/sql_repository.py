from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.viaje.application.schemas import ViajeCreate, ViajeRead
from app.features.viaje.domain.repositories import ViajeRepository
from app.infrastructure.db.models import ProgramacionViajeModel


class ViajeSqlRepository(ViajeRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[ViajeRead]:
        stmt = select(ProgramacionViajeModel).offset(offset).limit(limit).order_by(ProgramacionViajeModel.id_viaje)
        rows = self._db.scalars(stmt).all()
        return [ViajeRead.model_validate(row) for row in rows]

    def get_by_id(self, id_viaje: int) -> ViajeRead | None:
        row = self._db.get(ProgramacionViajeModel, id_viaje)
        if not row:
            return None
        return ViajeRead.model_validate(row)

    def create(self, payload: ViajeCreate) -> ViajeRead:
        row = ProgramacionViajeModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return ViajeRead.model_validate(row)
