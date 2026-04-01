---
name: run-status
description: Use when you need to interpret .workflow/runs/<run-id>/state.md for a design-driven run, summarize progress, and get the recommended next skill invocation for resume (read-only; does not advance the pipeline)
---

# run-status

## Overview

本 skill 为**工具型**步骤：**不写入业务状态、不替代各阶段 skill 对 `state.md` 的更新**，只读取并解释当前 run 的状态，输出结构化摘要与**续跑时建议打开的下一个 `skill/<name>/SKILL.md`**。

权威数据源：`.workflow/runs/<run-id>/state.md`（结构与模板见 [run-init/SKILL.md § Template](../run-init/SKILL.md#template)）。

## When to Use

- 新会话接手仓库，需要知道「这个 run 做到哪一步、下一步该执行谁」
- 失败后恢复，需要确认应从哪一 skill 重试
- 多 run 并存时，确认正在讨论的是哪一个 `run_id`

## Input

| 参数 | 必填 | 说明 |
|------|------|------|
| `state.md` 路径 | 二选一 | `.workflow/runs/<run-id>/state.md` 的明确路径 |
| 项目根 + `run_id` | 二选一 | 由 `run_id` 拼出 `.workflow/runs/<run-id>/state.md` |
| 仅项目根 | 否 | 若未给 `run_id`：列出 `.workflow/runs/` 下子目录中的 `state.md`，请用户确认或选最近修改的 run（说明选择依据） |

## Procedure

1. **定位 `state.md`**：按输入解析路径；若不存在则报错并提示先执行 `run-init`。
2. **读取 §1–§7**：解析基本信息、`current_stage`、`current_slice`、§3 阶段表、§4 切片表、§5 阻塞、§6 产物索引、§7 恢复策略（若存在）。
3. **读取 run-brief（若可解析）**：若 §6 `run_brief` 或默认路径 `.workflow/runs/<run-id>/run-brief.md` 存在，且除模板说明外**含有实质内容**（任一节非空且非仅「无」），在摘要中增加 **「本次 run 约束要点」**（3～5 条bullet，摘自范围/硬约束/非目标）；否则写一句「run-brief 未启用或未填写」。
4. **生成「状态摘要」**（见下方输出模板）：run 级 `status` 与 `current_stage`、阶段表中非 pending 的行、切片表中未完成或失败项、§5 是否要求人工介入。
5. **推导「续跑建议」**（见下方路由规则）：给出**唯一主推荐**的下一步 skill；若存在并列选项（例如多个可并行切片），列出并说明需人工选 slice；调用示例中附带 `run-brief.md` 路径（若存在）供下一阶段使用。
6. **（可选）** 若用户要求落盘审计：将本次摘要写入 `.workflow/runs/<run-id>/stages/plan/run-status.md`（带时间戳）；**默认不写文件**，仅在对话中输出即可。

## Output

按以下结构输出（可直接复制给执行者或下一会话）：

```markdown
## Run 状态摘要
- run_id / name / status / current_stage / current_slice
- 设计文档路径（§1 design_doc）
- 本次 run 约束要点（来自 `run-brief.md`，若已启用；否则注明未启用）
- 阶段表要点：各 stage 的 status 一行摘要
- 切片表要点：未完成或 verify 未通过的 slice_id 列表
- 阻塞与人工介入（§5）

## 续跑建议
- **下一步 skill**：`skill/<name>/SKILL.md`
- **建议调用示例**：`请按照 skill/<name>/SKILL.md 执行，…`（补全所需输入路径，如 `state.md`、设计文档、切片 id）
- **若处于失败重试**：指出应重试同一 skill 还是回退到上一阶段（对照 §7 与阶段/切片失败项）
- **若 run 已结束**：`status` 为 completed 且 `current_stage` 为 `close`（或 §3 表明 close 已完成）→ 说明无需续跑；新工作请 `run-init` 新 run
```

## 路由规则（推荐主路径）

以下按**常见约定**合并 §3 与 §4；若与 `current_stage` 不一致，**以阶段表 + 切片表为准**，并在摘要中注明矛盾及可能原因（例如手工改过 `state.md`）。

| 情形 | 下一步 skill | 备注 |
|------|----------------|------|
| §3 `intake` 仍为 pending，或结论为需补充 / intake 失败 | `design-intake` | 携带 `.workflow/docs/design/` 下设计文档与 `state.md` |
| `intake` 已完成，`normalize` 未完成或失败 | `design-normalize` | 需 intake 报告允许进入 normalize |
| `normalize` 已完成，`plan` 未完成 | `design-to-plan` | 输入 `.normalized.md` |
| `plan` 已完成，§4 尚无真实切片或 `slice` 行未完成 | `plan-to-slices` | 输入实现计划与 backlog |
| 切片已定义，存在 `pending` / `running` / `blocked` 或刚实现完待验的切片 | `slice-implement` 或 `slice-verify` | 有未验证实现 → 先 `slice-verify`；下一待做切片 → `slice-implement`（带 `slice-NNN.md`） |
| 所有切片 `verify_status` 均为 passed，集成未做或失败 | `integration-verify` | `current_stage` 可能为 `integrating` |
| 集成已通过，`curate` / `close` 未完成 | `result-curate` | |
| run 已完成 | （无） | 仅摘要，不调用流水线 skill |

**切片环内细化**（§4 有数据时）：

- 找到**按依赖顺序**第一个未完成切片：status 为 `pending` / `blocked`（且依赖已满足）→ **`slice-implement`**
- 某切片 status 为 `implemented`（或等价「待验证」）→ **`slice-verify`**
- `slice-verify` 失败 → 回到 **`slice-implement`** 修复同一切片后再次 `slice-verify`

若无法从表中判定（例如 §4 为空表占位符），在「续跑建议」中写明**缺失字段**，并建议人工补全 `state.md` 或重新执行能产生该表的 skill。

## Quality Gate（本 skill 自身）

- [ ] 已明确 `run_id` 与 `state.md` 路径
- [ ] 摘要与 §1–§5 一致，无臆造字段
- [ ] 续跑建议指向仓库内真实存在的 `skill/<name>/SKILL.md`
- [ ] 若存在阻塞或人工介入，已在摘要中突出，不盲目给出自动续跑步骤

## Failure Handling

| 场景 | 处理 |
|------|------|
| 多个 run，用户未指定 | 列出 run_id + `updated_at`（若可读），请用户指定或采用最近修改 |
| `state.md` 损坏或缺节 | 记录缺失章节，建议从最近「可恢复起点」（§7）或备份恢复 |
| 阶段表与切片表矛盾 | 输出两种解读可能，**优先建议人工核对**后再执行下一 skill |
