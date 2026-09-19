from __future__ import annotations
from app.features.direccion.application.schemas import DireccionCreate, DireccionRead
from app.features.direccion.domain.repositories import DireccionRepository
from app.shared.exceptions import NotFoundError


class DireccionUseCases:
    def __init__(self, repository: DireccionRepository) -> None:
        self._repository = repository

    def list_direcciones(self, limit: int, offset: int) -> list[DireccionRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_direccion(self, id_direccion: int) -> DireccionRead:
        found = self._repository.get_by_id(id_direccion)
        if not found:
            raise NotFoundError("Direccion no encontrada")
        return found

    def create_direccion(self, payload: DireccionCreate) -> DireccionRead:
        return self._repository.create(payload)
