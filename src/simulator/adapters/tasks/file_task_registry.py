"""Task registry that loads .task.json files from a directory."""

from __future__ import annotations

import json
from pathlib import Path

from simulator.domain.models.target_and_task import (
    StepExpect,
    TaskDefinition,
    TaskStep,
)


def _parse_step(step: dict) -> TaskStep:
    expect = step.get("expect")
    step_expect = None
    if expect and isinstance(expect, dict):
        matcher = expect.get("matcher") or {}
        step_expect = StepExpect(
            direction=str(matcher.get("direction", "receive")),
            message_type=str(matcher.get("message_type", "")),
            expected_count=int(expect.get("expected_count", 0)),
            comparison=str(expect.get("comparison", "eq")),
        )
    return TaskStep(
        step_id=str(step.get("step_id", "")),
        action=str(step.get("action", "send")),
        message_type=str(step.get("message_type", "")),
        payload_ref=step.get("payload_ref") if isinstance(step.get("payload_ref"), str) else None,
        expect=step_expect,
        timeout_ms=int(step.get("timeout_ms", 5000)),
    )


def load_task_file_from_dict(data: dict) -> TaskDefinition:
    """Build TaskDefinition from a dict (e.g. from form or API)."""
    steps = tuple(_parse_step(s) for s in data.get("steps") or [])
    payloads = {k: v for k, v in (data.get("payloads") or {}).items() if isinstance(v, dict)}
    defaults = dict(data.get("defaults") or {})
    return TaskDefinition(
        task_id=str(data.get("task_id", "")),
        name=str(data.get("name", "")),
        steps=steps,
        payloads=payloads,
        defaults=defaults,
    )


def load_task_file(path: Path) -> TaskDefinition:
    """Load one .task.json file into TaskDefinition."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return load_task_file_from_dict(data)


class FileTaskRegistryAdapter:
    """Implements TaskRegistryPort by loading .task.json from a directory."""

    def __init__(self, tasks_dir: Path | None = None) -> None:
        # Default: repo root is 4 levels up from this file (simulator/adapters/tasks)
        _repo = Path(__file__).resolve().parents[4]
        self._tasks_dir = tasks_dir or (_repo / "tests" / "fixtures" / "tasks")
        self._cache: dict[str, TaskDefinition] = {}
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        if self._tasks_dir.exists():
            for p in self._tasks_dir.glob("*.task.json"):
                try:
                    task = load_task_file(p)
                    self._cache[task.task_id] = task
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue
        self._loaded = True

    def get(self, task_id: str) -> TaskDefinition | None:
        self._ensure_loaded()
        return self._cache.get(task_id)

    def list_tasks(self) -> list[dict[str, object]]:
        self._ensure_loaded()
        return [{"task_id": t.task_id, "name": t.name} for t in self._cache.values()]

    def register_from_path(self, path: str) -> dict[str, object]:
        """Load a .task.json from path and register it (runtime load without restart)."""
        p = Path(path)
        if not p.exists() or not p.suffix.lower().endswith(".json"):
            return {"ok": False, "task_id": "", "error_code": "TASK_PATH_INVALID"}
        try:
            task = load_task_file(p)
            self._cache[task.task_id] = task
            self._loaded = True
            return {"ok": True, "task_id": task.task_id, "error_code": "OK"}
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            return {"ok": False, "task_id": "", "error_code": "TASK_LOAD_FAILED", "message": str(e)}

    def compose(self, base_task_ids: list[str], overrides: dict[str, object]) -> dict[str, object]:
        """Compose a new task from base tasks. Returns {ok, task_id, task_def, error_code}."""
        self._ensure_loaded()
        if not base_task_ids:
            return {"ok": False, "task_id": "", "error_code": "COMPOSE_NO_BASES"}
        tasks: list[TaskDefinition] = []
        for tid in base_task_ids:
            t = self._cache.get(tid)
            if t is None:
                return {"ok": False, "task_id": "", "error_code": "COMPOSE_BASE_NOT_FOUND", "missing": tid}
            tasks.append(t)
        # Merge: concatenate steps, merge payloads/defaults; overrides apply to result
        merged_steps: list[TaskStep] = []
        merged_payloads: dict[str, dict] = {}
        merged_defaults: dict[str, object] = {}
        for t in tasks:
            merged_steps.extend(t.steps)
            merged_payloads.update(t.payloads)
            merged_defaults.update(t.defaults)
        new_id = str(overrides.get("task_id") or f"composed-{'-'.join(base_task_ids)}")
        if new_id in self._cache:
            return {"ok": False, "task_id": new_id, "error_code": "COMPOSE_DUPLICATE_ID"}
        merged_defaults.update(overrides.get("defaults") or {})
        composed = TaskDefinition(
            task_id=new_id,
            name=str(overrides.get("name") or f"Composed from {', '.join(base_task_ids)}"),
            steps=tuple(merged_steps),
            payloads=merged_payloads,
            defaults=merged_defaults,
        )
        self._cache[new_id] = composed
        return {"ok": True, "task_id": new_id, "error_code": "OK"}

    def register_definition(self, definition: dict[str, object]) -> dict[str, object]:
        """Register a task from an in-memory definition (create from scratch). Returns {ok, task_id, error_code}."""
        try:
            task_id = str(definition.get("task_id") or "")
            if not task_id:
                return {"ok": False, "task_id": "", "error_code": "TASK_ID_REQUIRED"}
            if task_id in self._cache:
                return {"ok": False, "task_id": task_id, "error_code": "TASK_DUPLICATE_ID"}
            task = load_task_file_from_dict(definition)
            self._cache[task_id] = task
            self._loaded = True
            return {"ok": True, "task_id": task_id, "error_code": "OK"}
        except (KeyError, TypeError) as e:
            return {"ok": False, "task_id": "", "error_code": "TASK_DEFINITION_INVALID", "message": str(e)}
