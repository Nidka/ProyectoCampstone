from __future__ import annotations
from app.features.tipo_unidad.application.schemas import TipoUnidadCreate, TipoUnidadRead
from app.features.tipo_unidad.domain.repositories import TipoUnidadRepository
from app.shared.exceptions import ConflictError, NotFoundError


class TipoUnidadUseCases:
    def __init__(self, repository: TipoUnidadRepository) -> None:
        self._repository = repository

    def list_tipos_unidad(self, limit: int, offset: int) -> list[TipoUnidadRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_tipo_unidad(self, id_tipo_unidad: int) -> TipoUnidadRead:
        found = self._repository.get_by_id(id_tipo_unidad)
        if not found:
            raise NotFoundError("TipoUnidad no encontrado")
        return found

    def create_tipo_unidad(self, payload: TipoUnidadCreate) -> TipoUnidadRead:
        if self._repository.get_by_nombre(payload.nombre):
            raise ConflictError("El nombre del tipo de unidad ya existe")
        return self._repository.create(payload)
