from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.factura.application.schemas import FacturaCreate, FacturaRead
from app.features.factura.domain.repositories import FacturaRepository
from app.infrastructure.db.models import FacturaModel


class FacturaSqlRepository(FacturaRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[FacturaRead]:
        stmt = select(FacturaModel).offset(offset).limit(limit).order_by(FacturaModel.id_factura)
        rows = self._db.scalars(stmt).all()
        return [FacturaRead.model_validate(row) for row in rows]

    def get_by_id(self, id_factura: int) -> FacturaRead | None:
        row = self._db.get(FacturaModel, id_factura)
        if not row:
            return None
        return FacturaRead.model_validate(row)

    def get_by_numero(self, numero_factura: str) -> FacturaRead | None:
        stmt = select(FacturaModel).where(FacturaModel.numero_factura == numero_factura)
        row = self._db.scalars(stmt).first()
        if not row:
            return None
        return FacturaRead.model_validate(row)

    def create(self, payload: FacturaCreate) -> FacturaRead:
        row = FacturaModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return FacturaRead.model_validate(row)
