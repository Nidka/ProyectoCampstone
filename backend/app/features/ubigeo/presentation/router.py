from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.ubigeo.application.schemas import UbigeoCreate, UbigeoRead
from app.features.ubigeo.application.use_cases import UbigeoUseCases
from app.features.ubigeo.infrastructure.sql_repository import UbigeoSqlRepository
from app.shared.exceptions import ConflictError, NotFoundError

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> UbigeoUseCases:
    return UbigeoUseCases(repository=UbigeoSqlRepository(db))


@router.get("/ubigeos", response_model=list[UbigeoRead])
def list_ubigeos(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: UbigeoUseCases = Depends(get_use_cases),
) -> list[UbigeoRead]:
    return use_cases.list_ubigeos(limit=limit, offset=offset)


@router.get("/ubigeos/{codigo_ubigeo}", response_model=UbigeoRead)
def get_ubigeo(codigo_ubigeo: int, use_cases: UbigeoUseCases = Depends(get_use_cases)) -> UbigeoRead:
    try:
        return use_cases.get_ubigeo(codigo_ubigeo)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/ubigeos", response_model=UbigeoRead, status_code=status.HTTP_201_CREATED)
def create_ubigeo(payload: UbigeoCreate, use_cases: UbigeoUseCases = Depends(get_use_cases)) -> UbigeoRead:
    try:
        return use_cases.create_ubigeo(payload)
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
