from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import String, asc, cast, desc, or_, select
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.features.cliente.application.schemas import ClienteCreate, ClienteRead
from app.features.conductor.application.schemas import ConductorCreate, ConductorRead
from app.features.conductor_unidad.application.schemas import ConductorUnidadCreate, ConductorUnidadRead
from app.features.detalle_presupuesto.application.schemas import DetallePresupuestoCreate, DetallePresupuestoRead
from app.features.direccion.application.schemas import DireccionCreate, DireccionRead
from app.features.factura.application.schemas import FacturaCreate, FacturaRead
from app.features.guia_transportista.application.schemas import GuiaTransportistaCreate, GuiaTransportistaRead
from app.features.marca.application.schemas import MarcaCreate, MarcaRead
from app.features.presupuesto_viaje.application.schemas import PresupuestoViajeCreate, PresupuestoViajeRead
from app.features.producto_categoria.application.schemas import ProductoCategoriaCreate, ProductoCategoriaRead
from app.features.producto_transportado.application.schemas import ProductoTransportadoCreate, ProductoTransportadoRead
from app.features.rubro.application.schemas import RubroCreate, RubroRead
from app.features.subtipo_unidad.application.schemas import SubtipoUnidadCreate, SubtipoUnidadRead
from app.features.tipo_gasto.application.schemas import TipoGastoCreate, TipoGastoRead
from app.features.tipo_unidad.application.schemas import TipoUnidadCreate, TipoUnidadRead
from app.features.ubigeo.application.schemas import UbigeoCreate, UbigeoRead
from app.features.unidad.application.schemas import UnidadCreate, UnidadRead
from app.features.viaje.application.schemas import ViajeCreate, ViajeRead
from app.features.viaje_realizado.application.schemas import ViajeRealizadoCreate, ViajeRealizadoRead
from app.infrastructure.db.models import (
    ClienteModel,
    ConductorModel,
    ConductorUnidadModel,
    DetallePresupuestoModel,
    DireccionModel,
    FacturaModel,
    GuiaTransportistaModel,
    MarcaModel,
    PresupuestoViajeModel,
    ProductoCategoriaModel,
    ProductoTransportadoModel,
    ProgramacionViajeModel,
    RubroModel,
    SubtipoUnidadModel,
    TipoGastoModel,
    TipoUnidadModel,
    UbigeoModel,
    UnidadModel,
    ViajeRealizadoModel,
)

router = APIRouter()


@dataclass
class ResourceConfig:
    path: str
    id_field: str
    model: Any
    read_schema: type[BaseModel]
    write_schema: type[BaseModel]
    search_fields: list[str]


def _parse_filters(filters: str | None) -> dict[str, str]:
    if not filters:
        return {}
    result: dict[str, str] = {}
    parts = [part.strip() for part in filters.split(",") if part.strip()]
    for part in parts:
        if ":" not in part:
            continue
        key, value = part.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def _build_routes(config: ResourceConfig) -> None:
    async def list_advanced(
        limit: int = Query(default=50, ge=1, le=200),
        offset: int = Query(default=0, ge=0),
        search: str | None = Query(default=None),
        search_fields: str | None = Query(default=None),
        order_by: str | None = Query(default=None),
        order_dir: str = Query(default="asc", pattern="^(asc|desc)$"),
        filters: str | None = Query(default=None),
        db: Session = Depends(get_db_session),
    ) -> list[BaseModel]:
        stmt = select(config.model)

        if search:
            fields_to_use = config.search_fields
            if search_fields:
                requested = [f.strip() for f in search_fields.split(",") if f.strip()]
                fields_to_use = [f for f in requested if hasattr(config.model, f)]

            if fields_to_use:
                stmt = stmt.where(
                    or_(*[cast(getattr(config.model, field), String).ilike(f"%{search}%") for field in fields_to_use])
                )

        for key, value in _parse_filters(filters).items():
            if hasattr(config.model, key):
                stmt = stmt.where(cast(getattr(config.model, key), String) == value)

        order_column_name = order_by if order_by and hasattr(config.model, order_by) else config.id_field
        order_column = getattr(config.model, order_column_name)
        stmt = stmt.order_by(desc(order_column) if order_dir == "desc" else asc(order_column))

        rows = db.scalars(stmt.offset(offset).limit(limit)).all()
        return [config.read_schema.model_validate(row) for row in rows]

    async def update_item(
        item_id: int,
        payload: dict[str, Any],
        db: Session = Depends(get_db_session),
    ) -> BaseModel:
        row = db.get(config.model, item_id)
        if not row:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")

        for key, value in payload.items():
            if hasattr(row, key):
                setattr(row, key, value)

        db.add(row)
        db.commit()
        db.refresh(row)
        return config.read_schema.model_validate(row)

    async def delete_item(item_id: int, db: Session = Depends(get_db_session)) -> dict[str, Any]:
        row = db.get(config.model, item_id)
        if not row:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")

        db.delete(row)
        db.commit()
        return {"deleted": True, config.id_field: item_id}

    list_advanced.__name__ = f"list_advanced_{config.path.replace('-', '_')}"
    update_item.__name__ = f"update_{config.path.replace('-', '_')}"
    delete_item.__name__ = f"delete_{config.path.replace('-', '_')}"

    router.add_api_route(
        f"/advanced/{config.path}",
        list_advanced,
        methods=["GET"],
        response_model=list[config.read_schema],
    )
    router.add_api_route(
        f"/{config.path}/{{item_id}}",
        update_item,
        methods=["PUT"],
        response_model=config.read_schema,
    )
    router.add_api_route(
        f"/{config.path}/{{item_id}}",
        delete_item,
        methods=["DELETE"],
        response_model=dict,
    )


