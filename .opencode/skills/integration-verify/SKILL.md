---
name: integration-verify
description: Use when all slices are verified and you need cross-slice integration checks, E2E flows, and regression before closing the run
---

# integration-verify

全切片 `verified` 后做跨模块、E2E、回归；写 `integrate/integration-report.md`、`regression-report.md`；更新 `state.md`（`current_stage` → `integrating` 再记结果）。

## 输入

全部切片、`*.normalized.md`、`state.md`。

## 步骤

1. 确认 §4 均为 passed。  
2. 从设计抽取关键链路；查模块间接口与数据流；跑集成/回归测试（项目约定）。  
3. 汇总 pass/fail；失败项写入报告；必要时 `unresolved-integration-issues.md`。

## Gate

关键链路 + 集成测试 + 回归均通过 → 可进 `result-curate`。

## 失败

定位相关切片 → `slice-implement` → `slice-verify` → 再集成。非关键失败可记 `accepted deviation` 并注明。
