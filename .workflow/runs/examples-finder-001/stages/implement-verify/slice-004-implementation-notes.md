# slice-004 — implementation notes

- **generated_at**: 2026-04-02 (slice-implement)
- **run_id**: examples-finder-001

## 决策摘要

1. **`cli.run()`**：捕获 `KeyboardInterrupt`，在 **POSIX**（`os.name != "nt"`）下 `sys.exit(130)`，在 **Windows** 下 `sys.exit(1)`（§8.4：Windows 不承诺 130）。`SystemExit`（含 `argparse` 用法错误 **2**）原样向上抛出，不在此吞掉。

2. **`README.md`**：`examples/finder/README.md` 定稿——uv/pip、子命令、`path`/`text` 选项、相对根解析、UTF-8/二进制/NUL 启发式、stderr 诊断、`path:line:content` 与 Windows 盘符 `:`、symlink 策略、退出码表。

3. **`pyproject.toml`**：`readme = "README.md"`，`description` 更新为 slice-004。

4. **集成测试**：`tests/test_cli_integration.py`——缺子命令/未知子命令/`--help`/`path` 缺 `--name`、同 fixture 下 path+text、`run()` 对 `KeyboardInterrupt` 的映射。

5. **CI（B-14）**：仓库根下 **无** `.github/workflows`，按切片「仅当已有 CI」**不新增** workflow；记为 **deferred**，可在 `slice-verify` 报告中再次确认。
