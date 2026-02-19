# FR-GR-031

- Source GR ID: GR-031
- Priority: P0
- Status: Draft

## Feature Requirement
Support UDP and TCP protocols for simulation transport in the current project scope.

## Acceptance Criteria
- Simulator can send and receive simulation traffic over TCP.
- Simulator can send and receive simulation traffic over UDP.
- Protocol selection is configurable per simulation target or run configuration.

## Implementation Plan (MVP)

1. Define transport adapter interfaces for TCP and UDP in the shared engine layer.
2. Implement client and server mode behavior for both protocols.
3. Add per-target/run protocol selection in runtime configuration.
4. Add protocol smoke tests for TCP and UDP send/receive paths.
