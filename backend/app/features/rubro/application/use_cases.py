from __future__ import annotations
from app.features.rubro.application.schemas import RubroCreate, RubroRead
from app.features.rubro.domain.repositories import RubroRepository
from app.shared.exceptions import ConflictError, NotFoundError


class RubroUseCases:
    def __init__(self, repository: RubroRepository) -> None:
        self._repository = repository

    def list_rubros(self, limit: int, offset: int) -> list[RubroRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_rubro(self, id_rubro: int) -> RubroRead:
        found = self._repository.get_by_id(id_rubro)
        if not found:
            raise NotFoundError("Rubro no encontrado")
        return found

    def create_rubro(self, payload: RubroCreate) -> RubroRead:
        if self._repository.get_by_nombre(payload.nombre):
            raise ConflictError("El nombre del rubro ya existe")
        return self._repository.create(payload)
