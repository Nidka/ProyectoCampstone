from __future__ import annotations
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DetallePresupuestoBase(BaseModel):
    id_presupuesto: int
    id_tipo_gasto: int
    monto_estimado: Decimal
    estado_detallepresupuesto: bool | None = True


class DetallePresupuestoCreate(DetallePresupuestoBase):
    pass


class DetallePresupuestoRead(DetallePresupuestoBase):
    id_detalle_presupuesto: int
    model_config = ConfigDict(from_attributes=True)
