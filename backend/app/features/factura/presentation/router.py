from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.factura.application.schemas import FacturaCreate, FacturaRead
from app.features.factura.application.use_cases import FacturaUseCases
from app.features.factura.infrastructure.sql_repository import FacturaSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> FacturaUseCases:
    return FacturaUseCases(repository=FacturaSqlRepository(db))


@router.get("/facturas", response_model=list[FacturaRead])
def list_facturas(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: FacturaUseCases = Depends(get_use_cases),
) -> list[FacturaRead]:
    return use_cases.list_facturas(limit=limit, offset=offset)


@router.get("/facturas/{id_factura}", response_model=FacturaRead)
def get_factura(id_factura: int, use_cases: FacturaUseCases = Depends(get_use_cases)) -> FacturaRead:
    return use_cases.get_factura(id_factura)


@router.post("/facturas", response_model=FacturaRead, status_code=201)
def create_factura(payload: FacturaCreate, use_cases: FacturaUseCases = Depends(get_use_cases)) -> FacturaRead:
    return use_cases.create_factura(payload)
