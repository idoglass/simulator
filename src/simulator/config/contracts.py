"""Contract listing helpers from runtime config."""

from __future__ import annotations

from typing import Any


def list_contracts(config: dict[str, Any]) -> list[dict[str, str]]:
    """Extract target contract summaries in deterministic order."""
    rows = config.get("targets", [])
    if not isinstance(rows, list):
        return []

    contracts: list[dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        target_id = str(row.get("target_id", "")).strip()
        contract = row.get("contracts", {})
        if not target_id or not isinstance(contract, dict):
            continue

        source_ref = str(contract.get("source_ref", "")).strip()
        entry_type = str(contract.get("entry_type", "")).strip()
        if not source_ref:
            continue

        contracts.append(
            {
                "target_id": target_id,
                "source_ref": source_ref,
                "entry_type": entry_type or "unknown",
            }
        )

    return sorted(contracts, key=lambda item: (item["target_id"], item["source_ref"]))

