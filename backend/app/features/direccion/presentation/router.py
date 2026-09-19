from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.direccion.application.schemas import DireccionCreate, DireccionRead
from app.features.direccion.application.use_cases import DireccionUseCases
from app.features.direccion.infrastructure.sql_repository import DireccionSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> DireccionUseCases:
    return DireccionUseCases(repository=DireccionSqlRepository(db))


@router.get("/direcciones", response_model=list[DireccionRead])
def list_direcciones(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: DireccionUseCases = Depends(get_use_cases),
) -> list[DireccionRead]:
    return use_cases.list_direcciones(limit=limit, offset=offset)


@router.get("/direcciones/{id_direccion}", response_model=DireccionRead)
def get_direccion(id_direccion: int, use_cases: DireccionUseCases = Depends(get_use_cases)) -> DireccionRead:
    return use_cases.get_direccion(id_direccion)


@router.post("/direcciones", response_model=DireccionRead, status_code=201)
def create_direccion(payload: DireccionCreate, use_cases: DireccionUseCases = Depends(get_use_cases)) -> DireccionRead:
    return use_cases.create_direccion(payload)
