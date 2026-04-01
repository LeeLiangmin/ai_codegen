# slice-002 — implementation notes

- **generated_at**: 2026-04-01 (slice-implement)
- **run_id**: examples-finder-001

## 决策摘要

1. **CLI**：`argparse` 子命令 `path`（`finder path ROOT --name PATTERN [--type f|d|a] [--max-depth N]`）与占位子命令 `text`（固定 stderr + 退出码 **2**，满足 slice-002 不实现内容搜索）。入口：`python -m finder` 与 `[project.scripts] finder = finder.cli:run`。

2. **PathSearch**：`iter_matching_paths(root, name_regex, type_filter, options)` 基于 `iter_walk`；basename 使用 `re.search`（§4.1）；`--type` 与 `WalkEntry.is_directory` 对应 f/d/a。

3. **Output**：`format_path_line` 使用 `str(Path)`，平台原生路径字符串；`path:line:content` 留待 slice-003。

4. **退出码**：非法 `--max-depth`（负数）→ **2**；`InvalidRootError` / `re.error`（`--name`）→ **3**；扫描完成（含零行输出）→ **0**。

5. **测试**：`tests/test_path_search.py` 单元测试；`tests/test_cli_path.py` 子进程 `python -m finder` + `PYTHONPATH=项目根`。
