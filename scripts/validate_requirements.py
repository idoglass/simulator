#!/usr/bin/env python3
"""Repository requirement validation checks for CI."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERAL_REQ = ROOT / "requirements" / "GENERAL_REQUIREMENTS.md"
MASTER_REQ = ROOT / "requirements" / "feat" / "FEATURE_REQUIREMENTS_MASTER.md"
INDEX_REQ = ROOT / "requirements" / "feat" / "INDEX.md"

# FR-GR-001: baseline document must exist and be referenced as baseline in feature specs
BASELINE_REF_PATTERNS = ("GENERAL_REQUIREMENTS.md", "GENERAL_REQUIREMENTS", "baseline")

FEATURE_DOC_EXCLUSIONS = {
    "INDEX.md",
    "FEATURE_REQUIREMENTS_MASTER.md",
    "FEATURE_REQUIREMENTS_TEMPLATE.md",
    "FEATURE_REQUIREMENTS_EXAMPLE_RUNTIME_TASK_LOADING.md",
}


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)


def git_changed_files(base_ref: str | None, head_ref: str | None) -> list[str]:
    if not base_ref or not head_ref:
        return []
    completed = run(["git", "diff", "--name-only", f"{base_ref}...{head_ref}"])
    if completed.returncode != 0:
        # Fallback for odd merge-base cases.
        completed = run(["git", "diff", "--name-only", base_ref, head_ref])
        if completed.returncode != 0:
            print(f"[warn] Unable to compute git diff: {completed.stderr.strip()}")
            return []
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def fail(msg: str, failures: list[str]) -> None:
    print(f"[fail] {msg}")
    failures.append(msg)


def parse_gr_ids(text: str) -> set[str]:
    ids = set()
    for match in re.findall(r"\*\*GR-(\d+):\*\*", text):
        ids.add(f"GR-{int(match):03d}")
    return ids


def parse_master_gr_ids(text: str) -> set[str]:
    return set(re.findall(r"\|\s*FR-GR-\d+\s*\|\s*(GR-\d+)\s*\|", text))


def validate_baseline_requirements_fr_gr_001(failures: list[str]) -> None:
    """FR-GR-001: Keep an enforceable baseline requirements document in repository scope."""
    if not GENERAL_REQ.exists():
        fail(f"FR-GR-001: Missing baseline document {GENERAL_REQ.relative_to(ROOT)}", failures)
        return
    if not MASTER_REQ.exists():
        return
    master_text = MASTER_REQ.read_text(encoding="utf-8")
    if not any(p in master_text for p in BASELINE_REF_PATTERNS):
        fail(
            f"FR-GR-001: FEATURE_REQUIREMENTS_MASTER.md must reference baseline "
            f"({GENERAL_REQ.name}) as baseline reference",
            failures,
        )


def validate_index(index_path: Path, failures: list[str]) -> None:
    if not index_path.exists():
        fail(f"Missing {index_path.relative_to(ROOT)}", failures)
        return

    allowed_status = {"Planned", "In Progress", "Done", "Active", "Blocked"}
    lines = index_path.read_text(encoding="utf-8").splitlines()
    for raw in lines:
        line = raw.strip()
        if not line.startswith("|") or set(line.replace("|", "").strip()) == {"-"}:
            continue
        if "Order" in line and "Status" in line:
            continue

        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or cells[-1] == "---":
            continue
        status = cells[-1]
        if status not in allowed_status:
            fail(f"Invalid status '{status}' in {index_path.name}: {line}", failures)

        # Check links in any cell.
        for cell in cells:
            for rel in re.findall(r"\((\./[^)]+)\)", cell):
                target = (index_path.parent / rel).resolve()
                if not target.exists():
                    fail(
                        f"Broken link in {index_path.name}: {rel} (resolved {target})",
                        failures,
                    )


def validate_feature_baseline_alignment_fr_gr_002(gr_ids: set[str], failures: list[str]) -> None:
    """FR-GR-002: Every feature requirement document must include mapped GR IDs and align to baseline."""
    feat_dir = ROOT / "requirements" / "feat"
    for doc in feat_dir.glob("*.md"):
        if doc.name in FEATURE_DOC_EXCLUSIONS:
            continue
        text = doc.read_text(encoding="utf-8")
        if "Source GR ID:" not in text:
            fail(f"FR-GR-002: {doc.name} missing mapped GR ID ('Source GR ID:')", failures)
        if "## Feature Requirement" not in text:
            fail(f"FR-GR-002: {doc.name} missing '## Feature Requirement' section", failures)
        if "## Acceptance Criteria" not in text:
            fail(f"FR-GR-002: {doc.name} missing '## Acceptance Criteria' section", failures)

        match = re.search(r"Source GR ID:\s*(GR-\d+)", text)
        if not match:
            fail(f"FR-GR-002: {doc.name} has invalid/missing GR reference format", failures)
            continue
        gr = match.group(1)
        if gr not in gr_ids:
            fail(f"FR-GR-002: {doc.name} references {gr} which is not in baseline (conflict or unknown)", failures)


def validate_changed_feature_docs(changed: list[str], failures: list[str]) -> None:
    changed_feature_docs = []
    for path in changed:
        p = Path(path)
        if p.parts[:2] == ("requirements", "feat") and p.suffix == ".md":
            if p.name not in FEATURE_DOC_EXCLUSIONS:
                changed_feature_docs.append(ROOT / p)

    for doc in changed_feature_docs:
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8")
        for required in ("Source GR ID:", "## Feature Requirement", "## Acceptance Criteria"):
            if required not in text:
                fail(f"FR-GR-002: Changed feature doc {doc.name} missing '{required}'", failures)


def validate_runtime_change_requires_feature_doc(changed: list[str], failures: list[str]) -> None:
    if not changed:
        return

    runtime_changed = False
    feature_doc_changed = False
    for path in changed:
        p = Path(path)
        if p.parts[:2] == ("requirements", "feat") and p.suffix == ".md" and p.name not in FEATURE_DOC_EXCLUSIONS:
            feature_doc_changed = True

        # Runtime-impact heuristics.
        if path == "py-gui":
            runtime_changed = True
        if p.suffix == ".py" and not (
            path.startswith("requirements/")
            or path.startswith("skills/")
            or path.startswith("scripts/")
            or path.startswith(".github/")
        ):
            runtime_changed = True
        if path.endswith(".py") and path.startswith("py-gui/"):
            runtime_changed = True

    if runtime_changed and not feature_doc_changed:
        fail(
            "Runtime-impact changes detected but no feature requirement doc was updated under requirements/feat/",
            failures,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", default=None, help="PR base SHA/ref")
    parser.add_argument("--head-ref", default=None, help="PR head SHA/ref")
    args = parser.parse_args()

    failures: list[str] = []

    validate_baseline_requirements_fr_gr_001(failures)
    if failures:
        print("\nRequirement validation failed.")
        return 1

    for required in (GENERAL_REQ, MASTER_REQ, INDEX_REQ):
        if not required.exists():
            fail(f"Missing required file: {required.relative_to(ROOT)}", failures)
            print("\nRequirement validation failed.")
            return 1

    general_text = GENERAL_REQ.read_text(encoding="utf-8")
    master_text = MASTER_REQ.read_text(encoding="utf-8")
    gr_ids = parse_gr_ids(general_text)
    master_gr_ids = parse_master_gr_ids(master_text)

    missing_master = sorted(gr_ids - master_gr_ids)
    if missing_master:
        fail(f"FEATURE_REQUIREMENTS_MASTER.md missing GR rows: {', '.join(missing_master)}", failures)

    extra_master = sorted(master_gr_ids - gr_ids)
    if extra_master:
        fail(f"FEATURE_REQUIREMENTS_MASTER.md has unknown GR rows: {', '.join(extra_master)}", failures)

    validate_index(INDEX_REQ, failures)
    validate_feature_baseline_alignment_fr_gr_002(gr_ids, failures)

    changed = git_changed_files(args.base_ref, args.head_ref)
    validate_changed_feature_docs(changed, failures)
    validate_runtime_change_requires_feature_doc(changed, failures)

    if failures:
        print(f"\nRequirement validation failed with {len(failures)} issue(s).")
        return 1

    print("Requirement validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
