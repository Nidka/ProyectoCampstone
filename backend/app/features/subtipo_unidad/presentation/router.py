from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.subtipo_unidad.application.schemas import SubtipoUnidadCreate, SubtipoUnidadRead
from app.features.subtipo_unidad.application.use_cases import SubtipoUnidadUseCases
from app.features.subtipo_unidad.infrastructure.sql_repository import SubtipoUnidadSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> SubtipoUnidadUseCases:
    return SubtipoUnidadUseCases(repository=SubtipoUnidadSqlRepository(db))


@router.get("/subtipos-unidad", response_model=list[SubtipoUnidadRead])
def list_subtipos(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: SubtipoUnidadUseCases = Depends(get_use_cases),
) -> list[SubtipoUnidadRead]:
    return use_cases.list_subtipos(limit=limit, offset=offset)


@router.get("/subtipos-unidad/{id_subtipo_unidad}", response_model=SubtipoUnidadRead)
def get_subtipo(id_subtipo_unidad: int, use_cases: SubtipoUnidadUseCases = Depends(get_use_cases)) -> SubtipoUnidadRead:
    return use_cases.get_subtipo(id_subtipo_unidad)


@router.post("/subtipos-unidad", response_model=SubtipoUnidadRead, status_code=201)
def create_subtipo(payload: SubtipoUnidadCreate, use_cases: SubtipoUnidadUseCases = Depends(get_use_cases)) -> SubtipoUnidadRead:
    return use_cases.create_subtipo(payload)
