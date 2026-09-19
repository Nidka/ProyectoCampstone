from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.unidad.application.schemas import UnidadCreate, UnidadRead
from app.features.unidad.application.use_cases import UnidadUseCases
from app.features.unidad.infrastructure.sql_repository import UnidadSqlRepository
from app.shared.exceptions import ConflictError, NotFoundError

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> UnidadUseCases:
    return UnidadUseCases(repository=UnidadSqlRepository(db))


@router.get("/unidades", response_model=list[UnidadRead])
def list_unidades(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: UnidadUseCases = Depends(get_use_cases),
) -> list[UnidadRead]:
    return use_cases.list_unidades(limit=limit, offset=offset)


@router.get("/unidades/{id_unidad}", response_model=UnidadRead)
def get_unidad(id_unidad: int, use_cases: UnidadUseCases = Depends(get_use_cases)) -> UnidadRead:
    try:
        return use_cases.get_unidad(id_unidad)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/unidades", response_model=UnidadRead, status_code=status.HTTP_201_CREATED)
def create_unidad(payload: UnidadCreate, use_cases: UnidadUseCases = Depends(get_use_cases)) -> UnidadRead:
    try:
        return use_cases.create_unidad(payload)
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
