# Transport Adapters

Transport adapters connect network protocol behavior to shared simulator services.

- `tcp/`: TCP client/server adapter implementations.
- `udp/`: UDP client/server adapter implementations.

## Responsibilities

- Manage protocol-specific send/receive mechanics.
- Convert transport I/O into domain-level message contracts.
- Surface deterministic errors/timeouts to the core service layer.

## Non-responsibilities

- No UI rendering or command handling.
- No scenario/business rules outside transport concerns.
