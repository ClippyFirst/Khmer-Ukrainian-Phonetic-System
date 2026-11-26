"""Regression coverage for the standalone Pages artifact validator."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_google_distilled_syllables.py"


def test_validator_bootstraps_repository_src_without_editable_install() -> None:
    result = subprocess.run(
        [sys.executable, "-I", str(VALIDATOR)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "the following arguments are required: artifact" in result.stderr
    assert "ModuleNotFoundError" not in result.stderr
