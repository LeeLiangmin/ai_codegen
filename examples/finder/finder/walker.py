"""Filesystem tree walk with depth limit and symlink policy (§6.2)."""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

from finder.paths import is_within_root, join_child
from finder.types import SearchOptions, WalkEntry


def iter_walk(root: Path, options: SearchOptions) -> Iterator[WalkEntry]:
    """
    Depth-first pre-order walk under *root*.

    - Depth of *root* is 0; immediate children are depth 1.
    - If ``max_depth`` is ``N``, nodes with depth > N are not visited; at depth N,
      directories are still emitted but not descended into.
    - If ``follow_symlinks`` is False (default), directory symlinks are not traversed
      as directories; the symlink path itself may still appear as an entry if the
      parent directory is read (implementation lists dir entries; symlinks to dirs
      are reported via scandir as non-dir when follow_symlinks=False).
    """
    root = root.resolve(strict=True)
    yield from _walk_dir(root, root, 0, options)


def _walk_dir(root: Path, directory: Path, depth: int, options: SearchOptions) -> Iterator[WalkEntry]:
    if not is_within_root(root, directory):
        return
    try:
        is_dir = directory.is_dir(follow_symlinks=options.follow_symlinks)
    except OSError:
        # Unreadable node: skip entire subtree hook (§5.2).
        return

    yield WalkEntry(path=directory, is_directory=is_dir, depth=depth)

    if not is_dir:
        return
    if options.max_depth is not None and depth >= options.max_depth:
        return

    try:
        with os.scandir(directory) as scan:
            entries = list(scan)
    except OSError:
        # Permission or IO error: skip this directory's children (§5.2).
        return

    follow = options.follow_symlinks
    for entry in sorted(entries, key=lambda e: e.name):
        try:
            child = join_child(root, directory, entry.name)
        except ValueError:
            continue
        if not is_within_root(root, child):
            continue
        try:
            if entry.is_symlink() and not follow:
                # Do not recurse through symlink; optionally yield the symlink path as file.
                is_child_dir = False
            else:
                is_child_dir = entry.is_dir(follow_symlinks=follow)
        except OSError:
            continue

        if is_child_dir:
            yield from _walk_dir(root, child, depth + 1, options)
        else:
            yield WalkEntry(path=child, is_directory=False, depth=depth + 1)
