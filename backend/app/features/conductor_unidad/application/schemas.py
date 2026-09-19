from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConductorUnidadBase(BaseModel):
    id_conductor: int
    id_unidad: int
    fecha_asignacion: datetime
    fecha_fin: datetime | None = None
    estado_asignacion: bool = True


class ConductorUnidadCreate(ConductorUnidadBase):
    pass


class ConductorUnidadRead(ConductorUnidadBase):
    id_conductor_unidad: int
    model_config = ConfigDict(from_attributes=True)
