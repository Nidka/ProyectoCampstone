from __future__ import annotations
from typing import Protocol

from app.features.rubro.application.schemas import RubroCreate, RubroRead


class RubroRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[RubroRead]:
        ...

    def get_by_id(self, id_rubro: int) -> RubroRead | None:
        ...

    def get_by_nombre(self, nombre: str) -> RubroRead | None:
        ...

    def create(self, payload: RubroCreate) -> RubroRead:
        ...
