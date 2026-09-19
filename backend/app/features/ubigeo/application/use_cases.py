from __future__ import annotations
from app.features.ubigeo.application.schemas import UbigeoCreate, UbigeoRead
from app.features.ubigeo.domain.repositories import UbigeoRepository
from app.shared.exceptions import ConflictError, NotFoundError


class UbigeoUseCases:
    def __init__(self, repository: UbigeoRepository) -> None:
        self._repository = repository

    def list_ubigeos(self, limit: int, offset: int) -> list[UbigeoRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_ubigeo(self, codigo_ubigeo: int) -> UbigeoRead:
        found = self._repository.get_by_codigo(codigo_ubigeo)
        if not found:
            raise NotFoundError("Ubigeo no encontrado")
        return found

    def create_ubigeo(self, payload: UbigeoCreate) -> UbigeoRead:
        if self._repository.get_by_codigo(payload.codigo_ubigeo):
            raise ConflictError("El codigo_ubigeo ya existe")
        return self._repository.create(payload)
