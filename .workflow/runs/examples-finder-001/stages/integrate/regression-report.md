# 回归测试报告 — examples-finder-001

## 元数据

| 项 | 值 |
| --- | --- |
| run_id | examples-finder-001 |
| generated_at | 2026-04-02T02:45:00+08:00 |
| 代码根 | `examples/finder/` |

## 执行命令

```text
cd examples/finder
python -m compileall finder tests -q
uv run --no-sync pytest tests/ -v --tb=short
```

## 环境

- platform: win32（与集成验证执行环境一致）
- Python: 3.14.0（`.venv\Scripts\python.exe`）
- pytest: 9.0.2

## 结果摘要

| 指标 | 值 |
| --- | --- |
| 收集用例 | 43 |
| 通过 | 43 |
| 失败 | 0 |
| 跳过 | 0 |

## 按文件分布

| 测试模块 | 用例数（约） |
| --- | ---: |
| test_cli_integration.py | 6 |
| test_cli_path.py | 6 |
| test_cli_text.py | 7 |
| test_content_search.py | 5 |
| test_path_search.py | 4 |
| test_paths.py | 9 |
| test_walker.py | 5 |

## 结论

**passed** — 回归套件全部通过，未发现既有功能被破坏。
