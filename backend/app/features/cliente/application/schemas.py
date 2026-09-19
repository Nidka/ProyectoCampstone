from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ClienteBase(BaseModel):
    razon_social: str = Field(max_length=150)
    ruc: str = Field(min_length=11, max_length=11)
    telefono: str | None = Field(default=None, max_length=20)
    correo: EmailStr | None = None
    contacto: str | None = Field(default=None, max_length=100)
    id_rubro: int
    id_direccion_domicilio: int | None = None
    estado_cliente: bool = True


class ClienteCreate(ClienteBase):
    pass


class ClienteRead(ClienteBase):
    id_cliente: int
    model_config = ConfigDict(from_attributes=True)
