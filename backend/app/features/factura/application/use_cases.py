from __future__ import annotations
from app.features.factura.application.schemas import FacturaCreate, FacturaRead
from app.features.factura.domain.repositories import FacturaRepository
from app.shared.exceptions import ConflictError, NotFoundError


class FacturaUseCases:
    def __init__(self, repository: FacturaRepository) -> None:
        self._repository = repository

    def list_facturas(self, limit: int, offset: int) -> list[FacturaRead]:
        return self._repository.list(limit=limit, offset=offset)

    def get_factura(self, id_factura: int) -> FacturaRead:
        found = self._repository.get_by_id(id_factura)
        if not found:
            raise NotFoundError("Factura no encontrada")
        return found

    def create_factura(self, payload: FacturaCreate) -> FacturaRead:
        if self._repository.get_by_numero(payload.numero_factura):
            raise ConflictError("El numero de factura ya existe")
        return self._repository.create(payload)
