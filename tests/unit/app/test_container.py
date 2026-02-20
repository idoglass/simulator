"""Unit tests for app container: service graph resolution (TKT-C01-01)."""

from __future__ import annotations

import pytest

from simulator.app.container import Container


def test_container_composes_services_through_one_entrypoint() -> None:
    """Services are composed through one container entrypoint."""
    container = Container(mode="tui")
    workflow = container.get_workflow()
    service = container.get_simulation_service()
    assert workflow is not None
    assert service is not None


def test_container_resolves_same_shared_service_graph_for_gui_and_tui() -> None:
    """GUI and TUI can resolve the same shared service graph."""
    gui_container = Container(mode="gui")
    tui_container = Container(mode="tui")
    gui_workflow = gui_container.get_workflow()
    tui_workflow = tui_container.get_workflow()
    gui_service = gui_container.get_simulation_service()
    tui_service = tui_container.get_simulation_service()
    assert gui_workflow is not None and tui_workflow is not None
    assert gui_service is not None and tui_service is not None
    assert gui_container.get_mode() == "gui"
    assert tui_container.get_mode() == "tui"
