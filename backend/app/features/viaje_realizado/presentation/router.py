from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.viaje_realizado.application.schemas import ViajeRealizadoCreate, ViajeRealizadoRead
from app.features.viaje_realizado.application.use_cases import ViajeRealizadoUseCases
from app.features.viaje_realizado.infrastructure.sql_repository import ViajeRealizadoSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> ViajeRealizadoUseCases:
    return ViajeRealizadoUseCases(repository=ViajeRealizadoSqlRepository(db))


@router.get("/viajes-realizados", response_model=list[ViajeRealizadoRead])
def list_viajes_realizados(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: ViajeRealizadoUseCases = Depends(get_use_cases),
) -> list[ViajeRealizadoRead]:
    return use_cases.list_viajes_realizados(limit=limit, offset=offset)


@router.get("/viajes-realizados/{id_viaje_realizado}", response_model=ViajeRealizadoRead)
def get_viaje_realizado(
    id_viaje_realizado: int,
    use_cases: ViajeRealizadoUseCases = Depends(get_use_cases),
) -> ViajeRealizadoRead:
    return use_cases.get_viaje_realizado(id_viaje_realizado)


@router.post("/viajes-realizados", response_model=ViajeRealizadoRead, status_code=201)
def create_viaje_realizado(
    payload: ViajeRealizadoCreate,
    use_cases: ViajeRealizadoUseCases = Depends(get_use_cases),
) -> ViajeRealizadoRead:
    return use_cases.create_viaje_realizado(payload)
