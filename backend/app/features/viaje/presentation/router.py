from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.viaje.application.schemas import ViajeCreate, ViajeRead
from app.features.viaje.application.use_cases import ViajeUseCases
from app.features.viaje.infrastructure.sql_repository import ViajeSqlRepository
from app.shared.exceptions import NotFoundError

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> ViajeUseCases:
    return ViajeUseCases(repository=ViajeSqlRepository(db))


@router.get("/viajes", response_model=list[ViajeRead])
def list_viajes(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: ViajeUseCases = Depends(get_use_cases),
) -> list[ViajeRead]:
    return use_cases.list_viajes(limit=limit, offset=offset)


@router.get("/viajes/{id_viaje}", response_model=ViajeRead)
def get_viaje(id_viaje: int, use_cases: ViajeUseCases = Depends(get_use_cases)) -> ViajeRead:
    try:
        return use_cases.get_viaje(id_viaje)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/viajes", response_model=ViajeRead, status_code=status.HTTP_201_CREATED)
def create_viaje(payload: ViajeCreate, use_cases: ViajeUseCases = Depends(get_use_cases)) -> ViajeRead:
    return use_cases.create_viaje(payload)
