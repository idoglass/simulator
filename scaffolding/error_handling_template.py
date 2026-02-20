"""Error handling scaffolding template."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ErrorEnvelope:
    code: str
    message: str
    category: str
    severity: str = "error"
    path: str | None = None
    run_id: str | None = None
    task_id: str | None = None
    target_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def make_error(
    *,
    code: str,
    message: str,
    category: str,
    path: str | None = None,
    run_id: str | None = None,
    task_id: str | None = None,
    target_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a standardized error envelope.

    Keep `code` values aligned with `architecture/error-codes.md`.
    """
    return ErrorEnvelope(
        code=code,
        message=message,
        category=category,
        path=path,
        run_id=run_id,
        task_id=task_id,
        target_id=target_id,
        details=details or {},
    ).to_dict()

