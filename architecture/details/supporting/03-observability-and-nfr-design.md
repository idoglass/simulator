# DDS Supporting 03: Observability and NFR Design

## 1. Purpose

Define logging/event strategy and design mechanisms to satisfy SRS non-functional requirements.

## 2. Event Types

Required lifecycle events:

- run start/stop
- step start/send/verify/fail
- periodic task start/iteration/fail/stop
- transport send/receive timeout/failure
- validation failures

## 3. Logging Model

Every log entry should include:

- timestamp
- level
- run_id
- step_id (if applicable)
- task_id (if applicable)
- transport metadata
- error_code (if failure)

Redaction:

- sensitive payload fields must be masked before output

## 4. Metrics (Minimum)

Counters:

- runs started/completed/failed
- steps passed/failed
- periodic iterations started/failed/skipped
- errors by `error_code`

Timers:

- step dispatch latency
- end-to-end run duration
- verification duration

Gauges:

- active periodic tasks
- active run contexts

## 5. NFR Realization Notes

- **Portability (SRS-NFR-001):** keep adapter boundaries OS-neutral.
- **Testability (SRS-NFR-004):** expose deterministic service interfaces for unit tests.
- **Concurrency (SRS-NFR-006):** scheduler execution separated from foreground sequence loop.
- **Capacity/throughput (SRS-NFR-007/008):** use bounded worker pools and backpressure safeguards.

## 6. Capacity Safeguards

- enforce maximum configured active periodic tasks
- bound queue lengths for scheduler and event bus
- reject oversized transport payloads by `max_packet_bytes`
- emit warning before hard failure when nearing configured limits
