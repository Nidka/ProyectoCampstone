from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.viaje_realizado.application.schemas import ViajeRealizadoCreate, ViajeRealizadoRead
from app.features.viaje_realizado.domain.repositories import ViajeRealizadoRepository
from app.infrastructure.db.models import ViajeRealizadoModel


class ViajeRealizadoSqlRepository(ViajeRealizadoRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, limit: int, offset: int) -> list[ViajeRealizadoRead]:
        stmt = select(ViajeRealizadoModel).offset(offset).limit(limit).order_by(ViajeRealizadoModel.id_viaje_realizado)
        rows = self._db.scalars(stmt).all()
        return [ViajeRealizadoRead.model_validate(row) for row in rows]

    def get_by_id(self, id_viaje_realizado: int) -> ViajeRealizadoRead | None:
        row = self._db.get(ViajeRealizadoModel, id_viaje_realizado)
        if not row:
            return None
        return ViajeRealizadoRead.model_validate(row)

    def create(self, payload: ViajeRealizadoCreate) -> ViajeRealizadoRead:
        row = ViajeRealizadoModel(**payload.model_dump())
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return ViajeRealizadoRead.model_validate(row)
