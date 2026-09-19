from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.tipo_gasto.application.schemas import TipoGastoCreate, TipoGastoRead
from app.features.tipo_gasto.application.use_cases import TipoGastoUseCases
from app.features.tipo_gasto.infrastructure.sql_repository import TipoGastoSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> TipoGastoUseCases:
    return TipoGastoUseCases(repository=TipoGastoSqlRepository(db))


@router.get("/tipos-gasto", response_model=list[TipoGastoRead])
def list_tipos_gasto(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: TipoGastoUseCases = Depends(get_use_cases),
) -> list[TipoGastoRead]:
    return use_cases.list_tipos_gasto(limit=limit, offset=offset)


@router.get("/tipos-gasto/{id_tipo_gasto}", response_model=TipoGastoRead)
def get_tipo_gasto(id_tipo_gasto: int, use_cases: TipoGastoUseCases = Depends(get_use_cases)) -> TipoGastoRead:
    return use_cases.get_tipo_gasto(id_tipo_gasto)


@router.post("/tipos-gasto", response_model=TipoGastoRead, status_code=201)
def create_tipo_gasto(payload: TipoGastoCreate, use_cases: TipoGastoUseCases = Depends(get_use_cases)) -> TipoGastoRead:
    return use_cases.create_tipo_gasto(payload)
