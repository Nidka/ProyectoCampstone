from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.producto_transportado.application.schemas import ProductoTransportadoCreate, ProductoTransportadoRead
from app.features.producto_transportado.application.use_cases import ProductoTransportadoUseCases
from app.features.producto_transportado.infrastructure.sql_repository import ProductoTransportadoSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> ProductoTransportadoUseCases:
    return ProductoTransportadoUseCases(repository=ProductoTransportadoSqlRepository(db))


@router.get("/productos-transportados", response_model=list[ProductoTransportadoRead])
def list_productos(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: ProductoTransportadoUseCases = Depends(get_use_cases),
) -> list[ProductoTransportadoRead]:
    return use_cases.list_productos(limit=limit, offset=offset)


@router.get("/productos-transportados/{id_producto_transportado}", response_model=ProductoTransportadoRead)
def get_producto(
    id_producto_transportado: int,
    use_cases: ProductoTransportadoUseCases = Depends(get_use_cases),
) -> ProductoTransportadoRead:
    return use_cases.get_producto(id_producto_transportado)


@router.post("/productos-transportados", response_model=ProductoTransportadoRead, status_code=201)
def create_producto(
    payload: ProductoTransportadoCreate,
    use_cases: ProductoTransportadoUseCases = Depends(get_use_cases),
) -> ProductoTransportadoRead:
    return use_cases.create_producto(payload)
