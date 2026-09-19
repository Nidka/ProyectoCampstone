from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.conductor_unidad.application.schemas import ConductorUnidadCreate, ConductorUnidadRead
from app.features.conductor_unidad.application.use_cases import ConductorUnidadUseCases
from app.features.conductor_unidad.infrastructure.sql_repository import ConductorUnidadSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> ConductorUnidadUseCases:
    return ConductorUnidadUseCases(repository=ConductorUnidadSqlRepository(db))


@router.get("/asignaciones-conductor-unidad", response_model=list[ConductorUnidadRead])
def list_asignaciones(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: ConductorUnidadUseCases = Depends(get_use_cases),
) -> list[ConductorUnidadRead]:
    return use_cases.list_asignaciones(limit=limit, offset=offset)


@router.get("/asignaciones-conductor-unidad/{id_conductor_unidad}", response_model=ConductorUnidadRead)
def get_asignacion(id_conductor_unidad: int, use_cases: ConductorUnidadUseCases = Depends(get_use_cases)) -> ConductorUnidadRead:
    return use_cases.get_asignacion(id_conductor_unidad)


@router.post("/asignaciones-conductor-unidad", response_model=ConductorUnidadRead, status_code=201)
def create_asignacion(
    payload: ConductorUnidadCreate,
    use_cases: ConductorUnidadUseCases = Depends(get_use_cases),
) -> ConductorUnidadRead:
    return use_cases.create_asignacion(payload)
