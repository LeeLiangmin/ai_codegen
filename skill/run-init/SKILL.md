---
name: run-init
description: Use when starting a design-driven implementation run and need `.workflow/runs/<run-id>/` layout and initial `state.md` before any other pipeline stage
---

# run-init

## Overview

为一次设计驱动实现创建标准 run 目录结构与初始状态文件。

## When to Use

在开始任何设计实现任务之前执行。

前置条件：
- 设计文档已准备好（Markdown 格式）
- 已确定本次 run 的标识与目标

## Input

| 参数 | 必填 | 说明 |
|------|------|------|
| `run_id` | 是 | 运行标识，如 `my-project-run-001` |
| `design_doc` | 是 | 设计文档路径，如 `.workflow/docs/design/xxx.md` |
| `name` | 是 | 项目名称 |
| `objective` | 是 | 目标描述 |

## Procedure

1. **校验输入**：确认 `run_id`、`design_doc`、`name`、`objective` 均已提供，且设计文档路径对应的文件存在。
2. **创建 run 目录结构**：
   - `.workflow/runs/<run-id>/`
   - `.workflow/runs/<run-id>/slices/`
   - `.workflow/runs/<run-id>/stages/intake/`
   - `.workflow/runs/<run-id>/stages/normalize/`
   - `.workflow/runs/<run-id>/stages/plan/`（可选审计等落盘；默认可空）
   - `.workflow/runs/<run-id>/stages/implement-verify/`
   - `.workflow/runs/<run-id>/stages/integrate/`
   - `.workflow/runs/<run-id>/stages/curate/`
3. **创建 `.workflow/docs/design/` 目录**（如不存在）。
4. **创建 `.workflow/docs/implementation-plan/` 目录**（如不存在）。
5. **生成状态文件**：根据下方「Template」中 `state.md` 模板生成 `.workflow/runs/<run-id>/state.md`，将 `run_id`、`name`、`objective`、`design_doc`、`created_at`、`updated_at` 填入对应位置，`status` 设为 `created`；§6 产物索引中 `run_brief` 指向 `.workflow/runs/<run-id>/run-brief.md`。
6. **生成 run-brief（可插拔占位）**：根据下方「`run-brief.md` 模板」创建 `.workflow/runs/<run-id>/run-brief.md`。除标题与说明外各节默认为「无」时表示**本 run 不启用额外约束**；需要时由人工或后续会话填写，无需改流水线顺序。
7. **确认结果**：检查所有目录和文件均已成功创建。

## Output

- `.workflow/runs/<run-id>/state.md` — 初始状态文件
- `.workflow/runs/<run-id>/run-brief.md` — 本次 run 专用约束（可插拔；默认「无」即不生效）
- `.workflow/runs/<run-id>/slices/` — 切片目录（空）
- `.workflow/runs/<run-id>/stages/*/` — 各阶段产出目录（空）
- `.workflow/docs/design/` — 设计文档目录
- `.workflow/docs/implementation-plan/` — 实现计划目录

## Quality Gate

- [ ] 目录结构完整：`.workflow/runs/<run-id>/`、`slices/`、`stages/intake/`、`stages/normalize/`、`stages/plan/`、`stages/implement-verify/`、`stages/integrate/`、`stages/curate/`、`.workflow/docs/design/`、`.workflow/docs/implementation-plan/` 均存在
- [ ] `run-brief.md` 已创建且路径已写入 `state.md` §6 `run_brief`
- [ ] `state.md` 内容正确：所有 `<填入>` 占位符已替换为实际值
- [ ] `state.md` 中 `status` 为 `created`，`current_stage` 为 `init`
- [ ] 所有阶段状态均为 `pending`

## Failure Handling

- **目录已存在**：提示用户确认是否覆盖。若用户确认，清空后重新创建；若用户拒绝，终止并保留现有内容。
- **设计文档不存在**：终止并提示用户先准备设计文档。

## Template

以下为 `state.md` 的完整模板，执行时将 `<填入>` 替换为实际值：

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

- run_brief: `.workflow/runs/<run-id>/run-brief.md`（可插拔；与设计文档分离的本次 run 约束）
- implementation_plan: —
- slices_index: —
- verification_reports: —（有切片验证产出后可填 `.workflow/runs/<run-id>/stages/implement-verify/`）
- traceability_matrix: —（`result-curate` 后可填 `.workflow/runs/<run-id>/stages/curate/traceability-matrix.md`）
- final_index: —（`result-curate` 后可填 `.workflow/runs/<run-id>/stages/curate/final-index.md`）

## 7. 恢复策略

- 最近成功阶段：init
- 可恢复起点：intake
- 恢复前置条件：—
- 恢复说明：—
```

## 9. `run-brief.md` 模板

执行 `run-init` 时在 `.workflow/runs/<run-id>/run-brief.md` 写入以下初始内容（`<run-id>` 替换为实际 id）：

```markdown
# Run brief（本次 run 专用约束）

**可插拔**：除本说明外，各节仅为「无」或留空时，表示本 run **不附加**相对 evergreen 设计文档的额外约束；各阶段 skill 仍应知晓该文件路径。填写实质内容后，自 `design-intake` 起须与设计文档一并阅读，并在计划/切片中落实或记入风险。

## 范围与裁剪

无

## 硬约束（必须满足）

无

## 非目标（本 run 不做）

无

## 验收优先级

无

## 与设计文档冲突时

未指定时：须在对应阶段报告中显式记录冲突，**不擅自裁定**；必要时至 `.workflow/docs/implementation-plan/risks.md` 与人工确认后再推进。
```
