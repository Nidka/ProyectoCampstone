from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.producto_categoria.application.schemas import ProductoCategoriaCreate, ProductoCategoriaRead
from app.features.producto_categoria.domain.repositories import ProductoCategoriaRepository
from app.infrastructure.db.models import ProductoCategoriaModel


class ProductoCategoriaSqlRepository(ProductoCategoriaRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[ProductoCategoriaRead]:
        stmt = select(ProductoCategoriaModel).offset(offset).limit(limit).order_by(ProductoCategoriaModel.id_categoria)
        rows = self._db.scalars(stmt).all()
        return [ProductoCategoriaRead.model_validate(row) for row in rows]

    def get_by_id(self, id_categoria: int) -> ProductoCategoriaRead | None:
        row = self._db.get(ProductoCategoriaModel, id_categoria)
        if not row:
            return None
        return ProductoCategoriaRead.model_validate(row)

    def get_by_nombre(self, nombre: str) -> ProductoCategoriaRead | None:
        stmt = select(ProductoCategoriaModel).where(ProductoCategoriaModel.nombre == nombre)
        row = self._db.scalars(stmt).first()
        if not row:
            return None
        return ProductoCategoriaRead.model_validate(row)

    def create(self, payload: ProductoCategoriaCreate) -> ProductoCategoriaRead:
        row = ProductoCategoriaModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return ProductoCategoriaRead.model_validate(row)
