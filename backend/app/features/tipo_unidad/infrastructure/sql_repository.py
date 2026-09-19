from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.tipo_unidad.application.schemas import TipoUnidadCreate, TipoUnidadRead
from app.features.tipo_unidad.domain.repositories import TipoUnidadRepository
from app.infrastructure.db.models import TipoUnidadModel


class TipoUnidadSqlRepository(TipoUnidadRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[TipoUnidadRead]:
        stmt = select(TipoUnidadModel).offset(offset).limit(limit).order_by(TipoUnidadModel.id_tipo_unidad)
        rows = self._db.scalars(stmt).all()
        return [TipoUnidadRead.model_validate(row) for row in rows]

    def get_by_id(self, id_tipo_unidad: int) -> TipoUnidadRead | None:
        row = self._db.get(TipoUnidadModel, id_tipo_unidad)
        if not row:
            return None
        return TipoUnidadRead.model_validate(row)

    def get_by_nombre(self, nombre: str) -> TipoUnidadRead | None:
        stmt = select(TipoUnidadModel).where(TipoUnidadModel.nombre == nombre)
        row = self._db.scalars(stmt).first()
        if not row:
            return None
        return TipoUnidadRead.model_validate(row)

    def create(self, payload: TipoUnidadCreate) -> TipoUnidadRead:
        row = TipoUnidadModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return TipoUnidadRead.model_validate(row)
