---
name: design-normalize
description: Use when intake concluded to allow normalization and you need a single structured `*.normalized.md` plus normalization and unresolved-items reports
---

# design-normalize

## Overview

将设计资料统一收敛为结构化 Markdown 设计文档，使其满足 AI 实施要求。

## When to Use

intake 通过后执行。

前置条件：
- `.workflow/runs/<run-id>/stages/intake/intake-report.md` 结论为允许进入 normalize
- `.workflow/runs/<run-id>/state.md` 中 §3 阶段表 **intake** 行 `status` 为 `done`（完成）；**`current_stage`** 通常为 `intake`

## Input

| 参数 | 必填 | 说明 |
|------|------|------|
| 原始设计文档 | 是 | `.workflow/docs/design/` 下的 Markdown 文件 |
| 补充资料 | 否 | PDF、口头说明、会议纪要等 |
| intake 报告 | 是 | `.workflow/runs/<run-id>/stages/intake/intake-report.md` |
| `state.md` 路径 | 是 | `.workflow/runs/<run-id>/state.md` |
| `run-brief.md` | 否 | `.workflow/runs/<run-id>/run-brief.md`；有实质内容时，归一化须**尊重**其范围/硬约束/非目标，**不**将 brief 全文并入 `.normalized.md`（evergreen 与本次 run 约束分离） |

## Procedure

1. **读取输入**：加载原始设计文档和 intake 报告。若 `run-brief.md` 存在且含实质内容（见 [design-intake](../design-intake/SKILL.md) 对「实质内容」的判定），一并加载；归一化时不得扩展至 brief 声明的「非目标」，不得弱化 brief 中的硬约束表述（冲突留在 `normalization-report.md` / `unresolved-items.md`）。
2. **识别待处理项**：从 intake 报告中提取所有标记为 ⚠️（不完整）和 ❌（缺失）的章节，以及待确认项。
3. **合并补充信息**：将补充资料（PDF、口头说明等）中的相关内容整合到设计文档对应章节中。
4. **标准化章节结构**：按设计文档标准结构标准化章节（完整结构定义见 [design-intake § Template](../design-intake/SKILL.md#template)）。确保所有 12 个标准章节存在且顺序正确。
5. **补齐缺失内容**：根据上下文和补充资料，补齐缺失的术语定义、约束描述、接口细节、验收标准等。
6. **消除模糊表述**：将模糊表述转为明确定义。无法自动决策的项标记为 `[待确认]`，不伪造内容。
7. **生成规范化设计稿**：输出 `.workflow/docs/design/<name>.normalized.md`，确保满足标准结构。
8. **生成报告与待确认清单**：
   - `.workflow/runs/<run-id>/stages/normalize/normalization-report.md` — 记录所有修改、补充、标准化动作
   - `.workflow/runs/<run-id>/stages/normalize/unresolved-items.md` — 列出所有 `[待确认]` 项
9. **更新状态文件**：更新 `.workflow/runs/<run-id>/state.md`：
   - `current_stage` → `normalize`
   - normalize 行的 `status` → `done` 或 `failed`
   - `updated_at` → 当前时间

## Output

- `.workflow/docs/design/<name>.normalized.md` — 规范化设计稿
- `.workflow/runs/<run-id>/stages/normalize/normalization-report.md` — 规范化报告
- `.workflow/runs/<run-id>/stages/normalize/unresolved-items.md` — 待确认项清单
- 更新 `.workflow/runs/<run-id>/state.md`

## Quality Gate

- [ ] 输出文档满足设计文档标准结构（见 [design-intake § Template](../design-intake/SKILL.md#template) 中的设计文档结构参考）
- [ ] 所有 12 个标准章节存在且内容充分
- [ ] 待确认项已全部标记为 `[待确认]` 并收录到 `unresolved-items.md`
- [ ] intake 报告中标记的所有问题均已处理（补齐或标记为待确认）
- [ ] 规范化报告完整记录了所有修改动作
- [ ] `state.md` 已更新

## Failure Handling

- **无法自动补齐的关键信息**：标记为 `[待确认]`，不伪造内容。若待确认项过多（超过总章节的 50%），建议回到 intake 阶段重新评估。
- **补充资料与原设计冲突**：在 `normalization-report.md` 中列出冲突点，标注双方内容，建议人工决策。不自行选择任一方。
- **大量关键信息缺失**：当模块设计、接口设计、数据设计中任一完全缺失且无补充资料可参照时，将 normalize 状态设为 `failed`，建议回到 intake 阶段，由人工补充设计后重新流转。

## Template

本阶段不重复嵌入设计文档标准结构模板。

规范化时请参照 [design-intake § Template](../design-intake/SKILL.md#template) 中的**设计文档结构参考**，确保输出文档严格遵循该结构。
