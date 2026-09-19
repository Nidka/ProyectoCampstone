from __future__ import annotations
from typing import Protocol

from app.features.guia_transportista.application.schemas import GuiaTransportistaCreate, GuiaTransportistaRead


class GuiaTransportistaRepository(Protocol):
    def list(self, limit: int, offset: int) -> list[GuiaTransportistaRead]:
        ...

    def get_by_id(self, id_guia_transportista: int) -> GuiaTransportistaRead | None:
        ...

    def get_by_numero(self, numero_guia: str) -> GuiaTransportistaRead | None:
        ...

    def create(self, payload: GuiaTransportistaCreate) -> GuiaTransportistaRead:
        ...
