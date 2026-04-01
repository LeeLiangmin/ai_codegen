# slice-003 — implementation notes

- **generated_at**: 2026-04-02 (slice-implement)
- **run_id**: examples-finder-001

## 决策摘要

1. **`finder text ROOT PATTERN`**：`--regex`（默认，与「两者都不传」等价）与 `--fixed-strings` 互斥；`--max-depth`、`--glob` / `--glob-exclude`（可重复）与 Walker 组合；仅处理**文件**节点（跳过目录）。

2. **Glob**：`glob_filter.matches_path_globs` 对相对根的 `as_posix()` 路径及 **basename** 做 `fnmatch`；无 `--glob` 时不做 include 过滤。

3. **ContentSearch**：UTF-8 严格解码；`UnicodeDecodeError` 时跳过该文件并 **stderr 一行**（`skip (not valid UTF-8): path`）。首 **8192** 字节含 **NUL** 则视为二进制并跳过（§9.2）。超长行：仅在首 `MATCH_MAX_CHARS`（256KiB）窗口内做匹配；`TextHit.line_text` 展示截断至 `DISPLAY_MAX_CHARS`（4096）加 `...`。

4. **Output**：`format_text_hit` → `path:line:content`，行内换行压成空格；Windows 盘符与 `:` 冲突留 slice-004 README。

5. **`finder path`**：逻辑未改；回归测试 37 项全通过。
