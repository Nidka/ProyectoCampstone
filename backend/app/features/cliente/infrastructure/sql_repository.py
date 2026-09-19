from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.cliente.application.schemas import ClienteCreate, ClienteRead
from app.features.cliente.domain.repositories import ClienteRepository
from app.infrastructure.db.models import ClienteModel


class ClienteSqlRepository(ClienteRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[ClienteRead]:
        stmt = select(ClienteModel).offset(offset).limit(limit).order_by(ClienteModel.id_cliente)
        rows = self._db.scalars(stmt).all()
        return [ClienteRead.model_validate(row) for row in rows]

    def get_by_id(self, id_cliente: int) -> ClienteRead | None:
        row = self._db.get(ClienteModel, id_cliente)
        if not row:
            return None
        return ClienteRead.model_validate(row)

    def get_by_ruc(self, ruc: str) -> ClienteRead | None:
        stmt = select(ClienteModel).where(ClienteModel.ruc == ruc)
        row = self._db.scalars(stmt).first()
        if not row:
            return None
        return ClienteRead.model_validate(row)

    def create(self, payload: ClienteCreate) -> ClienteRead:
        row = ClienteModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return ClienteRead.model_validate(row)
