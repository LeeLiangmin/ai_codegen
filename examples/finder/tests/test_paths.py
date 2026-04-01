"""Tests for path resolution and root-subtree checks (slice-001)."""

from __future__ import annotations

from pathlib import Path

import pytest

from finder.paths import InvalidRootError, is_within_root, join_child, resolve_search_root, safe_join


def test_resolve_search_root_relative(tmp_path: Path) -> None:
    sub = tmp_path / "r"
    sub.mkdir()
    cwd = tmp_path
    got = resolve_search_root("r", cwd=cwd)
    assert got == sub.resolve()


def test_resolve_search_root_missing(tmp_path: Path) -> None:
    with pytest.raises(InvalidRootError):
        resolve_search_root(tmp_path / "nope", cwd=tmp_path)


def test_resolve_search_root_file_not_dir(tmp_path: Path) -> None:
    f = tmp_path / "f.txt"
    f.write_text("x")
    with pytest.raises(InvalidRootError):
        resolve_search_root(f, cwd=tmp_path)


def test_is_within_root_prefix(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    inner = (tmp_path / "a" / "b").resolve()
    inner.parent.mkdir(parents=True)
    assert is_within_root(root, root)
    assert is_within_root(root, inner)


def test_is_within_root_rejects_escape(tmp_path: Path) -> None:
    root = (tmp_path / "root").resolve()
    root.mkdir()
    outside = (tmp_path / "outside").resolve()
    outside.mkdir()
    assert not is_within_root(root, outside)


def test_safe_join_ok(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    a = tmp_path / "a"
    a.mkdir()
    got = safe_join(root, "a", "b")
    assert got == root / "a" / "b"


def test_join_child_under_search_root(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    sub = tmp_path / "sub"
    sub.mkdir()
    got = join_child(root, sub, "f.txt")
    assert got == sub / "f.txt"


def test_join_child_rejects_escape(tmp_path: Path) -> None:
    root = (tmp_path / "root").resolve()
    root.mkdir()
    outside = (tmp_path / "outside").resolve()
    outside.mkdir()
    with pytest.raises(ValueError):
        join_child(root, outside, "x")


def test_safe_join_rejects_dotdot(tmp_path: Path) -> None:
    root = (tmp_path / "root").resolve()
    root.mkdir()
    with pytest.raises(ValueError):
        safe_join(root, "..")


def test_is_within_root_symlink_file_stays_inside(tmp_path: Path) -> None:
    """Symlink path under root counts as inside even if target is outside (§6.2)."""
    root = (tmp_path / "root").resolve()
    root.mkdir()
    outside = (tmp_path / "outside").resolve()
    outside.mkdir()
    link = root / "link"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlink not supported")
    assert is_within_root(root, link)
