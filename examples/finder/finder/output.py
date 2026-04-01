"""Stdout line formatting (§6.5)."""

from __future__ import annotations

from pathlib import Path

from finder.types import TextHit


def format_path_line(path: Path) -> str:
    """One filesystem path per line (§8.2). Uses platform-native path string."""
    return str(path)


def format_text_hit(hit: TextHit) -> str:
    """One hit per line: ``path:line:content`` (§8.1). Collapses embedded newlines in content."""
    path_s = format_path_line(hit.file_path)
    text = hit.line_text.replace("\r", " ").replace("\n", " ")
    return f"{path_s}:{hit.line_number}:{text}"
