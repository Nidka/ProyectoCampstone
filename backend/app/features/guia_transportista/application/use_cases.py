from __future__ import annotations
from app.features.guia_transportista.application.schemas import GuiaTransportistaCreate, GuiaTransportistaRead
from app.features.guia_transportista.domain.repositories import GuiaTransportistaRepository
from app.shared.exceptions import ConflictError, NotFoundError


class GuiaTransportistaUseCases:
    def __init__(self, repository: GuiaTransportistaRepository) -> None:
        self._repository = repository

    def list_guias(self, limit: int, offset: int) -> list[GuiaTransportistaRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_guia(self, id_guia_transportista: int) -> GuiaTransportistaRead:
        found = self._repository.get_by_id(id_guia_transportista)
        if not found:
            raise NotFoundError("Guia no encontrada")
        return found

    def create_guia(self, payload: GuiaTransportistaCreate) -> GuiaTransportistaRead:
        if self._repository.get_by_numero(payload.numero_guia):
            raise ConflictError("El numero de guia ya existe")
        return self._repository.create(payload)
