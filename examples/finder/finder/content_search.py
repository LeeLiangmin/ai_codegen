"""
Content search by line (§6.3, §9.2).

Encoding: UTF-8 only. On ``UnicodeDecodeError`` the file is skipped; the caller may pass
``on_skip`` to emit a diagnostic (slice-003: skip + optional stderr line).

Binary heuristic: if the first BINARY_SNIFF bytes contain NUL, the file is skipped (§9.2).

Line length: lines longer than ``MATCH_MAX_CHARS`` are only scanned in their prefix for
matching; ``TextHit.line_text`` is truncated to ``DISPLAY_MAX_CHARS`` with ``...`` suffix.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from pathlib import Path

from finder.types import TextHit

BINARY_SNIFF = 8192
# Match within first N chars of a line to bound memory on extreme lines (§6.3).
MATCH_MAX_CHARS = 256 * 1024
DISPLAY_MAX_CHARS = 4096


def is_probably_binary(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            chunk = f.read(BINARY_SNIFF)
    except OSError:
        return True
    return b"\x00" in chunk


def _trim_display(text: str) -> str:
    if len(text) <= DISPLAY_MAX_CHARS:
        return text
    return text[:DISPLAY_MAX_CHARS] + "..."


def iter_text_hits_in_file(
    path: Path,
    *,
    use_regex: bool,
    pattern: str,
    regex: re.Pattern[str] | None,
    on_skip: Callable[[str], None] | None = None,
) -> Iterator[TextHit]:
    """
    Yield ``TextHit`` for lines matching *pattern*.

    *use_regex*: if True, *regex* must be a compiled pattern and is used with ``.search``;
    if False, *pattern* is a literal substring (``in``) on the line without trailing newline.
    """
    if is_probably_binary(path):
        return

    try:
        with path.open("r", encoding="utf-8", newline="") as f:
            for line_no, line in enumerate(f, start=1):
                raw = line.rstrip("\n\r")
                window = raw if len(raw) <= MATCH_MAX_CHARS else raw[:MATCH_MAX_CHARS]
                if use_regex:
                    assert regex is not None
                    if not regex.search(window):
                        continue
                else:
                    if pattern not in window:
                        continue
                yield TextHit(
                    file_path=path,
                    line_number=line_no,
                    line_text=_trim_display(raw),
                )
    except UnicodeDecodeError:
        if on_skip is not None:
            on_skip(f"skip (not valid UTF-8): {path}")
        return
    except OSError:
        return
