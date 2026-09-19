from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.conductor.application.schemas import ConductorCreate, ConductorRead
from app.features.conductor.domain.repositories import ConductorRepository
from app.infrastructure.db.models import ConductorModel


class ConductorSqlRepository(ConductorRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[ConductorRead]:
        stmt = select(ConductorModel).offset(offset).limit(limit).order_by(ConductorModel.id_conductor)
        rows = self._db.scalars(stmt).all()
        return [ConductorRead.model_validate(row) for row in rows]

    def get_by_id(self, id_conductor: int) -> ConductorRead | None:
        row = self._db.get(ConductorModel, id_conductor)
        if not row:
            return None
        return ConductorRead.model_validate(row)

    def get_by_dni(self, dni: str) -> ConductorRead | None:
        stmt = select(ConductorModel).where(ConductorModel.dni == dni)
        row = self._db.scalars(stmt).first()
        if not row:
            return None
        return ConductorRead.model_validate(row)

    def create(self, payload: ConductorCreate) -> ConductorRead:
        row = ConductorModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return ConductorRead.model_validate(row)
