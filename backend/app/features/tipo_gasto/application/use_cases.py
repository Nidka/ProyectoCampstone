from __future__ import annotations
from app.features.tipo_gasto.application.schemas import TipoGastoCreate, TipoGastoRead
from app.features.tipo_gasto.domain.repositories import TipoGastoRepository
from app.shared.exceptions import ConflictError, NotFoundError


class TipoGastoUseCases:
    def __init__(self, repository: TipoGastoRepository) -> None:
        self._repository = repository

    def list_tipos_gasto(self, limit: int, offset: int) -> list[TipoGastoRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_tipo_gasto(self, id_tipo_gasto: int) -> TipoGastoRead:
        found = self._repository.get_by_id(id_tipo_gasto)
        if not found:
            raise NotFoundError("TipoGasto no encontrado")
        return found

    def create_tipo_gasto(self, payload: TipoGastoCreate) -> TipoGastoRead:
        if self._repository.get_by_nombre(payload.nombre):
            raise ConflictError("El nombre del tipo de gasto ya existe")
        return self._repository.create(payload)
