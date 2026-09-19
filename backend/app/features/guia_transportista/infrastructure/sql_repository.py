from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.guia_transportista.application.schemas import GuiaTransportistaCreate, GuiaTransportistaRead
from app.features.guia_transportista.domain.repositories import GuiaTransportistaRepository
from app.infrastructure.db.models import GuiaTransportistaModel


class GuiaTransportistaSqlRepository(GuiaTransportistaRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[GuiaTransportistaRead]:
        stmt = select(GuiaTransportistaModel).offset(offset).limit(limit).order_by(GuiaTransportistaModel.id_guia_transportista)
        rows = self._db.scalars(stmt).all()
        return [GuiaTransportistaRead.model_validate(row) for row in rows]

    def get_by_id(self, id_guia_transportista: int) -> GuiaTransportistaRead | None:
        row = self._db.get(GuiaTransportistaModel, id_guia_transportista)
        if not row:
            return None
        return GuiaTransportistaRead.model_validate(row)

    def get_by_numero(self, numero_guia: str) -> GuiaTransportistaRead | None:
        stmt = select(GuiaTransportistaModel).where(GuiaTransportistaModel.numero_guia == numero_guia)
        row = self._db.scalars(stmt).first()
        if not row:
            return None
        return GuiaTransportistaRead.model_validate(row)

    def create(self, payload: GuiaTransportistaCreate) -> GuiaTransportistaRead:
        row = GuiaTransportistaModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return GuiaTransportistaRead.model_validate(row)
