---
name: design-normalize
description: Use when intake concluded to allow normalization and you need a single structured `*.normalized.md` plus normalization and unresolved-items reports
---

# design-normalize

把设计收敛为 `.workflow/docs/design/<name>.normalized.md`，并写 `normalization-report.md`、`unresolved-items.md`。

## 前置

intake 结论为允许进入 normalize；`state.md` intake 为 done。

## 输入

原始设计、intake 报告、可选补充材料、`state.md`；可选 `run-brief`（实质内容时：不得扩展至 brief 非目标，不得弱化硬约束；冲突写入报告）。

## 步骤

1. 合并补充信息；按 intake 未决项补齐或标 `[待确认]`（不编造）。  
2. 输出 `*.normalized.md`（结构清晰、可实施；章节顺序可与 intake 表对齐）。  
3. `normalization-report.md`：改了什么。`unresolved-items.md`：所有 `[待确认]`。  
4. `state.md`：`current_stage: normalize`，该行 done/failed。

## Gate

- [ ] 关键章节可实施；待确认已列出；`state.md` 已更新

## 失败

关键信息全无且无法标记待确认 → normalize `failed`，回 intake/人工。
