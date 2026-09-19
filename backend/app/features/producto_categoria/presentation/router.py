from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.producto_categoria.application.schemas import ProductoCategoriaCreate, ProductoCategoriaRead
from app.features.producto_categoria.application.use_cases import ProductoCategoriaUseCases
from app.features.producto_categoria.infrastructure.sql_repository import ProductoCategoriaSqlRepository

router = APIRouter()


def get_use_cases(db: Session = Depends(get_db_session)) -> ProductoCategoriaUseCases:
    return ProductoCategoriaUseCases(repository=ProductoCategoriaSqlRepository(db))


@router.get("/categorias-producto", response_model=list[ProductoCategoriaRead])
def list_categorias(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_cases: ProductoCategoriaUseCases = Depends(get_use_cases),
) -> list[ProductoCategoriaRead]:
    return use_cases.list_categorias(limit=limit, offset=offset)


@router.get("/categorias-producto/{id_categoria}", response_model=ProductoCategoriaRead)
def get_categoria(id_categoria: int, use_cases: ProductoCategoriaUseCases = Depends(get_use_cases)) -> ProductoCategoriaRead:
    return use_cases.get_categoria(id_categoria)


@router.post("/categorias-producto", response_model=ProductoCategoriaRead, status_code=201)
def create_categoria(payload: ProductoCategoriaCreate, use_cases: ProductoCategoriaUseCases = Depends(get_use_cases)) -> ProductoCategoriaRead:
    return use_cases.create_categoria(payload)
