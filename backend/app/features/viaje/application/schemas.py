from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ViajeBase(BaseModel):
    id_tracto: int
    id_carreta: int
    id_conductor_unidad: int
    id_direccion_origen: int
    id_direccion_destino: int
    fecha_programado: datetime
    id_cliente: int
    estado_viaje: bool = True


class ViajeCreate(ViajeBase):
    pass


class ViajeRead(ViajeBase):
    id_viaje: int
    model_config = ConfigDict(from_attributes=True)
