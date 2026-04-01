"""CLI integration tests for `finder text` (slice-003)."""

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


def test_text_zero_hits_exit_0(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("hello\n")
    r = _run("text", str(tmp_path), r"nomatch\d+")
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_text_regex_match(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("one\ntwo three\n")
    r = _run("text", str(tmp_path), r"thr..")
    assert r.returncode == 0
    lines = [ln for ln in r.stdout.splitlines() if ln.strip()]
    assert len(lines) == 1
    assert ":2:" in lines[0]
    assert "three" in lines[0]


def test_text_fixed_strings(tmp_path: Path) -> None:
    (tmp_path / "x.txt").write_text("a*b\n")
    r = _run("text", str(tmp_path), "a*b", "--fixed-strings")
    assert r.returncode == 0
    assert "a*b" in r.stdout


def test_text_invalid_regex_exit_3(tmp_path: Path) -> None:
    r = _run("text", str(tmp_path), "(")
    assert r.returncode == 3


def test_text_invalid_root_exit_3(tmp_path: Path) -> None:
    r = _run("text", str(tmp_path / "missing"), "x")
    assert r.returncode == 3


def test_text_glob_include(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("needle\n")
    (tmp_path / "b.py").write_text("needle\n")
    r = _run("text", str(tmp_path), "needle", "--glob", "*.txt")
    assert r.returncode == 0
    assert r.stdout.count("needle") == 1
    assert "a.txt" in r.stdout


def test_text_help() -> None:
    r = _run("text", "-h")
    assert r.returncode == 0
    assert "--fixed-strings" in r.stdout
