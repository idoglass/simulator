"""Target and task models for simulation runs. Generic, no app-model coupling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TargetRef:
    """Identifies the target application/system for a simulation run."""

    target_id: str
    name: str
    host: str
    port: int
    protocol: str  # tcp | udp
    mode: str  # client | server


@dataclass(frozen=True)
class MessageEnvelope:
    """One message unit for transport execution."""

    message_type: str
    direction: str  # send | receive
    payload: dict[str, Any]


@dataclass(frozen=True)
class StepExpect:
    """Expected interaction rule (MVP: count-based)."""

    direction: str
    message_type: str
    expected_count: int
    comparison: str  # eq


@dataclass(frozen=True)
class TaskStep:
    """One step in a task definition."""

    step_id: str
    action: str  # send | receive_expectation
    message_type: str
    payload_ref: str | None
    expect: StepExpect | None
    timeout_ms: int


@dataclass(frozen=True)
class TaskDefinition:
    """Executable task definition (from .task.json or registry)."""

    task_id: str
    name: str
    steps: tuple[TaskStep, ...]
    payloads: dict[str, dict[str, Any]]
    defaults: dict[str, Any]
