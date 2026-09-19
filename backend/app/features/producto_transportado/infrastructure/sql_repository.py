from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.producto_transportado.application.schemas import ProductoTransportadoCreate, ProductoTransportadoRead
from app.features.producto_transportado.domain.repositories import ProductoTransportadoRepository
from app.infrastructure.db.models import ProductoTransportadoModel


class ProductoTransportadoSqlRepository(ProductoTransportadoRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[ProductoTransportadoRead]:
        stmt = select(ProductoTransportadoModel).offset(offset).limit(limit).order_by(ProductoTransportadoModel.id_producto_transportado)
        rows = self._db.scalars(stmt).all()
        return [ProductoTransportadoRead.model_validate(row) for row in rows]

    def get_by_id(self, id_producto_transportado: int) -> ProductoTransportadoRead | None:
        row = self._db.get(ProductoTransportadoModel, id_producto_transportado)
        if not row:
            return None
        return ProductoTransportadoRead.model_validate(row)

    def create(self, payload: ProductoTransportadoCreate) -> ProductoTransportadoRead:
        row = ProductoTransportadoModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return ProductoTransportadoRead.model_validate(row)
