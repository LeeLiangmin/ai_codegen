"""Finder example package (slice-001: types, path safety, walker)."""

from finder.paths import InvalidRootError, is_within_root, join_child, resolve_search_root
from finder.types import PathHit, SearchOptions, SearchRoot, TextHit, WalkEntry
from finder.walker import iter_walk

__all__ = [
    "InvalidRootError",
    "PathHit",
    "SearchOptions",
    "SearchRoot",
    "TextHit",
    "WalkEntry",
    "is_within_root",
    "join_child",
    "iter_walk",
    "resolve_search_root",
]
