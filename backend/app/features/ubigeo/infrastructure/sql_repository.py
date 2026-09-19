from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.ubigeo.application.schemas import UbigeoCreate, UbigeoRead
from app.features.ubigeo.domain.repositories import UbigeoRepository
from app.infrastructure.db.models import UbigeoModel


class UbigeoSqlRepository(UbigeoRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[UbigeoRead]:
        stmt = select(UbigeoModel).offset(offset).limit(limit).order_by(UbigeoModel.codigo_ubigeo)
        rows = self._db.scalars(stmt).all()
        return [UbigeoRead.model_validate(row) for row in rows]

    def get_by_codigo(self, codigo_ubigeo: int) -> UbigeoRead | None:
        row = self._db.get(UbigeoModel, codigo_ubigeo)
        if not row:
            return None
        return UbigeoRead.model_validate(row)

    def create(self, payload: UbigeoCreate) -> UbigeoRead:
        row = UbigeoModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return UbigeoRead.model_validate(row)
