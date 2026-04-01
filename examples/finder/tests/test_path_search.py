"""Unit tests for path_search (slice-002)."""

from __future__ import annotations

import re
from pathlib import Path

from finder.path_search import iter_matching_paths
from finder.paths import resolve_search_root
from finder.types import SearchOptions


def test_basename_regex_search_not_anchored(tmp_path: Path) -> None:
    (tmp_path / "hello.txt").write_text("x")
    (tmp_path / "prehello.txt").write_text("y")
    root = resolve_search_root(tmp_path)
    rx = re.compile(r"hello")
    names = {h.path.name for h in iter_matching_paths(root, rx, "a", SearchOptions())}
    assert names == {"hello.txt", "prehello.txt"}


def test_type_f_only_files(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("x")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "b.txt").write_text("y")
    root = resolve_search_root(tmp_path)
    rx = re.compile(r".")
    opts = SearchOptions(max_depth=None)
    hits = list(iter_matching_paths(root, rx, "f", opts))
    assert all(h.kind == "file" for h in hits)
    assert {h.path.name for h in hits} == {"a.txt", "b.txt"}


def test_type_d_only_directories(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("x")
    sub = tmp_path / "sub"
    sub.mkdir()
    root = resolve_search_root(tmp_path)
    rx = re.compile(r"^s")
    hits = list(iter_matching_paths(root, rx, "d", SearchOptions()))
    assert len(hits) == 1
    assert hits[0].path.name == "sub"
    assert hits[0].kind == "directory"


def test_max_depth_limits_matches(tmp_path: Path) -> None:
    (tmp_path / "root.txt").write_text("x")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "deep.txt").write_text("y")
    root = resolve_search_root(tmp_path)
    rx = re.compile(r"\.txt$")
    hits = list(iter_matching_paths(root, rx, "f", SearchOptions(max_depth=1)))
    names = {h.path.name for h in hits}
    assert "root.txt" in names
    assert "deep.txt" not in names
