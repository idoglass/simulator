# Implementation Scaffolding Templates

These templates provide implementation starters aligned with architecture artifacts.

## Included Templates

- `port_template.py` - port interface contract starter
- `adapter_template.py` - adapter implementation starter
- `workflow_template.py` - run/workflow orchestration starter
- `config_template.py` - config resolution/validation starter
- `error_handling_template.py` - standardized error envelope starter

## Intended Usage

1. Copy a template into the target module path under `src/simulator/...`.
2. Rename placeholder classes/functions to feature-specific names.
3. Keep contract surfaces aligned with:
   - `architecture/port-contracts.md`
   - `architecture/config-model.md`
   - `architecture/error-codes.md`
4. Add tests using `tests/fixtures/` canonical data.

## Notes

- Templates are scaffolding aids, not runtime production modules.
- Keep business logic in domain/services; adapters translate boundaries only.
