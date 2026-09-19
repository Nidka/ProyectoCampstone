from __future__ import annotations
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PresupuestoViajeBase(BaseModel):
    id_viaje: int
    monto_total: Decimal
    fecha_registro: datetime
    estado_presupuesto: bool = True


class PresupuestoViajeCreate(PresupuestoViajeBase):
    pass


class PresupuestoViajeRead(PresupuestoViajeBase):
    id_presupuesto: int
    model_config = ConfigDict(from_attributes=True)
