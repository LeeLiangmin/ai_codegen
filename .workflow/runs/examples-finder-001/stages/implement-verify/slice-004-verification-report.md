# slice-004 验证报告

## 切片标识与验证时间

| 项 | 值 |
| --- | --- |
| run_id | examples-finder-001 |
| slice_id | slice-004 |
| title | §8.4 全链路、SIGINT、README、集成测试与可选 CI |
| verified_at | 2026-04-02T02:30:00+08:00 |
| 设计参考 | `.workflow/docs/design/finder.normalized.md` §5.2、§8.3、§8.4、§10.1、§10.2 |

## 改动清单（本切片范围）

- `examples/finder/finder/cli.py`（`run()`：`KeyboardInterrupt` → 130 POSIX / 1 Windows；`SystemExit` 透传）
- `examples/finder/README.md`（用户文档定稿）
- `examples/finder/pyproject.toml`（`readme = README.md`，`description`）
- `examples/finder/tests/test_cli_integration.py`

## 设计一致性检查结果

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| §8.4 退出码 | 通过 | **0** 成功含零输出（既有 path/text 测）；**2** 用法（缺子命令、未知子命令、`path` 缺 `--name`、非法 `--max-depth`）；**3** 非法根/非法正则；与 README 表一致 |
| SIGINT / Ctrl+C | 通过 | `run()` 映射 `KeyboardInterrupt`：**130** 当 `os.name != "nt"`，**1** 于 Windows；README 写明 Windows 不承诺 130；`test_run_maps_keyboard_interrupt` |
| `--help` | 通过 | 顶层 `finder --help` 列出 `path`/`text`（`test_top_level_help_exit_0`）；子命令 `-h` 既有测试覆盖 |
| README | 通过 | uv/pip、子命令与选项、相对根、编码/二进制/NUL、`path:line:content` 与 `:`、symlink、退出码 |
| 集成测试 | 通过 | `test_cli_integration.py` 跨 path+text fixture |
| 边界 | 通过 | 未引入第三大功能；未弱化路径/symlink 策略 |
| **B-14 CI** | **accepted deferral** | 仓库根 **无** `.github/workflows`；按切片「仅当已有 CI」未新增 job；与 `slice-004-implementation-notes.md` 一致 |

## 自动化检查结果

| 检查项 | 结果 | 命令 / 说明 |
| --- | --- | --- |
| 语法 / 字节码编译 | 通过 | `python -m compileall finder tests -q`（exit 0） |
| 格式 / ruff | 跳过 | 未配置；PATH 无 `ruff` |
| 类型检查 | 跳过 | 未启用 mypy/pyright |
| 单元 / 集成测试 | 通过 | `uv run --no-sync pytest tests/ -v --tb=short` → **43 passed** |
| POSIX SIGINT 130 | 部分自动化 | 非 Windows 上由 `test_run_maps_keyboard_interrupt` 断言 **130**；本机 Windows CI 路径断言 **1**，与 README 一致 |

## 总体结论

**passed** — slice-004 目标达成；全量测试通过；B-14 记为 **deferred/accepted** 并已在实现说明中记录。

## 失败项与修复建议

无。

## 后续建议

1. 运行 **`integration-verify`**（若流水线要求跨切片 E2E/回归）。  
2. 可选：新增 `.github/workflows/*` 调用 `uv sync && uv run pytest`（`examples/finder`）。  
3. **`result-curate`**：矩阵与交付索引。
