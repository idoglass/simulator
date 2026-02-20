# FR-GR-019

- Source GR ID: GR-019
- Priority: P0
- Status: Implemented

## Feature Requirement
Accept target input and execute simulation flow for that target.

## Acceptance Criteria
- Simulation run requires target input and executes against the selected target context.

## Implementation
- RunInput carries target_id; workflow resolves TargetRef via target_resolver (config/targets.py). Default targets (default-target, default-udp) in get_default_targets(); resolve_target() used at run time. Transport receives resolved TargetRef (host, port, protocol, mode).
