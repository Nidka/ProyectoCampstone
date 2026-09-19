from __future__ import annotations
from pydantic import BaseModel, EmailStr, field_validator


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    nombre: str
    rol: str = "operador"

    @field_validator("rol")
    @classmethod
    def rol_valido(cls, v: str) -> str:
        if v not in ("admin", "operador"):
            raise ValueError("Rol debe ser 'admin' u 'operador'")
        return v


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut


class UsuarioOut(BaseModel):
    id_usuario: int
    username: str
    email: str
    nombre: str
    rol: str
    estado: bool

    model_config = {"from_attributes": True}


TokenResponse.model_rebuild()
