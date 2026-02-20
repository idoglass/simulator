"""Tests for FR-GR-007: robust generic stateless simulator foundation."""

from __future__ import annotations

import unittest

from simulator.app.bootstrap import create_app
from simulator.domain.models.run_models import RunInput
from simulator.workflows import RunWorkflow


class TestSimulatorFoundation(unittest.TestCase):
    """Core simulator flow runs without coupling to one specific application model."""

    def test_run_workflow_executes_without_app_model_coupling(self) -> None:
        container = create_app(mode="tui")
        workflow: RunWorkflow = container["workflow"]
        run_input = RunInput(
            run_id="test-run-001",
            target_id="any-target",
            task_id="any-task",
            protocol="tcp",
        )
        result = workflow.run(run_input)
        self.assertEqual(result["run_id"], run_input.run_id)
        self.assertIn("observed", result)
        self.assertIn("verification", result)
        self.assertIs(result["verification"]["passed"], True)
        self.assertIn("summary", result["verification"])

    def test_run_workflow_stateless_multiple_runs(self) -> None:
        """No mutable per-session state between runs (stateless boundary)."""
        container = create_app(mode="tui")
        workflow: RunWorkflow = container["workflow"]
        r1 = workflow.run(
            RunInput(run_id="r1", target_id="t1", task_id="task1", protocol="udp")
        )
        r2 = workflow.run(
            RunInput(run_id="r2", target_id="t2", task_id="task2", protocol="tcp")
        )
        self.assertEqual(r1["run_id"], "r1")
        self.assertEqual(r2["run_id"], "r2")
        self.assertNotEqual(r1["run_id"], r2["run_id"])
