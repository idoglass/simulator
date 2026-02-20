"""Error envelope factory (TKT-S02-02)."""

from __future__ import annotations

from simulator.domain.models.error_envelope import ErrorEnvelope
from simulator.domain.services.error_catalog import CATALOG


def make_error(code: str, message: str, run_id: str | None = None, **context: object) -> ErrorEnvelope:
    category = code.split("-")[:2]
    return ErrorEnvelope(
        code=code,
        category="-".join(category) if len(category) >= 2 else "SRS-E",
        message=message,
        run_id=run_id,
        context=dict(context) if context else None,
    )
