from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.direccion.application.schemas import DireccionCreate, DireccionRead
from app.features.direccion.domain.repositories import DireccionRepository
from app.infrastructure.db.models import DireccionModel


class DireccionSqlRepository(DireccionRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[DireccionRead]:
        stmt = select(DireccionModel).offset(offset).limit(limit).order_by(DireccionModel.id_direccion)
        rows = self._db.scalars(stmt).all()
        return [DireccionRead.model_validate(row) for row in rows]

    def get_by_id(self, id_direccion: int) -> DireccionRead | None:
        row = self._db.get(DireccionModel, id_direccion)
        if not row:
            return None
        return DireccionRead.model_validate(row)

    def create(self, payload: DireccionCreate) -> DireccionRead:
        row = DireccionModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return DireccionRead.model_validate(row)
