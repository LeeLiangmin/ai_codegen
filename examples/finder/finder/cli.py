"""CLI entry: subcommands and exit codes (§6.1, §8.4)."""

from __future__ import annotations

import argparse
import os
import re
import sys

from finder.content_search import iter_text_hits_in_file
from finder.glob_filter import matches_path_globs
from finder.output import format_path_line, format_text_hit
from finder.path_search import iter_matching_paths
from finder.paths import InvalidRootError, resolve_search_root
from finder.types import SearchOptions
from finder.walker import iter_walk


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="finder",
        description="Find files and text under a directory (example CLI).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_path = sub.add_parser("path", help="List paths under ROOT matching --name regex.")
    p_path.add_argument("root", help="Search root directory")
    p_path.add_argument(
        "--name",
        required=True,
        metavar="PATTERN",
        help="Python regex matched against each path's basename (re.search)",
    )
    p_path.add_argument(
        "--type",
        dest="type_filter",
        choices=["f", "d", "a"],
        default="a",
        help="f=files only, d=directories only, a=all (default)",
    )
    p_path.add_argument(
        "--max-depth",
        type=int,
        default=None,
        metavar="N",
        help="Maximum depth below root (root depth is 0); omit for unlimited",
    )

    p_text = sub.add_parser("text", help="Search file contents under ROOT for PATTERN (§8.1).")
    p_text.add_argument("root", help="Search root directory")
    p_text.add_argument("pattern", help="Search pattern (regex by default, or literal with --fixed-strings)")
    mode = p_text.add_mutually_exclusive_group()
    mode.add_argument(
        "--regex",
        action="store_true",
        help="Treat PATTERN as Python regex (default if neither mode flag is set)",
    )
    mode.add_argument(
        "--fixed-strings",
        action="store_true",
        help="Treat PATTERN as a literal substring (mutually exclusive with --regex)",
    )
    p_text.add_argument(
        "--max-depth",
        type=int,
        default=None,
        metavar="N",
        help="Maximum depth below root (root depth is 0); omit for unlimited",
    )
    p_text.add_argument(
        "--glob",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Include only files matching this fnmatch pattern (relative path or basename); repeatable",
    )
    p_text.add_argument(
        "--glob-exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Exclude files matching this fnmatch pattern; repeatable",
    )

    return parser


def _run_path(args: argparse.Namespace) -> int:
    if args.max_depth is not None and args.max_depth < 0:
        print("error: --max-depth must be >= 0", file=sys.stderr)
        return 2

    try:
        root = resolve_search_root(args.root)
    except InvalidRootError as exc:
        print(str(exc), file=sys.stderr)
        return 3

    try:
        regex = re.compile(args.name)
    except re.error as exc:
        print(f"invalid --name regex: {exc}", file=sys.stderr)
        return 3

    options = SearchOptions(max_depth=args.max_depth, follow_symlinks=False)
    for hit in iter_matching_paths(root, regex, args.type_filter, options):
        line = format_path_line(hit.path)
        print(line)
    return 0


def _run_text(args: argparse.Namespace) -> int:
    if args.max_depth is not None and args.max_depth < 0:
        print("error: --max-depth must be >= 0", file=sys.stderr)
        return 2

    try:
        root = resolve_search_root(args.root)
    except InvalidRootError as exc:
        print(str(exc), file=sys.stderr)
        return 3

    use_regex = not args.fixed_strings
    compiled: re.Pattern[str] | None = None
    if use_regex:
        try:
            compiled = re.compile(args.pattern)
        except re.error as exc:
            print(f"invalid pattern (regex): {exc}", file=sys.stderr)
            return 3

    def on_skip(msg: str) -> None:
        print(msg, file=sys.stderr)

    options = SearchOptions(max_depth=args.max_depth, follow_symlinks=False)
    includes: list[str] = list(args.glob)
    excludes: list[str] = list(args.glob_exclude)

    for entry in iter_walk(root, options):
        if entry.is_directory:
            continue
        if not matches_path_globs(root, entry.path, includes, excludes):
            continue
        for hit in iter_text_hits_in_file(
            entry.path,
            use_regex=use_regex,
            pattern=args.pattern,
            regex=compiled,
            on_skip=on_skip,
        ):
            print(format_text_hit(hit))
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "path":
        return _run_path(args)
    if args.command == "text":
        return _run_text(args)
    parser.error("unknown command")
    return 2


def run() -> None:
    """
    Entry point for console script / ``python -m finder``.

    Maps ``KeyboardInterrupt`` (Ctrl+C / SIGINT) to exit **130** on POSIX per §8.4;
    on Windows uses **1** (platform does not guarantee 130; see README).
    ``argparse`` usage errors propagate as ``SystemExit(2)`` unchanged.
    """
    try:
        code = main()
    except KeyboardInterrupt:
        sys.exit(130 if os.name != "nt" else 1)
    except SystemExit:
        raise
    sys.exit(code)
