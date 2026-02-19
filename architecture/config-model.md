# Configuration Model (MVP)

This document defines runtime configuration shape, precedence rules, per-target/per-run overrides, and validation behavior.

## 1) Scope

- Defines how configuration is represented in a canonical runtime model.
- Defines how protocol behavior is configured for TCP/UDP client/server modes.
- Defines how run-time overrides are applied without breaking stateless execution boundaries.
- Covers portability checks required by the compatibility matrix (MVP: Windows and Linux).

## 2) Configuration Layers and Precedence

Configuration is resolved from multiple layers. Higher layers override lower layers.

Lowest -> highest precedence:

1. built-in defaults (application code)
2. project configuration file values
3. target-level configuration values
4. run-level override values (from GUI/TUI run form or API command)

Rules:

1. Resolution is deterministic ("last applicable layer wins").
2. Unknown keys are rejected during validation (no silent ignore).
3. Run-level overrides are ephemeral and must not mutate persisted target/project config.
4. A resolved snapshot is produced before run start and attached to run metadata.

## 3) Canonical Runtime Configuration Shape

The simulator loads file/source config and normalizes it to this runtime model.

```json
{
  "config_version": "1",
  "app": {
    "mode": "gui|tui",
    "log_level": "DEBUG|INFO|WARN|ERROR"
  },
  "compatibility": {
    "supported_os": ["windows", "linux"],
    "supported_arch": ["x86_64"],
    "python_version_range": ">=3.11,<3.14"
  },
  "targets": [
    {
      "target_id": "string",
      "name": "string",
      "transport": {
        "protocol": "tcp|udp",
        "mode": "client|server",
        "host": "string",
        "port": 1,
        "framing": {
          "id": "string|null"
        },
        "timeouts": {
          "connect_timeout_ms": 1000,
          "read_timeout_ms": 1000,
          "write_timeout_ms": 1000
        },
        "retries": {
          "max_retries": 0,
          "retry_backoff_ms": 0
        }
      },
      "contracts": {
        "source_ref": "string",
        "entry_type": "h_dir|ctypes_dir"
      },
      "defaults": {
        "task_id": "string|null",
        "capture_enabled": false
      }
    }
  ]
}
```

## 4) Run Request and Override Shape

A run request references a configured target and may provide overrides.

```json
{
  "target_id": "target-a",
  "task_id": "task-123",
  "overrides": {
    "transport": {
      "protocol": "udp",
      "mode": "client",
      "timeouts": {
        "read_timeout_ms": 2000
      }
    },
    "verification": {
      "rules_source": "inline|file|capture_metadata"
    },
    "capture": {
      "enabled": true,
      "output_path": "captures/latest.json"
    },
    "logging": {
      "log_level": "DEBUG"
    }
  }
}
```

Override rules:

1. `target_id` is required and must exist.
2. `task_id` override is optional; if missing, target default may be used.
3. Override objects are partial patches over the resolved target config.
4. Illegal override keys or type mismatches fail validation before run start.

## 5) Transport Configuration Rules (GR-031 Alignment)

Transport config in resolved runtime config must satisfy:

1. `protocol` in `{tcp, udp}`.
2. `mode` in `{client, server}`.
3. `host` non-empty and `port` in valid range (`1..65535`).
4. `read_timeout_ms` and `write_timeout_ms` must be positive integers.
5. `connect_timeout_ms` is required for TCP client mode.
6. `connect_timeout_ms` is optional/ignored for UDP mode.
7. Framing identifier is required when selected flow depends on framing.
8. Retry settings must be deterministic (`max_retries >= 0`, non-negative backoff).

This configuration model is the input contract for `architecture/transport-spec.md`.

## 6) Portability and Compatibility Matrix Rules (GR-011 Alignment)

`compatibility` config declares supported environments and is validated at startup:

1. `supported_os` must explicitly include MVP OS values: `windows`, `linux`.
2. `supported_arch` must be explicit (for example `x86_64`).
3. `python_version_range` must be parseable and validated against runtime.
4. Startup environment check result must be explicit:
   - compatible -> continue startup
   - incompatible -> fail fast with clear actionable error
5. GUI mode startup must validate GUI runtime prerequisites; TUI mode startup must validate TUI prerequisites.

## 7) Resolution Algorithm (Before Run Start)

1. Load project config.
2. Validate project config schema and compatibility section.
3. Resolve target by `target_id`.
4. Merge defaults + project + target + run overrides.
5. Validate merged result (schema + semantic rules).
6. Emit immutable `ResolvedRunConfig` snapshot.
7. Start run only if snapshot is valid.

## 8) Validation Categories and Error Codes

Validation failures must return structured deterministic errors:

- `CONFIG_SCHEMA_INVALID`
- `CONFIG_UNKNOWN_KEY`
- `CONFIG_TYPE_MISMATCH`
- `CONFIG_TARGET_NOT_FOUND`
- `CONFIG_PROTOCOL_INVALID`
- `CONFIG_PORT_INVALID`
- `CONFIG_TIMEOUT_INVALID`
- `CONFIG_FRAMING_REQUIRED`
- `CONFIG_COMPATIBILITY_UNSUPPORTED`
- `CONFIG_OVERRIDE_INVALID`

Each error should include:

- `code`
- `message`
- `path` (JSON-style path to invalid field)
- `run_id` (when available)
- `target_id` (when available)

## 9) Persistence and Stateless Boundary

1. Persisted configuration is source-of-truth for defaults and targets.
2. Per-run resolved config is immutable run metadata.
3. Run overrides must not mutate persisted configuration.
4. No mutable per-target execution state is retained between runs in process.

## 10) Architecture-Level Test Expectations

Minimum tests for configuration model:

1. valid project config + target config resolves successfully
2. run-level override precedence over target/project defaults
3. unknown key rejection
4. invalid protocol/mode rejection
5. missing TCP client `connect_timeout_ms` rejection
6. invalid port/timeouts rejection
7. unsupported OS/runtime compatibility rejection
8. deterministic `ResolvedRunConfig` for identical inputs

## 11) Requirement Mapping

- GR-011, GR-031
