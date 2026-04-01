"""Core data shapes aligned with finder.normalized.md §7.1."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class SearchRoot:
    """Logical search root; `path` should be absolute and resolved (directory)."""

    path: Path


@dataclass(frozen=True)
class SearchOptions:
    """Traversal options for Walker (§6.2, §7.1)."""

    max_depth: int | None = None
    follow_symlinks: bool = False


@dataclass(frozen=True)
class TextHit:
    """Content search hit (§7.1)."""

    file_path: Path
    line_number: int  # 1-based, >= 1
    line_text: str


@dataclass(frozen=True)
class PathHit:
    """Path listing hit (§7.1)."""

    path: Path
    kind: Literal["file", "directory"]


@dataclass(frozen=True)
class WalkEntry:
    """Single node emitted by the walker (slice-001 internal protocol)."""

    path: Path
    is_directory: bool
    depth: int
