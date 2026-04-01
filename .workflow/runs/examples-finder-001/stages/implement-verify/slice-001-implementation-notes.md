# slice-001 — implementation notes

- **generated_at**: 2026-04-01 (slice-implement)
- **run_id**: examples-finder-001

## 决策摘要

1. **`join_child(search_root, parent, name)`**  
   Walker 在枚举子项时，每次 `parent / name` 后按**用户搜索根** `search_root` 做 `is_within_root` 校验（`finder.normalized.md` §6.2），与仅相对父目录校验相比，更直接对齐设计表述，并避免边界歧义。

2. **`is_within_root`**  
   使用 `normpath` + `normcase` 前缀判断，**不**对候选路径做 `resolve()`，以便符号链接路径只要位于根下仍视为「在树内」（默认不跟随 symlink 的语义与设计 §4.1、§5.2 一致）。

3. **依赖与运行**  
   `pyproject.toml` 使用 `[dependency-groups]` + `[tool.uv] default-groups`，推荐 `uv sync` / `uv run pytest`；保留 `[project.optional-dependencies] dev` 供 `pip install -e ".[dev]"` 备用。

4. **权限 / IO 错误**  
   目录不可读时跳过该节点子项（§5.2）；未做 stderr 警告，后续 CLI 层可补充。

## 测试

- `tests/test_paths.py`、`tests/test_walker.py`：根非法、`max_depth`、symlink 不跟随、深度编号等。
- 本地执行：`PYTHONPATH=. python -m pytest tests/ -q`（或 `uv run pytest tests/ -q`）。
