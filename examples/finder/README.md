# Finder example (`finder-example`)

Small **Python 3.10+** CLI that lists paths by name (`finder path`) and searches file contents (`finder text`). It demonstrates a design-driven layout under `examples/finder/` (see also `DESIGN.md`).

## Install (uv)

From this directory:

```bash
uv sync
```

Run the CLI without a global install:

```bash
uv run finder --help
uv run pytest tests/ -q
```

Or install the package in editable mode:

```bash
uv pip install -e .
finder --help
```

Pip fallback: `pip install -e ".[dev]"` then `python -m pytest`.

## How to run

- **Installed script**: `finder <subcommand> ...`
- **Module**: `python -m finder <subcommand> ...` (set `PYTHONPATH=.` to the repo root of this example if not installed)

## Subcommands

### `finder path`

List paths under `ROOT` whose **basename** matches a Python regex (`re.search`).

```bash
finder path /path/to/root --name '\.txt$' --type f --max-depth 3
```

| Flag | Meaning |
| --- | --- |
| `--name PATTERN` | Required. Regex vs each path’s final segment. |
| `--type f\|d\|a` | Files only, directories only, or all (default `a`). |
| `--max-depth N` | Root depth is `0`; omit for unlimited. |

### `finder text`

Search **UTF-8 text files** line by line under `ROOT`.

```bash
finder text /path/to/root 'needle' --glob '*.md' --max-depth 5
finder text /path/to/root 'a+b' --fixed-strings
```

| Flag | Meaning |
| --- | --- |
| `PATTERN` | **Regex** by default; use `--fixed-strings` for literal substring. |
| `--regex` | Explicit regex mode (same as default). Mutually exclusive with `--fixed-strings`. |
| `--max-depth N` | Same depth rules as `path`. |
| `--glob` / `--glob-exclude` | Repeatable `fnmatch` patterns on relative path or basename. |

**Encoding & binary**

- Files are read as **UTF-8** with strict decoding. Invalid UTF-8 files are **skipped**; a line is printed to **stderr**: `skip (not valid UTF-8): <path>`.
- If the first **8192** bytes contain a **NUL** byte, the file is treated as **binary** and skipped (no stderr line).

**Output format (`text`)**

- Each hit is one stdout line: `path:lineNumber:lineContent`.
- Embedded newlines in the matched line are replaced with spaces in the printed field.
- On **Windows**, paths can contain `:` (drive letter). Only the **first** `:` separates path from line number; drive-prefixed paths still parse as `D:\...:<line>:...` readers should expect.

## Relative roots

Non-absolute `ROOT` is resolved against the **process current working directory** first, then validated as an existing directory under the same rules as absolute paths.

## Symlinks & safety

- **Symbolic links** to directories are **not** followed by default (no traversal into symlink targets).
- Path joins are checked so traversal stays under the user-provided root (see design §6.2).

## Exit codes (§8.4)

| Code | Meaning |
| --- | --- |
| `0` | Scan finished successfully, including **zero** matches / zero stdout lines. |
| `2` | Usage error (unknown flags, missing required args, invalid `--max-depth`, etc.). |
| `3` | Unrecoverable error (missing/non-directory root, invalid regex where applicable). |
| `130` | **POSIX / Unix-like**: interrupted (Ctrl+C / SIGINT), `128 + SIGINT`. |
| **Windows** | Ctrl+C typically exits with **`1`** in this implementation; **130 is not guaranteed**. |

## Development

```bash
uv run pytest tests/ -v
```

## Limitations (by design)

- No indexing daemon, no archive contents, no network search.
- Not `grep`: success is always exit `0` when the scan completes, even with no hits.
