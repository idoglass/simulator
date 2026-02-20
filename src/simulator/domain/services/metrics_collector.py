"""Metrics collector: counters/timers/gauges (TKT-S03-02)."""

from __future__ import annotations

from typing import Any


class MetricsCollector:
    """Counters, timers, gauges for NFR baseline."""

    def __init__(self) -> None:
        self._counters: dict[str, int] = {}
        self._gauges: dict[str, float] = {}

    def increment(self, name: str, value: int = 1) -> None:
        self._counters[name] = self._counters.get(name, 0) + value

    def gauge(self, name: str, value: float) -> None:
        self._gauges[name] = value

    def get_counter(self, name: str) -> int:
        return self._counters.get(name, 0)

    def get_gauge(self, name: str) -> float:
        return self._gauges.get(name, 0.0)
