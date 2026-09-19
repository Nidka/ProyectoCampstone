from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import engine
from app.core.exception_handlers import register_exception_handlers
from app.features.advanced_crud.presentation.router import router as advanced_crud_router
from app.features.auth.presentation.router import router as auth_router
from app.features.cliente.presentation.router import router as cliente_router
from app.features.conductor.presentation.router import router as conductor_router
from app.features.conductor_unidad.presentation.router import router as conductor_unidad_router
from app.features.detalle_presupuesto.presentation.router import router as detalle_presupuesto_router
from app.features.direccion.presentation.router import router as direccion_router
from app.features.factura.presentation.router import router as factura_router
from app.features.guia_transportista.presentation.router import router as guia_transportista_router
from app.features.marca.presentation.router import router as marca_router
from app.features.presupuesto_viaje.presentation.router import router as presupuesto_viaje_router
from app.features.producto_categoria.presentation.router import router as producto_categoria_router
from app.features.producto_transportado.presentation.router import router as producto_transportado_router
from app.features.rubro.presentation.router import router as rubro_router
from app.features.subtipo_unidad.presentation.router import router as subtipo_unidad_router
from app.features.tipo_gasto.presentation.router import router as tipo_gasto_router
from app.features.tipo_unidad.presentation.router import router as tipo_unidad_router
from app.features.ubigeo.presentation.router import router as ubigeo_router
from app.features.unidad.presentation.router import router as unidad_router
from app.features.viaje.presentation.router import router as viaje_router
from app.features.viaje_realizado.presentation.router import router as viaje_realizado_router
from app.infrastructure.db.models import Base

settings = get_settings()

# Crear tablas automáticamente al arrancar (incluyendo usuario)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, debug=settings.app_debug)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def seed_admin() -> None:
    from app.core.database import SessionLocal
    from app.features.auth.application.use_cases import SeedAdminUseCase
    from app.features.auth.infrastructure.sql_repository import SqlUsuarioRepository
    db = SessionLocal()
    try:
        SeedAdminUseCase(SqlUsuarioRepository(db)).execute()
    finally:
        db.close()


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.app_env}


# Auth (sin protección — son los endpoints de login/register)
app.include_router(auth_router, prefix="/api/v1")

# Resto de módulos
app.include_router(ubigeo_router,              prefix="/api/v1", tags=["ubigeos"])
app.include_router(advanced_crud_router,       prefix="/api/v1", tags=["advanced-crud"])
app.include_router(rubro_router,               prefix="/api/v1", tags=["rubros"])
app.include_router(marca_router,               prefix="/api/v1", tags=["marcas"])
app.include_router(tipo_unidad_router,         prefix="/api/v1", tags=["tipos-unidad"])
app.include_router(tipo_gasto_router,          prefix="/api/v1", tags=["tipos-gasto"])
app.include_router(producto_categoria_router,  prefix="/api/v1", tags=["categorias-producto"])
app.include_router(direccion_router,           prefix="/api/v1", tags=["direcciones"])
app.include_router(subtipo_unidad_router,      prefix="/api/v1", tags=["subtipos-unidad"])
app.include_router(conductor_router,           prefix="/api/v1", tags=["conductores"])
app.include_router(cliente_router,             prefix="/api/v1", tags=["clientes"])
app.include_router(unidad_router,              prefix="/api/v1", tags=["unidades"])
app.include_router(conductor_unidad_router,    prefix="/api/v1", tags=["asignaciones-conductor-unidad"])
app.include_router(viaje_router,               prefix="/api/v1", tags=["viajes"])
app.include_router(guia_transportista_router,  prefix="/api/v1", tags=["guias-transportista"])
app.include_router(viaje_realizado_router,     prefix="/api/v1", tags=["viajes-realizados"])
app.include_router(factura_router,             prefix="/api/v1", tags=["facturas"])
app.include_router(presupuesto_viaje_router,   prefix="/api/v1", tags=["presupuestos-viaje"])
app.include_router(detalle_presupuesto_router, prefix="/api/v1", tags=["detalles-presupuesto"])
app.include_router(producto_transportado_router, prefix="/api/v1", tags=["productos-transportados"])
