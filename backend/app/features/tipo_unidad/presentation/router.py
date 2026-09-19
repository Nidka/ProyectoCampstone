from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.tipo_unidad.application.schemas import TipoUnidadCreate, TipoUnidadRead
from app.features.tipo_unidad.application.use_cases import TipoUnidadUseCases
from app.features.tipo_unidad.infrastructure.sql_repository import TipoUnidadSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> TipoUnidadUseCases:
    return TipoUnidadUseCases(repository=TipoUnidadSqlRepository(db))


@router.get("/tipos-unidad", response_model=list[TipoUnidadRead])
def list_tipos_unidad(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: TipoUnidadUseCases = Depends(get_use_cases),
) -> list[TipoUnidadRead]:
    return use_cases.list_tipos_unidad(limit=limit, offset=offset)


@router.get("/tipos-unidad/{id_tipo_unidad}", response_model=TipoUnidadRead)
def get_tipo_unidad(id_tipo_unidad: int, use_cases: TipoUnidadUseCases = Depends(get_use_cases)) -> TipoUnidadRead:
    return use_cases.get_tipo_unidad(id_tipo_unidad)


@router.post("/tipos-unidad", response_model=TipoUnidadRead, status_code=201)
def create_tipo_unidad(payload: TipoUnidadCreate, use_cases: TipoUnidadUseCases = Depends(get_use_cases)) -> TipoUnidadRead:
    return use_cases.create_tipo_unidad(payload)
