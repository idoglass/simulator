#!/usr/bin/env python3
"""CI test runner: execute required regression suites (TKT-S04-01, TKT-S04-02)."""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"], timeout=300)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
