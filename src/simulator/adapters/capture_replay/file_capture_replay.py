"""File-based capture/replay adapter. Writes and reads .capture.json files."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from simulator.domain.models.run_models import ObservedInteractions


def _default_capture_dir() -> Path:
    _repo = Path(__file__).resolve().parents[4]
    return _repo / "captures"


class FileCaptureReplayAdapter:
    """Implements CaptureReplayPort: write capture to JSON file, read for replay."""

    def __init__(self, capture_dir: Path | None = None) -> None:
        self._capture_dir = capture_dir or _default_capture_dir()

    def write_capture(
        self,
        *,
        run_id: str,
        target_id: str,
        task_id: str,
        protocol: str,
        observed: ObservedInteractions,
    ) -> dict[str, object]:
        """Write capture artifact to a .capture.json file. Returns {ok, path, error_code}."""
        self._capture_dir.mkdir(parents=True, exist_ok=True)
        capture_id = f"cap-{uuid4().hex[:12]}"
        path = self._capture_dir / f"{capture_id}.capture.json"
        doc = {
            "capture_schema_version": "1.0.0",
            "capture_id": capture_id,
            "created_at": datetime.now(tz=timezone.utc).isoformat(),
            "producer": {"app_name": "simulator", "app_version": "0.1.0"},
            "context": {
                "run_id": run_id,
                "target_id": target_id,
                "task_id": task_id,
                "protocol": protocol,
            },
            "interactions": [dict(i) for i in observed.interactions],
            "transport_errors": list(observed.transport_errors),
        }
        try:
            path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
            return {"ok": True, "path": str(path), "capture_id": capture_id, "error_code": "OK"}
        except OSError as e:
            return {"ok": False, "path": "", "error_code": "CAPTURE_WRITE_FAILED", "message": str(e)}

    def read_capture(self, path: str) -> dict[str, object]:
        """Read capture file. Returns {ok, context, interactions, transport_errors, error_code}."""
        p = Path(path)
        if not p.exists():
            return {"ok": False, "error_code": "CAPTURE_FILE_NOT_FOUND"}
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            return {
                "ok": True,
                "context": data.get("context", {}),
                "interactions": data.get("interactions", []),
                "transport_errors": data.get("transport_errors", []),
                "error_code": "OK",
            }
        except (json.JSONDecodeError, OSError) as e:
            return {"ok": False, "error_code": "CAPTURE_READ_FAILED", "message": str(e)}