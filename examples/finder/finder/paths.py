"""Path resolution and root-subtree checks (§4.1, §4.2, §6.2)."""

from __future__ import annotations

import os
from pathlib import Path


class InvalidRootError(Exception):
    """Raised when the search root is missing, not a directory, or cannot be resolved."""

    pass


def resolve_search_root(raw: str | Path, *, cwd: Path | None = None) -> Path:
    """
    Resolve *raw* to an absolute existing directory.

    Relative paths are resolved against *cwd* (default: process CWD), matching
    the design expectation that CLI roots are resolved before subtree checks.
    """
    cwd = cwd or Path.cwd()
    p = Path(raw)
    if not p.is_absolute():
        p = cwd / p
    try:
        resolved = p.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise InvalidRootError(f"root does not exist or is inaccessible: {raw!r}") from exc
    if not resolved.is_dir():
        raise InvalidRootError(f"root is not a directory: {raw!r}")
    return resolved


def is_within_root(root: Path, candidate: Path) -> bool:
    """
    True if *candidate* is *root* or a path under *root* without following symlinks.

    Uses normpath + normcase prefix comparison so a symlink *file* whose target
    is outside the tree still counts as inside when its path is under *root*
    (default ``follow_symlinks=False`` traversal).
    """
    root_s = os.path.normcase(os.path.normpath(str(root.resolve(strict=True))))
    cand = candidate if candidate.is_absolute() else candidate.resolve(strict=False)
    cand_s = os.path.normcase(os.path.normpath(str(cand)))
    if cand_s == root_s:
        return True
    sep = os.sep
    if not root_s.endswith(sep):
        prefix = root_s + sep
    else:
        prefix = root_s
    return cand_s.startswith(prefix) and cand_s != root_s


def safe_join(search_root: Path, *parts: str | Path) -> Path:
    """Join *parts* onto *search_root*; each step must remain under *search_root* (§6.2)."""
    current = search_root
    for part in parts:
        current = current / part
        if not is_within_root(search_root, current):
            raise ValueError(f"path escapes search root after join: {current}")
    return current


def join_child(search_root: Path, parent: Path, name: str | Path) -> Path:
    """
    ``parent / name`` with containment check against *search_root* (not only *parent*).

    Required for Walker: design §6.2 mandates validation against the user search root
    after every join.
    """
    child = parent / name
    if not is_within_root(search_root, child):
        raise ValueError(f"path escapes search root after join: {child}")
    return child
