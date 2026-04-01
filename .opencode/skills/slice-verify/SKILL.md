---
name: slice-verify
description: Use when a slice is implemented and you need design-consistency checks, lint, typecheck, tests, and a written verification report with pass or fail
---

# slice-verify

对切片做设计一致性 + 项目 fmt/lint/类型/测试；写 `slice-<NNN>-verification-report.md`；更新切片与 `state.md`。

## 前置

切片 `implemented`；改动已就绪。

## 步骤

1. 对照切片目标与设计：接口、数据、无越权扩展。  
2. 运行仓库约定命令（如 `cargo fmt/clippy/test`、`npm test`、`tsc` 等）。  
3. 报告：命令、结果、结论 `passed`/`failed`；失败时写清项与修复方向。  
4. 切片 `verified` 或保持失败待修；`state.md` 同步。

## 产出

`stages/implement-verify/slice-<NNN>-verification-report.md`；可选 `failed-checks` 等。

## Gate

设计一致 + fmt + lint + 类型/编译 + 相关测试均通过 → `verified`。

## 失败

自动 fmt 可试 1～2 次；仍失败 → 回 `slice-implement`。反复多次 → 标 `escalated` 并人工。
