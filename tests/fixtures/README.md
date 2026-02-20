# Canonical Fixture Pack

These fixtures are canonical reference data for implementation and tests.

## Fixture Sets

- `contracts/raw/` - sample `.h` contract source
- `contracts/ctypes/` - sample generated ctypes contract source
- `tasks/` - runtime task examples (`.task.json`)
- `config/` - runtime configuration examples
- `captures/` - capture/replay artifacts (`.capture.json`)

## Usage

1. Use as baseline deterministic inputs for unit/integration tests.
2. Copy and mutate in test-specific directories when a scenario needs variants.
3. Keep fixture schema aligned with architecture specs:
   - `architecture/task-format.md`
   - `architecture/config-model.md`
   - `architecture/capture-schema-versioning.md`
