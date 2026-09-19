from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.detalle_presupuesto.application.schemas import DetallePresupuestoCreate, DetallePresupuestoRead
from app.features.detalle_presupuesto.application.use_cases import DetallePresupuestoUseCases
from app.features.detalle_presupuesto.infrastructure.sql_repository import DetallePresupuestoSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> DetallePresupuestoUseCases:
    return DetallePresupuestoUseCases(repository=DetallePresupuestoSqlRepository(db))


@router.get("/detalles-presupuesto", response_model=list[DetallePresupuestoRead])
def list_detalles(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: DetallePresupuestoUseCases = Depends(get_use_cases),
) -> list[DetallePresupuestoRead]:
    return use_cases.list_detalles(limit=limit, offset=offset)


@router.get("/detalles-presupuesto/{id_detalle_presupuesto}", response_model=DetallePresupuestoRead)
def get_detalle(
    id_detalle_presupuesto: int,
    use_cases: DetallePresupuestoUseCases = Depends(get_use_cases),
) -> DetallePresupuestoRead:
    return use_cases.get_detalle(id_detalle_presupuesto)


@router.post("/detalles-presupuesto", response_model=DetallePresupuestoRead, status_code=201)
def create_detalle(
    payload: DetallePresupuestoCreate,
    use_cases: DetallePresupuestoUseCases = Depends(get_use_cases),
) -> DetallePresupuestoRead:
    return use_cases.create_detalle(payload)
