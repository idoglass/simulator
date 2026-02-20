"""Tests for FR-GR-007 and MVP: foundation, shared engine, runtime load, verification, logging."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from simulator.app.bootstrap import create_app
from simulator.domain.models.run_models import RunInput
from simulator.domain.models.run_models import ObservedInteractions
from simulator.adapters.logging.console_logging import ConsoleLoggingAdapter
from simulator.adapters.verification.count_verification import CountVerificationAdapter
from simulator.workflows import RunWorkflow


class TestSimulatorFoundation(unittest.TestCase):
    """Core simulator flow runs without coupling to one specific application model."""

    def test_run_workflow_executes_without_app_model_coupling(self) -> None:
        """MVP: target + task resolved; transport and verification run (pass/fail depends on server)."""
        container = create_app(mode="tui")
        workflow: RunWorkflow = container["workflow"]
        run_input = RunInput(
            run_id="test-run-001",
            target_id="default-target",
            task_id="ping-smoke",
            protocol="tcp",
        )
        result = workflow.run(run_input)
        self.assertEqual(result["run_id"], run_input.run_id)
        self.assertIn("observed", result)
        self.assertIn("verification", result)
        self.assertIn("summary", result["verification"])
        self.assertIn("passed", result["verification"])

    def test_run_workflow_stateless_multiple_runs(self) -> None:
        """No mutable per-session state between runs (stateless boundary)."""
        container = create_app(mode="tui")
        workflow: RunWorkflow = container["workflow"]
        r1 = workflow.run(
            RunInput(run_id="r1", target_id="default-target", task_id="ping-smoke", protocol="tcp")
        )
        r2 = workflow.run(
            RunInput(run_id="r2", target_id="default-udp", task_id="ping-smoke", protocol="udp")
        )
        self.assertEqual(r1["run_id"], "r1")
        self.assertEqual(r2["run_id"], "r2")
        self.assertNotEqual(r1["run_id"], r2["run_id"])

    def test_simulation_service_same_api_as_workflow(self) -> None:
        """Shared simulation service produces equivalent result for same inputs (FR-GR-026)."""
        container = create_app(mode="tui")
        service = container["simulation_service"]
        result = service.run(
            run_id="svc-run-1",
            target_id="default-target",
            task_id="ping-smoke",
            protocol="tcp",
        )
        self.assertEqual(result["run_id"], "svc-run-1")
        self.assertIn("verification", result)

    def test_list_tasks_returns_registered_tasks(self) -> None:
        """Task registry exposes list of tasks (e.g. from fixtures)."""
        container = create_app(mode="tui")
        service = container["simulation_service"]
        tasks = service.list_tasks()
        self.assertIsInstance(tasks, list)
        self.assertTrue(any(t.get("task_id") == "ping-smoke" for t in tasks))

    def test_load_task_runtime_registration(self) -> None:
        """Runtime task load: register from path without restart (FR-GR-028)."""
        container = create_app(mode="tui")
        service = container["simulation_service"]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".task.json", delete=False) as f:
            f.write('{"task_id":"temp-task","name":"Temp","steps":[],"payloads":{},"defaults":{}}')
            path = f.name
        try:
            result = service.load_task(path)
            self.assertTrue(result.get("ok"))
            self.assertEqual(result.get("task_id"), "temp-task")
            self.assertEqual(result.get("error_code"), "OK")
            tasks = service.list_tasks()
            self.assertTrue(any(t.get("task_id") == "temp-task" for t in tasks))
        finally:
            Path(path).unlink(missing_ok=True)

    def test_verification_count_rules_mismatch(self) -> None:
        """Count verification fails when observed count does not match expected."""
        adapter = CountVerificationAdapter()
        expected = [{"message_type": "PingResponse", "direction": "receive", "expected_count": 1, "comparison": "eq"}]
        observed = ObservedInteractions(interactions=(), transport_errors=())
        result = adapter.verify_count_rules(expected, observed)
        self.assertFalse(result.passed)
        self.assertEqual(len(result.mismatches), 1)
        self.assertEqual(result.mismatches[0]["actual_count"], 0)

    def test_verification_count_rules_pass(self) -> None:
        """Count verification passes when observed matches expected."""
        adapter = CountVerificationAdapter()
        expected = [{"message_type": "PingResponse", "direction": "receive", "expected_count": 1, "comparison": "eq"}]
        observed = ObservedInteractions(
            interactions=({"direction": "receive", "message_type": "PingResponse"},),
            transport_errors=(),
        )
        result = adapter.verify_count_rules(expected, observed)
        self.assertTrue(result.passed)

    def test_logging_redacts_sensitive_keys(self) -> None:
        """Sensitive field values are redacted in logs (FR-GR-059)."""
        redacted = ConsoleLoggingAdapter._redact({"run_id": "r1", "password": "secret123", "task_id": "t1"})
        self.assertEqual(redacted["run_id"], "r1")
        self.assertEqual(redacted["password"], "[REDACTED]")
        self.assertEqual(redacted["task_id"], "t1")

    def test_compose_task_registers_new_task(self) -> None:
        """Task composition creates valid task with unique ID (FR-GR-027)."""
        container = create_app(mode="tui")
        service = container["simulation_service"]
        # Ensure we have at least ping-smoke
        tasks = service.list_tasks()
        self.assertGreaterEqual(len(tasks), 1)
        tid = tasks[0]["task_id"]
        r = service.compose_task([tid, tid], {"task_id": "composed-test", "name": "Composed"})
        self.assertTrue(r.get("ok"), str(r))
        self.assertEqual(r.get("task_id"), "composed-test")
        listed = service.list_tasks()
        self.assertTrue(any(t.get("task_id") == "composed-test" for t in listed))

    def test_create_task_from_definition(self) -> None:
        """Create from scratch registers task (GUI/TUI create)."""
        container = create_app(mode="tui")
        service = container["simulation_service"]
        r = service.create_task({
            "task_id": "created-test-1",
            "name": "Created",
            "steps": [],
            "payloads": {},
            "defaults": {},
        })
        self.assertTrue(r.get("ok"), str(r))
        self.assertEqual(r.get("task_id"), "created-test-1")
        listed = service.list_tasks()
        self.assertTrue(any(t.get("task_id") == "created-test-1" for t in listed))

    def test_run_writes_capture_when_port_wired(self) -> None:
        """Run with capture_replay port yields capture_path (FR-GR-029)."""
        container = create_app(mode="tui")
        workflow = container["workflow"]
        run_input = RunInput(
            run_id="cap-run-1",
            target_id="default-target",
            task_id="ping-smoke",
            protocol="tcp",
        )
        result = workflow.run(run_input)
        self.assertIn("run_id", result)
        self.assertIn("capture_path", result)
        self.assertTrue(isinstance(result.get("capture_path"), str) and len(result.get("capture_path", "")) > 0)
