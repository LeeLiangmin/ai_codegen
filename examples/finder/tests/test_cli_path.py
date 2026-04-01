"""CLI integration tests for `finder path` (slice-002)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    return subprocess.run(
        [sys.executable, "-m", "finder", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=env,
    )


def test_path_success_zero_matches(tmp_path: Path) -> None:
    r = _run("path", str(tmp_path), "--name", r"^nomatch$")
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_path_lists_matches(tmp_path: Path) -> None:
    (tmp_path / "foo.txt").write_text("a")
    (tmp_path / "bar.py").write_text("b")
    r = _run("path", str(tmp_path), "--name", r"\.txt$")
    assert r.returncode == 0
    lines = [ln for ln in r.stdout.splitlines() if ln.strip()]
    assert len(lines) == 1
    assert lines[0].endswith("foo.txt")


def test_path_invalid_regex_exit_3() -> None:
    r = _run("path", ".", "--name", "(")
    assert r.returncode == 3
    assert "regex" in r.stderr.lower() or "invalid" in r.stderr.lower()


def test_path_missing_root_exit_3(tmp_path: Path) -> None:
    missing = tmp_path / "nope"
    r = _run("path", str(missing), "--name", "x")
    assert r.returncode == 3


def test_path_max_depth_invalid_exit_2(tmp_path: Path) -> None:
    r = _run("path", str(tmp_path), "--name", ".", "--max-depth", "-1")
    assert r.returncode == 2


def test_path_help() -> None:
    r = _run("path", "-h")
    assert r.returncode == 0
    assert "--name" in r.stdout
