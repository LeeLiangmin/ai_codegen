"""Unit tests for content_search and glob_filter (slice-003)."""

from __future__ import annotations

import re
from pathlib import Path

from finder.content_search import iter_text_hits_in_file
from finder.glob_filter import matches_path_globs
from finder.paths import resolve_search_root


def test_glob_include_basename(tmp_path: Path) -> None:
    root = resolve_search_root(tmp_path)
    a = tmp_path / "a.txt"
    a.write_text("x")
    b = tmp_path / "b.py"
    b.write_text("y")
    assert matches_path_globs(root, a, ["*.txt"], [])
    assert not matches_path_globs(root, b, ["*.txt"], [])


def test_glob_exclude(tmp_path: Path) -> None:
    root = resolve_search_root(tmp_path)
    a = tmp_path / "keep.txt"
    a.write_text("x")
    assert matches_path_globs(root, a, [], ["*.py"])
    assert not matches_path_globs(root, a, [], ["*.txt"])


def test_regex_hit(tmp_path: Path) -> None:
    f = tmp_path / "t.txt"
    f.write_text("hello world\nline two\n")
    rx = re.compile(r"world")
    hits = list(
        iter_text_hits_in_file(f, use_regex=True, pattern="", regex=rx, on_skip=None),
    )
    assert len(hits) == 1
    assert hits[0].line_number == 1
    assert "world" in hits[0].line_text


def test_fixed_string_special_chars_not_regex(tmp_path: Path) -> None:
    f = tmp_path / "t.txt"
    f.write_text("a+b.txt line\n")
    hits = list(
        iter_text_hits_in_file(
            f,
            use_regex=False,
            pattern="a+b",
            regex=None,
            on_skip=None,
        ),
    )
    assert len(hits) == 1


def test_binary_file_skipped(tmp_path: Path) -> None:
    f = tmp_path / "bin.dat"
    f.write_bytes(b"\x00\x01\x02")
    hits = list(
        iter_text_hits_in_file(
            f,
            use_regex=True,
            pattern="x",
            regex=re.compile("x"),
            on_skip=None,
        ),
    )
    assert hits == []
