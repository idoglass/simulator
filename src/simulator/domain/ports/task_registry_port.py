"""Task registry port. Adapters provide task lookup and registration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from simulator.domain.models.target_and_task import TaskDefinition


class TaskRegistryPort(Protocol):
    """Get and list registered tasks; register atomically; compose from base tasks (runtime, no restart)."""

    def get(self, task_id: str) -> "TaskDefinition | None": ...
    def list_tasks(self) -> list[dict[str, object]]: ...
    def register_from_path(self, path: str) -> dict[str, object]: ...
    def compose(self, base_task_ids: list[str], overrides: dict[str, object]) -> dict[str, object]: ...
    def register_definition(self, definition: dict[str, object]) -> dict[str, object]: ...  # create from scratch
