from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.marca.application.schemas import MarcaCreate, MarcaRead
from app.features.marca.domain.repositories import MarcaRepository
from app.infrastructure.db.models import MarcaModel


class MarcaSqlRepository(MarcaRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[MarcaRead]:
        stmt = select(MarcaModel).offset(offset).limit(limit).order_by(MarcaModel.id_marca)
        rows = self._db.scalars(stmt).all()
        return [MarcaRead.model_validate(row) for row in rows]

    def get_by_id(self, id_marca: int) -> MarcaRead | None:
        row = self._db.get(MarcaModel, id_marca)
        if not row:
            return None
        return MarcaRead.model_validate(row)

    def get_by_nombre(self, nombre: str) -> MarcaRead | None:
        stmt = select(MarcaModel).where(MarcaModel.nombre == nombre)
        row = self._db.scalars(stmt).first()
        if not row:
            return None
        return MarcaRead.model_validate(row)

    def create(self, payload: MarcaCreate) -> MarcaRead:
        row = MarcaModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return MarcaRead.model_validate(row)
