# DDS Core 05: Transport Adapter Design

## 1. Purpose

Provide a unified send/receive abstraction over TCP/UDP in client/server modes with strict validation and timeout behavior.

## 2. Adapter Interface

```text
TransportGateway.send_and_receive(
  transport_config,
  message_payload,
  timeout_policy,
  correlation_meta
) -> TransportResult
```

`TransportResult`:

- `send_status`
- `receive_status`
- `response_payload` (optional)
- `timing`
- `error_code` (optional)

## 3. Mode Handling

- TCP client: connect to `remote_endpoint`, send, await response
- TCP server: bind/listen on `local_endpoint`, accept flow handling based on task design
- UDP client: send datagram to `remote_endpoint`, optional response window
- UDP server: bind on `local_endpoint`, receive/request-reply behavior via registered task logic

## 4. Validation Rules

Before runtime:

- endpoint format `host:port`
- port range `1..65535`
- timeout values in configured ranges
- protocol/mode compatibility checks

On failure:

- raise concrete code (`SRS-E-VAL-005` or transport error set)

## 5. Timeout and Retry Application

Timeout precedence:

1. message-level `send_timeout_ms`
2. sequence-level `step_timeout_ms`
3. transport defaults (`connect/read/write`)

Retry is orchestrator-controlled; transport adapter remains attempt-scoped.

## 6. Error Mapping

- open/connect failure -> `SRS-E-TRN-001`
- send timeout -> `SRS-E-TRN-002`
- receive timeout -> `SRS-E-TRN-003`
- peer reset/closed -> `SRS-E-TRN-004`

## 7. Observability Contract

Each attempt emits:

- protocol/mode
- endpoint(s)
- bytes sent/received
- start/end timestamps
- correlation ID and run ID
- success/failure and mapped error code
