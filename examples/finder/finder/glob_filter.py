"""Path glob include/exclude for text search (§8.1), using fnmatch on paths under root."""

from __future__ import annotations

import fnmatch
from pathlib import Path


def matches_path_globs(
    root: Path,
    file_path: Path,
    includes: list[str],
    excludes: list[str],
) -> bool:
    """
    *file_path* must be under *root*. If *includes* is empty, any path passes the include stage.
    Then exclude if any *excludes* pattern matches the relative path (posix) or basename.
    """
    try:
        rel = file_path.relative_to(root.resolve())
    except ValueError:
        return False
    rel_posix = rel.as_posix()
    base = rel.name

    if includes:
        if not any(
            fnmatch.fnmatch(rel_posix, pat) or fnmatch.fnmatch(base, pat) for pat in includes
        ):
            return False

    if excludes and any(
        fnmatch.fnmatch(rel_posix, pat) or fnmatch.fnmatch(base, pat) for pat in excludes
    ):
        return False
    return True
