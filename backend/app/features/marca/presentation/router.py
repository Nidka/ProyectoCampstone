from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.marca.application.schemas import MarcaCreate, MarcaRead
from app.features.marca.application.use_cases import MarcaUseCases
from app.features.marca.infrastructure.sql_repository import MarcaSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> MarcaUseCases:
    return MarcaUseCases(repository=MarcaSqlRepository(db))


@router.get("/marcas", response_model=list[MarcaRead])
def list_marcas(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: MarcaUseCases = Depends(get_use_cases),
) -> list[MarcaRead]:
    return use_cases.list_marcas(limit=limit, offset=offset)


@router.get("/marcas/{id_marca}", response_model=MarcaRead)
def get_marca(id_marca: int, use_cases: MarcaUseCases = Depends(get_use_cases)) -> MarcaRead:
    return use_cases.get_marca(id_marca)


@router.post("/marcas", response_model=MarcaRead, status_code=201)
def create_marca(payload: MarcaCreate, use_cases: MarcaUseCases = Depends(get_use_cases)) -> MarcaRead:
    return use_cases.create_marca(payload)
