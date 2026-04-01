# 设计实现追踪矩阵 — examples-finder-001

来源：`.workflow/docs/design/finder.normalized.md`；代码与测试根：`examples/finder/`。

### 设计实现追踪矩阵

| design_id | design_section | module | interface | code_path | test_path | status | deviation | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6.1 | CLI 入口 | finder | `run()` / argparse 编排 | `examples/finder/finder/cli.py` | `examples/finder/tests/test_cli_path.py`；`test_cli_text.py`；`test_cli_integration.py` | completed | none | `__main__.py` 调用 `run()` |
| 8.1 | `finder text` | finder | `text` 子命令 | `examples/finder/finder/cli.py` | `test_cli_text.py`；`test_cli_integration.py` | completed | none | 默认正则、`--fixed-strings`、glob |
| 8.2 | `finder path` | finder | `path` 子命令 | `examples/finder/finder/cli.py` | `test_cli_path.py`；`test_cli_integration.py` | completed | none | `--name` basename 正则、`--type` |
| 8.3 | `--help` | finder | argparse help | `examples/finder/finder/cli.py` | 集成/手测；验证报告勾选 | completed | none | |
| 8.4 | 退出码 / SIGINT | finder | `SystemExit` / `KeyboardInterrupt` 映射 | `examples/finder/finder/cli.py` | `test_cli_integration.py` 等 | completed | none | Unix 130；Windows 见 README |
| 6.2 | Walker | finder | `iter_walk` | `examples/finder/finder/walker.py` | `examples/finder/tests/test_walker.py` | completed | none | 深度、默认不跟随 symlink |
| 6.3 | ContentSearch | finder | `iter_text_hits_in_file` 等 | `examples/finder/finder/content_search.py` | `examples/finder/tests/test_content_search.py` | completed | none | UTF-8 跳过策略、NUL 启发式、行长上限 |
| 6.4 | PathSearch | finder | `iter_matching_paths` | `examples/finder/finder/path_search.py` | `examples/finder/tests/test_path_search.py` | completed | none | |
| 6.5 | Output | finder | `format_text_hit` / `format_path_line` | `examples/finder/finder/output.py` | 经 path/text CLI 与单测间接覆盖 | completed | none | `path:line:content` |
| 7.1 | SearchOptions / TextHit / PathHit | finder | dataclasses | `examples/finder/finder/types.py` | `test_paths.py`；`test_walker.py`；内容/路径搜索测 | completed | none | 与 §7.1 字段对齐 |
| 4.1 / 6.* | 根解析与安全路径 | finder | `resolve_search_root` 等 | `examples/finder/finder/paths.py` | `examples/finder/tests/test_paths.py` | completed | none | 根下校验、非法根 → 码 3 |
| 5.1 / 8.1 | glob 包含/排除 | finder | `matches_path_globs` | `examples/finder/finder/glob_filter.py` | `test_content_search.py`；CLI 测试 | completed | none | |
| 3.1 / 12.2 | README 与使用说明 | docs | — | `examples/finder/README.md` | 人工与集成报告对照设计 | completed | none | uv、平台差异、编码/二进制说明 |
| B-14 | 可选 CI | 工程 | 仓库 workflow | —（未新增） | — | partial | accepted | 仓库无 `.github/workflows`；按切片 defer，见 `deviations-summary.md` |

**状态说明**：`partial` 仅用于 B-14（计划内可选项未实施）；核心设计模块均为 `completed`。

**覆盖率**：§6 模块、§7 实体、§8 CLI 与退出码、§5 主/异常流程均在代码与测试中体现；§9–§11 以实现与 README 行为体现，无单独代码文件。
