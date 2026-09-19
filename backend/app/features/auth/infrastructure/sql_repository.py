from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.features.auth.domain.repositories import IUsuarioRepository
from app.infrastructure.db.models import UsuarioModel


class SqlUsuarioRepository(IUsuarioRepository):

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_username(self, username: str) -> Optional[UsuarioModel]:
        return self._db.query(UsuarioModel).filter(UsuarioModel.username == username).first()

    def get_by_email(self, email: str) -> Optional[UsuarioModel]:
        return self._db.query(UsuarioModel).filter(UsuarioModel.email == email).first()

    def create(self, username: str, email: str, hashed_password: str, nombre: str, rol: str) -> UsuarioModel:
        user = UsuarioModel(
            username=username,
            email=email,
            hashed_password=hashed_password,
            nombre=nombre,
            rol=rol,
            estado=True,
            created_at=datetime.now(timezone.utc),
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def count(self) -> int:
        return self._db.query(UsuarioModel).count()
