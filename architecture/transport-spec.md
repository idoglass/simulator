# Transport Specification (TCP/UDP, MVP)

This document defines protocol behavior for transport adapters in MVP.

## 1) Scope

- Protocols: **TCP** and **UDP**
- Modes: **client and server** for both protocols
- Runtime: desktop application
- Consumers: shared simulation workflows via `TransportPort`

## 2) Common Transport Contract

Transport adapters implement `TransportPort` and expose one core execution behavior:

- Input: target, protocol, ordered messages, timeout config
- Output: ordered observed interactions + transport-level errors

Common requirements:
1. Deterministic ordering of observations as seen by the adapter.
2. Structured, deterministic error reporting.
3. Correlation fields included in emitted interaction/error records (`run_id`, `target_id`, `task_id` where available).

## 3) TCP Behavior

### 3.1 Client Mode
- Open connection to target endpoint.
- Send message stream in configured order.
- Read responses/events according to flow definition and timeout policy.
- Close connection gracefully on completion or failure.

### 3.2 Server Mode
- Bind/listen on configured endpoint.
- Accept inbound connection(s) in configured run scope.
- Receive inbound messages, emit observed interactions, and respond per task/flow rules.
- Close connection(s) on completion, timeout, or cancellation.

### 3.3 Framing Assumption (MVP)
- Use a deterministic framing strategy configured per run/target.
- If framing is undefined/invalid for a run, fail validation before execution.

## 4) UDP Behavior

### 4.1 Client Mode
- Send datagrams to target endpoint in configured order.
- Receive datagrams within timeout windows.
- No connection state is assumed between datagrams.

### 4.2 Server Mode
- Bind socket to configured endpoint.
- Receive datagrams and emit observed interactions.
- Respond with datagrams per configured flow/task behavior.

### 4.3 Delivery Notes (MVP)
- UDP is treated as best-effort transport.
- Packet loss/reordering should be represented in observed interactions where detectable.

## 5) Timeout and Retry Policy

MVP baseline:

1. `connect_timeout_ms` (TCP client connect only)
2. `read_timeout_ms`
3. `write_timeout_ms`
4. `max_retries` (optional, per message/run policy)

Rules:
- Timeout values are explicit per run/target config.
- Retries are deterministic and logged.
- Retry exhaustion yields structured failure result.

## 6) Error Semantics

Transport adapters must map low-level errors to simulator transport error categories:

- `TRANSPORT_CONNECT_TIMEOUT`
- `TRANSPORT_READ_TIMEOUT`
- `TRANSPORT_WRITE_TIMEOUT`
- `TRANSPORT_CONNECTION_REFUSED`
- `TRANSPORT_CONNECTION_RESET`
- `TRANSPORT_BIND_FAILED`
- `TRANSPORT_PROTOCOL_ERROR`
- `TRANSPORT_RETRY_EXHAUSTED`

Each error entry should include:
- category/code
- message
- protocol
- endpoint
- timestamp
- correlation IDs

## 7) Configuration Surface (MVP)

Per target/run transport config should include:

- `protocol`: `tcp` or `udp`
- `mode`: `client` or `server`
- endpoint (host/port)
- timeout settings
- retry settings
- framing identifier (if applicable)

## 8) Validation Rules Before Execution

1. Protocol must be one of `{tcp, udp}`.
2. Mode must be one of `{client, server}`.
3. Endpoint and timeout settings must be present and valid.
4. Framing config required for flows that depend on framing.
5. Invalid config prevents run start.

## 9) Test Expectations (Architecture-Level)

For each protocol/mode combination:

- TCP client happy path
- TCP server happy path
- UDP client happy path
- UDP server happy path
- Timeout failure path
- Retry exhaustion path (if retries enabled)

## 10) Requirement Mapping

- GR-031, GR-020, GR-026, GR-039, GR-059
