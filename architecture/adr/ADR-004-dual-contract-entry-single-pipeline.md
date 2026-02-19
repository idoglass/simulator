# ADR-004: Dual Contract Entry Types with One Canonical Validation Pipeline

- Status: Accepted
- Date: 2026-02-19

## Context

The simulator must support contracts from raw `.h` directories and generated `ctypes` directories while keeping runtime behavior consistent.

## Decision

Allow both entry types, but force both through one canonical normalize+validate pipeline before producing `ContractBundle`.

- Conflicting symbols across sources fail load operation.
- Equivalent symbols are merged with provenance retained.
- Validation rules are identical regardless of source type.

## Consequences

Positive:

- Flexibility for teams using different contract preparation workflows.
- Lower drift risk because runtime model and validators are shared.
- Better auditability via source provenance metadata.

Trade-offs:

- Additional ingestion complexity.
- Need strong parity tests across both entry paths.

## Alternatives Considered

1. Support only raw `.h` input (rejected): limits integration workflows.
2. Support only generated `ctypes` input (rejected): adds generation prerequisite and tooling coupling.

## Requirement Mapping

- GR-009, GR-022, GR-023
