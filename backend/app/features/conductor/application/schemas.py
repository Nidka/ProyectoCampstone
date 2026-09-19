from __future__ import annotations
from datetime import date

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ConductorBase(BaseModel):
    dni: str = Field(min_length=8, max_length=8)
    nombre1: str = Field(max_length=50)
    nombre2: str | None = Field(default=None, max_length=50)
    apellido1: str = Field(max_length=50)
    apellido2: str | None = Field(default=None, max_length=50)
    licencia_conducir: str = Field(max_length=20)
    telefono: str | None = Field(default=None, max_length=20)
    correo: EmailStr | None = None
    direccion: str | None = Field(default=None, max_length=200)
    fecha_nacimiento: date | None = None
    estado_conductor: bool = True


class ConductorCreate(ConductorBase):
    pass


class ConductorRead(ConductorBase):
    id_conductor: int
    model_config = ConfigDict(from_attributes=True)
