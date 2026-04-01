"""Path listing by basename regex and type filter (§6.4, §4.1)."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path

from finder.types import PathHit, SearchOptions
from finder.walker import iter_walk


def iter_matching_paths(
    root: Path,
    name_regex: re.Pattern[str],
    type_filter: str,
    options: SearchOptions,
) -> Iterator[PathHit]:
    """
    Walk *root* with *options* and yield `PathHit` for entries whose basename matches
    ``name_regex`` via ``re.search`` (§4.1).

    *type_filter*: ``"f"`` files only, ``"d"`` directories only, ``"a"`` both.
    """
    for entry in iter_walk(root, options):
        if not name_regex.search(entry.path.name):
            continue
        if type_filter == "f" and entry.is_directory:
            continue
        if type_filter == "d" and not entry.is_directory:
            continue
        kind = "directory" if entry.is_directory else "file"
        yield PathHit(path=entry.path, kind=kind)
