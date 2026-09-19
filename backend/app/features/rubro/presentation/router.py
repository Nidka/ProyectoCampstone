from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.rubro.application.schemas import RubroCreate, RubroRead
from app.features.rubro.application.use_cases import RubroUseCases
from app.features.rubro.infrastructure.sql_repository import RubroSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> RubroUseCases:
    return RubroUseCases(repository=RubroSqlRepository(db))


@router.get("/rubros", response_model=list[RubroRead])
def list_rubros(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: RubroUseCases = Depends(get_use_cases),
) -> list[RubroRead]:
    return use_cases.list_rubros(limit=limit, offset=offset)


@router.get("/rubros/{id_rubro}", response_model=RubroRead)
def get_rubro(id_rubro: int, use_cases: RubroUseCases = Depends(get_use_cases)) -> RubroRead:
    return use_cases.get_rubro(id_rubro)


@router.post("/rubros", response_model=RubroRead, status_code=201)
def create_rubro(payload: RubroCreate, use_cases: RubroUseCases = Depends(get_use_cases)) -> RubroRead:
    return use_cases.create_rubro(payload)
