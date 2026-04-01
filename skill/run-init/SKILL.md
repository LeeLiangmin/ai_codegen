---
name: run-init
description: Use when starting a design-driven implementation run and need `.workflow/runs/<run-id>/` layout and initial `state.md` before any other pipeline stage
---

# run-init

创建 `.workflow/runs/<run-id>/`、初始 `state.md`、占位 `run-brief.md` 及 `stages/*`、`slices/`。

## 输入

`run_id`、`design_doc`（须已存在）、`name`、`objective`。

## 步骤

1. 建目录：`.workflow/runs/<run-id>/`、`slices/`、`stages/{intake,normalize,plan,implement-verify,integrate,curate}/`；`.workflow/docs/{design,implementation-plan}/`（若无）。
2. 按下方模板写 `state.md`（`status: created`，`current_stage: init`，§3 各 stage `pending`）。
3. 按下方模板写 `run-brief.md`（各节「无」= 本 run 不附加约束）。

## 产出

`state.md`、`run-brief.md`、空目录骨架。

## Gate

- [ ] 设计文件存在；`state.md` 无未替换占位符；`run_brief` 已写入 §6。

## 异常

目录已存在 → 询问是否覆盖。设计不存在 → 停止。

## Template：`state.md`

将 `<填入>` 替换为实际值：

```markdown
# Run 状态文件

## 1. 基本信息

- run_id: <填入>
- name: <填入>
- objective: <填入>
- design_doc: <填入>
- created_at: <填入>
- updated_at: <填入>
- status: created

## 2. 当前阶段

- current_stage: init
- current_slice: —
- stage_owner: AI
- retry_count: 0

## 3. 阶段结果摘要

| stage | status | input | output | checks | notes |
| --- | --- | --- | --- | --- | --- |
| intake | pending | | | | |
| normalize | pending | | | | |
| plan | pending | | | | |
| slice | pending | | | | |
| implement | pending | | | | |
| verify | pending | | | | |
| integrate | pending | | | | |
| curate | pending | | | | |
| close | pending | | | | |

## 4. 切片状态

| slice_id | title | status | dependency | verify_status | deviation | notes |
| --- | --- | --- | --- | --- | --- | --- |
| | | pending | | pending | none | |

## 5. 风险与阻塞

- 当前风险：无
- 当前阻塞：无
- 是否需要人工介入：no
- 人工介入原因：—

## 6. 产物索引

- run_brief: `.workflow/runs/<run-id>/run-brief.md`
- implementation_plan: —
- slices_index: —
- verification_reports: —
- traceability_matrix: —
- final_index: —

## 7. 恢复策略

- 最近成功阶段：init
- 可恢复起点：intake
- 恢复前置条件：—
- 恢复说明：—
```

## Template：`run-brief.md`

```markdown
# Run brief（本次 run 专用约束）

**可插拔**：除说明外各节为「无」或空则本 run 不附加相对 evergreen 设计的额外约束。

## 范围与裁剪

无

## 硬约束（必须满足）

无

## 非目标（本 run 不做）

无

## 验收优先级

无

## 与设计文档冲突时

须在阶段报告中显式记录；必要时至 `risks.md` 与人工确认后再推进。
```
