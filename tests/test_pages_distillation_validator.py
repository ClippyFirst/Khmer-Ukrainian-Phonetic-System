from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_pages_distillation_validator_resolves_src_package_without_pythonpath() -> None:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    missing_artifact = ROOT / "does-not-exist-google-distillation-artifact.json"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_google_distilled_syllables.py"), str(missing_artifact)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "ModuleNotFoundError" not in result.stderr
    assert "FileNotFoundError" in result.stderr
