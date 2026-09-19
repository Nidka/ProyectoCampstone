from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.unidad.application.schemas import UnidadCreate, UnidadRead
from app.features.unidad.domain.repositories import UnidadRepository
from app.infrastructure.db.models import UnidadModel


class UnidadSqlRepository(UnidadRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[UnidadRead]:
        stmt = select(UnidadModel).offset(offset).limit(limit).order_by(UnidadModel.id_unidad)
        rows = self._db.scalars(stmt).all()
        return [UnidadRead.model_validate(row) for row in rows]

    def get_by_id(self, id_unidad: int) -> UnidadRead | None:
        row = self._db.get(UnidadModel, id_unidad)
        if not row:
            return None
        return UnidadRead.model_validate(row)

    def get_by_placa(self, placa: str) -> UnidadRead | None:
        stmt = select(UnidadModel).where(UnidadModel.placa == placa)
        row = self._db.scalars(stmt).first()
        if not row:
            return None
        return UnidadRead.model_validate(row)

    def create(self, payload: UnidadCreate) -> UnidadRead:
        row = UnidadModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return UnidadRead.model_validate(row)
