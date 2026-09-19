from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.presupuesto_viaje.application.schemas import PresupuestoViajeCreate, PresupuestoViajeRead
from app.features.presupuesto_viaje.application.use_cases import PresupuestoViajeUseCases
from app.features.presupuesto_viaje.infrastructure.sql_repository import PresupuestoViajeSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> PresupuestoViajeUseCases:
    return PresupuestoViajeUseCases(repository=PresupuestoViajeSqlRepository(db))


@router.get("/presupuestos-viaje", response_model=list[PresupuestoViajeRead])
def list_presupuestos(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: PresupuestoViajeUseCases = Depends(get_use_cases),
) -> list[PresupuestoViajeRead]:
    return use_cases.list_presupuestos(limit=limit, offset=offset)


@router.get("/presupuestos-viaje/{id_presupuesto}", response_model=PresupuestoViajeRead)
def get_presupuesto(
    id_presupuesto: int,
    use_cases: PresupuestoViajeUseCases = Depends(get_use_cases),
) -> PresupuestoViajeRead:
    return use_cases.get_presupuesto(id_presupuesto)


@router.post("/presupuestos-viaje", response_model=PresupuestoViajeRead, status_code=201)
def create_presupuesto(
    payload: PresupuestoViajeCreate,
    use_cases: PresupuestoViajeUseCases = Depends(get_use_cases),
) -> PresupuestoViajeRead:
    return use_cases.create_presupuesto(payload)
