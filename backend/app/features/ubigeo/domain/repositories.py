from __future__ import annotations
from typing import Protocol

from app.features.ubigeo.application.schemas import UbigeoCreate, UbigeoRead


class UbigeoRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[UbigeoRead]:
        ...

    def get_by_codigo(self, codigo_ubigeo: int) -> UbigeoRead | None:
        ...

    def create(self, payload: UbigeoCreate) -> UbigeoRead:
        ...
