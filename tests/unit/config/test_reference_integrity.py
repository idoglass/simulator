"""Unit tests for repository reference integrity (TKT-C02-02)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from simulator.config.repository_impl import (
    FileApplicationRepository,
    FileTargetRepository,
    FileTaskRepository,
)
from simulator.domain.models.simulation_entities import (
    SimulatedApplication,
    TargetDefinition,
    TaskDefinitionSRS,
)


def test_target_save_requires_existing_app() -> None:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        app_repo = FileApplicationRepository(root)
        app_repo.save(SimulatedApplication(app_id="a1", app_name="App1"))
        target_repo = FileTargetRepository(root, app_repo)
        target_repo.save(
            TargetDefinition(
                target_id="t1",
                target_name="T1",
                application_ref="a1",
                transport_ref="tr1",
            )
        )
        assert target_repo.get("t1") is not None
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        app_repo = FileApplicationRepository(root)
        target_repo = FileTargetRepository(root, app_repo)
        try:
            target_repo.save(
                TargetDefinition(
                    target_id="t1",
                    target_name="T1",
                    application_ref="nonexistent",
                    transport_ref="tr1",
                )
            )
        except ValueError as e:
            assert "application_ref" in str(e)


def test_task_save_requires_existing_app() -> None:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        app_repo = FileApplicationRepository(root)
        app_repo.save(SimulatedApplication(app_id="a1", app_name="App1"))
        task_repo = FileTaskRepository(root, app_repo)
        task_repo.save(
            TaskDefinitionSRS(
                task_id="task1",
                application_ref="a1",
                task_name="Task1",
                registration_type="built_in",
                task_ref="ping",
            )
        )
        assert task_repo.get("task1") is not None
