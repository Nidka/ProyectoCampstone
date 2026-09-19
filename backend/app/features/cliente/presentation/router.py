from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.cliente.application.schemas import ClienteCreate, ClienteRead
from app.features.cliente.application.use_cases import ClienteUseCases
from app.features.cliente.infrastructure.sql_repository import ClienteSqlRepository
from app.shared.exceptions import ConflictError, NotFoundError

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> ClienteUseCases:
    return ClienteUseCases(repository=ClienteSqlRepository(db))


@router.get("/clientes", response_model=list[ClienteRead])
def list_clientes(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: ClienteUseCases = Depends(get_use_cases),
) -> list[ClienteRead]:
    return use_cases.list_clientes(limit=limit, offset=offset)


@router.get("/clientes/{id_cliente}", response_model=ClienteRead)
def get_cliente(id_cliente: int, use_cases: ClienteUseCases = Depends(get_use_cases)) -> ClienteRead:
    try:
        return use_cases.get_cliente(id_cliente)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/clientes", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
def create_cliente(payload: ClienteCreate, use_cases: ClienteUseCases = Depends(get_use_cases)) -> ClienteRead:
    try:
        return use_cases.create_cliente(payload)
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
