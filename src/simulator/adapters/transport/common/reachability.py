"""Reachability check: TCP connect or UDP send with timeout. No dependency on full transport adapter."""

from __future__ import annotations

import socket
from typing import Any

from simulator.domain.models.target_and_task import TargetRef


def check_reachable(target: TargetRef, timeout_sec: float = 2.0) -> dict[str, Any]:
    """
    Check if target is reachable (TCP connect or UDP sendto with timeout).
    Returns {"ok": True} or {"ok": False, "error": "..."}.
    """
    try:
        if (target.protocol or "tcp").lower() == "tcp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout_sec)
            try:
                sock.connect((target.host, target.port))
                return {"ok": True}
            finally:
                sock.close()
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout_sec)
            try:
                sock.sendto(b"", (target.host, target.port))
                return {"ok": True}
            finally:
                sock.close()
    except socket.timeout:
        return {"ok": False, "error": "timeout"}
    except OSError as e:
        return {"ok": False, "error": str(e)}
    except Exception as e:
        return {"ok": False, "error": str(e)}
