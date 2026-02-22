"""Contract model: container-backed list/add/update/delete with listener notification."""

from __future__ import annotations

from typing import Any, Callable


class ContractModel:
    def __init__(self, container: dict[str, Any]) -> None:
        self._container = container
        self._listeners: list[Callable[[], None]] = []

    def add_listener(self, callback: Callable[[], None]) -> None:
        self._listeners.append(callback)

    def _notify_listeners(self) -> None:
        for cb in list(self._listeners):
            cb()

    def get_all(self) -> list[dict[str, Any]]:
        contracts = self._container["list_contracts"]()
        return [
            {
                "contract_id": c.contract_id,
                "application_ref": c.application_ref,
                "source_type": c.source_type,
                "source_path": c.source_path,
                "version": c.version,
                "checksum_sha256": c.checksum_sha256,
            }
            for c in contracts
        ]

    def get(self, contract_id: str) -> dict[str, Any] | None:
        for c in self.get_all():
            if c.get("contract_id") == contract_id:
                return c
        return None

    def add(self, record: dict[str, Any]) -> None:
        self._container["add_contract"](record)
        self._notify_listeners()

    def update(self, old_id: str, record: dict[str, Any]) -> None:
        self._container["update_contract"](old_id, record)
        self._notify_listeners()

    def delete(self, contract_id: str) -> None:
        self._container["delete_contract"](contract_id)
        self._notify_listeners()
