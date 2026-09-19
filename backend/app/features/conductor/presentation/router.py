from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.conductor.application.schemas import ConductorCreate, ConductorRead
from app.features.conductor.application.use_cases import ConductorUseCases
from app.features.conductor.infrastructure.sql_repository import ConductorSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> ConductorUseCases:
    return ConductorUseCases(repository=ConductorSqlRepository(db))


@router.get("/conductores", response_model=list[ConductorRead])
def list_conductores(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: ConductorUseCases = Depends(get_use_cases),
) -> list[ConductorRead]:
    return use_cases.list_conductores(limit=limit, offset=offset)


@router.get("/conductores/{id_conductor}", response_model=ConductorRead)
def get_conductor(id_conductor: int, use_cases: ConductorUseCases = Depends(get_use_cases)) -> ConductorRead:
    return use_cases.get_conductor(id_conductor)


@router.post("/conductores", response_model=ConductorRead, status_code=201)
def create_conductor(payload: ConductorCreate, use_cases: ConductorUseCases = Depends(get_use_cases)) -> ConductorRead:
    return use_cases.create_conductor(payload)
