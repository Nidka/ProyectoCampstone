from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from app.infrastructure.db.models import UsuarioModel


class IUsuarioRepository(ABC):

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UsuarioModel]: ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UsuarioModel]: ...

    @abstractmethod
    def create(self, username: str, email: str, hashed_password: str, nombre: str, rol: str) -> UsuarioModel: ...

    @abstractmethod
    def count(self) -> int: ...
