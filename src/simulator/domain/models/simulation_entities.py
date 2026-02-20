"""SRS Section 3 domain entities (TKT-C02-01). Typed entities for app/target/contract/task/transport/sequence."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

ID_REGEX = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


@dataclass(frozen=True)
class SimulatedApplication:
    """SRS 3.2."""

    app_id: str
    app_name: str
    description: str = ""
    enabled: bool = True


@dataclass(frozen=True)
class TargetDefinition:
    """SRS 3.3."""

    target_id: str
    target_name: str
    application_ref: str
    transport_ref: str
    timeout_ms: int = 5000
    retry_count: int = 1


@dataclass(frozen=True)
class ContractDefinition:
    """SRS 3.4."""

    contract_id: str
    application_ref: str
    source_type: str  # repo_h | user_h
    source_path: str
    version: str = "0.1.0"
    checksum_sha256: str = ""


@dataclass(frozen=True)
class TaskDefinitionSRS:
    """SRS 3.5 (workspace entity; runtime uses domain.models.target_and_task.TaskDefinition)."""

    task_id: str
    application_ref: str
    task_name: str
    registration_type: str  # built_in | runtime_loaded
    task_ref: str
    execution_mode: str = "oneshot"  # oneshot | periodic
    periodic_config: dict[str, Any] | None = None


@dataclass(frozen=True)
class TransportDefinition:
    """SRS 3.6."""

    transport_id: str
    application_ref: str
    protocol: str = "tcp"
    mode: str = "client"
    local_endpoint: str = ""
    remote_endpoint: str = ""
    connect_timeout_ms: int = 3000
    read_timeout_ms: int = 5000
    write_timeout_ms: int = 5000
    max_packet_bytes: int = 65535


@dataclass(frozen=True)
class SequenceStepDefinition:
    """SRS sequence step (order_index unique per sequence)."""

    order_index: int
    task_ref: str
    failure_policy: str = "stop"  # stop | continue