RESOURCE_CONFIGS = [
    ResourceConfig("ubigeos", "codigo_ubigeo", UbigeoModel, UbigeoRead, UbigeoCreate, ["provincia", "distrito", "departamento"]),
    ResourceConfig("rubros", "id_rubro", RubroModel, RubroRead, RubroCreate, ["nombre", "descripcion"]),
    ResourceConfig("marcas", "id_marca", MarcaModel, MarcaRead, MarcaCreate, ["nombre", "pais_origen", "descripcion"]),
    ResourceConfig("tipos-unidad", "id_tipo_unidad", TipoUnidadModel, TipoUnidadRead, TipoUnidadCreate, ["nombre", "descripcion"]),
    ResourceConfig("tipos-gasto", "id_tipo_gasto", TipoGastoModel, TipoGastoRead, TipoGastoCreate, ["nombre", "descripcion"]),
    ResourceConfig("categorias-producto", "id_categoria", ProductoCategoriaModel, ProductoCategoriaRead, ProductoCategoriaCreate, ["nombre", "descripcion"]),
    ResourceConfig("direcciones", "id_direccion", DireccionModel, DireccionRead, DireccionCreate, ["direccion_detallada", "referencia", "descripcion"]),
    ResourceConfig("subtipos-unidad", "id_subtipo_unidad", SubtipoUnidadModel, SubtipoUnidadRead, SubtipoUnidadCreate, ["nombre", "descripcion"]),
    ResourceConfig("conductores", "id_conductor", ConductorModel, ConductorRead, ConductorCreate, ["dni", "nombre1", "apellido1", "licencia_conducir"]),
    ResourceConfig("clientes", "id_cliente", ClienteModel, ClienteRead, ClienteCreate, ["razon_social", "ruc", "contacto"]),
    ResourceConfig("unidades", "id_unidad", UnidadModel, UnidadRead, UnidadCreate, ["placa", "modelo"]),
    ResourceConfig("asignaciones-conductor-unidad", "id_conductor_unidad", ConductorUnidadModel, ConductorUnidadRead, ConductorUnidadCreate, []),
    ResourceConfig("viajes", "id_viaje", ProgramacionViajeModel, ViajeRead, ViajeCreate, []),
    ResourceConfig("guias-transportista", "id_guia_transportista", GuiaTransportistaModel, GuiaTransportistaRead, GuiaTransportistaCreate, ["numero_guia", "guias_remitente"]),
    ResourceConfig("viajes-realizados", "id_viaje_realizado", ViajeRealizadoModel, ViajeRealizadoRead, ViajeRealizadoCreate, ["observaciones"]),
    ResourceConfig("facturas", "id_factura", FacturaModel, FacturaRead, FacturaCreate, ["numero_factura"]),
    ResourceConfig("presupuestos-viaje", "id_presupuesto", PresupuestoViajeModel, PresupuestoViajeRead, PresupuestoViajeCreate, []),
    ResourceConfig("detalles-presupuesto", "id_detalle_presupuesto", DetallePresupuestoModel, DetallePresupuestoRead, DetallePresupuestoCreate, []),
    ResourceConfig("productos-transportados", "id_producto_transportado", ProductoTransportadoModel, ProductoTransportadoRead, ProductoTransportadoCreate, ["descripcion_producto"]),
]

for cfg in RESOURCE_CONFIGS:
    _build_routes(cfg)
