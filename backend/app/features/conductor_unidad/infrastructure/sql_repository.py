from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.conductor_unidad.application.schemas import ConductorUnidadCreate, ConductorUnidadRead
from app.features.conductor_unidad.domain.repositories import ConductorUnidadRepository
from app.infrastructure.db.models import ConductorUnidadModel


class ConductorUnidadSqlRepository(ConductorUnidadRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[ConductorUnidadRead]:
        stmt = select(ConductorUnidadModel).offset(offset).limit(limit).order_by(ConductorUnidadModel.id_conductor_unidad)
        rows = self._db.scalars(stmt).all()
        return [ConductorUnidadRead.model_validate(row) for row in rows]

    def get_by_id(self, id_conductor_unidad: int) -> ConductorUnidadRead | None:
        row = self._db.get(ConductorUnidadModel, id_conductor_unidad)
        if not row:
            return None
        return ConductorUnidadRead.model_validate(row)

    def create(self, payload: ConductorUnidadCreate) -> ConductorUnidadRead:
        row = ConductorUnidadModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return ConductorUnidadRead.model_validate(row)
