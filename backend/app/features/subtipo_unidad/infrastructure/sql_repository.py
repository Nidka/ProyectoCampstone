from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.subtipo_unidad.application.schemas import SubtipoUnidadCreate, SubtipoUnidadRead
from app.features.subtipo_unidad.domain.repositories import SubtipoUnidadRepository
from app.infrastructure.db.models import SubtipoUnidadModel


class SubtipoUnidadSqlRepository(SubtipoUnidadRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[SubtipoUnidadRead]:
        stmt = select(SubtipoUnidadModel).offset(offset).limit(limit).order_by(SubtipoUnidadModel.id_subtipo_unidad)
        rows = self._db.scalars(stmt).all()
        return [SubtipoUnidadRead.model_validate(row) for row in rows]

    def get_by_id(self, id_subtipo_unidad: int) -> SubtipoUnidadRead | None:
        row = self._db.get(SubtipoUnidadModel, id_subtipo_unidad)
        if not row:
            return None
        return SubtipoUnidadRead.model_validate(row)

    def create(self, payload: SubtipoUnidadCreate) -> SubtipoUnidadRead:
        row = SubtipoUnidadModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return SubtipoUnidadRead.model_validate(row)
