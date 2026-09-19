from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.rubro.application.schemas import RubroCreate, RubroRead
from app.features.rubro.domain.repositories import RubroRepository
from app.infrastructure.db.models import RubroModel


class RubroSqlRepository(RubroRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[RubroRead]:
        stmt = select(RubroModel).offset(offset).limit(limit).order_by(RubroModel.id_rubro)
        rows = self._db.scalars(stmt).all()
        return [RubroRead.model_validate(row) for row in rows]

    def get_by_id(self, id_rubro: int) -> RubroRead | None:
        row = self._db.get(RubroModel, id_rubro)
        if not row:
            return None
        return RubroRead.model_validate(row)

    def get_by_nombre(self, nombre: str) -> RubroRead | None:
        stmt = select(RubroModel).where(RubroModel.nombre == nombre)
        row = self._db.scalars(stmt).first()
        if not row:
            return None
        return RubroRead.model_validate(row)

    def create(self, payload: RubroCreate) -> RubroRead:
        row = RubroModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return RubroRead.model_validate(row)
