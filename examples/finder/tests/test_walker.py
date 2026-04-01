"""Tests for iter_walk (slice-001)."""

from __future__ import annotations

from pathlib import Path

import pytest

from finder.paths import resolve_search_root
from finder.types import SearchOptions
from finder.walker import iter_walk


def test_max_depth_zero_yields_only_root(tmp_path: Path) -> None:
    (tmp_path / "file.txt").write_text("x")
    root = resolve_search_root(tmp_path)
    entries = list(iter_walk(root, SearchOptions(max_depth=0)))
    assert len(entries) == 1
    assert entries[0].path == root
    assert entries[0].is_directory
    assert entries[0].depth == 0


def test_max_depth_one_skips_nested_files(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("a")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "b.txt").write_text("b")
    root = resolve_search_root(tmp_path)
    opts = SearchOptions(max_depth=1)
    by_name = {e.path.name: e for e in iter_walk(root, opts)}
    assert "a.txt" in by_name
    assert "sub" in by_name
    assert by_name["a.txt"].depth == 1
    assert "b.txt" not in by_name


def test_default_follow_symlinks_false_skips_symlink_dir_children(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret")
    link = root / "to_outside"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlink not supported")

    r = resolve_search_root(root)
    names = [e.path.name for e in iter_walk(r, SearchOptions(follow_symlinks=False))]
    assert "to_outside" in names
    assert "secret.txt" not in names


def test_follow_symlinks_true_traverses_symlink_dir(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret")
    link = root / "to_outside"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlink not supported")

    r = resolve_search_root(root)
    names = [e.path.name for e in iter_walk(r, SearchOptions(follow_symlinks=True, max_depth=3))]
    assert "secret.txt" in names


def test_walk_depth_numbering(tmp_path: Path) -> None:
    d1 = tmp_path / "l1"
    d1.mkdir()
    d2 = d1 / "l2"
    d2.mkdir()
    (d2 / "leaf.txt").write_text("x")
    root = resolve_search_root(tmp_path)
    entries = list(iter_walk(root, SearchOptions(max_depth=None)))
    root_entry = next(e for e in entries if e.path.resolve() == root.resolve())
    assert root_entry.depth == 0
    l1 = next(e for e in entries if e.path.name == "l1")
    assert l1.depth == 1
    leaf = next(e for e in entries if e.path.name == "leaf.txt")
    # root (0) -> l1 (1) -> l2 (2) -> leaf.txt (3)
    assert leaf.depth == 3
