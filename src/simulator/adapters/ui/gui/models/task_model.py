"""Task model: container/service-backed list, load, compose, create, get, unregister."""

from typing import Any, Callable


class TaskModel:
    def __init__(self, container):
        self._container = container
        self._listeners = []

    def add_listener(self, callback):
        self._listeners.append(callback)

    def _notify_listeners(self):
        for cb in list(self._listeners):
            cb()

    def get_all(self):
        return self._container["simulation_service"].list_tasks()

    def get(self, task_id):
        get_task = self._container.get("get_task")
        if get_task:
            return get_task(task_id)
        return None

    def load_task(self, path):
        r = self._container["simulation_service"].load_task(path)
        self._notify_listeners()
        return r

    def compose_task(self, base_task_ids, overrides):
        r = self._container["simulation_service"].compose_task(base_task_ids, overrides)
        self._notify_listeners()
        return r

    def add(self, record):
        r = self._container["simulation_service"].create_task(record)
        self._notify_listeners()
        return r  # {ok, task_id, error_code, message}

    def delete(self, task_id):
        r = self._container["unregister_task"](task_id)
        self._notify_listeners()
        return r
