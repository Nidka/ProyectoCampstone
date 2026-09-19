from __future__ import annotations
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.features.auth.domain.repositories import IUsuarioRepository
from app.features.auth.application.schemas import TokenResponse, UsuarioOut
from app.shared.exceptions import ConflictError, NotFoundError

SECRET_KEY = "lizar-srl-fleet-manager-secret-2025"
ALGORITHM  = "HS256"
TOKEN_EXP_MINUTES = 60 * 8  # 8 horas


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def _create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXP_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


class RegisterUseCase:
    def __init__(self, repo: IUsuarioRepository) -> None:
        self._repo = repo

    def execute(self, username: str, email: str, password: str, nombre: str, rol: str) -> UsuarioOut:
        if self._repo.get_by_username(username):
            raise ConflictError(f"El usuario '{username}' ya existe")
        if self._repo.get_by_email(email):
            raise ConflictError(f"El email '{email}' ya está registrado")
        user = self._repo.create(
            username=username,
            email=email,
            hashed_password=_hash(password),
            nombre=nombre,
            rol=rol,
        )
        return UsuarioOut.model_validate(user)


class LoginUseCase:
    def __init__(self, repo: IUsuarioRepository) -> None:
        self._repo = repo

    def execute(self, username: str, password: str) -> TokenResponse:
        user = self._repo.get_by_username(username)
        if not user or not _verify(password, user.hashed_password):
            raise NotFoundError("Credenciales inválidas")
        if not user.estado:
            raise NotFoundError("Usuario inactivo")
        token = _create_token({"sub": user.username, "rol": user.rol, "id": user.id_usuario})
        return TokenResponse(access_token=token, usuario=UsuarioOut.model_validate(user))


class SeedAdminUseCase:
    """Crea un admin por defecto si no existe ningún usuario."""
    def __init__(self, repo: IUsuarioRepository) -> None:
        self._repo = repo

    def execute(self) -> None:
        if self._repo.count() == 0:
            self._repo.create(
                username="admin",
                email="admin@lizar.pe",
                hashed_password=_hash("admin123"),
                nombre="Administrador",
                rol="admin",
            )
