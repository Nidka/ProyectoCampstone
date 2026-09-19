from __future__ import annotations
from typing import Protocol

from app.features.direccion.application.schemas import DireccionCreate, DireccionRead


class DireccionRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[DireccionRead]:
        ...

    def get_by_id(self, id_direccion: int) -> DireccionRead | None:
        ...

    def create(self, payload: DireccionCreate) -> DireccionRead:
        ...
