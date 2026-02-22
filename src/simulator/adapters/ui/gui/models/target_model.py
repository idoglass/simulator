"""Target model: container-backed list/add/update/delete with listener notification."""

from typing import Any, Callable


class TargetModel:
    def __init__(self, container):
        self._container = container
        self._listeners = []

    def add_listener(self, callback):
        self._listeners.append(callback)

    def _notify_listeners(self):
        for cb in list(self._listeners):
            cb()

    def get_all(self):
        targets = self._container["list_targets"]()
        return [
            {
                "target_id": t.target_id,
                "name": t.name,
                "host": t.host,
                "port": t.port,
                "protocol": t.protocol,
                "mode": t.mode,
            }
            for t in targets
        ]

    def get(self, target_id):
        for t in self.get_all():
            if t.get("target_id") == target_id:
                return t
        return None

    def add(self, record):
        self._container["add_target"](record)
        self._notify_listeners()

    def update(self, old_id, record):
        self._container["update_target"](old_id, record)
        self._notify_listeners()

    def delete(self, target_id):
        self._container["delete_target"](target_id)
        self._notify_listeners()
