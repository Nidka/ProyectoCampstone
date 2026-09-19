from __future__ import annotations
from typing import Protocol

from app.features.cliente.application.schemas import ClienteCreate, ClienteRead


class ClienteRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[ClienteRead]:
        ...

    def get_by_id(self, id_cliente: int) -> ClienteRead | None:
        ...

    def get_by_ruc(self, ruc: str) -> ClienteRead | None:
        ...

    def create(self, payload: ClienteCreate) -> ClienteRead:
        ...
