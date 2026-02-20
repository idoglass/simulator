"""Error code catalog (TKT-S02-02)."""

from __future__ import annotations

SRS_E_VAL = "SRS-E-VAL"
SRS_E_TASK = "SRS-E-TASK"
SRS_E_TRN = "SRS-E-TRN"
SRS_E_VER = "SRS-E-VER"
SRS_E_RUN = "SRS-E-RUN"
SRS_E_INT = "SRS-E-INT"

CATALOG: dict[str, str] = {
    "SRS-E-VAL-001": "validation_failed",
    "SRS-E-TRN-001": "transport_config_invalid",
    "SRS-E-VER-001": "verification_failed",
}
