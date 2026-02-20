"""Capture/replay port: persist and load capture artifacts for replay."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from simulator.domain.models.run_models import ObservedInteractions


class CaptureReplayPort(Protocol):
    """Write capture to file; read capture for replay. File-based in MVP."""

    def write_capture(
        self,
        *,
        run_id: str,
        target_id: str,
        task_id: str,
        protocol: str,
        observed: "ObservedInteractions",
    ) -> dict[str, Any]: ...

    def read_capture(self, path: str) -> dict[str, Any]: ...
