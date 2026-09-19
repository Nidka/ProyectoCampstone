from __future__ import annotations
from app.features.cliente.application.schemas import ClienteCreate, ClienteRead
from app.features.cliente.domain.repositories import ClienteRepository
from app.shared.exceptions import ConflictError, NotFoundError


class ClienteUseCases:
    def __init__(self, repository: ClienteRepository) -> None:
        self._repository = repository

    def list_clientes(self, limit: int, offset: int) -> list[ClienteRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_cliente(self, id_cliente: int) -> ClienteRead:
        found = self._repository.get_by_id(id_cliente)
        if not found:
            raise NotFoundError("Cliente no encontrado")
        return found

    def create_cliente(self, payload: ClienteCreate) -> ClienteRead:
        if self._repository.get_by_ruc(payload.ruc):
            raise ConflictError("El RUC ya existe")
        return self._repository.create(payload)
