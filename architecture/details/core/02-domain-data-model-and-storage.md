# DDS Core 02: Domain Data Model and Storage

## 1. Purpose

Translate SRS Section 3 field-level schemas into a concrete domain model and persistence approach.

## 2. Aggregate Roots

1. `SimulatedApplication`
2. `TargetDefinition`
3. `ContractDefinition`
4. `TaskDefinition`
5. `TransportDefinition`
6. `MessageDefinition`
7. `ExpectedResponse`
8. `SequenceDefinition` (owns `SequenceStep`)

Runtime-only model:

- `PeriodicTaskRuntime` (per-run)

## 3. Relationship Model

- Application 1:N Targets
- Application 1:N Contracts
- Application 1:N Tasks
- Application 1:N Transports
- Application 1:N Sequences
- Target 1:N Messages
- Message 1:1 ExpectedResponse (MVP assumption)
- Sequence 1:N SequenceSteps (ordered by `order_index`)

## 4. Persistence Boundary

Persisted:

- All configuration entities above except `PeriodicTaskRuntime`

Not persisted across runs:

- mutable run state
- in-flight scheduler state
- transient counters tied to one run context

## 5. Storage Shape (Canonical)

```text
workspace_config/
  applications/
    <app_id>.json
  targets/
    <target_id>.json
  contracts/
    <contract_id>.json
  tasks/
    <task_id>.json
  transports/
    <transport_id>.json
  messages/
    <message_id>.json
  expectations/
    <expectation_id>.json
  sequences/
    <sequence_id>.json
```

Note: actual backend can be file, sqlite, or other adapter; canonical shape defines logical contract only.

## 6. Data Integrity Rules

1. `app_name` is unique across workspace.
2. Every `*_ref` must resolve before save and before run.
3. `order_index` must be unique per `sequence_ref`.
4. `periodic_config` is required when `execution_mode=periodic`.
5. `max_parallel_runs` is required when overlap policy is `parallel`.
6. Transport mode/endpoint consistency:
   - server mode requires `local_endpoint`
   - client mode requires `remote_endpoint`

## 7. Repository Interfaces

```text
ApplicationRepo: create/get/list/update/delete
TargetRepo: create/get/list/update/delete
ContractRepo: create/get/list/update/delete
TaskRepo: create/get/list/update/delete
TransportRepo: create/get/list/update/delete
MessageRepo: create/get/list/update/delete
ExpectationRepo: create/get/list/update/delete
SequenceRepo: create/get/list/update/delete
```

Cross-repository query interface:

- `get_run_bundle(sequence_id)` -> fully resolved immutable run bundle

## 8. Versioning and Migration

- Use semantic `version` on contract definitions.
- Persisted schema metadata should include `schema_version`.
- On load, migration adapter upgrades older persisted shape to current canonical model.
