# ADR-003: Task Format is JSON with Semantic Schema Versioning

- Status: Accepted
- Date: 2026-02-19

## Context

Tasks must be loadable at runtime, composable from existing tasks, and validated deterministically across platforms.

## Decision

Use JSON task documents (`.task.json`) with `task_schema_version` using semantic versioning.

- MVP loader supports schema major version `1`.
- Unknown major versions fail fast with deterministic error.
- Runtime registration remains atomic after parse/validate/normalize steps.

## Consequences

Positive:

- Deterministic parsing and broad tooling support.
- Straightforward schema validation and migration tooling.
- Good compatibility with Python ecosystem and CI pipelines.

Trade-offs:

- JSON lacks comments and can be verbose.
- Human editing ergonomics are weaker than YAML for some users.

## Alternatives Considered

1. YAML task files (rejected for MVP): higher parser/format variability risk.
2. Python-based task scripts (rejected for MVP): higher safety and determinism concerns.

## Requirement Mapping

- GR-027, GR-028, GR-023
