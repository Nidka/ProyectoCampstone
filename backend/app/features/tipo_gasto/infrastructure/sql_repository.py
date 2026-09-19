from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.tipo_gasto.application.schemas import TipoGastoCreate, TipoGastoRead
from app.features.tipo_gasto.domain.repositories import TipoGastoRepository
from app.infrastructure.db.models import TipoGastoModel


class TipoGastoSqlRepository(TipoGastoRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[TipoGastoRead]:
        stmt = select(TipoGastoModel).offset(offset).limit(limit).order_by(TipoGastoModel.id_tipo_gasto)
        rows = self._db.scalars(stmt).all()
        return [TipoGastoRead.model_validate(row) for row in rows]

    def get_by_id(self, id_tipo_gasto: int) -> TipoGastoRead | None:
        row = self._db.get(TipoGastoModel, id_tipo_gasto)
        if not row:
            return None
        return TipoGastoRead.model_validate(row)

    def get_by_nombre(self, nombre: str) -> TipoGastoRead | None:
        stmt = select(TipoGastoModel).where(TipoGastoModel.nombre == nombre)
        row = self._db.scalars(stmt).first()
        if not row:
            return None
        return TipoGastoRead.model_validate(row)

    def create(self, payload: TipoGastoCreate) -> TipoGastoRead:
        row = TipoGastoModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return TipoGastoRead.model_validate(row)
