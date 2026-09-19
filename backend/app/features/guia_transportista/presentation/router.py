from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.guia_transportista.application.schemas import GuiaTransportistaCreate, GuiaTransportistaRead
from app.features.guia_transportista.application.use_cases import GuiaTransportistaUseCases
from app.features.guia_transportista.infrastructure.sql_repository import GuiaTransportistaSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> GuiaTransportistaUseCases:
    return GuiaTransportistaUseCases(repository=GuiaTransportistaSqlRepository(db))


@router.get("/guias-transportista", response_model=list[GuiaTransportistaRead])
def list_guias(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: GuiaTransportistaUseCases = Depends(get_use_cases),
) -> list[GuiaTransportistaRead]:
    return use_cases.list_guias(limit=limit, offset=offset)


@router.get("/guias-transportista/{id_guia_transportista}", response_model=GuiaTransportistaRead)
def get_guia(
    id_guia_transportista: int,
    use_cases: GuiaTransportistaUseCases = Depends(get_use_cases),
) -> GuiaTransportistaRead:
    return use_cases.get_guia(id_guia_transportista)


@router.post("/guias-transportista", response_model=GuiaTransportistaRead, status_code=201)
def create_guia(
    payload: GuiaTransportistaCreate,
    use_cases: GuiaTransportistaUseCases = Depends(get_use_cases),
) -> GuiaTransportistaRead:
    return use_cases.create_guia(payload)
