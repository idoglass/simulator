"""Unit tests for SRS entity validators (TKT-C02-01)."""

from __future__ import annotations

from simulator.domain.services.model_validation import (
    validate_endpoint,
    validate_id,
    validate_name,
    validate_timeout_ms,
)


def test_validate_id_accepts_valid() -> None:
    assert validate_id("app1") == []
    assert validate_id("my.app_id-01") == []


def test_validate_id_rejects_empty_and_bad_format() -> None:
    assert "id_required" in validate_id("")
    assert "id_format" in validate_id("bad space")
    assert "id_format" in validate_id("x" * 65)


def test_validate_name_accepts_valid() -> None:
    assert validate_name("My App") == []
    assert validate_name("  trimmed  ".strip()) == []


def test_validate_name_rejects_empty_and_too_long() -> None:
    assert "name_empty" in validate_name("")
    assert "name_too_long" in validate_name("x" * 200)


def test_validate_timeout_ms() -> None:
    assert validate_timeout_ms(5000) == []
    assert "timeout_out_of_range" in validate_timeout_ms(50)
    assert "timeout_out_of_range" in validate_timeout_ms(200_000)


def test_validate_endpoint() -> None:
    assert validate_endpoint("127.0.0.1:8080") == []
    assert "endpoint_port_range" in validate_endpoint("host:0")
    assert "endpoint_format" in validate_endpoint("nocolon")
