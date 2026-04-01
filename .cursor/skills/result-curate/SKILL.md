---
name: result-curate
description: Use when integration verification passed and you need traceability matrix, deviations summary, delivery index, and next-iteration context for archival
---

# result-curate

汇总设计→代码→验证映射与交付物；写 `curate/` 下文件；`state.md` 收尾（`current_stage: close`，`status: completed` 若适用）。

## 前置

集成验证通过（或项目约定等价条件）。

## 步骤

1. 建 `traceability-matrix.md`：设计项 ↔ 代码/测试路径 ↔ 状态（完成/部分/缺）↔ 偏差。  
2. `deviations-summary.md`：汇总各 `*-deviation.md`。  
3. `final-index.md`：run 概览、交付路径、验证摘要、剩余风险。  
4. `next-iteration-context.md`：下一步、待确认、勿自动推进区。  
5. `state.md` §6 补全索引；`current_stage: close`。

## 产出路径

`.workflow/runs/<run-id>/stages/curate/{traceability-matrix,deviations-summary,final-index,next-iteration-context}.md`

## Gate

- [ ] 主要设计点有映射；偏差有说明；`state.md` 已关闭 run

## 失败

大量 missing → 不标 close，回实现或补记录。

## 矩阵最小表头

`| design_ref | module | code_path | test_path | status | deviation |`
