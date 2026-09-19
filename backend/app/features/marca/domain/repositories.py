from __future__ import annotations
from typing import Protocol

from app.features.marca.application.schemas import MarcaCreate, MarcaRead


class MarcaRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[MarcaRead]:
        ...

    def get_by_id(self, id_marca: int) -> MarcaRead | None:
        ...

    def get_by_nombre(self, nombre: str) -> MarcaRead | None:
        ...

    def create(self, payload: MarcaCreate) -> MarcaRead:
        ...
