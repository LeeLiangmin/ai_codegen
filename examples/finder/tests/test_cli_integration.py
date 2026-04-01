"""Cross-cutting CLI tests (slice-004): exit codes, help, combined fixtures."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

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


def test_missing_subcommand_exit_2() -> None:
    r = subprocess.run(
        [sys.executable, "-m", "finder"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(ROOT)},
    )
    assert r.returncode == 2


def test_unknown_subcommand_exit_2() -> None:
    r = _run("not-a-command")
    assert r.returncode == 2


def test_top_level_help_exit_0() -> None:
    r = _run("--help")
    assert r.returncode == 0
    assert "path" in r.stdout
    assert "text" in r.stdout


def test_path_missing_name_exit_2(tmp_path: Path) -> None:
    r = _run("path", str(tmp_path))
    assert r.returncode == 2


def test_fixture_path_and_text(tmp_path: Path) -> None:
    d = tmp_path / "sub"
    d.mkdir()
    (d / "note.txt").write_text("hello special-value\n", encoding="utf-8")
    r_path = _run("path", str(tmp_path), "--name", r"\.txt$", "--type", "f")
    assert r_path.returncode == 0
    assert "note.txt" in r_path.stdout
    r_text = _run("text", str(tmp_path), r"special.value", "--glob", "*.txt")
    assert r_text.returncode == 0
    assert "special-value" in r_text.stdout


def test_run_maps_keyboard_interrupt(monkeypatch: pytest.MonkeyPatch) -> None:
    import finder.cli as cli

    def boom() -> int:
        raise KeyboardInterrupt

    monkeypatch.setattr(cli, "main", boom)
    expected = 130 if os.name != "nt" else 1
    with pytest.raises(SystemExit) as excinfo:
        cli.run()
    assert excinfo.value.code == expected
