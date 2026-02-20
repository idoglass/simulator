# FR-GR-022

- Source GR ID: GR-022
- Priority: P0
- Status: Implemented

## Feature Requirement
Use `.h`/`ctypes` metadata from repository-managed and/or user-provided files for message structures, participants, and flow rules.

## Acceptance Criteria
- Invalid type or field references are rejected during validation regardless of definition source.

## Implementation
- **ContractPort** in domain/ports; **StubContractAdapter** in adapters/contracts. load_sources and validate_message implemented; stub accepts all. Full .h/ctypes validation can be added in adapters/contracts.
